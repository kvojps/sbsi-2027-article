# Métricas dos artefatos OWL

Derivadas dos arquivos a cada execução de `tools/generation/customizar_owl.py`. Contam o que está **no arquivo**: a gUFO importada não entra, porque o que está sob avaliação é a ontologia de domínio.

| | baseline | rodada 2, gerada | rodada 2, customizada |
|---|---|---|---|
| classes nomeadas | 32 | 44 | 44 |
| expressões de classe anônimas | 28 | 42 | 42 |
| propriedades de objeto | 28 | 34 | 68 |
| propriedades de dados | 0 | 0 | 0 |
| subsunções (`rdfs:subClassOf`) | 60 | 86 | 86 |
| equivalências | 0 | 2 | 2 |
| conjuntos de disjunção | 0 | 2 | 4 |
| pares de inversas nomeadas | 0 | 0 | 34 |
| axiomas | 381 | 558 | 809 |
| anotações | 60 | 78 | 475 |
| triplas | 441 | 636 | 1284 |

## Como se conta

- **Classes nomeadas** e **propriedades**: sujeitos com o `rdf:type` correspondente e IRI no namespace da OntoMPO. Os termos da gUFO que a C1 declara localmente ficam de fora — são dela, não do domínio.
- **Propriedades de dados: zero**, nos três artefatos, e é um número a declarar, não a esconder. O modelo publicado não tem nenhum atributo, embora o Apêndice A da conceituação especifique atributos de classe e de instância para cada conceito — é o achado **B6**. A camada de atributos é do ticket 07, onde a instanciação a exige: a QC3 pergunta *quando* uma carga ocorreu e a QC6 pede a cadeia de proveniência.
- **Axiomas** são as triplas cujo predicado não é de anotação; **anotações**, as demais. A soma das duas é o total de triplas. Não é a contagem de axiomas lógicos da OWL 2, que agruparia várias triplas em um axioma só — é a contagem que se pode derivar do arquivo sem um raciocinador, e ela é comparável entre as colunas porque é a mesma regra nas três.

