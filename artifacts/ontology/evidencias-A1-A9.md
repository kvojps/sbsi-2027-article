# Evidência das deficiências A1–A9 no modelo *as-is*

Este documento fecha o ticket 03: para cada uma das nove deficiências previstas no *spec*, registra
**onde ela está** no baseline reconstruído, **se alguma ferramenta a acusou** e, quando nenhuma
acusa, **qual é o argumento ontológico** que a sustenta. Ao fim, registra o que as ferramentas
apontaram além de A1–A9.

Os artefatos referenciados estão em `baseline/`:

| Arquivo | O que é |
|---|---|
| `ontompo-as-is.ontouml.json` | o modelo OntoUML no OntoUML Schema, formato de intercâmbio do plugin |
| `ontompo-as-is.ttl` | a OWL de baseline, pela transformação gUFO oficial |
| `ontompo-as-is.owl` / `.oops.owl` | a mesma OWL em RDF/XML, completa e na cópia submetida ao OOPS! |
| `relatorio-plugin-ontouml.md` / `.json` | a verificação sintática e semântica contra a UFO |
| `relatorio-oops.md` / `.xml` | os *pitfalls* do OOPS! |
| `controle-verificacao.md` | o controle que prova que o verificador está de fato rodando |

## O resultado que precisa ser dito primeiro

**Nenhuma das duas ferramentas automáticas acusa qualquer uma das nove deficiências.** O verificador
do plugin OntoUML devolve zero problemas sobre o baseline; o OOPS! devolve sete achados, todos de
higiene de OWL — anotação, disjunção, convenção de nome — e nenhum sobre fundamentação ontológica.

Isso não enfraquece os achados: delimita o que cada instrumento pode dizer, e a delimitação é
verificável. O conjunto de regras do verificador tem 24 códigos, todos sobre estereótipo de classe,
provedor de identidade, natureza e generalização (a lista completa está no cabeçalho de
`relatorio-plugin-ontouml.md`). **Nenhum trata de restrição meronímica, de aridade de relator, de
distinção endurante/perdurante ou de sobrecarga de construto.** O OOPS! opera um nível abaixo, sobre
o grafo RDF, e não conhece a UFO.

O zero do verificador foi submetido a controle. `controle-verificacao.md` aplica três mutações
conhecidas ao mesmo modelo, pelo mesmo caminho de código, e cada uma é acusada com o código
esperado — remover a generalização de `System` para `Agent` produz
`class_missing_identity_provider`, fazer `Software` especializar `View` produz
`generalization_incompatible_class_rigidity`, e dar a `ProjectObservatory` um segundo sortal último
produz `class_multiple_identity_providers`. O zero é resultado, não cano entupido.

Duas consequências para o artigo:

1. A seção de análise ontológica não pode apresentar A1–A9 como saída de ferramenta. Elas são
   resultado de análise fundamentada, e a evidência objetiva que as sustenta é **a estrutura do
   modelo reconstruído**, que é machine-readable e está depositada, mais o argumento explícito
   abaixo.
2. O antes/depois medido por ferramenta, que o ticket 04 vai produzir, mede higiene de OWL, não
   correção ontológica. Prometer mais do que isso é convite a parecer.

## A1 — `CrudOperation` colapsa Create, Update e Delete

**Classificação BWW.** *Construct overload*.

**No baseline.** Uma única classe «relator» `CrudOperation`, com exatamente duas mediações:
`mediation_CrudOperation_Agent` (Agent, 1) e `mediation_CrudOperation_CrudView` (CrudView, 1). Não
há subclasse, partição, atributo nem enumeração que discrimine qual operação está em jogo. Em
`ontompo-as-is.ttl`, `ontompo:CrudOperation` é `gufo:Kind` sob `gufo:Relator`, e nada mais.

**Ferramentas.** Nenhuma acusa. O OOPS! lista `CrudOperation` no P08 por não ter definição — sintoma,
não o defeito.

**Argumento.** Um construto está sobrecarregado quando um mesmo construto gramatical representa mais
de um construto ontológico [wand1993ontological]. `Create`, `Update` e `Delete` têm pós-condições
distintas e mutuamente incompatíveis: a primeira faz existir um item de dado que não existia, a
segunda altera as propriedades de um item que permanece o mesmo, a terceira faz deixar de existir. Em
UFO essas três são mudanças de estado de tipos diferentes — criação, mudança qualitativa e
terminação — e nenhuma delas é distinguível no modelo. Um leitor que queira saber *o que aconteceu
com o dado* não obtém resposta do modelo; obtém-a do nome da classe, que é justamente o que a
formalização deveria eliminar.

