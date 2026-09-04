# 04: Correções estruturais (A1–A4, A8, A9)

**What to build:** a primeira rodada de revisão do modelo, cobrindo as deficiências que não exigem
adotar novas microteorias da UFO. Ao fim, o modelo revisado apresenta menos violações que o baseline,
e a diferença está medida, não afirmada.

Deficiências desta rodada:

- **A1** `CrudOperation` colapsa Create, Update e Delete, que têm pós-condições distintas — *construct overload*
- **A2** `Software` modelado como composição de `Hardware`, misturando o virtual e o físico — mereologia inválida
- **A3** `«MemberOf»` entre `ObservatoryGroup` e os papéis de agente com o losango do lado do «role», declarando o coletivo como *parte* do papel — a UFO prescreve o inverso
- **A4** classe de domínio nomeada `Relator`, colidindo com o metaconceito da própria UFO
- **A8** `Management` e `Operation` como relators de aridade não justificada
- **A9** `ProjectObservatory` especializa `Software` e é ao mesmo tempo especializado por `DataManager` e `View`

**Blocked by:** 03 (linha de base)

**Status:** resolved

- [x] CRUD decomposto em operações com pós-condições distintas
- [x] Relação entre `Software` e `Hardware` remodelada como execução ou hospedagem, com justificativa ontológica escrita
- [x] Losango das `«MemberOf»` na direção correta, com o coletivo como todo
- [x] Classe de domínio `Relator` renomeada para termo que não colida com o vocabulário da UFO
- [x] Aridade de `Management` e `Operation` resolvida: decomposta em binárias ou justificada como n-ária por escrito
- [x] Hierarquia do `ProjectObservatory` revista de modo que o princípio de identidade seja coerente
- [x] Plugin OntoUML re-executado; relatório salvo e comparável ao baseline
- [x] Cada correção tem registrado o par antes/depois que a seção de análise vai usar

## Comments

Rodada entregue em `ontologia/rodada-1/`: o modelo revisado em
`ontompo-rodada-1.ontouml.json`, a OWL em `.ttl`, o relatório do plugin, o relatório do verificador
complementar, o controle e o diff estrutural. A leitura de tudo isso, com o par antes/depois e a
justificativa ontológica de cada correção, está em `ontologia/correcoes-rodada-1.md`. O ferramental
novo é `scripts/ontouml/modelo-rodada-1.js`, `gerar-rodada-1.js`, `verificador-ufo-extra.js` e
`diff-modelos.js`, mais `scripts/verificar_rodada1.py` para a conferência da checklist.

**O que foi feito em cada correção.** A1: `CrudOperation` continua provendo identidade e ganha uma
partição disjunta e completa em `Create`, `Read`, `Update` e `Delete` — e a decomposição torna
visível que `Read`, ao contrário das outras três, não tem pós-condição sobre o dado. A2: a
«componentOf» de `Hardware` para `Software` sai e entra o relator `SoftwareExecution`, com a material
derivada dele; o mínimo 1 muda de lado, de modo que software não se manifesta sem hardware mas
hardware pode não executar nada — o `1..*` do baseline expulsava do domínio o switch e o nobreak.
A3: o losango vai para o lado do coletivo nas três «memberOf», e o mínimo do lado do membro sobe de
0 para 1; isso fecha B2 de passagem, porque a terceira relação passa a declarar todo e parte. A4:
`Relator` vira `Reporter`. A8: `Management` e `Operation` viram quatro relatores binários, e a ponta
`Network` de `Operation` não gerou relator novo porque `Connection` já reificava aquele fato — a
quaternária era em parte redundante com um relator do próprio modelo, achado que só apareceu ao
decompor. A9: `DataManager` e `View` passam a ser papéis de `Software` e componentes do observatório
por «componentOf».

