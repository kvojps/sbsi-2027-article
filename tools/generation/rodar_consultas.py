#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Executa as questoes de competencia em SPARQL sobre o cenario instanciado (tickets 07 e 08).

Uso: python tools/generation/rodar_consultas.py [diretorio-ontologia]

Carrega, num unico grafo:

  - a ontologia revisada e customizada (`owl/ontompo.ttl`);
  - a gUFO local (`sources/gufo/gufo.ttl`), que ela importa;
  - os dados de instancia do observatorio principal (`instancias/observatorio.ttl`);
  - os do segundo observatorio sintetico (`instancias/observatorio-b.ttl`), que
    so a QC7 atravessa — as demais QCs se prendem ao namespace do principal por
    um FILTER, entao carregar o segundo nao muda o resultado delas.

Roda cada `consultas/*.rq`, em ordem de nome, e grava ao lado de cada uma:

  - `<nome>-resultado.csv`   o resultado completo, cru, reaproveitavel;
  - `<nome>-resultado.md`    a pergunta, a consulta verbatim e a tabela.

Sem raciocinador: as consultas andam so sobre triplas afirmadas. Quando uma QC
precisa de inversa, ela usa a inversa nomeada que a customizacao C4 acrescentou,
ou um caminho `^` de propriedade — nunca inferencia.

A serializacao e deterministica: a ordem das linhas e a que o `ORDER BY` da
consulta define — nao e reordenada aqui, para que o artefato salvo reflita o
agrupamento que a consulta pediu — o terminador de linha e `\\n` em qualquer
plataforma, e nao ha BOM. Duas execucoes seguidas produzem arquivos identicos
byte a byte. Por isso **toda consulta precisa de um `ORDER BY` total**: sem ele,
a ordem das linhas depende do percurso do grafo e o artefato deixa de ser
reproduzivel.
"""

from __future__ import annotations

import csv
import io
import sys
from pathlib import Path

import rdflib

DIRETORIO_PADRAO = Path("artifacts/ontology")
GUFO_LOCAL = Path("sources/gufo/gufo.ttl")


def carregar_grafo(diretorio: Path) -> rdflib.Graph:
    grafo = rdflib.Graph()
    obrigatorios = (
        diretorio / "owl" / "ontompo.ttl",
        GUFO_LOCAL,
        diretorio / "instancias" / "observatorio.ttl",
        diretorio / "instancias" / "observatorio-b.ttl",
    )
    for caminho in obrigatorios:
        if not caminho.exists():
            raise FileNotFoundError(caminho)
        grafo.parse(caminho.as_posix(), format="turtle")
    return grafo


def termo_para_texto(termo) -> str:
    """Forma canonica de um termo para CSV/Markdown, estavel entre execucoes."""
    if isinstance(termo, rdflib.URIRef):
        return str(termo)
    if isinstance(termo, rdflib.Literal):
        return str(termo)
    if isinstance(termo, rdflib.BNode):
        return f"_:{termo}"
    return "" if termo is None else str(termo)


def cabecalho_da_consulta(texto: str) -> tuple[str, list[str]]:
    """Le o bloco de comentarios `#` do topo: primeira linha vira titulo, o resto, descricao."""
    linhas = []
    for linha in texto.splitlines():
        if linha.startswith("#"):
            conteudo = linha.lstrip("#").strip()
            if conteudo or linhas:
                linhas.append(conteudo)
        elif linha.strip() == "":
            if linhas:
                break
        else:
            break
    while linhas and linhas[-1] == "":
        linhas.pop()
    titulo = linhas[0] if linhas else ""
    corpo = [linha for linha in linhas[1:] if linha]
    return titulo, corpo


def executar(grafo: rdflib.Graph, texto: str) -> tuple[list[str], list[tuple[str, ...]]]:
    if "ORDER BY" not in texto.upper():
        raise ValueError("consulta sem ORDER BY: a ordem das linhas nao seria reproduzivel")
    resultado = grafo.query(texto)
    variaveis = [str(v) for v in resultado.vars]
    linhas = [
        tuple(termo_para_texto(linha[v]) for v in resultado.vars) for linha in resultado
    ]
    return variaveis, linhas


def escrever_csv(caminho: Path, variaveis: list[str], linhas: list[tuple[str, ...]]) -> str:
    buffer = io.StringIO()
    escritor = csv.writer(buffer, lineterminator="\n")
    escritor.writerow(variaveis)
    escritor.writerows(linhas)
    conteudo = buffer.getvalue()
    caminho.write_text(conteudo, encoding="utf-8", newline="\n")
    return conteudo


def escrever_md(
    caminho: Path,
    titulo: str,
    descricao: list[str],
    texto_consulta: str,
    variaveis: list[str],
    linhas: list[tuple[str, ...]],
    csv_nome: str,
) -> None:
    partes = [f"# {titulo}", ""]
    if descricao:
        partes.append(" ".join(descricao))
        partes.append("")
    partes += [
        "Executada por `tools/generation/rodar_consultas.py` sobre a ontologia revisada "
        "(`artifacts/ontology/owl/ontompo.ttl`), a gUFO (`sources/gufo/gufo.ttl`) e os dados "
        "de instância dos observatórios (`artifacts/ontology/instancias/observatorio.ttl` e "
        "`observatorio-b.ttl`). As QC1–QC6 se prendem ao namespace do observatório principal; "
        "só a QC7 atravessa os dois.",
        "",
        "## Consulta SPARQL",
        "",
        "```sparql",
        texto_consulta.rstrip("\n"),
        "```",
        "",
        f"## Resultado — {len(linhas)} linha(s)",
        "",
        "| " + " | ".join(variaveis) + " |",
        "|" + "|".join(["---"] * len(variaveis)) + "|",
    ]
    for linha in linhas:
        partes.append("| " + " | ".join(celula.replace("|", "\\|") for celula in linha) + " |")
    partes += ["", f"_Resultado completo, cru, em `{csv_nome}`._", ""]
    caminho.write_text("\n".join(partes), encoding="utf-8", newline="\n")


def main() -> int:
    diretorio = Path(sys.argv[1]) if len(sys.argv) > 1 else DIRETORIO_PADRAO
    consultas_dir = diretorio / "consultas"
    if not consultas_dir.is_dir():
        print(f"ERRO: {consultas_dir} nao existe.")
        return 1

    grafo = carregar_grafo(diretorio)
    arquivos = sorted(consultas_dir.glob("*.rq"))
    if not arquivos:
        print(f"ERRO: nenhuma consulta em {consultas_dir}.")
        return 1

    for caminho_rq in arquivos:
        texto = caminho_rq.read_text(encoding="utf-8")
        titulo, descricao = cabecalho_da_consulta(texto)
        variaveis, linhas = executar(grafo, texto)
        csv_nome = f"{caminho_rq.stem}-resultado.csv"
        escrever_csv(consultas_dir / csv_nome, variaveis, linhas)
        escrever_md(
            consultas_dir / f"{caminho_rq.stem}-resultado.md",
            titulo,
            descricao,
            texto,
            variaveis,
            linhas,
            csv_nome,
        )
        print(f"{caminho_rq.name}: {len(linhas)} linha(s) -> {csv_nome}, {caminho_rq.stem}-resultado.md")

    return 0


if __name__ == "__main__":
    sys.exit(main())
