# Correções da rodada 2 — A5, A6, A7, e o que a rodada 1 adiou

Este documento fecha o ticket 05. É a rodada que traz para o modelo as duas microteorias da UFO que
a formalização publicada abdicou — **UFO-B**, dos eventos e da sua participação temporal, e
**UFO-C**, dos agentes e da distinção entre os físicos e os sociais. Para cada correção registra o
par **antes/depois** que a seção de análise ontológica vai usar, a **justificativa** que a sustenta e
o que ela muda na OWL e nas questões de competência.

O antes desta rodada é a **rodada 1**, não o baseline: o que ela tem de justificar é o que ela mesma
mudou. A distância acumulada até o *as-is* está nos verificadores, que rodam sobre os três modelos.

Os artefatos estão em `rodada-2/`:

| Arquivo | O que é |
|---|---|
| `ontompo-rodada-2.ontouml.json` | o modelo revisado, no OntoUML Schema |
| `ontompo-rodada-2.ttl` | a OWL da rodada, pela mesma transformação gUFO das anteriores |
| `relatorio-plugin-ontouml.md` / `.json` | a verificação contra a UFO, pelo motor do plugin |
| `relatorio-verificador-ufo-b-c.md` / `.json` | as nove regras estruturais, nos três modelos |
| `controle-verificacao.md` | o controle que torna interpretável o relatório vazio do plugin |
| `diff-rodada-1-rodada-2.md` | o diff estrutural entre as duas rodadas, derivado delas |

O baseline permanece intacto em `baseline/`, e a rodada 1 em `rodada-1/`. As três metades convivem:
nenhuma substitui a anterior, porque é a comparação entre elas que dá evidência.

## O que esta rodada abandona junto

Cai com ela a defesa de **"lightweight ontology"**. Ela não sobrevive à adoção das microteorias —
adotá-las é exatamente deixar de ser leve —, e como argumento já era passivo: um parecer do ONTOBRAS
a usou para dizer que a etapa OntoUML foi desperdício, outro para dizer que a ontologia estava
conceitualmente incompleta. Sob o enquadramento deste artigo a defesa perde função, e a segunda
crítica vira o achado de primeira linha desta rodada. `verificar_rodada2.py` varre o modelo e as
notas atrás de resquícios dela e reprova se algum sobreviver.

## A diferença, medida

O ticket 03 estabeleceu que o verificador do plugin OntoUML devolve zero sobre o *as-is*; o 04, que
ele continua devolvendo zero sobre a rodada 1. Sobre a rodada 2 ele devolve zero de novo, e pela
mesma razão: **nenhuma das suas 24 regras distingue endurante de perdurante a partir do papel que o
conceito tem no domínio**, que é precisamente o que A5 e B8 são.

Quem mede é `tools/verification/verificador-ufo-b-c.js`, que aplica aos três modelos as cinco regras
da rodada 1 mais quatro novas. Rodar as cinco antigas junto não é zelo: uma rodada que zerasse as
suas regras reintroduzindo as que a anterior fechou apareceria aqui.

| Regra | Tipo | Severidade | *as-is* | rodada 1 | rodada 2 |
|---|---|---|---|---|---|
| `memberof_whole_not_collective` | medição | error | 2 | 0 | 0 |
| `parthood_ends_undeclared` | medição | error | 1 | 0 | 0 |
| `mediation_optional_relatum` | medição | error | 3 | 0 | 0 |
| `class_name_collides_with_metaconcept` | medição | error | 1 | 0 | 0 |
| `relator_arity_above_binary` | medição | warning | 3 | 1 | 0 |
| `modelo_sem_perdurante` | medição | error | 1 | 1 | 0 |
| `modelo_sem_relacao_temporal` | medição | error | 1 | 1 | 0 |
| `evento_sem_participante` | guarda | error | 0 | 0 | 0 |
| `participacao_invertida` | guarda | error | 0 | 0 | 0 |
| **total** | | | **12** | **3** | **0** |