**O antes/depois precisou de um instrumento novo, e a razão é o resultado do ticket 03.** O
verificador do plugin devolve zero sobre o baseline e continua devolvendo zero sobre o revisado:
nenhuma das seis deficiências está ao alcance das suas 24 regras. Zero contra zero não mede revisão
nenhuma. `verificador-ufo-extra.js` acrescenta cinco regras estruturais — todo de «memberOf» que não
é coletivo, meronímica sem todo nem parte, mediação com mínimo zero na ponta mediada, nome de classe
colidindo com metaconceito da UFO, e relator n-ário —, e a diferença medida é **10 no baseline
contra 1 na rodada 1**. As cinco disparam sobre o baseline, e a execução reprova se alguma deixar de
disparar, pela mesma razão que o controle de mutação do ticket 03 existe: regra que nunca dispara
não mede nada.

O que o zero do plugin garante, e vale dizer no artigo, é outra coisa: nenhuma das seis correções
introduziu violação das regras que ele de fato tem — provedor de identidade, rigidez, natureza na
partição nova. O controle em `rodada-1/controle-verificacao.md` mostra que ele acusaria.

**Três das seis não viram regra, e isso é deliberado.** A1, A2 e A9 são defeitos de significado, não
de forma. Codificar "software não é feito de hardware" como regra seria escrever a resposta no
gabarito. Continuam sustentadas por argumento ontológico explícito. A seção de análise precisa
apresentar o número como o que ele é — cinco restrições estruturais da UFO, medidas antes e depois —
e não como veredito de correção ontológica em geral.

**Um achado novo, e ele veio do instrumento.** `Observation` medeia três relata — `Knowledge`,
`Agent` e `Disseminator` — e é o relator n-ário que sobrou. A8 nomeia `Management` e `Operation`;
`Observation` passou despercebido nas duas leituras manuais. Fica registrado como **B8** e não é
corrigido aqui, porque uma observação é candidata natural a evento e a decomposição correta depende
de UFO-B: vai junto com A5, no ticket 05. Que a ferramenta tenha encontrado o que a inspeção manual
não encontrou é material para o artigo — sustenta a tese de que deficiências representacionais
permanecem latentes.

**OOPS! não foi reexecutado.** O antes/depois de *pitfalls* de OWL é do ticket 06, junto com a
customização; rodá-lo agora, sobre uma OWL que ainda vai mudar em 05 e 06, produziria um número que
o próprio ticket 06 invalidaria.

**Conferência.** `scripts/verificar_rodada1.py` reprova quando o modelo diverge do que o ticket
pediu, quando qualquer uma das seis correções é desfeita, quando o baseline é corrigido de passagem,
quando as correções de A1 a A4 e A9 não sobrevivem à transformação gUFO, quando alguma regra do
verificador complementar deixa de disparar sobre o baseline, quando a rodada não mede melhora,
quando uma correção fica sem par antes/depois ou sem justificativa, e quando o achado que sobra fica
sem endereço. As treze verificações foram exercitadas contra cópias deliberadamente quebradas antes
de a checagem ser considerada pronta.

**O enunciado de A3 neste ticket foi corrigido.** A descrição herdada do *spec* — «CompOf» ligando
`ObservatoryUser` a `ObservatoryGroup` — é falsa: o ticket 03 verificou nos diagramas em resolução de
origem que o estereótipo sempre foi «MemberOf», e que o defeito é a direção do losango. O bullet e o
item da checklist acima foram reescritos para o que foi de fato corrigido; a descrição errada
sobrevive no `spec.md`, e o ticket 10 precisa corrigi-la lá antes de escrever a seção de análise.

**Refatoração de passagem.** A geração de artefatos saiu de `gerar-baseline.js` para `gerar.js`,
compartilhado, para que baseline e rodadas passem pelo mesmo caminho de código — se a geração mudar,
muda para os dois, e os relatórios continuam comparáveis. `controle-verificacao.js` ganhou
`--modelo=`. Os artefatos do baseline saem byte a byte idênticos aos commitados, exceto duas linhas
de texto que agora apontam para a rodada 1.
