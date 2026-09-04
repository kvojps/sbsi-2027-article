# Correções da rodada 1 — A1, A2, A3, A4, A8, A9

Este documento fecha o ticket 04. Para cada uma das seis deficiências que não exigem adotar novas
microteorias da UFO, registra o par **antes/depois** que a seção de análise ontológica vai usar, a
**justificativa** que sustenta a correção e o que ela muda na OWL e nas questões de competência.

Os artefatos estão em `rodada-1/`:

| Arquivo | O que é |
|---|---|
| `ontompo-rodada-1.ontouml.json` | o modelo revisado, no OntoUML Schema |
| `ontompo-rodada-1.ttl` | a OWL da rodada, pela mesma transformação gUFO do baseline |
| `relatorio-plugin-ontouml.md` / `.json` | a verificação contra a UFO, pelo motor do plugin |
| `relatorio-verificador-extra.md` / `.json` | o verificador complementar, *as-is* contra rodada 1 |
| `controle-verificacao.md` | o controle que torna interpretável o relatório vazio do plugin |
| `diff-as-is-rodada-1.md` | o diff estrutural entre os dois modelos, derivado deles |

O baseline permanece intacto em `baseline/`. As duas metades convivem: é a comparação que dá
evidência, e uma correção aplicada de passagem ao *as-is* destruiria o termo de comparação.

## A diferença, medida

O ticket pede que o modelo revisado apresente menos violações que o baseline, **medidas**. Medir
exigiu enfrentar o resultado do ticket 03: o verificador do plugin OntoUML devolve zero sobre o
*as-is*, e continua devolvendo zero sobre o revisado. Zero contra zero não mede revisão nenhuma. As
24 regras do plugin tratam de estereótipo, provedor de identidade, natureza e generalização; as
deficiências desta rodada não estão ao alcance de nenhuma delas.

A saída foi um segundo instrumento: `scripts/ontouml/verificador-ufo-extra.js`, cinco regras que
operacionalizam restrições da UFO que o plugin não cobre. Cada uma é estrutural — computada do
modelo, sem julgamento de domínio — e cada uma dispara sobre o *as-is*, o que impede que o zero do
revisado seja lido como instrumento ausente.

| Regra | Severidade | *as-is* | rodada 1 |
|---|---|---|---|
| `memberof_whole_not_collective` | error | 2 | 0 |
| `parthood_ends_undeclared` | error | 1 | 0 |
| `mediation_optional_relatum` | error | 3 | 0 |
| `class_name_collides_with_metaconcept` | error | 1 | 0 |
| `relator_arity_above_binary` | warning | 3 | 1 |
| **total** | | **10** | **1** |

E o que o plugin diz, embora não meça a revisão, não é vazio: **zero antes, zero depois** significa
que nenhuma das seis correções introduziu violação das regras que ele de fato tem — nem provedor de
identidade perdido, nem rigidez violada, nem natureza incompatível na partição nova. O controle em
`rodada-1/controle-verificacao.md` mostra que ele acusaria, com três mutações conhecidas aplicadas
ao modelo revisado pelo mesmo caminho de código.

**O que este número não é.** Não é medida de correção ontológica em geral. Três das seis
deficiências desta rodada — A1, A2 e A9 — são defeitos de significado, não de forma: uma sobrecarga
de construto, uma mereologia inválida entre dois complexos funcionais e uma taxonomia que confunde
princípio de identidade não viram regra sem que a regra seja escrita já sabendo a resposta. Elas
continuam sustentadas por argumento, abaixo. O artigo precisa dizer isso; prometer "relatórios
automáticos melhorados" sem essa ressalva é convite a parecer.

---

## A1 — `CrudOperation` decomposta

**Classificação BWW.** *Construct overload*.

**Antes.** Uma única classe «relator» `CrudOperation`, com duas mediações — `Agent` (1) e `CrudView`
(1) — e nada que discriminasse qual operação estava em jogo. Nenhuma subclasse, nenhuma partição,
nenhum atributo.

**Depois.** `CrudOperation` continua sendo o «relator» que provê o princípio de identidade, e passa a
ser particionada em quatro «subkind» de natureza relator:

