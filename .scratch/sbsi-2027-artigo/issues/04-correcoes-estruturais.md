# 04: Correções estruturais (A1–A4, A8, A9)

**What to build:** a primeira rodada de revisão do modelo, cobrindo as deficiências que não exigem
adotar novas microteorias da UFO. Ao fim, o modelo revisado apresenta menos violações que o baseline,
e a diferença está medida, não afirmada.

Deficiências desta rodada:

- **A1** `CrudOperation` colapsa Create, Update e Delete, que têm pós-condições distintas — *construct overload*
- **A2** `Software` modelado como composição de `Hardware`, misturando o virtual e o físico — mereologia inválida
- **A3** `«CompOf»` ligando `ObservatoryUser` a `ObservatoryGroup`, que é «Collective» — a UFO prescreve `«MemberOf»`
- **A4** classe de domínio nomeada `Relator`, colidindo com o metaconceito da própria UFO
- **A8** `Management` e `Operation` como relators de aridade não justificada
- **A9** `ProjectObservatory` especializa `Software` e é ao mesmo tempo especializado por `DataManager` e `View`

**Blocked by:** 03 (linha de base)

**Status:** ready-for-agent

- [ ] CRUD decomposto em operações com pós-condições distintas
- [ ] Relação entre `Software` e `Hardware` remodelada como execução ou hospedagem, com justificativa ontológica escrita
- [ ] `«MemberOf»` no lugar de `«CompOf»`, com o losango na direção correta
- [ ] Classe de domínio `Relator` renomeada para termo que não colida com o vocabulário da UFO
- [ ] Aridade de `Management` e `Operation` resolvida: decomposta em binárias ou justificada como n-ária por escrito
- [ ] Hierarquia do `ProjectObservatory` revista de modo que o princípio de identidade seja coerente
- [ ] Plugin OntoUML re-executado; relatório salvo e comparável ao baseline
- [ ] Cada correção tem registrado o par antes/depois que a seção de análise vai usar
