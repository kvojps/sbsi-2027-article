#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifica a consistencia da OWL por raciocinador, com controle positivo.

Uso: python tools/verification/raciocinador.py [diretorio-ontologia]

Roda o mesmo raciocinador sobre as duas metades do ticket 06 — a OWL **gerada**
pela transformacao gUFO e a OWL **customizada** — junto com a gUFO local, e
grava `relatorio-raciocinador.md` e `.json` em `artifacts/ontology/owl/`.

Um relatorio de consistencia vazio nao e interpretavel sozinho: pode significar
"nada errado" ou "raciocinador que nunca acusa". Por isso cada execucao aplica
tambem uma bateria de **mutacoes**, cada uma um individuo que viola uma
disjuncao que a ontologia afirma, e exige o resultado esperado de cada uma nos
dois artefatos. E o mesmo controle positivo que `controle-verificacao.js` faz
para o plugin OntoUML.

As mutacoes tambem sao a **medicao da customizacao**: metade e acusada nos dois
artefatos, porque viola algo que a transformacao ou a gUFO ja afirmavam; a outra
metade so e acusada no customizado, porque viola o que a C3 e a C4
acrescentaram. A coluna "gerada" nao acusar e o resultado, nao a falha.

Sobre o raciocinador: `owlrl` implementa o perfil **OWL 2 RL** sobre a rdflib.
Foi escolhido por ser o unico raciocinador disponivel sem Java, e o que ele nao
cobre esta escrito no relatorio — nao e pouco, e vale dizer.

Sai com codigo 1 se algum artefato for inconsistente ou se alguma mutacao nao
produzir o resultado esperado.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import rdflib
from rdflib import RDF, Namespace, URIRef

try:
    import owlrl
except ImportError as erro:  # pragma: no cover - dependencia ausente
    print(f"ERRO: dependencia ausente ({erro.name}). Rode: pip install rdflib owlrl")
    sys.exit(1)

ONTOLOGIA_PADRAO = Path("artifacts/ontology/owl")
CUSTOMIZADA = Path("artifacts/ontology/owl/ontompo.ttl")
GERADA = Path("artifacts/ontology/rodada-2/ontompo-rodada-2.ttl")
GUFO_LOCAL = Path("sources/gufo/gufo.ttl")

ONTOMPO = Namespace("https://example.org/ontompo/rodada-2#")
TESTE = Namespace("https://example.org/ontompo/controle#")

# O owlrl publica inconsistencia como tripla de erro, com este predicado.
ERRO = URIRef("http://www.daml.org/2002/03/agents/agent-ont#error")

ARTEFATOS = [("gerada", GERADA), ("customizada", CUSTOMIZADA)]

# (nome, triplas da mutacao, acusada na gerada?, o que a sustenta)
MUTACOES = [
    (
        "um indivíduo que é `PhysicalAgent` e `SocialAgent`",
        [(TESTE.a, RDF.type, ONTOMPO.PhysicalAgent), (TESTE.a, RDF.type, ONTOMPO.SocialAgent)],
        True,
        "a partição `agentNature`, que a adoção de UFO-C (A6) introduziu e a transformação "
        "carrega para o OWL",
    ),
    (
        "um indivíduo que é `CreateOperation` e `DeleteOperation`",
        [(TESTE.b, RDF.type, ONTOMPO.CreateOperation), (TESTE.b, RDF.type, ONTOMPO.DeleteOperation)],
        True,
        "a partição `crudOperationType`, que a decomposição de A1 introduziu",
    ),
    (
        "um indivíduo que é `Person` e `Observation`",
        [(TESTE.c, RDF.type, ONTOMPO.Person), (TESTE.c, RDF.type, ONTOMPO.Observation)],
        True,
        "`gufo:Endurant` disjunto de `gufo:Event`, na ontologia de fundamentação — é o que dá "
        "dentes à adoção de UFO-B (A5, B8): antes da rodada 2, `Observation` era um relator "
        "endurante e a mutação passaria",
    ),
    (
        "uma `Observation` da qual um `Load` participa como agente",
        [(TESTE.d, RDF.type, ONTOMPO.Load), (TESTE.d, ONTOMPO.participation_Agent_Observation, TESTE.e)],
        True,
        "o domínio de `participation_Agent_Observation` é `Agent`, endurante, e `Load` é evento "
        "— mostra que domínio e alcance gerados têm consequência, e não são decoração",
    ),
    (
        "um indivíduo que é `Project` e `DataSource`",
        [(TESTE.f, RDF.type, ONTOMPO.Project), (TESTE.f, RDF.type, ONTOMPO.DataSource)],
        False,
        "a disjunção entre «kind» acrescentada pela **C3** — dois princípios de identidade "
        "distintos não valem para o mesmo indivíduo. `Person` e `Organization` não serviriam "
        "de controle aqui: a partição `agentNature` já os separava",
    ),
    (
        "um indivíduo que é `Hardware` e `Network`",
        [(TESTE.g, RDF.type, ONTOMPO.Hardware), (TESTE.g, RDF.type, ONTOMPO.Network)],
        False,
        "a mesma disjunção entre «kind» da **C3**, agora na camada de infraestrutura",
    ),
    (
        "um `DataManager` que é o próprio `ProjectObservatory`",
        [
            (TESTE.h, RDF.type, ONTOMPO.DataManager),
            (TESTE.h, RDF.type, ONTOMPO.ProjectObservatory),
        ],
        False,
        "a disjunção entre os subtipos de `Software` acrescentada pela **C3**, que fecha o que "
        "sobrou de A9",
    ),
    (
        "uma `Observation` que tem um `Load` por participante",
        [
            (TESTE.i, RDF.type, ONTOMPO.Load),
            (TESTE.j, ONTOMPO.hasParticipant_Observation_Agent, TESTE.i),
        ],
        False,
        "a inversa nomeada acrescentada pela **C4**: no artefato gerado a propriedade não "
        "existe, e a mutação não diz nada",
    ),
]


