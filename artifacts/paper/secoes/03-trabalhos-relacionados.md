# 3. Trabalhos Relacionados

<!--
Superfície de escrita da seção 3. Convenções em `01-introducao.md`; conferência em
`tools/verification/verificar_seccoes_introducao_metodo.py`.

A lacuna precisa ficar **nomeada**, e não implícita: é o que o critério de Novidade avalia. -->

O posicionamento compara papéis; não pretende inventariar toda a literatura. Ontologias em
observatórios servem como infraestrutura para dados observados, como os de serviços de imagens
[chen2008apply], dados solar-terrestres [fox2009ontology], desastres e sensores
[masmoudi2018ontology] e políticas de saúde [yoshiura2018towards]. Em outro eixo, a análise
ontológica toma modelos conceituais como objeto: a Representation Theory examina gramáticas
[recker2011ontological], e o *ontological unpacking* revisa o Viral Conceptual Model com OntoUML
para explicitar sua semântica e apoiar interoperabilidade [bernasconi2022semantic]. A reconciliação
de modelos de domínio com a UFO também foi aplicada à administração pública brasileira [detoni2019ontologia].

**Quadro comparativo dos trabalhos mais próximos.**

| Linha de trabalho | Objeto | Fundamentação | Traço à fonte | Artefato e avaliação |
| --- | --- | --- | --- | --- |
| Ontologias de observatórios | Dados observados | Ontologia de domínio | Não é o foco | Infraestrutura e inferência sobre dados |
| *Ontological unpacking* | Modelo conceitual viral | UFO e OntoUML | Modelo para semântica explicitada | OntoVCM e aplicações de interoperabilidade |
| Este trabalho | Modelo de referência de observatórios de projetos | UFO e Representation Theory | Prosa, decisão e correção | OntoMPO revisada; comparação antes/depois reexecutável |

A lacuna é positiva e delimitada: falta articular, para um modelo de referência de observatórios de
projetos, o traço da prosa até a decisão de formalização e sua correção, a classificação dos achados
pela Representation Theory e a evidência reexecutável da diferença entre linha de base e revisão.
O trabalho se restringe a essa combinação: não reduz as ontologias de observatórios à análise de
seus modelos, nem confunde o *unpacking* do VCM com uma comparação operacional antes/depois. A
contribuição consiste em uma análise rastreável, na OntoMPO revisada e no pacote de evidências que
permite reexecutar suas capacidades. A próxima seção explicita o desenho que produz os achados, o
artefato e a evidência avaliativa.
