# QC1 — Quais Views são disponibilizadas por um dado DataManager?

Cenário: observatório de projetos de pesquisa e extensão de uma universidade pública brasileira, descrito nos Anais Estendidos do XVIII SBSI (2022), DOI 10.5753/sbsi_estendido.2022.222995. Trabalho anterior do próprio autor, referido em terceira pessoa. Alvo: o gerenciamento de conteúdo do observatório (obs:gerenciadorDeConteudo). A pergunta é de domínio: percorre o relator ViewProvision, que a análise ontológica introduziu na correção de A9 (composição no lugar de especialização), e devolve as visões do observatório agrupadas pelo papel que cada uma exerce. Uma ontologia sem ViewProvision/DataManager/View, ou sem os dados do observatório, não devolve linha nenhuma.

Executada por `tools/generation/rodar_consultas.py` sobre a ontologia revisada (`artifacts/ontology/owl/ontompo.ttl`), a gUFO (`sources/gufo/gufo.ttl`) e os dados de instância do observatório (`artifacts/ontology/instancias/observatorio.ttl`).

## Consulta SPARQL

```sparql
# QC1 — Quais Views são disponibilizadas por um dado DataManager?
# Cenário: observatório de projetos de pesquisa e extensão de uma universidade
# pública brasileira, descrito nos Anais Estendidos do XVIII SBSI (2022),
# DOI 10.5753/sbsi_estendido.2022.222995. Trabalho anterior do próprio autor,
# referido em terceira pessoa.
# Alvo: o gerenciamento de conteúdo do observatório (obs:gerenciadorDeConteudo).
#
# A pergunta é de domínio: percorre o relator ViewProvision, que a análise
# ontológica introduziu na correção de A9 (composição no lugar de especialização),
# e devolve as visões do observatório agrupadas pelo papel que cada uma exerce.
# Uma ontologia sem ViewProvision/DataManager/View, ou sem os dados do
# observatório, não devolve linha nenhuma.
PREFIX ontompo: <https://example.org/ontompo/rodada-2#>
PREFIX obs: <https://example.org/ontompo/instancia-observatorio#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?view ?rotuloView ?papel ?rotuloPapel
WHERE {
  ?provisao a ontompo:ViewProvision ;
            ontompo:mediation_ViewProvision_DataManager obs:gerenciadorDeConteudo ;
            ontompo:mediation_ViewProvision_View ?view .
  ?view a ?papel ;
        skos:prefLabel ?rotuloView .
  ?papel rdfs:subClassOf ontompo:View ;
         skos:prefLabel ?rotuloPapel .
  FILTER (langMatches(lang(?rotuloView), "pt"))
  FILTER (langMatches(lang(?rotuloPapel), "pt"))
}
ORDER BY ?rotuloPapel ?rotuloView
```

## Resultado — 8 linha(s)

| view | rotuloView | papel | rotuloPapel |
|---|---|---|---|
| https://example.org/ontompo/instancia-observatorio#analisesDetalhadas | Análises detalhadas dos projetos | https://example.org/ontompo/rodada-2#Disseminator | Disseminação |
| https://example.org/ontompo/instancia-observatorio#downloadDeDadosBrutos | Download de dados brutos dos projetos | https://example.org/ontompo/rodada-2#Disseminator | Disseminação |
| https://example.org/ontompo/instancia-observatorio#forunsDeDiscussao | Fóruns de discussão | https://example.org/ontompo/rodada-2#Reporter | Relacionamento |
| https://example.org/ontompo/instancia-observatorio#interacaoComProjetos | Interação dos usuários com os projetos | https://example.org/ontompo/rodada-2#Reporter | Relacionamento |
| https://example.org/ontompo/instancia-observatorio#noticiasEmRedesSociais | Publicação de notícias em redes sociais | https://example.org/ontompo/rodada-2#Reporter | Relacionamento |
| https://example.org/ontompo/instancia-observatorio#cadastroDeMidia | Cadastro de mídia sobre os projetos | https://example.org/ontompo/rodada-2#CrudView | Visão CRUD |
| https://example.org/ontompo/instancia-observatorio#consultaDeDadosDosProjetos | Consulta de dados dos projetos | https://example.org/ontompo/rodada-2#CrudView | Visão CRUD |
| https://example.org/ontompo/instancia-observatorio#manutencaoDeProjetos | Manutenção de projetos | https://example.org/ontompo/rodada-2#CrudView | Visão CRUD |

_Resultado completo, cru, em `qc1-resultado.csv`._
