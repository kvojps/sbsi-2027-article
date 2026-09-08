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
[sakata2013construccao, tinati2015building, keever2017decada]. Um observatório se materializa de
três formas: como “unidade organizacional, quando o observatório se configura como um elemento
formal da organização”; como mecanismo ou processo pelo qual um grupo executa as atividades de
observação; ou como instrumento tecnológico que apoia essas funções [vieira2020universal].
Observatórios de projetos compartilham esses princípios e se distinguem pelo objeto: têm como
finalidade “a disponibilização sistemática, objetiva e detalhada de informações específicas sobre
projetos”, apoiada em métricas, indicadores e mecanismos de representação e interação
[vieira2021model].

O termo é de nicho no campo de projetos, e convém demarcá-lo frente aos vizinhos com que se
confunde. O **gerenciamento de projetos** exerce autoridade sobre o projeto: planeja, decide e age
sobre escopo, prazo, custo e riscos, respondendo por seus resultados [pmi2021pmbok,
turner2016gower]. Um observatório não gerencia os projetos que observa nem responde por eles. O
**monitoramento e controle de projetos** é o grupo de processos que compara o desempenho observado
à linha de base para provocar ação corretiva, e sua audiência é a equipe e o patrocinador. O
observatório não fecha essa malha: seu produto é informação divulgada, sua audiência é externa à
execução e seu escopo é um conjunto de projetos, não um só. Ferramentas de monitoramento de
projetos governamentais servem ao gestor que executa [trois2017transparency]; o observatório serve
a quem o fiscaliza. O **escritório de projetos (PMO)** é a unidade organizacional que padroniza,
apoia ou dirige a governança de projetos, com graus variados de autoridade [pmi2021pmbok]; o
observatório carece dessa autoridade e se dirige a partes interessadas fora da organização
executora. As figuras são compatíveis: um PMO pode manter um observatório, e um observatório pode
reunir projetos de várias organizações, sem PMO algum.

A categoria é geral — há observatórios urbanos [keever2017decada], turísticos
[pimentel2018observatorio] e de saúde [yoshiura2018towards] —, e o recorte aqui é o objeto.

## 2.2. O Modelo para Observatórios de Projetos

O MPO é um modelo conceitual de referência para a concepção e a análise de observatórios de
projetos, publicado em versão preliminar [vieira2021model], avaliado e evoluído em estudos
posteriores [vieira2022evaluating, vieira2023survey] e consolidado em sua versão final
[vieira2022thesis]. Ele reúne 61 conceitos em três níveis — geral, intermediário e específico — e
três dimensões, cada uma dividida em subdimensões que agrupam os elementos. Toda a descrição é
textual: cada elemento tem definição em prosa e uma coluna de relações também em prosa, redigida
com verbos como *Suporta*, *Viabiliza* e *Especifica*.

A dimensão **Estruturas** “reúne os elementos relacionados à configuração estrutural e estática
dos observatórios de projetos” e tem três subdimensões. *Componentes* agrupa os elementos de
Coleta, Processamento e Armazenamento dos dados, o de Disseminação, que divulga análises, e o de
Relacionamento, que coordena a interação entre usuários, projetos e o observatório; a eles se
somam os elementos de infraestrutura de TI que os sustentam — Redes, Hardware, Serviços,
Gerenciamento de dados e Software. *Conteúdos* “referem-se à categorização dos projetos incluídos
no observatório e ao registro das observações realizadas pelos participantes humanos”, e abrangem
os projetos, suas temáticas, os usuários e o próprio observatório. *Características* “dizem
respeito às propriedades dos dados armazenados no observatório”: sustentabilidade, abrangência,
interoperabilidade, acesso, rede de colaboração, segurança, interatividade, formato dos dados e
dados parciais.

A dimensão **Processos** descreve os procedimentos executados no observatório. Sua primeira
subdimensão, entrada e saída de dados, “abrange as etapas de coleta, armazenamento e
compartilhamento de dados”, detalhando os processos de Coletar, Tratar, Armazenar e
Disponibilizar. A segunda, o processamento de dados, “compreende os mecanismos, ferramentas e
procedimentos empregados para analisar, compreender, avaliar e interagir com os dados dos projetos
de maneira significativa”, e reúne os processos de Transformar, Classificar, Comunicar,
Visualizar, Combinar, Refletir, Interagir, Acompanhar, Avaliar, Colaborar e Responsabilizar.
Vários nomes reaparecem nas duas dimensões: Coleta, Processamento e Armazenamento são elementos de
Estruturas, e Coletar, Tratar e Armazenar, de Processos, cada verbo descrito como realizado por
meio do componente correspondente.

