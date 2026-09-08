# 6. A OntoMPO Revisada

<!--
Superfície de escrita da seção 6, no orçamento que `../esqueleto.md` declara para ela.
O ticket 13 porta este arquivo para `../artigo.tex` e insere aqui o diagrama integrado.

Convenções que `tools/verification/verificar_seccoes_ontologia_avaliacao_conclusao.py` confere,
aqui e nas seções 7 a 9:

  - aspas curvas “…” marcam citação **verbatim** da fonte, e só isso;
  - «…» marcam estereótipo de OntoUML, nunca citação;
  - todo número é conferido contra o artefato que o produziu — as métricas contra
    `artifacts/ontology/owl/metricas.md`, a contagem de elementos contra o relatório do plugin;
  - nada atribui as deficiências ao MPO em linguagem natural.
-->

O artefato revisado reúne 44 classes, 35 relações e 21 generalizações, com duas partições disjuntas
e completas, e acompanha as três dimensões do modelo de referência (Figura 1). Todas as classes
chegam definidas, o que o artefato analisado não fazia: 24 definições vêm do glossário do apêndice
da conceituação, cinco foram redigidas a partir do papel que o conceito exerce nos diagramas, e
quinze nasceram com os conceitos que as rodadas introduziram.

## 6.1. As três camadas

Na camada de **agentes**, `Agent` deixou de fornecer princípio de identidade e passou a «category»
não-sortal, partida em `PhysicalAgent` e `SocialAgent`. Sob a primeira está `Person`, e sob ela o
«role» `ObservatoryUser`, de quem consulta ou alimenta o observatório; sob a segunda,
`Organization`. `StakeHolder` é «roleMixin», porque a definição de parte interessada abrange
indivíduo, grupo e organização — três princípios de identidade — e nenhum sortal único a comporta.
`System`, o ator não-humano que troca dados com o observatório, é papel de `ComputationalSystem`, o
tipo que lhe dá identidade e que a formalização deixara implícito; `ObservatoryGroup` é
«collective».

Na camada de **estruturas**, `Software` é «kind» e se especializa em três subtipos mutuamente
disjuntos: `ProjectObservatory`, o observatório propriamente dito, é «subkind»; `DataManager`
responde pela coleta, pelo tratamento, pelo armazenamento e pela disponibilização dos dados; e
`View` é a interface pela qual o observatório se apresenta. Os dois últimos são partes do
observatório por «componentOf» e se especializam nos papéis que o modelo distingue: o gerenciamento
em `Collector`, `Processor`, `Storer` e `CrudRepository`; a interface em `Disseminator`, que divulga
dados e análises, `Reporter`, que coordena a interação entre usuários, projetos e sistemas, e
`CrudView`, que dispara operações sobre o repositório. Os conteúdos são `Project`, `Knowledge` — o
que a observação produz — e `DataSource`; a infraestrutura reúne `Hardware`, `Network` e `Service`.
Sete relatores reificam os vínculos que a prosa enuncia por verbo: `ProjectDataManagement` liga um
gerenciamento ao projeto por cujos dados ele responde e `ViewProvision`, à interface que ele
disponibiliza; `SocialInteraction` e `Log` ligam um agente à interface com que ele interage e à que
registra sua ação; e `SoftwareExecution`, `ServiceProvision` e `Connection` cobrem execução, serviço
e rede.

A camada de **processos** é a que não existia. `EtlProcess` é «event» complexo com `Extract`,
`Transform` e `Load` como partes, cada uma com participantes declarados: a fonte e o papel de coleta
na extração, os de coleta e processamento na transformação, os de processamento e armazenamento na
carga. `CrudOperation` é evento partido em `CreateOperation`, `ReadOperation`, `UpdateOperation` e
`DeleteOperation`, e `Observation` é o evento pelo qual um agente observa um conteúdo divulgado, do
qual nasce o `Knowledge` correspondente. É essa camada que dá ao artefato um *quando* e um *quem*, e
dela dependem quatro das sete questões de competência (§7).

## 6.2. Do modelo em OntoUML à ontologia em OWL

A implementação não foi traduzida à mão: o modelo revisado passa pela transformação gUFO oficial
[almeida2019gufo], executada pela `ontouml-js`, e cada elemento da OWL corresponde ao elemento do
modelo que o gerou — é essa correspondência a garantia de preservação semântica que uma tradução
manual não oferece.

Sobre o gerado incidem cinco customizações, todas **aditivas por regra**: nenhuma tripla produzida
pela transformação é removida ou alterada, e a contenção do gerado dentro do customizado é conferida
a cada execução. A **C1** declara localmente os termos da gUFO que o artefato referencia — tipo,
rótulo, domínio e alcance —, para que o arquivo se sustente quando a importação não é resolvida; a
**C2** devolve a cada classe sua definição e seus rótulos preferidos; a **C3** declara disjuntos os
«kind» do modelo, consequência da semântica do estereótipo que a transformação não carrega, e os
três subtipos de `Software`; a **C4** dá nome à inversa de cada propriedade de objeto, sem o que a
proveniência teria de ser percorrida por caminho invertido a cada passo; e a **C5** acrescenta
título, licença e versão. Somam 648 triplas, publicadas à parte como o acréscimo exato.

Três decisões foram deliberadamente **não** tomadas: os identificadores não foram renomeados, porque
isso quebraria a correspondência com o modelo; os papéis irmãos não foram declarados disjuntos,
porque nada na fonte impede que um componente colete e armazene; e nenhuma axiomatização pesada foi
acrescentada, por decisão de escopo (§8).

## 6.3. Métricas do artefato

A Tabela 2 conta o que está nos arquivos, sem a gUFO importada.

**Tabela 2. Métricas dos artefatos OWL.**

| | linha de base | revisada, gerada | revisada, customizada |
|---|---|---|---|
| classes nomeadas | 32 | 44 | 44 |
| propriedades de objeto | 28 | 34 | 68 |
| propriedades de dados | 0 | 0 | 0 |
| subsunções | 60 | 86 | 86 |
| conjuntos de disjunção | 0 | 2 | 4 |
| pares de inversas nomeadas | 0 | 0 | 34 |
| axiomas | 381 | 558 | 809 |
| anotações | 60 | 78 | 475 |
| triplas | 441 | 636 | 1284 |

Duas linhas pedem leitura. As **propriedades de dados são zero** nas três colunas, e é número para
declarar, não para esconder: a conceituação especifica atributos para cada conceito, e nenhum chegou
ao diagrama (§8). O salto nas **anotações** é a C2 medida.

<!--
ticket 13: o diagrama integrado do modelo revisado entra nesta seção, regerado a partir de
`artifacts/ontology/rodada-2/ontompo-rodada-2.ontouml.json`. Os diagramas por camada vão para o
depósito se a paginação apertar. O link do depósito entra aqui e na §7 quando o DOI existir
(ticket 09, pendência humana).
-->
