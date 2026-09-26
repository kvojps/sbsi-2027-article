# 2. Referencial Teórico

<!--
Superfície de escrita da seção 2. Convenções em `01-introducao.md`; conferência em
`tools/verification/verificar_seccoes_introducao_metodo.py`.

Esta seção não descreve a Methontology: método é a seção 4. Ela também não antecipa nenhum achado
da seção 5; aqui o MPO é apresentado como a fonte o descreve. -->

## 2.1. Observatórios de projetos

Não há definição única para *observatório*, mas os estudos o associam à observação e à promoção da
transparência, por coleta, consolidação, armazenamento, análise e divulgação de dados
[sakata2013construccao, tinati2015building, keever2017decada]. Ele pode ser unidade organizacional,
processo ou instrumento tecnológico [vieira2020universal]. Observatórios de projetos divulgam
sistematicamente informações específicas sobre projetos [vieira2021model].

O termo ocupa um nicho nos projetos. O **gerenciamento de projetos** planeja, decide e responde
por escopo, prazo, custo e riscos [pmi2021pmbok, turner2016gower]; o observatório não gerencia os
projetos observados. O **monitoramento e controle de projetos** compara desempenho à linha de base
para provocar ação corretiva para equipe e patrocinador; o observatório divulga informação a uma
audência externa e cobre um conjunto de projetos [trois2017transparency]. O **escritório de projetos
(PMO)** padroniza, apoia ou dirige a governança [pmi2021pmbok], autoridade que o observatório não
detém, embora um PMO possa mantê-lo. Há observatórios urbanos [keever2017decada], turísticos
[pimentel2018observatorio] e de saúde [yoshiura2018towards]; o recorte aqui é o objeto.

## 2.2. O Modelo para Observatórios de Projetos

O MPO é um modelo conceitual de referência para a concepção e a análise de observatórios de
projetos, publicado em versão preliminar [vieira2021model], avaliado e evoluído em estudos
posteriores [vieira2022evaluating, vieira2023survey] e consolidado em sua versão final
[farias2025conceptual]. Ele reúne 61 conceitos em três níveis e três dimensões, cada uma dividida em
subdimensões e descrita em prosa.

A dimensão **Estruturas** “reúne os elementos relacionados à configuração estrutural e estática
dos observatórios de projetos” em três subdimensões. *Componentes* agrupa os elementos de Coleta,
Processamento e Armazenamento dos dados, o de Disseminação e o de Relacionamento, que coordena a
interação entre usuários, projetos e o observatório, mais a infraestrutura de TI que os sustenta:
Redes, Hardware, Serviços, Gerenciamento de dados e Software. *Conteúdos* abrangem os projetos, suas
temáticas, os usuários e o próprio observatório; *Características*, as nove propriedades dos dados
armazenados, entre elas interoperabilidade, acesso e segurança.

A dimensão **Processos** descreve os procedimentos executados no observatório: a subdimensão de
entrada e saída de dados detalha Coletar, Tratar, Armazenar e Disponibilizar, e a de processamento
reúne outros onze, de Transformar a Responsabilizar. Vários nomes reaparecem nas duas dimensões:
Coleta, Processamento e Armazenamento são elementos de Estruturas, e Coletar, Tratar e Armazenar,
de Processos; cada verbo é descrito como realizado por meio do componente correspondente.

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
[wand1993ontological, weber1997ontological]. Dois tipos de correspondência são examinados: o *mapeamento
de representação*, dos construtos ontológicos aos da gramática, e o *mapeamento de interpretação*,
no percurso inverso. Quando alguma deixa de ser total e unívoca, a teoria nomeia quatro
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
declarar qual é o par sob exame: aqui, o modelo de referência em prosa e a formalização que dele se
derivou (§4).

## 2.4. UFO e OntoUML

A Unified Foundational Ontology fornece as categorias contra as quais modelos de domínio são
avaliados [guizzardi2005ontological, guizzardi2022ufo]. Nesta análise, da **UFO-A** importam
identidade, rigidez e dependência, além da diferença entre «componentOf» e «memberOf»; da **UFO-B**,
que eventos têm partes temporais e participantes; e da **UFO-C**, que agentes físicos e sociais não
compartilham necessariamente a mesma identidade. A OntoUML torna essas distinções verificáveis
[guizzardi2008grounding, ontouml_readthedocs].