**As duas regras novas de medição não escrevem a resposta no gabarito, e isso importa.** Nenhuma
delas afirma que `Extract` deveria ser um evento — isso é julgamento de domínio, e está no argumento
de A5. O que elas registram é que o modelo inteiro não usa **nenhum** construto da microteoria: nem
uma classe de natureza evento ou situação (`modelo_sem_perdurante`), nem uma relação de
participação, criação, terminação ou dependência histórica (`modelo_sem_relacao_temporal`). É o
*construct deficit* de UFO-B na única forma que é computável do próprio modelo. São duas regras e não
uma porque são independentes: declarar eventos e não ligá-los a nada é exatamente a adoção de
fachada.

**As duas regras de guarda têm outro tipo de controle, e a diferença precisa ser dita.** Elas só
podem disparar sobre um modelo que já adotou UFO-B; sobre o *as-is* não têm o que verificar, e a
regra do ticket 04 — *regra que não dispara sobre o baseline não mede nada* — não se aplica a elas
sem as tornar impossíveis. O controle positivo delas é uma **mutação do próprio modelo revisado**,
aplicada pelo mesmo caminho de código, como em `controle-verificacao.md`: remover as três relações
que ligam `Observation` a seus participantes tem de produzir `evento_sem_participante`, e trocar as
pontas de `participation_Collector_Extract` tem de produzir `participacao_invertida`. A execução
reprova se alguma mutação passar despercebida.

**O que o zero do plugin diz, e não é pouco nesta rodada.** A revisão troca dois estereótipos de
classe por camada inteira — «kind» por «category» na camada de agentes, «relator» por «event» no ETL
— e cada troca mexe com natureza, sortalidade e rigidez nas generalizações vizinhas, que é
exatamente o território das 24 regras. Zero significa que nenhuma dessas trocas quebrou nada. O
controle em `rodada-2/controle-verificacao.md` mostra que ele acusaria, com quatro mutações
conhecidas, uma delas escolhida para exercitar a fronteira que a rodada introduziu: fazer `Extract`
especializar `Collector` produz `generalization_incompatible_natures`, porque um perdurante não pode
especializar um endurante.

**O que este número não é.** Não é medida de correção ontológica em geral. **A6 e A7 não viraram
regra, e isso é deliberado**, pela mesma razão que A1, A2 e A9 não viraram na rodada 1: que um
«kind» genérico colapse pessoa, grupo e organização, e que um sistema computacional não porte
momentos intencionais, são defeitos de significado, não de forma. Codificá-los como regra seria
escrever a resposta no gabarito. Continuam sustentados por argumento, abaixo.

---

## A5 — ETL vira evento

**Classificação BWW.** *Construct deficit* (UFO-B).

**Antes.** `Extract`, `Transform` e `Load` eram «relator», ligados aos seus relata por seis
mediações: `Extract` mediava `Collector` (1) e `DataSource` (1); `Transform`, `Collector` (1) e
`Processor` (1); `Load`, `Processor` (1) e `Storer` (1). Na OWL os três eram `gufo:Kind` sob
`gufo:Relator`, e o arquivo inteiro não tinha uma única ocorrência de `gufo:Event`, de participação
ou de qualquer propriedade de tempo.

**Depois.** Os três são «event». As seis mediações viram seis «participation», e entra um quarto
evento, `EtlProcess`, do qual os três são partes próprias por «participational»:

```
EtlProcess «event»
  ├──«participational»── Extract   «event» ←«participation»── Collector, DataSource
  ├──«participational»── Transform «event» ←«participation»── Collector, Processor
  └──«participational»── Load      «event» ←«participation»── Processor, Storer
```

**As multiplicidades são as mesmas, e a preservação é verificada.** Onde a rodada 1 tinha
`«mediation» Extract [1..*] -> Collector [1]`, a rodada 2 tem `«participation» Collector [1] ->
Extract [1..*]`: as mesmas duas multiplicidades, trocadas de lado junto com as pontas. O `1..*` do
lado do evento continua dizendo o que a dependência existencial da mediação dizia — um coletor só é
coletor porque participou de ao menos uma extração. `verificar_rodada2.py` confere as dez
substituições uma a uma, multiplicidade a multiplicidade, e reprova se alguma relação que o modelo
anterior expressava deixar de estar representada.