O nome `CrudOperation` é a prova pública da sobrecarga: quatro letras iniciais anunciam quatro
fenômenos num construto só.

## A2 — `Software` como composição de `Hardware`

**Classificação BWW.** *Construct excess* / mereologia inválida.

**No baseline.** `componentOf_Hardware_Software`, com a parte em `Hardware` (1..\*) e o todo em
`Software` (1..\*); o losango preto está desenhado do lado de `Software` no diagrama de
infraestrutura. Sobrevive à transformação:

```turtle
ontompo:componentOf_Hardware_Software rdf:type owl:ObjectProperty;
    rdfs:domain ontompo:Hardware;
    rdfs:range ontompo:Software;
    rdfs:subPropertyOf gufo:isComponentOf.
```

**Ferramentas.** Nenhuma acusa. O verificador não tem regra meronímica; `Software` e `Hardware` são
ambos «kind» e portanto ambos restritos a complexo funcional, de modo que a checagem de naturezas —
a única que chega perto — passa.

**Argumento.** Em UFO, «componentOf» é parthood entre complexos funcionais, e a parte contribui para
o princípio de identidade do todo [guizzardi2005ontological]. Software não é feito de hardware. O
teste é direto: troque-se todo o hardware sob uma aplicação e a aplicação continua sendo a mesma
aplicação; troquem-se os componentes de um complexo funcional e não se tem mais o mesmo complexo. A
relação real é de execução e hospedagem — o hardware suporta a manifestação do software, e o
software depende existencialmente dele para se manifestar, sem ser dele composto.

A multiplicidade agrava: `1..*` na ponta de `Hardware` obriga todo hardware a ser componente de pelo
menos um software, o que exclui do domínio qualquer equipamento que não execute aplicação alguma —
um switch, um nobreak, um disco de backup.

A rigor, a mereologia inválida está declarada em OWL contra a própria gUFO: `gufo:isComponentOf`
carrega as restrições de parthood da UFO, e o baseline as instancia com os relata trocados.

## A3 — `«MemberOf»` entre `ObservatoryGroup` e os papéis de agente, com o todo do lado errado

**Classificação BWW.** Violação de restrição da UFO.

**Divergência com o *spec*, que precisa ser corrigida no artigo.** O *spec* descreve A3 como
`«CompOf»` ligando `ObservatoryUser` a `ObservatoryGroup`. Nos diagramas publicados, lidos em
resolução de origem — tanto o da camada de agentes quanto o integrado —, **o estereótipo é
`«MemberOf»`, não `«CompOf»`**. O defeito existe, mas é outro: é a *direção*. Quem escrever a seção
de análise ontológica precisa usar esta descrição, e não a do *spec*; a original é falsificável por
qualquer revisor que abra a dissertação. Fica registrado para o ticket 10.

**No baseline.** Três relações «memberOf», todas com `ObservatoryGroup` como origem:

| Relação | Todo declarado | Parte declarada | Multiplicidades |
|---|---|---|---|
| `memberOf_ObservatoryGroup_ObservatoryUser` | `ObservatoryUser` («role») | `ObservatoryGroup` («collective») | 1 no grupo, 0..\* no papel |
| `memberOf_ObservatoryGroup_StakeHolder` | `StakeHolder` («role») | `ObservatoryGroup` («collective») | 1 no grupo, 0..\* no papel |
| `memberOf_ObservatoryGroup_System` | **nenhum** | **nenhuma** | 1 no grupo, 0..\* no papel |

No JSON, o `aggregationKind` fica na ponta de `ObservatoryUser` e `StakeHolder` (`SHARED`) — o
losango está do lado do papel. Na terceira, `aggregationKind` é `NONE` nas duas pontas: a relação
carrega o estereótipo de agregação sem designar todo nem parte. Não é erro de transcrição; o recorte
ampliado de `mpo_agents_formalization.png` mostra a linha chegando limpa na caixa de `System`.

Na OWL a inversão vira asserção:

```turtle
ontompo:memberOf_ObservatoryGroup_ObservatoryUser rdf:type owl:ObjectProperty;
    rdfs:domain ontompo:ObservatoryGroup;
    rdfs:range ontompo:ObservatoryUser;
    rdfs:subPropertyOf gufo:isCollectionMemberOf.
```

**Ferramentas.** Nenhuma acusa, pela mesma razão de A2.