```
CrudOperation «relator»
  ├── CreateOperation «subkind»
  ├── ReadOperation   «subkind»
  ├── UpdateOperation «subkind»
  └── DeleteOperation «subkind»
```

A partição `crudOperationType` é **disjunta e completa**: toda operação é exatamente uma das quatro,
e as quatro esgotam o construto que o nome do original anunciava. As duas mediações permanecem no
tipo geral, porque valem para as quatro: toda operação tem um agente e uma visão.

**Justificativa.** Um construto está sobrecarregado quando um mesmo construto gramatical representa
mais de um construto ontológico [wand1993ontological]. As três operações que alteram o dado têm
pós-condições mutuamente incompatíveis — `Create` faz existir o que não existia, `Update` altera
propriedades de um item que permanece o mesmo, `Delete` faz deixar de existir. A quarta é o caso
que a decomposição torna visível: `Read` **não tem pós-condição sobre o dado**, e essa diferença,
que é a mais grosseira das quatro, era a mais invisível no construto colapsado. Separá-las é o
mínimo que permite dizer, no modelo, o que aconteceu com o dado.

**Na OWL.** As quatro chegam como `owl:Class` sob `ontompo:CrudOperation`, e a partição vira
`owl:AllDisjointClasses` mais um `owl:unionOf` de completude — os primeiros axiomas de disjunção do
modelo, contra os zero do baseline (B4).

**Limite desta correção, e onde ele é resolvido.** Uma operação continua sendo modelada como
endurante. A leitura eventiva — cada operação como evento, com pré e pós-estado e participação
temporal — depende de UFO-B e é do ticket 05, que trata a mesma questão para o ETL em A5. O que
esta rodada entrega é a separação dos tipos; a temporalidade vem depois.

## A2 — a composição inválida vira execução

**Classificação BWW.** *Construct excess* / mereologia inválida.

**Antes.** `componentOf_Hardware_Software`, parte em `Hardware` (`1..*`), todo em `Software`
(`1..*`), losango do lado de `Software`. Na OWL, `rdfs:subPropertyOf gufo:isComponentOf` com domínio
`Hardware` e alcance `Software`.

**Depois.** A «componentOf» sai. Entra o relator `SoftwareExecution`, que reifica o fato de um
software estar sendo executado por um hardware, com duas mediações — `Software` (`1..*` do lado do
relator) e `Hardware` (`0..*`) — e a material `material_Software_Hardware` derivada dele, `Software`
(`0..*`) para `Hardware` (`1..*`).

**Justificativa.** Em UFO, «componentOf» é parthood entre complexos funcionais, e a parte contribui
para o princípio de identidade do todo [guizzardi2005ontological]. Software não é feito de hardware:
troque-se todo o hardware sob uma aplicação e a aplicação continua sendo a mesma aplicação; troquem-se
os componentes de um complexo funcional e não se tem mais o mesmo complexo. O que existe entre os
dois é dependência de manifestação — o hardware executa o software, o software precisa de hardware
para se manifestar, e nenhum dos dois é parte do outro.

Reificar essa dependência num relator, em vez de declará-la como material solta, é o que dá lugar
para as duas coisas que o modelo vai precisar dizer sobre ela: quando a execução começou, e sob que
condições. As duas são do ticket 05.

**As multiplicidades também eram o defeito, e a inversão é deliberada.** O `1..*` do baseline na
ponta de `Hardware` obrigava todo hardware a ser componente de pelo menos um software, o que
expulsava do domínio o switch, o nobreak e o disco de backup. Agora o mínimo 1 está do lado do
**software** — que de fato não se manifesta sem hardware — e o hardware pode não executar nada.

**Na OWL.** `ontompo:componentOf_Hardware_Software` desaparece; entram
`ontompo:mediation_SoftwareExecution_Software`, `ontompo:mediation_SoftwareExecution_Hardware` e
`ontompo:material_Software_Hardware`, esta com `gufo:isDerivedFrom ontompo:SoftwareExecution`.
Nenhuma asserção `gufo:isComponentOf` entre software e hardware sobrevive.

## A3 — o losango do lado do coletivo

**Classificação BWW.** Violação de restrição da UFO.

