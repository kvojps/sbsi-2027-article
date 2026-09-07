# QC3 — Que agente executou a carga de uma dada fonte de dados, e quando?

Cenário: observatório de projetos de pesquisa e extensão de uma universidade pública brasileira, descrito nos Anais Estendidos do XVIII SBSI (2022), DOI 10.5753/sbsi_estendido.2022.222995. Trabalho anterior do próprio autor, referido em terceira pessoa. A pergunta é de domínio e só passou a ter resposta na segunda rodada: a análise moveu Extract, Transform e Load de «relator» endurante para «event» UFO-B (A5). A carga de uma fonte é o evento Load que pertence ao mesmo EtlProcess que a extração daquela fonte; quem a executou são os participantes nos papéis Processor e Storer; o "quando" é gufo:hasEndPointInXSDDate sobre o Load, que gufo:Event já provê e a instanciação preenche. Sem a cadeia de ETL ou sem as subpropriedades de gufo:participatedIn que a análise introduziu, não devolve linha nenhuma.

Executada por `tools/generation/rodar_consultas.py` sobre a ontologia revisada (`artifacts/ontology/owl/ontompo.ttl`), a gUFO (`sources/gufo/gufo.ttl`) e os dados de instância dos observatórios (`artifacts/ontology/instancias/observatorio.ttl` e `observatorio-b.ttl`). As QC1–QC6 se prendem ao namespace do observatório principal; só a QC7 atravessa os dois.

## Consulta SPARQL

```sparql
# QC3 — Que agente executou a carga de uma dada fonte de dados, e quando?
# Cenário: observatório de projetos de pesquisa e extensão de uma universidade
# pública brasileira, descrito nos Anais Estendidos do XVIII SBSI (2022),
# DOI 10.5753/sbsi_estendido.2022.222995. Trabalho anterior do próprio autor,
# referido em terceira pessoa.
#
# A pergunta é de domínio e só passou a ter resposta na segunda rodada: a
# análise moveu Extract, Transform e Load de «relator» endurante para «event»
# UFO-B (A5). A carga de uma fonte é o evento Load que pertence ao mesmo
# EtlProcess que a extração daquela fonte; quem a executou são os participantes
# nos papéis Processor e Storer; o "quando" é gufo:hasEndPointInXSDDate sobre o
# Load, que gufo:Event já provê e a instanciação preenche. Sem a cadeia de ETL
# ou sem as subpropriedades de gufo:participatedIn que a análise introduziu, não
# devolve linha nenhuma.
PREFIX ontompo: <https://example.org/ontompo/rodada-2#>
PREFIX obs: <https://example.org/ontompo/instancia-observatorio#>
PREFIX gufo: <http://purl.org/nemo/gufo#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?fonte ?rotuloFonte ?carga ?executor ?rotuloExecutor ?papelExecutor ?quando
WHERE {
  ?fonte a ontompo:DataSource ;
         skos:prefLabel ?rotuloFonte ;
         ontompo:participation_DataSource_Extract ?extracao .
  ?extracao ontompo:participational_Extract_EtlProcess ?processo .
  ?carga a ontompo:Load ;
         ontompo:participational_Load_EtlProcess ?processo ;
         gufo:hasEndPointInXSDDate ?quando .
  ?executor ?participacao ?carga ;
            skos:prefLabel ?rotuloExecutor .
  ?participacao rdfs:subPropertyOf gufo:participatedIn ;
               rdfs:domain ?papelExecutor .
  ?papelExecutor rdfs:subClassOf ontompo:DataManager .
  FILTER (STRSTARTS(STR(?fonte), "https://example.org/ontompo/instancia-observatorio#"))
  FILTER (langMatches(lang(?rotuloFonte), "pt"))
  FILTER (langMatches(lang(?rotuloExecutor), "pt"))
}
ORDER BY ?rotuloFonte ?papelExecutor ?quando ?fonte ?carga
```

## Resultado — 4 linha(s)

| fonte | rotuloFonte | carga | executor | rotuloExecutor | papelExecutor | quando |
|---|---|---|---|---|---|---|
| https://example.org/ontompo/instancia-observatorio#fonteCadastroDeProjetos | Cadastro de projetos pela equipe e pelos coordenadores | https://example.org/ontompo/instancia-observatorio#carga_cadastro | https://example.org/ontompo/instancia-observatorio#gerenciadorDeConteudo | Gerenciamento de conteúdo do observatório | https://example.org/ontompo/rodada-2#Processor | 2023-03-06 |
| https://example.org/ontompo/instancia-observatorio#fonteCadastroDeProjetos | Cadastro de projetos pela equipe e pelos coordenadores | https://example.org/ontompo/instancia-observatorio#carga_cadastro | https://example.org/ontompo/instancia-observatorio#gerenciadorDeConteudo | Gerenciamento de conteúdo do observatório | https://example.org/ontompo/rodada-2#Storer | 2023-03-06 |
| https://example.org/ontompo/instancia-observatorio#fontePlanilhaDadosAbertos | Planilha de dados abertos de projetos institucionais | https://example.org/ontompo/instancia-observatorio#carga_dadosAbertos | https://example.org/ontompo/instancia-observatorio#gerenciadorDeConteudo | Gerenciamento de conteúdo do observatório | https://example.org/ontompo/rodada-2#Processor | 2023-09-11 |
| https://example.org/ontompo/instancia-observatorio#fontePlanilhaDadosAbertos | Planilha de dados abertos de projetos institucionais | https://example.org/ontompo/instancia-observatorio#carga_dadosAbertos | https://example.org/ontompo/instancia-observatorio#gerenciadorDeConteudo | Gerenciamento de conteúdo do observatório | https://example.org/ontompo/rodada-2#Storer | 2023-09-11 |

_Resultado completo, cru, em `qc3-resultado.csv`._
