# As customizações da OWL, uma a uma

A transformação gUFO oficial produz a OWL a partir do modelo OntoUML; este documento registra o que foi acrescentado por cima dela, e por quê. Gerado por `tools/generation/customizar_owl.py` — não editar à mão.

**Toda customização é aditiva.** Nenhuma tripla gerada pela transformação foi removida ou alterada, e a contenência é verificada a cada execução por `tools/verification/verificar_owl.py`. É essa a garantia de preservação semântica: ela não depende de inspeção, e sim de o artefato customizado conter o gerado inteiro. O acréscimo, isolado, está em `diff-gerado-customizado.ttl`.

| # | Customização | Triplas acrescentadas |
|---|---|---|
| C1 | Declaração local dos termos da gUFO que o artefato usa | 79 |
| C2 | Definições e rótulos preferidos, fechando B3 e B5 | 244 |
| C3 | Axiomas de disjunção, fechando B4 | 46 |
| C4 | Inversas nomeadas para cada propriedade de objeto | 272 |
| C5 | Metadados da ontologia | 7 |
| | **total** | **648** |

## C1 — Declaração local dos termos da gUFO que o artefato usa

**O que faz.** Cada IRI da gUFO referenciado pelo artefato — `gufo:Kind`, `gufo:Role`, `gufo:mediates`, `gufo:participatedIn` e os demais — recebe aqui o que a gUFO diz sobre ele: o tipo, o rótulo, o domínio e o alcance, mais `rdfs:isDefinedBy` apontando para lá. Tudo é **copiado** de `sources/gufo/gufo.ttl`, não escolhido; se um termo usado não estiver declarado lá, a geração falha.

O conjunto fecha sobre domínio e alcance: declarar `gufo:mediates` sem declarar o `gufo:Endurant` do alcance dele trocaria um elemento sem tipo por outro. São dezenove termos citados pelo artefato e três que o fecho traz.

O que **não** é copiado: a taxonomia da gUFO (`rdfs:subClassOf`) e as definições dela. O artefato importa a gUFO, não a inclui. E um `rdfs:domain` cujo valor na gUFO é uma expressão de classe anônima fica sem cópia — copiá-lo vazio seria pior que não declarar.

**Por que.** O artefato precisa se sustentar quando o `owl:imports` não é dereferenciado, e não é hipótese: é o que o OOPS! faz — a cópia submetida a ele tem o `owl:imports` removido, porque com ele o serviço devolve `unexpected_error`. Sem as declarações, treze elementos apareciam como *untyped class* (P34) e três como *untyped property* (P35) no relatório do baseline, e `evidencias-A1-A9.md` os registrou como artefato do pipeline, não como defeito do modelo. São artefato do pipeline, e é aqui que o pipeline os resolve. Como cada tripla repete o que a gUFO afirma, nada de novo é afirmado sobre o domínio.

Tem um custo, e ele está medido em `comparacao-oops.md`: um termo declarado passa a ser um elemento que o OOPS! avalia, e os termos da gUFO, avaliados fora da ontologia deles, aparecem sem anotação própria (P08) e sem ligação com o resto (P04). Fechar isso exigiria trazer a gUFO para dentro do arquivo, que é exatamente o que o `owl:imports` existe para evitar.

## C2 — Definições e rótulos preferidos, fechando B3 e B5

**O que faz.** Toda classe ganha `rdfs:comment` com sua definição em português, e `skos:prefLabel` em português e em inglês. Toda propriedade de objeto ganha `rdfs:comment` derivado do seu estereótipo. As definições estão em `tools/generation/anotacoes_ontompo.py`, cada uma com a origem declarada: `glossario` para as que vêm do Apêndice A da conceituação do MPO, `modelo` para as que foram redigidas a partir do papel do conceito nos diagramas, `revisao` para os conceitos que a análise introduziu.

**Por que.** É o achado **B3**, e ele é o mais embaraçoso dos que a reconstrução expôs: o OOPS! acusa 63 elementos sem anotação no modelo *as-is*, enquanto o Apêndice A **define 53 termos**. As definições existiam; a formalização as descartou. Uma ontologia de referência sem definição não resolve o problema que este trabalho diz resolver — duas iniciativas que se dizem aderentes ao MPO sob leituras incompatíveis não têm onde arbitrar a divergência, e a QC7 não teria o que comparar.

O rótulo preferido em inglês é também onde **B5** é endereçado: `Stakeholder` com h minúsculo, `CRUD` como acrônimo, `Data Source` separado. O **IRI não muda**, e essa é uma escolha, não um esquecimento: renomear `ontompo:StakeHolder` quebraria a correspondência entre o elemento OWL e o elemento OntoUML que o gerou, que é justamente a garantia que a transformação oficial oferece. P22 é um *pitfall* lexical, e o que se lê é o rótulo.