**Nota sobre o enunciado do *spec*.** O *spec* descreve A3 como «CompOf» ligando `ObservatoryUser` a
`ObservatoryGroup`. Nos diagramas publicados, lidos em resolução de origem, o estereótipo é
**«MemberOf»** nas três relações; o defeito é a **direção**. A descrição correta está em
`evidencias-A1-A9.md` e precisa ser a usada no artigo — a do *spec* é falsificável por qualquer
revisor que abra a dissertação.

**Antes.** Três «memberOf» com `ObservatoryGroup` («collective») como **parte** declarada e um
«role» como **todo**:

| Relação | Todo declarado | Multiplicidades |
|---|---|---|
| `memberOf_ObservatoryGroup_ObservatoryUser` | `ObservatoryUser` («role») | grupo 1, papel 0..* |
| `memberOf_ObservatoryGroup_StakeHolder` | `StakeHolder` («role») | grupo 1, papel 0..* |
| `memberOf_ObservatoryGroup_System` | **nenhum** | grupo 1, papel 0..* |

**Depois.** Três «memberOf» com `ObservatoryGroup` como **todo**, losango do lado do coletivo nas
três, e o mínimo do lado do membro elevado de 0 para 1:

| Relação | Todo | Multiplicidades |
|---|---|---|
| `memberOf_ObservatoryUser_ObservatoryGroup` | `ObservatoryGroup` | membro 1..*, grupo 1 |
| `memberOf_StakeHolder_ObservatoryGroup` | `ObservatoryGroup` | membro 1..*, grupo 1 |
| `memberOf_System_ObservatoryGroup` | `ObservatoryGroup` | membro 1..*, grupo 1 |

**Justificativa.** «memberOf» exige que o todo seja um coletivo e que as partes sejam seus membros
[guizzardi2005ontological]. O baseline declarava o inverso, e a inversão sobrevivia à transformação:
`gufo:isCollectionMemberOf` ia de `ObservatoryGroup` para `ObservatoryUser`, isto é, o modelo
afirmava que **o grupo do observatório é membro do usuário**. Somada à asserção de que
`ObservatoryUser` é `gufo:Role` sobre complexo funcional, a mesma classe seria coleção e complexo
funcional.

O mínimo 1 do lado do membro corrige o resto: uma coleção sem membro nenhum não é uma coleção. O `1`
do lado do grupo é o que os diagramas trazem e foi preservado.

**Isso também fecha B2.** A terceira relação, com `System`, carregava o estereótipo de agregação sem
losango em nenhuma das duas pontas — parthood sem parthood declarada, indeterminada em vez de
errada. Agora declara, como as irmãs.

**Na OWL.** `gufo:isCollectionMemberOf` agora vai de `ObservatoryUser`, `StakeHolder` e `System`
para `ObservatoryGroup`. É a asserção invertida do baseline, endireitada, e é verificável linha a
linha entre os dois `.ttl`.

## A4 — `Relator` vira `Reporter`

**Classificação BWW.** *Construct redundancy* terminológica.

**Antes.** Uma classe «role» de nome `Relator`, especializando `View` e mediada por
`SocialInteraction` e `Log`. Na OWL, `ontompo:Relator` (um `gufo:Role`) convivia com `gufo:Relator`,
o metaconceito.

**Depois.** A mesma classe, com o mesmo lugar na taxonomia e as mesmas duas mediações, sob o nome
`Reporter`.

**Justificativa.** Numa linguagem cujo metamodelo define «relator» como categoria de fundamentação,
uma classe de domínio homônima faz dois significados incompatíveis ocuparem o mesmo termo: para a
UFO, um relator é um endurante que depende existencialmente de várias entidades; para o MPO,
`Relator` é quem relata. Desambiguar exigia o contexto tipográfico — a caixa amarela «role», não a
laranja «relator» —, o que é precisamente o tipo de dependência que a formalização deveria eliminar
[wand1993ontological].

`Reporter` é a tradução direta do termo do domínio e mantém o paralelo com o irmão `Disseminator`,
de modo que a correção não custa nada à leitura do modelo original. O nome do conceito no glossário
do Apêndice A não muda; muda o identificador.

