#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifica a secao de analise ontologica do MPO (checklist do ticket 10).

Uso: python tools/verification/verificar_analise_ontologica.py [diretorio-do-artigo]

O texto da secao 5 mora em `artifacts/paper/secoes/05-analise-ontologica.md` e e
o unico lugar do repositorio onde as nove deficiencias aparecem com o **traco**
ate o ponto do MPO que as permitiu. Este verificador le esse texto como
terceiro — sem importar de `tools/generation/` e sem reusar o codigo que
produziu os modelos — e confronta cada afirmacao dele com a fonte que a
sustenta:

  1. a secao existe, o esqueleto aponta para ela e o orcamento de paginas que o
     esqueleto declara para a secao 5 e respeitado. A medida nao e estimada: o
     texto e portado para o template SBC e compilado, e o que se compara e a
     pagina inteira mais a fracao ocupada na ultima;
  2. as nove deficiencias estao na Tabela 1, cada uma com classificacao e com a
     coluna do traco preenchida, e cada codigo A1-A9 reaparece na prosa;
  3. cada classificacao cai na tipologia de Representation Theory (*overload*,
     *redundancy*, *excess*, *deficit*) ou esta marcada como fora dela — e, se
     esta, a prosa justifica por que a tipologia nao se aplica;
  4. **toda aspa curva do texto e citacao verbatim da fonte.** Cada uma e
     procurada, com espacos normalizados, em `sources/dissertation/`. E o que
     torna o traco falsificavel: uma citacao inventada reprova aqui;
  5. a afirmacao de que o acronimo CRUD nao ocorre no MPO nem na conceituacao e
     conferida contra os proprios arquivos da fonte;
  6. todo identificador entre crases que nomeia classe do modelo existe no
     baseline ou na rodada 2 — o texto nao pode citar construto que nenhum dos
     dois tem;
  7. os numeros citados batem com os artefatos: a divergencia da QC7 e recontada
     do `.csv`, o glossario de 53 termos vem da fonte, as nove regras e o zero do
     plugin vem dos relatorios;
  8. os achados fora de A1-A9 estao todos contabilizados: o total declarado na
     secao e a soma das disposicoes conferem com os codigos B registrados nos
     artefatos da ontologia;
  9. o texto declara a subdeterminacao como resultado e o limite n=1, mostra um
     par antes/depois, fundamenta cada bloco em referencia da UFO ou da
     Representation Theory, e nao cita chave que falte no `.bib`;
 10. nada atribui as deficiencias ao MPO em linguagem natural, nao ha mencao
     identificadora, primeira pessoa nem resquicio da defesa de ontologia leve.

