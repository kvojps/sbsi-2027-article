# 01: Pacote de registro no JEMS3

**What to build:** o material que o autor precisa ter em mãos para registrar o artigo no JEMS3 até
**08/09/2026**: título em inglês, resumo estruturado em inglês e a seleção de tópicos de interesse.
Ao fim deste ticket, o autor consegue preencher o formulário do JEMS3 de ponta a ponta sem escrever
mais nada.

Atenção ao peso da decisão: depois de 14/09 **não é possível alterar título, resumo, tópicos ou
autoria** — nem retirar o artigo do processo. O que for registrado aqui vale para todo o ciclo,
incluindo o rebuttal.

**Blocked by:** None (can start immediately)

**Status:** ready-for-human

- [x] Título registrado como *OntoMPO: Ontological Analysis and Refinement of the Model for Project Observatories*
- [x] Resumo estruturado em inglês, com no máximo 300 palavras contadas
- [x] Os sete labels presentes e nomeados no texto: Research Context, Scientific and/or Practical Problem, Proposed Solution and/or Analysis, Related IS Theory, Research Method, Summary of Results, Contributions and Impact to IS area
- [x] O campo *Related IS Theory* nomeia explicitamente Representation Theory (Wand & Weber)
- [x] O campo *Proposed Solution and/or Analysis* declara a análise ontológica e o modelo revisado como contribuição, e não a formalização do MPO
- [x] O campo *Summary of Results* menciona a quantidade de deficiências representacionais encontradas
- [x] Palavras-chave em inglês definidas
- [x] Tópicos selecionados: transparência e accountability em SI; SI para gestão de dados, informação e conhecimento; paradigmas, modelagem, design, engenharia e avaliação de SI; SI organizacionais
- [x] O resumo não contém nenhuma identificação de autoria, instituição ou ferramenta que identifique
- [x] Entregue ao autor para registro no JEMS3 — a submissão em si é ação humana

## Comments

Pacote entregue em `submissao/jems3-pacote-registro.md`, com título, resumo estruturado, palavras-chave
e tópicos prontos para copiar campo a campo no formulário.

Conferência automática em `scripts/verificar_pacote_jems3.py`: título exato, sete labels presentes e na
ordem da chamada, contagem de palavras, *Related IS Theory* nomeando Representation Theory (Wand &
Weber), *Proposed Solution* declarando análise + modelo revisado e negando a formalização, *Summary of
Results* quantificando as deficiências, varredura de anonimato e os quatro tópicos.

O limite de 300 palavras é cobrado sobre a contagem mais severa plausível — hifens e barras também
separando palavras. O resumo fecha em 292 palavras na contagem simples e 297 na estrita.

Pendência humana: o registro no JEMS3 até 08/09/2026. `Status` passa a `ready-for-human` por isso.

Compromisso assumido pelo resumo: *Summary of Results* afirma nove deficiências, questões de competência
não-vazias e relatórios automáticos melhorados. Depois de 14/09 o texto não muda mais, então isso vira
critério de aceite dos tickets 07 e 08.
