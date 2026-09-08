#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifica as secoes 1 a 4 do artigo (checklist do ticket 11).

Uso: python tools/verification/verificar_seccoes_introducao_metodo.py [diretorio-do-artigo]

O texto das quatro primeiras secoes mora em `artifacts/paper/secoes/01-introducao.md`,
`02-referencial.md`, `03-trabalhos-relacionados.md` e `04-metodo.md`. Elas sao a
metade do artigo que estabelece o problema e justifica o desenho de pesquisa, e
cinco criticas do ONTOBRAS sao endereçadas ali: o artigo nao ser autocontido; a
terminologia de nicho nao posicionada; a redundancia entre secoes; a falta de
posicionamento frente a metodologias recentes; e a ausencia de ancoragem
teorica. Este verificador le esses textos como terceiro — sem importar do codigo
que produziu qualquer artefato — e confronta cada exigencia da checklist com a
fonte que a sustenta:

  1. as quatro secoes existem, o esqueleto aponta para cada uma e o orcamento de
     paginas que ele declara para cada uma e respeitado. A medida e a mesma do
     ticket 10 quando ha `pdflatex`: o texto e portado para o template SBC e
     compilado. Sem `pdflatex`, cai numa estimativa por linhas **calibrada pela
     medida compilada da secao 5**, que o proprio esqueleto registra;
  2. a introducao situa o trabalho no tripe, aponta dominio e problema
     organizacional, ancora a motivacao na Organizational Information Processing
     Theory, declara a contribuicao, nomeia o Desafio 3 e o Desafio 2 do II
     GranDSI-Br e traz o mapa do artigo;
  3. o referencial posiciona observatorios frente a gerenciamento de projetos,
     monitoramento e PMO; descreve o MPO de forma autocontida — as tres
     dimensoes, suas subdimensoes e os elementos que a secao 5 discute —;
     apresenta a tipologia de Representation Theory inteira; e cobre UFO-A,
     UFO-B e UFO-C;
  4. os trabalhos relacionados citam ontologias em contextos de observatorio e
     analises ontologicas de modelos conceituais, e **nomeiam a lacuna**;
  5. o metodo declara o envelope DSR, explicita a continuidade com o ciclo do
     proprio MPO, posiciona a Methontology frente a LOT e a NeOn, descreve o
     procedimento da analise e desenha a avaliacao nas tres frentes;
  6. **nao ha conteudo repetido entre secoes**: nenhuma sequencia de doze
     palavras reaparece em duas delas (a secao 5 entra na comparacao), nenhuma
     citacao verbatim e reusada e a Methontology so e descrita na secao 4;
  7. **toda aspa curva e citacao verbatim da fonte**, procurada com espacos
     normalizados em `sources/dissertation/` — o mesmo criterio do ticket 10;
  8. as referencias exigidas pela chamada e pelos pareceres estao citadas: Anais
     do SBSI, Anais Estendidos, iSys e II GranDSI-Br, e nenhuma chave citada
     falta no `.bib`;
  9. nada atribui as deficiencias ao MPO em linguagem natural, e nao ha mencao
     identificadora, primeira pessoa nem resquicio da defesa de ontologia leve —
     trabalhos do proprio autor entram em terceira pessoa.

