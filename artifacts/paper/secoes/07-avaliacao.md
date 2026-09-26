# 7. Avaliação

<!--
Superfície de escrita da seção 7. Convenções em `06-ontompo-revisada.md`; conferência em
`tools/verification/verificar_seccoes_ontologia_avaliacao_conclusao.py`.

Esta seção relata **resultados**; o desenho da avaliação e a razão de cada frente são da §4, e o
verificador reprova a repetição. Todo número é conferido contra o artefato: as linhas de cada QC
contra `artifacts/ontology/consultas/qc*-resultado.csv`, os totais das ferramentas contra os
relatórios do plugin, do verificador estrutural e do OOPS!.
-->

## 7.1. As questões de competência sobre o cenário instanciado

A instanciação deriva cada indivíduo de trecho identificado da publicação do cenário
[sbsi_estendido], e declara cada acréscimo: segunda fonte, ETL temporal, componente adicional,
projetos e observações. O depósito traz o mapa trecho--indivíduo e o segundo observatório municipal,
sintético, exigido pela QC7 e limitado na §8. As sete consultas retornaram resultado não-vazio e
semanticamente correto (Tabela 3), sem interrogar a arquitetura. É evidência de **capacidade do
artefato no cenário**, não de eficácia de uma implantação organizacional.

**Tabela 3. As sete questões de competência sobre o cenário instanciado.**

| | Pergunta | Linhas | Construto de que depende |
|---|---|---|---|
| QC1 | Que interfaces um gerenciamento provê? | 8 | `ViewProvision`, de A9 |
| QC2 | Quem acessa que conteúdo de um projeto? | 4 | `StakeHolder` «roleMixin», de A6 |
| QC3 | Quem carregou uma fonte, e quando? | 4 | o ETL como evento, de A5 |
| QC4 | Que projetos ficaram sem observação? | 1 | `Observation` como evento, de B8 |
| QC5 | Que motivações movem cada tipo de ator? | 7 | a taxonomia de `Agent`, de A6 e A7 |
| QC6 | Qual a proveniência de um conteúdo? | 4 | a parthood de `EtlProcess`, de A5 |
| QC7 | Dois observatórios cobrem o mesmo? | 31 | as classes revisadas, com a C2 |

As consultas e seus resultados completos estão no Apêndice A e no depósito aberto, que inclui um
script para reexecutá-las e conferir cada resultado contra o arquivo gravado.

Depósito suplementar: [Zenodo](https://zenodo.org/records/22969990?preview=1&token=eyJhbGciOiJIUzUxMiJ9.eyJpZCI6ImRhOThkYzljLTdhNWItNDRkNC05ZmFkLTU1MzYxM2Q5ODM4YyIsImRhdGEiOnt9LCJyYW5kb20iOiJkYmU3YjYyODM4YzYwODc3OGQyMmJlYmQwMTMyMTJkYSJ9.ShohIhZWp6RjaaQjTbTIqyrm7vfUaAP9I63o0L94Xb3UejO1DYRM7EnAj-CqB4ou-C7c9z61bqWwxXsU_KB3gw).

As divergências, inclusive as que desfavorecem o artefato, foram registradas. Cada questão foi
executada contra uma expectativa escrita previamente: QC2 responde pelo relator, não por acesso amplo; QC3 identifica
papéis de software, não pessoa; QC4 depende de gerenciamentos distintos; e QC6 retorna os processos
do gerenciamento responsável, não o produtor do conteúdo. São limites do modelo revisado.

A QC7 compara cobertura conceitual em cenário controlado: dos 31 conceitos que ao menos uma das
iniciativas instancia, **23 são comuns e oito divergem**: conhecimento, grupo do observatório, interação social, observação, parte
interessada e relacionamento aparecem só no primeiro; agente social e organização, só no segundo.
Ela demonstra que a OntoMPO revisada permite medir a divergência entre os dois conjuntos
instanciados; não prova aderência de observatórios reais ao MPO nem sua frequência fora desse
cenário.

## 7.2. Conformidade à UFO, antes e depois

O verificador de conformidade sintática e semântica devolve **zero problema sobre os três modelos**,
inclusive a linha de base defeituosa; tratá-lo como efeito da revisão seria enganoso, pois suas 24
regras não alcançam meronímia, aridade de relator ou a distinção endurante/perdurante. Quatro
mutações conhecidas confirmam que acusa violações. É evidência de conformidade estrutural no alcance
das regras, não validação substantiva do artefato.

A distância medida por nove regras estruturais cai de **12 na linha de base para 3 depois da primeira
rodada e 0 depois da segunda**. Elas cobrem, entre outras restrições, membro invertido, mediação com
mínimo zero, relator acima de binário e ausência da microteoria de eventos. Sete têm a linha de base
como controle positivo; as duas que vigiam evento sem participante e participação invertida usam
mutações do revisado, acusadas nas duas.

## 7.3. *Pitfalls* na OWL, antes e depois

As execuções do detector de *pitfalls* [poveda2014oops] seguem o mesmo caminho de código. O total
cai de **105 para 56**; entre os elementos listados que pertencem à OntoMPO, cai de **60 para zero**,
ausências de anotação fechadas pela C2. Ficam fora dessa contagem a convenção de nome, deliberadamente
aberta, e a inversa declarada, de 21 para 7 propriedades da gUFO.

A C1 transforma termos da gUFO em elementos avaliados pelo serviço; fechá-los exigiria embutir a
importação. Por isso, classe não tipada sobe de 13 para 16. Ambos os artefatos OWL são
**consistentes** no perfil OWL 2 RL, e oito mutações confirmam que o raciocinador acusa, quatro nos
dois e quatro só no customizado. Junto aos *pitfalls*, isso informa a qualidade da implementação
OWL; não substitui a evidência de capacidade das questões de competência.
