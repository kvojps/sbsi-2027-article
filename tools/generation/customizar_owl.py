#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Customiza a OWL que a transformacao gUFO gerou, e preserva o diff (ticket 06).

Uso: python tools/generation/customizar_owl.py [ttl-gerada] [diretorio-de-saida]

Dois pareceres do ONTOBRAS perguntaram a mesma coisa por caminhos diferentes:
como se garante que a semantica do OntoUML foi preservada no OWL, e o que
exatamente os autores acrescentaram ao que a ferramenta ja gera. A resposta
deste script e um invariante, nao uma afirmacao:

    **toda customizacao e aditiva.** Nenhuma tripla gerada pela transformacao e
    removida ou alterada; o artefato customizado e o gerado mais um acrescimo, e
    o acrescimo e gravado inteiro, em `diff-gerado-customizado.ttl`.

Sob esse invariante a preservacao semantica nao depende de inspecao: ela e
verificavel por conteinencia de grafos, e `../verification/verificar_owl.py`
verifica. O preco e que o que so poderia ser corrigido reescrevendo o gerado —
o achado B5, de convencao de nome — e endereçado por rotulo e nao por IRI, com
a razao escrita.

As cinco customizacoes estao em `CUSTOMIZACOES`, cada uma com a funcao que a
aplica e a justificativa que vai para `customizacoes.md`. Sao produzidos:

  - `ontompo.ttl`                     a OWL customizada;
  - `diff-gerado-customizado.ttl`     exatamente as triplas acrescentadas;
  - `diff-gerado-customizado.md`      o mesmo, agrupado e legivel;
  - `customizacoes.md`                cada customizacao e sua justificativa;
  - `metricas.md`                     classes, propriedades e axiomas, nos tres
                                      artefatos.

