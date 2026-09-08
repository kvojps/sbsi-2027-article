# 2. Referencial Teórico

<!--
Superfície de escrita da seção 2. Convenções em `01-introducao.md`; conferência em
`tools/verification/verificar_seccoes_introducao_metodo.py`.

Esta seção não descreve a Methontology: método é a seção 4. Ela também não antecipa nenhum achado
da seção 5 — aqui o MPO é apresentado como a fonte o descreve. -->

## 2.1. Observatórios de projetos

Não há na literatura definição única para *observatório*. Os estudos convergem em associá-lo a
“instrumentos voltados à observação e à promoção da transparência”, com atividades de coleta,
consolidação, armazenamento, análise e divulgação de dados sobre um setor ou área do conhecimento
[sakata2013construccao, tinati2015building, keever2017decada], e um observatório se materializa
como “unidade organizacional, quando o observatório se configura como um elemento formal da
organização”, como processo pelo qual um grupo executa a observação, ou como instrumento
tecnológico [vieira2020universal]. Observatórios de projetos se distinguem pelo objeto: têm como
finalidade “a disponibilização sistemática, objetiva e detalhada de informações específicas sobre
projetos” [vieira2021model].

O termo é de nicho no campo de projetos, e convém demarcá-lo frente aos vizinhos com que se
confunde. O **gerenciamento de projetos** exerce autoridade sobre o projeto — planeja, decide e age
sobre escopo, prazo, custo e riscos, respondendo por seus resultados [pmi2021pmbok,
turner2016gower] —, e um observatório não gerencia os projetos que observa nem responde por eles. O
**monitoramento e controle de projetos** compara o desempenho observado à linha de base para
provocar ação corretiva, e sua audiência é a equipe e o patrocinador; o observatório não fecha essa
malha — seu produto é informação divulgada, sua audiência é externa à execução e seu escopo é um
conjunto de projetos, não um só, e ferramentas de monitoramento governamental servem ao gestor que
executa [trois2017transparency], não a quem o fiscaliza. O **escritório
de projetos (PMO)** padroniza, apoia ou dirige a governança de projetos [pmi2021pmbok], autoridade
de que o observatório carece — mas as figuras são compatíveis: um PMO pode manter um observatório, e
um observatório pode reunir projetos de várias organizações, sem PMO algum. A categoria é geral — há
observatórios urbanos [keever2017decada], turísticos [pimentel2018observatorio] e de saúde
[yoshiura2018towards] —, e o recorte aqui é o objeto.

## 2.2. O Modelo para Observatórios de Projetos

O MPO é um modelo conceitual de referência para a concepção e a análise de observatórios de
projetos, publicado em versão preliminar [vieira2021model], avaliado e evoluído em estudos
posteriores [vieira2022evaluating, vieira2023survey] e consolidado em sua versão final
[vieira2022thesis]. Ele reúne 61 conceitos em três níveis e três dimensões, cada uma dividida em
subdimensões, e toda a descrição é textual: cada elemento tem definição em prosa e uma coluna de
relações também em prosa, redigida com verbos como *Suporta*, *Viabiliza* e *Especifica*.

A dimensão **Estruturas** “reúne os elementos relacionados à configuração estrutural e estática
dos observatórios de projetos” em três subdimensões. *Componentes* agrupa os elementos de Coleta,
Processamento e Armazenamento dos dados, o de Disseminação e o de Relacionamento, que coordena a
interação entre usuários, projetos e o observatório, mais a infraestrutura de TI que os sustenta —
Redes, Hardware, Serviços, Gerenciamento de dados e Software. *Conteúdos* abrangem os projetos, suas
temáticas, os usuários e o próprio observatório; *Características*, as nove propriedades dos dados
armazenados, entre elas interoperabilidade, acesso e segurança.