**Argumento.** «memberOf» exige que o todo seja um coletivo e que as partes sejam seus membros
[guizzardi2005ontological]. Aqui o coletivo é a parte declarada e um «role» de complexo funcional é o
todo declarado — exatamente o inverso. A `gufo:isCollectionMemberOf` vai de membro para coleção, de
modo que o baseline afirma que **o grupo do observatório é membro do usuário**. Somada à afirmação
de que `ObservatoryUser` é `gufo:Role` sobre complexos funcionais, a asserção é contraditória: a
mesma classe seria coleção e complexo funcional.

A terceira relação é um defeito adicional e independente, registrado abaixo como B2.

## A4 — classe de domínio chamada `Relator`

**Classificação BWW.** *Construct redundancy* terminológica.

**No baseline.** Uma classe «role» de nome `Relator`, especializando `View` e mediada por
`SocialInteraction` e `Log`. Na OWL, `ontompo:Relator` é `gufo:Role`, e convive no mesmo documento
com `gufo:Relator`, o metaconceito da UFO.

**Ferramentas.** Indiretamente, sim — e este é o único dos nove que aparece numa saída de ferramenta.
O relatório do OOPS! lista, no mesmo *pitfall* P08, os dois elementos afetados:

```
- http://purl.org/nemo/gufo#Relator
- https://example.org/ontompo/as-is#Relator
```

A colisão está impressa na saída da ferramenta, ainda que a ferramenta não a esteja reportando *como*
colisão. (O gerador de relatório imprime IRI completo, e não nome curto, exatamente quando dois
elementos colidem no nome curto — encurtar apagaria a evidência.)

**Argumento.** Numa linguagem cujo metamodelo define «relator» como categoria de fundamentação,
nomear uma classe de domínio `Relator` faz dois significados incompatíveis ocuparem o mesmo termo:
para a UFO, um relator é um endurante que existencialmente depende de várias entidades; para o MPO,
`Relator` é quem relata. Um leitor precisa do contexto tipográfico — a caixa amarela «role», não a
laranja «relator» — para desambiguar. Isso é redundância de construto no sentido de Wand e Weber
[wand1993ontological]: dois construtos gramaticais para o mesmo termo, com o agravante de que um
deles é da própria linguagem.

## A5 — ETL modelado como relator endurante, não como evento

**Classificação BWW.** *Construct deficit* (UFO-B).

**No baseline.** `Extract`, `Transform` e `Load` são «relator». `Extract` medeia `Collector` (1) e
`DataSource` (1); `Transform` medeia `Collector` (1) e `Processor` (1); `Load` medeia `Processor` (1)
e `Storer` (1). Na OWL, os três são `gufo:Kind` sob `gufo:Relator`. **O arquivo inteiro não tem uma
única ocorrência de `gufo:Event`, de participação temporal ou de qualquer propriedade de tempo.**

**Ferramentas.** Nenhuma acusa. O verificador não tem regra que distinga endurante de perdurante a
partir do nome ou do papel do conceito no domínio.

**Argumento.** Relatores são endurantes: estão inteiramente presentes a cada instante em que existem
e não têm partes temporais [guizzardi2005ontological]. Uma extração, uma transformação e uma carga
são processos: têm início e fim, desdobram-se no tempo, têm partes temporais e têm participantes
[guizzardi2008grounding]. A diferença não é de gosto — ela decide o que o modelo consegue responder.
QC3 do *spec* pergunta *que agente executou a carga de uma dada fonte de dados, e quando*. Com ETL
como relator endurante não há "quando": não existe no modelo nada que carregue tempo. A questão de
competência é irrespondível por construção, e é a evidência mais forte de A5.

## A6 — `Agent` como «kind» genérico, sem distinção físico/social

**Classificação BWW.** *Construct deficit* (UFO-C).

**No baseline.** Um único `Agent` «kind», com três papéis abaixo: `ObservatoryUser`, `StakeHolder` e
`System`. Não há `Person`, não há `Organization`, não há distinção entre agente físico e agente
social, e não há qualquer classe que separe agente de objeto.

**Ferramentas.** Nenhuma acusa. A hierarquia é formalmente legal: três antirrígidos especializando um
rígido.

**Argumento.** A UFO-C distingue agentes de objetos pela capacidade de portar momentos intencionais —
crenças, intenções, compromissos — e distingue agentes físicos de agentes sociais
[guizzardi2008grounding]. O glossário do Apêndice A da dissertação define *Partes interessadas dos
projetos* como "indivíduo, grupo ou organização", e *Equipe de gestão e desenvolvimento* como "time":
o próprio material de origem enumera pessoas, grupos e organizações como instâncias, três coisas com
princípios de identidade distintos, todas colapsadas num «kind» só. Um «kind» fornece exatamente um
princípio de identidade; um construto que reúne pessoa, equipe e organização não pode fornecê-lo.

