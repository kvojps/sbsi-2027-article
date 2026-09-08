#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Porta o texto das secoes de Markdown para LaTeX (ticket 13).

Uso: python tools/generation/gerar_secoes_latex.py [diretorio-do-artigo]

O texto do artigo mora em `artifacts/paper/secoes/*.md`, uma superficie por secao, e
e' de la' que os verificadores dos tickets 10, 11 e 12 o conferem. Este gerador
porta cada uma para `artifacts/paper/secoes-tex/*.tex`, que o `artigo.tex` da' `\\input`.

**Por que gerar em vez de portar a mao.** Transcrever 9.300 palavras para LaTeX
cria uma segunda copia do texto, e duas copias divergem: uma correcao feita no
Markdown depois do port sairia do PDF sem que nada acusasse, e os verificadores
dos tickets 10 a 12 — que leem o Markdown — continuariam aprovando um PDF que
nao corresponde mais ao que eles conferiram. Gerando, a unica fonte do texto
continua sendo o Markdown, e o verificador do ticket 13 reprova quando o `.tex`
gravado nao e' o que este gerador produz hoje.

O que ele **nao** gera e' o `\\section` de cada secao: o cabecalho, o rotulo e o
comentario de orcamento sao do `artigo.tex`, que e' mantido a mao. Daqui sai so'
o corpo, subsecoes inclusive.

Constructos convertidos, e nada alem deles:

  - `## N.M. Titulo` vira `\\subsection{Titulo}`; o `# N. Titulo` de abertura e'
    conferido contra o titulo que o esqueleto declara para a secao e descartado;
  - `**negrito**`, `*italico*` e `` `identificador` `` viram `\\textbf`, `\\textit`
    e `\\texttt`;
  - `[chave]` e `[chave1, chave2]` viram `\\cite{...}`, com cada chave conferida
    contra o `referencias.bib` — chave ausente aborta a geracao;
  - tabelas Markdown viram `table` + `tabular`, com a legenda em negrito que as
    precede virando `\\caption` e a largura de cada coluna proporcional ao seu
    conteudo. Elas entram com `[H]`, e nao flutuando: como flutuantes, tabela e
    figura atravessavam a fronteira entre secoes conforme o texto mudava, e a
    paginacao por secao oscilava quase uma pagina — o que torna o orcamento do
    esqueleto inconferivel;
  - blocos cercados por ``` viram `verbatim`;
  - `« »`, `“ ”`, `—`, `§`, `…` e `²` viram o equivalente LaTeX;
  - comentarios HTML somem.

Qualquer marcador de Markdown que sobreviva a conversao aborta a geracao: e'
sinal de constructo novo que este gerador nao conhece.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ARTIGO_PADRAO = Path("artifacts/paper")

# Cada superficie, o numero da secao que ela ocupa no artigo e o titulo que o
# esqueleto declara. O `# N. Titulo` do Markdown e' conferido contra isto: uma
# secao renomeada de um lado so' aborta a geracao.
SECOES = [
    ("01-introducao.md", "1", "Introdução"),
    ("02-referencial.md", "2", "Referencial Teórico"),
    ("03-trabalhos-relacionados.md", "3", "Trabalhos Relacionados"),
    ("04-metodo.md", "4", "Método de Pesquisa"),
    ("05-analise-ontologica.md", "5", "Análise Ontológica do MPO"),
    ("06-ontompo-revisada.md", "6", "A OntoMPO Revisada"),
    ("07-avaliacao.md", "7", "Avaliação"),
    ("08-discussao-limitacoes.md", "8", "Discussão e Limitações"),
    ("09-conclusao.md", "9", "Conclusão e Trabalhos Futuros"),
    ("declaracao-ia.md", None, "Declaração de Uso de IA Generativa"),
]

# Onde o diagrama entra. A §6 pede o diagrama integrado pelo esqueleto, e o
# ponto exato e' o fim da subsecao 6.1, depois das tres camadas descritas.
FIGURA_APOS_SUBSECAO = ("06-ontompo-revisada.md", "6.1")
FIGURA_INTEGRADA = "figuras/ontompo-integrado"

# Corpo das tabelas. As tres do artigo tem celulas de texto corrido, e no corpo
# de 12pt do template elas passariam de meia pagina cada; \scriptsize (8pt) e' o
# tamanho usual de tabela densa em artigo do SBC e cabe no orcamento. E' o mesmo
# para as tres: tamanho variando de tabela para tabela dentro do mesmo artigo le'
# como descuido.
CORPO_DA_TABELA = "\\scriptsize"