def carregar(caminho: Path, gufo: rdflib.Graph) -> rdflib.Graph:
    grafo = rdflib.Graph()
    grafo.parse(caminho.as_posix(), format="turtle")
    for tripla in gufo:
        grafo.add(tripla)
    return grafo


def inconsistencias(grafo: rdflib.Graph) -> list[str]:
    """Fecha o grafo sob OWL 2 RL e devolve as inconsistencias, ordenadas."""
    copia = rdflib.Graph()
    for tripla in grafo:
        copia.add(tripla)
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(copia)
    return sorted({str(objeto) for objeto in copia.objects(None, ERRO)})


LIMITACOES = """O raciocinador é o `owlrl`, que implementa o perfil **OWL 2 RL** sobre a rdflib.
Foi escolhido porque é o único disponível sem uma máquina virtual Java — o HermiT e o Pellet, que a
`owlready2` empacota, exigem uma. A escolha tem preço, e ele precisa estar escrito:

- **Restrições de cardinalidade qualificada ficam fora do perfil.** O artefato tem 40
  `owl:Restriction`, das quais 24 com `owl:minQualifiedCardinality` e 7 com
  `owl:qualifiedCardinality`, todas em posição de superclasse — que é onde o OWL 2 RL não as
  avalia. Um indivíduo que violasse uma dessas cardinalidades passaria por aqui. É a maior lacuna
  desta verificação, e ela cobre justamente o que a transformação gUFO gera a partir das
  multiplicidades do modelo OntoUML.
- **A verificação é sobre a base de conhecimento, não sobre a satisfatibilidade dos conceitos.** Um
  raciocinador DL diria se alguma classe é necessariamente vazia mesmo sem instância nenhuma; o
  OWL 2 RL só acusa quando há um indivíduo que viola. É por isso que cada mutação introduz um
  indivíduo: sem ele, não há o que acusar.
- **As anotações da C2 e as declarações da C1 não têm conteúdo lógico**, e por isso não têm controle
  positivo aqui. Não é omissão: não há o que um raciocinador possa dizer sobre um `rdfs:comment`. O
  que mede a C1 é o relatório do OOPS!, onde P34 e P35 caem; o que mede a C2 é o mesmo relatório,
  onde P08 cai.

O que a verificação cobre, dito com precisão: **nenhuma disjunção, subsunção, domínio ou alcance
declarado nos dois artefatos entra em contradição com os demais nem com a gUFO**, e a bateria de
mutações mostra que a verificação acusaria se entrasse."""