O RDF/XML (`ontompo.owl`) e a copia submetida (`ontompo.oops.owl`) saem de
`../verification/rodar_oops.py`, pelo mesmo caminho de codigo que os produziu
para o baseline — e essa igualdade que torna os dois relatorios do OOPS!
comparaveis.
"""

from __future__ import annotations

import sys
from pathlib import Path

import rdflib
from rdflib import RDF, RDFS, OWL, Literal, Namespace, URIRef

from anotacoes_ontompo import CLASSES, ESTEREOTIPOS
from rdf_deterministico import GrafoOrdenado, carregar, normalizado

TTL_PADRAO = Path("artifacts/ontology/rodada-2/ontompo-rodada-2.ttl")
SAIDA_PADRAO = Path("artifacts/ontology/owl")
GUFO_LOCAL = Path("sources/gufo/gufo.ttl")
# So `metricas.md` o le, e so para ter a coluna do "antes" ao lado das outras.
BASELINE_TTL = Path("artifacts/ontology/baseline/ontompo-as-is.ttl")

ONTOLOGIA = URIRef("https://example.org/ontompo/rodada-2")
ONTOMPO = Namespace("https://example.org/ontompo/rodada-2#")
GUFO = Namespace("http://purl.org/nemo/gufo#")
GUFO_IRI = URIRef("http://purl.org/nemo/gufo")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
DCT = Namespace("http://purl.org/dc/terms/")
VANN = Namespace("http://purl.org/vocab/vann/")

PT = "pt-BR"

# Predicados que anotam sem afirmar nada sobre o dominio. Separa-los do resto e
# o que permite contar axiomas logicos em `metricas.md`.
ANOTACOES = {
    RDFS.label,
    RDFS.comment,
    RDFS.isDefinedBy,
    SKOS.prefLabel,
    OWL.versionInfo,
    DCT.title,
    DCT.description,
    DCT.license,
    DCT.rights,
    VANN.preferredNamespacePrefix,
    VANN.preferredNamespaceUri,
}

# Tipos que a C1 re-declara localmente, quando a gUFO os declara.
TIPOS_DECLARAVEIS = [OWL.Class, OWL.ObjectProperty, OWL.DatatypeProperty, OWL.AnnotationProperty]

# O que mais a C1 copia da gUFO sobre cada termo que o artefato usa. Sao os
# predicados que dizem o que o termo *e* — nao a taxonomia da gUFO nem as suas
# definicoes, que ficam de fora de proposito: o artefato importa a gUFO, nao a
# inclui, e o `rdfs:isDefinedBy` diz onde a definicao esta.
PREDICADOS_DA_DECLARACAO = [RDFS.label, RDFS.domain, RDFS.range]


def _lista_rdf(itens: list[URIRef], prefixo_do_no: str) -> tuple[URIRef, list[tuple]]:
    """Monta uma lista RDF com nos anonimos de rotulo estavel.

    Os rotulos sao reescritos por conteudo em `normalizado()`; os daqui existem
    so para que a montagem nao dependa do sorteio da rdflib.
    """
    triplas: list[tuple] = []
    cabeca = RDF.nil
    for indice in range(len(itens) - 1, -1, -1):
        no = rdflib.term.BNode(f"{prefixo_do_no}_{indice}")
        triplas.append((no, RDF.first, itens[indice]))
        triplas.append((no, RDF.rest, cabeca))
        cabeca = no
    return cabeca, triplas


def _nome(iri: URIRef) -> str:
    return str(iri).rsplit("#", 1)[-1]


def _namespace(grafo: rdflib.Graph) -> str:
    """O namespace do dominio, lido do proprio grafo.

    Cada modelo tem o seu — o baseline usa `.../as-is#`, a rodada 2 usa
    `.../rodada-2#` —, e `metricas.md` mede os dois lado a lado. Deduzi-lo da
    `owl:Ontology` evita passar o namespace certo em cada chamada.
    """
    ontologias = sorted(
        (s for s in grafo.subjects(RDF.type, OWL.Ontology) if isinstance(s, URIRef)), key=str
    )
    if len(ontologias) != 1:
        raise RuntimeError(f"esperava uma owl:Ontology no grafo, achei {len(ontologias)}")
    return f"{ontologias[0]}#"


def _sujeitos_do_tipo(grafo: rdflib.Graph, tipo: URIRef, namespace: str) -> list[URIRef]:
    return sorted(
        (
            s
            for s in grafo.subjects(RDF.type, tipo)
            if isinstance(s, URIRef) and str(s).startswith(namespace)
        ),
        key=str,
    )


def _propriedades_de_objeto(gerado: rdflib.Graph, namespace: str | None = None) -> list[URIRef]:
    return _sujeitos_do_tipo(gerado, OWL.ObjectProperty, namespace or str(ONTOMPO))


def _classes_nomeadas(gerado: rdflib.Graph, namespace: str | None = None) -> list[URIRef]:
    return _sujeitos_do_tipo(gerado, OWL.Class, namespace or str(ONTOMPO))


# --------------------------------------------------------------------------- #
# As cinco customizacoes                                                        #
# --------------------------------------------------------------------------- #


def _termos_gufo_usados(gerado: rdflib.Graph, gufo: rdflib.Graph) -> list[URIRef]:
    """Os termos da gUFO que o artefato usa, mais os que o dominio e o alcance deles trazem.

    Declarar `gufo:mediates` sem declarar o `gufo:Endurant` do seu alcance
    deixaria o artefato apontando para um termo que ele nao declara — trocaria
    um elemento sem tipo por outro. O fecho e pequeno, tres termos alem dos
    dezenove que o artefato cita diretamente, porque so `rdfs:domain` e
    `rdfs:range` sao seguidos.
    """
    fecho = {
        termo
        for tripla in gerado
        for termo in tripla
        if isinstance(termo, URIRef)
        and str(termo).startswith(str(GUFO))
        and str(termo) != str(GUFO)
    }
    while True:
        novos = {
            objeto
            for termo in fecho
            for predicado in (RDFS.domain, RDFS.range)
            for objeto in gufo.objects(termo, predicado)
            if isinstance(objeto, URIRef) and str(objeto).startswith(str(GUFO))
        } - fecho
        if not novos:
            return sorted(fecho, key=str)
        fecho |= novos


def c1_declarar_termos_gufo(gerado: rdflib.Graph, gufo: rdflib.Graph) -> list[tuple]:
    """Re-declara localmente cada termo da gUFO que o artefato usa."""
    triplas: list[tuple] = []
    for termo in _termos_gufo_usados(gerado, gufo):
        tipos = [t for t in TIPOS_DECLARAVEIS if (termo, RDF.type, t) in gufo]
        if not tipos:
            raise RuntimeError(
                f"{termo} e usado pelo artefato e a gUFO local nao o declara: "
                "ou o termo esta errado, ou sources/gufo/gufo.ttl mudou"
            )
        for tipo in tipos:
            triplas.append((termo, RDF.type, tipo))
        for predicado in PREDICADOS_DA_DECLARACAO:
            for objeto in sorted(gufo.objects(termo, predicado), key=str):
                if isinstance(objeto, rdflib.term.BNode):
                    # A gUFO da a `gufo:isDerivedFrom` um dominio que e uma
                    # expressao de classe anonima. Copiar o no sem o conteudo
                    # dele deixaria um `rdfs:domain [ ]` vazio no artefato, que
                    # e pior do que nao declarar dominio nenhum; copiar o
                    # conteudo seria trazer a gUFO para dentro.
                    continue
                triplas.append((termo, predicado, objeto))
        triplas.append((termo, RDFS.isDefinedBy, GUFO_IRI))
    return triplas


def c2_anotar(gerado: rdflib.Graph, gufo: rdflib.Graph) -> list[tuple]:
    """Devolve as definicoes ao modelo, e o rotulo preferido ao vocabulario."""
    triplas: list[tuple] = []

    classes = _classes_nomeadas(gerado)
    faltando = sorted(_nome(c) for c in classes if _nome(c) not in CLASSES)
    sobrando = sorted(set(CLASSES) - {_nome(c) for c in classes})
    if faltando or sobrando:
        raise RuntimeError(
            "anotacoes_ontompo.CLASSES nao corresponde ao modelo — "
            f"sem verbete: {faltando}; verbete sem classe: {sobrando}"
        )

    for classe in classes:
        definicao, rotulo_pt, rotulo_en, _origem = CLASSES[_nome(classe)]
        triplas.append((classe, RDFS.comment, Literal(definicao, lang=PT)))
        triplas.append((classe, SKOS.prefLabel, Literal(rotulo_pt, lang=PT)))
        triplas.append((classe, SKOS.prefLabel, Literal(rotulo_en, lang="en")))
        triplas.append((classe, RDFS.isDefinedBy, ONTOLOGIA))

    for propriedade in _propriedades_de_objeto(gerado):
        estereotipo, origem, destino = _partes_do_nome(propriedade)
        modelo_direto = ESTEREOTIPOS[estereotipo][0]
        triplas.append(
            (
                propriedade,
                RDFS.comment,
                Literal(modelo_direto.format(origem=origem, destino=destino), lang=PT),
            )
        )
        triplas.append((propriedade, RDFS.isDefinedBy, ONTOLOGIA))

    return triplas


def c3_disjuncoes(gerado: rdflib.Graph, gufo: rdflib.Graph) -> list[tuple]:
    """Declara disjunto o que a UFO ja obriga a ser disjunto."""
    triplas: list[tuple] = []

    kinds = sorted(
        (s for s in gerado.subjects(RDF.type, GUFO.Kind) if isinstance(s, URIRef)), key=str
    )
    if len(kinds) < 2:
        raise RuntimeError("nenhum «kind» no artefato: a disjuncao de kinds nao teria sentido")

    componentes = [ONTOMPO.DataManager, ONTOMPO.View, ONTOMPO.ProjectObservatory]
    for alvo in componentes:
        if (alvo, RDF.type, OWL.Class) not in gerado:
            raise RuntimeError(f"{alvo} nao esta no artefato gerado")

    for prefixo, membros in (("kinds", kinds), ("softwares", componentes)):
        cabeca, triplas_da_lista = _lista_rdf(list(membros), f"disj_{prefixo}")
        no = rdflib.term.BNode(f"disj_{prefixo}")
        triplas.append((no, RDF.type, OWL.AllDisjointClasses))
        triplas.append((no, OWL.members, cabeca))
        triplas.extend(triplas_da_lista)

    return triplas


def _partes_do_nome(propriedade: URIRef) -> tuple[str, str, str]:
    partes = _nome(propriedade).split("_")
    if len(partes) != 3 or partes[0] not in ESTEREOTIPOS:
        raise RuntimeError(
            f"{propriedade} nao segue `<estereotipo>_<origem>_<destino>`: "
            "a regra de nomeacao da transformacao mudou"
        )
    return partes[0], partes[1], partes[2]


def c4_inversas(gerado: rdflib.Graph, gufo: rdflib.Graph) -> list[tuple]:
    """Nomeia a inversa de cada propriedade, para que a consulta ande nos dois sentidos."""
    triplas: list[tuple] = []
    for propriedade in _propriedades_de_objeto(gerado):
        estereotipo, origem, destino = _partes_do_nome(propriedade)
        _direto, modelo_inverso, token = ESTEREOTIPOS[estereotipo]
        inversa = ONTOMPO[f"{token}_{destino}_{origem}"]
        if (inversa, None, None) in gerado:
            raise RuntimeError(f"{inversa} ja existe no gerado: a inversa colidiria")

        dominio = gerado.value(propriedade, RDFS.domain)
        alcance = gerado.value(propriedade, RDFS.range)
        if dominio is None or alcance is None:
            raise RuntimeError(f"{propriedade} nao tem dominio e alcance: a inversa seria cega")

        triplas.append((inversa, RDF.type, OWL.ObjectProperty))
        triplas.append((inversa, OWL.inverseOf, propriedade))
        triplas.append((propriedade, OWL.inverseOf, inversa))
        triplas.append((inversa, RDFS.domain, alcance))
        triplas.append((inversa, RDFS.range, dominio))
        triplas.append((inversa, RDFS.label, Literal(_nome(inversa), lang="en")))
        triplas.append(
            (
                inversa,
                RDFS.comment,
                Literal(modelo_inverso.format(origem=destino, destino=origem), lang=PT),
            )
        )
        triplas.append((inversa, RDFS.isDefinedBy, ONTOLOGIA))
    return triplas


def c5_metadados(gerado: rdflib.Graph, gufo: rdflib.Graph) -> list[tuple]:
    """Da identidade, licenca e prefixo ao artefato, sem dar autoria."""
    if (ONTOLOGIA, RDF.type, OWL.Ontology) not in gerado:
        raise RuntimeError(f"{ONTOLOGIA} nao e declarada owl:Ontology no gerado")
    return [
        (
            ONTOLOGIA,
            DCT.title,
            Literal("OntoMPO — ontologia do Modelo para Observatórios de Projetos", lang=PT),
        ),
        (
            ONTOLOGIA,
            DCT.description,
            Literal(
                "Formalização do MPO revisada por análise ontológica fundamentada na UFO. "
                "Gerada a partir do modelo OntoUML pela transformação gUFO oficial e "
                "customizada por acréscimo; o acréscimo está no arquivo "
                "diff-gerado-customizado.ttl.",
                lang=PT,
            ),
        ),
        (ONTOLOGIA, DCT.license, URIRef("https://creativecommons.org/licenses/by/4.0/")),
        (ONTOLOGIA, OWL.versionInfo, Literal("rodada-2, customizada")),
        (ONTOLOGIA, VANN.preferredNamespacePrefix, Literal("ontompo")),
        (ONTOLOGIA, VANN.preferredNamespaceUri, Literal(str(ONTOMPO))),
        (
            ONTOLOGIA,
            RDFS.comment,
            Literal(
                "Sem dct:creator: enquanto a revisão do artigo for duplamente anônima, "
                "declarar autoria aqui a quebraria. O IRI de exemplo é provisório e é "
                "fixado no depósito.",
                lang=PT,
            ),
        ),
    ]


CUSTOMIZACOES = [
    {
        "id": "C1",
        "titulo": "Declaração local dos termos da gUFO que o artefato usa",
        "aplicar": c1_declarar_termos_gufo,
        "o_que": (
            "Cada IRI da gUFO referenciado pelo artefato — `gufo:Kind`, `gufo:Role`, "
            "`gufo:mediates`, `gufo:participatedIn` e os demais — recebe aqui o que a gUFO diz "
            "sobre ele: o tipo, o rótulo, o domínio e o alcance, mais `rdfs:isDefinedBy` "
            "apontando para lá. Tudo é **copiado** de `sources/gufo/gufo.ttl`, não escolhido; se "
            "um termo usado não estiver declarado lá, a geração falha.\n\n"
            "O conjunto fecha sobre domínio e alcance: declarar `gufo:mediates` sem declarar o "
            "`gufo:Endurant` do alcance dele trocaria um elemento sem tipo por outro. São "
            "dezenove termos citados pelo artefato e três que o fecho traz.\n\n"
            "O que **não** é copiado: a taxonomia da gUFO (`rdfs:subClassOf`) e as definições "
            "dela. O artefato importa a gUFO, não a inclui. E um `rdfs:domain` cujo valor na "
            "gUFO é uma expressão de classe anônima fica sem cópia — copiá-lo vazio seria pior "
            "que não declarar."
        ),
        "por_que": (
            "O artefato precisa se sustentar quando o `owl:imports` não é dereferenciado, e não é "
            "hipótese: é o que o OOPS! faz — a cópia submetida a ele tem o `owl:imports` removido, "
            "porque com ele o serviço devolve `unexpected_error`. Sem as declarações, treze "
            "elementos apareciam como *untyped class* (P34) e três como *untyped property* (P35) "
            "no relatório do baseline, e `evidencias-A1-A9.md` os registrou como artefato do "
            "pipeline, não como defeito do modelo. São artefato do pipeline, e é aqui que o "
            "pipeline os resolve. Como cada tripla repete o que a gUFO afirma, nada de novo é "
            "afirmado sobre o domínio.\n\n"
            "Tem um custo, e ele está medido em `comparacao-oops.md`: um termo declarado passa a "
            "ser um elemento que o OOPS! avalia, e os termos da gUFO, avaliados fora da "
            "ontologia deles, aparecem sem anotação própria (P08) e sem ligação com o resto "
            "(P04). Fechar isso exigiria trazer a gUFO para dentro do arquivo, que é exatamente "
            "o que o `owl:imports` existe para evitar."
        ),
    },
    {
        "id": "C2",
        "titulo": "Definições e rótulos preferidos, fechando B3 e B5",
        "aplicar": c2_anotar,
        "o_que": (
            "Toda classe ganha `rdfs:comment` com sua definição em português, e `skos:prefLabel` "
            "em português e em inglês. Toda propriedade de objeto ganha `rdfs:comment` derivado do "
            "seu estereótipo. As definições estão em `tools/generation/anotacoes_ontompo.py`, cada "
            "uma com a origem declarada: `glossario` para as que vêm do Apêndice A da "
            "conceituação do MPO, `modelo` para as que foram redigidas a partir do papel do "
            "conceito nos diagramas, `revisao` para os conceitos que a análise introduziu."
        ),
        "por_que": (
            "É o achado **B3**, e ele é o mais embaraçoso dos que a reconstrução expôs: o OOPS! "
            "acusa 63 elementos sem anotação no modelo *as-is*, enquanto o Apêndice A **define 53 "
            "termos**. As definições existiam; a formalização as descartou. Uma ontologia de "
            "referência sem definição não resolve o problema que este trabalho diz resolver — "
            "duas iniciativas que se dizem aderentes ao MPO sob leituras incompatíveis não têm "
            "onde arbitrar a divergência, e a QC7 não teria o que comparar.\n\n"
            "O rótulo preferido em inglês é também onde **B5** é endereçado: `Stakeholder` com h "
            "minúsculo, `CRUD` como acrônimo, `Data Source` separado. O **IRI não muda**, e essa é "
            "uma escolha, não um esquecimento: renomear `ontompo:StakeHolder` quebraria a "
            "correspondência entre o elemento OWL e o elemento OntoUML que o gerou, que é "
            "justamente a garantia que a transformação oficial oferece. P22 é um *pitfall* "
            "lexical, e o que se lê é o rótulo."
        ),
    },
    {
        "id": "C3",
        "titulo": "Axiomas de disjunção, fechando B4",
        "aplicar": c3_disjuncoes,
        "o_que": (
            "Dois `owl:AllDisjointClasses`. O primeiro declara mutuamente disjuntos todos os "
            "«kind» do modelo, coletados do próprio artefato pelo tipo `gufo:Kind`. O segundo "
            "declara disjuntos `DataManager`, `View` e `ProjectObservatory`, os três subtipos de "
            "`Software`."
        ),
        "por_que": (
            "É o achado **B4**: fora das duas partições que as rodadas introduziram, o modelo não "
            "declara disjunção em lugar nenhum. A disjunção entre kinds não é uma decisão de "
            "modelagem — é consequência da UFO. Um «kind» fornece um princípio de identidade, e "
            "dois princípios de identidade distintos não podem valer para o mesmo indivíduo; "
            "declarar a disjunção só torna verificável o que a semântica do estereótipo já "
            "afirmava, e a transformação gUFO não carrega para o OWL.\n\n"
            "A segunda disjunção fecha o que sobrou de **A9**: o `componentOf` entre `DataManager` "
            "e `ProjectObservatory` é parthood própria, que é irreflexiva, e a `ViewProvision` "
            "medeia um gerenciador e uma visão como relata distintos. O que o modelo tratava como "
            "óbvio passa a ser checável.\n\n"
            "O que **não** foi declarado disjunto, deliberadamente: os papéis irmãos "
            "(`Collector`, `Processor`, `Storer`, `CrudRepository`; `Disseminator`, `Reporter`, "
            "`CrudView`). Nada no material de origem impede que um mesmo componente de software "
            "colete e armazene, e afirmar disjunção ali seria decidir sobre o domínio, não sobre "
            "a formalização."
        ),
    },
    {
        "id": "C4",
        "titulo": "Inversas nomeadas para cada propriedade de objeto",
        "aplicar": c4_inversas,
        "o_que": (
            "Cada propriedade `<estereótipo>_<origem>_<destino>` ganha uma inversa "
            "`<token>_<destino>_<origem>`, com domínio e alcance trocados, rótulo e definição. O "
            "token vem do estereótipo: `mediation` dá `mediatedBy`, `participation` dá "
            "`hasParticipant`, `componentOf` dá `hasComponent`, e assim por diante. O "
            "`owl:inverseOf` é declarado nos dois sentidos — logicamente redundante, e é a forma "
            "que uma ferramenta que só olhe o sujeito consegue ler."
        ),
        "por_que": (
            "A transformação roda com `createInverses: false`, e o relatório do baseline registrou "
            "os 21 elementos de P13 como artefato do pipeline — o que continua verdadeiro: não é "
            "defeito do modelo. É, porém, uma limitação do artefato OWL, e ela aparece na "
            "avaliação: a QC6 pede a cadeia de proveniência de um conteúdo divulgado até a fonte "
            "de dados, e essa cadeia se percorre no sentido contrário ao das participações "
            "geradas, que vão do endurante para o evento. Sem inversa nomeada, a consulta precisa "
            "de caminho invertido a cada passo.\n\n"
            "O artefato gerado já usa as inversas — em `owl:onProperty [ owl:inverseOf ... ]`, "
            "dentro das restrições. Elas existiam anônimas; a customização apenas lhes dá nome."
        ),
    },
    {
        "id": "C5",
        "titulo": "Metadados da ontologia",
        "aplicar": c5_metadados,
        "o_que": (
            "Título, descrição, licença CC BY 4.0, `owl:versionInfo` e o par `vann:` de prefixo e "
            "namespace preferidos, sobre a `owl:Ontology`."
        ),
        "por_que": (
            "O depósito aberto (ticket 09) exige licença e identificação do artefato, e um "
            "arquivo OWL sem elas é um arquivo que ninguém sabe se pode reusar. **Não** há "
            "`dct:creator`: enquanto a revisão for duplamente anônima, declarar autoria dentro do "
            "artefato a quebraria — o depósito é anônimo por requisito, e o IRI de exemplo "
            "continua provisório até o ticket 09."
        ),
    },
]


# --------------------------------------------------------------------------- #
# Relatorios                                                                    #
# --------------------------------------------------------------------------- #


def _turtle_curto(termo) -> str:
    texto = str(termo)
    if isinstance(termo, Literal):
        marca = f"@{termo.language}" if termo.language else ""
        return f'"{texto}"{marca}'
    if isinstance(termo, rdflib.term.BNode):
        return "[]"
    for prefixo, iri in (
        ("ontompo:", str(ONTOMPO)),
        ("gufo:", str(GUFO)),
        ("owl:", str(OWL)),
        ("rdfs:", str(RDFS)),
        ("rdf:", str(RDF)),
        ("skos:", str(SKOS)),
        ("dct:", str(DCT)),
        ("vann:", str(VANN)),
    ):
        if texto.startswith(iri):
            return prefixo + texto[len(iri) :]
    return f"<{texto}>"


def _contagens(triplas: list[tuple]) -> dict[str, int]:
    return {
        "triplas": len(triplas),
        "anotacoes": sum(1 for t in triplas if t[1] in ANOTACOES),
        "axiomas": sum(1 for t in triplas if t[1] not in ANOTACOES),
    }


def relatorio_customizacoes(por_customizacao: dict[str, list[tuple]]) -> str:
    linhas = [
        "# As customizações da OWL, uma a uma",
        "",
        "A transformação gUFO oficial produz a OWL a partir do modelo OntoUML; este documento "
        "registra o que foi acrescentado por cima dela, e por quê. Gerado por "
        "`tools/generation/customizar_owl.py` — não editar à mão.",
        "",
        "**Toda customização é aditiva.** Nenhuma tripla gerada pela transformação foi removida "
        "ou alterada, e a contenência é verificada a cada execução por "
        "`tools/verification/verificar_owl.py`. É essa a garantia de preservação semântica: ela "
        "não depende de inspeção, e sim de o artefato customizado conter o gerado inteiro. O "
        "acréscimo, isolado, está em `diff-gerado-customizado.ttl`.",
        "",
        "| # | Customização | Triplas acrescentadas |",
        "|---|---|---|",
    ]
    for customizacao in CUSTOMIZACOES:
        quantidade = len(por_customizacao[customizacao["id"]])
        linhas.append(f"| {customizacao['id']} | {customizacao['titulo']} | {quantidade} |")
    total = sum(len(v) for v in por_customizacao.values())
    linhas.append(f"| | **total** | **{total}** |")
    linhas.append("")

    for customizacao in CUSTOMIZACOES:
        linhas.append(f"## {customizacao['id']} — {customizacao['titulo']}")
        linhas.append("")
        linhas.append("**O que faz.** " + customizacao["o_que"])
        linhas.append("")
        linhas.append("**Por que.** " + customizacao["por_que"])
        linhas.append("")

    linhas.append("## O que deliberadamente não foi customizado")
    linhas.append("")
    linhas.append(
        "- **Os IRIs.** Renomear `ontompo:StakeHolder` ou `ontompo:CrudOperation` fecharia P22 "
        "no relatório, e quebraria a correspondência entre cada elemento OWL e o elemento "
        "OntoUML que o gerou — que é a garantia pela qual se usa a transformação oficial em "
        "vez de traduzir à mão. B5 é endereçado por `skos:prefLabel`."
    )
    linhas.append(
        "- **Os nomes gerados das propriedades** (`mediation_Log_Agent` e afins), pela mesma "
        "razão. O sublinhado contra o CamelCase das classes é o que P22 aponta."
    )
    linhas.append(
        "- **A dupla tipagem de cada classe** como `owl:Class` e `owl:NamedIndividual`. É o "
        "*punning* que a gUFO exige para que uma classe possa ser instância de `gufo:Kind`; "
        "parece redundância e não é."
    )
    linhas.append(
        "- **Disjunção entre papéis irmãos**, e qualquer axioma que exigisse decidir o que o "
        "material de origem não diz."
    )
    linhas.append(
        "- **Regras SWRL, cadeias de papéis e axiomatização pesada**, fora de escopo por decisão "
        "de pesquisa registrada no *spec*."
    )
    linhas.append("")
    return "\n".join(linhas) + "\n"


def relatorio_diff(
    gerado: rdflib.Graph, customizado: rdflib.Graph, por_customizacao: dict[str, list[tuple]]
) -> str:
    linhas = [
        "# Diff: a OWL gerada contra a OWL customizada",
        "",
        "Derivado dos dois grafos a cada execução de `tools/generation/customizar_owl.py`. A "
        "leitura de cada acréscimo — o que é e por que existe — está em `customizacoes.md`; as "
        "triplas cruas, em `diff-gerado-customizado.ttl`.",
        "",
        "## Contagens",
        "",
        "| | gerada | customizada |",
        "|---|---|---|",
        f"| triplas | {len(gerado)} | {len(customizado)} |",
    ]
    antes = _contagens(list(gerado))
    depois = _contagens(list(customizado))
    for rotulo, chave in (("anotações", "anotacoes"), ("axiomas", "axiomas")):
        linhas.append(f"| {rotulo} | {antes[chave]} | {depois[chave]} |")
    linhas.append("")
    linhas.append(
        f"Removidas: **0**. Alteradas: **0**. Acrescentadas: "
        f"**{len(customizado) - len(gerado)}**."
    )
    linhas.append("")

    for customizacao in CUSTOMIZACOES:
        triplas = por_customizacao[customizacao["id"]]
        linhas.append(f"## {customizacao['id']} — {customizacao['titulo']} ({len(triplas)})")
        linhas.append("")
        linhas.append("| sujeito | predicado | objeto |")
        linhas.append("|---|---|---|")
        for sujeito, predicado, objeto in triplas:
            celulas = [
                _turtle_curto(termo).replace("|", "\\|") for termo in (sujeito, predicado, objeto)
            ]
            linhas.append("| " + " | ".join(f"`{celula}`" for celula in celulas) + " |")
        linhas.append("")
    return "\n".join(linhas) + "\n"


def _metricas(grafo: rdflib.Graph) -> dict[str, int]:
    triplas = list(grafo)
    namespace = _namespace(grafo)
    classes = _classes_nomeadas(grafo, namespace)
    objeto = _propriedades_de_objeto(grafo, namespace)
    dados = _sujeitos_do_tipo(grafo, OWL.DatatypeProperty, namespace)
    anonimas = {
        s
        for s in grafo.subjects(RDF.type, OWL.Restriction)
        if isinstance(s, rdflib.term.BNode)
    } | {s for s in grafo.subjects(RDF.type, OWL.Class) if isinstance(s, rdflib.term.BNode)}
    disjuncoes = len(list(grafo.subjects(RDF.type, OWL.AllDisjointClasses))) + len(
        list(grafo.triples((None, OWL.disjointWith, None)))
    )
    contagens = _contagens(triplas)
    return {
        "classes nomeadas": len(classes),
        "expressões de classe anônimas": len(anonimas),
        "propriedades de objeto": len(objeto),
        "propriedades de dados": len(dados),
        "subsunções (`rdfs:subClassOf`)": len(list(grafo.triples((None, RDFS.subClassOf, None)))),
        "equivalências": len(list(grafo.triples((None, OWL.equivalentClass, None)))),
        "conjuntos de disjunção": disjuncoes,
        # Pares, nao declaracoes: a customizacao afirma `owl:inverseOf` nos dois
        # sentidos, e contar as declaracoes daria o dobro das inversas que ha.
        "pares de inversas nomeadas": len(
            {
                frozenset((str(s), str(o)))
                for s, o in grafo.subject_objects(OWL.inverseOf)
                if isinstance(s, URIRef) and isinstance(o, URIRef)
            }
        ),
        "axiomas": contagens["axiomas"],
        "anotações": contagens["anotacoes"],
        "triplas": contagens["triplas"],
    }


def relatorio_metricas(colunas: list[tuple[str, rdflib.Graph]]) -> str:
    medidas = [(rotulo, _metricas(grafo)) for rotulo, grafo in colunas]
    chaves = list(medidas[0][1])
    linhas = [
        "# Métricas dos artefatos OWL",
        "",
        "Derivadas dos arquivos a cada execução de `tools/generation/customizar_owl.py`. Contam o "
        "que está **no arquivo**: a gUFO importada não entra, porque o que está sob avaliação é a "
        "ontologia de domínio.",
        "",
        "| | " + " | ".join(rotulo for rotulo, _ in medidas) + " |",
        "|---" * (len(medidas) + 1) + "|",
    ]
    for chave in chaves:
        valores = " | ".join(str(medida[chave]) for _, medida in medidas)
        linhas.append(f"| {chave} | {valores} |")
    linhas.append("")
    linhas.append("## Como se conta")
    linhas.append("")
    linhas.append(
        "- **Classes nomeadas** e **propriedades**: sujeitos com o `rdf:type` correspondente e IRI "
        "no namespace da OntoMPO. Os termos da gUFO que a C1 declara localmente ficam de fora — "
        "são dela, não do domínio."
    )
    linhas.append(
        "- **Propriedades de dados: zero**, nos três artefatos, e é um número a declarar, não a "
        "esconder. O modelo publicado não tem nenhum atributo, embora o Apêndice A da "
        "conceituação especifique atributos de classe e de instância para cada conceito — é o "
        "achado **B6**. A camada de atributos é do ticket 07, onde a instanciação a exige: a QC3 "
        "pergunta *quando* uma carga ocorreu e a QC6 pede a cadeia de proveniência."
    )
    linhas.append(
        "- **Axiomas** são as triplas cujo predicado não é de anotação; **anotações**, as demais. "
        "A soma das duas é o total de triplas. Não é a contagem de axiomas lógicos da OWL 2, que "
        "agruparia várias triplas em um axioma só — é a contagem que se pode derivar do arquivo "
        "sem um raciocinador, e ela é comparável entre as colunas porque é a mesma regra nas três."
    )
    linhas.append("")
    return "\n".join(linhas) + "\n"


# --------------------------------------------------------------------------- #


def main() -> int:
    caminho_ttl = Path(sys.argv[1]) if len(sys.argv) > 1 else TTL_PADRAO
    saida = Path(sys.argv[2]) if len(sys.argv) > 2 else SAIDA_PADRAO

    for caminho in (caminho_ttl, GUFO_LOCAL):
        if not caminho.exists():
            print(f"ERRO: {caminho} nao existe.")
            return 1

    gerado = carregar(caminho_ttl)
    gufo = rdflib.Graph()
    gufo.parse(GUFO_LOCAL.as_posix(), format="turtle")

    por_customizacao: dict[str, list[tuple]] = {}
    acrescimo = GrafoOrdenado()
    for customizacao in CUSTOMIZACOES:
        triplas = customizacao["aplicar"](gerado, gufo)
        novas = [t for t in triplas if t not in gerado and t not in acrescimo]
        if len(novas) != len(set(novas)):
            raise RuntimeError(f"{customizacao['id']} produziu triplas repetidas")
        por_customizacao[customizacao["id"]] = novas
        for tripla in novas:
            acrescimo.add(tripla)

    customizado = GrafoOrdenado()
    for prefixo, iri in gerado.namespaces():
        customizado.bind(prefixo, iri)
    for prefixo, iri in (("skos", SKOS), ("dct", DCT), ("vann", VANN)):
        customizado.bind(prefixo, iri)
    for tripla in gerado:
        customizado.add(tripla)
    for tripla in acrescimo:
        customizado.add(tripla)

    faltando = [t for t in gerado if t not in customizado]
    if faltando:
        raise RuntimeError(f"a customizacao deixou de ser aditiva: {len(faltando)} triplas perdidas")

    customizado = normalizado(customizado)
    acrescimo_normalizado = normalizado(acrescimo)
    for prefixo, iri in (("ontompo", ONTOMPO), ("gufo", GUFO), ("skos", SKOS)):
        acrescimo_normalizado.bind(prefixo, iri)

    saida.mkdir(parents=True, exist_ok=True)
    (saida / "ontompo.ttl").write_text(customizado.serialize(format="turtle"), encoding="utf-8")
    (saida / "diff-gerado-customizado.ttl").write_text(
        acrescimo_normalizado.serialize(format="turtle"), encoding="utf-8"
    )
    (saida / "customizacoes.md").write_text(
        relatorio_customizacoes(por_customizacao), encoding="utf-8"
    )
    (saida / "diff-gerado-customizado.md").write_text(
        relatorio_diff(gerado, customizado, por_customizacao), encoding="utf-8"
    )
    (saida / "metricas.md").write_text(
        relatorio_metricas(
            [
                ("baseline", carregar(BASELINE_TTL)),
                ("rodada 2, gerada", gerado),
                ("rodada 2, customizada", customizado),
            ]
        ),
        encoding="utf-8",
    )

    print(f"OWL customizada -> {saida / 'ontompo.ttl'}")
    print(f"triplas: {len(gerado)} geradas + {len(acrescimo)} acrescentadas = {len(customizado)}")
    for customizacao in CUSTOMIZACOES:
        print(f"  {customizacao['id']}: {len(por_customizacao[customizacao['id']])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