Sai com codigo 1 se qualquer verificacao falhar.
"""

from __future__ import annotations

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

SECOES = {
    "01": "01-introducao.md",
    "02": "02-referencial.md",
    "03": "03-trabalhos-relacionados.md",
    "04": "04-metodo.md",
}

SECAO_5 = "05-analise-ontologica.md"

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

# Geometria do sbc-template: A4 com margens 3,5/2,5/3/3 cm da o corpo de 23,7 cm
# de altura, composto em 12/14 pt — 48 linhas por pagina. A largura de 15 cm em
# Times 12 pt cabe cerca de 93 caracteres. O fator de calibracao vem da secao 5,
# cuja medida compilada o esqueleto registra, de modo que a estimativa e ancorada
# num texto real e nao num palpite.
LINHAS_POR_PAGINA = 48.0
CARACTERES_POR_LINHA = 93.0

TIPOLOGIA = ("overload", "redundancy", "excess", "deficit")

# O tripe que a trilha cobra. "Procedimentos" e opcional porque as duas formas
# circulam na chamada; pessoas, processos e tecnologias nao sao.
TRIPE = ("pessoas", "processos", "tecnologias")

DIMENSOES = ("Estruturas", "Processos", "Agentes")

SUBDIMENSOES = ("Componentes", "Conteúdos", "Características", "Atores", "Motivações")

# Os elementos do MPO sobre os quais a analise da secao 5 se apoia. Um leitor que
# nunca ouviu falar do modelo precisa encontra-los aqui, e nao na secao 5.
ELEMENTOS_DO_MPO = (
    "Coleta",
    "Processamento",
    "Armazenamento",
    "Disseminação",
    "Relacionamento",
    "Hardware",
    "Software",
    "Gerenciamento de dados",
    "Coletar",
    "Tratar",
    "Armazenar",
    "Responsabilizar",
)

VIZINHOS = {
    "gerenciamento de projetos": r"gerenciamento de projetos",
    "monitoramento de projetos": r"monitoramento",
    "PMO": r"PMO|escrit[óo]rio de projetos",
}

# Atribuir a deficiencia ao MPO — ou ao modelo de referencia, que e o mesmo em
# outras palavras — e a alegacao falsificavel que o CONTEXT.md manda evitar: o
# MPO e prosa, e os construtos sao escolhas da formalizacao. A regra vale aqui
# pelo mesmo motivo que vale na secao 5.
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
)

LEVE = (r"ontologia\s+leve", r"lightweight\s+ontology")

# «nos» sem acento e preposicao em portugues, e por isso fica de fora.
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
    """O texto que vai para o artigo: sem os comentarios HTML de bastidor."""
    return re.sub(r"<!--.*?-->", "", texto, flags=re.S)


def _normalizar(texto: str) -> str:
    """Deixa comparavel um trecho de LaTeX e um trecho de Markdown."""
    texto = re.sub(r"\\[a-zA-Z]+\s*", "", texto)
    texto = texto.replace("{", "").replace("}", "").replace("~", " ")
    texto = texto.replace("``", '"').replace("''", '"')
    texto = unicodedata.normalize("NFC", texto)
    return re.sub(r"\s+", " ", texto).strip().lower()


def _corrido(texto: str) -> str:
    """O texto sem comentarios e com espaco colapsado.

    O Markdown quebra linha onde couber, e uma expressao do texto pode cair
    metade numa linha e metade na outra. Toda busca por expressao trabalha
    sobre esta forma, e nao sobre o arquivo cru.
    """
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


# --------------------------------------------------------------------------
# 1. o plano e o orcamento de paginas
# --------------------------------------------------------------------------


def _orcamentos(esqueleto: str) -> dict[str, float]:
    """Le a tabela de orcamento do esqueleto: numero da secao -> paginas."""
    orcamentos: dict[str, float] = {}
    for linha in esqueleto.splitlines():
        if not linha.strip().startswith("|"):
            continue
        colunas = [c.strip() for c in linha.strip().strip("|").split("|")]
        if len(colunas) < 3 or not re.fullmatch(r"\d{1,2}", colunas[0]):
            continue
        try:
            orcamentos[colunas[0].zfill(2)] = float(colunas[-1].replace(",", "."))
        except ValueError:
            continue
    return orcamentos


def _medida_da_secao_5(esqueleto: str) -> float | None:
    """A medida compilada da secao 5, que o esqueleto registra. E a regua."""
    achado = re.search(r"mede\s+\*\*([\d,]+)\s+páginas?\*\*", esqueleto)
    return float(achado.group(1).replace(",", ".")) if achado else None


def _linhas(markdown: str) -> float:
    """Linhas de 14 pt que o texto ocupa, por bloco do Markdown."""
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

def verificar_plano(diretorio: Path, textos: dict[str, str], res: Resultado) -> None:
    esqueleto = _ler(diretorio / "esqueleto.md")
    for numero, nome in SECOES.items():
        res.exigir(
            nome in esqueleto,
            f"o esqueleto nao aponta para secoes/{nome}: o ticket 13 nao acha o texto",
        )
    orcamentos = _orcamentos(esqueleto)
    if not res.exigir(
        all(n in orcamentos for n in SECOES),
        "orcamento de alguma das secoes 1 a 4 ausente na tabela do esqueleto",
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
        # Sem pdflatex: estimativa por linhas, calibrada pela medida compilada da
        # secao 5 que o esqueleto registra. Sem essa regua nao ha o que estimar.
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
    for numero in sorted(SECOES):
        paginas = medidas[numero]
        total += paginas
        print(f"  secao {numero}: {paginas:.2f} pagina(s), orcamento {orcamentos[numero]:.2f}")
        res.exigir(
            paginas <= orcamentos[numero],
            f"a secao {numero} mede {paginas:.2f} paginas e o esqueleto lhe da "
            f"{orcamentos[numero]:.2f}",
        )
    orcado = sum(orcamentos[n] for n in SECOES)
    print(f"  paginacao {origem}: {total:.2f} de {orcado:.2f} paginas")
    res.exigir(
        total <= orcado,
        f"as quatro secoes somam {total:.2f} paginas e o orcamento previsto e {orcado:.2f}",
    )


# --------------------------------------------------------------------------
# 2. a introducao
# --------------------------------------------------------------------------


def verificar_introducao(texto: str, res: Resultado) -> None:
    corpo = _corrido(texto)
    minusculo = corpo.lower()

    for termo in TRIPE:
        res.exigir(termo in minusculo, f"a introducao nao situa o trabalho no tripe: falta «{termo}»")
    res.exigir(
        re.search(r"dom[íi]nio de aplica[çc][ãa]o", minusculo) is not None,
        "a introducao nao aponta explicitamente o dominio de aplicacao",
    )
    res.exigir(
        re.search(r"problema organizacional", minusculo) is not None,
        "a introducao nao aponta explicitamente o problema organizacional",
    )
    res.exigir(
        "organizational information processing theory" in minusculo,
        "a Organizational Information Processing Theory nao e citada na motivacao",
    )
    res.exigir(
        bool(_chaves(texto) & {"galbraith1973designing", "galbraith1974organization"}),
        "a motivacao invoca a OIPT sem referenciar sua fonte",
    )
    res.exigir(
        "grandsi" in minusculo and "araujo2025grandsi" in _chaves(texto),
        "a contribuicao nao esta conectada ao II GranDSI-Br, com referencia",
    )
    res.exigir(
        re.search(r"desafio 3", minusculo) is not None
        and "eco(sistemas" in minusculo.replace(" ", ""),
        'o Desafio 3, "Eco(Sistemas²) de Informação", nao esta nomeado',
    )
    res.exigir(
        re.search(r"desafio 2", minusculo) is not None,
        "o Desafio 2 nao aparece como alinhamento secundario",
    )
    res.exigir(
        re.search(r"contribui[çc][ãa]o", minusculo) is not None
        and re.search(r"an[áa]lise ontol[óo]gica", minusculo) is not None
        and re.search(r"modelo revisado", minusculo) is not None,
        "a contribuicao declarada — a analise e o modelo revisado — nao esta explicita",
    )
    res.exigir(
        re.search(r"n[ãa]o (é|e) formalizar o MPO|n[ãa]o (é|e) a formaliza[çc][ãa]o", corpo)
        is not None,
        "a introducao nao diz que a contribuicao NAO e formalizar o MPO",
    )
    secoes_citadas = set(re.findall(r"§(\d)", corpo))
    res.exigir(
        len(secoes_citadas) >= 6,
        f"o mapa do artigo cita so {len(secoes_citadas)} secoes: o leitor nao sabe onde esta o que",
    )


# --------------------------------------------------------------------------
# 3. o referencial teorico
# --------------------------------------------------------------------------


def _subsecoes(texto: str) -> dict[str, str]:
    partes: dict[str, str] = {}
    titulo = "(abertura)"
    acumulado: list[str] = []
    for linha in _sem_comentarios(texto).splitlines():
        if linha.startswith("## "):
            partes[titulo] = "\n".join(acumulado)
            titulo = linha[3:].strip()
            acumulado = []
        else:
            acumulado.append(linha)
    partes[titulo] = "\n".join(acumulado)
    return partes


def verificar_referencial(texto: str, res: Resultado) -> None:
    corpo = _corrido(texto)
    minusculo = corpo.lower()
    partes = _subsecoes(texto)
    titulos = " | ".join(partes).lower()

    for esperado in ("observat", "modelo para observat", "representation theory", "ufo"):
        res.exigir(
            esperado in titulos,
            f"o referencial nao tem subsecao sobre «{esperado}»",
        )

    # 2.1 — a critica de terminologia de nicho
    for nome, padrao in VIZINHOS.items():
        res.exigir(
            re.search(padrao, corpo, re.IGNORECASE) is not None,
            f"observatorios nao sao posicionados frente a {nome}",
        )
    res.exigir(
        bool(_chaves(texto) & {"pmi2021pmbok", "turner2016gower"}),
        "o posicionamento frente a gerenciamento de projetos nao referencia a literatura da area",
    )

    # 2.2 — o MPO autocontido
    res.exigir("61 conceitos" in corpo, "a descricao do MPO nao diz quantos conceitos ele reune")
    for dimensao in DIMENSOES:
        res.exigir(dimensao in corpo, f"a dimensao {dimensao} do MPO nao esta descrita")
    for subdimensao in SUBDIMENSOES:
        res.exigir(
            subdimensao in corpo,
            f"a subdimensao {subdimensao} do MPO nao esta descrita",
        )
    faltando = [e for e in ELEMENTOS_DO_MPO if e not in corpo]
    res.exigir(
        not faltando,
        f"elementos do MPO que a analise discute e o referencial nao apresenta: "
        f"{', '.join(faltando)}",
    )

    # 2.3 — Representation Theory inteira
    for termo in TIPOLOGIA:
        res.exigir(
            termo in minusculo,
            f"a tipologia de Representation Theory esta incompleta: falta *construct {termo}*",
        )
    res.exigir(
        bool(_chaves(texto) & {"wand1993ontological", "wand1995deep", "weber1997ontological"}),
        "a Representation Theory e apresentada sem referencia a sua fonte",
    )

    # 2.4 — as tres microteorias
    for micro in ("UFO-A", "UFO-B", "UFO-C"):
        res.exigir(micro in corpo, f"o referencial nao cobre a {micro}")
    res.exigir("OntoUML" in corpo, "o referencial nao apresenta a OntoUML")


# --------------------------------------------------------------------------
# 4. trabalhos relacionados
# --------------------------------------------------------------------------


def verificar_relacionados(texto: str, res: Resultado) -> None:
    chaves = _chaves(texto)
    observatorios = {"chen2008apply", "fox2009ontology", "masmoudi2018ontology", "yoshiura2018towards"}
    faltando = sorted(observatorios - chaves)
    res.exigir(
        not faltando,
        f"ontologias em contextos de observatorio nao situadas: falta {', '.join(faltando)}",
    )
    analises = {
        "recker2011ontological",
        "guizzardi2005ontological",
        "gonccalves2011using",
        "mario2020handling",
        "detoni2019ontologia",
    }
    res.exigir(
        len(chaves & analises) >= 2,
        "nenhuma analise ontologica de modelos conceituais fundamentada em UFO ou BWW e citada",
    )
    corpo = _corrido(texto)
    res.exigir(
        re.search(r"lacuna", corpo, re.IGNORECASE) is not None,
        "a lacuna nao esta nomeada: o revisor de Novidade precisa le-la, nao inferi-la",
    )
    res.exigir(
        re.search(r"nenhum(a)?\b", corpo, re.IGNORECASE) is not None,
        "a lacuna nao diz o que nenhum dos trabalhos faz",
    )


# --------------------------------------------------------------------------
# 5. o metodo
# --------------------------------------------------------------------------


def verificar_metodo(texto: str, res: Resultado) -> None:
    corpo = _corrido(texto)
    minusculo = corpo.lower()
    chaves = _chaves(texto)

    res.exigir(
        "design science research" in minusculo,
        "o metodo nao declara o Design Science Research como envelope",
    )
    res.exigir(
        bool(chaves & {"hevner2004design", "peffers2007design"}),
        "o envelope DSR e declarado sem referencia",
    )
    res.exigir(
        re.search(r"ciclo", minusculo) is not None
        and bool(chaves & {"vieira2021model", "vieira2022evaluating", "vieira2023survey"}),
        "a continuidade com o ciclo DSR sob o qual o MPO foi construido nao esta explicitada",
    )
    res.exigir(
        "Methontology" in corpo and "fernandez1997methontology" in chaves,
        "o metodo de construcao do artefato nao esta declarado",
    )
    for alternativa, chave in (("LOT", "poveda2022lot"), ("NeOn", "suarez2012neon")):
        res.exigir(
            alternativa in corpo and chave in chaves,
            f"a Methontology nao e posicionada frente a {alternativa}",
        )
    res.exigir(
        re.search(r"linha de base", minusculo) is not None,
        "o procedimento da analise nao descreve a reconstrucao da linha de base",
    )
    res.exigir(
        re.search(r"contou como defici[êe]ncia", minusculo) is not None,
        "o metodo nao diz o que contou como deficiencia",
    )
    res.exigir(
        "wand1993ontological" in chaves,
        "o metodo nao diz como cada achado foi classificado na tipologia",
    )
    # as tres frentes da avaliacao
    res.exigir(
        re.search(r"quest[õo]es de compet[êe]ncia", minusculo) is not None
        and re.search(r"sete", minusculo) is not None,
        "a primeira frente da avaliacao — as sete questoes de competencia — nao esta desenhada",
    )
    res.exigir(
        re.search(r"conformidade", minusculo) is not None,
        "a segunda frente — a verificacao de conformidade a UFO — nao esta desenhada",
    )
    res.exigir(
        "poveda2014oops" in chaves,
        "a terceira frente — a deteccao de pitfalls na OWL — nao esta desenhada",
    )
    res.exigir(
        re.search(r"controle positivo", minusculo) is not None,
        "o desenho da avaliacao nao diz por que um relatorio vazio seria interpretavel",
    )
    res.exigir(
        "sbsi_estendido" in chaves,
        "o cenario de instanciacao nao e referenciado pela publicacao que o documenta",
    )


# --------------------------------------------------------------------------
# 6. redundancia entre secoes, citacoes e tom
# --------------------------------------------------------------------------


PALAVRAS_REPETIDAS = 12


def _sequencias(texto: str) -> dict[tuple[str, ...], str]:
    """As sequencias de PALAVRAS_REPETIDAS palavras seguidas do texto.

    Comparar frase com frase seria fragil: bastaria trocar a pontuacao final
    para o mesmo trecho passar por novo. Comparar sequencias de palavras — sem
    pontuacao, sem caixa e sem marcacao — pega o trecho copiado onde quer que
    ele comece.
    """
    corpo = _normalizar(_sem_comentarios(texto))
    palavras = re.findall(r"[0-9a-zà-ÿ]+", corpo)
    n = PALAVRAS_REPETIDAS
    return {
        tuple(palavras[i : i + n]): " ".join(palavras[i : i + n])
        for i in range(max(0, len(palavras) - n + 1))
    }


def verificar_redundancia(textos: dict[str, str], secao5: str, res: Resultado) -> None:
    todos = dict(textos)
    if secao5:
        todos["05"] = secao5

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

    # A redundancia entre o referencial e o metodo foi critica explicita de um
    # parecer, e ela tinha nome: Methontology descrita duas vezes.
    for numero in ("01", "02", "03"):
        res.exigir(
            "Methontology" not in _corrido(textos[numero]),
            f"a secao {numero} descreve a Methontology, que e assunto exclusivo do metodo",
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

    exigidas = {
        "Anais do SBSI": {"vieira2021model", "vieira2022evaluating", "vieira2023survey"},
        "Anais Estendidos do SBSI": {"sbsi_estendido"},
        "iSys": {"detoni2019ontologia"},
        "II GranDSI-Br": {"araujo2025grandsi"},
    }
    for veiculo, chaves in exigidas.items():
        res.exigir(
            bool(citadas & chaves),
            f"nenhuma referencia a {veiculo} nas secoes 1 a 4",
        )


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
    for numero, nome in SECOES.items():
        caminho = diretorio / "secoes" / nome
        texto = _ler(caminho)
        if not res.exigir(bool(texto), f"{caminho} ausente ou vazio"):
            print(f"FALHOU: {res.falhas[-1]}")
            return 1
        textos[numero] = texto

    verificar_plano(diretorio, textos, res)
    verificar_introducao(textos["01"], res)
    verificar_referencial(textos["02"], res)
    verificar_relacionados(textos["03"], res)
    verificar_metodo(textos["04"], res)
    verificar_redundancia(textos, _ler(diretorio / "secoes" / SECAO_5), res)
    verificar_citacoes(textos, res)
    verificar_bibliografia(diretorio, textos, res)
    verificar_tom(textos, res)

    print(f"verificacoes: {res.checagens}")
    if res.falhas:
        print(f"FALHOU: {len(res.falhas)} problema(s)")
        for falha in res.falhas:
            print(f"  - {falha}")
        return 1
    print("OK: a checklist do ticket 11 esta cumprida")
    return 0


if __name__ == "__main__":
    sys.exit(main())
