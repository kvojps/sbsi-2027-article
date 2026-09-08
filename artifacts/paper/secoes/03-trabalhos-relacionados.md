# 3. Trabalhos Relacionados

<!--
Superfície de escrita da seção 3. Convenções em `01-introducao.md`; conferência em
`tools/verification/verificar_seccoes_introducao_metodo.py`.

A lacuna precisa ficar **nomeada**, e não implícita: é o que o critério de Novidade avalia. -->

Ontologias já foram empregadas em contextos de observatório, sempre como meio de integrar e
recuperar os dados do fenômeno observado. Numa delas, o casamento semântico entre pedidos de
usuários e serviços de processamento de imagens sustenta um observatório virtual multiagente
[chen2008apply]; o *Virtual Solar-Terrestrial Observatory* organiza dados de física solar sob
ontologias que ocultam a heterogeneidade das fontes [fox2009ontology]; no monitoramento ambiental,
uma ontologia modular fundamentada na Basic Formal Ontology integra desastres, sensores e medições
e habilita inferência sobre dados de precipitação [masmoudi2018ontology]; e, na saúde, um modelo
conceitual de observatórios incorpora camada semântica para estruturar o conhecimento que sustenta
políticas públicas [yoshiura2018towards]. Em todos, a ontologia é infraestrutura para os dados
observados; nenhum toma como objeto o modelo conceitual que descreve o próprio observatório.

Na direção complementar, há trabalhos que tomam modelos conceituais como objeto e os avaliam
ontologicamente. A Representation Theory foi aplicada a gramáticas de modelagem de processos para
identificar deficiências representacionais e medir seu efeito percebido sobre quem as usa
[recker2011ontological]. Na linha da UFO, a avaliação ontológica de linguagens e modelos é o
método que fundamenta a própria OntoUML [guizzardi2005ontological], e há ontologias de referência
construídas por reconciliação de um modelo de domínio preexistente com as categorias da UFO — na
cardiologia [gonccalves2011using], no direito penal [mario2020handling] e na administração pública
brasileira, em que a autorização orçamentária e a execução da despesa recebem ontologia de
referência publicada na iSys [detoni2019ontologia]. Esses trabalhos demonstram o método; nenhum
deles tem por objeto um modelo de referência do domínio de observatórios.

A lacuna que este artigo ocupa está no cruzamento das duas linhas, e tem três marcas. Primeira:
nenhum trabalho submete um modelo de referência publicado do domínio de observatórios a uma
análise ontológica crítica. Segunda: nos trabalhos que analisam modelos, o resultado é a ontologia
construída; aqui o resultado declarado são as deficiências que a formalização publicada expôs,
classificadas por uma teoria de SI, com cada achado rastreado até o ponto do texto do modelo de
referência que o permitiu — é o que converte correção de um artefato em conhecimento sobre o modelo
que o originou. Terceira: a evidência é a diferença entre um estado anterior e um posterior, ambos
publicados e reexecutáveis, e não uma afirmação sobre a qualidade do resultado final.
