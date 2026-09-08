# 1. Introdução

<!--
Superfície de escrita da seção 1, no orçamento que `../esqueleto.md` declara para ela.
O ticket 13 porta este arquivo para `../artigo.tex`.

Convenções que `tools/verification/verificar_seccoes_introducao_metodo.py` confere, aqui e nas
seções 2 a 4:

  - aspas curvas “…” marcam citação **verbatim** da fonte, e só isso. Cada ocorrência é
    procurada, com espaços normalizados, em `sources/dissertation/`;
  - nenhuma citação curva se repete entre seções, e nenhuma frase longa reaparece em duas
    delas: a redundância entre seções foi crítica explícita de um parecer;
  - Methontology é assunto exclusivo da seção 4; a seção 2 não a descreve;
  - texto impessoal, sem primeira pessoa e sem menção identificadora.
-->

Organizações realizam sua estratégia por projetos, e a exigência de dar visibilidade a eles há
muito deixou de ser interna: a Lei de Acesso à Informação estabeleceu o acesso à informação
pública como regra, e não como exceção [L12527], e a literatura de gerenciamento passou a tratar a
transparência como atributo do próprio desenvolvimento do projeto [betta2018transparency]. Atender
a essa exigência mobiliza **pessoas** — as partes interessadas dentro e fora da organização
executora —, **processos e procedimentos** — as rotinas de coleta, tratamento e divulgação da
informação sobre os projetos — e **tecnologias** — a infraestrutura que sustenta essas rotinas. O
observatório de projetos é a estrutura sociotécnica que articula os três: uma entidade dedicada à
observação contínua de um conjunto de projetos, que centraliza, analisa e divulga informação sobre
eles [vieira2021model].

Por que estruturas assim existem é o que a Organizational Information Processing Theory explica
[galbraith1973designing, galbraith1974organization]: quanto maior a incerteza de uma tarefa, maior
a informação que precisa ser processada entre quem a executa e quem decide sobre ela, e a
organização responde ampliando sua capacidade de processamento. Um observatório de projetos é um
mecanismo desse tipo, com uma particularidade: a capacidade que ele amplia não é a de quem
gerencia os projetos, e sim a de quem precisa acompanhá-los de fora — financiadores, órgãos de
controle e sociedade. É essa assimetria que o sustenta como categoria própria (§2.1).

O domínio de aplicação deste artigo são os observatórios de projetos em organizações que prestam
contas a terceiros — universidades públicas, agências de fomento e órgãos executores de políticas
—, e seu modelo de referência é o Modelo para Observatórios de Projetos (MPO) [vieira2021model,
vieira2022thesis], que organiza 61 conceitos “distribuídos em três níveis hierárquicos” e em três
dimensões. O problema organizacional está em como esse modelo é descrito. Sendo prosa, o MPO não
fixa a interpretação de seus conceitos: uma iniciativa que se declara aderente a ele não tem como
demonstrar em que a aderência consiste, duas que usam o mesmo termo podem estar nomeando entidades
distintas, e a prestação de contas — que exige percorrer o caminho do conteúdo divulgado até a
fonte que o originou — não encontra no modelo o encadeamento que permitiria auditá-la.

A tese defendida aqui é que esses efeitos não são acidente de um modelo particular: **modelos
conceituais de referência descritos em linguagem natural carregam deficiências representacionais
sistemáticas e invisíveis a quem os aplica**. Invisíveis porque o texto não é contraditório: é
subdeterminado, e a lacuna só aparece quando alguém precisa decidir o que cada conceito é.
Submeter o MPO a uma análise ontológica fundamentada na Unified Foundational Ontology (UFO) tornou
nove dessas lacunas observáveis, cada uma classificada pela tipologia da Representation Theory
[wand1993ontological], corrigida com justificativa ontológica e rastreada até o ponto do modelo
que a permitiu.

A contribuição declarada, portanto, não é formalizar o MPO — uma formalização já existe, publicada
por terceiros, e é ela o objeto analisado. A contribuição é a **análise ontológica** e o **modelo
revisado** que dela resultou, com um procedimento reusável para auditar modelos de referência
descritos em prosa e a evidência antes/depois que separa o que a análise afirma do que as
ferramentas atestam. Esse resultado responde ao Desafio 3 do II GranDSI-Br, *Eco(Sistemas²) de
Informação* [araujo2025grandsi]: observatórios são ecossistemas de informação que só se integram
se os conceitos que trocam significarem o mesmo dos dois lados, e é essa interoperabilidade
semântica que uma especificação verificável do modelo de referência torna possível.
Secundariamente, alinha-se ao Desafio 2, *SI Inteligentes sob a Perspectiva Sociotécnica*, ao
explicitar a camada de agentes que a formalização tratava como tipo único.

O artigo segue assim. A §2 apresenta os observatórios de projetos, o MPO, a Representation Theory
e a UFO; a §3 situa o trabalho frente à literatura e a §4 descreve o desenho de pesquisa. A §5
apresenta a análise ontológica e as nove deficiências, com seus traços e correções; a §6, a OntoMPO
revisada, e a §7, sua avaliação. A §8 discute lições e limitações e a §9 conclui.