## C3 — Axiomas de disjunção, fechando B4

**O que faz.** Dois `owl:AllDisjointClasses`. O primeiro declara mutuamente disjuntos todos os «kind» do modelo, coletados do próprio artefato pelo tipo `gufo:Kind`. O segundo declara disjuntos `DataManager`, `View` e `ProjectObservatory`, os três subtipos de `Software`.

**Por que.** É o achado **B4**: fora das duas partições que as rodadas introduziram, o modelo não declara disjunção em lugar nenhum. A disjunção entre kinds não é uma decisão de modelagem — é consequência da UFO. Um «kind» fornece um princípio de identidade, e dois princípios de identidade distintos não podem valer para o mesmo indivíduo; declarar a disjunção só torna verificável o que a semântica do estereótipo já afirmava, e a transformação gUFO não carrega para o OWL.

A segunda disjunção fecha o que sobrou de **A9**: o `componentOf` entre `DataManager` e `ProjectObservatory` é parthood própria, que é irreflexiva, e a `ViewProvision` medeia um gerenciador e uma visão como relata distintos. O que o modelo tratava como óbvio passa a ser checável.

O que **não** foi declarado disjunto, deliberadamente: os papéis irmãos (`Collector`, `Processor`, `Storer`, `CrudRepository`; `Disseminator`, `Reporter`, `CrudView`). Nada no material de origem impede que um mesmo componente de software colete e armazene, e afirmar disjunção ali seria decidir sobre o domínio, não sobre a formalização.

## C4 — Inversas nomeadas para cada propriedade de objeto

**O que faz.** Cada propriedade `<estereótipo>_<origem>_<destino>` ganha uma inversa `<token>_<destino>_<origem>`, com domínio e alcance trocados, rótulo e definição. O token vem do estereótipo: `mediation` dá `mediatedBy`, `participation` dá `hasParticipant`, `componentOf` dá `hasComponent`, e assim por diante. O `owl:inverseOf` é declarado nos dois sentidos — logicamente redundante, e é a forma que uma ferramenta que só olhe o sujeito consegue ler.

**Por que.** A transformação roda com `createInverses: false`, e o relatório do baseline registrou os 21 elementos de P13 como artefato do pipeline — o que continua verdadeiro: não é defeito do modelo. É, porém, uma limitação do artefato OWL, e ela aparece na avaliação: a QC6 pede a cadeia de proveniência de um conteúdo divulgado até a fonte de dados, e essa cadeia se percorre no sentido contrário ao das participações geradas, que vão do endurante para o evento. Sem inversa nomeada, a consulta precisa de caminho invertido a cada passo.

O artefato gerado já usa as inversas — em `owl:onProperty [ owl:inverseOf ... ]`, dentro das restrições. Elas existiam anônimas; a customização apenas lhes dá nome.

## C5 — Metadados da ontologia

**O que faz.** Título, descrição, licença CC BY 4.0, `owl:versionInfo` e o par `vann:` de prefixo e namespace preferidos, sobre a `owl:Ontology`.

**Por que.** O depósito aberto (ticket 09) exige licença e identificação do artefato, e um arquivo OWL sem elas é um arquivo que ninguém sabe se pode reusar. **Não** há `dct:creator`: enquanto a revisão for duplamente anônima, declarar autoria dentro do artefato a quebraria — o depósito é anônimo por requisito, e o IRI de exemplo continua provisório até o ticket 09.

## O que deliberadamente não foi customizado

- **Os IRIs.** Renomear `ontompo:StakeHolder` ou `ontompo:CrudOperation` fecharia P22 no relatório, e quebraria a correspondência entre cada elemento OWL e o elemento OntoUML que o gerou — que é a garantia pela qual se usa a transformação oficial em vez de traduzir à mão. B5 é endereçado por `skos:prefLabel`.
- **Os nomes gerados das propriedades** (`mediation_Log_Agent` e afins), pela mesma razão. O sublinhado contra o CamelCase das classes é o que P22 aponta.
- **A dupla tipagem de cada classe** como `owl:Class` e `owl:NamedIndividual`. É o *punning* que a gUFO exige para que uma classe possa ser instância de `gufo:Kind`; parece redundância e não é.
- **Disjunção entre papéis irmãos**, e qualquer axioma que exigisse decidir o que o material de origem não diz.
- **Regras SWRL, cadeias de papéis e axiomatização pesada**, fora de escopo por decisão de pesquisa registrada no *spec*.