A consequência prática é a QC5 do *spec* — *que motivações levam cada tipo de ator a interagir com o
observatório* —, que pressupõe tipos de ator que o modelo não tem.

## A7 — `System` como «role» sem kind subjacente adequado

**Classificação BWW.** *Construct deficit*.

**No baseline.** `System` é «role» e especializa `Agent` «kind». Formalmente há provedor de
identidade, e o verificador nada acusa — o controle em `controle-verificacao.md` mostra que ele
*acusaria* (`class_missing_identity_provider`) se a generalização fosse removida. Ou seja: o defeito
não é ausência de provedor, é provedor errado.

**Ferramentas.** Nenhuma acusa.

**Argumento.** A dissertação declara a omissão por escrito, no capítulo de resultados: o kind
subjacente ao papel `System`, "o tipo rígido que fundamenta sua existência fora do contexto
relacional do observatório, não foi explicitado no diagrama, constituindo uma simplificação do
modelo cuja explicitação é apontada como melhoria para trabalhos futuros". É a evidência mais barata
dos nove achados — o defeito está admitido na fonte.

O que a dissertação não diz é que a simplificação adotada não é neutra: ao pendurar `System` sob
`Agent`, o modelo afirma que todo sistema computacional externo é um agente. Em UFO-C, agente é o que
porta momentos intencionais; um sistema que fornece um serviço não crê, não pretende e não se
compromete. O papel existe e é legítimo — o sistema participa das interações do observatório —, mas o
sortal último que o fundamenta é outro, e é ele que falta.

## A8 — `Management` e `Operation` como relatores n-ários não justificados

**Classificação BWW.** Ambiguidade de aridade.

**No baseline.** `Management` medeia três entidades: `Project` (1), `DataManager` (1) e `View` (1).
`Operation` medeia quatro: `Software` (0..\*), `Service` (1), `Hardware` (0..\*) e `Network` (0..\*).
Nem o diagrama nem o Apêndice A dizem que fato relacional único cada um reifica.

**Ferramentas.** Nenhuma acusa.

**Argumento.** Um relator reifica um fato relacional, e sua aridade deveria decorrer do fato reificado
[guizzardi2005ontological]. `Operation` não sobrevive ao teste: **três das suas quatro mediações têm
mínimo zero na ponta mediada** — `mediation_Operation_Software`, `mediation_Operation_Hardware` e
`mediation_Operation_Network` são todas `0..*`. O modelo portanto admite uma instância de `Operation`
que medeia um `Service` e mais nada. Mas um relator existe *porque* conecta os relata; um relator que
pode existir conectando um só relatum não reifica relação nenhuma.

Isso é mais forte do que "aridade não justificada": mínimo zero numa ponta mediada contradiz a
dependência existencial que define a mediação, e vale como defeito próprio — está registrado abaixo
como B1.

`Management` não tem o problema de cardinalidade — as três pontas são 1 — mas reifica um fato
relacional que o material de origem não nomeia. Um relator que liga um projeto, um gerenciador de
dados e uma visão pode ser três coisas diferentes, e o modelo não diz qual.

## A9 — `ProjectObservatory` especializa `Software` e é especializado por `DataManager` e `View`

**Classificação BWW.** Confusão de princípio de identidade.

**No baseline.** A cadeia de generalizações é:

```
Software «kind»
  └── ProjectObservatory «subkind»
        ├── DataManager «role» ── CrudRepository, Collector, Processor, Storer
        └── View «role» ──────── Disseminator, Relator, CrudView
```

**Ferramentas.** Nenhuma acusa. Papéis antirrígidos especializando um subkind rígido é legal, e o
subkind especializando o kind também.

**Argumento.** A hierarquia afirma que todo `DataManager` é um `ProjectObservatory` e que todo `View`
é um `ProjectObservatory`. Como `View` é especializado por `Disseminator`, `Relator` e `CrudView`,
segue que cada visão, cada disseminador e cada relator **é um observatório de projetos inteiro**.

A consequência é verificável contra o próprio *spec*: QC1 pergunta *quais Views são disponibilizadas
por um dado `DataManager`*. A pergunta pressupõe muitas visões por gerenciador; o modelo faz de cada
visão um observatório. Perguntar quais observatórios um observatório disponibiliza não é a pergunta
de domínio que a QC quer fazer, e nenhuma consulta sobre este modelo devolve o que ela pede.