A dimensão **Agentes** “trata dos participantes envolvidos nos observatórios de projetos,
considerando tanto sua natureza quanto os fatores que motivam sua interação com o observatório”. A
subdimensão *Atores* enumera as partes interessadas dos projetos, a equipe de gestão e
desenvolvimento, os usuários do observatório e os sistemas computacionais externos que trocam
dados com ele. A subdimensão *Motivações* “dizem respeito aos fatores que impulsionam os atores a
interagir com o observatório” e lista onze delas — transparência, conhecimento, tomada de decisão,
melhoria, inovação, priorização, controle, interação, disseminação, aprendizagem e engajamento —,
cada uma associada aos processos que a viabilizam. São esses elementos, e as relações que a prosa
enuncia entre eles, que a análise da §5 discute.

## 2.3. Representation Theory

A Representation Theory, de Wand e Weber, é a teoria de Sistemas de Informação que sustenta a
análise. Seu ponto de partida é que um sistema de informação é uma representação de um domínio do
mundo real, e que a estrutura profunda do sistema — o que ele afirma sobre esse domínio —
determina sua capacidade de informar [wand1995deep]. Daí o critério aplicado a gramáticas de
modelagem: uma gramática descreve bem o mundo na medida em que seus construtos correspondem, um a
um, aos de uma ontologia de referência [wand1993ontological, weber1997ontological].

Duas correspondências são examinadas: o *mapeamento de representação*, que vai dos construtos
ontológicos aos da gramática, e o *mapeamento de interpretação*, que faz o percurso inverso.
Quando alguma delas deixa de ser total e unívoca, a teoria nomeia quatro deficiências:

- **déficit de construto** (*construct deficit*): há construto ontológico que a gramática não
  expressa, e o que ele representaria fica fora do modelo ou é dito por convenção externa;
- **sobrecarga de construto** (*construct overload*): um construto da gramática representa dois ou
  mais construtos ontológicos, e distinções do domínio colapsam num símbolo só;
- **redundância de construto** (*construct redundancy*): dois ou mais construtos da gramática
  representam o mesmo construto ontológico, e quem lê decide se a diferença significa algo;
- **excesso de construto** (*construct excess*): um construto da gramática não corresponde a
  construto ontológico algum, e a ontologia de referência não fixa seu significado.

A teoria prevê que se manifestem como ambiguidade, perda de informação e dependência de convenções
não documentadas, e há evidência empírica de que afetam o uso efetivo de modelos por seus
destinatários [recker2011ontological]. O que a tipologia classifica é o *mapeamento* entre uma
gramática e uma ontologia, e usá-la exige declarar qual é o par sob exame — aqui, o modelo de
referência em prosa e a formalização que dele se derivou (§4). O ganho: os achados deixam de ser
preferência de quem analisa e ficam comparáveis a outros estudos.

## 2.4. UFO e OntoUML

A Unified Foundational Ontology é uma ontologia de fundamentação que fornece as categorias e as
restrições contra as quais modelos de domínio são construídos e avaliados
[guizzardi2005ontological, guizzardi2022ufo], organizada em microteorias. A **UFO-A** trata dos
endurantes, entidades que persistem no tempo mantendo sua identidade, e as distingue por três
critérios: *identidade* — quem fornece o princípio pelo qual um indivíduo é o mesmo ao longo do
tempo —, *rigidez* e *dependência*. Desses critérios saem os sortais («kind», «subkind», «phase»,
«role»), os não-sortais («category», «mixin», «roleMixin»), os momentos («relator», «mode») e os
coletivos («collective»), além das relações de parte-todo, que distinguem a composição entre
complexos funcionais («componentOf») da adesão de um membro a um coletivo («memberOf»). A
**UFO-B** trata dos perdurantes: eventos têm partes temporais e contam com a participação de
endurantes, o que permite responder *quando* algo ocorreu e *quem* dele participou. A **UFO-C**
trata das entidades sociais e intencionais: distingue agentes de objetos não agentivos pela posse
de momentos intencionais — intenções, crenças, compromissos — e, entre os agentes, os físicos dos
sociais.

A OntoUML dá forma a essas categorias como estereótipos de um perfil UML, impondo aos modelos as
restrições correspondentes [guizzardi2008grounding, ontouml_readthedocs]. Modelar nela obriga a
decidir, para cada classe, qual categoria ontológica ela instancia — obrigação que converte
escolhas implícitas de um texto em compromissos explícitos e verificáveis por ferramenta, e que a
torna adequada a domínios sociotécnicos.
