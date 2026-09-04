# 0002 — A customização da OWL é aditiva

Dois pareceres do ONTOBRAS perguntaram a mesma coisa por caminhos diferentes: como se garante que a
semântica do OntoUML foi preservada no OWL, e o que exatamente os autores acrescentaram ao que a
ferramenta já gera. Ambas ficam sem resposta enquanto a customização for descrita em prosa. A decisão
do ticket 06 é trocar a prosa por um invariante:

> **Toda customização é aditiva.** Nenhuma tripla produzida pela transformação gUFO é removida ou
> alterada. O artefato customizado é o gerado mais um acréscimo, e o acréscimo é gravado inteiro, em
> `artifacts/ontology/owl/diff-gerado-customizado.ttl`.

Sob esse invariante, a preservação semântica deixa de ser afirmação e vira contenência de grafos:
`tools/verification/verificar_owl.py` confere que toda tripla do gerado está no customizado, e que
gerado mais acréscimo dá exatamente o customizado. Um terceiro não precisa acreditar; roda.

## As três faces da decisão

**O preço é B5, e ele foi pago.** O achado de convenção de nome — `StakeHolder` com H maiúsculo,
`Crud*` contra o acrônimo `CRUD` — só se fecharia renomeando IRIs, que é subtração. A saída é
endereçá-lo por `skos:prefLabel`, deixando o IRI como a transformação o gerou. Não é rodeio: renomear
quebraria a correspondência entre cada elemento OWL e o elemento OntoUML que o originou, que é a
única razão de usar a transformação oficial em vez de traduzir à mão. O *pitfall* P22 continua no
relatório do OOPS!, com a razão escrita ao lado.

**A gUFO entra por declaração, não por inclusão.** A cópia submetida ao OOPS! tem o `owl:imports`
removido — com ele o serviço devolve `unexpected_error` —, então os termos que a gUFO empresta
chegam lá sem a ontologia que os define. A customização C1 re-declara cada termo usado, copiando de
`sources/gufo/gufo.ttl` o tipo, o rótulo, o domínio e o alcance. **Não** copia a taxonomia nem as
definições: o artefato importa a gUFO, não a inclui. A consequência é visível no relatório e está
registrada — termos declarados passam a ser elementos que o OOPS! avalia fora da ontologia deles, e
aparecem em P04, P08 e P11. Por isso a comparação vem em duas leituras, *total* e *domínio*.

**O raciocinador é OWL 2 RL, por falta de Java.** `owlrl` sobre a rdflib é o único disponível sem
máquina virtual Java; HermiT e Pellet, que a `owlready2` empacota, exigem uma. A lacuna é real e está
escrita no relatório: as 31 restrições de cardinalidade qualificada que a transformação emite ficam
fora do perfil. Trocar por um raciocinador DL é a melhoria óbvia se o ambiente ganhar Java.

## Consequências

- `sources/gufo/gufo.ttl` é insumo novo, com SHA-256 registrado no `README.md` de lá e conferido pelo
  verificador. Dereferenciar o IRI a cada execução tornaria a verificação dependente de rede.
- Uma customização nova entra como um verbete em `CUSTOMIZACOES`, em
  `tools/generation/customizar_owl.py`, com a função que a aplica e as duas justificativas que vão
  para `customizacoes.md`. Customização sem justificativa reprova.
- `tools/generation/rdf_deterministico.py` passou a ordenar o percurso do grafo e a desempatar nós
  anônimos de conteúdo idêntico pelo contexto. Sem as duas, a serialização RDF/XML mudava de ordem a
  cada execução e as listas das partições colidiam. Os dois arquivos RDF/XML do baseline foram
  regravados na ordem estável; são **isomorfos** aos anteriores, e o modelo não foi tocado.
- O OOPS! passa a rodar sobre dois artefatos, pelo mesmo caminho de código. A comparação entre eles é
  o antes/depois de *pitfalls* que o ticket 03 deixou marcado para cá.