**Justificativa.** Relatores são endurantes: estão inteiramente presentes a cada instante em que
existem e não têm partes temporais [guizzardi2005ontological]. Uma extração, uma transformação e uma
carga são processos — têm início e fim, desdobram-se no tempo, têm partes temporais e têm
participantes [guizzardi2008grounding]. A diferença não é de gosto: ela decide o que o modelo
consegue responder. A **QC3** pergunta *que agente executou a carga de uma dada fonte de dados, e
quando*. Com o ETL como relator endurante não havia "quando" — não existia no modelo nada que
carregasse tempo, e a questão de competência era irrespondível por construção. Com o ETL como
evento, o "quando" passa a ter onde ser dito sem que o modelo precise inventar atributo nenhum:
`gufo:Event` já traz `gufo:hasBeginPointInXSDDateTimeStamp` e `gufo:hasEndPointInXSDDateTimeStamp`,
e é a instanciação do ticket 07 que os preenche. O "quem" é a participação.

**Por que um evento complexo, e não três soltos.** A **QC6** pede a cadeia de proveniência de um
conteúdo divulgado até a fonte de dados original. Três eventos independentes não dizem que aquela
carga corresponde àquela extração; a parthood entre eventos diz. `EtlProcess` é o acontecimento
único do qual a extração daquela fonte, a transformação e a carga naquele armazenamento são partes,
e é ele que dá à QC6 um caminho a percorrer.

**Na OWL.** Saem seis `gufo:mediates`. Entram seis `rdfs:subPropertyOf gufo:participatedIn`, com
domínio no endurante e alcance no evento — a direção que a gUFO exige —, três
`rdfs:subPropertyOf gufo:isEventProperPartOf`, e quatro classes `gufo:EventType` sob `gufo:Event`.
Nenhuma mediação restante toca um evento, e a verificação confere isso nas duas pontas de todas
elas.

## B8 — `Observation` era o relator ternário que sobrou

**Classificação BWW.** *Construct deficit* (UFO-B); na rodada 1, ambiguidade de aridade.

**Antes.** `Observation` era «relator» e mediava três relata — `Knowledge` (1..\*), `Agent` (1) e
`Disseminator` (1). Era o único achado que o verificador complementar deixava em aberto ao fim da
rodada 1, e era achado do **instrumento**, não da inspeção manual: A8 nomeou `Management` e
`Operation`, e `Observation` passou despercebido nas duas leituras. A rodada 1 o registrou como B8 e
o endereçou a esta, com a razão escrita: uma observação é candidata natural a evento, e a
decomposição correta dependia de UFO-B.

**Depois.** `Observation` é «event». `Agent` e `Disseminator` passam a participar dela por
«participation». `Knowledge` não participa: passa a ser **criado** nela, por «creation».

**Justificativa.** Observar é um acontecimento, não um vínculo. Quem observa e por onde o observado
é disseminado são participantes; o que passa a ser conhecido não estava lá antes do evento e por
isso não participa dele — ele é seu produto. A distinção entre participação e criação é da UFO-B
[guizzardi2008grounding] e não tinha como ser feita com uma mediação, que trata os três relata como
iguais. Reificar a observação como relator forçava exatamente esse achatamento, e é por isso que a
aridade três aparecia: não eram três participantes de um vínculo, eram dois participantes e um
produto de um evento.

**O que isso vale para o artigo.** Que a ferramenta tenha encontrado o que a análise manual não
encontrou já era material para a tese de que deficiências representacionais permanecem latentes. Que
o achado tenha se resolvido como *construct deficit* de UFO-B, e não como a decomposição de aridade
que A8 aplicou a `Management` e `Operation`, é o segundo tempo do mesmo argumento: o instrumento
apontou o lugar, mas a classificação correta só apareceu com a microteoria.