**Na OWL.** `ontompo:Relator` desaparece do grafo. O único `Relator` restante é `gufo:Relator`, e a
listagem do OOPS! que imprimia os dois IRIs lado a lado deixa de ter dois.

## A8 — aridade resolvida por decomposição

**Classificação BWW.** Ambiguidade de aridade.

**Antes.** `Management` mediava três relata — `Project` (1), `DataManager` (1), `View` (1) — e
`Operation` mediava quatro — `Software` (0..*), `Service` (1), `Hardware` (0..*), `Network` (0..*).
Nem o diagrama nem o Apêndice A dizem que fato relacional único cada um reifica.

**Depois.** Ambos decompostos em relatores binários, cada um reificando um fato nomeável:

| Antes | Depois | Fato reificado |
|---|---|---|
| `Management` (Project, DataManager, View) | `ProjectDataManagement` (DataManager, Project) | um gerenciador de dados gerencia os dados de um projeto |
| | `ViewProvision` (DataManager, View) | um gerenciador de dados disponibiliza uma visão |
| `Operation` (Software, Service, Hardware, Network) | `SoftwareExecution` (Software, Hardware) | um hardware executa um software |
| | `ServiceProvision` (Service, Software) | um software provê um serviço |
| | `Connection`, que já existia | um hardware está conectado a uma rede |

**Justificativa.** Um relator reifica um fato relacional, e sua aridade deveria decorrer do fato
reificado [guizzardi2005ontological]. Nenhum dos dois sobrevivia ao teste.

`Operation` falhava do modo mais duro: **três das suas quatro mediações tinham mínimo zero na ponta
mediada**, de modo que o modelo admitia uma `Operation` mediando um `Service` e mais nada — um
relator que pode não reificar relação alguma, o que contradiz a dependência existencial que define a
mediação. Era o achado B1 do ticket 03, e a decomposição o elimina: as quatro mediações novas têm
mínimo 1 na ponta mediada.

`Management` não tinha o problema de cardinalidade — as três pontas eram 1 — mas reificava um fato
que o material de origem não nomeia. Um relator ligando um projeto, um gerenciador de dados e uma
visão pode ser três coisas diferentes. A decomposição escolhe entre elas com apoio no próprio
*spec*: a QC1 pergunta *quais Views são disponibilizadas por um dado `DataManager`*, o que pressupõe
um fato binário entre gerenciador e visão — que é `ViewProvision`. O outro fato, entre gerenciador e
projeto, é `ProjectDataManagement`.

A quarta ponta de `Operation`, `Network`, não gerou relator novo: `Connection` já reificava
exatamente o fato "um hardware está conectado a uma rede". A quaternária, portanto, além de mal
justificada, era em parte **redundante** com um relator que o próprio modelo já tinha — achado que
só apareceu ao decompor, e que vale citar no artigo.

**Na OWL.** Saem nove `gufo:mediates` de `Management` e `Operation`; entram oito, todas com mínimo 1
na ponta mediada, e nenhum relator do modelo medeia mais que dois relata — com uma exceção
registrada abaixo.

## A9 — `DataManager` e `View` deixam de ser observatórios

**Classificação BWW.** Confusão de princípio de identidade.

**Antes.**

```
Software «kind»
  └── ProjectObservatory «subkind»
        ├── DataManager «role» ── CrudRepository, Collector, Processor, Storer
        └── View «role» ──────── Disseminator, Relator, CrudView
```

**Depois.**

```
Software «kind»
  ├── ProjectObservatory «subkind»
  ├── DataManager «role» ── CrudRepository, Collector, Processor, Storer
  └── View «role» ──────── Disseminator, Reporter, CrudView

DataManager (1..*) ──«componentOf»──> ProjectObservatory (1)
View        (1..*) ──«componentOf»──> ProjectObservatory (1)
```

**Justificativa.** A hierarquia do baseline afirmava que todo `DataManager` é um `ProjectObservatory`
e que todo `View` é um `ProjectObservatory`. Como `View` é especializado por `Disseminator`,
`Reporter` e `CrudView`, seguia que **cada visão é um observatório de projetos inteiro** — e a
consequência é verificável contra o próprio *spec*: a QC1 pergunta quais visões um dado gerenciador
disponibiliza, pergunta que pressupõe muitas visões por observatório, enquanto o modelo fazia de
cada visão um observatório. Nenhuma consulta sobre o modelo antigo devolve o que a QC pede.

