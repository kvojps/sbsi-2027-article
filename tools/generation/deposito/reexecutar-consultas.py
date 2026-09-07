#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reexecuta as sete questoes de competencia sobre os arquivos deste deposito.

Uso: python reexecutar-consultas.py

Requisito unico: rdflib 7.x  (pip install "rdflib>=7,<8")

Para cada `ontology/consultas/qcN.rq`, carrega num unico grafo a OWL revisada
(`ontology/owl/ontompo.ttl`), a gUFO local (`gufo/gufo.ttl`) e os dados de
instancia dos dois observatorios, executa a consulta e compara o resultado,
linha a linha, com o `ontology/consultas/qcN-resultado.csv` gravado no deposito.
Sai com codigo 1 se qualquer consulta divergir do resultado gravado.

As consultas andam so sobre triplas afirmadas — sem raciocinador —, exatamente
como foram geradas. Toda consulta precisa de um `ORDER BY` total: sem ele a
ordem das linhas dependeria do percurso do grafo e a comparacao com o `.csv`
gravado nao seria reproduzivel.

Este arquivo e a fonte de `tools/generation/deposito/`; `gerar_deposito.py` o
copia para a raiz do deposito. Fora do deposito ele nao roda — os caminhos sao
relativos a propria pasta.
"""

from __future__ import annotations

import csv
import sys
from pathlib import Path

import rdflib

AQUI = Path(__file__).resolve().parent
GRAFOS = [
    AQUI / "ontology" / "owl" / "ontompo.ttl",
    AQUI / "gufo" / "gufo.ttl",
    AQUI / "ontology" / "instancias" / "observatorio.ttl",
    AQUI / "ontology" / "instancias" / "observatorio-b.ttl",
]


def termo(valor: object) -> str:
    if isinstance(valor, rdflib.BNode):
        return f"_:{valor}"
    return "" if valor is None else str(valor)


def main() -> int:
    grafo = rdflib.Graph()
    for caminho in GRAFOS:
        if not caminho.exists():
            print(f"FALTA: {caminho}")
            return 1
        grafo.parse(caminho.as_posix(), format="turtle")

    consultas = sorted((AQUI / "ontology" / "consultas").glob("qc*.rq"))
    if not consultas:
        print("nenhuma consulta encontrada")
        return 1

    divergiu = False
    for rq in consultas:
        texto = rq.read_text(encoding="utf-8")
        if "ORDER BY" not in texto.upper():
            print(f"FALHOU {rq.name}: consulta sem ORDER BY — resultado nao reproduzivel")
            divergiu = True
            continue

        esperado_csv = rq.with_name(f"{rq.stem}-resultado.csv")
        resultado = grafo.query(texto)
        variaveis = [str(v) for v in resultado.vars]
        obtidas = [[termo(linha[v]) for v in resultado.vars] for linha in resultado]

        with esperado_csv.open(encoding="utf-8", newline="") as fh:
            linhas_csv = list(csv.reader(fh))
        cabecalho, esperadas = linhas_csv[0], [list(l) for l in linhas_csv[1:]]

        ok = cabecalho == variaveis and esperadas == obtidas
        print(f"{'OK  ' if ok else 'FALHOU'} {rq.name}: {len(obtidas)} linha(s) "
              f"(gravado: {len(esperadas)})")
        if not ok:
            divergiu = True
            print(f"     cabecalho obtido:  {variaveis}")
            print(f"     cabecalho gravado: {cabecalho}")
            for i, (a, b) in enumerate(zip(obtidas, esperadas)):
                if a != b:
                    print(f"     linha {i}: obtido {a} != gravado {b}")

    if divergiu:
        print("\nDIVERGENCIA: ao menos uma consulta nao reproduz o resultado gravado.")
        return 1
    print("\nOK: as sete consultas reproduzem, linha a linha, os resultados gravados.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
