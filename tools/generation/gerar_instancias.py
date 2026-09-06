#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Monta os dados de instancia do observatorio, para a avaliacao funcional (ticket 07).

Uso: python tools/generation/gerar_instancias.py [diretorio-de-saida]

O cenario e um observatorio de projetos de pesquisa e extensao de uma
universidade publica brasileira, descrito nos **Anais Estendidos do XVIII SBSI
(2022)**, DOI 10.5753/sbsi_estendido.2022.222995. E trabalho anterior do proprio
autor: toda mencao aqui — IRIs, rotulos, comentarios — e em **terceira pessoa** e
nao identifica autoria nem instituicao.

Cada instancia deriva de um trecho da publicacao. O mapa trecho -> instancia
esta em `artifacts/ontology/instancias/procedencia.md`, legivel por um terceiro
que tenha a publicacao em maos. Este script e a fonte editavel; o `.ttl` e
gerado e nao se edita a mao.

O que a publicacao documenta e que vira instancia:

  - o observatorio, um prototipo em WordPress/PHP/MySQL (`ProjectObservatory`);
  - o gerenciamento de conteudo por onde ele organiza os dados dos projetos
    (`DataManager`);
  - as oito funcionalidades da secao 4.1, cada uma como uma `View` no papel que
    lhe cabe (`CrudView`, `Disseminator` ou `Reporter`), componente do
    observatorio e disponibilizada pelo gerenciamento de conteudo por meio de um
    relator `ViewProvision`;
  - os tres perfis de ator da survey de avaliacao (`ObservatoryUser`);
  - o sistema de gestao de projetos da universidade, citado como sistema a parte
    sem integracao com o observatorio (`System`).

O que **nao** vira instancia, de proposito: a cadeia de ETL e proveniencia
(`DataSource`, `Extract`, `Transform`, `Load`). A publicacao descreve um
prototipo cuja coleta e o cadastro manual de projetos, nao um pipeline; QC3 e
QC6, que exigem essa cadeia, ficam para o ticket 08.

Saida:

  - `observatorio.ttl`   os dados de instancia, Turtle deterministica.
