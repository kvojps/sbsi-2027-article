# QC5 — Que motivações levam cada tipo de ator a interagir com o observatório?

Cenário: observatório de projetos de pesquisa e extensão de uma universidade pública brasileira, descrito nos Anais Estendidos do XVIII SBSI (2022), DOI 10.5753/sbsi_estendido.2022.222995. A publicação-fonte é referida em terceira pessoa pelo seu DOI. A pergunta é de domínio e pressupõe "tipos de ator", que o modelo publicado não tinha: a análise (A6) reorganizou a camada de agentes, com ObservatoryUser como papel de Person e StakeHolder como roleMixin. A consulta agrupa por esse tipo — lido do rótulo preferido que a classe tem na OntoMPO — as motivações registradas em cada relator SocialInteraction. Sem a hierarquia de Agent da análise ou sem as interações instanciadas, não devolve linha nenhuma.

Executada por `tools/generation/rodar_consultas.py` sobre a ontologia revisada (`artifacts/ontology/owl/ontompo.ttl`), a gUFO (`sources/gufo/gufo.ttl`) e os dados de instância dos observatórios (`artifacts/ontology/instancias/observatorio.ttl` e `observatorio-b.ttl`). As QC1–QC6 se prendem ao namespace do observatório principal; só a QC7 atravessa os dois.

## Consulta SPARQL

```sparql
# QC5 — Que motivações levam cada tipo de ator a interagir com o observatório?
# Cenário: observatório de projetos de pesquisa e extensão de uma universidade
# pública brasileira, descrito nos Anais Estendidos do XVIII SBSI (2022),
# DOI 10.5753/sbsi_estendido.2022.222995. A publicação-fonte é referida em
# terceira pessoa pelo seu DOI.
#
# A pergunta é de domínio e pressupõe "tipos de ator", que o modelo publicado
# não tinha: a análise (A6) reorganizou a camada de agentes, com ObservatoryUser
# como papel de Person e StakeHolder como roleMixin. A consulta agrupa por esse
# tipo — lido do rótulo preferido que a classe tem na OntoMPO — as motivações
# registradas em cada relator SocialInteraction. Sem a hierarquia de Agent da
# análise ou sem as interações instanciadas, não devolve linha nenhuma.
PREFIX ontompo: <https://example.org/ontompo/rodada-2#>
PREFIX obs: <https://example.org/ontompo/instancia-observatorio#>
PREFIX dct: <http://purl.org/dc/terms/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?tipoAtor ?rotuloTipo ?ator ?rotuloAtor ?motivacao
WHERE {
  ?interacao a ontompo:SocialInteraction ;
             ontompo:mediation_SocialInteraction_Agent ?ator ;
             dct:description ?motivacao .
  ?ator a ?tipoAtor ;
        skos:prefLabel ?rotuloAtor .
  ?tipoAtor rdfs:subClassOf* ontompo:Agent ;
            skos:prefLabel ?rotuloTipo .
  FILTER (STRSTARTS(STR(?ator), "https://example.org/ontompo/instancia-observatorio#"))
  FILTER (langMatches(lang(?rotuloTipo), "pt"))
  FILTER (langMatches(lang(?rotuloAtor), "pt"))
  FILTER (langMatches(lang(?motivacao), "pt"))
}
ORDER BY ?rotuloTipo ?rotuloAtor ?motivacao ?tipoAtor ?ator
```

## Resultado — 7 linha(s)

| tipoAtor | rotuloTipo | ator | rotuloAtor | motivacao |
|---|---|---|---|---|
| https://example.org/ontompo/rodada-2#StakeHolder | Parte interessada | https://example.org/ontompo/instancia-observatorio#parteInteressadaAgenciaDeFomento | Agência de fomento | Acompanhar a divulgação pública dos projetos apoiados. |
| https://example.org/ontompo/rodada-2#StakeHolder | Parte interessada | https://example.org/ontompo/instancia-observatorio#parteInteressadaComunidadeAtendida | Comunidade atendida | Relatar necessidades e dar retorno sobre os projetos de extensão. |
| https://example.org/ontompo/rodada-2#StakeHolder | Parte interessada | https://example.org/ontompo/instancia-observatorio#parteInteressadaCoordenacaoDeProjeto | Coordenação de projeto observado | Acompanhar comentários, reações e relatos de erro sobre o projeto coordenado. |
| https://example.org/ontompo/rodada-2#StakeHolder | Parte interessada | https://example.org/ontompo/instancia-observatorio#parteInteressadaCoordenacaoDeProjeto | Coordenação de projeto observado | Discutir a temática do projeto coordenado em fóruns. |
| https://example.org/ontompo/rodada-2#ObservatoryUser | Usuário do observatório | https://example.org/ontompo/instancia-observatorio#usuarioDaSociedade | Usuário da sociedade | Acompanhar projetos de extensão que beneficiam a comunidade. |
| https://example.org/ontompo/rodada-2#ObservatoryUser | Usuário do observatório | https://example.org/ontompo/instancia-observatorio#usuarioDocente | Usuário docente | Divulgar os projetos de pesquisa sob coordenação docente. |
| https://example.org/ontompo/rodada-2#ObservatoryUser | Usuário do observatório | https://example.org/ontompo/instancia-observatorio#usuarioEstudante | Usuário estudante | Trocar informação sobre projetos de interesse acadêmico. |

_Resultado completo, cru, em `qc5-resultado.csv`._