Sai com codigo 1 se qualquer verificacao falhar.
"""

from __future__ import annotations

import csv
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

ARTIGO_PADRAO = Path("artifacts/paper")
ONTOLOGIA = Path("artifacts/ontology")
FONTE = Path("sources/dissertation")

NOME_SECAO = "05-analise-ontologica.md"

# Os arquivos da fonte contra os quais toda citacao curva e conferida. Sao
# somente-leitura: o repositorio nunca os edita.
FONTES = (
    FONTE / "conteudo" / "fundamentacao.tex",
    FONTE / "conteudo" / "resultados.tex",
    FONTE / "conteudo" / "metodologia.tex",
    FONTE / "conteudo" / "introducao.tex",
    FONTE / "conteudo" / "conclusao.tex",
    FONTE / "postextuais" / "apendices.tex",
)

# Onde o MPO e a conceituacao dele estao descritos. A afirmacao de que o
# acronimo CRUD nao ocorre neles e conferida aqui, e so aqui: o capitulo de
# resultados descreve a formalizacao, onde CrudManager aparece de fato.
FONTES_DO_MPO = (
    FONTE / "conteudo" / "fundamentacao.tex",
    FONTE / "postextuais" / "apendices.tex",
)

CODIGOS = [f"A{n}" for n in range(1, 10)]

TIPOLOGIA = ("overload", "redundancy", "excess", "deficit")
MARCA_FORA = "fora:"

# Fundamentacao aceitavel para uma correcao: UFO/OntoUML ou Representation
# Theory. Preferencia de modelagem nao e argumento.
CHAVES_FUNDAMENTO = (
    "guizzardi2005ontological",
    "guizzardi2008grounding",
    "guizzardi2022ufo",
    "wand1993ontological",
    "wand1995deep",
    "weber1997ontological",
    "recker2011ontological",
)

# Atribuir a deficiencia ao MPO em linguagem natural e a alegacao falsificavel
# que o ticket manda evitar: o MPO e prosa, e nao contem os construtos.
ATRIBUICOES_PROIBIDAS = (
    r"defici[êe]ncias?\s+do\s+MPO",
    r"defeitos?\s+do\s+MPO",
    r"erros?\s+do\s+MPO",
    r"falhas?\s+do\s+MPO",
    r"o\s+MPO\s+cont[ée]m\s+`",
    r"o\s+MPO\s+declara\s+software",
)

TERMOS_IDENTIFICADORES = (
    "josé ferreira",
    "santos júnior",
    "santos junior",
    "ivaldir",
    "hermano",
    "universidade de pernambuco",
    "poli.br",
    "upe.br",
    "github.com/",
)

LEVE = (r"ontologia\s+leve", r"lightweight\s+ontology")

# «nos» sem acento e preposicao em portugues, e por isso fica de fora.
PRIMEIRA_PESSOA = re.compile(
    r"\b(nós|nosso|nossa|nossos|nossas|realizamos|propomos|apresentamos|"
    r"desenvolvemos|analisamos|conduzimos)\b",
    re.IGNORECASE,
)

UNIDADES = {
    "um": 1,
    "uma": 1,
    "dois": 2,
    "duas": 2,
    "três": 3,
    "tres": 3,
    "quatro": 4,
    "cinco": 5,
    "seis": 6,
    "sete": 7,
    "oito": 8,
    "nove": 9,
}

DEZENAS = {
    "dez": 10,
    "onze": 11,
    "doze": 12,
    "treze": 13,
    "quatorze": 14,
    "catorze": 14,
    "quinze": 15,
    "dezesseis": 16,
    "dezessete": 17,
    "dezoito": 18,
    "dezenove": 19,
    "vinte": 20,
    "trinta": 30,
    "quarenta": 40,
    "cinquenta": 50,
    "sessenta": 60,
    "setenta": 70,
    "oitenta": 80,
    "noventa": 90,
}


def _numeral(palavras: str) -> int | None:
    """Le «oito» ou «vinte e três» — o texto escreve numero pequeno por extenso."""
    partes = [p for p in palavras.lower().split() if p != "e"]
    if len(partes) == 1:
        return UNIDADES.get(partes[0]) or DEZENAS.get(partes[0])
    if len(partes) == 2 and partes[0] in DEZENAS and partes[1] in UNIDADES:
        return DEZENAS[partes[0]] + UNIDADES[partes[1]]
    return None


def _por_extenso(valor: int) -> list[str]:
    """As formas escritas possiveis de um numero, para procurar no texto."""
    formas = [str(valor)]
    for palavra, numero in {**UNIDADES, **DEZENAS}.items():
        if numero == valor:
            formas.append(palavra)
    if 20 < valor < 100 and valor % 10:
        dezena = next(p for p, n in DEZENAS.items() if n == valor - valor % 10)
        formas += [f"{dezena} e {p}" for p, n in UNIDADES.items() if n == valor % 10]
    return formas


class Resultado:
    def __init__(self) -> None:
        self.falhas: list[str] = []
        self.checagens = 0

    def exigir(self, condicao: bool, mensagem: str) -> bool:
        self.checagens += 1
        if not condicao:
            self.falhas.append(mensagem)
        return bool(condicao)


def _ler(caminho: Path) -> str:
    try:
        return caminho.read_text(encoding="utf-8")
    except OSError:
        return ""


def _sem_comentarios(texto: str) -> str:
    """O texto que vai para o artigo: sem os comentarios HTML de bastidor."""
    return re.sub(r"<!--.*?-->", "", texto, flags=re.S)


def _normalizar(texto: str) -> str:
    """Deixa comparavel um trecho de LaTeX e um trecho de Markdown.

    Tira comandos de formatacao (`\\textbf{...}` e afins), colapsa espaco e
    quebra de linha, e ignora caixa — uma citacao pode comecar no meio de uma
    frase da fonte.
    """
    texto = re.sub(r"\\[a-zA-Z]+\s*", "", texto)
    texto = texto.replace("{", "").replace("}", "").replace("~", " ")
    texto = texto.replace("``", '"').replace("''", '"')
    texto = unicodedata.normalize("NFC", texto)
    return re.sub(r"\s+", " ", texto).strip().lower()


def _blocos(texto: str) -> tuple[str, list[str], list[str]]:
    """Separa o texto em (prosa, linhas da tabela, linhas da listagem)."""
    tabela: list[str] = []
    listagem: list[str] = []
    prosa: list[str] = []
    dentro_da_listagem = False
    for linha in texto.splitlines():
        if linha.startswith("```"):
            dentro_da_listagem = not dentro_da_listagem
            continue
        if dentro_da_listagem:
            listagem.append(linha)
        elif linha.strip().startswith("|"):
            tabela.append(linha.strip())
        else:
            prosa.append(linha)
    return "\n".join(prosa), tabela, listagem


# --------------------------------------------------------------------------
# 1. o texto, o plano e o orcamento de paginas
# --------------------------------------------------------------------------


def _orcamento_da_secao_5(esqueleto: str) -> float | None:
    for linha in esqueleto.splitlines():
        if linha.strip().startswith("| 5 |"):
            colunas = [c.strip() for c in linha.strip().strip("|").split("|")]
            try:
                return float(colunas[-1].replace(",", "."))
            except ValueError:
                return None
    return None


def _para_latex(markdown: str) -> str:
    """Porte grosseiro para LaTeX, so para medir. O porte real e do ticket 13."""

    def inline(t: str) -> str:
        t = re.sub(r"`([^`]*)`", lambda m: r"\texttt{" + m.group(1).replace("_", r"\_") + "}", t)
        t = re.sub(r"\*\*([^*]*)\*\*", lambda m: r"\textbf{" + m.group(1) + "}", t)
        t = re.sub(r"\*([^*]*)\*", lambda m: r"\textit{" + m.group(1) + "}", t)
        t = t.replace("&", r"\&").replace("%", r"\%").replace("#", r"\#")
        t = t.replace("«", "<<").replace("»", ">>")
        t = t.replace("\u201c", "``").replace("\u201d", "''")
        t = re.sub(r"\[([a-z0-9, ]+)\]", lambda m: r"\cite{" + m.group(1) + "}", t)
        return t.replace("\n", " ")

    corpo: list[str] = []
    for bloco in _sem_comentarios(markdown).split("\n\n"):
        b = bloco.strip()
        if not b:
            continue
        if b.startswith("# "):
            corpo.append(r"\section{" + inline(b[2:]) + "}")
        elif b.startswith("## "):
            corpo.append(r"\subsection{" + inline(b[3:]) + "}")
        elif b.startswith("```"):
            dentro = b.split("\n", 1)[1].rsplit("```", 1)[0]
            corpo.append("\\begin{verbatim}\n" + dentro.rstrip() + "\n\\end{verbatim}")
        elif b.lstrip().startswith("|"):
            linhas = []
            for l in b.split("\n"):
                celulas = [c.strip() for c in l.strip().strip("|").split("|")]
                if set("".join(celulas)) <= set("-: "):
                    continue
                linhas.append(" & ".join(inline(c) for c in celulas) + r" \\ \hline")
            corpo.append(
                r"\begin{table}[h]\footnotesize\begin{tabular}"
                r"{|p{0.5cm}|p{4.6cm}|p{2.6cm}|p{4.6cm}|}\hline"
                "\n" + "\n".join(linhas) + "\n\\end{tabular}\\end{table}"
            )
        else:
            corpo.append(inline(b))
    preambulo = "\n".join(
        (
            r"\documentclass[12pt]{article}",
            r"\usepackage{sbc-template}",
            r"\usepackage{graphicx,url}",
            r"\usepackage[utf8]{inputenc}",
            r"\usepackage[T1]{fontenc}",
            r"\usepackage[brazilian]{babel}",
            r"\sloppy",
            r"\begin{document}",
            "",
        )
    )
    fecho = "\n" + r"\typeout{PAGINAFINAL \the\pagetotal\space de \the\textheight}" + "\n"
    return preambulo + "\n\n".join(corpo) + fecho + r"\end{document}" + "\n"


def _medir_paginas(diretorio: Path, markdown: str) -> float | None:
    """Compila o texto no template SBC e devolve paginas inteiras + fracao."""
    if shutil.which("pdflatex") is None:
        return None
    with tempfile.TemporaryDirectory() as tmp:
        destino = Path(tmp)
        shutil.copy(diretorio / "sbc-template.sty", destino / "sbc-template.sty")
        (destino / "medida.tex").write_text(_para_latex(markdown), encoding="utf-8")
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "medida.tex"],
            cwd=destino,
            capture_output=True,
        )
        log = (destino / "medida.log").read_text(encoding="utf-8", errors="ignore")
    paginas = re.findall(r"\((\d+) pages?", log)
    fim = re.search(r"PAGINAFINAL ([\d.]+)pt de ([\d.]+)pt", log)
    if not paginas or not fim:
        return None
    return (int(paginas[-1]) - 1) + float(fim.group(1)) / float(fim.group(2))



# --------------------------------------------------------------------------
# medida de paginas: o porte do ticket 13
# --------------------------------------------------------------------------

# Blocos do `artigo.tex`, na ordem em que aparecem. O porte do ticket 13 e' a
# medida definitiva de paginacao — o `_para_latex` acima e' um porte grosseiro,
# feito quando o `.tex` real ainda nao existia, e erra por nao flutuar tabelas
# nem quebrar celulas. Quando o porte existe e compila, e' ele que vale; o
# grosseiro so' sobrevive como reserva para quem rodar isto sem o ticket 13
# pronto.
BLOCOS_DO_PORTE = (
    "01", "02", "03", "04", "05", "06", "07", "08", "09",
    "ia", "referencias", "apendice",
)


def _medir_no_porte(diretorio: Path) -> dict[str, float] | None:
    """Compila `artigo.tex` com marcas e devolve as paginas de cada bloco.

    Le o artigo portado como terceiro: injeta um `\\typeout` antes de cada
    cabecalho de secao numa **copia** e conta a distancia entre marcas. Devolve
    `None` — e o chamador cai na estimativa — quando nao ha `pdflatex`, quando o
    porte ainda nao foi gerado ou quando a compilacao nao fecha.
    """
    if shutil.which("pdflatex") is None:
        return None
    artigo = diretorio / "artigo.tex"
    if not artigo.exists() or not (diretorio / "secoes-tex").is_dir():
        return None

    marca = r"\typeout{MARCA-\thepage-\the\pagetotal-\the\textheight}"
    fonte = artigo.read_text(encoding="utf-8")
    fonte = re.sub(r"(?m)^(\\section\*?\{)", lambda m: marca + "\n" + m.group(1), fonte)
    for ancora in (r"\bibliographystyle{sbc}", r"\input{apendice-sparql}", r"\end{document}"):
        if ancora not in fonte:
            return None
        fonte = fonte.replace(ancora, marca + "\n" + ancora, 1)

    with tempfile.TemporaryDirectory() as tmp:
        destino = Path(tmp)
        for item in diretorio.iterdir():
            if item.name in {"artigo.tex", "medida.tex"}:
                continue
            if item.is_dir():
                shutil.copytree(item, destino / item.name)
            else:
                shutil.copy(item, destino / item.name)
        (destino / "medida.tex").write_text(fonte, encoding="utf-8")
        ambiente = {**os.environ, "max_print_line": "1000"}
        for passo in ("pdflatex", "bibtex", "pdflatex", "pdflatex"):
            argumentos = (
                [passo, "medida"]
                if passo == "bibtex"
                else [passo, "-interaction=nonstopmode", "medida.tex"]
            )
            subprocess.run(argumentos, cwd=destino, capture_output=True, env=ambiente)
        log = (destino / "medida.log").read_text(encoding="utf-8", errors="ignore")

    marcas = re.findall(r"MARCA-(\d+)-([\d.]+)pt-([\d.]+)pt", log)
    if len(marcas) != len(BLOCOS_DO_PORTE) + 1:
        return None
    posicoes = [(int(p) - 1) + float(t) / float(h) for p, t, h in marcas]
    medidas = {"frontmatter": posicoes[0], "total": posicoes[-1]}
    for i, bloco in enumerate(BLOCOS_DO_PORTE):
        medidas[bloco] = posicoes[i + 1] - posicoes[i]
    return medidas

def verificar_plano(diretorio: Path, texto: str, res: Resultado) -> None:
    esqueleto = _ler(diretorio / "esqueleto.md")
    res.exigir(
        NOME_SECAO in esqueleto,
        f"o esqueleto nao aponta para secoes/{NOME_SECAO}: o ticket 13 nao acha o texto",
    )
    orcamento = _orcamento_da_secao_5(esqueleto)
    if not res.exigir(orcamento is not None, "orcamento da secao 5 ausente no esqueleto"):
        return
    porte = _medir_no_porte(diretorio)
    if porte is not None:
        paginas, origem = porte["05"], "porte do ticket 13"
    else:
        paginas, origem = _medir_paginas(diretorio, texto), "porte provisorio"
    if paginas is None:
        print("AVISO: pdflatex ausente ou compilacao falhou; paginacao nao medida")
        return
    print(
        f"paginas medidas: {paginas:.2f} (orcamento do esqueleto: {orcamento:.2f}) "
        f"[{origem}]"
    )
    res.exigir(
        paginas <= orcamento,
        f"a secao mede {paginas:.2f} paginas e o esqueleto lhe da {orcamento:.2f}",
    )


# --------------------------------------------------------------------------
# 2 e 3. as nove deficiencias, sua classificacao e seu traco
# --------------------------------------------------------------------------


def verificar_tabela(texto: str, res: Resultado) -> None:
    prosa, tabela, _ = _blocos(_sem_comentarios(texto))
    linhas = {}
    for linha in tabela:
        celulas = [c.strip() for c in linha.strip("|").split("|")]
        if len(celulas) >= 4 and re.fullmatch(r"A[1-9]", celulas[0]):
            linhas[celulas[0]] = celulas
    for codigo in CODIGOS:
        if not res.exigir(codigo in linhas, f"{codigo} ausente da Tabela 1"):
            continue
        celulas = linhas[codigo]
        res.exigir(
            len(celulas) == 4 and all(celulas[1:]),
            f"{codigo}: a Tabela 1 tem celula vazia — deficiencia, classificacao e traco",
        )
        classificacao = celulas[2].lower()
        res.exigir(
            any(t in classificacao for t in TIPOLOGIA) or MARCA_FORA in classificacao,
            f"{codigo}: classificacao «{celulas[2]}» nao e da tipologia nem esta marcada "
            "como fora dela",
        )
        traco = celulas[3]
        res.exigir(
            len(traco.split()) >= 4,
            f"{codigo}: o traco ate o MPO esta vazio ou generico demais («{traco}»)",
        )
        res.exigir(
            codigo in prosa,
            f"{codigo} aparece so na Tabela 1: a prosa precisa dizer o que foi observado, "
            "por que e deficiencia e como foi corrigida",
        )
    fora = [c for c, cel in linhas.items() if MARCA_FORA in cel[2].lower()]
    if fora:
        res.exigir(
            all(c in prosa for c in fora)
            and re.search(r"ficam fora dela|fora da tipologia", prosa) is not None,
            f"{', '.join(sorted(fora))} estao fora da tipologia e o texto nao justifica por que",
        )


def verificar_citacoes(texto: str, res: Resultado) -> None:
    """Toda aspa curva e citacao verbatim: cada uma tem de estar na fonte."""
    fonte = " || ".join(_normalizar(_ler(caminho)) for caminho in FONTES)
    corpo = _sem_comentarios(texto)
    citacoes = re.findall(r"\u201c([^\u201d]+)\u201d", corpo)
    res.exigir(
        len(citacoes) >= 8,
        f"so {len(citacoes)} citacoes da fonte: cada traco precisa de ancora verbatim",
    )
    for citacao in citacoes:
        res.exigir(
            _normalizar(citacao) in fonte,
            f"citacao nao encontrada na fonte, palavra por palavra: «{citacao[:60]}»",
        )
    # cada bloco de analise ancora em pelo menos uma citacao
    for titulo, bloco in _subsecoes(corpo).items():
        if re.search(r"\(A\d", titulo):
            res.exigir(
                "\u201c" in bloco,
                f"a subsecao «{titulo}» nao traz citacao da fonte: traco sem ancora",
            )


def verificar_crud(texto: str, res: Resultado) -> None:
    afirma = re.search(r"acr[óo]nimo CRUD n[ãa]o ocorre", _sem_comentarios(texto))
    if not afirma:
        return
    res.checagens += 1
    for caminho in FONTES_DO_MPO:
        if re.search(r"crud", _ler(caminho), re.IGNORECASE):
            res.falhas.append(
                f"o texto afirma que CRUD nao ocorre no MPO, mas ocorre em {caminho}"
            )
            return


def _subsecoes(texto: str) -> dict[str, str]:
    partes: dict[str, str] = {}
    titulo = "(abertura)"
    acumulado: list[str] = []
    for linha in texto.splitlines():
        if linha.startswith("## "):
            partes[titulo] = "\n".join(acumulado)
            titulo = linha[3:].strip()
            acumulado = []
        else:
            acumulado.append(linha)
    partes[titulo] = "\n".join(acumulado)
    return partes


# --------------------------------------------------------------------------
# 4. o texto contra os artefatos
# --------------------------------------------------------------------------


def _classes_do_modelo(caminho: Path) -> set[str]:
    nomes: set[str] = set()

    def visitar(no: object) -> None:
        if isinstance(no, dict):
            if no.get("type") == "Class" and no.get("name"):
                nomes.add(str(no["name"]))
            for valor in no.values():
                visitar(valor)
        elif isinstance(no, list):
            for valor in no:
                visitar(valor)

    try:
        visitar(json.loads(_ler(caminho)))
    except json.JSONDecodeError:
        pass
    return nomes


def verificar_identificadores(texto: str, res: Resultado) -> None:
    """Nenhum construto citado pode ser invencao do texto."""
    baseline = _classes_do_modelo(ONTOLOGIA / "baseline" / "ontompo-as-is.ontouml.json")
    revisado = _classes_do_modelo(ONTOLOGIA / "rodada-2" / "ontompo-rodada-2.ontouml.json")
    if not res.exigir(
        bool(baseline and revisado), "modelos as-is e rodada 2 nao lidos: nada a conferir"
    ):
        return
    conhecidos = baseline | revisado
    citados = {
        ident
        for ident in re.findall(r"`([A-Z][A-Za-z]+)`", _sem_comentarios(texto))
        if not ident.startswith("QC")
    }
    desconhecidos = sorted(citados - conhecidos)
    res.exigir(
        not desconhecidos,
        f"identificadores citados que nao existem em nenhum dos modelos: "
        f"{', '.join(desconhecidos)}",
    )


def verificar_numeros(texto: str, res: Resultado) -> None:
    corpo = _sem_comentarios(texto)

    # QC7: a divergencia entre os dois observatorios, recontada do csv
    caminho = ONTOLOGIA / "consultas" / "qc7-resultado.csv"
    linhas = list(csv.DictReader(_ler(caminho).splitlines()))
    if res.exigir(bool(linhas), f"{caminho} vazio ou ausente"):
        colunas = list(linhas[0].keys())
        divergentes = [l for l in linhas if "0" in (l[colunas[-1]], l[colunas[-2]])]
        comuns = len(linhas) - len(divergentes)
        for valor, papel in ((len(divergentes), "divergentes"), (comuns, "comuns")):
            achado = any(
                re.search(rf"\b{re.escape(forma)}\b", corpo, re.IGNORECASE)
                for forma in _por_extenso(valor)
            )
            res.exigir(
                achado,
                f"a QC7 tem {valor} conceitos {papel} e o texto nao diz esse numero",
            )

    # o glossario da conceituacao
    if re.search(r"gloss[áa]rio de (\d+) termos", corpo):
        declarado = re.search(r"gloss[áa]rio de (\d+) termos", corpo).group(1)
        res.exigir(
            f"{declarado} termos" in _ler(FONTE / "conteudo" / "resultados.tex"),
            f"o texto fala em glossario de {declarado} termos, numero que a fonte nao traz",
        )

    # as regras estruturais e o zero do plugin
    relatorio = _ler(ONTOLOGIA / "rodada-2" / "relatorio-verificador-ufo-b-c.md")
    regras = set(re.findall(r"^\| `([a-z_]+)` \|", relatorio, re.M))
    if re.search(r"nove regras estruturais", corpo):
        res.exigir(
            len(regras) == 9,
            f"o texto fala em nove regras estruturais e o relatorio traz {len(regras)}",
        )
    if re.search(r"devolve zero problema sobre a linha de base", corpo):
        achados = json.loads(
            _ler(ONTOLOGIA / "baseline" / "relatorio-plugin-ontouml.json") or "[]"
        )
        res.exigir(
            achados == [],
            "o texto afirma zero do plugin sobre a linha de base, e o relatorio nao esta vazio",
        )


def verificar_achados_extras(texto: str, res: Resultado) -> None:
    """Os achados fora de A1-A9 precisam estar todos contabilizados."""
    registrados: set[str] = set()
    for nome in (
        "evidencias-A1-A9.md",
        "correcoes-rodada-1.md",
        "correcoes-rodada-2.md",
    ):
        registrados |= set(re.findall(r"\bB(\d+)\b", _ler(ONTOLOGIA / nome)))
    total = len(registrados)
    if not res.exigir(total > 0, "nenhum achado B registrado nos artefatos da ontologia"):
        return
    corpo = _sem_comentarios(texto)
    bloco = next(
        (b for t, b in _subsecoes(corpo).items() if "achados" in t.lower()),
        "",
    )
    if not res.exigir(bool(bloco), "nenhuma subsecao trata dos achados fora de A1-A9"):
        return
    # A subsecao abre declarando o total e depois distribui os achados em frases
    # que comecam por numeral. A soma das disposicoes tem de fechar com o total,
    # senao algum achado ficou sem destino.
    frases = re.split(r"(?<=[.:]) +", " ".join(bloco.split()))
    numerais = [
        (frase, _numeral(re.match(r"([A-Za-zÀ-ÿ]+)", frase).group(1)))
        for frase in frases
        if re.match(r"([A-Za-zÀ-ÿ]+)", frase)
    ]
    abertura = next((valor for _, valor in numerais if valor is not None), None)
    if not res.exigir(
        abertura is not None,
        "a secao nao declara quantos achados apareceram fora da lista",
    ):
        return
    res.exigir(
        abertura == total,
        f"a secao declara {abertura} achados fora da lista e os artefatos registram {total}",
    )
    soma = 0
    vista_abertura = False
    for _, valor in numerais:
        if valor is None:
            continue
        if not vista_abertura:
            vista_abertura = True
            continue
        soma += valor
    res.exigir(
        soma == total,
        f"as disposicoes descritas somam {soma} achados, e sao {total} a contabilizar",
    )


# --------------------------------------------------------------------------
# 5. o que a secao tem de dizer, e o que nao pode dizer
# --------------------------------------------------------------------------


def verificar_argumento(diretorio: Path, texto: str, res: Resultado) -> None:
    corpo = _sem_comentarios(texto)
    prosa, _, listagem = _blocos(corpo)

    res.exigir(
        re.search(r"subdetermina", corpo, re.IGNORECASE) is not None,
        "a subdeterminacao do MPO nao esta declarada como resultado",
    )
    res.exigir(
        re.search(r"n\s*=\s*1", corpo) is not None,
        "o limite n=1 (um formalizador) nao esta declarado",
    )
    res.exigir(
        any("antes" in l for l in listagem) and any("depois" in l for l in listagem),
        "nenhum par antes/depois visivel para as correcoes que mudam o diagrama",
    )

    chaves = set(re.findall(r"\[([a-z0-9, ]+)\]", prosa))
    citadas = {c.strip() for grupo in chaves for c in grupo.split(",") if c.strip()}
    bib = _ler(diretorio / "referencias.bib")
    faltando = sorted(c for c in citadas if f"{{{c}," not in bib)
    res.exigir(not faltando, f"chaves citadas sem entrada no .bib: {', '.join(faltando)}")
    res.exigir(
        bool(citadas & set(CHAVES_FUNDAMENTO)),
        "nenhuma correcao fundamentada em UFO ou Representation Theory",
    )
    for titulo, bloco in _subsecoes(prosa).items():
        if not re.search(r"\(A\d", titulo):
            continue
        usadas = {
            c.strip()
            for grupo in re.findall(r"\[([a-z0-9, ]+)\]", bloco)
            for c in grupo.split(",")
        }
        res.exigir(
            bool(usadas & set(CHAVES_FUNDAMENTO)),
            f"a subsecao «{titulo}» corrige sem argumento ontologico referenciado",
        )


def verificar_localizacao_e_tom(texto: str, res: Resultado) -> None:
    corpo = _sem_comentarios(texto)
    for padrao in ATRIBUICOES_PROIBIDAS:
        achado = re.search(padrao, corpo, re.IGNORECASE)
        res.exigir(
            achado is None,
            f"o texto atribui a deficiencia ao MPO em linguagem natural: "
            f"«{achado.group(0) if achado else ''}»",
        )
    res.exigir(
        re.search(r"formaliza[çc][ãa]o publicada", corpo) is not None,
        "o texto nao localiza as deficiencias na formalizacao publicada",
    )
    minusculo = corpo.lower()
    for termo in TERMOS_IDENTIFICADORES:
        res.exigir(termo not in minusculo, f"mencao identificadora no texto: «{termo}»")
    for padrao in LEVE:
        res.exigir(
            re.search(padrao, corpo, re.IGNORECASE) is None,
            "resquicio da defesa de ontologia leve, abandonada pelo spec",
        )
    achado = PRIMEIRA_PESSOA.search(corpo)
    res.exigir(
        achado is None,
        f"primeira pessoa no texto («{achado.group(0) if achado else ''}»): "
        "o objeto de analise e trabalho de terceiros",
    )


def main() -> int:
    diretorio = Path(sys.argv[1]) if len(sys.argv) > 1 else ARTIGO_PADRAO
    caminho = diretorio / "secoes" / NOME_SECAO
    res = Resultado()

    texto = _ler(caminho)
    if not res.exigir(bool(texto), f"{caminho} ausente ou vazio"):
        print(f"FALHOU: {res.falhas[0]}")
        return 1

    verificar_plano(diretorio, texto, res)
    verificar_tabela(texto, res)
    verificar_citacoes(texto, res)
    verificar_crud(texto, res)
    verificar_identificadores(texto, res)
    verificar_numeros(texto, res)
    verificar_achados_extras(texto, res)
    verificar_argumento(diretorio, texto, res)
    verificar_localizacao_e_tom(texto, res)

    print(f"verificacoes: {res.checagens}")
    if res.falhas:
        print(f"FALHOU: {len(res.falhas)} problema(s)")
        for falha in res.falhas:
            print(f"  - {falha}")
        return 1
    print("OK: a checklist do ticket 10 esta cumprida")
    return 0


if __name__ == "__main__":
    sys.exit(main())
