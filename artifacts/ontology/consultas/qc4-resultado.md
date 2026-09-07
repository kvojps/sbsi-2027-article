# QC4 — Quais projetos de um observatório não tiveram observações registradas em um período?

Cenário: observatório de projetos de pesquisa e extensão de uma universidade pública brasileira, descrito nos Anais Estendidos do XVIII SBSI (2022), DOI 10.5753/sbsi_estendido.2022.222995. Trabalho anterior do próprio autor, referido em terceira pessoa. Período consultado: 01/01/2023 a 30/06/2023 (primeiro semestre de 2023). A pergunta é de domínio: um projeto do observatório é o que um ProjectDataManagement liga a um DataManager componente do observatório; ele "teve observação no período" quando existe um evento Observation, datado no período, sobre uma Disseminator que aquele mesmo gerenciamento disponibiliza. A consulta devolve os projetos para os quais essa observação não existe. O evento Observation e a sua data só passaram a caber no modelo com a adoção de UFO-B (B8). Sem a instância ou sem a hierarquia de classes da OntoMPO, não devolve linha nenhuma.

Executada por `tools/generation/rodar_consultas.py` sobre a ontologia revisada (`artifacts/ontology/owl/ontompo.ttl`), a gUFO (`sources/gufo/gufo.ttl`) e os dados de instância dos observatórios (`artifacts/ontology/instancias/observatorio.ttl` e `observatorio-b.ttl`). As QC1–QC6 se prendem ao namespace do observatório principal; só a QC7 atravessa os dois.

## Consulta SPARQL

```sparql
# QC4 — Quais projetos de um observatório não tiveram observações registradas em um período?
# Cenário: observatório de projetos de pesquisa e extensão de uma universidade
# pública brasileira, descrito nos Anais Estendidos do XVIII SBSI (2022),
# DOI 10.5753/sbsi_estendido.2022.222995. Trabalho anterior do próprio autor,
# referido em terceira pessoa.
# Período consultado: 01/01/2023 a 30/06/2023 (primeiro semestre de 2023).
#
# A pergunta é de domínio: um projeto do observatório é o que um
# ProjectDataManagement liga a um DataManager componente do observatório; ele
# "teve observação no período" quando existe um evento Observation, datado no
# período, sobre uma Disseminator que aquele mesmo gerenciamento disponibiliza.
# A consulta devolve os projetos para os quais essa observação não existe. O
# evento Observation e a sua data só passaram a caber no modelo com a adoção de
# UFO-B (B8). Sem a instância ou sem a hierarquia de classes da OntoMPO, não
# devolve linha nenhuma.
PREFIX ontompo: <https://example.org/ontompo/rodada-2#>
PREFIX obs: <https://example.org/ontompo/instancia-observatorio#>
PREFIX gufo: <http://purl.org/nemo/gufo#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?projeto ?rotuloProjeto ?observatorio
WHERE {
  ?observatorio a ontompo:ProjectObservatory .
  ontompo:ProjectObservatory rdfs:subClassOf ontompo:Software .
  ?gerenciador ontompo:componentOf_DataManager_ProjectObservatory ?observatorio .
  ?gerencia a ontompo:ProjectDataManagement ;
            ontompo:mediation_ProjectDataManagement_DataManager ?gerenciador ;
            ontompo:mediation_ProjectDataManagement_Project ?projeto .
  ?projeto a ontompo:Project ;
           skos:prefLabel ?rotuloProjeto .
  FILTER (STRSTARTS(STR(?projeto), "https://example.org/ontompo/instancia-observatorio#"))
  FILTER (langMatches(lang(?rotuloProjeto), "pt"))
  FILTER NOT EXISTS {
    ?provisao ontompo:mediation_ViewProvision_DataManager ?gerenciador ;
              ontompo:mediation_ViewProvision_View ?disseminador .
    ?disseminador ontompo:participation_Disseminator_Observation ?observacao .
    ?observacao gufo:hasEndPointInXSDDate ?data .
    FILTER (?data >= "2023-01-01"^^xsd:date && ?data <= "2023-06-30"^^xsd:date)
  }
}
ORDER BY ?rotuloProjeto ?projeto
```

## Resultado — 1 linha(s)

| projeto | rotuloProjeto | observatorio |
|---|---|---|
| https://example.org/ontompo/instancia-observatorio#projetoPesquisaAplicada | Projeto de pesquisa aplicada (cenário) | https://example.org/ontompo/instancia-observatorio#observatorio |

_Resultado completo, cru, em `qc4-resultado.csv`._
