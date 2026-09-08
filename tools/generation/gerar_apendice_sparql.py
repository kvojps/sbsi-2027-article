#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera o Apendice A — consultas SPARQL e resultados (ticket 13).

Uso: python tools/generation/gerar_apendice_sparql.py

O esqueleto orca uma pagina para o apendice, e as sete consultas somam 273
linhas: elas nao cabem. A checklist do ticket admite as duas formas — "as
consultas SPARQL e resultados completos, **ou** remissao explicita ao deposito"
—, e o apendice faz as duas coisas na proporcao que a pagina permite: traz na
integra a consulta que sustenta a tese do artigo, a QC7, e remete
explicitamente ao deposito para as outras seis e para o resultado completo de
cada uma, nomeando o caminho de cada arquivo e o script que as reexecuta.

Sumarizar os resultados aqui seria devolver ao leitor a avaliacao
irreproduzivel que o artigo critica; e' por isso que a remissao nomeia arquivo
por arquivo em vez de dizer "os resultados estao no deposito".

Nada e' digitado: o corpo da consulta sai de `artifacts/ontology/consultas/qc7.rq`
e o numero de linhas de cada resultado, do `.csv` correspondente. Trocar um
numero aqui sem trocar o artefato e' impossivel — nao ha numero aqui.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

CONSULTAS = Path("artifacts/ontology/consultas")
DESTINO = Path("artifacts/paper/apendice-sparql.tex")

# A consulta que vai na integra. E' a que sustenta a contribuicao — comparabilidade
# entre iniciativas — e a unica cujo resultado o texto discute coluna a coluna.
NA_INTEGRA = "qc7"

QCS = [f"qc{i}" for i in range(1, 8)]


def linhas_do_resultado(qc: str) -> int:
    caminho = CONSULTAS / f"{qc}-resultado.csv"
    with caminho.open(encoding="utf-8", newline="") as f:
        return max(sum(1 for _ in csv.reader(f)) - 1, 0)


def corpo_da_consulta(qc: str) -> str:
    """O texto da consulta sem o cabecalho de comentarios, que o artigo ja diz."""
    linhas = (CONSULTAS / f"{qc}.rq").read_text(encoding="utf-8").split("\n")
    for i, linha in enumerate(linhas):
        if not linha.startswith("#"):
            return "\n".join(linhas[i:]).strip("\n")
    raise SystemExit(f"erro: {qc}.rq nao tem corpo alem dos comentarios")


def main(argv: list[str]) -> int:
    if not CONSULTAS.is_dir():
        print(f"erro: {CONSULTAS} nao existe", file=sys.stderr)
        return 1

    contagens = {qc: linhas_do_resultado(qc) for qc in QCS}
    total = sum(contagens.values())
    listagem = ", ".join(
        f"{qc.upper()} ({contagens[qc]})" for qc in QCS
    )

    partes = [
        "% GERADO por tools/generation/gerar_apendice_sparql.py a partir de",
        "% artifacts/ontology/consultas/. Nao editar a mao: a proxima geracao desfaz.",
        "\\section*{Apêndice A -- Consultas SPARQL e Resultados}",
        "\\label{sec:apendice-sparql}",
        "",
        "As sete consultas e seus resultados completos acompanham o depósito aberto citado na "
        "Seção~\\ref{sec:avaliacao}, em \\texttt{ontology/consultas/}: \\texttt{qcN.rq} traz a "
        "consulta como foi executada, com o comentário que declara o cenário e o construto que ela "
        "percorre, e \\texttt{qcN-resultado.csv}, o resultado íntegro, sem recorte nem agregação. "
        "O script \\texttt{reexecutar-consultas.py}, na raiz do depósito, reexecuta as sete e "
        "confere cada uma contra o \\texttt{.csv} gravado. As linhas devolvidas por questão são "
        f"{listagem}, {total} ao todo, e "
        "\\texttt{ontology/consultas/divergencias.md} registra, questão a questão, a expectativa "
        "escrita antes da execução e em que o resultado divergiu dela.",
        "",
        "Vai abaixo, na íntegra, a QC7 --- \\textit{dois observatórios distintos que se dizem "
        "aderentes ao MPO cobrem os mesmos conceitos?} ---, de que a contribuição depende: para cada "
        "conceito da ontologia revisada ela conta os indivíduos de cada observatório que o "
        "instanciam, direta ou por subclasse, e as linhas em que uma contagem é zero e a outra não "
        "são os conceitos em que as duas iniciativas divergem.",
        "",
        # `Verbatim`, e nao `BVerbatim`: o corpo da consulta tem 28 linhas e a
        # caixa do BVerbatim e' indivisivel — quando ela nao cabe no que resta da
        # pagina, vai inteira para a seguinte e deixa meia pagina em branco, o
        # que custava uma pagina no total. O Verbatim quebra.
        "\\begin{Verbatim}[fontsize=\\tiny, xleftmargin=1.2cm]",
        corpo_da_consulta(NA_INTEGRA),
        "\\end{Verbatim}",
        "",
    ]

    DESTINO.write_text("\n".join(partes), encoding="utf-8")
    print(f"gerado {DESTINO}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
