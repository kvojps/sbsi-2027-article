# QC6 — Dado um conteúdo divulgado, qual a cadeia de proveniência até a fonte de dados original?

Cenário: observatório de projetos de pesquisa e extensão de uma universidade pública brasileira, descrito nos Anais Estendidos do XVIII SBSI (2022), DOI 10.5753/sbsi_estendido.2022.222995. Trabalho anterior do próprio autor, referido em terceira pessoa. A pergunta sustenta a contribuição do artigo — proveniência. Ela só tem caminho a percorrer porque a análise (A5) tornou o ETL um EtlProcess com Extract, Transform e Load como partes próprias: de cada conteúdo divulgado (Disseminator), pelo ViewProvision até o gerenciamento que o disponibiliza, pela participação Storer/Load até a carga, pela parthood de evento até o EtlProcess, e daí à extração e à fonte de dados que dela participou. Devolve a cadeia inteira, nó a nó. Sem a cadeia de ETL ou sem as subpropriedades de gufo:isEventProperPartOf que a análise introduziu, não devolve linha nenhuma.

Executada por `tools/generation/rodar_consultas.py` sobre a ontologia revisada (`artifacts/ontology/owl/ontompo.ttl`), a gUFO (`sources/gufo/gufo.ttl`) e os dados de instância dos observatórios (`artifacts/ontology/instancias/observatorio.ttl` e `observatorio-b.ttl`). As QC1–QC6 se prendem ao namespace do observatório principal; só a QC7 atravessa os dois.

## Consulta SPARQL

```sparql
# QC6 — Dado um conteúdo divulgado, qual a cadeia de proveniência até a fonte de dados original?
# Cenário: observatório de projetos de pesquisa e extensão de uma universidade
# pública brasileira, descrito nos Anais Estendidos do XVIII SBSI (2022),
# DOI 10.5753/sbsi_estendido.2022.222995. Trabalho anterior do próprio autor,
# referido em terceira pessoa.
#
# A pergunta sustenta a contribuição do artigo — proveniência. Ela só tem
# caminho a percorrer porque a análise (A5) tornou o ETL um EtlProcess com
# Extract, Transform e Load como partes próprias: de cada conteúdo divulgado
# (Disseminator), pelo ViewProvision até o gerenciamento que o disponibiliza,
# pela participação Storer/Load até a carga, pela parthood de evento até o
# EtlProcess, e daí à extração e à fonte de dados que dela participou. Devolve a
# cadeia inteira, nó a nó. Sem a cadeia de ETL ou sem as subpropriedades de
# gufo:isEventProperPartOf que a análise introduziu, não devolve linha nenhuma.
PREFIX ontompo: <https://example.org/ontompo/rodada-2#>
PREFIX obs: <https://example.org/ontompo/instancia-observatorio#>
PREFIX gufo: <http://purl.org/nemo/gufo#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?conteudo ?rotuloConteudo ?gerenciamento ?carga ?quando ?processoEtl ?extracao ?fonte ?rotuloFonte
WHERE {
  ?conteudo a ontompo:Disseminator ;
            skos:prefLabel ?rotuloConteudo .
  ontompo:Disseminator rdfs:subClassOf ontompo:View .
  ?provisao a ontompo:ViewProvision ;
            ontompo:mediation_ViewProvision_View ?conteudo ;
            ontompo:mediation_ViewProvision_DataManager ?gerenciamento .
  ?gerenciamento ontompo:participation_Storer_Load ?carga .
  ?carga a ontompo:Load ;
         ontompo:participational_Load_EtlProcess ?processoEtl ;
         gufo:hasEndPointInXSDDate ?quando .
  ?extracao ontompo:participational_Extract_EtlProcess ?processoEtl .
  ?fonte ontompo:participation_DataSource_Extract ?extracao ;
         a ontompo:DataSource ;
         skos:prefLabel ?rotuloFonte .
  FILTER (STRSTARTS(STR(?conteudo), "https://example.org/ontompo/instancia-observatorio#"))
  FILTER (langMatches(lang(?rotuloConteudo), "pt"))
  FILTER (langMatches(lang(?rotuloFonte), "pt"))
}
ORDER BY ?rotuloConteudo ?rotuloFonte ?quando ?conteudo ?carga ?fonte
```

## Resultado — 4 linha(s)

| conteudo | rotuloConteudo | gerenciamento | carga | quando | processoEtl | extracao | fonte | rotuloFonte |
|---|---|---|---|---|---|---|---|---|
| https://example.org/ontompo/instancia-observatorio#analisesDetalhadas | Análises detalhadas dos projetos | https://example.org/ontompo/instancia-observatorio#gerenciadorDeConteudo | https://example.org/ontompo/instancia-observatorio#carga_cadastro | 2023-03-06 | https://example.org/ontompo/instancia-observatorio#processoEtl_cadastro | https://example.org/ontompo/instancia-observatorio#extracao_cadastro | https://example.org/ontompo/instancia-observatorio#fonteCadastroDeProjetos | Cadastro de projetos pela equipe e pelos coordenadores |
| https://example.org/ontompo/instancia-observatorio#analisesDetalhadas | Análises detalhadas dos projetos | https://example.org/ontompo/instancia-observatorio#gerenciadorDeConteudo | https://example.org/ontompo/instancia-observatorio#carga_dadosAbertos | 2023-09-11 | https://example.org/ontompo/instancia-observatorio#processoEtl_dadosAbertos | https://example.org/ontompo/instancia-observatorio#extracao_dadosAbertos | https://example.org/ontompo/instancia-observatorio#fontePlanilhaDadosAbertos | Planilha de dados abertos de projetos institucionais |
| https://example.org/ontompo/instancia-observatorio#downloadDeDadosBrutos | Download de dados brutos dos projetos | https://example.org/ontompo/instancia-observatorio#gerenciadorDeConteudo | https://example.org/ontompo/instancia-observatorio#carga_cadastro | 2023-03-06 | https://example.org/ontompo/instancia-observatorio#processoEtl_cadastro | https://example.org/ontompo/instancia-observatorio#extracao_cadastro | https://example.org/ontompo/instancia-observatorio#fonteCadastroDeProjetos | Cadastro de projetos pela equipe e pelos coordenadores |
| https://example.org/ontompo/instancia-observatorio#downloadDeDadosBrutos | Download de dados brutos dos projetos | https://example.org/ontompo/instancia-observatorio#gerenciadorDeConteudo | https://example.org/ontompo/instancia-observatorio#carga_dadosAbertos | 2023-09-11 | https://example.org/ontompo/instancia-observatorio#processoEtl_dadosAbertos | https://example.org/ontompo/instancia-observatorio#extracao_dadosAbertos | https://example.org/ontompo/instancia-observatorio#fontePlanilhaDadosAbertos | Planilha de dados abertos de projetos institucionais |

_Resultado completo, cru, em `qc6-resultado.csv`._
