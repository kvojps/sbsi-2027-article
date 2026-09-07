# OOPS!: o baseline contra a OWL revisada e customizada

Derivado das duas respostas brutas do serviço a cada execução de `tools/verification/comparar_oops.py`. O *antes* é `../baseline/relatorio-oops.xml`, sobre o modelo *as-is*; o *depois* é `relatorio-oops.xml`, sobre `ontompo.ttl`.

As duas execuções passam pelo mesmo caminho de código, `rodar_oops.py`, e submetem a mesma coisa: a ontologia em RDF/XML, sem o `owl:imports`. É essa igualdade que torna os números comparáveis.

## Contagem

| Código | *Pitfall* | Importância | antes | depois | antes (domínio) | depois (domínio) |
|---|---|---|---|---|---|---|
| `P10` | Missing disjointness | Important | 1 | — | n/d | — |
| `P11` | Missing domain or range in properties | Important | — | 1 | — | 0 |
| `P30` | Equivalent classes not explicitly declared | Important | — | 1 | — | n/d |
| `P34` | Untyped class | Important | 13 | 16 | 0 | n/d |
| `P35` | Untyped property | Important | 3 | — | 0 | — |
| `P04` | Creating unconnected ontology elements | Minor | — | 8 | — | 0 |
| `P08` | Missing annotations | Minor | 63 | 22 | 60 | 0 |
| `P13` | Inverse relationships not explicitly declared | Minor | 21 | 7 | n/d | n/d |
| `P22` | Using different naming conventions in the ontology | Minor | 1 | 1 | 0 | 0 |
| *warning* | WARNING: the following classes do not have rdf:type owl:Class or equivalent. | — | 3 | — | 0 | — |
| | **total** | | **105** | **56** | **60** | **0** |

`n/d` onde o serviço devolve a contagem sem listar os elementos, e por isso não se pode separar o que é do domínio. `—` onde o *pitfall* não aparece naquele relatório.

## Como ler cada linha

- **`P10`** (domínio) — Ausência de axiomas de disjunção — o achado **B4**, fechado pela **C3**.
- **`P11`** (gUFO) — Propriedade sem domínio ou alcance. É `gufo:isDerivedFrom`, cujo domínio, na gUFO, é uma expressão de classe anônima. A **C1** copia domínio e alcance quando são um termo nomeado; copiar uma expressão anônima seria trazer a gUFO para dentro do artefato, e deixar um `rdfs:domain` vazio seria pior que não declarar.
- **`P30`** (heurística) — Classes equivalentes não declaradas. O serviço não lista elemento afetado, e a heurística procura conceitos duplicados entre ontologias reusadas. Aparece depois de a **C1** declarar os termos da gUFO ao lado dos do domínio — é consequência de as duas passarem a conviver no mesmo arquivo, não de duplicação no modelo.
- **`P34`** (misto) — Elemento usado como classe sem declaração. No baseline eram seis termos da gUFO mais sete nós anônimos; a **C1** fecha os seis. O que sobra são só nós anônimos — as restrições de cardinalidade que a transformação gUFO emite, que não têm IRI para declarar. Cresce porque a rodada 2 tem mais restrições que o *as-is*, não porque piorou.
- **`P35`** (gUFO) — Propriedade usada sem declaração. Eram três termos da gUFO; a **C1** os declara.
- **`P04`** (gUFO) — Elementos sem ligação com o resto. São as classes da gUFO que a **C1** declara localmente: o artefato as usa e as tipa, mas a taxonomia que as conecta fica na gUFO, onde ela deve ficar. Aparece no revisado porque antes esses termos sequer estavam declarados.
- **`P08`** (misto) — Elementos sem anotação legível — o achado **B3**. A **C2** devolve definição e rótulo preferido a todas as 44 classes e 34 propriedades do domínio. O resto são os termos que a gUFO empresta, que chegam ao serviço sem a ontologia que os define.
- **`P13`** (misto) — Relação sem inversa declarada. A **C4** nomeia a inversa das 34 propriedades do domínio e declara o `owl:inverseOf` nos dois sentidos; o que sobra são as propriedades da gUFO.
- **`P22`** (domínio) — Convenção de nome — o achado **B5**. **Deliberadamente não fechado**: renomear os IRIs quebraria a correspondência entre cada elemento OWL e o elemento OntoUML que o gerou, que é a garantia pela qual se usa a transformação oficial. A **C2** endereça B5 por `skos:prefLabel`, que é o que se lê.
- ***warning*** (gUFO) — *Warning* do serviço, que repete em outra forma o que P34 diz sobre os termos da gUFO. Some junto com eles.

## O que os números dizem

Na leitura *domínio*, que é a que fala do modelo, os elementos apontados caem de **60** para **0**. Os 60 do baseline eram todos de `P08`, as definições ausentes; nenhum elemento da OntoMPO sobrou apontado.

Dois *pitfalls* ficam de fora dessa contagem porque o serviço não lista elementos para eles. Um é `P22`, o único que a customização decidiu deliberadamente não fechar, com a razão escrita em `customizacoes.md`. O outro é `P13`, que cai de 21 para 7 — e sete é exatamente o número de propriedades da gUFO que a **C1** declara no arquivo, o que sustenta a leitura de que o que sobra é delas e não do domínio. É inferência pela contagem, não elemento listado, e vale dito assim.

Na leitura *total* a queda é menor, e a diferença não é ruído: a **C1** declara no arquivo os termos que a gUFO empresta, e um termo declarado passa a ser um elemento que o OOPS! avalia — sem anotação própria (P08), sem ligação com o resto (P04), sem domínio quando o da gUFO é anônimo (P11). São termos da ontologia de fundamentação, avaliados fora dela. Trocar essa avaliação por uma melhor exigiria inlinear a gUFO no artefato, que é precisamente o que `owl:imports` existe para evitar.

O `P34` cresce de 13 para 16 pelo mesmo tipo de razão, na direção oposta: some a metade nomeada, que era da gUFO, e sobra só a anônima — as restrições de cardinalidade, que a rodada 2 tem em maior número que o *as-is* porque tem mais participações.

