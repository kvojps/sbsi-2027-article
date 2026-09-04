# Verificador complementar: *as-is* contra rodada 1

As cinco regras abaixo operacionalizam restricoes da UFO que as 24 do plugin OntoUML nao cobrem. Sao aplicadas ao mesmo modelo, pelo mesmo caminho de codigo, antes e depois da primeira rodada de revisao. Saida bruta em `relatorio-verificador-extra.json`; o codigo das regras esta em `tools/verification/verificador-ufo-extra.js`.

## Diferenca medida

| Regra | Severidade | *as-is* | rodada 1 |
|---|---|---|---|
| `memberof_whole_not_collective` | error | 2 | 0 |
| `parthood_ends_undeclared` | error | 1 | 0 |
| `mediation_optional_relatum` | error | 3 | 0 |
| `class_name_collides_with_metaconcept` | error | 1 | 0 |
| `relator_arity_above_binary` | warning | 3 | 1 |
| **total** | | **10** | **1** |

Para comparacao, o verificador do plugin OntoUML devolve zero problemas sobre os dois modelos: as deficiencias desta rodada estao todas fora do alcance das 24 regras dele. E por isso que este segundo instrumento existe.

## As regras

### `memberof_whole_not_collective` — o todo de uma «memberOf» tem de ser um coletivo

Em UFO, «memberOf» e a parthood entre um coletivo e seus membros: o todo e uma colecao e a parte e membro dela. Um todo que nao e coletivo torna a relacao ininterpretavel e, na gUFO, produz uma assercao `isCollectionMemberOf` invertida.

### `parthood_ends_undeclared` — relacao meronimica sem todo nem parte declarados

Uma relacao de parthood so significa alguma coisa depois de dito qual ponta e o todo. Sem extremidade de agregacao em nenhuma das duas, a relacao carrega o estereotipo mereologico sem exercer nenhuma restricao mereologica.

### `mediation_optional_relatum` — mediacao com minimo zero na ponta mediada

Uma «mediation» e dependencia existencial: o relator nao existe sem o mediado. Minimo zero na ponta mediada admite um relator que nao conecta aquele relatum, isto e, um relator que pode nao reificar relacao nenhuma.

### `class_name_collides_with_metaconcept` — classe de dominio com nome de metaconceito da UFO

O nome de uma classe de dominio e o de uma categoria de fundamentacao passam a designar coisas diferentes no mesmo documento. Na OWL a colisao fica literal: `gufo:Relator` e `ontompo:Relator` convivem no mesmo grafo.

### `relator_arity_above_binary` — relator n-ario sem fato relacional nomeado

A aridade de um relator decorre do fato relacional que ele reifica. Um relator que medeia mais de dois relata pode estar reificando um fato genuinamente n-ario ou varios fatos binarios colapsados num construto so — e o modelo, sozinho, nao distingue os dois casos. Severidade *warning*: o achado e um pedido de justificativa, nao um veredito.

## Achados no modelo *as-is*

| # | Severidade | Codigo | Elemento | Descricao |
|---|---|---|---|---|
| 1 | error | `memberof_whole_not_collective` | `memberOf_ObservatoryGroup_ObservatoryUser` | o todo declarado e `ObservatoryUser`, de natureza functional-complex, e nao um coletivo |
| 2 | error | `memberof_whole_not_collective` | `memberOf_ObservatoryGroup_StakeHolder` | o todo declarado e `StakeHolder`, de natureza functional-complex, e nao um coletivo |
| 3 | error | `parthood_ends_undeclared` | `memberOf_ObservatoryGroup_System` | «memberOf» sem losango em nenhuma das duas pontas |
| 4 | error | `mediation_optional_relatum` | `mediation_Operation_Software` | Operation medeia Software com `0..*` na ponta mediada |
| 5 | error | `mediation_optional_relatum` | `mediation_Operation_Hardware` | Operation medeia Hardware com `0..*` na ponta mediada |
| 6 | error | `mediation_optional_relatum` | `mediation_Operation_Network` | Operation medeia Network com `0..*` na ponta mediada |
| 7 | error | `class_name_collides_with_metaconcept` | `Relator` | «role» de dominio homonima do metaconceito da UFO |
| 8 | warning | `relator_arity_above_binary` | `Observation` | medeia 3 relata: Knowledge, Agent, Disseminator |
| 9 | warning | `relator_arity_above_binary` | `Management` | medeia 3 relata: Project, DataManager, View |
| 10 | warning | `relator_arity_above_binary` | `Operation` | medeia 4 relata: Software, Service, Hardware, Network |

## Achados no modelo da rodada 1

| # | Severidade | Codigo | Elemento | Descricao |
|---|---|---|---|---|
| 1 | warning | `relator_arity_above_binary` | `Observation` | medeia 3 relata: Knowledge, Agent, Disseminator |

## Controle

Uma regra que nunca dispara nao mede nada. As cinco disparam sobre o modelo *as-is*, e a execucao reprova se alguma delas deixar de disparar — o zero da rodada 1 e resultado, e nao ausencia de instrumento.
