# Verificador de microteorias: *as-is*, rodada 1 e rodada 2

As regras abaixo operacionalizam restricoes da UFO que as 24 do plugin OntoUML nao cobrem. As cinco da rodada 1 (ticket 04) e as quatro da rodada 2 (ticket 05) sao aplicadas aos tres modelos pelo mesmo caminho de codigo. Saida bruta em `relatorio-verificador-ufo-b-c.json`; o codigo das regras esta em `tools/verification/verificador-ufo-extra.js` e `tools/verification/verificador-ufo-b-c.js`.

## Diferenca medida

| Regra | Tipo | Severidade | *as-is* | rodada 1 | rodada 2 |
|---|---|---|---|---|---|
| `memberof_whole_not_collective` | medicao | error | 2 | 0 | 0 |
| `parthood_ends_undeclared` | medicao | error | 1 | 0 | 0 |
| `mediation_optional_relatum` | medicao | error | 3 | 0 | 0 |
| `class_name_collides_with_metaconcept` | medicao | error | 1 | 0 | 0 |
| `relator_arity_above_binary` | medicao | warning | 3 | 1 | 0 |
| `modelo_sem_perdurante` | medicao | error | 1 | 1 | 0 |
| `modelo_sem_relacao_temporal` | medicao | error | 1 | 1 | 0 |
| `evento_sem_participante` | guarda | error | 0 | 0 | 0 |
| `participacao_invertida` | guarda | error | 0 | 0 | 0 |
| **total** | | | **12** | **3** | **0** |

O verificador do plugin OntoUML devolve zero sobre os tres modelos. E por isso que este segundo instrumento existe, e por isso que ele cresce junto com as rodadas: uma rodada que zerasse as suas regras reintroduzindo as da anterior apareceria aqui.

## As regras da rodada 2

### `modelo_sem_perdurante` — o modelo nao declara nenhum perdurante

*Regra de medicao.* A UFO parte da divisao entre endurantes, que estao inteiramente presentes a cada instante em que existem, e perdurantes, que se desdobram no tempo e tem partes temporais. Um modelo sem nenhuma classe de natureza evento ou situacao nao representa mudanca: nao tem onde dizer o que aconteceu, quando, nem em que ordem. A regra nao afirma que este ou aquele conceito deveria ser evento — isso e julgamento de dominio, e esta no argumento de A5. Ela registra que a metade perdurante do vocabulario esta inteira ausente, que e o *construct deficit* na sua forma verificavel.

### `modelo_sem_relacao_temporal` — o modelo nao declara nenhuma relacao da UFO-B

*Regra de medicao.* Declarar eventos e metade da adocao; a outra e liga-los ao mundo. Sem «participation», «participational», «creation», «termination», «historicalDependence», «bringsAbout» ou «triggers», nada no modelo diz quem participou de que, o que passou a existir e o que deixou de existir. E uma regra independente da anterior: um modelo pode ter eventos e nao liga-los a nada, e e exatamente esse o caso que a adocao de fachada produz.

### `evento_sem_participante` — tipo de evento sem nenhum participante declarado

*Regra de guarda.* Um evento em UFO-B existe pela participacao dos endurantes que o compoem: nao ha evento sem participante. Um tipo de evento que nao esta na ponta de nenhuma «participation», «participational», «creation» ou «termination» — nem por heranca de um tipo mais geral — e um evento de que nada participa, o que e uma troca de estereotipo sem adocao de microteoria.

### `participacao_invertida` — participacao com o evento na ponta do participante

*Regra de guarda.* A «participation» vai do endurante que participa para o evento de que ele participa, e a transformacao gUFO a escreve como `gufo:participatedIn` com aquele dominio e aquele alcance. Invertida, a OWL afirma que o evento participa do endurante — uma assercao que nenhum raciocinador recusa e que nenhum leitor entende. Vale o mesmo para a «creation», que vai do criado para o evento que o criou.

As cinco da rodada 1 estao documentadas em `../rodada-1/relatorio-verificador-extra.md`.

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
| 11 | error | `modelo_sem_perdurante` | `OntoMPO` | nenhuma das 32 classes tem natureza evento ou situacao: a UFO-B nao foi adotada |
| 12 | error | `modelo_sem_relacao_temporal` | `OntoMPO` | nenhuma das 28 relacoes tem estereotipo da UFO-B: nao ha participacao, criacao nem terminacao no modelo |

## Achados no modelo rodada-1

| # | Severidade | Codigo | Elemento | Descricao |
|---|---|---|---|---|
| 1 | warning | `relator_arity_above_binary` | `Observation` | medeia 3 relata: Knowledge, Agent, Disseminator |
| 2 | error | `modelo_sem_perdurante` | `OntoMPO` | nenhuma das 38 classes tem natureza evento ou situacao: a UFO-B nao foi adotada |
| 3 | error | `modelo_sem_relacao_temporal` | `OntoMPO` | nenhuma das 32 relacoes tem estereotipo da UFO-B: nao ha participacao, criacao nem terminacao no modelo |

## Achados no modelo rodada-2

Nenhum problema encontrado.

## Controle

Uma regra que nunca dispara nao mede nada. As regras de medicao tem como controle positivo o proprio *as-is*, sobre o qual as sete disparam, e a execucao reprova se alguma deixar de disparar. As regras de guarda nao podem ter esse controle — sobre um modelo sem UFO-B elas nao tem o que verificar —, entao o controle delas e uma mutacao do modelo da rodada 2, aplicada pelo mesmo caminho de codigo, como em `controle-verificacao.md`.

| Mutacao | Codigo esperado | Por que deveria falhar | Acusada |
|---|---|---|---|
| Observation perde as tres relacoes que a ligam a seus participantes | `evento_sem_participante` | um tipo de evento de que nada participa nao e um evento adotado, e um rotulo | sim |
| a participacao de Collector em Extract tem as pontas trocadas | `participacao_invertida` | invertida, a gUFO passa a afirmar que a extracao participa do coletor | sim |

Reproduzir com `node tools/verification/verificador-ufo-b-c.js`.
