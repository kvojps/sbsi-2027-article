# 15: Posicionamento da contribuição e lacuna delimitada

**What to build:** reposicionar a contribuição no corpo do artigo para que ela seja reconhecível
antes da seção de análise: uma análise ontológica rastreável de um modelo de referência para
observatórios de projetos, a OntoMPO revisada e evidência reexecutável de suas capacidades. A
novidade não pode depender da afirmação ampla de que ninguém aplicou UFO a modelos conceituais.

O artigo já tem o artefato e a cadeia de evidências; falta situá-los contra o trabalho mais próximo.
O caso de *ontological unpacking* do Viral Conceptual Model também revisa um modelo conceitual com
OntoUML em benefício da interoperabilidade. A diferença defensável está no objeto (modelo de
referência de observatórios de projetos), no traço fonte em prosa → decisão de formalização →
correção, na classificação pela Representation Theory e na comparação reexecutável antes/depois.

Também é necessário incluir a publicação consolidada do MPO, de 2025, sem substituir as fontes que
documentam suas versões e avaliações anteriores. O texto não pode sugerir que a tese de 2022 é a
última formulação do modelo quando a versão consolidada está publicada.

**Blocked by:** 14 (conformidade, anonimato e submissão), para decidir a forma de citar a
formalização analisada sem quebrar a revisão duplamente anônima.

**Status:** resolved

- [x] Entrada bibliográfica completa para a publicação consolidada do MPO (IEEE Access, 2025) conferida contra DOI e adicionada sem duplicar obra existente
- [x] Entrada bibliográfica completa para Bernasconi et al. (2022), *Semantic interoperability: ontological unpacking of a viral conceptual model*, adicionada e citada
- [x] Seção de trabalhos relacionados reescrita por eixos comparáveis: ontologias de observatórios; análise/revisão ontológica de modelos conceituais; avaliação operacional de ontologias
- [x] Quadro comparativo compacto apresenta objeto, fundamentação, rastreabilidade à fonte, artefato revisado e estratégia de avaliação dos trabalhos mais próximos
- [x] Lacuna declarada em termos positivos e delimitados, sem alegação não verificável de inexistência universal de trabalhos
- [x] Introdução lista as três contribuições: procedimento, artefato OntoMPO revisado e pacote de evidências reexecutáveis
- [x] A formalização analisada é localizável para o revisor por citação ou artefato suplementar anonimizado; ela não fica sem fonte
- [x] Texto preserva o anonimato, cita trabalhos próprios em terceira pessoa e cabe no orçamento compensando o acréscimo com cortes no referencial genérico

## Comments

O texto atual em `artifacts/paper/secoes/03-trabalhos-relacionados.md` tem uma lacuna bem enunciada,
mas compara o trabalho sobretudo com ontologias aplicadas a observatórios e deixa de fora o
comparador metodológico mais perigoso. Isso torna a frase “nenhum deles” fácil de contestar, ainda
que a contribuição de domínio continue original.

O quadro não é revisão sistemática; é instrumento de posicionamento. Deve conter poucos trabalhos,
mas distinguir explicitamente: (i) ontologia usada como infraestrutura de dados observados; (ii)
análise ontológica de um modelo ou linguagem; (iii) análise de um modelo de referência com fonte em
linguagem natural e evidência antes/depois. O trabalho deve ocupar apenas a terceira célula, sem
desqualificar as outras.

O novo material não pode ampliar o PDF. A fonte provável é a §2.4, que pode explicar somente as
distinções da UFO efetivamente mobilizadas em A1--A9; detalhes de transformação e métricas seguem
na §6 ou no depósito.

## Resolution

Implementado no manuscrito e conferido por
`tools/verification/verificar_posicionamento_lacuna.py`. A publicação consolidada do MPO foi
registrada como `farias2025conceptual` (DOI `10.1109/ACCESS.2025.3589743`) e o comparador
metodológico como `bernasconi2022semantic` (DOI `10.1186/s12859-022-05022-0`). A formalização
analisada permanece anônima e localizável como linha de base no artefato suplementar anônimo.
