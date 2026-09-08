#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera as figuras do artigo a partir do modelo revisado (ticket 13).

Uso: python tools/generation/gerar_figuras.py

As imagens que existiam eram do modelo **antigo**: reaproveita-las publicaria
diagramas que contradizem a secao de analise — o artigo mostraria os defeitos ao
lado da afirmacao de que foram corrigidos. Por isso nenhuma figura do artigo vem
de `sources/dissertation/`: todas sao desenhadas aqui, em TikZ, a partir de
`artifacts/ontology/rodada-2/ontompo-rodada-2.ontouml.json`.

O que e' derivado do modelo e o que e' escolha desta ferramenta:

  - **do modelo**: quais classes existem, o estereotipo de cada uma, quais
    generalizacoes e quais relacoes as ligam, e o estereotipo de cada relacao.
    Nada disso e' digitado aqui — sai do `.ontouml.json` a cada execucao, e o
    verificador do ticket 13 confere o TikZ gravado contra o modelo, sem
    importar deste arquivo;
  - **desta ferramenta**: onde cada caixa fica. Posicao e' decisao de leitura, e
    o `.ontouml.json` nao a carrega (o campo `diagrams` e' nulo). `POSICOES`
    abaixo e' essa decisao, e e' entrada da ferramenta, como `tools/model/`.

A geracao aborta se `POSICOES` e o modelo divergirem — classe posicionada que
nao existe, ou classe do modelo sem posicao. E' o que impede a figura de
sobreviver a uma rodada seguinte sem ser revista.

Saidas:

  - `artifacts/paper/figuras/ontompo-integrado.tex` — o diagrama integrado, que
    fica no artigo (§6);
  - `artifacts/paper/figuras/camada-{agentes,estruturas,processos}.tex` — os
    diagramas por camada. Pelo corte previsto na spec, eles nao entram no artigo
    quando a paginacao aperta: vao para o deposito, e e' para la' que
    `gerar_deposito.py` os copia.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

MODELO = Path("artifacts/ontology/rodada-2/ontompo-rodada-2.ontouml.json")
DESTINO = Path("artifacts/paper/figuras")

# Geometria do diagrama integrado, em centimetros. A largura util do texto no
# template SBC (a4paper, margens de 3cm) e' 15cm; seis colunas de 2,5cm cabem
# nela, e o nome mais longo do modelo ("ProjectDataManagement", 21 caracteres)
# mede 2,2cm com o corpo de 6pt, dentro do passo. O conjunto — caixas, fundo de
# camada e legenda — tem de caber nos 15cm, e o verificador do ticket 13 mede a
# figura compilada para conferir.
COLUNAS = 6
PASSO_X = 2.45
PASSO_Y = 0.80
LARGURA_CAIXA = 2.28
ALTURA_CAIXA = 0.52

# Corpo do texto dentro da figura. 6pt para o nome e 5pt para o estereotipo:
# e' o piso de legibilidade em impressao, e o verificador do ticket 13 reprova
# se alguem baixar daqui.
CORPO_NOME = 6
CORPO_ESTEREOTIPO = 5
CORPO_MINIMO = 5

# As tres camadas, na ordem em que aparecem de cima para baixo, com o rotulo que
# cada uma leva no diagrama.
CAMADAS = (
    ("agentes", "Agentes (UFO-C)"),
    ("estruturas", "Estruturas (UFO-A)"),
    ("processos", "Processos (UFO-B)"),
)

# Posicao de cada classe: camada, coluna (0 a 5) e linha dentro da camada.
# Escolhidas para que generalizacao desca na vertical e para que classes ligadas
# por relacao fiquem vizinhas.
POSICOES: dict[str, tuple[str, int, int]] = {
    # --- agentes -----------------------------------------------------------
    "Agent": ("agentes", 2, 0),
    "PhysicalAgent": ("agentes", 0, 1),
    "SocialAgent": ("agentes", 2, 1),
    "StakeHolder": ("agentes", 4, 1),
    "Person": ("agentes", 0, 2),
    "Organization": ("agentes", 2, 2),
    "ComputationalSystem": ("agentes", 3, 2),
    "ObservatoryGroup": ("agentes", 5, 2),
    "ObservatoryUser": ("agentes", 0, 3),
    "System": ("agentes", 3, 3),
    # --- estruturas --------------------------------------------------------
    "Software": ("estruturas", 0, 0),
    "Hardware": ("estruturas", 2, 0),
    "Network": ("estruturas", 3, 0),
    "Service": ("estruturas", 4, 0),
    "DataSource": ("estruturas", 5, 0),
    "ProjectObservatory": ("estruturas", 0, 1),
    "DataManager": ("estruturas", 1, 1),
    "View": ("estruturas", 2, 1),
    "SoftwareExecution": ("estruturas", 3, 1),
    "Connection": ("estruturas", 4, 1),
    "ServiceProvision": ("estruturas", 5, 1),
    "Collector": ("estruturas", 0, 2),
    "Processor": ("estruturas", 1, 2),
    "Storer": ("estruturas", 2, 2),
    "Disseminator": ("estruturas", 3, 2),
    "Reporter": ("estruturas", 4, 2),
    "CrudView": ("estruturas", 5, 2),
    "CrudRepository": ("estruturas", 0, 3),
    "ProjectDataManagement": ("estruturas", 1, 3),
    "ViewProvision": ("estruturas", 2, 3),
    "SocialInteraction": ("estruturas", 3, 3),
    "Log": ("estruturas", 4, 3),
    "Project": ("estruturas", 5, 3),
    "Knowledge": ("estruturas", 5, 4),
    # --- processos ---------------------------------------------------------
    "EtlProcess": ("processos", 0, 0),
    "CrudOperation": ("processos", 3, 0),
    "Observation": ("processos", 5, 0),
    "Extract": ("processos", 0, 1),
    "Transform": ("processos", 1, 1),
    "Load": ("processos", 2, 1),
    "CreateOperation": ("processos", 3, 1),
    "ReadOperation": ("processos", 4, 1),
    "UpdateOperation": ("processos", 5, 1),
    "DeleteOperation": ("processos", 3, 2),
}

# Como cada familia de aresta e' desenhada. A legenda do diagrama nomeia as
# cinco, e e' ela que dispensa rotular 56 arestas uma a uma.
FAMILIAS = {
    "generalizacao": ("generalização", "gen"),
    "parthood": ("«componentOf», «memberOf», «participational»", "parte"),
    "mediacao": ("«mediation»", "med"),
    "participacao": ("«participation»", "part"),
    "outras": ("«material», «creation», «derivation»", "outra"),
}

# Quantos itens da legenda cabem por linha sem que um rotulo invada o proximo.
LEGENDA_POR_LINHA = 3

FAMILIA_DE_ESTEREOTIPO = {
    "componentOf": "parthood",
    "memberOf": "parthood",
    "participational": "parthood",
    "mediation": "mediacao",
    "participation": "participacao",
    "material": "outras",
    "creation": "outras",
    "derivation": "outras",
}


class ErroDeFigura(Exception):
    """Modelo e layout divergiram, ou o modelo trouxe algo que o gerador nao desenha."""


def carregar(caminho: Path) -> dict:
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    conteudo = dados["model"]["contents"]
    por_id = {x["id"]: x for x in conteudo}

    classes = {}
    for x in conteudo:
        if x["type"] == "Class":
            classes[x["name"]] = x.get("stereotype") or ""

    generalizacoes = []
    for x in conteudo:
        if x["type"] == "Generalization":
            especifica = por_id[x["specific"]["id"]]["name"]
            geral = por_id[x["general"]["id"]]["name"]
            generalizacoes.append((especifica, geral))

    relacoes = []
    for x in conteudo:
        if x["type"] != "Relation":
            continue
        pontas = []
        for prop in x["properties"]:
            alvo = por_id.get(prop["propertyType"]["id"])
            pontas.append(alvo["name"] if alvo and alvo["type"] == "Class" else None)
        estereotipo = x.get("stereotype") or ""
        # A derivacao liga uma relacao a um relator, e nao duas classes: ela nao
        # tem as duas pontas no diagrama de classes, e nao vira aresta.
        if None in pontas:
            continue
        relacoes.append((pontas[0], pontas[1], estereotipo))

    return {"classes": classes, "generalizacoes": generalizacoes, "relacoes": relacoes}


def conferir_layout(classes: dict[str, str]) -> None:
    posicionadas = set(POSICOES)
    do_modelo = set(classes)
    sobrando = posicionadas - do_modelo
    faltando = do_modelo - posicionadas
    if sobrando:
        raise ErroDeFigura(
            "classe posicionada que nao existe no modelo revisado: " + ", ".join(sorted(sobrando))
        )
    if faltando:
        raise ErroDeFigura(
            "classe do modelo revisado sem posicao na figura: " + ", ".join(sorted(faltando))
        )
    ocupadas: dict[tuple[str, int, int], str] = {}
    for nome, chave in POSICOES.items():
        if chave in ocupadas:
            raise ErroDeFigura(f"{nome} e {ocupadas[chave]} ocupam a mesma celula {chave}")
        ocupadas[chave] = nome


def coordenadas(camadas_alturas: dict[str, int]) -> dict[str, tuple[float, float]]:
    """Converte (camada, coluna, linha) em (x, y) em centimetros."""
    inicio: dict[str, float] = {}
    y = 0.0
    for chave, _rotulo in CAMADAS:
        if chave not in camadas_alturas:
            continue
        inicio[chave] = y
        y -= (camadas_alturas[chave] + 1) * PASSO_Y
    saida = {}
    for nome, (camada, col, linha) in POSICOES.items():
        if camada not in inicio:
            continue
        saida[nome] = (col * PASSO_X, inicio[camada] - linha * PASSO_Y)
    return saida


def identificador(nome: str) -> str:
    return "n" + nome


def desenhar(modelo: dict, camadas: tuple[str, ...], titulo_legenda: bool) -> str:
    classes = {n: e for n, e in modelo["classes"].items() if POSICOES[n][0] in camadas}
    alturas = {}
    for nome in classes:
        camada, _col, linha = POSICOES[nome]
        alturas[camada] = max(alturas.get(camada, 0), linha)
    pos = coordenadas(alturas)

    linhas: list[str] = []
    linhas.append("% GERADO por tools/generation/gerar_figuras.py a partir de")
    linhas.append("% artifacts/ontology/rodada-2/ontompo-rodada-2.ontouml.json.")
    linhas.append("% Nao editar a mao: a proxima geracao desfaz.")
    linhas.append("\\begin{tikzpicture}[")
    linhas.append(f"  every node/.style={{font=\\fontsize{{{CORPO_NOME}}}{{{CORPO_NOME + 1}}}\\selectfont}},")
    linhas.append(
        "  classe/.style={draw, rectangle, rounded corners=1pt, inner sep=1pt,"
        f" minimum width={LARGURA_CAIXA}cm, minimum height={ALTURA_CAIXA}cm, align=center}},"
    )
    linhas.append("  gen/.style={draw, -{Triangle[open, length=3pt, width=3pt]}, thin},")
    linhas.append("  parte/.style={draw, -{Diamond[length=3pt, width=2.5pt]}, thin},")
    linhas.append("  med/.style={draw, dashed, dash pattern=on 2pt off 1.5pt, thin},")
    linhas.append("  part/.style={draw, dotted, thin},")
    linhas.append("  outra/.style={draw, gray, thin},")
    linhas.append("]")

    # fundo de cada camada
    for chave, rotulo in CAMADAS:
        if chave not in alturas:
            continue
        membros = [n for n in classes if POSICOES[n][0] == chave]
        xs = [pos[n][0] for n in membros]
        ys = [pos[n][1] for n in membros]
        x0 = min(xs) - LARGURA_CAIXA / 2 - 0.12
        x1 = max(xs) + LARGURA_CAIXA / 2 + 0.12
        y0 = min(ys) - ALTURA_CAIXA / 2 - 0.12
        y1 = max(ys) + ALTURA_CAIXA / 2 + 0.30
        linhas.append(
            f"\\fill[black!4, rounded corners=2pt] ({x0:.2f},{y0:.2f}) rectangle ({x1:.2f},{y1:.2f});"
        )
        linhas.append(
            f"\\node[anchor=north west, font=\\fontsize{{{CORPO_ESTEREOTIPO}}}"
            f"{{{CORPO_ESTEREOTIPO + 1}}}\\selectfont\\itshape, text=black!55]"
            f" at ({x0 + 0.06:.2f},{y1 - 0.02:.2f}) {{{rotulo}}};"
        )

    # caixas
    for nome, estereotipo in sorted(classes.items()):
        x, y = pos[nome]
        rotulo = (
            f"\\fontsize{{{CORPO_ESTEREOTIPO}}}{{{CORPO_ESTEREOTIPO + 1}}}\\selectfont"
            f"«{estereotipo}»\\\\\\fontsize{{{CORPO_NOME}}}{{{CORPO_NOME + 1}}}\\selectfont"
            f"\\textbf{{{nome}}}"
        )
        linhas.append(
            f"\\node[classe] ({identificador(nome)}) at ({x:.2f},{y:.2f}) {{{rotulo}}};"
        )

    # arestas
    desenhadas = 0
    for especifica, geral in modelo["generalizacoes"]:
        if especifica not in classes or geral not in classes:
            continue
        linhas.append(
            f"\\draw[gen] ({identificador(especifica)}) -- ({identificador(geral)});"
        )
        desenhadas += 1

    for origem, destino, estereotipo in modelo["relacoes"]:
        if origem not in classes or destino not in classes:
            continue
        familia = FAMILIA_DE_ESTEREOTIPO.get(estereotipo)
        if familia is None:
            raise ErroDeFigura(f"estereotipo de relacao sem estilo definido: «{estereotipo}»")
        estilo = FAMILIAS[familia][1]
        linhas.append(
            f"\\draw[{estilo}] ({identificador(origem)}) -- ({identificador(destino)});"
        )
        desenhadas += 1

    if titulo_legenda:
        xs = [p[0] for p in pos.values()]
        ys = [p[1] for p in pos.values()]
        y0 = min(ys) - ALTURA_CAIXA / 2 - 0.50
        x = min(xs) - LARGURA_CAIXA / 2
        largura = max(xs) - min(xs) + LARGURA_CAIXA
        passo = largura / LEGENDA_POR_LINHA
        for i, (rotulo, estilo) in enumerate(FAMILIAS.values()):
            xi = x + (i % LEGENDA_POR_LINHA) * passo
            yi = y0 - (i // LEGENDA_POR_LINHA) * 0.32
            linhas.append(
                f"\\draw[{estilo}] ({xi:.2f},{yi:.2f}) -- ({xi + 0.40:.2f},{yi:.2f});"
            )
            linhas.append(
                f"\\node[anchor=west, font=\\fontsize{{{CORPO_ESTEREOTIPO}}}"
                f"{{{CORPO_ESTEREOTIPO + 1}}}\\selectfont] at ({xi + 0.45:.2f},{yi:.2f})"
                f" {{{rotulo}}};"
            )

    linhas.append("\\end{tikzpicture}")
    return "\n".join(linhas) + "\n"


def main(argv: list[str]) -> int:
    if not MODELO.exists():
        print(f"erro: {MODELO} nao existe", file=sys.stderr)
        return 1
    modelo = carregar(MODELO)
    try:
        conferir_layout(modelo["classes"])
    except ErroDeFigura as e:
        print(f"erro: {e}", file=sys.stderr)
        return 1

    DESTINO.mkdir(parents=True, exist_ok=True)
    saidas = [("ontompo-integrado.tex", tuple(c for c, _ in CAMADAS), True)]
    for chave, _rotulo in CAMADAS:
        saidas.append((f"camada-{chave}.tex", (chave,), True))

    for nome, camadas, legenda in saidas:
        try:
            tikz = desenhar(modelo, camadas, legenda)
        except ErroDeFigura as e:
            print(f"erro: {e}", file=sys.stderr)
            return 1
        (DESTINO / nome).write_text(tikz, encoding="utf-8")
        print(f"gerado {DESTINO / nome}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
