#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifica as secoes 6 a 9 e a declaracao de IA (checklist do ticket 12).

Uso: python tools/verification/verificar_seccoes_ontologia_avaliacao_conclusao.py [diretorio-do-artigo]

O texto do fechamento do artigo mora em `artifacts/paper/secoes/06-ontompo-revisada.md`,
`07-avaliacao.md`, `08-discussao-limitacoes.md`, `09-conclusao.md` e
`declaracao-ia.md`. Duas criticas do ONTOBRAS dependem especificamente deste
trecho: a conclusao que resumia resultados em vez de discutir licoes e
limitacoes, e a avaliacao apresentada so de forma sumarizada, que a tornava
irreproduzivel. Este verificador le esses textos como terceiro — sem importar do
codigo que produziu qualquer artefato — e confronta cada exigencia da checklist
com a fonte que a sustenta:

  1. as cinco superficies existem, o esqueleto aponta para cada uma e o
     orcamento de paginas que ele declara e respeitado. A medida e a dos tickets
     10 e 11: compilada no template SBC quando ha `pdflatex`, e senao estimada
     por linhas e **calibrada pela medida compilada da secao 5**, que o proprio
     esqueleto registra;
  2. a secao 6 **descreve** a ontologia revisada em vez de listar seus
     conceitos: os nomes de classe conferidos contra o proprio
     `ontompo-rodada-2.ontouml.json`, a razao entre prosa e identificador acima
     de um piso, e o vocabulario de estereotipos presente. As contagens de
     classes, relacoes e generalizacoes batem com o relatorio do plugin;
  3. o caminho do OntoUML ao OWL esta descrito — a transformacao gUFO com a
     ferramenta oficial, as cinco customizacoes uma a uma, a regra aditiva e a
     publicacao do acrescimo — e as metricas do artefato batem, celula a celula,
     com `artifacts/ontology/owl/metricas.md`;
  4. a secao 7 relata as **tres frentes**: as sete questoes de competencia com o
     numero de linhas de cada uma conferido contra o `.csv` gravado, a
     verificacao de conformidade e as regras estruturais com os numeros antes e
     depois, e o OOPS! com os seus. Nenhum numero e aceito do texto: todos vem do
     artefato correspondente;
  5. consultas e resultados completos sao **referenciados**, no apendice ou no
     deposito, e nunca so sumarizados, e as divergencias entre o que se
     esperava e o que a consulta devolveu estao registradas, inclusive as que
     desfavorecem o artefato;
  6. o cenario de instanciacao aparece em terceira pessoa, sem identificar quem
     o construiu;
  7. a secao 8 traz licoes, e nao repeticao de resultado — os numeros que a
     secao 7 relata nao reaparecem la —, e declara as limitacoes exigidas, entre
     elas a ausencia de validacao com especialistas contra o pano de fundo dos
     grupos focais e dos estudos de caso, e o observatorio sintetico da
     comparacao;
  8. a secao 9 entrega a contribuicao para SI nas tres formas previstas e os
     trabalhos futuros exigidos, com os modelos de linguagem como direcao e nao
     como resultado;
  9. a declaracao de uso de IA generativa nomeia ferramenta e frentes de
     emprego, como manda o Codigo de Conduta da SBC;
 10. **nao ha conteudo repetido entre secoes**: nenhuma sequencia de doze
     palavras reaparece em duas delas — as secoes 1 a 5 entram na comparacao —,
     nenhuma citacao verbatim e reusada, e o desenho da avaliacao continua
     exclusivo da secao 4;
 11. **toda aspa curva e citacao verbatim da fonte**, procurada com espacos
     normalizados em `sources/dissertation/`;
 12. nada atribui as deficiencias ao MPO em linguagem natural, e nao ha mencao
     identificadora, primeira pessoa nem resquicio da defesa de ontologia leve.