A dimensão **Processos** descreve os procedimentos executados no observatório: a subdimensão de
entrada e saída de dados detalha Coletar, Tratar, Armazenar e Disponibilizar, e a de processamento
reúne outros onze, de Transformar a Responsabilizar. Vários nomes reaparecem nas duas dimensões —
Coleta, Processamento e Armazenamento são elementos de Estruturas, e Coletar, Tratar e Armazenar,
de Processos —, cada verbo descrito como realizado por meio do componente correspondente.

A dimensão **Agentes** “trata dos participantes envolvidos nos observatórios de projetos,
considerando tanto sua natureza quanto os fatores que motivam sua interação com o observatório”: a
subdimensão *Atores* enumera as partes interessadas dos projetos, a equipe de gestão e
desenvolvimento, os usuários do observatório e os sistemas computacionais externos que trocam
dados com ele, e a subdimensão *Motivações* lista onze fatores que os levam a interagir com ele.
São esses elementos, e as relações que a prosa enuncia entre eles, que a análise da §5 discute.

## 2.3. Representation Theory

A Representation Theory, de Wand e Weber, é a teoria de Sistemas de Informação que sustenta a
análise. Seu ponto de partida é que um sistema de informação é uma representação de um domínio do
mundo real, e que a estrutura profunda do sistema determina sua capacidade de informar
[wand1995deep]. Daí o critério aplicado a gramáticas de modelagem: uma gramática descreve bem o
mundo na medida em que seus construtos correspondem, um a um, aos de uma ontologia de referência
[wand1993ontological, weber1997ontological]. Duas correspondências são examinadas — o *mapeamento
de representação*, dos construtos ontológicos aos da gramática, e o *mapeamento de interpretação*,
no percurso inverso —, e, quando alguma deixa de ser total e unívoca, a teoria nomeia quatro
deficiências:

**déficit de construto** (*construct deficit*), quando há construto ontológico que a gramática não
expressa; **sobrecarga de construto** (*construct overload*), quando um construto da gramática
representa dois ou mais construtos ontológicos e distinções do domínio colapsam num símbolo só;
**redundância de construto** (*construct redundancy*), quando dois ou mais construtos representam o
mesmo construto ontológico; e **excesso de construto** (*construct excess*), quando um construto da
gramática não corresponde a construto ontológico algum. A teoria prevê que se manifestem como
ambiguidade, perda de informação e dependência de convenções não documentadas, e há evidência
empírica de que afetam o uso efetivo de modelos por seus destinatários [recker2011ontological]. O
que a tipologia classifica é o *mapeamento* entre uma gramática e uma ontologia, e usá-la exige
declarar qual é o par sob exame — aqui, o modelo de referência em prosa e a formalização que dele se
derivou (§4).

## 2.4. UFO e OntoUML

A Unified Foundational Ontology é uma ontologia de fundamentação que fornece as categorias e as
restrições contra as quais modelos de domínio são construídos e avaliados
[guizzardi2005ontological, guizzardi2022ufo], organizada em microteorias. A **UFO-A** trata dos
endurantes e os distingue por *identidade*, *rigidez* e *dependência*; desses critérios saem os
sortais («kind», «subkind», «phase», «role»), os não-sortais («category», «mixin», «roleMixin»), os
momentos («relator», «mode») e os coletivos («collective»), além das relações de parte-todo, que
distinguem a composição entre complexos funcionais («componentOf») da adesão de um membro a um
coletivo («memberOf»). A **UFO-B** trata dos perdurantes: eventos têm partes temporais e contam com
a participação de endurantes, o que permite responder *quando* algo ocorreu e *quem* dele
participou. A **UFO-C** trata das entidades sociais e intencionais: distingue agentes de objetos não
agentivos pela posse de momentos intencionais e, entre os agentes, os físicos dos sociais.

A OntoUML dá forma a essas categorias como estereótipos de um perfil UML, impondo aos modelos as
restrições correspondentes [guizzardi2008grounding, ontouml_readthedocs]. Modelar nela obriga a
decidir, para cada classe, qual categoria ontológica ela instancia — obrigação que converte
escolhas implícitas de um texto em compromissos explícitos e verificáveis por ferramenta.