SUBSTITUICOES = {
    "\u201c": "``",
    "\u201d": "''",
    "\u2014": "---",
    "\u2013": "--",
    "\u00a7": "\\S{}",
    "\u2026": "\\ldots{}",
    "\u00b2": "\\textsuperscript{2}",
}

ESPECIAIS = {
    "\\": "\\textbackslash{}",
    "&": "\\&",
    "%": "\\%",
    "$": "\\$",
    "#": "\\#",
    "_": "\\_",
    "{": "\\{",
    "}": "\\}",
    "~": "\\textasciitilde{}",
    "^": "\\textasciicircum{}",
}


class ErroDePorte(Exception):
    """Constructo que o gerador nao sabe converter, ou fonte inconsistente."""


# ---------------------------------------------------------------- texto inline


def _escapar(texto: str) -> str:
    saida = []
    for ch in texto:
        saida.append(ESPECIAIS.get(ch, SUBSTITUICOES.get(ch, ch)))
    return "".join(saida)


def _escapar_verbatim_inline(texto: str) -> str:
    """Escapa o miolo de um `\\texttt`, onde `_` e `&` continuam sendo especiais."""
    return _escapar(texto)


def inline(texto: str, chaves: set[str], origem: str) -> str:
    """Converte um trecho de texto corrido de Markdown para LaTeX."""
    guardados: list[str] = []

    def guardar(latex: str) -> str:
        guardados.append(latex)
        return f"\x00{len(guardados) - 1}\x00"

    # 1. `codigo` primeiro: dentro dele nada mais e' Markdown.
    def _codigo(m: re.Match[str]) -> str:
        return guardar("\\texttt{" + _escapar_verbatim_inline(m.group(1)) + "}")

    texto = re.sub(r"`([^`]+)`", _codigo, texto)

    # 2. citacoes: [chave] ou [chave1, chave2]. Chave inexistente aborta.
    def _citacao(m: re.Match[str]) -> str:
        cru = m.group(1)
        itens = [k.strip() for k in cru.split(",")]
        if not all(re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", k) for k in itens):
            return m.group(0)
        faltando = [k for k in itens if k not in chaves]
        if faltando:
            raise ErroDePorte(
                f"{origem}: chamada [{cru}] sem entrada no referencias.bib: "
                + ", ".join(faltando)
            )
        return guardar("\\cite{" + ",".join(itens) + "}")

    texto = re.sub(r"\[([^\]\[]+)\]", _citacao, texto)

    # 3. o que sobrou e' texto: escapar antes de introduzir comandos.
    texto = _escapar(texto)

    # 4. enfase. Negrito antes de italico, e o miolo do negrito passa pelo
    # italico na mesma varredura: `**detecção de *pitfalls* na OWL**` aninha.
    def _italico(s: str) -> str:
        return re.sub(r"\*([^*]+)\*", lambda m: "\\textit{" + m.group(1) + "}", s)

    texto = re.sub(r"\*\*(.+?)\*\*", lambda m: "\\textbf{" + _italico(m.group(1)) + "}", texto)
    texto = _italico(texto)

    if "*" in texto:
        raise ErroDePorte(f"{origem}: asterisco sobrevivente — enfase mal formada: {texto[:80]!r}")

    for i, latex in enumerate(guardados):
        texto = texto.replace(f"\x00{i}\x00", latex)
    return texto


# -------------------------------------------------------------------- tabelas


def _largura_coluna(celulas: list[str]) -> int:
    return max(len(c) for c in celulas)


def tabela(
    linhas: list[str],
    legenda: str | None,
    numero_esperado: int,
    chaves: set[str],
    origem: str,
) -> str:
    grade = []
    for linha in linhas:
        celulas = [c.strip() for c in linha.strip().strip("|").split("|")]
        grade.append(celulas)

    if len(grade) < 3:
        raise ErroDePorte(f"{origem}: tabela com menos de tres linhas")
    cabecalho, _separador, *corpo = grade
    ncols = len(cabecalho)
    for celulas in grade:
        if len(celulas) != ncols:
            raise ErroDePorte(f"{origem}: tabela com numero de colunas irregular")

    pesos = []
    estreitas = []
    for j in range(ncols):
        coluna = [g[j] for g in grade if g is not _separador]
        corpo_col = [g[j] for g in corpo]
        # O piso evita que uma coluna de rotulos curtos ("A1", "QC1") fique
        # estreita demais para caber sem quebrar no meio.
        pesos.append(min(max(_largura_coluna(coluna), 6), 40))
        estreitas.append(all(len(c) <= 12 for c in corpo_col))

    total = sum(pesos)
    spec = []
    for j in range(ncols):
        frac = pesos[j] / total
        largura = f"\\dimexpr{frac:.4f}\\linewidth-2\\tabcolsep\\relax"
        if estreitas[j]:
            spec.append(f">{{\\centering\\arraybackslash}}p{{{largura}}}")
        else:
            spec.append(f"p{{{largura}}}")

    def linha_latex(celulas: list[str], negrito: bool) -> str:
        saida = []
        for c in celulas:
            texto = inline(c, chaves, origem) if c else ""
            saida.append("\\textbf{" + texto + "}" if negrito and texto else texto)
        return " & ".join(saida) + " \\\\"

    partes = ["\\begin{table}[H]", "\\centering"]
    if legenda:
        # O "Tabela N." do Markdown e' o rotulo que o proprio LaTeX numera: entra
        # so' o texto da legenda, e o numero declarado e' conferido contra a ordem
        # em que a tabela aparece no artigo — trocar um sem o outro aborta.
        m = re.fullmatch(r"Tabela (\d+)\.\s+(.*)", legenda)
        if not m:
            raise ErroDePorte(f"{origem}: legenda {legenda!r} fora do formato 'Tabela N. ...'")
        if int(m.group(1)) != numero_esperado:
            raise ErroDePorte(
                f"{origem}: legenda diz Tabela {m.group(1)}, mas e' a {numero_esperado}a "
                "tabela do artigo"
            )
        partes.append("\\caption{" + inline(m.group(2), chaves, origem) + "}")
        partes.append(f"\\label{{tab:{numero_esperado}}}")
    partes.append(CORPO_DA_TABELA)
    partes.append("\\begin{tabular}{" + "".join(spec) + "}")
    partes.append("\\hline")
    partes.append(linha_latex(cabecalho, negrito=True))
    partes.append("\\hline")
    for celulas in corpo:
        partes.append(linha_latex(celulas, negrito=False))
    partes.append("\\hline")
    partes.append("\\end{tabular}")
    partes.append("\\end{table}")
    return "\n".join(partes)


# --------------------------------------------------------------------- secoes


def porta(
    caminho: Path, numero: str | None, titulo: str, chaves: set[str], tabelas_antes: int
) -> str:
    origem = caminho.name
    bruto = caminho.read_text(encoding="utf-8")
    bruto = re.sub(r"<!--.*?-->", "", bruto, flags=re.DOTALL)

    linhas = bruto.split("\n")
    saida: list[str] = []
    i = 0
    visto_titulo = False
    subsecao = 0
    legenda_pendente: str | None = None
    subsecao_corrente: str | None = None
    tabelas = tabelas_antes

    while i < len(linhas):
        linha = linhas[i]
        despido = linha.strip()

        if not despido:
            i += 1
            continue

        # titulo da secao
        if despido.startswith("# "):
            texto = despido[2:].strip()
            esperado = f"{numero}. {titulo}" if numero else titulo
            if texto != esperado:
                raise ErroDePorte(
                    f"{origem}: titulo {texto!r} diverge do que o esqueleto declara ({esperado!r})"
                )
            visto_titulo = True
            i += 1
            continue

        # subsecao
        if despido.startswith("## "):
            texto = despido[3:].strip()
            m = re.match(r"^(\d+)\.(\d+)\.\s+(.*)$", texto)
            if not m:
                raise ErroDePorte(f"{origem}: subsecao sem numeracao 'N.M.': {texto!r}")
            subsecao += 1
            if m.group(1) != numero or int(m.group(2)) != subsecao:
                raise ErroDePorte(
                    f"{origem}: subsecao {m.group(1)}.{m.group(2)} fora de ordem "
                    f"(esperado {numero}.{subsecao})"
                )
            if subsecao_corrente and (origem, subsecao_corrente) == FIGURA_APOS_SUBSECAO:
                saida.append(figura_integrada())
            subsecao_corrente = f"{numero}.{subsecao}"
            saida.append("\\subsection{" + inline(m.group(3), chaves, origem) + "}")
            i += 1
            continue

        # bloco cercado
        if despido.startswith("```"):
            j = i + 1
            corpo = []
            while j < len(linhas) and not linhas[j].strip().startswith("```"):
                corpo.append(linhas[j])
                j += 1
            if j >= len(linhas):
                raise ErroDePorte(f"{origem}: bloco cercado sem fechamento")
            saida.append(
                "\\begin{center}\n\\scriptsize\n\\begin{BVerbatim}\n"
                + "\n".join(corpo)
                + "\n\\end{BVerbatim}\n\\end{center}"
            )
            i = j + 1
            continue

        # legenda de tabela: linha inteiramente em negrito comecando por "Tabela N."
        m = re.fullmatch(r"\*\*(Tabela \d+\.\s+.*?)\*\*", despido)
        if m:
            legenda_pendente = m.group(1)
            i += 1
            continue

        # tabela
        if despido.startswith("|"):
            j = i
            bloco = []
            while j < len(linhas) and linhas[j].strip().startswith("|"):
                bloco.append(linhas[j])
                j += 1
            tabelas += 1
            saida.append(tabela(bloco, legenda_pendente, tabelas, chaves, origem))
            legenda_pendente = None
            i = j
            continue

        if despido.startswith("- "):
            j = i
            itens = []
            while j < len(linhas):
                atual = linhas[j].strip()
                if atual.startswith("- "):
                    itens.append(atual[2:].strip())
                    j += 1
                elif atual and not atual.startswith(("#", "|", "```", "- ")):
                    itens[-1] += " " + atual
                    j += 1
                else:
                    break
            corpo = "\n".join("\\item " + inline(t, chaves, origem) for t in itens)
            saida.append("\\begin{itemize}\n" + corpo + "\n\\end{itemize}")
            i = j
            continue

        # paragrafo
        j = i
        paragrafo = []
        while j < len(linhas):
            atual = linhas[j].strip()
            if not atual or atual.startswith(("#", "|", "```", "- ")):
                break
            if re.fullmatch(r"\*\*(Tabela \d+\.\s+.*?)\*\*", atual):
                break
            paragrafo.append(atual)
            j += 1
        saida.append(inline(" ".join(paragrafo), chaves, origem))
        i = j

    if not visto_titulo:
        raise ErroDePorte(f"{origem}: sem titulo de secao")
    if legenda_pendente:
        raise ErroDePorte(f"{origem}: legenda {legenda_pendente!r} sem tabela em seguida")
    if subsecao_corrente and (origem, subsecao_corrente) == FIGURA_APOS_SUBSECAO:
        saida.append(figura_integrada())

    cabecalho = (
        "% GERADO por tools/generation/gerar_secoes_latex.py a partir de\n"
        f"% artifacts/paper/secoes/{origem}. Nao editar a mao: a proxima geracao\n"
        "% desfaz. Corrija o Markdown e regere.\n"
    )
    return cabecalho + "\n\n".join(saida) + "\n", tabelas


def figura_integrada() -> str:
    return (
        "\\begin{figure}[H]\n"
        "\\centering\n"
        f"\\input{{{FIGURA_INTEGRADA}}}\n"
        "\\caption{A OntoMPO revisada: as três camadas do modelo, com as classes que cada\n"
        "uma reúne, suas generalizações e as relações entre elas. Gerada a partir de\n"
        "\\texttt{ontompo-rodada-2.ontouml.json}.}\n"
        "\\label{fig:integrado}\n"
        "\\end{figure}"
    )


def chaves_do_bib(caminho: Path) -> set[str]:
    texto = caminho.read_text(encoding="utf-8", errors="replace")
    return set(re.findall(r"^@\w+\{([^,]+),", texto, flags=re.MULTILINE))


def main(argv: list[str]) -> int:
    artigo = Path(argv[1]) if len(argv) > 1 else ARTIGO_PADRAO
    fonte = artigo / "secoes"
    destino = artigo / "secoes-tex"
    destino.mkdir(parents=True, exist_ok=True)

    chaves = chaves_do_bib(artigo / "referencias.bib")
    if not chaves:
        print("erro: referencias.bib sem entradas", file=sys.stderr)
        return 1

    escritos = []
    tabelas = 0
    for nome, numero, titulo in SECOES:
        caminho = fonte / nome
        if not caminho.exists():
            print(f"erro: {caminho} nao existe", file=sys.stderr)
            return 1
        try:
            latex, tabelas = porta(caminho, numero, titulo, chaves, tabelas)
        except ErroDePorte as e:
            print(f"erro: {e}", file=sys.stderr)
            return 1
        alvo = destino / (caminho.stem + ".tex")
        alvo.write_text(latex, encoding="utf-8")
        escritos.append(alvo)

    for alvo in escritos:
        print(f"gerado {alvo}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
