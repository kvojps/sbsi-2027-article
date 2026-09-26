#!/usr/bin/env python3
"""Verifica RQs e a calibração da evidência do ticket 16.

Uso: python tools/verification/verificar_perguntas_pesquisa_evidencia.py

Lê apenas o corpo do manuscrito. O abstract e os metadados do JEMS3 são
deliberadamente excluídos: são registro congelado e não são objeto deste ticket.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


RAIZ = Path("artifacts/paper/secoes")


def ler(nome: str) -> str:
    return (RAIZ / nome).read_text(encoding="utf-8")


def exigir(condicao: bool, mensagem: str, falhas: list[str]) -> None:
    if not condicao:
        falhas.append(mensagem)


def corrido(texto: str) -> str:
    return re.sub(r"\s+", " ", texto)


def tabela_1(analise: str) -> list[list[str]]:
    linhas: list[list[str]] = []
    for linha in analise.splitlines():
        celulas = [c.strip() for c in linha.strip().strip("|").split("|")]
        if len(celulas) == 6 and re.fullmatch(r"A[1-9]", celulas[0]):
            linhas.append(celulas)
    return linhas


def main() -> int:
    introducao = corrido(ler("01-introducao.md"))
    metodo = corrido(ler("04-metodo.md"))
    analise = ler("05-analise-ontologica.md")
    avaliacao = corrido(ler("07-avaliacao.md"))
    discussao = ler("08-discussao-limitacoes.md")
    conclusao = corrido(ler("09-conclusao.md"))
    falhas: list[str] = []

    exigir("RQ1:" in introducao and "pontos de abertura do MPO" in introducao,
           "introducao nao formula a RQ1 sobre os pontos de abertura do MPO", falhas)
    exigir("RQ2:" in introducao and "representação, consulta e comparação" in introducao,
           "introducao nao formula a RQ2 sobre capacidades no cenário", falhas)
    exigir("não eficácia" in introducao and "validação em produção" in introducao,
           "introducao nao calibra o alcance da RQ2", falhas)

    for passo in ("Reconstrução", "Leitura", "Qualificação", "Classificação"):
        exigir(passo in metodo, f"metodo nao preserva o passo {passo} da RQ1", falhas)
    exigir("respondem à **RQ1**" in metodo,
           "metodo nao associa a reconstrucao, leitura, qualificacao e classificacao a RQ1", falhas)
    for termo in ("questões de competência", "controle positivo", "conformidade estrutural", "qualidade da implementação OWL"):
        exigir(termo in metodo, f"metodo nao distingue a funcao probatoria de {termo}", falhas)

    cabecalho = "| # | Fonte textual | Decisão da formalização | Problema ontológico | Correção | Classificação |"
    exigir(cabecalho in analise, "Tabela 1 nao explicita a cadeia completa de evidencias", falhas)
    linhas = tabela_1(analise)
    exigir({linha[0] for linha in linhas} == {f"A{i}" for i in range(1, 10)},
           "Tabela 1 nao contem A1--A9 uma vez cada", falhas)
    exigir(all(all(c for c in linha[1:]) for linha in linhas),
           "Tabela 1 tem celula vazia na cadeia de evidencia", falhas)

    for termo in ("capacidade do artefato no cenário", "conformidade estrutural", "qualidade da implementação OWL"):
        exigir(termo in avaliacao, f"avaliacao nao separa evidencia de {termo}", falhas)
    exigir("controle positivo" in metodo and "relatório vazio" in metodo,
           "metodo nao limita a leitura de relatorio vazio de ferramenta", falhas)
    exigir("cenário controlado" in avaliacao and "não prova aderência de observatórios reais" in avaliacao,
           "QC7 nao esta calibrada como comparacao de cobertura no cenário", falhas)

    for limite in ("Não houve validação com especialistas", "Há um formalizador", "sintético", "implantação operacional"):
        exigir(limite in discussao, f"discussao nao declara a limitacao: {limite}", falhas)
    for termo in ("À **RQ1**", "À **RQ2**", "permite desvios", "demonstra, no cenário avaliado", "oferece base"):
        exigir(termo in conclusao, f"conclusao nao responde/calibra: {termo}", falhas)

    if falhas:
        for falha in falhas:
            print(f"FALHOU: {falha}")
        return 1
    print("PASSOU: ticket 16 — RQs, cadeia de evidencia e alcance calibrado")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
