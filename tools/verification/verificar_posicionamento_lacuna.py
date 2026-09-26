#!/usr/bin/env python3
"""Verifica o posicionamento e a lacuna do ticket 15.

Uso: python tools/verification/verificar_posicionamento_lacuna.py [diretorio-do-artigo]

Le o manuscrito como terceiro: confirma as duas referencias acrescentadas, a
comparacao por eixos, a declaracao positiva da lacuna, as tres contribuicoes e
a localizacao anonima da formalizacao que serve de linha de base.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ARTIGO_PADRAO = Path("artifacts/paper")


def ler(caminho: Path) -> str:
    try:
        return caminho.read_text(encoding="utf-8")
    except OSError:
        return ""


def sem_comentarios(texto: str) -> str:
    return re.sub(r"<!--.*?-->", "", texto, flags=re.S)


def exigir(condicao: bool, mensagem: str, falhas: list[str]) -> None:
    if not condicao:
        falhas.append(mensagem)


def entrada_bib(texto: str, chave: str) -> str:
    inicio = re.search(rf"@\w+\{{{re.escape(chave)},", texto, re.I)
    if not inicio:
        return ""
    proxima = re.search(r"\n@\w+\{", texto[inicio.end() :])
    fim = inicio.end() + proxima.start() if proxima else len(texto)
    return texto[inicio.start() : fim]


def main() -> int:
    diretorio = Path(sys.argv[1]) if len(sys.argv) > 1 else ARTIGO_PADRAO
    secoes = diretorio / "secoes"
    introducao = sem_comentarios(ler(secoes / "01-introducao.md"))
    relacionados = sem_comentarios(ler(secoes / "03-trabalhos-relacionados.md"))
    analise = sem_comentarios(ler(secoes / "05-analise-ontologica.md"))
    bib = ler(diretorio / "referencias.bib")
    falhas: list[str] = []

    mpo = entrada_bib(bib, "farias2025conceptual")
    viral = entrada_bib(bib, "bernasconi2022semantic")
    exigir(bool(mpo), "falta a entrada da publicacao consolidada do MPO", falhas)
    exigir(bool(viral), "falta a entrada de Bernasconi et al. (2022)", falhas)
    exigir(all(c in mpo for c in ("IEEE", "Access", "129143--129160", "10.1109/ACCESS.2025.3589743")),
           "entrada do MPO sem metadados completos conferidos", falhas)
    exigir(all(c in viral for c in ("BMC", "Bioinformatics", "10.1186/s12859-022-05022-0")),
           "entrada de Bernasconi et al. sem metadados completos", falhas)
    exigir("farias2025conceptual" in introducao, "introducao nao cita a publicacao consolidada do MPO", falhas)
    exigir("bernasconi2022semantic" in relacionados, "comparador metodologico nao esta citado", falhas)

    for cabecalho in ("Objeto", "Fundamentação", "Traço à fonte", "Artefato e avaliação"):
        exigir(cabecalho in relacionados, f"quadro comparativo sem coluna {cabecalho!r}", falhas)
    for linha in ("Ontologias de observatórios", "*Ontological unpacking*", "Este trabalho"):
        exigir(linha in relacionados, f"quadro comparativo sem linha {linha!r}", falhas)
    exigir("A lacuna é positiva e delimitada" in relacionados,
           "lacuna nao esta declarada em termos positivos e delimitados", falhas)
    exigir("nenhum trabalho" not in relacionados.lower(),
           "secao repete alegacao universal de inexistencia", falhas)

    for contribuicao in ("procedimento reusável", "OntoMPO revisada", "pacote de evidências reexecutáveis"):
        exigir(contribuicao in introducao, f"introducao nao enumera {contribuicao}", falhas)
    # A composição LaTeX pode quebrar a expressão ao fim da linha; a presença
    # editorial não depende dessa quebra tipográfica.
    introducao_corrido = re.sub(r"\s+", " ", introducao)
    analise_corrido = re.sub(r"\s+", " ", analise)
    exigir("artefato suplementar anônimo" in introducao_corrido and "artefato suplementar anônimo" in analise_corrido,
           "formalizacao analisada nao esta localizavel pelo artefato suplementar anonimo", falhas)

    if falhas:
        for falha in falhas:
            print(f"FALHOU: {falha}")
        return 1
    print("PASSOU: ticket 15 — posicionamento, lacuna e fontes verificaveis")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