def relatorio_markdown(resultado: dict) -> str:
    linhas = [
        "# Consistência da OWL, por raciocinador",
        "",
        "Derivado dos artefatos a cada execução de `tools/verification/raciocinador.py`, com a "
        "gUFO local de `sources/gufo/`. Saída bruta em `relatorio-raciocinador.json`.",
        "",
        "## Consistência",
        "",
        "| Artefato | Triplas (com a gUFO) | Inconsistências |",
        "|---|---|---|",
    ]
    for nome, dados in resultado["artefatos"].items():
        linhas.append(f"| {nome} | {dados['triplas']} | {len(dados['inconsistencias'])} |")
    linhas.append("")
    if all(not d["inconsistencias"] for d in resultado["artefatos"].values()):
        linhas.append(
            "As duas são consistentes. A customização não introduziu contradição: era o risco "
            "real da **C3**, que declara disjuntos dezoito «kind» de uma vez."
        )
    else:
        linhas.append("**Há inconsistência.** Ver o detalhamento abaixo.")
        for nome, dados in resultado["artefatos"].items():
            for mensagem in dados["inconsistencias"]:
                linhas.append(f"- `{nome}`: {mensagem}")
    linhas.append("")
    linhas.append("## Controle positivo")
    linhas.append("")
    linhas.append(
        "Cada linha é uma mutação aplicada aos dois artefatos, e cada uma tem de dar o resultado "
        "esperado. As quatro primeiras são acusadas nos dois, porque violam algo que a "
        "transformação ou a gUFO já afirmavam; as quatro últimas só no customizado, e é isso que "
        "a customização acrescentou de conteúdo lógico."
    )
    linhas.append("")
    linhas.append("| Mutação | gerada | customizada | O que a sustenta |")
    linhas.append("|---|---|---|---|")
    for controle in resultado["controles"]:
        marca = {True: "acusada", False: "não acusada"}
        linhas.append(
            f"| {controle['mutacao']} | {marca[controle['gerada']]} | "
            f"{marca[controle['customizada']]} | {controle['sustenta']} |"
        )
    linhas.append("")
    if resultado["falhas"]:
        linhas.append("**Controles que não deram o esperado:**")
        linhas.append("")
        for falha in resultado["falhas"]:
            linhas.append(f"- {falha}")
        linhas.append("")
    else:
        linhas.append(
            "Todos os controles deram o esperado, o que torna interpretável o zero da tabela "
            "acima."
        )
        linhas.append("")
    linhas.append("## O que esta verificação não cobre")
    linhas.append("")
    linhas.append(LIMITACOES)
    linhas.append("")
    return "\n".join(linhas) + "\n"


def main() -> int:
    saida = Path(sys.argv[1]) if len(sys.argv) > 1 else ONTOLOGIA_PADRAO

    for caminho in (CUSTOMIZADA, GERADA, GUFO_LOCAL):
        if not caminho.exists():
            print(f"ERRO: {caminho} nao existe. Rode antes: python tools/generation/customizar_owl.py")
            return 1

    gufo = rdflib.Graph()
    gufo.parse(GUFO_LOCAL.as_posix(), format="turtle")

    grafos = {nome: carregar(caminho, gufo) for nome, caminho in ARTEFATOS}

    resultado: dict = {"artefatos": {}, "controles": [], "falhas": []}
    for nome, grafo in grafos.items():
        achados = inconsistencias(grafo)
        resultado["artefatos"][nome] = {"triplas": len(grafo), "inconsistencias": achados}
        if achados:
            resultado["falhas"].append(f"`{nome}` e inconsistente sem nenhuma mutacao")

    for mutacao, triplas, esperado_na_gerada, sustenta in MUTACOES:
        linha = {"mutacao": mutacao, "sustenta": sustenta, "esperado_na_gerada": esperado_na_gerada}
        for nome, grafo in grafos.items():
            mutante = rdflib.Graph()
            for tripla in grafo:
                mutante.add(tripla)
            for tripla in triplas:
                mutante.add(tripla)
            linha[nome] = bool(inconsistencias(mutante))
        if linha["customizada"] is not True:
            resultado["falhas"].append(
                f"a mutacao «{mutacao}» nao foi acusada na OWL customizada: "
                "sem ela, o zero do relatorio nao e interpretavel"
            )
        if linha["gerada"] is not esperado_na_gerada:
            resultado["falhas"].append(
                f"a mutacao «{mutacao}» deu {linha['gerada']} na OWL gerada, "
                f"e o esperado era {esperado_na_gerada}"
            )
        resultado["controles"].append(linha)

    saida.mkdir(parents=True, exist_ok=True)
    (saida / "relatorio-raciocinador.json").write_text(
        f"{json.dumps(resultado, indent=2, ensure_ascii=False)}\n", encoding="utf-8"
    )
    (saida / "relatorio-raciocinador.md").write_text(
        relatorio_markdown(resultado), encoding="utf-8"
    )

    for nome, dados in resultado["artefatos"].items():
        print(f"{nome:12} -> {len(dados['inconsistencias'])} inconsistencia(s)")
    for controle in resultado["controles"]:
        print(
            f"  controle gerada={controle['gerada']!s:5} "
            f"customizada={controle['customizada']!s:5}  {controle['mutacao']}"
        )
    if resultado["falhas"]:
        print(f"\nFALHOU: {len(resultado['falhas'])} problema(s)")
        for falha in resultado["falhas"]:
            print(f"  - {falha}")
        return 1
    print("\nOK: consistentes, e os controles acusam o que deviam")
    return 0


if __name__ == "__main__":
    sys.exit(main())
