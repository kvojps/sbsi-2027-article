# QC2 — Quais partes interessadas têm acesso a quais conteúdos de um projeto observado?

Cenário: observatório de projetos de pesquisa e extensão de uma universidade pública brasileira, descrito nos Anais Estendidos do XVIII SBSI (2022), DOI 10.5753/sbsi_estendido.2022.222995. A publicação-fonte é referida em terceira pessoa pelo seu DOI. A pergunta é de domínio: percorre o relator SocialInteraction — o vínculo que a OntoMPO tem entre um agente e o conteúdo do observatório — de cada parte interessada (StakeHolder, que a análise passou a modelar como roleMixin sobre indivíduo, grupo ou organização, A6) até a visão de relacionamento com que ela interage, e daí, pelo ViewProvision e pelo ProjectDataManagement, até o projeto observado cujos dados aquele gerenciamento responde. Sem os dados do observatório, ou sem a hierarquia de View que a análise reorganizou, não devolve linha nenhuma.

Executada por `tools/generation/rodar_consultas.py` sobre a ontologia revisada (`artifacts/ontology/owl/ontompo.ttl`), a gUFO (`sources/gufo/gufo.ttl`) e os dados de instância dos observatórios (`artifacts/ontology/instancias/observatorio.ttl` e `observatorio-b.ttl`). As QC1–QC6 se prendem ao namespace do observatório principal; só a QC7 atravessa os dois.

## Consulta SPARQL

```sparql
# QC2 — Quais partes interessadas têm acesso a quais conteúdos de um projeto observado?
# Cenário: observatório de projetos de pesquisa e extensão de uma universidade
# pública brasileira, descrito nos Anais Estendidos do XVIII SBSI (2022),
# DOI 10.5753/sbsi_estendido.2022.222995. A publicação-fonte é referida em
# terceira pessoa pelo seu DOI.
#
# A pergunta é de domínio: percorre o relator SocialInteraction — o vínculo que
# a OntoMPO tem entre um agente e o conteúdo do observatório — de cada parte
# interessada (StakeHolder, que a análise passou a modelar como roleMixin sobre
# indivíduo, grupo ou organização, A6) até a visão de relacionamento com que ela
# interage, e daí, pelo ViewProvision e pelo ProjectDataManagement, até o projeto
# observado cujos dados aquele gerenciamento responde. Sem os dados do
# observatório, ou sem a hierarquia de View que a análise reorganizou, não
# devolve linha nenhuma.
PREFIX ontompo: <https://example.org/ontompo/rodada-2#>
PREFIX obs: <https://example.org/ontompo/instancia-observatorio#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?parte ?rotuloParte ?conteudo ?rotuloConteudo ?rotuloPapel ?projeto ?rotuloProjeto
WHERE {
  ?interacao a ontompo:SocialInteraction ;
             ontompo:mediation_SocialInteraction_Agent ?parte ;
             ontompo:mediation_SocialInteraction_Reporter ?conteudo .
  ?parte a ontompo:StakeHolder ;
         skos:prefLabel ?rotuloParte .
  ?conteudo a ?papel ;
            skos:prefLabel ?rotuloConteudo .
  ?papel rdfs:subClassOf ontompo:View ;
         skos:prefLabel ?rotuloPapel .
  ?provisao a ontompo:ViewProvision ;
            ontompo:mediation_ViewProvision_View ?conteudo ;
            ontompo:mediation_ViewProvision_DataManager ?gerenciador .
  ?gerencia a ontompo:ProjectDataManagement ;
            ontompo:mediation_ProjectDataManagement_DataManager ?gerenciador ;
            ontompo:mediation_ProjectDataManagement_Project ?projeto .
  ?projeto a ontompo:Project ;
           skos:prefLabel ?rotuloProjeto .
  FILTER (STRSTARTS(STR(?parte), "https://example.org/ontompo/instancia-observatorio#"))
  FILTER (langMatches(lang(?rotuloParte), "pt"))
  FILTER (langMatches(lang(?rotuloConteudo), "pt"))
  FILTER (langMatches(lang(?rotuloPapel), "pt"))
  FILTER (langMatches(lang(?rotuloProjeto), "pt"))
}
ORDER BY ?rotuloParte ?rotuloConteudo ?rotuloProjeto ?parte ?conteudo ?projeto
```

## Resultado — 4 linha(s)

| parte | rotuloParte | conteudo | rotuloConteudo | rotuloPapel | projeto | rotuloProjeto |
|---|---|---|---|---|---|---|
| https://example.org/ontompo/instancia-observatorio#parteInteressadaAgenciaDeFomento | Agência de fomento | https://example.org/ontompo/instancia-observatorio#noticiasEmRedesSociais | Publicação de notícias em redes sociais | Relacionamento | https://example.org/ontompo/instancia-observatorio#projetoExtensaoComunitaria | Projeto de extensão comunitária (cenário) |
| https://example.org/ontompo/instancia-observatorio#parteInteressadaComunidadeAtendida | Comunidade atendida | https://example.org/ontompo/instancia-observatorio#interacaoComProjetos | Interação dos usuários com os projetos | Relacionamento | https://example.org/ontompo/instancia-observatorio#projetoExtensaoComunitaria | Projeto de extensão comunitária (cenário) |
| https://example.org/ontompo/instancia-observatorio#parteInteressadaCoordenacaoDeProjeto | Coordenação de projeto observado | https://example.org/ontompo/instancia-observatorio#forunsDeDiscussao | Fóruns de discussão | Relacionamento | https://example.org/ontompo/instancia-observatorio#projetoExtensaoComunitaria | Projeto de extensão comunitária (cenário) |
| https://example.org/ontompo/instancia-observatorio#parteInteressadaCoordenacaoDeProjeto | Coordenação de projeto observado | https://example.org/ontompo/instancia-observatorio#interacaoComProjetos | Interação dos usuários com os projetos | Relacionamento | https://example.org/ontompo/instancia-observatorio#projetoExtensaoComunitaria | Projeto de extensão comunitária (cenário) |

_Resultado completo, cru, em `qc2-resultado.csv`._