**Na OWL.** Saem três `gufo:mediates`. Entram duas `gufo:participatedIn` e uma
`gufo:wasCreatedIn` de `Knowledge` para `Observation`.

## A1 — a leitura eventiva que a rodada 1 adiou

**Classificação BWW.** *Construct overload*, corrigido na rodada 1; o que se fecha aqui é o limite
que aquela correção declarou.

**Antes.** A rodada 1 decompôs `CrudOperation` numa partição disjunta e completa de quatro
«subkind» de natureza relator, e registrou por escrito o que ficava faltando: *"uma operação
continua sendo modelada como endurante. A leitura eventiva — cada operação como evento, com pré e
pós-estado e participação temporal — depende de UFO-B e é do ticket 05"*. As duas mediações, para
`Agent` (1) e `CrudView` (1), continuavam no tipo geral.

**Depois.** `CrudOperation` e as quatro operações são «event». A partição `crudOperationType`
sobrevive intacta à troca de estereótipo — separar os quatro tipos nunca dependeu de eles serem
endurantes — e as duas mediações viram participações de `Agent` e `CrudView` no tipo geral, herdadas
pelas quatro.

**Justificativa.** Uma operação de escrita é um acontecimento com pré-estado e pós-estado; foi
exatamente a incompatibilidade entre as pós-condições de `Create`, `Update` e `Delete` que sustentou
a sobrecarga de construto de A1 [wand1993ontological]. Modelar como endurante o construto cuja
justificativa é a diferença entre pós-condições era manter, na forma, o que a decomposição corrigiu
no conteúdo. Como evento, `ReadOperation` fica com a propriedade que a decomposição da rodada 1
tornou visível e não tinha onde escrever: é a única das quatro que não muda estado nenhum.

**O que continua em aberto, e onde.** As pós-condições em si — o que passa a existir numa criação, o
que deixa de existir numa exclusão — precisam do conceito de item de dado, que o Apêndice A da
dissertação define e o modelo publicado não tem (B6). Com ele, `CreateOperation` e `DeleteOperation`
ganham «creation» e «termination», como `Observation` ganhou aqui. Fica para os tickets 06 e 07,
junto com a camada de atributos.

**Na OWL.** As quatro operações passam de `owl:Class` sob `ontompo:CrudOperation` com `gufo:SubKind`
a `gufo:EventType`; a disjunção da partição continua lá, e ganha a companhia da segunda, de A6.

## A6 — `Agent` vira a taxonomia UFO-C que faltava

**Classificação BWW.** *Construct deficit* (UFO-C).

**Antes.** Um único `Agent` «kind», com três papéis abaixo — `ObservatoryUser`, `StakeHolder` e
`System`. Não havia `Person`, não havia `Organization`, não havia distinção entre agente físico e
agente social.

**Depois.**

```
Agent «category» {complexo funcional, coletivo}
  ├── PhysicalAgent «category» ── Person «kind» ── ObservatoryUser «role»
  ├── SocialAgent   «category» ── Organization «kind»
  └── StakeHolder «roleMixin» {complexo funcional, coletivo}

ComputationalSystem «kind» ── System «role»          (A7, fora de Agent)
```

A partição `agentNature` é **disjunta e completa**: todo agente é físico ou social, e não os dois.

**Justificativa.** A UFO-C distingue agentes de objetos pela capacidade de portar momentos
intencionais — crenças, intenções, compromissos — e distingue agentes físicos de agentes sociais
[guizzardi2008grounding]. O defeito do baseline não é a ausência dessa distinção como ornamento: é
que um «kind» fornece **exatamente um** princípio de identidade, e o material de origem enumera
três. O glossário do Apêndice A define *Partes interessadas dos projetos* como "indivíduo, grupo ou
organização". Pessoa, equipe e organização têm princípios de identidade distintos — uma organização
sobrevive à troca de todos os seus membros, uma equipe não sobrevive do mesmo modo, e uma pessoa não
é um agregado de ninguém. Reuni-los sob um «kind» é afirmar que compartilham um princípio de
identidade que eles não compartilham.