O que `DataManager` e `View` são, no material de origem, é papel desempenhado por **componentes** do
observatório — a subcamada "Componentes" do MPO. A correção é trocar especialização por composição:
os dois passam a ser papéis de `Software`, que lhes dá o princípio de identidade, e a serem partes
do observatório por «componentOf», que é parthood legítima entre complexos funcionais. `1..*` do
lado da parte e `1` do lado do todo dizem que um observatório tem ao menos um gerenciador e ao menos
uma visão, e que cada um pertence a exatamente um observatório.

`ProjectObservatory` continua «subkind» de `Software`; nada nesta rodada exige mexer nisso, e a
questão de o observatório ser mais que software é sociotécnica, não mereológica.

**Na OWL.** Saem `DataManager rdfs:subClassOf ProjectObservatory` e a equivalente de `View`; entram
`componentOf_DataManager_ProjectObservatory` e `componentOf_View_ProjectObservatory`, ambas
`rdfs:subPropertyOf gufo:isComponentOf`, mais `DataManager rdfs:subClassOf Software` e `View
rdfs:subClassOf Software`.

---

## O que ficou em aberto

### B8 — `Observation` é o relator ternário que sobrou

O verificador complementar acusa, sobre o modelo revisado, uma única ocorrência:

```
[warning] relator_arity_above_binary  Observation  medeia 3 relata: Knowledge, Agent, Disseminator
```

É achado do instrumento, não da inspeção manual: A8 nomeia `Management` e `Operation`, e
`Observation` passou despercebido nas duas leituras. Fica registrado como **B8**, e não é corrigido
aqui por dois motivos. Primeiro, está fora do enunciado desta rodada. Segundo, e mais importante,
uma observação é candidata natural a **evento**, não a relator: quem observa, o que passa a ser
conhecido e por onde é disseminado são participantes de um acontecimento, e a decomposição correta
depende de UFO-B. Endereçado ao ticket 05, junto com A5.

Que o instrumento tenha encontrado o que a análise manual não encontrou é, por si, material para o
artigo: sustenta a tese de que deficiências representacionais permanecem latentes.

### Deficiências das próximas rodadas

| # | Deficiência | Onde é resolvida |
|---|---|---|
| A5 | ETL como «relator» endurante em vez de evento | ticket 05 (UFO-B) |
| A6 | `Agent` como «kind» genérico, sem distinção físico/social | ticket 05 (UFO-C) |
| A7 | `System` como «role» sem kind subjacente explícito | ticket 05 (UFO-C) |
| B3 | 63 elementos sem definição, contra 53 termos definidos no Apêndice A | ticket 06 (customização da OWL) |
| B4 | axiomas de disjunção — parcialmente resolvido pela partição de A1 | ticket 06 |
| B5 | convenção de nome (`StakeHolder`, `Crud*`, `DataSource`) | ticket 06 |
| B6 | a camada de atributos do Apêndice A não existe no modelo | tickets 05 e 07 |
| B7 | nenhuma associação nomeada no modelo publicado | registro histórico; os nomes são da reconstrução |

### O que esta rodada não mediu

O OOPS! não foi reexecutado aqui: o antes/depois de *pitfalls* de OWL é do ticket 06, junto com a
customização, e rodá-lo agora, sobre uma OWL que ainda vai mudar, produziria um número que o próprio
ticket 06 invalidaria. A comparação quantitativa com o relatório OOPS! do baseline está na checklist
daquele ticket.

## Reproduzir

```sh
cd scripts/ontouml && npm ci && cd ../..
node scripts/ontouml/gerar-rodada-1.js                        # modelo, verificacao e OWL
node scripts/ontouml/controle-verificacao.js --modelo=rodada-1 # controle do plugin
node scripts/ontouml/verificador-ufo-extra.js                 # as cinco regras, antes e depois
node scripts/ontouml/diff-modelos.js                          # o diff estrutural
python scripts/verificar_rodada1.py                           # confere a checklist do ticket 04
```