O que `DataManager` e `View` são, no material de origem, é papel desempenhado por *componentes* do
observatório — a subcamada "Componentes" do MPO —, não especialização do observatório. Trocar
especialização por composição é a correção, e ela é do ticket 04.

---

## Achados além de A1–A9

O ticket pede que deficiências apontadas pelas ferramentas fora da lista fiquem registradas. Seguem,
separadas do que é artefato do próprio pipeline.

### B1 — mediações com mínimo zero na ponta mediada

`mediation_Operation_Software`, `mediation_Operation_Hardware` e `mediation_Operation_Network` têm
`0..*` na ponta mediada. Uma «mediation» é relação de dependência existencial: o relator não pode
existir sem o mediado, e a multiplicidade mínima na ponta mediada tem de ser ao menos 1
[guizzardi2005ontological]. Estrutural, machine-checkable a partir do JSON, e não coberto por nenhuma
das 24 regras do verificador. **Candidato forte a achado adicional no artigo** — é o único defeito
novo que a reconstrução revelou e que se sustenta sozinho.

### B2 — relação meronímica sem todo nem parte

`memberOf_ObservatoryGroup_System` tem `aggregationKind` `NONE` nas duas pontas: carrega o
estereótipo de agregação sem designar quem é o todo. As duas irmãs, com `ObservatoryUser` e
`StakeHolder`, designam — invertido, o que é A3. Uma relação de parthood sem parthood declarada não
é sequer interpretável como errada; é indeterminada.

### B3 — nenhuma definição sobrevive ao modelo (OOPS! P08, 63 elementos)

O OOPS! acusa 63 elementos sem anotação legível — todas as 32 classes e todas as 28 relações, mais
três termos da gUFO. É achado real e vale citar no artigo pelo contraste: **o Apêndice A da
dissertação define 53 termos**, com definição, sinônimos, instâncias, atributos e constantes. As
definições existem e não chegaram ao modelo. A conceituação da Methontology foi feita e depois
descartada na formalização.

### B4 — nenhum axioma de disjunção (OOPS! P10)

O modelo não declara disjunção em lugar nenhum. `DataManager` e `View` especializam o mesmo
`ProjectObservatory` sem serem declarados disjuntos, e nada impede uma entidade de ser as duas ao
mesmo tempo. Vale pouco isolado, mas soma a A9.

### B5 — convenção de nome inconsistente (OOPS! P22, marginal)

O OOPS! aponta `DataSource`. Vale registrar mais dois casos que ele não pega: `StakeHolder` com H
maiúsculo, contra a grafia corrente *Stakeholder*, e `Crud*` contra o acrônimo `CRUD`.

### B6 — a camada de atributos do Apêndice A não existe no modelo

O modelo tem **zero atributos**. O Apêndice A especifica, para cada conceito, atributos de classe,
atributos de instância e tabelas de constantes — tipo, subtipo, provedor, local, período, custo,
disponibilidade, capacidade, protocolo, topologia, formato. Nada disso foi formalizado. Nenhuma
ferramenta acusa, porque um modelo sem atributos é um modelo válido; mas a QC3, que pede *quando* uma
carga ocorreu, e a QC6, que pede a cadeia de proveniência, precisam de atributos que o modelo não
tem.

### B7 — nenhuma associação é nomeada

Nenhuma das 28 relações do modelo publicado tem nome; só o estereótipo. Os nomes que aparecem no
baseline (`mediation_Observation_Agent` e afins) foram gerados na reconstrução, de forma
determinística, para que a transformação gUFO produzisse IRIs estáveis — a ausência no original está
registrada aqui para que ninguém a leia como conteúdo do modelo.

### Não são achados: artefatos do pipeline

Três saídas do OOPS! não dizem nada sobre o modelo e não devem entrar no artigo:

- **P34, *untyped class*, 13 elementos** — são termos da gUFO (`Kind`, `Role`, `Relator`, `SubKind`,
  `FunctionalComplex`, `VariableCollection`) e nós anônimos de restrição. Ficam sem declaração porque
  o `owl:imports gufo:` é removido da cópia submetida; com ele presente, o serviço devolve
  `unexpected_error`.
- **P35, *untyped property*, 3 elementos** — `mediates`, `isComponentOf`, `isCollectionMemberOf`, pela
  mesma razão.
- **P13, *inverse relationships not explicitly declared*, 21 elementos** — consequência da opção
  `createInverses: false` na transformação gUFO, não do modelo.

O *warning* final do OOPS! (`classes do not have rdf:type owl:Class`) lista os mesmos três termos da
gUFO e cai no mesmo caso.