Sai com codigo 1 se qualquer verificacao falhar.
"""

from __future__ import annotations

import csv
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
from pathlib import Path

ARTIGO_PADRAO = Path("artifacts/paper")
FONTE = Path("sources/dissertation")
ONTOLOGIA = Path("artifacts/ontology")

SECOES = {
    "06": "06-ontompo-revisada.md",
    "07": "07-avaliacao.md",
    "08": "08-discussao-limitacoes.md",
    "09": "09-conclusao.md",
}

DECLARACAO = "declaracao-ia.md"

# As secoes ja escritas, que entram na comparacao de redundancia mas nao sao
# alvo de nenhuma outra regra daqui.
ANTERIORES = (
    "01-introducao.md",
    "02-referencial.md",
    "03-trabalhos-relacionados.md",
    "04-metodo.md",
    "05-analise-ontologica.md",
)

FONTES = (
    FONTE / "conteudo" / "fundamentacao.tex",
    FONTE / "conteudo" / "resultados.tex",
    FONTE / "conteudo" / "metodologia.tex",
    FONTE / "conteudo" / "introducao.tex",
    FONTE / "conteudo" / "conclusao.tex",
    FONTE / "postextuais" / "apendices.tex",
)

# Mesma geometria e mesma calibracao do verificador do ticket 11.
LINHAS_POR_PAGINA = 48.0
CARACTERES_POR_LINHA = 93.0
SECAO_5 = "05-analise-ontologica.md"

MODELO_REVISADO = ONTOLOGIA / "rodada-2" / "ontompo-rodada-2.ontouml.json"
PLUGIN_REVISADO = ONTOLOGIA / "rodada-2" / "relatorio-plugin-ontouml.md"
ESTRUTURAL = ONTOLOGIA / "rodada-2" / "relatorio-verificador-ufo-b-c.md"
METRICAS = ONTOLOGIA / "owl" / "metricas.md"
COMPARACAO_OOPS = ONTOLOGIA / "owl" / "comparacao-oops.md"
CONSULTAS = ONTOLOGIA / "consultas"

# Quanta prosa cada identificador precisa ter em volta para que a secao 6 conte
# como descricao e nao como lista. Uma listagem de conceitos fica perto de tres
# ou quatro palavras por identificador; um texto que descreve, muito acima.
PALAVRAS_POR_IDENTIFICADOR = 12.0

# Quantos dos conceitos do modelo revisado a secao 6 precisa apresentar. Nao sao
# os 44: uma secao de 1,75 pagina que nomeasse todos seria a lista que a
# checklist proibe. O piso existe para que nenhuma camada fique de fora.
CONCEITOS_MINIMOS = 30

ESTEREOTIPOS = ("«kind»", "«role»", "«category»", "«roleMixin»", "«event»", "«collective»")

CUSTOMIZACOES = ("C1", "C2", "C3", "C4", "C5")

# Numeros que a secao 7 relata. Reaparecer na secao 8 e o sintoma exato da
# critica do parecer: discussao que repete resultado em vez de discuti-lo.
NUMEROS_DE_RESULTADO = ("105", "56", "648", "1284", "809", "475", "31", "23")

TIPOLOGIA_FORA = ("Methontology", "Design Science Research")

ATRIBUICOES_PROIBIDAS = (
    r"defici[êe]ncias?\s+d[oa]\s+(MPO|modelo de refer[êe]ncia)",
    r"defeitos?\s+d[oa]\s+(MPO|modelo de refer[êe]ncia)",
    r"erros?\s+d[oa]\s+(MPO|modelo de refer[êe]ncia)",
    r"falhas?\s+d[oa]\s+(MPO|modelo de refer[êe]ncia)",
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
    "próprio autor",
    "proprio autor",
)

LEVE = (r"ontologia\s+leve", r"lightweight\s+ontology")

PRIMEIRA_PESSOA = re.compile(
    r"\b(nós|nosso|nossa|nossos|nossas|realizamos|propomos|apresentamos|"
    r"desenvolvemos|analisamos|conduzimos|construímos|adotamos)\b",
    re.IGNORECASE,
)


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
    return re.sub(r"<!--.*?-->", "", texto, flags=re.S)


def _normalizar(texto: str) -> str:
    texto = re.sub(r"\\[a-zA-Z]+\s*", "", texto)
    texto = texto.replace("{", "").replace("}", "").replace("~", " ")
    texto = texto.replace("``", '"').replace("''", '"')
    texto = unicodedata.normalize("NFC", texto)
    return re.sub(r"\s+", " ", texto).strip().lower()


def _corrido(texto: str) -> str:
    return re.sub(r"\s+", " ", _sem_comentarios(texto))


def _citacoes(texto: str) -> list[str]:
    return re.findall(r"\u201c([^\u201d]+)\u201d", _sem_comentarios(texto))


def _chaves(texto: str) -> set[str]:
    return {
        chave.strip()
        for grupo in re.findall(r"\[([a-z0-9_,\s]+)\]", _sem_comentarios(texto))
        for chave in grupo.split(",")
        if chave.strip()
    }


def _tabelas(texto: str) -> list[list[list[str]]]:
    """As tabelas Markdown do texto, cada uma como lista de linhas de celulas."""
    tabelas: list[list[list[str]]] = []
    atual: list[list[str]] = []
    for linha in _sem_comentarios(texto).splitlines():
        cru = linha.strip()
        if cru.startswith("|"):
            celulas = [c.strip() for c in cru.strip("|").split("|")]
            if set("".join(celulas)) <= set("-: "):
                continue
            atual.append(celulas)
        elif atual:
            tabelas.append(atual)
            atual = []
    if atual:
        tabelas.append(atual)
    return tabelas


# --------------------------------------------------------------------------
# os artefatos, lidos como terceiro
# --------------------------------------------------------------------------


def _classes_do_modelo() -> set[str]:
    """Os nomes de classe do modelo revisado, lidos do artefato de intercambio."""
    try:
        dados = json.loads(MODELO_REVISADO.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return set()
    nomes: set[str] = set()

    def andar(no: object) -> None:
        if isinstance(no, dict):
            if no.get("type") == "Class" and isinstance(no.get("name"), str):
                nomes.add(no["name"])
            for valor in no.values():
                andar(valor)
        elif isinstance(no, list):
            for valor in no:
                andar(valor)

    andar(dados)
    return nomes


def _contagens_do_plugin() -> dict[str, int]:
    """Classes, relacoes e generalizacoes que o relatorio do plugin declara."""
    texto = _ler(PLUGIN_REVISADO)
    contagens: dict[str, int] = {}
    for rotulo, chave in (
        ("Classes verificadas", "classes"),
        ("Relacoes verificadas", "relacoes"),
        ("Generalizacoes verificadas", "generalizacoes"),
    ):
        achado = re.search(rf"{rotulo}:\s*(\d+)", texto)
        if achado:
            contagens[chave] = int(achado.group(1))
    return contagens


def _rotulo_de_metrica(celula: str) -> str:
    """O nome de uma linha de metrica, sem o parentese que diz como ela se conta.

    O artefato escreve «subsuncoes (`rdfs:subClassOf`)» e o artigo escreve
    «subsuncoes»: e a mesma metrica, e o que precisa bater sao os numeros.
    """
    rotulo = re.sub(r"\([^)]*\)", " ", celula)
    return re.sub(r"[`*]", "", rotulo).strip().lower()


def _metricas_do_artefato() -> dict[str, tuple[int, int, int]]:
    """A tabela de metricas da OWL: rotulo da linha -> as tres colunas."""
    metricas: dict[str, tuple[int, int, int]] = {}
    for tabela in _tabelas(_ler(METRICAS)):
        for celulas in tabela:
            if len(celulas) != 4:
                continue
            numeros = [c.replace("`", "").strip() for c in celulas[1:]]
            if not all(re.fullmatch(r"\d+", n) for n in numeros):
                continue
            metricas[_rotulo_de_metrica(celulas[0])] = tuple(  # type: ignore[assignment]
                int(n) for n in numeros
            )
    return metricas


def _totais_estruturais() -> tuple[int, int, int] | None:
    """A linha de total do verificador de microteorias: as-is, rodada 1, rodada 2."""
    for tabela in _tabelas(_ler(ESTRUTURAL)):
        for celulas in tabela:
            if not celulas[0].startswith("**total**"):
                continue
            numeros = [
                int(n)
                for c in celulas
                for n in re.findall(r"\d+", c.replace("*", ""))
            ]
            if len(numeros) >= 3:
                return (numeros[-3], numeros[-2], numeros[-1])
    return None


def _totais_oops() -> tuple[int, int, int, int] | None:
    """A linha de total do comparativo do OOPS!: antes, depois, e as de dominio."""
    for tabela in _tabelas(_ler(COMPARACAO_OOPS)):
        for celulas in tabela:
            if "total" not in celulas[1].lower():
                continue
            numeros = [
                int(c.replace("*", "").strip())
                for c in celulas
                if re.fullmatch(r"\**\d+\**", c.strip())
            ]
            if len(numeros) >= 4:
                return (numeros[0], numeros[1], numeros[2], numeros[3])
    return None


def _linhas_das_qc() -> dict[str, int]:
    """Quantas linhas cada consulta devolveu, contadas no proprio .csv."""
    linhas: dict[str, int] = {}
    for numero in range(1, 8):
        caminho = CONSULTAS / f"qc{numero}-resultado.csv"
        try:
            with caminho.open(encoding="utf-8", newline="") as arquivo:
                linhas[f"QC{numero}"] = max(0, sum(1 for _ in csv.reader(arquivo)) - 1)
        except OSError:
            continue
    return linhas


def _divergencia_da_qc7() -> tuple[int, int, int] | None:
    """Conceitos cobertos pelos dois cenarios, e os que so um deles instancia."""
    caminho = CONSULTAS / "qc7-resultado.csv"
    try:
        with caminho.open(encoding="utf-8", newline="") as arquivo:
            linhas = list(csv.DictReader(arquivo))
    except OSError:
        return None
    if not linhas:
        return None
    colunas = [c for c in linhas[0] if c and c.lower().startswith("instancias")]
    if len(colunas) != 2:
        return None
    divergentes = sum(
        1
        for linha in linhas
        if (linha[colunas[0]].strip() == "0") != (linha[colunas[1]].strip() == "0")
    )
    return (len(linhas), len(linhas) - divergentes, divergentes)


# --------------------------------------------------------------------------
# 1. o plano e o orcamento de paginas
# --------------------------------------------------------------------------


def _orcamentos(esqueleto: str) -> dict[str, float]:
    orcamentos: dict[str, float] = {}
    for linha in esqueleto.splitlines():
        if not linha.strip().startswith("|"):
            continue
        colunas = [c.strip() for c in linha.strip().strip("|").split("|")]
        if len(colunas) < 3:
            continue
        if re.fullmatch(r"\d{1,2}", colunas[0]):
            chave = colunas[0].zfill(2)
        elif "IA generativa" in colunas[1]:
            chave = "ia"
        else:
            continue
        try:
            orcamentos[chave] = float(colunas[-1].replace(",", "."))
        except ValueError:
            continue
    return orcamentos


def _medida_da_secao_5(esqueleto: str) -> float | None:
    achado = re.search(r"mede\s+\*\*([\d,]+)\s+páginas?\*\*", esqueleto)
    return float(achado.group(1).replace(",", ".")) if achado else None


def _linhas(markdown: str) -> float:
    total = 0.0
    for bloco in _sem_comentarios(markdown).split("\n\n"):
        b = bloco.strip()
        if not b:
            continue
        if b.startswith("```"):
            total += len([l for l in b.split("\n") if not l.startswith("```")]) + 1.5
        elif b.lstrip().startswith("|"):
            for linha in b.split("\n"):
                celulas = [c.strip() for c in linha.strip().strip("|").split("|")]
                if set("".join(celulas)) <= set("-: "):
                    continue
                total += max(math.ceil(len(c) / 22) for c in celulas) * 0.75 + 0.3
            total += 2
        elif b.startswith("#"):
            total += 2.0
        elif b.lstrip().startswith("- "):
            for item in re.split(r"\n(?=- )", b):
                total += math.ceil(len(re.sub(r"\s+", " ", item)) / CARACTERES_POR_LINHA) + 0.3
        else:
            total += math.ceil(len(re.sub(r"\s+", " ", b)) / CARACTERES_POR_LINHA) + 0.43
    return total


def _para_latex(markdown: str) -> str:
    """Porte grosseiro para LaTeX, so para medir. O porte real e do ticket 13."""

    def inline(t: str) -> str:
        t = re.sub(r"`([^`]*)`", lambda m: r"\texttt{" + m.group(1).replace("_", r"\_") + "}", t)
        t = re.sub(r"\*\*([^*]*)\*\*", lambda m: r"\textbf{" + m.group(1) + "}", t)
        t = re.sub(r"\*([^*]*)\*", lambda m: r"\textit{" + m.group(1) + "}", t)
        t = t.replace("&", r"\&").replace("%", r"\%").replace("#", r"\#")
        t = t.replace("«", "<<").replace("»", ">>")
        t = t.replace("\u201c", "``").replace("\u201d", "''")
        t = t.replace("²", r"\textsuperscript{2}")
        t = re.sub(r"\[([a-z0-9_, ]+)\]", lambda m: r"\cite{" + m.group(1) + "}", t)
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
        elif b.lstrip().startswith("|"):
            linhas = [
                [c.strip() for c in linha.strip().strip("|").split("|")]
                for linha in b.split("\n")
                if linha.strip().startswith("|")
            ]
            linhas = [c for c in linhas if not set("".join(c)) <= set("-: ")]
            colunas = max(len(c) for c in linhas)
            corpo.append(
                "\\begin{tabular}{" + "l" * colunas + "}\n"
                + " \\\\\n".join(" & ".join(inline(c) for c in linha) for linha in linhas)
                + "\n\\end{tabular}"
            )
        elif b.lstrip().startswith("- "):
            itens = [
                r"\item " + inline(i.strip()[2:])
                for i in re.split(r"\n(?=- )", b)
                if i.strip()
            ]
            corpo.append("\\begin{itemize}\n" + "\n".join(itens) + "\n\\end{itemize}")
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

def verificar_plano(diretorio: Path, textos: dict[str, str], res: Resultado) -> None:
    esqueleto = _ler(diretorio / "esqueleto.md")
    for nome in list(SECOES.values()) + [DECLARACAO]:
        res.exigir(
            nome in esqueleto,
            f"o esqueleto nao aponta para secoes/{nome}: o ticket 13 nao acha o texto",
        )
    orcamentos = _orcamentos(esqueleto)
    if not res.exigir(
        all(n in orcamentos for n in list(SECOES) + ["ia"]),
        "orcamento de alguma das secoes 6 a 9 ou da declaracao ausente na tabela do esqueleto",
    ):
        return

    porte = _medir_no_porte(diretorio)
    compiladas = (
        {} if porte is not None
        else {n: _medir_paginas(diretorio, t) for n, t in textos.items()}
    )
    if porte is not None:
        medidas = {n: porte[n] for n in textos}
        origem = "porte do ticket 13"
    elif all(v is not None for v in compiladas.values()):
        medidas = compiladas
        origem = "porte provisorio"
    else:
        secao5 = _ler(diretorio / "secoes" / SECAO_5)
        alvo = _medida_da_secao_5(esqueleto)
        if not res.exigir(
            bool(secao5) and alvo is not None,
            "sem pdflatex e sem a medida compilada da secao 5 no esqueleto: "
            "a paginacao nao pode ser conferida",
        ):
            return
        fator = alvo / (_linhas(secao5) / LINHAS_POR_PAGINA)
        medidas = {n: _linhas(t) / LINHAS_POR_PAGINA * fator for n, t in textos.items()}
        origem = f"estimada (calibrada em {alvo:.2f} paginas da secao 5, fator {fator:.3f})"

    total = 0.0
    for numero in sorted(textos):
        paginas = medidas[numero]
        total += paginas
        rotulo = "declaracao" if numero == "ia" else f"secao {numero}"
        print(f"  {rotulo}: {paginas:.2f} pagina(s), orcamento {orcamentos[numero]:.2f}")
        res.exigir(
            paginas <= orcamentos[numero],
            f"a {rotulo} mede {paginas:.2f} paginas e o esqueleto lhe da "
            f"{orcamentos[numero]:.2f}",
        )
    orcado = sum(orcamentos[n] for n in textos)
    print(f"  paginacao {origem}: {total:.2f} de {orcado:.2f} paginas")
    res.exigir(
        total <= orcado,
        f"o fechamento soma {total:.2f} paginas e o orcamento previsto e {orcado:.2f}",
    )


# --------------------------------------------------------------------------
# 2. a secao 6 — a ontologia revisada
# --------------------------------------------------------------------------


def verificar_ontologia_revisada(texto: str, res: Resultado) -> None:
    corpo = _corrido(texto)
    minusculo = corpo.lower()
    chaves = _chaves(texto)

    # 2.1 os conceitos, conferidos contra o proprio modelo
    classes = _classes_do_modelo()
    if not res.exigir(bool(classes), f"{MODELO_REVISADO} nao pode ser lido: nada a conferir"):
        return
    citados = {c for c in classes if re.search(rf"`{re.escape(c)}`", corpo)}
    res.exigir(
        len(citados) >= CONCEITOS_MINIMOS,
        f"a secao 6 apresenta {len(citados)} dos {len(classes)} conceitos do modelo revisado, "
        f"e o piso e {CONCEITOS_MINIMOS}",
    )
    inventados = {
        nome
        for nome in re.findall(r"`([A-Z][A-Za-z]+)`", corpo)
        if nome not in classes
    }
    res.exigir(
        not inventados,
        f"a secao 6 nomeia conceito que nao esta no modelo revisado: {', '.join(sorted(inventados))}",
    )

    # 2.2 descritos, e nao listados
    ocorrencias = len(re.findall(r"`[^`]+`", corpo))
    palavras = len(re.findall(r"[0-9A-Za-zÀ-ÿ]+", re.sub(r"`[^`]+`", " ", corpo)))
    densidade = palavras / ocorrencias if ocorrencias else 0.0
    print(f"  secao 6: {len(citados)} conceitos, {densidade:.1f} palavras por identificador")
    res.exigir(
        densidade >= PALAVRAS_POR_IDENTIFICADOR,
        f"a secao 6 tem {densidade:.1f} palavras de prosa por identificador (piso "
        f"{PALAVRAS_POR_IDENTIFICADOR:.0f}): os conceitos estao listados, nao descritos",
    )
    faltando = [e for e in ESTEREOTIPOS if e not in corpo]
    res.exigir(
        not faltando,
        f"a secao 6 descreve conceitos sem dizer a categoria ontologica de cada um: "
        f"falta {', '.join(faltando)}",
    )

    # 2.3 as contagens do artefato
    contagens = _contagens_do_plugin()
    if res.exigir(bool(contagens), f"{PLUGIN_REVISADO} nao pode ser lido: nada a conferir"):
        for chave, rotulo in (
            ("classes", "classes"),
            ("relacoes", "relações"),
            ("generalizacoes", "generalizações"),
        ):
            esperado = contagens.get(chave)
            res.exigir(
                esperado is not None
                and re.search(rf"\b{esperado}\s+{rotulo}", corpo) is not None,
                f"a secao 6 nao declara «{esperado} {rotulo}», que e o que o relatorio do "
                f"plugin conta no modelo revisado",
            )

    # 2.4 o caminho do OntoUML ao OWL
    res.exigir(
        "gUFO" in corpo and "almeida2019gufo" in chaves,
        "a secao 6 nao descreve a transformacao gUFO, com referencia",
    )
    res.exigir(
        "ontouml-js" in minusculo,
        "a secao 6 nao nomeia a ferramenta que executa a transformacao",
    )
    faltando = [c for c in CUSTOMIZACOES if not re.search(rf"\*\*{c}\*\*|`{c}`|\b{c}\b", corpo)]
    res.exigir(
        not faltando,
        f"a secao 6 nao diz o que foi customizado sobre o gerado: falta {', '.join(faltando)}",
    )
    res.exigir(
        re.search(r"aditiv", minusculo) is not None,
        "a secao 6 nao declara que a customizacao e aditiva — e o que torna a preservacao "
        "semantica verificavel em vez de afirmada",
    )
    res.exigir(
        re.search(r"acr[ée]scimo|diff", minusculo) is not None,
        "a secao 6 nao diz que o acrescimo da customizacao foi publicado a parte",
    )

    # 2.5 as metricas
    metricas = _metricas_do_artefato()
    if not res.exigir(bool(metricas), f"{METRICAS} nao pode ser lido: nada a conferir"):
        return
    tabelas = [t for t in _tabelas(texto) if len(t) > 3]
    if not res.exigir(bool(tabelas), "a secao 6 nao traz a tabela de metricas do artefato"):
        return
    reportadas: dict[str, tuple[int, ...]] = {}
    for tabela in tabelas:
        for celulas in tabela:
            if len(celulas) != 4:
                continue
            numeros = [c.replace("`", "").strip() for c in celulas[1:]]
            if not all(re.fullmatch(r"\d+", n) for n in numeros):
                continue
            reportadas[_rotulo_de_metrica(celulas[0])] = tuple(int(n) for n in numeros)
    res.exigir(
        len(reportadas) >= 6,
        f"a tabela de metricas da secao 6 tem {len(reportadas)} linhas de numeros: "
        "as metricas do artefato nao estao reportadas",
    )
    for rotulo, valores in reportadas.items():
        esperado = metricas.get(rotulo)
        res.exigir(
            esperado is not None,
            f"a secao 6 reporta a metrica «{rotulo}», que nao existe em {METRICAS}",
        )
        if esperado is not None:
            res.exigir(
                esperado == valores,
                f"a metrica «{rotulo}» na secao 6 e {valores} e o artefato diz {esperado}",
            )


# --------------------------------------------------------------------------
# 3. a secao 7 — a avaliacao
# --------------------------------------------------------------------------


def verificar_avaliacao(texto: str, res: Resultado) -> None:
    corpo = _corrido(texto)
    minusculo = corpo.lower()
    chaves = _chaves(texto)

    # 3.1 as sete questoes de competencia, com o numero de linhas do .csv
    linhas = _linhas_das_qc()
    if not res.exigir(
        len(linhas) == 7, f"so {len(linhas)} das sete consultas tem resultado gravado em {CONSULTAS}"
    ):
        return
    for questao, quantas in sorted(linhas.items()):
        res.exigir(
            quantas > 0,
            f"a {questao} devolveu resultado vazio: a avaliacao nao sustenta o que afirma",
        )
        res.exigir(
            re.search(rf"\|\s*{questao}\s*\|", corpo) is not None,
            f"a secao 7 nao relata a {questao} na tabela das questoes de competencia",
        )
        linha = re.search(rf"\|\s*{questao}\s*\|([^\n]*)", _sem_comentarios(texto))
        res.exigir(
            linha is not None and re.search(rf"\|\s*{quantas}\s*\|", linha.group(1)) is not None,
            f"a secao 7 nao reporta as {quantas} linhas que a {questao} devolveu",
        )

    # 3.2 a QC7, que sustenta a tese
    divergencia = _divergencia_da_qc7()
    if res.exigir(divergencia is not None, "a QC7 nao pode ser lida do .csv gravado"):
        assert divergencia is not None
        total, comuns, divergentes = divergencia
        res.exigir(
            re.search(rf"\b{total}\b", corpo) is not None
            and re.search(rf"\b{comuns}\b", corpo) is not None,
            f"a secao 7 nao relata a cobertura da QC7: {total} conceitos, {comuns} comuns",
        )
        res.exigir(
            re.search(rf"\b({divergentes}|oito)\b", minusculo) is not None,
            f"a secao 7 nao relata os {divergentes} conceitos em que os dois cenarios divergem",
        )

    # 3.3 consultas e resultados completos, nunca so sumarizados
    res.exigir(
        re.search(r"ap[êe]ndice", minusculo) is not None,
        "a secao 7 nao remete ao apendice das consultas e resultados completos",
    )
    res.exigir(
        re.search(r"dep[óo]sito", minusculo) is not None,
        "a secao 7 nao remete ao deposito aberto, onde os resultados completos estao",
    )
    res.exigir(
        re.search(r"complet", minusculo) is not None,
        "a secao 7 nao diz que consultas e resultados estao completos, e nao sumarizados",
    )
    # Registrar divergencia e dizer, no mesmo folego, contra o que ela foi
    # medida. So a palavra «divergencia» passaria por qualquer texto que fale da
    # QC7, que devolve divergencia por desenho.
    res.exigir(
        re.search(
            r"diverg\w*[\s\S]{0,200}(expectativa|esperad)|(expectativa|esperad)\w*[\s\S]{0,200}diverg",
            minusculo,
        )
        is not None,
        "a secao 7 nao registra as divergencias entre o que se esperava e o que a consulta "
        "devolveu",
    )
    res.exigir(
        re.search(r"desfavorec|contra o artefato|limite do modelo", minusculo) is not None,
        "a secao 7 nao diz que as divergencias registradas incluem as que desfavorecem o artefato",
    )

    # 3.4 o cenario, em terceira pessoa
    res.exigir(
        "sbsi_estendido" in chaves,
        "o cenario instanciado nao e referenciado pela publicacao que o documenta",
    )
    res.exigir(
        re.search(r"sint[ée]tic", minusculo) is not None,
        "a secao 7 nao diz que o segundo observatorio da comparacao e sintetico",
    )

    # 3.5 a segunda frente: conformidade a UFO e as regras estruturais
    res.exigir(
        re.search(r"conformidade", minusculo) is not None,
        "a secao 7 nao relata a frente de conformidade sintatica e semantica a UFO",
    )
    res.exigir(
        re.search(r"controle positivo", minusculo) is not None
        and re.search(r"muta[çc]", minusculo) is not None,
        "a secao 7 relata relatorio vazio sem o controle positivo — a mutacao conhecida — que o "
        "torna interpretavel",
    )
    totais = _totais_estruturais()
    if res.exigir(totais is not None, f"{ESTRUTURAL} nao pode ser lido: nada a conferir"):
        assert totais is not None
        for valor in totais:
            res.exigir(
                re.search(rf"\b{valor}\b", corpo) is not None,
                f"a secao 7 nao reporta o numero {valor} das regras estruturais "
                f"(as-is, rodada 1, rodada 2 = {totais})",
            )

    # 3.6 a terceira frente: os pitfalls
    res.exigir(
        "poveda2014oops" in chaves,
        "a frente de deteccao de pitfalls e relatada sem referencia a ferramenta",
    )
    oops = _totais_oops()
    if res.exigir(oops is not None, f"{COMPARACAO_OOPS} nao pode ser lido: nada a conferir"):
        assert oops is not None
        antes, depois, antes_dominio, depois_dominio = oops
        for valor, papel in (
            (antes, "o total antes"),
            (depois, "o total depois"),
            (antes_dominio, "os elementos de dominio antes"),
        ):
            res.exigir(
                re.search(rf"\b{valor}\b", corpo) is not None,
                f"a secao 7 nao reporta {papel} do OOPS! ({valor})",
            )
        res.exigir(
            re.search(rf"\b{depois_dominio}\b|zero", minusculo) is not None,
            "a secao 7 nao reporta os elementos de dominio que sobram depois",
        )


# --------------------------------------------------------------------------
# 4. a secao 8 — discussao e limitacoes
# --------------------------------------------------------------------------


LIMITACOES = {
    "ausencia de validacao com especialistas": r"especialistas",
    "o pano de fundo dos grupos focais e estudos de caso": r"grupos? focais|estudos? de caso",
    "o observatorio sintetico da comparacao": r"sint[ée]tic",
    "o unico formalizador": r"um formalizador|n=1|formaliza[çc][õo]es independentes",
    "a ausencia de implantacao operacional": r"implanta[çc][ãa]o operacional",
    "a ausencia de axiomatizacao pesada": r"axiomatiza[çc][ãa]o pesada",
}


def verificar_discussao(texto: str, res: Resultado) -> None:
    corpo = _corrido(texto)
    minusculo = corpo.lower()

    licoes = re.findall(r"\*\*([^*]{20,})\*\*", corpo)
    res.exigir(
        len(licoes) >= 3,
        f"a secao 8 traz {len(licoes)} licoes destacadas: a discussao precisa de licoes "
        "aprendidas, e um parecer criticou exatamente a sua ausencia",
    )
    res.exigir(
        re.search(r"linguagem natural|em prosa", minusculo) is not None,
        "a secao 8 nao diz o que a analise ensina sobre modelos de referencia descritos em prosa",
    )

    repetidos = [n for n in NUMEROS_DE_RESULTADO if re.search(rf"\b{n}\b", corpo)]
    res.exigir(
        not repetidos,
        f"a secao 8 repete numeros que a secao 7 ja relatou ({', '.join(repetidos)}): "
        "a discussao discute, nao resume",
    )

    for nome, padrao in LIMITACOES.items():
        res.exigir(
            re.search(padrao, minusculo) is not None,
            f"a secao 8 nao declara a limitacao: {nome}",
        )
    res.exigir(
        re.search(r"limita", minusculo) is not None,
        "a secao 8 nao nomeia as limitacoes como tais",
    )
    # A secao 7 relata o cenario; a 8 discute. Recita-lo aqui e redundancia.
    res.exigir(
        "sbsi_estendido" not in _chaves(texto),
        "a secao 8 recita o cenario de instanciacao, que e assunto da secao 7",
    )


# --------------------------------------------------------------------------
# 5. a secao 9 — conclusao e trabalhos futuros
# --------------------------------------------------------------------------


CONTRIBUICOES = {
    "base semantica verificavel para auditar aderencia": r"aderência",
    "rastreabilidade de proveniencia para prestacao de contas": r"proveni[êe]ncia",
    "procedimento reusavel de auditoria de modelos de referencia": r"procedimento",
}

FUTUROS = {
    "estudo comparativo entre observatorios reais": r"comparativ",
    "alinhamento com ontologias de gerenciamento de projetos": r"gerenciamento de projetos",
    "integracao com modelos de linguagem": r"modelos de linguagem|LLM",
}


def verificar_conclusao(texto: str, res: Resultado) -> None:
    corpo = _corrido(texto)
    minusculo = corpo.lower()
    chaves = _chaves(texto)

    for nome, padrao in CONTRIBUICOES.items():
        res.exigir(
            re.search(padrao, corpo, re.IGNORECASE) is not None,
            f"a conclusao nao entrega a contribuicao para SI: {nome}",
        )
    res.exigir(
        re.search(r"presta[çc][ãa]o de contas", minusculo) is not None,
        "a conclusao nao liga a rastreabilidade a prestacao de contas",
    )
    res.exigir(
        "grandsi" in minusculo and "araujo2025grandsi" in chaves,
        "a conclusao nao conecta o resultado ao II GranDSI-Br, com referencia",
    )
    res.exigir(
        re.search(r"desafio 3", minusculo) is not None,
        "a conclusao nao nomeia o desafio ao qual o resultado responde",
    )
    for nome, padrao in FUTUROS.items():
        res.exigir(
            re.search(padrao, corpo, re.IGNORECASE) is not None,
            f"os trabalhos futuros nao incluem: {nome}",
        )
    # Os modelos de linguagem sao direcao, nao resultado — decisao da spec.
    achado = re.search(r"[^.]*modelos de linguagem[^.]*\.", corpo, re.IGNORECASE)
    res.exigir(
        achado is not None
        and re.search(r"dire[çc][ãa]o|n[ãa]o como resultado", achado.group(0), re.IGNORECASE)
        is not None,
        "a integracao com modelos de linguagem nao esta declarada como direcao, e nao resultado",
    )


# --------------------------------------------------------------------------
# 6. a declaracao de uso de IA generativa
# --------------------------------------------------------------------------


def verificar_declaracao(texto: str, res: Resultado) -> None:
    corpo = _corrido(texto)
    minusculo = corpo.lower()

    res.exigir(
        re.search(r"IA generativa|intelig[êe]ncia artificial generativa", corpo, re.IGNORECASE)
        is not None,
        "a declaracao nao nomeia o uso de IA generativa",
    )
    res.exigir(
        "sbc" in minusculo and re.search(r"c[óo]digo de conduta", minusculo) is not None,
        "a declaracao nao invoca o Codigo de Conduta da SBC, que e o que a exige",
    )
    # Nomear a ferramenta e exigencia; um nome proprio de produto, e nao apenas
    # a categoria, e o que distingue declarar de aludir.
    res.exigir(
        re.search(r"\b(Claude|ChatGPT|GPT-[0-9]|Gemini|Copilot|Llama)\b", corpo) is not None,
        "a declaracao nao nomeia a ferramenta empregada",
    )
    empregos = ("código", "texto", "revis")
    faltando = [e for e in empregos if e not in minusculo]
    res.exigir(
        not faltando,
        f"a declaracao nao diz onde a ferramenta foi empregada: falta {', '.join(faltando)}",
    )
    res.exigir(
        re.search(r"n[ãa]o foi empregada|n[ãa]o foram gerados|n[ãa]o foi usada", minusculo)
        is not None,
        "a declaracao nao delimita onde a ferramenta NAO foi empregada",
    )
    res.exigir(
        re.search(r"responsabilidade|respondem por", minusculo) is not None,
        "a declaracao nao assume a responsabilidade pelo conteudo",
    )


# --------------------------------------------------------------------------
# 7. redundancia, citacoes, bibliografia e tom
# --------------------------------------------------------------------------


PALAVRAS_REPETIDAS = 12


def _sequencias(texto: str) -> dict[tuple[str, ...], str]:
    corpo = _normalizar(_sem_comentarios(texto))
    palavras = re.findall(r"[0-9a-zà-ÿ]+", corpo)
    n = PALAVRAS_REPETIDAS
    return {
        tuple(palavras[i : i + n]): " ".join(palavras[i : i + n])
        for i in range(max(0, len(palavras) - n + 1))
    }


def verificar_redundancia(
    textos: dict[str, str], anteriores: dict[str, str], res: Resultado
) -> None:
    todos = dict(anteriores)
    todos.update(textos)

    vistas: dict[tuple[str, ...], str] = {}
    repetidas: list[str] = []
    for numero, texto in sorted(todos.items()):
        for sequencia, legivel in _sequencias(texto).items():
            if sequencia in vistas and vistas[sequencia] != numero:
                repetidas.append(f"secoes {vistas[sequencia]} e {numero}: «{legivel[:70]}»")
            else:
                vistas.setdefault(sequencia, numero)
    res.exigir(
        not repetidas,
        f"conteudo repetido entre secoes ({PALAVRAS_REPETIDAS} palavras seguidas ou mais): "
        + "; ".join(repetidas[:3]),
    )

    citacoes: dict[str, str] = {}
    reusadas: list[str] = []
    for numero, texto in sorted(todos.items()):
        for citacao in _citacoes(texto):
            chave = _normalizar(citacao)
            if chave in citacoes and citacoes[chave] != numero:
                reusadas.append(f"secoes {citacoes[chave]} e {numero}: «{citacao[:50]}»")
            else:
                citacoes.setdefault(chave, numero)
    res.exigir(
        not reusadas, "a mesma citacao da fonte aparece em duas secoes: " + "; ".join(reusadas)
    )

    # O desenho da avaliacao e do metodo; o fechamento relata resultados.
    for numero, texto in sorted(textos.items()):
        for termo in TIPOLOGIA_FORA:
            res.exigir(
                termo not in _corrido(texto),
                f"a secao {numero} descreve «{termo}», que e assunto exclusivo do metodo",
            )


def verificar_citacoes(textos: dict[str, str], res: Resultado) -> None:
    fonte = " || ".join(_normalizar(_ler(caminho)) for caminho in FONTES)
    if not res.exigir(bool(fonte.strip()), "as fontes da dissertacao nao foram lidas"):
        return
    for numero, texto in sorted(textos.items()):
        for citacao in _citacoes(texto):
            res.exigir(
                _normalizar(citacao) in fonte,
                f"secao {numero}: citacao nao encontrada na fonte, palavra por palavra: "
                f"«{citacao[:60]}»",
            )


def verificar_bibliografia(diretorio: Path, textos: dict[str, str], res: Resultado) -> None:
    bib = _ler(diretorio / "referencias.bib")
    citadas: set[str] = set()
    for texto in textos.values():
        citadas |= _chaves(texto)
    faltando = sorted(c for c in citadas if f"{{{c}," not in bib)
    res.exigir(not faltando, f"chaves citadas sem entrada no .bib: {', '.join(faltando)}")


def verificar_tom(textos: dict[str, str], res: Resultado) -> None:
    for numero, texto in sorted(textos.items()):
        corpo = _corrido(texto)
        minusculo = corpo.lower()
        for padrao in ATRIBUICOES_PROIBIDAS:
            achado = re.search(padrao, corpo, re.IGNORECASE)
            res.exigir(
                achado is None,
                f"secao {numero}: a deficiencia e atribuida ao modelo em linguagem natural "
                f"(«{achado.group(0) if achado else ''}») — ela e da formalizacao publicada",
            )
        for termo in TERMOS_IDENTIFICADORES:
            res.exigir(
                termo not in minusculo, f"secao {numero}: mencao identificadora «{termo}»"
            )
        for padrao in LEVE:
            res.exigir(
                re.search(padrao, corpo, re.IGNORECASE) is None,
                f"secao {numero}: resquicio da defesa de ontologia leve, abandonada pelo spec",
            )
        achado = PRIMEIRA_PESSOA.search(corpo)
        res.exigir(
            achado is None,
            f"secao {numero}: primeira pessoa («{achado.group(0) if achado else ''}») — "
            "trabalhos do proprio autor sao citados em terceira pessoa",
        )


def main() -> int:
    diretorio = Path(sys.argv[1]) if len(sys.argv) > 1 else ARTIGO_PADRAO
    res = Resultado()

    textos: dict[str, str] = {}
    for numero, nome in list(SECOES.items()) + [("ia", DECLARACAO)]:
        caminho = diretorio / "secoes" / nome
        texto = _ler(caminho)
        if not res.exigir(bool(texto), f"{caminho} ausente ou vazio"):
            print(f"FALHOU: {res.falhas[-1]}")
            return 1
        textos[numero] = texto

    anteriores = {
        nome[:2]: _ler(diretorio / "secoes" / nome)
        for nome in ANTERIORES
        if (diretorio / "secoes" / nome).exists()
    }

    verificar_plano(diretorio, textos, res)
    verificar_ontologia_revisada(textos["06"], res)
    verificar_avaliacao(textos["07"], res)
    verificar_discussao(textos["08"], res)
    verificar_conclusao(textos["09"], res)
    verificar_declaracao(textos["ia"], res)
    verificar_redundancia(textos, anteriores, res)
    verificar_citacoes(textos, res)
    verificar_bibliografia(diretorio, textos, res)
    verificar_tom(textos, res)

    print(f"verificacoes: {res.checagens}")
    if res.falhas:
        print(f"FALHOU: {len(res.falhas)} problema(s)")
        for falha in res.falhas:
            print(f"  - {falha}")
        return 1
    print("OK: a checklist do ticket 12 esta cumprida")
    return 0


if __name__ == "__main__":
    sys.exit(main())
