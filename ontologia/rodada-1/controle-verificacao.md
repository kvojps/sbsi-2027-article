# Controle do verificador OntoUML

O relatorio do plugin sobre o modelo revisado (rodada 1) nao acusa nenhum problema. Este controle existe para que esse zero seja lido como resultado, e nao como falha de execucao: as mutacoes abaixo sao aplicadas ao mesmo modelo, pelo mesmo caminho de codigo, e cada uma precisa ser acusada com o codigo esperado.

Modelo sem mutacao: 0 problema(s).

| Mutacao | Codigo esperado | Por que deveria falhar | Acusada |
|---|---|---|---|
| System perde a generalizacao para Agent | `class_missing_identity_provider` | um sortal sem sortal ultimo acima dele fica sem principio de identidade | sim |
| Hardware passa a especializar DataManager | `generalization_incompatible_class_rigidity` | um tipo rigido nao pode especializar um tipo antirrigido | sim |
| ProjectObservatory passa a especializar tambem Project | `class_multiple_identity_providers` | duas ancestralidades ate sortais ultimos distintos dao dois principios de identidade | sim |

Reproduzir com `node scripts/ontouml/controle-verificacao.js --modelo=rodada-1`.
