#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Monta os dados de instancia dos observatorios, para a avaliacao funcional (tickets 07 e 08).

Uso: python tools/generation/gerar_instancias.py [diretorio-de-saida]

Sao dois cenarios, gravados lado a lado:

  - `observatorio.ttl`    o cenario principal — um observatorio de projetos de
    pesquisa e extensao de uma universidade publica brasileira, descrito nos
    **Anais Estendidos do XVIII SBSI (2022)**, DOI
    10.5753/sbsi_estendido.2022.222995. E trabalho anterior do proprio autor:
    toda mencao aqui — IRIs, rotulos, comentarios — e em **terceira pessoa** e
    nao identifica autoria nem instituicao. O mapa trecho -> instancia esta em
    `artifacts/ontology/instancias/procedencia.md`.

  - `observatorio-b.ttl`  um **segundo observatorio, sintetico** — um
    observatorio municipal de obras publicas, sem fonte na literatura,
    construido para a QC7 comparar a cobertura conceitual de duas iniciativas
    que se dizem aderentes ao MPO. A premissa esta registrada no ticket 08 e em
    `procedencia.md`.

O ticket 07 abriu `observatorio.ttl` com o que a publicacao documenta e uma QC
ponta a ponta. O ticket 08 completa as sete QCs, e para isso acrescenta ao
cenario principal a cadeia de ETL/proveniencia (`DataSource`, `EtlProcess`,
`Extract`/`Transform`/`Load` com carimbo de tempo), as partes interessadas e as
suas interacoes com motivacao registrada, os projetos observados e as
observacoes datadas. O que dessas adicoes vai alem do que a publicacao
documenta — a segunda fonte de dados, o modulo de coleta e os nomes de projeto —
esta marcado como premissa em `procedencia.md`.

Este script e a fonte editavel; os `.ttl` sao gerados e nao se editam a mao.

Saida:

  - `observatorio.ttl`    o cenario principal, Turtle deterministica.
  - `observatorio-b.ttl`  o segundo observatorio sintetico, Turtle deterministica.