`Agent` como «category» é a correção direta disso: uma categoria é rígida e **não-sortal**, isto é,
classifica entidades que obedecem a princípios de identidade diferentes sem lhes fornecer um. Os
sortais últimos que faltavam entram embaixo — `Person` sob `PhysicalAgent`, `Organization` sob
`SocialAgent`.

`StakeHolder` deixa de ser «role» e vira «roleMixin» pela mesma razão, e este é o ponto mais direto
do argumento: um papel sortal só pode ser desempenhado por instâncias de um kind, e a definição do
próprio glossário abrange três. O `roleMixin` é o construto que a UFO tem para exatamente isso — um
papel antirrígido sobre múltiplos kinds. O modelo publicado não podia expressá-lo porque não tinha a
camada de não-sortais.

`ObservatoryUser`, ao contrário, é sortal: um usuário do observatório é uma pessoa, e passa a ser
papel de `Person`, que agora lhe fornece identidade.

**A consequência prática.** A **QC5** — *que motivações levam cada tipo de ator a interagir com o
observatório* — pressupõe tipos de ator que o modelo não tinha. Com a taxonomia, "tipo de ator"
passa a ser uma pergunta com resposta no modelo, e a distinção físico/social é o que permite
separar a motivação de uma pessoa da de uma organização.

**Na OWL.** `ontompo:Agent` deixa de ser `gufo:Kind` e passa a `gufo:Category`; entram
`PhysicalAgent` e `SocialAgent`, também categorias, `Person` e `Organization` como `gufo:Kind`, e
`StakeHolder` como `gufo:RoleMixin`. A partição vira `owl:AllDisjointClasses` mais o `owl:unionOf`
de completude — o segundo par de axiomas de disjunção do modelo, contra os zero do baseline (B4).

## A7 — o kind subjacente a `System`

**Classificação BWW.** *Construct deficit*.

**Antes.** `System` era «role» especializando `Agent` «kind». Formalmente havia provedor de
identidade, e o verificador nada acusava — o controle mostra que ele acusaria
`class_missing_identity_provider` se a generalização fosse removida. O defeito não era ausência de
provedor: era **provedor errado**.

**Depois.** Entra `ComputationalSystem` «kind», e `System` passa a ser papel dele. `System` deixa de
descender de `Agent`.

**Justificativa.** É a deficiência mais barata das nove, porque a própria dissertação a declara por
escrito, no capítulo de resultados: o tipo rígido que fundamenta a existência de `System` fora do
contexto relacional do observatório "não foi explicitado no diagrama, constituindo uma simplificação
do modelo cuja explicitação é apontada como melhoria para trabalhos futuros". Explicitá-lo é fechar
um trabalho futuro que o próprio autor nomeou.

O que a dissertação não diz, e a UFO-C diz, é que a simplificação **não era neutra**. Ao pendurar
`System` sob `Agent`, o modelo afirmava que todo sistema computacional externo é um agente. Em UFO-C
agente é o que porta momentos intencionais; um sistema que fornece um serviço não crê, não pretende
e não se compromete. O papel existe e é legítimo — o sistema participa das interações do
observatório —, mas o sortal último que o fundamenta é outro, e é ele que faltava. Essa é a razão
pela qual A7 não podia ser resolvida na rodada 1: sem a camada de não-sortais de A6 não havia onde
`Agent` deixar de ser o teto de tudo.

**Na OWL.** `ontompo:System rdfs:subClassOf ontompo:Agent` desaparece; entra
`ontompo:System rdfs:subClassOf ontompo:ComputationalSystem`, com `ComputationalSystem` como
`gufo:Kind`.

---

## O que ficou em aberto

### B9 — `SocialInteraction` continua «relator», e o teste que a rodada aplicou não o poupa

O critério desta rodada foi explícito: vira evento o construto que o material de origem descreve
como acontecimento. Aplicado sem exceção, ele alcança `SocialInteraction` — uma interação social é,
em UFO-C, um evento comunicativo, não um vínculo entre um `Agent` e um `Reporter`. Ele **não** foi
convertido aqui, por duas razões que precisam ficar registradas em vez de dissimuladas.