"""

from __future__ import annotations

import sys
from pathlib import Path

import rdflib
from rdflib import OWL, RDF, RDFS, Literal, Namespace, URIRef

from rdf_deterministico import normalizado

SAIDA_PADRAO = Path("artifacts/ontology/instancias")

ONTOMPO = Namespace("https://example.org/ontompo/rodada-2#")
ONTOMPO_IRI = URIRef("https://example.org/ontompo/rodada-2")
OBS = Namespace("https://example.org/ontompo/instancia-observatorio#")
OBS_IRI = URIRef("https://example.org/ontompo/instancia-observatorio")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
DCT = Namespace("http://purl.org/dc/terms/")

PT = "pt-BR"
FONTE_DOI = URIRef("https://doi.org/10.5753/sbsi_estendido.2022.222995")

# --------------------------------------------------------------------------- #
# O que a publicacao documenta                                                 #
# --------------------------------------------------------------------------- #

# O observatorio e o seu gerenciamento de conteudo.
OBSERVATORIO = (
    "observatorio",
    "ProjectObservatory",
    "Observatório de projetos de pesquisa e extensão (protótipo)",
    "Protótipo funcional de observatório de projetos de pesquisa e extensão de uma "
    "universidade pública brasileira, construído em WordPress (PHP e MySQL) e avaliado "
    "por uma survey; descrito nos Anais Estendidos do XVIII SBSI (2022), seções 4.1 e 4.2.",
)
GERENCIADOR = (
    "gerenciadorDeConteudo",
    "DataManager",
    "Gerenciamento de conteúdo do observatório",
    "Sistema de gerenciamento de conteúdo (WordPress, sobre PHP e MySQL) por meio do "
    "qual o observatório organiza, gerencia e disponibiliza os dados dos projetos; "
    "Anais Estendidos do XVIII SBSI (2022), seção 4.2.",
)

# As oito funcionalidades da secao 4.1, cada uma no papel de View que lhe cabe.
# (nome, papel, rotulo, trecho da publicacao)
FUNCIONALIDADES = [
    (
        "manutencaoDeProjetos",
        "CrudView",
        "Manutenção de projetos",
        "«Manter projetos para que possam ser acessados pela Sociedade» "
        "(Anais Estendidos do XVIII SBSI, 2022, seção 4.1).",
    ),
    (
        "consultaDeDadosDosProjetos",
        "CrudView",
        "Consulta de dados dos projetos",
        "«Consultar dados dos projetos» (Anais Estendidos do XVIII SBSI, 2022, seção 4.1).",
    ),
    (
        "cadastroDeMidia",
        "CrudView",
        "Cadastro de mídia sobre os projetos",
        "«Cadastrar mídia sobre os projetos» (Anais Estendidos do XVIII SBSI, 2022, seção 4.1).",
    ),
    (
        "downloadDeDadosBrutos",
        "Disseminator",
        "Download de dados brutos dos projetos",
        "«Realizar download de dados brutos dos projetos» "
        "(Anais Estendidos do XVIII SBSI, 2022, seção 4.1).",
    ),
    (
        "analisesDetalhadas",
        "Disseminator",
        "Análises detalhadas dos projetos",
        "«Acessar análise detalhadas dos projetos»; a seção 2 cita gráficos e tabelas "
        "(Anais Estendidos do XVIII SBSI, 2022, seções 2 e 4.1).",
    ),
    (
        "interacaoComProjetos",
        "Reporter",
        "Interação dos usuários com os projetos",
        "«Permitir que usuários interajam com os projetos a partir da inclusão de "
        "comentários, reações e relatos de erro» "
        "(Anais Estendidos do XVIII SBSI, 2022, seção 4.1).",
    ),
    (
        "forunsDeDiscussao",
        "Reporter",
        "Fóruns de discussão",
        "«Cadastrar e participar de fóruns de discussão» "
        "(Anais Estendidos do XVIII SBSI, 2022, seção 4.1).",
    ),
    (
        "noticiasEmRedesSociais",
        "Reporter",
        "Publicação de notícias em redes sociais",
        "«Postar notícias em redes sociais» (Anais Estendidos do XVIII SBSI, 2022, seção 4.1).",
    ),
]

# Os perfis de ator convidados para a survey de avaliacao (secao 4.3).
ATORES = [
    (
        "usuarioEstudante",
        "ObservatoryUser",
        "Usuário estudante",
        "Estudantes, 64% das 25 pessoas convidadas para a survey de avaliação "
        "(Anais Estendidos do XVIII SBSI, 2022, seção 4.3).",
    ),
    (
        "usuarioDocente",
        "ObservatoryUser",
        "Usuário docente",
        "Docentes, 12% das 25 pessoas convidadas para a survey de avaliação "
        "(Anais Estendidos do XVIII SBSI, 2022, seção 4.3).",
    ),
    (
        "usuarioDaSociedade",
        "ObservatoryUser",
        "Usuário da sociedade",
        "Representantes da sociedade, 24% das 25 pessoas convidadas para a survey; "
        "cidadãos que podem se beneficiar dos projetos divulgados "
        "(Anais Estendidos do XVIII SBSI, 2022, seções 1 e 4.3).",
    ),
]

# O sistema de gestao de projetos da universidade: sistema a parte, sem integracao.
SISTEMAS_EXTERNOS = [
    (
        "sistemaDeGestaoDeProjetos",
        "System",
        "Sistema de gestão de projetos de pesquisa da universidade",
        "«A universidade em questão possui um sistema para gestão de projetos de pesquisa, "
        "já o observatório é um sistema à parte que não possui integração com a ferramenta» "
        "(Anais Estendidos do XVIII SBSI, 2022, seção 5).",
    ),
]


def _individuo(grafo: rdflib.Graph, nome: str, papel: str, rotulo: str, comentario: str) -> URIRef:
    sujeito = OBS[nome]
    grafo.add((sujeito, RDF.type, ONTOMPO[papel]))
    grafo.add((sujeito, RDFS.label, Literal(rotulo, lang=PT)))
    grafo.add((sujeito, SKOS.prefLabel, Literal(rotulo, lang=PT)))
    grafo.add((sujeito, RDFS.comment, Literal(comentario, lang=PT)))
    grafo.add((sujeito, RDFS.isDefinedBy, OBS_IRI))
    return sujeito


def construir() -> rdflib.Graph:
    grafo = rdflib.Graph()
    for prefixo, ns in (
        ("obs", OBS),
        ("ontompo", ONTOMPO),
        ("owl", OWL),
        ("rdfs", RDFS),
        ("skos", SKOS),
        ("dct", DCT),
    ):
        grafo.bind(prefixo, ns)

    grafo.add((OBS_IRI, RDF.type, OWL.Ontology))
    grafo.add((OBS_IRI, OWL.imports, ONTOMPO_IRI))
    grafo.add((OBS_IRI, DCT.source, FONTE_DOI))
    grafo.add(
        (
            OBS_IRI,
            DCT.description,
            Literal(
                "Dados de instância de um observatório de projetos de pesquisa e extensão de "
                "uma universidade pública brasileira, derivados do que a publicação nos Anais "
                "Estendidos do XVIII SBSI (2022) documenta. Cenário usado para exercitar as "
                "questões de competência da OntoMPO revisada. O mapa trecho→instância está em "
                "procedencia.md.",
                lang=PT,
            ),
        )
    )
    grafo.add(
        (
            OBS_IRI,
            RDFS.comment,
            Literal(
                "Sem dct:creator: o cenário é trabalho anterior do próprio autor e a revisão do "
                "artigo é duplamente anônima. A fonte é referida em terceira pessoa e nenhum "
                "rótulo identifica autoria, instituição ou localidade.",
                lang=PT,
            ),
        )
    )

    observatorio = _individuo(grafo, *OBSERVATORIO)
    gerenciador = _individuo(grafo, *GERENCIADOR)
    grafo.add((gerenciador, ONTOMPO.componentOf_DataManager_ProjectObservatory, observatorio))

    for nome, papel, rotulo, comentario in FUNCIONALIDADES:
        view = _individuo(grafo, nome, papel, rotulo, comentario)
        grafo.add((view, ONTOMPO.componentOf_View_ProjectObservatory, observatorio))
        provisao = OBS[f"disponibilizacaoDe_{nome}"]
        grafo.add((provisao, RDF.type, ONTOMPO.ViewProvision))
        grafo.add(
            (
                provisao,
                RDFS.label,
                Literal(f"Disponibilização de {rotulo[0].lower() + rotulo[1:]}", lang=PT),
            )
        )
        grafo.add((provisao, RDFS.comment, Literal(
            "Relator que liga o gerenciamento de conteúdo do observatório à visão que ele "
            f"disponibiliza: {rotulo.lower()}.", lang=PT)))
        grafo.add((provisao, ONTOMPO.mediation_ViewProvision_DataManager, gerenciador))
        grafo.add((provisao, ONTOMPO.mediation_ViewProvision_View, view))
        grafo.add((provisao, RDFS.isDefinedBy, OBS_IRI))

    for entrada in ATORES + SISTEMAS_EXTERNOS:
        _individuo(grafo, *entrada)

    return grafo


def main() -> int:
    saida = Path(sys.argv[1]) if len(sys.argv) > 1 else SAIDA_PADRAO
    saida.mkdir(parents=True, exist_ok=True)

    grafo = normalizado(construir())
    destino = saida / "observatorio.ttl"
    destino.write_text(grafo.serialize(format="turtle"), encoding="utf-8", newline="\n")

    individuos = {
        s
        for s in grafo.subjects(RDF.type, None)
        if isinstance(s, URIRef) and str(s).startswith(str(OBS)) and s != OBS_IRI
    }
    print(f"instâncias -> {destino}")
    print(f"indivíduos: {len(individuos)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