"""

from __future__ import annotations

import sys
from pathlib import Path

import rdflib
from rdflib import OWL, RDF, RDFS, XSD, Literal, Namespace, URIRef

from rdf_deterministico import normalizado

SAIDA_PADRAO = Path("artifacts/ontology/instancias")

ONTOMPO = Namespace("https://example.org/ontompo/rodada-2#")
ONTOMPO_IRI = URIRef("https://example.org/ontompo/rodada-2")
OBS = Namespace("https://example.org/ontompo/instancia-observatorio#")
OBS_IRI = URIRef("https://example.org/ontompo/instancia-observatorio")
OBSB = Namespace("https://example.org/ontompo/instancia-observatorio-b#")
OBSB_IRI = URIRef("https://example.org/ontompo/instancia-observatorio-b")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
DCT = Namespace("http://purl.org/dc/terms/")
GUFO = Namespace("http://purl.org/nemo/gufo#")

PT = "pt-BR"
FONTE_DOI = URIRef("https://doi.org/10.5753/sbsi_estendido.2022.222995")

# gUFO ja traz o "quando" de um evento em propriedades de dado sobre gufo:Event;
# a instanciacao e que as preenche (ver correcoes-rodada-2.md, A5). Granularidade
# de data basta para "e quando" e para o filtro de periodo da QC4.
GUFO_INICIO = GUFO.hasBeginPointInXSDDate
GUFO_FIM = GUFO.hasEndPointInXSDDate

# --------------------------------------------------------------------------- #
# O que a publicacao documenta (cenario principal, ticket 07)                   #
# --------------------------------------------------------------------------- #

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


def _vinculo(grafo: rdflib.Graph, nome: str, papel: str, rotulo: str, comentario: str) -> URIRef:
    """Individuo de evento ou relator: sem skos:prefLabel, como os do ticket 07."""
    sujeito = OBS[nome]
    grafo.add((sujeito, RDF.type, ONTOMPO[papel]))
    grafo.add((sujeito, RDFS.label, Literal(rotulo, lang=PT)))
    grafo.add((sujeito, RDFS.comment, Literal(comentario, lang=PT)))
    grafo.add((sujeito, RDFS.isDefinedBy, OBS_IRI))
    return sujeito


def _prefixos(grafo: rdflib.Graph, obs_ns: Namespace, obs_prefixo: str) -> None:
    for prefixo, ns in (
        (obs_prefixo, obs_ns),
        ("ontompo", ONTOMPO),
        ("owl", OWL),
        ("rdfs", RDFS),
        ("skos", SKOS),
        ("dct", DCT),
        ("gufo", GUFO),
        ("xsd", XSD),
    ):
        grafo.bind(prefixo, ns)


def _cadeia_etl(
    grafo: rdflib.Graph,
    sufixo: str,
    rotulo_processo: str,
    gerenciador: URIRef,
    fonte: URIRef,
    inicio: str,
    fim: str,
) -> dict[str, URIRef]:
    """Um EtlProcess com Extract, Transform e Load como partes proprias.

    O gerenciador de dados participa como Collector, Processor e Storer; a fonte,
    como DataSource na extracao. O Load carrega o "quando" em gufo:...InXSDDate.
    """
    processo = _vinculo(
        grafo,
        f"processoEtl_{sufixo}",
        "EtlProcess",
        f"Processo de ETL — {rotulo_processo}",
        f"Evento complexo que leva os dados de {rotulo_processo} até o repositório do "
        "observatório; a extração, a transformação e a carga são partes próprias dele.",
    )
    extracao = _vinculo(
        grafo,
        f"extracao_{sufixo}",
        "Extract",
        f"Extração — {rotulo_processo}",
        f"Evento de coleta dos dados de {rotulo_processo}.",
    )
    transformacao = _vinculo(
        grafo,
        f"transformacao_{sufixo}",
        "Transform",
        f"Transformação — {rotulo_processo}",
        f"Evento de tratamento e modelagem dos dados de {rotulo_processo}.",
    )
    carga = _vinculo(
        grafo,
        f"carga_{sufixo}",
        "Load",
        f"Carga — {rotulo_processo}",
        f"Evento de armazenamento, no repositório do observatório, dos dados de {rotulo_processo}.",
    )

    grafo.add((extracao, ONTOMPO.participational_Extract_EtlProcess, processo))
    grafo.add((transformacao, ONTOMPO.participational_Transform_EtlProcess, processo))
    grafo.add((carga, ONTOMPO.participational_Load_EtlProcess, processo))

    grafo.add((fonte, ONTOMPO.participation_DataSource_Extract, extracao))
    grafo.add((gerenciador, ONTOMPO.participation_Collector_Extract, extracao))
    grafo.add((gerenciador, ONTOMPO.participation_Collector_Transform, transformacao))
    grafo.add((gerenciador, ONTOMPO.participation_Processor_Transform, transformacao))
    grafo.add((gerenciador, ONTOMPO.participation_Processor_Load, carga))
    grafo.add((gerenciador, ONTOMPO.participation_Storer_Load, carga))

    grafo.add((carga, GUFO_INICIO, Literal(inicio, datatype=XSD.date)))
    grafo.add((carga, GUFO_FIM, Literal(fim, datatype=XSD.date)))
    grafo.add((extracao, GUFO_FIM, Literal(inicio, datatype=XSD.date)))

    return {
        "processo": processo,
        "extracao": extracao,
        "transformacao": transformacao,
        "carga": carga,
    }


def _metadados_ontologia(grafo: rdflib.Graph) -> None:
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
                "Estendidos do XVIII SBSI (2022) documenta, com a cadeia de ETL/proveniência, "
                "as partes interessadas e as observações que as sete questões de competência "
                "exercitam. O mapa trecho→instância e as premissas do que vai além da fonte "
                "estão em procedencia.md.",
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


def construir() -> rdflib.Graph:
    """O cenario principal: o que a publicacao documenta (ticket 07) mais a
    cadeia de proveniencia, as partes interessadas e as observacoes (ticket 08).
    """
    grafo = rdflib.Graph()
    _prefixos(grafo, OBS, "obs")
    _metadados_ontologia(grafo)

    # ---- ticket 07: o que a publicacao documenta -------------------------- #
    observatorio = _individuo(grafo, *OBSERVATORIO)
    gerenciador = _individuo(grafo, *GERENCIADOR)
    grafo.add((gerenciador, ONTOMPO.componentOf_DataManager_ProjectObservatory, observatorio))

    views: dict[str, URIRef] = {}
    for nome, papel, rotulo, comentario in FUNCIONALIDADES:
        view = _individuo(grafo, nome, papel, rotulo, comentario)
        views[nome] = view
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

    atores: dict[str, URIRef] = {}
    for entrada in ATORES + SISTEMAS_EXTERNOS:
        atores[entrada[0]] = _individuo(grafo, *entrada)

    # ---- ticket 08: o grupo do observatorio ------------------------------ #
    grupo = _individuo(
        grafo,
        "grupoDoObservatorio",
        "ObservatoryGroup",
        "Grupo do observatório (protótipo)",
        "Coletivo reunido em torno do observatório: a equipe de gerenciamento e "
        "operação, os perfis de usuário da survey e o sistema externo citado; "
        "Anais Estendidos do XVIII SBSI (2022), seções 4.2 e 4.3.",
    )
    for nome in ("usuarioEstudante", "usuarioDocente", "usuarioDaSociedade"):
        grafo.add((atores[nome], ONTOMPO.memberOf_ObservatoryUser_ObservatoryGroup, grupo))
    grafo.add(
        (atores["sistemaDeGestaoDeProjetos"], ONTOMPO.memberOf_System_ObservatoryGroup, grupo)
    )

    # ---- ticket 08: projetos observados e a gerencia de dados ----------- #
    # Nomes de projeto nao constam da publicacao (ela documenta um prototipo e a
    # sua avaliacao, nao um acervo). Estes dois sao projetos-exemplo do cenario,
    # um por tipo que a secao 4.1 distingue — extensao acessivel a Sociedade e
    # pesquisa —, marcados como premissa em procedencia.md.
    extensao = _individuo(
        grafo,
        "projetoExtensaoComunitaria",
        "Project",
        "Projeto de extensão comunitária (cenário)",
        "Projeto observado do tipo extensão, mantido para acesso pela Sociedade "
        "(Anais Estendidos do XVIII SBSI, 2022, seção 4.1). Projeto-exemplo do "
        "cenário: a publicação não nomeia projetos.",
    )
    pesquisa = _individuo(
        grafo,
        "projetoPesquisaAplicada",
        "Project",
        "Projeto de pesquisa aplicada (cenário)",
        "Projeto observado do tipo pesquisa, cujos dados são coletados mas ainda "
        "não divulgados por nenhuma visão. Projeto-exemplo do cenário: a "
        "publicação não nomeia projetos.",
    )

    # A publicacao descreve um unico gerenciador de conteudo. Este modulo de
    # coleta e acrescentado ao cenario para a QC4 poder distinguir um projeto
    # cujos dados sao coletados mas nao chegam a nenhuma Disseminator — premissa
    # registrada em procedencia.md.
    coleta = _individuo(
        grafo,
        "gerenciadorDeColeta",
        "DataManager",
        "Módulo de coleta de dados de projetos (cenário)",
        "Componente de gerenciamento de dados que integra dados de projetos ainda "
        "não publicados em nenhuma visão. Acréscimo do cenário para exercitar a QC4; "
        "a publicação documenta um único gerenciador de conteúdo.",
    )
    grafo.add((coleta, ONTOMPO.componentOf_DataManager_ProjectObservatory, observatorio))

    for sufixo, gestor, projeto, rot in (
        ("extensaoComunitaria", gerenciador, extensao, "extensão comunitária"),
        ("pesquisaAplicada", coleta, pesquisa, "pesquisa aplicada"),
    ):
        gestao = _vinculo(
            grafo,
            f"gerenciaDadosDe_{sufixo}",
            "ProjectDataManagement",
            f"Gerência de dados — {rot}",
            f"Vínculo pelo qual um gerenciamento de dados responde pelos dados do projeto de {rot}.",
        )
        grafo.add((gestao, ONTOMPO.mediation_ProjectDataManagement_DataManager, gestor))
        grafo.add((gestao, ONTOMPO.mediation_ProjectDataManagement_Project, projeto))

    # ---- ticket 08: as fontes de dados e a cadeia de ETL --------------- #
    grafo.add((gerenciador, RDF.type, ONTOMPO.Collector))
    grafo.add((gerenciador, RDF.type, ONTOMPO.Processor))
    grafo.add((gerenciador, RDF.type, ONTOMPO.Storer))

    fonte_cadastro = _individuo(
        grafo,
        "fonteCadastroDeProjetos",
        "DataSource",
        "Cadastro de projetos pela equipe e pelos coordenadores",
        "Origem principal dos dados exibidos: o cadastro de projetos preenchido "
        "pela equipe e pelos coordenadores (Anais Estendidos do XVIII SBSI, 2022, "
        "seções 4.1 e 4.2).",
    )
    fonte_planilha = _individuo(
        grafo,
        "fontePlanilhaDadosAbertos",
        "DataSource",
        "Planilha de dados abertos de projetos institucionais",
        "Segunda origem: uma planilha de dados abertos importada periodicamente. "
        "Acréscimo do cenário para a QC3 e a QC6 exercitarem «uma dada fonte»; a "
        "publicação documenta coleta manual.",
    )

    _cadeia_etl(
        grafo,
        "cadastro",
        "cadastro de projetos",
        gerenciador,
        fonte_cadastro,
        inicio="2023-03-06",
        fim="2023-03-06",
    )
    _cadeia_etl(
        grafo,
        "dadosAbertos",
        "dados abertos institucionais",
        gerenciador,
        fonte_planilha,
        inicio="2023-09-11",
        fim="2023-09-11",
    )

    # ---- ticket 08: observacoes datadas (QC4) -------------------------- #
    # Ambas observam conteudo disseminado pelo gerenciador de conteudo, que
    # responde pelos dados do projeto de extensao. O projeto de pesquisa, cujos
    # dados estao com o modulo de coleta e nao aparecem em nenhuma Disseminator,
    # nao tem observacao registrada.
    for sufixo, ator, disseminador, data in (
        ("1", atores["usuarioEstudante"], views["analisesDetalhadas"], "2023-04-10"),
        ("2", atores["usuarioDaSociedade"], views["downloadDeDadosBrutos"], "2023-09-15"),
    ):
        observacao = _vinculo(
            grafo,
            f"observacao_{sufixo}",
            "Observation",
            f"Observação {sufixo}",
            "Evento em que um agente observa conteúdo divulgado pelo observatório e "
            "no qual passa a existir conhecimento sobre os projetos observados.",
        )
        grafo.add((ator, ONTOMPO.participation_Agent_Observation, observacao))
        grafo.add((disseminador, ONTOMPO.participation_Disseminator_Observation, observacao))
        grafo.add((observacao, GUFO_FIM, Literal(data, datatype=XSD.date)))
        conhecimento = _vinculo(
            grafo,
            f"conhecimento_{sufixo}",
            "Knowledge",
            f"Conhecimento {sufixo}",
            "Conhecimento sobre os projetos observados, criado na observação correspondente.",
        )
        grafo.add((conhecimento, ONTOMPO.creation_Knowledge_Observation, observacao))

    # ---- ticket 08: partes interessadas e as suas interacoes (QC2, QC5) - #
    partes = {}
    for nome, rotulo, comentario in (
        (
            "parteInteressadaCoordenacaoDeProjeto",
            "Coordenação de projeto observado",
            "Coordenação de um projeto observado, que acompanha o que o observatório "
            "divulga sobre ele. O Apêndice A da conceituação define parte interessada "
            "como «indivíduo, grupo ou organização».",
        ),
        (
            "parteInteressadaAgenciaDeFomento",
            "Agência de fomento",
            "Agência de fomento interessada nos resultados dos projetos que apoia.",
        ),
        (
            "parteInteressadaComunidadeAtendida",
            "Comunidade atendida",
            "Comunidade atendida por um projeto de extensão; cidadãos que podem se "
            "beneficiar dos projetos divulgados (Anais Estendidos do XVIII SBSI, 2022, seção 1).",
        ),
    ):
        parte = _individuo(grafo, nome, "StakeHolder", rotulo, comentario)
        partes[nome] = parte
        grafo.add((parte, ONTOMPO.memberOf_StakeHolder_ObservatoryGroup, grupo))

    # (relator SocialInteraction, agente, Reporter, motivacao)
    interacoes = [
        (
            "coordenacao_interacaoComProjetos",
            partes["parteInteressadaCoordenacaoDeProjeto"],
            "interacaoComProjetos",
            "Acompanhar comentários, reações e relatos de erro sobre o projeto coordenado.",
        ),
        (
            "coordenacao_foruns",
            partes["parteInteressadaCoordenacaoDeProjeto"],
            "forunsDeDiscussao",
            "Discutir a temática do projeto coordenado em fóruns.",
        ),
        (
            "agenciaDeFomento_noticias",
            partes["parteInteressadaAgenciaDeFomento"],
            "noticiasEmRedesSociais",
            "Acompanhar a divulgação pública dos projetos apoiados.",
        ),
        (
            "comunidadeAtendida_interacaoComProjetos",
            partes["parteInteressadaComunidadeAtendida"],
            "interacaoComProjetos",
            "Relatar necessidades e dar retorno sobre os projetos de extensão.",
        ),
        (
            "estudante_foruns",
            atores["usuarioEstudante"],
            "forunsDeDiscussao",
            "Trocar informação sobre projetos de interesse acadêmico.",
        ),
        (
            "docente_noticias",
            atores["usuarioDocente"],
            "noticiasEmRedesSociais",
            "Divulgar os projetos de pesquisa sob coordenação docente.",
        ),
        (
            "sociedade_interacaoComProjetos",
            atores["usuarioDaSociedade"],
            "interacaoComProjetos",
            "Acompanhar projetos de extensão que beneficiam a comunidade.",
        ),
    ]
    for sufixo, agente, reporter_nome, motivacao in interacoes:
        interacao = _vinculo(
            grafo,
            f"interacao_{sufixo}",
            "SocialInteraction",
            f"Interação social — {sufixo}",
            "Vínculo de interação entre um agente do observatório e o conteúdo dele.",
        )
        grafo.add((interacao, ONTOMPO.mediation_SocialInteraction_Agent, agente))
        grafo.add((interacao, ONTOMPO.mediation_SocialInteraction_Reporter, views[reporter_nome]))
        grafo.add((interacao, DCT.description, Literal(motivacao, lang=PT)))

    return grafo


def construir_observatorio_b() -> rdflib.Graph:
    """Segundo observatorio, **sintetico**: um observatorio municipal de obras
    publicas. Sem fonte na literatura; existe para a QC7 comparar a cobertura
    conceitual de duas iniciativas que se dizem aderentes ao MPO.

    Cobre de proposito um recorte diferente do cenario principal: tem
    `Organization` e `SocialAgent` (a prefeitura mantenedora), que o principal
    nao instancia, e **nao** tem `Reporter`, `SocialInteraction`, `Observation`,
    `Knowledge`, `ObservatoryGroup` nem `StakeHolder`, que o principal tem. E
    essa assimetria que a QC7 mede.
    """
    grafo = rdflib.Graph()
    _prefixos(grafo, OBSB, "obsb")

    grafo.add((OBSB_IRI, RDF.type, OWL.Ontology))
    grafo.add((OBSB_IRI, OWL.imports, ONTOMPO_IRI))
    grafo.add(
        (
            OBSB_IRI,
            DCT.description,
            Literal(
                "Segundo observatório, sintético: um observatório municipal de obras "
                "públicas. Sem fonte na literatura e sem dct:creator — construído para a "
                "QC7 comparar a cobertura conceitual de duas iniciativas aderentes ao MPO. "
                "A premissa está registrada no ticket 08 e em procedencia.md.",
                lang=PT,
            ),
        )
    )
    grafo.add(
        (
            OBSB_IRI,
            RDFS.comment,
            Literal(
                "Cenário sintético. Nenhum rótulo identifica pessoa, instituição ou "
                "município reais; a iniciativa e os seus elementos são fictícios.",
                lang=PT,
            ),
        )
    )

    def ind(nome: str, papel: str, rotulo: str, comentario: str) -> URIRef:
        sujeito = OBSB[nome]
        grafo.add((sujeito, RDF.type, ONTOMPO[papel]))
        grafo.add((sujeito, RDFS.label, Literal(rotulo, lang=PT)))
        grafo.add((sujeito, SKOS.prefLabel, Literal(rotulo, lang=PT)))
        grafo.add((sujeito, RDFS.comment, Literal(comentario, lang=PT)))
        grafo.add((sujeito, RDFS.isDefinedBy, OBSB_IRI))
        return sujeito

    observatorio = ind(
        "observatorioMunicipal",
        "ProjectObservatory",
        "Observatório municipal de obras públicas (sintético)",
        "Observatório fictício que divulga o andamento de obras públicas de um município.",
    )
    prefeitura = ind(
        "prefeituraMantenedora",
        "Organization",
        "Prefeitura mantenedora",
        "Organização que mantém o observatório municipal e responde pelas obras divulgadas.",
    )
    portal = ind(
        "portalDeDados",
        "DataManager",
        "Portal de dados do observatório municipal",
        "Ferramenta de software que organiza, gerencia e disponibiliza os dados das obras.",
    )
    grafo.add((portal, RDF.type, ONTOMPO.Collector))
    grafo.add((portal, RDF.type, ONTOMPO.Processor))
    grafo.add((portal, RDF.type, ONTOMPO.Storer))
    grafo.add((portal, ONTOMPO.componentOf_DataManager_ProjectObservatory, observatorio))

    visoes = {}
    for nome, papel, rotulo in (
        ("painelDeIndicadores", "Disseminator", "Painel de indicadores das obras"),
        ("relatoriosMensais", "Disseminator", "Relatórios mensais de execução"),
        ("consultaPublica", "CrudView", "Consulta pública de obras"),
    ):
        visao = ind(nome, papel, rotulo, f"Visão «{rotulo.lower()}» do observatório municipal.")
        visoes[nome] = visao
        grafo.add((visao, ONTOMPO.componentOf_View_ProjectObservatory, observatorio))
        provisao = OBSB[f"disponibilizacaoDe_{nome}"]
        grafo.add((provisao, RDF.type, ONTOMPO.ViewProvision))
        grafo.add((provisao, RDFS.label, Literal(f"Disponibilização de {rotulo.lower()}", lang=PT)))
        grafo.add((provisao, RDFS.isDefinedBy, OBSB_IRI))
        grafo.add((provisao, ONTOMPO.mediation_ViewProvision_DataManager, portal))
        grafo.add((provisao, ONTOMPO.mediation_ViewProvision_View, visao))

    fonte = ind(
        "baseDeTransparenciaMunicipal",
        "DataSource",
        "Base de dados de transparência municipal",
        "Origem dos dados das obras: o sistema de transparência da prefeitura.",
    )
    processo = OBSB["processoEtlMunicipal"]
    grafo.add((processo, RDF.type, ONTOMPO.EtlProcess))
    grafo.add((processo, RDFS.label, Literal("Processo de ETL — dados de obras", lang=PT)))
    grafo.add((processo, RDFS.isDefinedBy, OBSB_IRI))
    partes_etl = {}
    for nome, papel, rotulo in (
        ("extracaoMunicipal", "Extract", "Extração — dados de obras"),
        ("transformacaoMunicipal", "Transform", "Transformação — dados de obras"),
        ("cargaMunicipal", "Load", "Carga — dados de obras"),
    ):
        evento = OBSB[nome]
        grafo.add((evento, RDF.type, ONTOMPO[papel]))
        grafo.add((evento, RDFS.label, Literal(rotulo, lang=PT)))
        grafo.add((evento, RDFS.isDefinedBy, OBSB_IRI))
        partes_etl[papel] = evento
    grafo.add((partes_etl["Extract"], ONTOMPO.participational_Extract_EtlProcess, processo))
    grafo.add((partes_etl["Transform"], ONTOMPO.participational_Transform_EtlProcess, processo))
    grafo.add((partes_etl["Load"], ONTOMPO.participational_Load_EtlProcess, processo))
    grafo.add((fonte, ONTOMPO.participation_DataSource_Extract, partes_etl["Extract"]))
    grafo.add((portal, ONTOMPO.participation_Collector_Extract, partes_etl["Extract"]))
    grafo.add((portal, ONTOMPO.participation_Collector_Transform, partes_etl["Transform"]))
    grafo.add((portal, ONTOMPO.participation_Processor_Transform, partes_etl["Transform"]))
    grafo.add((portal, ONTOMPO.participation_Processor_Load, partes_etl["Load"]))
    grafo.add((portal, ONTOMPO.participation_Storer_Load, partes_etl["Load"]))
    grafo.add((partes_etl["Load"], GUFO_FIM, Literal("2024-02-15", datatype=XSD.date)))
    grafo.add((partes_etl["Load"], GUFO_INICIO, Literal("2024-02-15", datatype=XSD.date)))

    ind(
        "usuarioCidadao",
        "ObservatoryUser",
        "Usuário cidadão",
        "Cidadão que consulta o andamento das obras do município.",
    )
    ind(
        "usuarioServidor",
        "ObservatoryUser",
        "Usuário servidor público",
        "Servidor da prefeitura que acompanha a execução das obras.",
    )
    ind(
        "orgaoDeControleExterno",
        "System",
        "Sistema de órgão de controle externo",
        "Sistema externo de um órgão de controle que consome os dados publicados.",
    )

    obra = ind(
        "obraDePavimentacao",
        "Project",
        "Obra de pavimentação (sintética)",
        "Obra pública observada pelo observatório municipal.",
    )
    gestao = OBSB["gerenciaDadosDaObra"]
    grafo.add((gestao, RDF.type, ONTOMPO.ProjectDataManagement))
    grafo.add((gestao, RDFS.label, Literal("Gerência de dados — obra de pavimentação", lang=PT)))
    grafo.add((gestao, RDFS.isDefinedBy, OBSB_IRI))
    grafo.add((gestao, ONTOMPO.mediation_ProjectDataManagement_DataManager, portal))
    grafo.add((gestao, ONTOMPO.mediation_ProjectDataManagement_Project, obra))

    _ = prefeitura  # a prefeitura entra na cobertura da QC7 por Organization/SocialAgent
    return grafo


def _escrever(grafo: rdflib.Graph, destino: Path, obs_ns: Namespace, obs_iri: URIRef) -> int:
    normal = normalizado(grafo)
    destino.write_text(normal.serialize(format="turtle"), encoding="utf-8", newline="\n")
    individuos = {
        s
        for s in normal.subjects(RDF.type, None)
        if isinstance(s, URIRef) and str(s).startswith(str(obs_ns)) and s != obs_iri
    }
    print(f"instâncias -> {destino}")
    print(f"indivíduos: {len(individuos)}")
    return len(individuos)


def main() -> int:
    saida = Path(sys.argv[1]) if len(sys.argv) > 1 else SAIDA_PADRAO
    saida.mkdir(parents=True, exist_ok=True)

    _escrever(construir(), saida / "observatorio.ttl", OBS, OBS_IRI)
    _escrever(construir_observatorio_b(), saida / "observatorio-b.ttl", OBSB, OBSB_IRI)
    return 0


if __name__ == "__main__":
    sys.exit(main())