A primeira é de escopo: A5 nomeia o ETL, e B8 foi endereçado a esta rodada por escrito na anterior;
`SocialInteraction` não foi. A segunda é substantiva: `Log` está no mesmo par de mediações e **não**
é um evento — um registro de log é um endurante, produzido por um evento —, e decidir se
`SocialInteraction` é o evento de interagir ou o registro daquela interação exige do material de
origem uma distinção que ele não faz. Converter os dois seria uniformidade sem fundamento; converter
um e não o outro sem dizer por quê seria pior.

Fica como **B9**, com a mesma disciplina com que B8 ficou registrado na rodada 1: candidato a
evento, dependente de uma leitura do Apêndice A que o ticket 07 vai precisar fazer de qualquer modo
para instanciar o cenário. Que o teste tenha produzido um candidato novo ao ser aplicado a sério é,
de novo, evidência para a tese do artigo.

### B10 — `ObservatoryGroup` reúne agentes e não-agentes

As três «memberOf» corrigidas em A3 continuam como estavam, e uma delas passa a incomodar: depois de
A7, `System` não é um agente, e continua declarado membro do mesmo coletivo de que `ObservatoryUser`
e `StakeHolder` são membros. Um coletivo em UFO é uma coleção cujos membros têm estrutura uniforme;
uma coleção que mistura pessoas e sistemas computacionais não a tem.

A tensão **não existia antes desta rodada** — enquanto tudo era `Agent`, os membros eram uniformes
por construção —, e é a adoção da UFO-C que a torna visível. Não é corrigida aqui porque as duas
saídas disponíveis mudam o conteúdo do modelo publicado: ou o grupo deixa de ter sistemas como
membros, ou deixa de ser um coletivo de agentes. Escolher entre elas é decisão de domínio, e o
material de origem não a suporta sozinho. Fica declarada como limitação e endereçada ao ticket 07,
onde a instanciação vai forçar a escolha.

É por isso que `ObservatoryGroup` **não** foi colocado sob `SocialAgent` nesta rodada, embora um
grupo seja o exemplo canônico de agente social em UFO-C: declará-lo agente enquanto ele tem sistemas
por membros seria trocar uma tensão silenciosa por uma contradição explícita.

### Deficiências das próximas rodadas

| # | Deficiência | Onde é resolvida |
|---|---|---|
| B3 | 63 elementos sem definição, contra 53 termos definidos no Apêndice A | ticket 06 (customização da OWL) |
| B4 | axiomas de disjunção — as duas partições cobrem parte | ticket 06 |
| B5 | convenção de nome (`StakeHolder`, `Crud*`, `DataSource`) | ticket 06 |
| B6 | a camada de atributos do Apêndice A não existe no modelo | ticket 07 |
| B7 | nenhuma associação nomeada no modelo publicado | registro histórico |
| B9 | `SocialInteraction` como relator, candidato a evento | ticket 07 |
| B10 | `ObservatoryGroup` com membros de naturezas incompatíveis | ticket 07 |

### O que esta rodada não mediu

O OOPS! continua sem ser reexecutado. O antes/depois de *pitfalls* de OWL é do ticket 06, junto com
a customização, e a OWL desta rodada ainda vai mudar lá — rodá-lo agora produziria um número que
aquele ticket invalidaria. A comparação quantitativa com o relatório do baseline está na checklist
do 06.

## Reproduzir

```sh
cd tools && npm ci && cd ..
node tools/generation/gerar-rodada-2.js                              # modelo, verificacao e OWL
node tools/verification/controle-verificacao.js --modelo=rodada-2    # controle do plugin
node tools/verification/verificador-ufo-b-c.js                       # as nove regras, nos tres modelos
node tools/generation/diff-modelos.js --de=rodada-1 --para=rodada-2  # o diff estrutural
python tools/verification/verificar_rodada2.py                       # confere a checklist do ticket 05
```
