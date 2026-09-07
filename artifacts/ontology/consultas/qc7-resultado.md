# QC7 — Dois observatórios distintos que se dizem aderentes ao MPO cobrem os mesmos conceitos?

Cenário A: observatório de projetos de pesquisa e extensão de uma universidade pública brasileira, descrito nos Anais Estendidos do XVIII SBSI (2022), DOI 10.5753/sbsi_estendido.2022.222995. Trabalho anterior do próprio autor, referido em terceira pessoa. Cenário B: um observatório municipal de obras públicas, sintético, construído para esta comparação (premissa registrada no ticket 08). A pergunta sustenta a contribuição do artigo — comparabilidade entre iniciativas. Para cada conceito da OntoMPO (classe com rótulo preferido em português), a consulta conta quantos indivíduos de cada observatório o instanciam, direta ou por subclasse. As linhas em que uma contagem é zero e a outra não são os conceitos em que as duas iniciativas divergem, mesmo ambas se dizendo aderentes ao MPO — é a subdeterminação do modelo, tornada verificável. Conceitos que nenhum dos dois instancia ficam de fora (HAVING). Sem a ontologia, não há classe com rótulo; sem as instâncias, toda contagem é zero e não há linha.

Executada por `tools/generation/rodar_consultas.py` sobre a ontologia revisada (`artifacts/ontology/owl/ontompo.ttl`), a gUFO (`sources/gufo/gufo.ttl`) e os dados de instância dos observatórios (`artifacts/ontology/instancias/observatorio.ttl` e `observatorio-b.ttl`). As QC1–QC6 se prendem ao namespace do observatório principal; só a QC7 atravessa os dois.

## Consulta SPARQL

```sparql
# QC7 — Dois observatórios distintos que se dizem aderentes ao MPO cobrem os mesmos conceitos?
# Cenário A: observatório de projetos de pesquisa e extensão de uma universidade
# pública brasileira, descrito nos Anais Estendidos do XVIII SBSI (2022),
# DOI 10.5753/sbsi_estendido.2022.222995. Trabalho anterior do próprio autor,
# referido em terceira pessoa.
# Cenário B: um observatório municipal de obras públicas, sintético, construído
# para esta comparação (premissa registrada no ticket 08).
#
# A pergunta sustenta a contribuição do artigo — comparabilidade entre
# iniciativas. Para cada conceito da OntoMPO (classe com rótulo preferido em
# português), a consulta conta quantos indivíduos de cada observatório o
# instanciam, direta ou por subclasse. As linhas em que uma contagem é zero e a
# outra não são os conceitos em que as duas iniciativas divergem, mesmo ambas se
# dizendo aderentes ao MPO — é a subdeterminação do modelo, tornada verificável.
# Conceitos que nenhum dos dois instancia ficam de fora (HAVING). Sem a
# ontologia, não há classe com rótulo; sem as instâncias, toda contagem é zero e
# não há linha.
PREFIX ontompo: <https://example.org/ontompo/rodada-2#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?conceito ?rotuloConceito (COUNT(DISTINCT ?iA) AS ?instanciasA) (COUNT(DISTINCT ?iB) AS ?instanciasB)
WHERE {
  ?conceito a owl:Class ;
            skos:prefLabel ?rotuloConceito .
  FILTER (STRSTARTS(STR(?conceito), "https://example.org/ontompo/rodada-2#"))
  FILTER (langMatches(lang(?rotuloConceito), "pt"))
  OPTIONAL {
    ?iA a ?tipoA .
    ?tipoA rdfs:subClassOf* ?conceito .
    FILTER (STRSTARTS(STR(?iA), "https://example.org/ontompo/instancia-observatorio#"))
  }
  OPTIONAL {
    ?iB a ?tipoB .
    ?tipoB rdfs:subClassOf* ?conceito .
    FILTER (STRSTARTS(STR(?iB), "https://example.org/ontompo/instancia-observatorio-b#"))
  }
}
GROUP BY ?conceito ?rotuloConceito
HAVING (COUNT(DISTINCT ?iA) + COUNT(DISTINCT ?iB) > 0)
ORDER BY ?rotuloConceito ?conceito
```

## Resultado — 31 linha(s)

| conceito | rotuloConceito | instanciasA | instanciasB |
|---|---|---|---|
| https://example.org/ontompo/rodada-2#Agent | Agente | 6 | 3 |
| https://example.org/ontompo/rodada-2#PhysicalAgent | Agente físico | 3 | 2 |
| https://example.org/ontompo/rodada-2#SocialAgent | Agente social | 0 | 1 |
| https://example.org/ontompo/rodada-2#Storer | Armazenamento | 1 | 1 |
| https://example.org/ontompo/rodada-2#Load | Carga | 2 | 1 |
| https://example.org/ontompo/rodada-2#Collector | Coleta | 1 | 1 |
| https://example.org/ontompo/rodada-2#Knowledge | Conhecimento | 2 | 0 |
| https://example.org/ontompo/rodada-2#ViewProvision | Disponibilização de visão | 8 | 3 |
| https://example.org/ontompo/rodada-2#Disseminator | Disseminação | 2 | 2 |
| https://example.org/ontompo/rodada-2#Extract | Extração | 2 | 1 |
| https://example.org/ontompo/rodada-2#DataSource | Fonte de dados | 2 | 1 |
| https://example.org/ontompo/rodada-2#DataManager | Gerenciamento de dados | 2 | 1 |
| https://example.org/ontompo/rodada-2#ProjectDataManagement | Gerência de dados de projeto | 2 | 1 |
| https://example.org/ontompo/rodada-2#ObservatoryGroup | Grupo do observatório | 1 | 0 |
| https://example.org/ontompo/rodada-2#SocialInteraction | Interação social | 7 | 0 |
| https://example.org/ontompo/rodada-2#ProjectObservatory | Observatório de projetos | 1 | 1 |
| https://example.org/ontompo/rodada-2#Observation | Observação | 2 | 0 |
| https://example.org/ontompo/rodada-2#Organization | Organização | 0 | 1 |
| https://example.org/ontompo/rodada-2#StakeHolder | Parte interessada | 3 | 0 |
| https://example.org/ontompo/rodada-2#Person | Pessoa | 3 | 2 |
| https://example.org/ontompo/rodada-2#Processor | Processamento | 1 | 1 |
| https://example.org/ontompo/rodada-2#EtlProcess | Processo de ETL | 2 | 1 |
| https://example.org/ontompo/rodada-2#Project | Projeto | 2 | 1 |
| https://example.org/ontompo/rodada-2#Reporter | Relacionamento | 3 | 0 |
| https://example.org/ontompo/rodada-2#System | Sistema | 1 | 1 |
| https://example.org/ontompo/rodada-2#ComputationalSystem | Sistema computacional | 1 | 1 |
| https://example.org/ontompo/rodada-2#Software | Software | 11 | 5 |
| https://example.org/ontompo/rodada-2#Transform | Transformação | 2 | 1 |
| https://example.org/ontompo/rodada-2#ObservatoryUser | Usuário do observatório | 3 | 2 |
| https://example.org/ontompo/rodada-2#View | Visão | 8 | 3 |
| https://example.org/ontompo/rodada-2#CrudView | Visão CRUD | 3 | 1 |

_Resultado completo, cru, em `qc7-resultado.csv`._
