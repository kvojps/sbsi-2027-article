# Diff: a OWL gerada contra a OWL customizada

Derivado dos dois grafos a cada execução de `tools/generation/customizar_owl.py`. A leitura de cada acréscimo — o que é e por que existe — está em `customizacoes.md`; as triplas cruas, em `diff-gerado-customizado.ttl`.

## Contagens

| | gerada | customizada |
|---|---|---|
| triplas | 636 | 1284 |
| anotações | 78 | 475 |
| axiomas | 558 | 809 |

Removidas: **0**. Alteradas: **0**. Acrescentadas: **648**.

## C1 — Declaração local dos termos da gUFO que o artefato usa (79)

| sujeito | predicado | objeto |
|---|---|---|
| `gufo:Category` | `rdf:type` | `owl:Class` |
| `gufo:Category` | `rdfs:label` | `"Category"@en` |
| `gufo:Category` | `rdfs:isDefinedBy` | `<http://purl.org/nemo/gufo>` |
| `gufo:Collection` | `rdf:type` | `owl:Class` |
| `gufo:Collection` | `rdfs:label` | `"Collection"@en` |
| `gufo:Collection` | `rdfs:isDefinedBy` | `<http://purl.org/nemo/gufo>` |
| `gufo:Endurant` | `rdf:type` | `owl:Class` |
| `gufo:Endurant` | `rdfs:label` | `"Endurant"@en` |
| `gufo:Endurant` | `rdfs:isDefinedBy` | `<http://purl.org/nemo/gufo>` |
| `gufo:EndurantType` | `rdf:type` | `owl:Class` |
| `gufo:EndurantType` | `rdfs:label` | `"EndurantType"@en` |
| `gufo:EndurantType` | `rdfs:isDefinedBy` | `<http://purl.org/nemo/gufo>` |
| `gufo:Event` | `rdf:type` | `owl:Class` |
| `gufo:Event` | `rdfs:label` | `"Event"@en` |
| `gufo:Event` | `rdfs:isDefinedBy` | `<http://purl.org/nemo/gufo>` |
| `gufo:EventType` | `rdf:type` | `owl:Class` |
| `gufo:EventType` | `rdfs:label` | `"EventType"@en` |
| `gufo:EventType` | `rdfs:isDefinedBy` | `<http://purl.org/nemo/gufo>` |
| `gufo:FunctionalComplex` | `rdf:type` | `owl:Class` |
| `gufo:FunctionalComplex` | `rdfs:label` | `"FunctionalComplex"@en` |
| `gufo:FunctionalComplex` | `rdfs:isDefinedBy` | `<http://purl.org/nemo/gufo>` |
| `gufo:Kind` | `rdf:type` | `owl:Class` |
| `gufo:Kind` | `rdfs:label` | `"Kind"@en` |
| `gufo:Kind` | `rdfs:isDefinedBy` | `<http://purl.org/nemo/gufo>` |
| `gufo:MaterialRelationshipType` | `rdf:type` | `owl:Class` |
| `gufo:MaterialRelationshipType` | `rdfs:label` | `"MaterialRelationshipType"@en` |
| `gufo:MaterialRelationshipType` | `rdfs:isDefinedBy` | `<http://purl.org/nemo/gufo>` |
| `gufo:Object` | `rdf:type` | `owl:Class` |
| `gufo:Object` | `rdfs:label` | `"Object"@en` |
| `gufo:Object` | `rdfs:isDefinedBy` | `<http://purl.org/nemo/gufo>` |
| `gufo:Relator` | `rdf:type` | `owl:Class` |
| `gufo:Relator` | `rdfs:label` | `"Relator"@en` |
| `gufo:Relator` | `rdfs:isDefinedBy` | `<http://purl.org/nemo/gufo>` |
| `gufo:Role` | `rdf:type` | `owl:Class` |
| `gufo:Role` | `rdfs:label` | `"Role"@en` |
| `gufo:Role` | `rdfs:isDefinedBy` | `<http://purl.org/nemo/gufo>` |
| `gufo:RoleMixin` | `rdf:type` | `owl:Class` |
| `gufo:RoleMixin` | `rdfs:label` | `"RoleMixin"@en` |
| `gufo:RoleMixin` | `rdfs:isDefinedBy` | `<http://purl.org/nemo/gufo>` |
| `gufo:SubKind` | `rdf:type` | `owl:Class` |
| `gufo:SubKind` | `rdfs:label` | `"SubKind"@en` |
| `gufo:SubKind` | `rdfs:isDefinedBy` | `<http://purl.org/nemo/gufo>` |
| `gufo:VariableCollection` | `rdf:type` | `owl:Class` |
| `gufo:VariableCollection` | `rdfs:label` | `"VariableCollection"@en` |
| `gufo:VariableCollection` | `rdfs:isDefinedBy` | `<http://purl.org/nemo/gufo>` |
| `gufo:isCollectionMemberOf` | `rdf:type` | `owl:ObjectProperty` |
| `gufo:isCollectionMemberOf` | `rdfs:label` | `"isCollectionMemberOf"@en` |
| `gufo:isCollectionMemberOf` | `rdfs:domain` | `gufo:Object` |
| `gufo:isCollectionMemberOf` | `rdfs:range` | `gufo:Collection` |
| `gufo:isCollectionMemberOf` | `rdfs:isDefinedBy` | `<http://purl.org/nemo/gufo>` |
| `gufo:isComponentOf` | `rdf:type` | `owl:ObjectProperty` |
| `gufo:isComponentOf` | `rdfs:label` | `"isComponentOf"@en` |
| `gufo:isComponentOf` | `rdfs:domain` | `gufo:Object` |
| `gufo:isComponentOf` | `rdfs:range` | `gufo:FunctionalComplex` |
| `gufo:isComponentOf` | `rdfs:isDefinedBy` | `<http://purl.org/nemo/gufo>` |
| `gufo:isDerivedFrom` | `rdf:type` | `owl:ObjectProperty` |
| `gufo:isDerivedFrom` | `rdfs:label` | `"isDerivedFrom"@en` |
| `gufo:isDerivedFrom` | `rdfs:range` | `gufo:EndurantType` |
| `gufo:isDerivedFrom` | `rdfs:isDefinedBy` | `<http://purl.org/nemo/gufo>` |
| `gufo:isEventProperPartOf` | `rdf:type` | `owl:ObjectProperty` |
| `gufo:isEventProperPartOf` | `rdfs:label` | `"isEventProperPartOf"@en` |
| `gufo:isEventProperPartOf` | `rdfs:domain` | `gufo:Event` |
| `gufo:isEventProperPartOf` | `rdfs:range` | `gufo:Event` |
| `gufo:isEventProperPartOf` | `rdfs:isDefinedBy` | `<http://purl.org/nemo/gufo>` |
| `gufo:mediates` | `rdf:type` | `owl:ObjectProperty` |
| `gufo:mediates` | `rdfs:label` | `"mediates"@en` |
| `gufo:mediates` | `rdfs:domain` | `gufo:Relator` |
| `gufo:mediates` | `rdfs:range` | `gufo:Endurant` |
| `gufo:mediates` | `rdfs:isDefinedBy` | `<http://purl.org/nemo/gufo>` |
| `gufo:participatedIn` | `rdf:type` | `owl:ObjectProperty` |
| `gufo:participatedIn` | `rdfs:label` | `"participatedIn"@en` |
| `gufo:participatedIn` | `rdfs:domain` | `gufo:Object` |
| `gufo:participatedIn` | `rdfs:range` | `gufo:Event` |
| `gufo:participatedIn` | `rdfs:isDefinedBy` | `<http://purl.org/nemo/gufo>` |
| `gufo:wasCreatedIn` | `rdf:type` | `owl:ObjectProperty` |
| `gufo:wasCreatedIn` | `rdfs:label` | `"wasCreatedIn"@en` |
| `gufo:wasCreatedIn` | `rdfs:domain` | `gufo:Endurant` |
| `gufo:wasCreatedIn` | `rdfs:range` | `gufo:Event` |
| `gufo:wasCreatedIn` | `rdfs:isDefinedBy` | `<http://purl.org/nemo/gufo>` |

## C2 — Definições e rótulos preferidos, fechando B3 e B5 (244)

| sujeito | predicado | objeto |
|---|---|---|
| `ontompo:Agent` | `rdfs:comment` | `"Categoria não-sortal que reúne tudo o que porta intenções e age no contexto de um observatório de projetos, seja um agente físico ou um agente social."@pt-BR` |
| `ontompo:Agent` | `skos:prefLabel` | `"Agente"@pt-BR` |
| `ontompo:Agent` | `skos:prefLabel` | `"Agent"@en` |
| `ontompo:Agent` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:Collector` | `rdfs:comment` | `"Papel do gerenciamento de dados quando captura, de forma interna ou externa, os dados dos projetos observados."@pt-BR` |
| `ontompo:Collector` | `skos:prefLabel` | `"Coleta"@pt-BR` |
| `ontompo:Collector` | `skos:prefLabel` | `"Collector"@en` |
| `ontompo:Collector` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:ComputationalSystem` | `rdfs:comment` | `"Sistema computacional, tomado como o tipo que fornece princípio de identidade aos sistemas que interagem com o observatório."@pt-BR` |
| `ontompo:ComputationalSystem` | `skos:prefLabel` | `"Sistema computacional"@pt-BR` |
| `ontompo:ComputationalSystem` | `skos:prefLabel` | `"Computational System"@en` |
| `ontompo:ComputationalSystem` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:Connection` | `rdfs:comment` | `"Vínculo pelo qual um hardware do observatório se liga a uma rede."@pt-BR` |
| `ontompo:Connection` | `skos:prefLabel` | `"Conexão"@pt-BR` |
| `ontompo:Connection` | `skos:prefLabel` | `"Connection"@en` |
| `ontompo:Connection` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:CreateOperation` | `rdfs:comment` | `"Operação CRUD que faz passar a existir um registro que não existia."@pt-BR` |
| `ontompo:CreateOperation` | `skos:prefLabel` | `"Operação de criação"@pt-BR` |
| `ontompo:CreateOperation` | `skos:prefLabel` | `"CRUD Create Operation"@en` |
| `ontompo:CreateOperation` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:CrudOperation` | `rdfs:comment` | `"Evento de operação sobre um repositório de dados do observatório."@pt-BR` |
| `ontompo:CrudOperation` | `skos:prefLabel` | `"Operação CRUD"@pt-BR` |
| `ontompo:CrudOperation` | `skos:prefLabel` | `"CRUD Operation"@en` |
| `ontompo:CrudOperation` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:CrudRepository` | `rdfs:comment` | `"Papel do gerenciamento de dados quando ele expõe um repositório sobre o qual operações CRUD são executadas."@pt-BR` |
| `ontompo:CrudRepository` | `skos:prefLabel` | `"Repositório CRUD"@pt-BR` |
| `ontompo:CrudRepository` | `skos:prefLabel` | `"CRUD Repository"@en` |
| `ontompo:CrudRepository` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:CrudView` | `rdfs:comment` | `"Papel da visão quando é por ela que uma operação CRUD sobre o repositório é disparada."@pt-BR` |
| `ontompo:CrudView` | `skos:prefLabel` | `"Visão CRUD"@pt-BR` |
| `ontompo:CrudView` | `skos:prefLabel` | `"CRUD View"@en` |
| `ontompo:CrudView` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:DataManager` | `rdfs:comment` | `"Ferramentas de software necessárias para que o observatório organize, gerencie e processe os dados relacionados aos projetos observados."@pt-BR` |
| `ontompo:DataManager` | `skos:prefLabel` | `"Gerenciamento de dados"@pt-BR` |
| `ontompo:DataManager` | `skos:prefLabel` | `"Data Manager"@en` |
| `ontompo:DataManager` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:DataSource` | `rdfs:comment` | `"Origem principal dos dados coletados: sistemas internos, partes interessadas externas, bases de dados abertas ou sensores."@pt-BR` |
| `ontompo:DataSource` | `skos:prefLabel` | `"Fonte de dados"@pt-BR` |
| `ontompo:DataSource` | `skos:prefLabel` | `"Data Source"@en` |
| `ontompo:DataSource` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:DeleteOperation` | `rdfs:comment` | `"Operação CRUD que faz deixar de existir um registro."@pt-BR` |
| `ontompo:DeleteOperation` | `skos:prefLabel` | `"Operação de exclusão"@pt-BR` |
| `ontompo:DeleteOperation` | `skos:prefLabel` | `"CRUD Delete Operation"@en` |
| `ontompo:DeleteOperation` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:Disseminator` | `rdfs:comment` | `"Papel do software quando divulga análises e reflexões sobre os dados dos projetos observados, segundo as diretrizes de acesso e segurança do observatório."@pt-BR` |
| `ontompo:Disseminator` | `skos:prefLabel` | `"Disseminação"@pt-BR` |
| `ontompo:Disseminator` | `skos:prefLabel` | `"Disseminator"@en` |
| `ontompo:Disseminator` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:EtlProcess` | `rdfs:comment` | `"Evento complexo que leva os dados da fonte até o repositório do observatório, e do qual a extração, a transformação e a carga são partes próprias."@pt-BR` |
| `ontompo:EtlProcess` | `skos:prefLabel` | `"Processo de ETL"@pt-BR` |
| `ontompo:EtlProcess` | `skos:prefLabel` | `"ETL Process"@en` |
| `ontompo:EtlProcess` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:Extract` | `rdfs:comment` | `"Evento de identificação e coleta dos dados e informações relevantes sobre os projetos observados e suas temáticas."@pt-BR` |
| `ontompo:Extract` | `skos:prefLabel` | `"Extração"@pt-BR` |
| `ontompo:Extract` | `skos:prefLabel` | `"Extract"@en` |
| `ontompo:Extract` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:Hardware` | `rdfs:comment` | `"Equipamento físico de tecnologia da informação utilizado nos processos executados pelos observatórios de projetos."@pt-BR` |
| `ontompo:Hardware` | `skos:prefLabel` | `"Hardware"@pt-BR` |
| `ontompo:Hardware` | `skos:prefLabel` | `"Hardware"@en` |
| `ontompo:Hardware` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:Knowledge` | `rdfs:comment` | `"Conhecimento sobre os projetos observados, adquirido e construído a partir do conteúdo que o observatório disponibiliza."@pt-BR` |
| `ontompo:Knowledge` | `skos:prefLabel` | `"Conhecimento"@pt-BR` |
| `ontompo:Knowledge` | `skos:prefLabel` | `"Knowledge"@en` |
| `ontompo:Knowledge` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:Load` | `rdfs:comment` | `"Evento de armazenamento, em um repositório, dos dados coletados e transformados sobre os projetos observados."@pt-BR` |
| `ontompo:Load` | `skos:prefLabel` | `"Carga"@pt-BR` |
| `ontompo:Load` | `skos:prefLabel` | `"Load"@en` |
| `ontompo:Load` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:Log` | `rdfs:comment` | `"Registro que responsabiliza um agente por suas ações no contexto do observatório, e que sustenta a auditoria dessas ações."@pt-BR` |
| `ontompo:Log` | `skos:prefLabel` | `"Registro de auditoria"@pt-BR` |
| `ontompo:Log` | `skos:prefLabel` | `"Log"@en` |
| `ontompo:Log` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:Network` | `rdfs:comment` | `"Componentes que possibilitam a comunicação, o gerenciamento e as operações de rede entre um observatório de projetos e os sistemas internos e externos das organizações."@pt-BR` |
| `ontompo:Network` | `skos:prefLabel` | `"Rede"@pt-BR` |
| `ontompo:Network` | `skos:prefLabel` | `"Network"@en` |
| `ontompo:Network` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:Observation` | `rdfs:comment` | `"Evento em que um agente observa o conteúdo divulgado pelo observatório e no qual passa a existir conhecimento sobre os projetos observados."@pt-BR` |
| `ontompo:Observation` | `skos:prefLabel` | `"Observação"@pt-BR` |
| `ontompo:Observation` | `skos:prefLabel` | `"Observation"@en` |
| `ontompo:Observation` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:ObservatoryGroup` | `rdfs:comment` | `"Coletivo de agentes reunidos em torno de um observatório de projetos: a equipe responsável pelo gerenciamento, manutenção e operação do observatório, seus usuários e os sistemas que com ele trocam."@pt-BR` |
| `ontompo:ObservatoryGroup` | `skos:prefLabel` | `"Grupo do observatório"@pt-BR` |
| `ontompo:ObservatoryGroup` | `skos:prefLabel` | `"Observatory Group"@en` |
| `ontompo:ObservatoryGroup` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:ObservatoryUser` | `rdfs:comment` | `"Ator humano que desfruta das utilidades que um observatório de projetos proporciona."@pt-BR` |
| `ontompo:ObservatoryUser` | `skos:prefLabel` | `"Usuário do observatório"@pt-BR` |
| `ontompo:ObservatoryUser` | `skos:prefLabel` | `"Observatory User"@en` |
| `ontompo:ObservatoryUser` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:Organization` | `rdfs:comment` | `"Instituição à qual uma parte interessada pertence, e que pode ela própria afetar ou ser afetada pelos projetos observados."@pt-BR` |
| `ontompo:Organization` | `skos:prefLabel` | `"Organização"@pt-BR` |
| `ontompo:Organization` | `skos:prefLabel` | `"Organization"@en` |
| `ontompo:Organization` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:Person` | `rdfs:comment` | `"Ser humano que participa de um observatório de projetos, em qualquer papel."@pt-BR` |
| `ontompo:Person` | `skos:prefLabel` | `"Pessoa"@pt-BR` |
| `ontompo:Person` | `skos:prefLabel` | `"Person"@en` |
| `ontompo:Person` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:PhysicalAgent` | `rdfs:comment` | `"Agente cuja existência é a de um objeto físico concreto — no domínio do observatório, o indivíduo humano."@pt-BR` |
| `ontompo:PhysicalAgent` | `skos:prefLabel` | `"Agente físico"@pt-BR` |
| `ontompo:PhysicalAgent` | `skos:prefLabel` | `"Physical Agent"@en` |
| `ontompo:PhysicalAgent` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:Processor` | `rdfs:comment` | `"Papel do gerenciamento de dados quando trata e converte os dados brutos dos projetos em uma forma mais significativa."@pt-BR` |
| `ontompo:Processor` | `skos:prefLabel` | `"Processamento"@pt-BR` |
| `ontompo:Processor` | `skos:prefLabel` | `"Processor"@en` |
| `ontompo:Processor` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:Project` | `rdfs:comment` | `"Projeto observado: aquele sobre o qual o observatório reúne e divulga dados, informação e conhecimento, e que ele não gerencia."@pt-BR` |
| `ontompo:Project` | `skos:prefLabel` | `"Projeto"@pt-BR` |
| `ontompo:Project` | `skos:prefLabel` | `"Project"@en` |
| `ontompo:Project` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:ProjectDataManagement` | `rdfs:comment` | `"Vínculo pelo qual um gerenciamento de dados responde pelos dados de um projeto observado."@pt-BR` |
| `ontompo:ProjectDataManagement` | `skos:prefLabel` | `"Gerência de dados de projeto"@pt-BR` |
| `ontompo:ProjectDataManagement` | `skos:prefLabel` | `"Project Data Management"@en` |
| `ontompo:ProjectDataManagement` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:ProjectObservatory` | `rdfs:comment` | `"Observatório de projetos: o software que coleta, integra e divulga informação sobre um conjunto de projetos observados, para dar transparência e prestação de contas a partes interessadas externas."@pt-BR` |
| `ontompo:ProjectObservatory` | `skos:prefLabel` | `"Observatório de projetos"@pt-BR` |
| `ontompo:ProjectObservatory` | `skos:prefLabel` | `"Project Observatory"@en` |
| `ontompo:ProjectObservatory` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:ReadOperation` | `rdfs:comment` | `"Operação CRUD que consulta um registro sem alterá-lo."@pt-BR` |
| `ontompo:ReadOperation` | `skos:prefLabel` | `"Operação de leitura"@pt-BR` |
| `ontompo:ReadOperation` | `skos:prefLabel` | `"CRUD Read Operation"@en` |
| `ontompo:ReadOperation` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:Reporter` | `rdfs:comment` | `"Papel do software quando coordena os relacionamentos entre os usuários, a interação deles com os projetos e com o observatório, e o relacionamento do observatório com outros sistemas."@pt-BR` |
| `ontompo:Reporter` | `skos:prefLabel` | `"Relacionamento"@pt-BR` |
| `ontompo:Reporter` | `skos:prefLabel` | `"Reporter"@en` |
| `ontompo:Reporter` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:Service` | `rdfs:comment` | `"Serviços executados por terceiros para estruturar, operar e manter a infraestrutura de TI de um observatório de projetos."@pt-BR` |
| `ontompo:Service` | `skos:prefLabel` | `"Serviço"@pt-BR` |
| `ontompo:Service` | `skos:prefLabel` | `"Service"@en` |
| `ontompo:Service` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:ServiceProvision` | `rdfs:comment` | `"Vínculo pelo qual um serviço é prestado a um software do observatório de projetos."@pt-BR` |
| `ontompo:ServiceProvision` | `skos:prefLabel` | `"Prestação de serviço"@pt-BR` |
| `ontompo:ServiceProvision` | `skos:prefLabel` | `"Service Provision"@en` |
| `ontompo:ServiceProvision` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:SocialAgent` | `rdfs:comment` | `"Agente cuja existência depende de uma construção social: organizações e grupos que agem como um só."@pt-BR` |
| `ontompo:SocialAgent` | `skos:prefLabel` | `"Agente social"@pt-BR` |
| `ontompo:SocialAgent` | `skos:prefLabel` | `"Social Agent"@en` |
| `ontompo:SocialAgent` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:SocialInteraction` | `rdfs:comment` | `"Vínculo de interação entre os agentes de um observatório de projetos e entre eles e o conteúdo dele."@pt-BR` |
| `ontompo:SocialInteraction` | `skos:prefLabel` | `"Interação social"@pt-BR` |
| `ontompo:SocialInteraction` | `skos:prefLabel` | `"Social Interaction"@en` |
| `ontompo:SocialInteraction` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:Software` | `rdfs:comment` | `"Aplicações que possibilitam a execução dos processos executados pelos observatórios de projetos."@pt-BR` |
| `ontompo:Software` | `skos:prefLabel` | `"Software"@pt-BR` |
| `ontompo:Software` | `skos:prefLabel` | `"Software"@en` |
| `ontompo:Software` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:SoftwareExecution` | `rdfs:comment` | `"Vínculo pelo qual um software é executado sobre um hardware. Substitui a composição inválida entre os dois, corrigida em A2."@pt-BR` |
| `ontompo:SoftwareExecution` | `skos:prefLabel` | `"Execução de software"@pt-BR` |
| `ontompo:SoftwareExecution` | `skos:prefLabel` | `"Software Execution"@en` |
| `ontompo:SoftwareExecution` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:StakeHolder` | `rdfs:comment` | `"Indivíduo, grupo ou organização que pode afetar ou ser afetado por uma decisão, atividade ou resultado de um projeto observado."@pt-BR` |
| `ontompo:StakeHolder` | `skos:prefLabel` | `"Parte interessada"@pt-BR` |
| `ontompo:StakeHolder` | `skos:prefLabel` | `"Stakeholder"@en` |
| `ontompo:StakeHolder` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:Storer` | `rdfs:comment` | `"Papel do gerenciamento de dados quando armazena os dados coletados sobre os projetos, mantendo a referência aos dados brutos de origem."@pt-BR` |
| `ontompo:Storer` | `skos:prefLabel` | `"Armazenamento"@pt-BR` |
| `ontompo:Storer` | `skos:prefLabel` | `"Storer"@en` |
| `ontompo:Storer` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:System` | `rdfs:comment` | `"Ator não-humano: sistema computacional externo ao ambiente do observatório que executa alguma ação ou fornece algum serviço a ele."@pt-BR` |
| `ontompo:System` | `skos:prefLabel` | `"Sistema"@pt-BR` |
| `ontompo:System` | `skos:prefLabel` | `"System"@en` |
| `ontompo:System` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:Transform` | `rdfs:comment` | `"Evento de transformação e modelagem dos dados coletados pelo observatório de projetos."@pt-BR` |
| `ontompo:Transform` | `skos:prefLabel` | `"Transformação"@pt-BR` |
| `ontompo:Transform` | `skos:prefLabel` | `"Transform"@en` |
| `ontompo:Transform` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:UpdateOperation` | `rdfs:comment` | `"Operação CRUD que altera o conteúdo de um registro que já existia."@pt-BR` |
| `ontompo:UpdateOperation` | `skos:prefLabel` | `"Operação de atualização"@pt-BR` |
| `ontompo:UpdateOperation` | `skos:prefLabel` | `"CRUD Update Operation"@en` |
| `ontompo:UpdateOperation` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:View` | `rdfs:comment` | `"Papel do software quando apresenta ao usuário o conteúdo do observatório de projetos."@pt-BR` |
| `ontompo:View` | `skos:prefLabel` | `"Visão"@pt-BR` |
| `ontompo:View` | `skos:prefLabel` | `"View"@en` |
| `ontompo:View` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:ViewProvision` | `rdfs:comment` | `"Vínculo pelo qual um gerenciamento de dados disponibiliza uma visão."@pt-BR` |
| `ontompo:ViewProvision` | `skos:prefLabel` | `"Disponibilização de visão"@pt-BR` |
| `ontompo:ViewProvision` | `skos:prefLabel` | `"View Provision"@en` |
| `ontompo:ViewProvision` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:componentOf_DataManager_ProjectObservatory` | `rdfs:comment` | `"Declara DataManager como componente do complexo funcional ProjectObservatory."@pt-BR` |
| `ontompo:componentOf_DataManager_ProjectObservatory` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:componentOf_View_ProjectObservatory` | `rdfs:comment` | `"Declara View como componente do complexo funcional ProjectObservatory."@pt-BR` |
| `ontompo:componentOf_View_ProjectObservatory` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:creation_Knowledge_Observation` | `rdfs:comment` | `"Declara que Knowledge passa a existir no evento Observation."@pt-BR` |
| `ontompo:creation_Knowledge_Observation` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:material_Software_Hardware` | `rdfs:comment` | `"Relação material entre Software e Hardware, derivada do relator que a fundamenta."@pt-BR` |
| `ontompo:material_Software_Hardware` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:mediation_Connection_Hardware` | `rdfs:comment` | `"Liga o relator Connection ao Hardware que ele medeia. Uma mediação da UFO é dependência existencial: não há Connection sem o Hardware."@pt-BR` |
| `ontompo:mediation_Connection_Hardware` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:mediation_Connection_Network` | `rdfs:comment` | `"Liga o relator Connection ao Network que ele medeia. Uma mediação da UFO é dependência existencial: não há Connection sem o Network."@pt-BR` |
| `ontompo:mediation_Connection_Network` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:mediation_Log_Agent` | `rdfs:comment` | `"Liga o relator Log ao Agent que ele medeia. Uma mediação da UFO é dependência existencial: não há Log sem o Agent."@pt-BR` |
| `ontompo:mediation_Log_Agent` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:mediation_Log_Reporter` | `rdfs:comment` | `"Liga o relator Log ao Reporter que ele medeia. Uma mediação da UFO é dependência existencial: não há Log sem o Reporter."@pt-BR` |
| `ontompo:mediation_Log_Reporter` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:mediation_ProjectDataManagement_DataManager` | `rdfs:comment` | `"Liga o relator ProjectDataManagement ao DataManager que ele medeia. Uma mediação da UFO é dependência existencial: não há ProjectDataManagement sem o DataManager."@pt-BR` |
| `ontompo:mediation_ProjectDataManagement_DataManager` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:mediation_ProjectDataManagement_Project` | `rdfs:comment` | `"Liga o relator ProjectDataManagement ao Project que ele medeia. Uma mediação da UFO é dependência existencial: não há ProjectDataManagement sem o Project."@pt-BR` |
| `ontompo:mediation_ProjectDataManagement_Project` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:mediation_ServiceProvision_Service` | `rdfs:comment` | `"Liga o relator ServiceProvision ao Service que ele medeia. Uma mediação da UFO é dependência existencial: não há ServiceProvision sem o Service."@pt-BR` |
| `ontompo:mediation_ServiceProvision_Service` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:mediation_ServiceProvision_Software` | `rdfs:comment` | `"Liga o relator ServiceProvision ao Software que ele medeia. Uma mediação da UFO é dependência existencial: não há ServiceProvision sem o Software."@pt-BR` |
| `ontompo:mediation_ServiceProvision_Software` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:mediation_SocialInteraction_Agent` | `rdfs:comment` | `"Liga o relator SocialInteraction ao Agent que ele medeia. Uma mediação da UFO é dependência existencial: não há SocialInteraction sem o Agent."@pt-BR` |
| `ontompo:mediation_SocialInteraction_Agent` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:mediation_SocialInteraction_Reporter` | `rdfs:comment` | `"Liga o relator SocialInteraction ao Reporter que ele medeia. Uma mediação da UFO é dependência existencial: não há SocialInteraction sem o Reporter."@pt-BR` |
| `ontompo:mediation_SocialInteraction_Reporter` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:mediation_SoftwareExecution_Hardware` | `rdfs:comment` | `"Liga o relator SoftwareExecution ao Hardware que ele medeia. Uma mediação da UFO é dependência existencial: não há SoftwareExecution sem o Hardware."@pt-BR` |
| `ontompo:mediation_SoftwareExecution_Hardware` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:mediation_SoftwareExecution_Software` | `rdfs:comment` | `"Liga o relator SoftwareExecution ao Software que ele medeia. Uma mediação da UFO é dependência existencial: não há SoftwareExecution sem o Software."@pt-BR` |
| `ontompo:mediation_SoftwareExecution_Software` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:mediation_ViewProvision_DataManager` | `rdfs:comment` | `"Liga o relator ViewProvision ao DataManager que ele medeia. Uma mediação da UFO é dependência existencial: não há ViewProvision sem o DataManager."@pt-BR` |
| `ontompo:mediation_ViewProvision_DataManager` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:mediation_ViewProvision_View` | `rdfs:comment` | `"Liga o relator ViewProvision ao View que ele medeia. Uma mediação da UFO é dependência existencial: não há ViewProvision sem o View."@pt-BR` |
| `ontompo:mediation_ViewProvision_View` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:memberOf_ObservatoryUser_ObservatoryGroup` | `rdfs:comment` | `"Declara ObservatoryUser como membro do coletivo ObservatoryGroup."@pt-BR` |
| `ontompo:memberOf_ObservatoryUser_ObservatoryGroup` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:memberOf_StakeHolder_ObservatoryGroup` | `rdfs:comment` | `"Declara StakeHolder como membro do coletivo ObservatoryGroup."@pt-BR` |
| `ontompo:memberOf_StakeHolder_ObservatoryGroup` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:memberOf_System_ObservatoryGroup` | `rdfs:comment` | `"Declara System como membro do coletivo ObservatoryGroup."@pt-BR` |
| `ontompo:memberOf_System_ObservatoryGroup` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:participation_Agent_CrudOperation` | `rdfs:comment` | `"Registra a participação de Agent no evento CrudOperation."@pt-BR` |
| `ontompo:participation_Agent_CrudOperation` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:participation_Agent_Observation` | `rdfs:comment` | `"Registra a participação de Agent no evento Observation."@pt-BR` |
| `ontompo:participation_Agent_Observation` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:participation_Collector_Extract` | `rdfs:comment` | `"Registra a participação de Collector no evento Extract."@pt-BR` |
| `ontompo:participation_Collector_Extract` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:participation_Collector_Transform` | `rdfs:comment` | `"Registra a participação de Collector no evento Transform."@pt-BR` |
| `ontompo:participation_Collector_Transform` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:participation_CrudView_CrudOperation` | `rdfs:comment` | `"Registra a participação de CrudView no evento CrudOperation."@pt-BR` |
| `ontompo:participation_CrudView_CrudOperation` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:participation_DataSource_Extract` | `rdfs:comment` | `"Registra a participação de DataSource no evento Extract."@pt-BR` |
| `ontompo:participation_DataSource_Extract` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:participation_Disseminator_Observation` | `rdfs:comment` | `"Registra a participação de Disseminator no evento Observation."@pt-BR` |
| `ontompo:participation_Disseminator_Observation` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:participation_Processor_Load` | `rdfs:comment` | `"Registra a participação de Processor no evento Load."@pt-BR` |
| `ontompo:participation_Processor_Load` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:participation_Processor_Transform` | `rdfs:comment` | `"Registra a participação de Processor no evento Transform."@pt-BR` |
| `ontompo:participation_Processor_Transform` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:participation_Storer_Load` | `rdfs:comment` | `"Registra a participação de Storer no evento Load."@pt-BR` |
| `ontompo:participation_Storer_Load` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:participational_Extract_EtlProcess` | `rdfs:comment` | `"Declara o evento Extract como parte própria do evento EtlProcess."@pt-BR` |
| `ontompo:participational_Extract_EtlProcess` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:participational_Load_EtlProcess` | `rdfs:comment` | `"Declara o evento Load como parte própria do evento EtlProcess."@pt-BR` |
| `ontompo:participational_Load_EtlProcess` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:participational_Transform_EtlProcess` | `rdfs:comment` | `"Declara o evento Transform como parte própria do evento EtlProcess."@pt-BR` |
| `ontompo:participational_Transform_EtlProcess` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |

## C3 — Axiomas de disjunção, fechando B4 (46)

| sujeito | predicado | objeto |
|---|---|---|
| `[]` | `rdf:type` | `owl:AllDisjointClasses` |
| `[]` | `owl:members` | `[]` |
| `[]` | `rdf:first` | `ontompo:ViewProvision` |
| `[]` | `rdf:rest` | `rdf:nil` |
| `[]` | `rdf:first` | `ontompo:SoftwareExecution` |
| `[]` | `rdf:rest` | `[]` |
| `[]` | `rdf:first` | `ontompo:Software` |
| `[]` | `rdf:rest` | `[]` |
| `[]` | `rdf:first` | `ontompo:SocialInteraction` |
| `[]` | `rdf:rest` | `[]` |
| `[]` | `rdf:first` | `ontompo:ServiceProvision` |
| `[]` | `rdf:rest` | `[]` |
| `[]` | `rdf:first` | `ontompo:Service` |
| `[]` | `rdf:rest` | `[]` |
| `[]` | `rdf:first` | `ontompo:ProjectDataManagement` |
| `[]` | `rdf:rest` | `[]` |
| `[]` | `rdf:first` | `ontompo:Project` |
| `[]` | `rdf:rest` | `[]` |
| `[]` | `rdf:first` | `ontompo:Person` |
| `[]` | `rdf:rest` | `[]` |
| `[]` | `rdf:first` | `ontompo:Organization` |
| `[]` | `rdf:rest` | `[]` |
| `[]` | `rdf:first` | `ontompo:ObservatoryGroup` |
| `[]` | `rdf:rest` | `[]` |
| `[]` | `rdf:first` | `ontompo:Network` |
| `[]` | `rdf:rest` | `[]` |
| `[]` | `rdf:first` | `ontompo:Log` |
| `[]` | `rdf:rest` | `[]` |
| `[]` | `rdf:first` | `ontompo:Knowledge` |
| `[]` | `rdf:rest` | `[]` |
| `[]` | `rdf:first` | `ontompo:Hardware` |
| `[]` | `rdf:rest` | `[]` |
| `[]` | `rdf:first` | `ontompo:DataSource` |
| `[]` | `rdf:rest` | `[]` |
| `[]` | `rdf:first` | `ontompo:Connection` |
| `[]` | `rdf:rest` | `[]` |
| `[]` | `rdf:first` | `ontompo:ComputationalSystem` |
| `[]` | `rdf:rest` | `[]` |
| `[]` | `rdf:type` | `owl:AllDisjointClasses` |
| `[]` | `owl:members` | `[]` |
| `[]` | `rdf:first` | `ontompo:ProjectObservatory` |
| `[]` | `rdf:rest` | `rdf:nil` |
| `[]` | `rdf:first` | `ontompo:View` |
| `[]` | `rdf:rest` | `[]` |
| `[]` | `rdf:first` | `ontompo:DataManager` |
| `[]` | `rdf:rest` | `[]` |

## C4 — Inversas nomeadas para cada propriedade de objeto (272)

| sujeito | predicado | objeto |
|---|---|---|
| `ontompo:hasComponent_ProjectObservatory_DataManager` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:hasComponent_ProjectObservatory_DataManager` | `owl:inverseOf` | `ontompo:componentOf_DataManager_ProjectObservatory` |
| `ontompo:componentOf_DataManager_ProjectObservatory` | `owl:inverseOf` | `ontompo:hasComponent_ProjectObservatory_DataManager` |
| `ontompo:hasComponent_ProjectObservatory_DataManager` | `rdfs:domain` | `ontompo:ProjectObservatory` |
| `ontompo:hasComponent_ProjectObservatory_DataManager` | `rdfs:range` | `ontompo:DataManager` |
| `ontompo:hasComponent_ProjectObservatory_DataManager` | `rdfs:label` | `"hasComponent_ProjectObservatory_DataManager"@en` |
| `ontompo:hasComponent_ProjectObservatory_DataManager` | `rdfs:comment` | `"Devolve os componentes de ProjectObservatory que são DataManager."@pt-BR` |
| `ontompo:hasComponent_ProjectObservatory_DataManager` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:hasComponent_ProjectObservatory_View` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:hasComponent_ProjectObservatory_View` | `owl:inverseOf` | `ontompo:componentOf_View_ProjectObservatory` |
| `ontompo:componentOf_View_ProjectObservatory` | `owl:inverseOf` | `ontompo:hasComponent_ProjectObservatory_View` |
| `ontompo:hasComponent_ProjectObservatory_View` | `rdfs:domain` | `ontompo:ProjectObservatory` |
| `ontompo:hasComponent_ProjectObservatory_View` | `rdfs:range` | `ontompo:View` |
| `ontompo:hasComponent_ProjectObservatory_View` | `rdfs:label` | `"hasComponent_ProjectObservatory_View"@en` |
| `ontompo:hasComponent_ProjectObservatory_View` | `rdfs:comment` | `"Devolve os componentes de ProjectObservatory que são View."@pt-BR` |
| `ontompo:hasComponent_ProjectObservatory_View` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:created_Observation_Knowledge` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:created_Observation_Knowledge` | `owl:inverseOf` | `ontompo:creation_Knowledge_Observation` |
| `ontompo:creation_Knowledge_Observation` | `owl:inverseOf` | `ontompo:created_Observation_Knowledge` |
| `ontompo:created_Observation_Knowledge` | `rdfs:domain` | `ontompo:Observation` |
| `ontompo:created_Observation_Knowledge` | `rdfs:range` | `ontompo:Knowledge` |
| `ontompo:created_Observation_Knowledge` | `rdfs:label` | `"created_Observation_Knowledge"@en` |
| `ontompo:created_Observation_Knowledge` | `rdfs:comment` | `"Devolve o que passou a existir no evento Observation, e é Knowledge."@pt-BR` |
| `ontompo:created_Observation_Knowledge` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:inverseMaterial_Hardware_Software` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:inverseMaterial_Hardware_Software` | `owl:inverseOf` | `ontompo:material_Software_Hardware` |
| `ontompo:material_Software_Hardware` | `owl:inverseOf` | `ontompo:inverseMaterial_Hardware_Software` |
| `ontompo:inverseMaterial_Hardware_Software` | `rdfs:domain` | `ontompo:Hardware` |
| `ontompo:inverseMaterial_Hardware_Software` | `rdfs:range` | `ontompo:Software` |
| `ontompo:inverseMaterial_Hardware_Software` | `rdfs:label` | `"inverseMaterial_Hardware_Software"@en` |
| `ontompo:inverseMaterial_Hardware_Software` | `rdfs:comment` | `"Relação material entre Hardware e Software, no sentido inverso ao gerado."@pt-BR` |
| `ontompo:inverseMaterial_Hardware_Software` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:mediatedBy_Hardware_Connection` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:mediatedBy_Hardware_Connection` | `owl:inverseOf` | `ontompo:mediation_Connection_Hardware` |
| `ontompo:mediation_Connection_Hardware` | `owl:inverseOf` | `ontompo:mediatedBy_Hardware_Connection` |
| `ontompo:mediatedBy_Hardware_Connection` | `rdfs:domain` | `ontompo:Hardware` |
| `ontompo:mediatedBy_Hardware_Connection` | `rdfs:range` | `ontompo:Connection` |
| `ontompo:mediatedBy_Hardware_Connection` | `rdfs:label` | `"mediatedBy_Hardware_Connection"@en` |
| `ontompo:mediatedBy_Hardware_Connection` | `rdfs:comment` | `"Liga o Hardware ao relator Connection que o medeia."@pt-BR` |
| `ontompo:mediatedBy_Hardware_Connection` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:mediatedBy_Network_Connection` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:mediatedBy_Network_Connection` | `owl:inverseOf` | `ontompo:mediation_Connection_Network` |
| `ontompo:mediation_Connection_Network` | `owl:inverseOf` | `ontompo:mediatedBy_Network_Connection` |
| `ontompo:mediatedBy_Network_Connection` | `rdfs:domain` | `ontompo:Network` |
| `ontompo:mediatedBy_Network_Connection` | `rdfs:range` | `ontompo:Connection` |
| `ontompo:mediatedBy_Network_Connection` | `rdfs:label` | `"mediatedBy_Network_Connection"@en` |
| `ontompo:mediatedBy_Network_Connection` | `rdfs:comment` | `"Liga o Network ao relator Connection que o medeia."@pt-BR` |
| `ontompo:mediatedBy_Network_Connection` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:mediatedBy_Agent_Log` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:mediatedBy_Agent_Log` | `owl:inverseOf` | `ontompo:mediation_Log_Agent` |
| `ontompo:mediation_Log_Agent` | `owl:inverseOf` | `ontompo:mediatedBy_Agent_Log` |
| `ontompo:mediatedBy_Agent_Log` | `rdfs:domain` | `ontompo:Agent` |
| `ontompo:mediatedBy_Agent_Log` | `rdfs:range` | `ontompo:Log` |
| `ontompo:mediatedBy_Agent_Log` | `rdfs:label` | `"mediatedBy_Agent_Log"@en` |
| `ontompo:mediatedBy_Agent_Log` | `rdfs:comment` | `"Liga o Agent ao relator Log que o medeia."@pt-BR` |
| `ontompo:mediatedBy_Agent_Log` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:mediatedBy_Reporter_Log` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:mediatedBy_Reporter_Log` | `owl:inverseOf` | `ontompo:mediation_Log_Reporter` |
| `ontompo:mediation_Log_Reporter` | `owl:inverseOf` | `ontompo:mediatedBy_Reporter_Log` |
| `ontompo:mediatedBy_Reporter_Log` | `rdfs:domain` | `ontompo:Reporter` |
| `ontompo:mediatedBy_Reporter_Log` | `rdfs:range` | `ontompo:Log` |
| `ontompo:mediatedBy_Reporter_Log` | `rdfs:label` | `"mediatedBy_Reporter_Log"@en` |
| `ontompo:mediatedBy_Reporter_Log` | `rdfs:comment` | `"Liga o Reporter ao relator Log que o medeia."@pt-BR` |
| `ontompo:mediatedBy_Reporter_Log` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:mediatedBy_DataManager_ProjectDataManagement` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:mediatedBy_DataManager_ProjectDataManagement` | `owl:inverseOf` | `ontompo:mediation_ProjectDataManagement_DataManager` |
| `ontompo:mediation_ProjectDataManagement_DataManager` | `owl:inverseOf` | `ontompo:mediatedBy_DataManager_ProjectDataManagement` |
| `ontompo:mediatedBy_DataManager_ProjectDataManagement` | `rdfs:domain` | `ontompo:DataManager` |
| `ontompo:mediatedBy_DataManager_ProjectDataManagement` | `rdfs:range` | `ontompo:ProjectDataManagement` |
| `ontompo:mediatedBy_DataManager_ProjectDataManagement` | `rdfs:label` | `"mediatedBy_DataManager_ProjectDataManagement"@en` |
| `ontompo:mediatedBy_DataManager_ProjectDataManagement` | `rdfs:comment` | `"Liga o DataManager ao relator ProjectDataManagement que o medeia."@pt-BR` |
| `ontompo:mediatedBy_DataManager_ProjectDataManagement` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:mediatedBy_Project_ProjectDataManagement` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:mediatedBy_Project_ProjectDataManagement` | `owl:inverseOf` | `ontompo:mediation_ProjectDataManagement_Project` |
| `ontompo:mediation_ProjectDataManagement_Project` | `owl:inverseOf` | `ontompo:mediatedBy_Project_ProjectDataManagement` |
| `ontompo:mediatedBy_Project_ProjectDataManagement` | `rdfs:domain` | `ontompo:Project` |
| `ontompo:mediatedBy_Project_ProjectDataManagement` | `rdfs:range` | `ontompo:ProjectDataManagement` |
| `ontompo:mediatedBy_Project_ProjectDataManagement` | `rdfs:label` | `"mediatedBy_Project_ProjectDataManagement"@en` |
| `ontompo:mediatedBy_Project_ProjectDataManagement` | `rdfs:comment` | `"Liga o Project ao relator ProjectDataManagement que o medeia."@pt-BR` |
| `ontompo:mediatedBy_Project_ProjectDataManagement` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:mediatedBy_Service_ServiceProvision` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:mediatedBy_Service_ServiceProvision` | `owl:inverseOf` | `ontompo:mediation_ServiceProvision_Service` |
| `ontompo:mediation_ServiceProvision_Service` | `owl:inverseOf` | `ontompo:mediatedBy_Service_ServiceProvision` |
| `ontompo:mediatedBy_Service_ServiceProvision` | `rdfs:domain` | `ontompo:Service` |
| `ontompo:mediatedBy_Service_ServiceProvision` | `rdfs:range` | `ontompo:ServiceProvision` |
| `ontompo:mediatedBy_Service_ServiceProvision` | `rdfs:label` | `"mediatedBy_Service_ServiceProvision"@en` |
| `ontompo:mediatedBy_Service_ServiceProvision` | `rdfs:comment` | `"Liga o Service ao relator ServiceProvision que o medeia."@pt-BR` |
| `ontompo:mediatedBy_Service_ServiceProvision` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:mediatedBy_Software_ServiceProvision` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:mediatedBy_Software_ServiceProvision` | `owl:inverseOf` | `ontompo:mediation_ServiceProvision_Software` |
| `ontompo:mediation_ServiceProvision_Software` | `owl:inverseOf` | `ontompo:mediatedBy_Software_ServiceProvision` |
| `ontompo:mediatedBy_Software_ServiceProvision` | `rdfs:domain` | `ontompo:Software` |
| `ontompo:mediatedBy_Software_ServiceProvision` | `rdfs:range` | `ontompo:ServiceProvision` |
| `ontompo:mediatedBy_Software_ServiceProvision` | `rdfs:label` | `"mediatedBy_Software_ServiceProvision"@en` |
| `ontompo:mediatedBy_Software_ServiceProvision` | `rdfs:comment` | `"Liga o Software ao relator ServiceProvision que o medeia."@pt-BR` |
| `ontompo:mediatedBy_Software_ServiceProvision` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:mediatedBy_Agent_SocialInteraction` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:mediatedBy_Agent_SocialInteraction` | `owl:inverseOf` | `ontompo:mediation_SocialInteraction_Agent` |
| `ontompo:mediation_SocialInteraction_Agent` | `owl:inverseOf` | `ontompo:mediatedBy_Agent_SocialInteraction` |
| `ontompo:mediatedBy_Agent_SocialInteraction` | `rdfs:domain` | `ontompo:Agent` |
| `ontompo:mediatedBy_Agent_SocialInteraction` | `rdfs:range` | `ontompo:SocialInteraction` |
| `ontompo:mediatedBy_Agent_SocialInteraction` | `rdfs:label` | `"mediatedBy_Agent_SocialInteraction"@en` |
| `ontompo:mediatedBy_Agent_SocialInteraction` | `rdfs:comment` | `"Liga o Agent ao relator SocialInteraction que o medeia."@pt-BR` |
| `ontompo:mediatedBy_Agent_SocialInteraction` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:mediatedBy_Reporter_SocialInteraction` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:mediatedBy_Reporter_SocialInteraction` | `owl:inverseOf` | `ontompo:mediation_SocialInteraction_Reporter` |
| `ontompo:mediation_SocialInteraction_Reporter` | `owl:inverseOf` | `ontompo:mediatedBy_Reporter_SocialInteraction` |
| `ontompo:mediatedBy_Reporter_SocialInteraction` | `rdfs:domain` | `ontompo:Reporter` |
| `ontompo:mediatedBy_Reporter_SocialInteraction` | `rdfs:range` | `ontompo:SocialInteraction` |
| `ontompo:mediatedBy_Reporter_SocialInteraction` | `rdfs:label` | `"mediatedBy_Reporter_SocialInteraction"@en` |
| `ontompo:mediatedBy_Reporter_SocialInteraction` | `rdfs:comment` | `"Liga o Reporter ao relator SocialInteraction que o medeia."@pt-BR` |
| `ontompo:mediatedBy_Reporter_SocialInteraction` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:mediatedBy_Hardware_SoftwareExecution` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:mediatedBy_Hardware_SoftwareExecution` | `owl:inverseOf` | `ontompo:mediation_SoftwareExecution_Hardware` |
| `ontompo:mediation_SoftwareExecution_Hardware` | `owl:inverseOf` | `ontompo:mediatedBy_Hardware_SoftwareExecution` |
| `ontompo:mediatedBy_Hardware_SoftwareExecution` | `rdfs:domain` | `ontompo:Hardware` |
| `ontompo:mediatedBy_Hardware_SoftwareExecution` | `rdfs:range` | `ontompo:SoftwareExecution` |
| `ontompo:mediatedBy_Hardware_SoftwareExecution` | `rdfs:label` | `"mediatedBy_Hardware_SoftwareExecution"@en` |
| `ontompo:mediatedBy_Hardware_SoftwareExecution` | `rdfs:comment` | `"Liga o Hardware ao relator SoftwareExecution que o medeia."@pt-BR` |
| `ontompo:mediatedBy_Hardware_SoftwareExecution` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:mediatedBy_Software_SoftwareExecution` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:mediatedBy_Software_SoftwareExecution` | `owl:inverseOf` | `ontompo:mediation_SoftwareExecution_Software` |
| `ontompo:mediation_SoftwareExecution_Software` | `owl:inverseOf` | `ontompo:mediatedBy_Software_SoftwareExecution` |
| `ontompo:mediatedBy_Software_SoftwareExecution` | `rdfs:domain` | `ontompo:Software` |
| `ontompo:mediatedBy_Software_SoftwareExecution` | `rdfs:range` | `ontompo:SoftwareExecution` |
| `ontompo:mediatedBy_Software_SoftwareExecution` | `rdfs:label` | `"mediatedBy_Software_SoftwareExecution"@en` |
| `ontompo:mediatedBy_Software_SoftwareExecution` | `rdfs:comment` | `"Liga o Software ao relator SoftwareExecution que o medeia."@pt-BR` |
| `ontompo:mediatedBy_Software_SoftwareExecution` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:mediatedBy_DataManager_ViewProvision` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:mediatedBy_DataManager_ViewProvision` | `owl:inverseOf` | `ontompo:mediation_ViewProvision_DataManager` |
| `ontompo:mediation_ViewProvision_DataManager` | `owl:inverseOf` | `ontompo:mediatedBy_DataManager_ViewProvision` |
| `ontompo:mediatedBy_DataManager_ViewProvision` | `rdfs:domain` | `ontompo:DataManager` |
| `ontompo:mediatedBy_DataManager_ViewProvision` | `rdfs:range` | `ontompo:ViewProvision` |
| `ontompo:mediatedBy_DataManager_ViewProvision` | `rdfs:label` | `"mediatedBy_DataManager_ViewProvision"@en` |
| `ontompo:mediatedBy_DataManager_ViewProvision` | `rdfs:comment` | `"Liga o DataManager ao relator ViewProvision que o medeia."@pt-BR` |
| `ontompo:mediatedBy_DataManager_ViewProvision` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:mediatedBy_View_ViewProvision` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:mediatedBy_View_ViewProvision` | `owl:inverseOf` | `ontompo:mediation_ViewProvision_View` |
| `ontompo:mediation_ViewProvision_View` | `owl:inverseOf` | `ontompo:mediatedBy_View_ViewProvision` |
| `ontompo:mediatedBy_View_ViewProvision` | `rdfs:domain` | `ontompo:View` |
| `ontompo:mediatedBy_View_ViewProvision` | `rdfs:range` | `ontompo:ViewProvision` |
| `ontompo:mediatedBy_View_ViewProvision` | `rdfs:label` | `"mediatedBy_View_ViewProvision"@en` |
| `ontompo:mediatedBy_View_ViewProvision` | `rdfs:comment` | `"Liga o View ao relator ViewProvision que o medeia."@pt-BR` |
| `ontompo:mediatedBy_View_ViewProvision` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:hasMember_ObservatoryGroup_ObservatoryUser` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:hasMember_ObservatoryGroup_ObservatoryUser` | `owl:inverseOf` | `ontompo:memberOf_ObservatoryUser_ObservatoryGroup` |
| `ontompo:memberOf_ObservatoryUser_ObservatoryGroup` | `owl:inverseOf` | `ontompo:hasMember_ObservatoryGroup_ObservatoryUser` |
| `ontompo:hasMember_ObservatoryGroup_ObservatoryUser` | `rdfs:domain` | `ontompo:ObservatoryGroup` |
| `ontompo:hasMember_ObservatoryGroup_ObservatoryUser` | `rdfs:range` | `ontompo:ObservatoryUser` |
| `ontompo:hasMember_ObservatoryGroup_ObservatoryUser` | `rdfs:label` | `"hasMember_ObservatoryGroup_ObservatoryUser"@en` |
| `ontompo:hasMember_ObservatoryGroup_ObservatoryUser` | `rdfs:comment` | `"Devolve os membros do coletivo ObservatoryGroup que são ObservatoryUser."@pt-BR` |
| `ontompo:hasMember_ObservatoryGroup_ObservatoryUser` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:hasMember_ObservatoryGroup_StakeHolder` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:hasMember_ObservatoryGroup_StakeHolder` | `owl:inverseOf` | `ontompo:memberOf_StakeHolder_ObservatoryGroup` |
| `ontompo:memberOf_StakeHolder_ObservatoryGroup` | `owl:inverseOf` | `ontompo:hasMember_ObservatoryGroup_StakeHolder` |
| `ontompo:hasMember_ObservatoryGroup_StakeHolder` | `rdfs:domain` | `ontompo:ObservatoryGroup` |
| `ontompo:hasMember_ObservatoryGroup_StakeHolder` | `rdfs:range` | `ontompo:StakeHolder` |
| `ontompo:hasMember_ObservatoryGroup_StakeHolder` | `rdfs:label` | `"hasMember_ObservatoryGroup_StakeHolder"@en` |
| `ontompo:hasMember_ObservatoryGroup_StakeHolder` | `rdfs:comment` | `"Devolve os membros do coletivo ObservatoryGroup que são StakeHolder."@pt-BR` |
| `ontompo:hasMember_ObservatoryGroup_StakeHolder` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:hasMember_ObservatoryGroup_System` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:hasMember_ObservatoryGroup_System` | `owl:inverseOf` | `ontompo:memberOf_System_ObservatoryGroup` |
| `ontompo:memberOf_System_ObservatoryGroup` | `owl:inverseOf` | `ontompo:hasMember_ObservatoryGroup_System` |
| `ontompo:hasMember_ObservatoryGroup_System` | `rdfs:domain` | `ontompo:ObservatoryGroup` |
| `ontompo:hasMember_ObservatoryGroup_System` | `rdfs:range` | `ontompo:System` |
| `ontompo:hasMember_ObservatoryGroup_System` | `rdfs:label` | `"hasMember_ObservatoryGroup_System"@en` |
| `ontompo:hasMember_ObservatoryGroup_System` | `rdfs:comment` | `"Devolve os membros do coletivo ObservatoryGroup que são System."@pt-BR` |
| `ontompo:hasMember_ObservatoryGroup_System` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:hasParticipant_CrudOperation_Agent` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:hasParticipant_CrudOperation_Agent` | `owl:inverseOf` | `ontompo:participation_Agent_CrudOperation` |
| `ontompo:participation_Agent_CrudOperation` | `owl:inverseOf` | `ontompo:hasParticipant_CrudOperation_Agent` |
| `ontompo:hasParticipant_CrudOperation_Agent` | `rdfs:domain` | `ontompo:CrudOperation` |
| `ontompo:hasParticipant_CrudOperation_Agent` | `rdfs:range` | `ontompo:Agent` |
| `ontompo:hasParticipant_CrudOperation_Agent` | `rdfs:label` | `"hasParticipant_CrudOperation_Agent"@en` |
| `ontompo:hasParticipant_CrudOperation_Agent` | `rdfs:comment` | `"Devolve os participantes do evento CrudOperation que são Agent."@pt-BR` |
| `ontompo:hasParticipant_CrudOperation_Agent` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:hasParticipant_Observation_Agent` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:hasParticipant_Observation_Agent` | `owl:inverseOf` | `ontompo:participation_Agent_Observation` |
| `ontompo:participation_Agent_Observation` | `owl:inverseOf` | `ontompo:hasParticipant_Observation_Agent` |
| `ontompo:hasParticipant_Observation_Agent` | `rdfs:domain` | `ontompo:Observation` |
| `ontompo:hasParticipant_Observation_Agent` | `rdfs:range` | `ontompo:Agent` |
| `ontompo:hasParticipant_Observation_Agent` | `rdfs:label` | `"hasParticipant_Observation_Agent"@en` |
| `ontompo:hasParticipant_Observation_Agent` | `rdfs:comment` | `"Devolve os participantes do evento Observation que são Agent."@pt-BR` |
| `ontompo:hasParticipant_Observation_Agent` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:hasParticipant_Extract_Collector` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:hasParticipant_Extract_Collector` | `owl:inverseOf` | `ontompo:participation_Collector_Extract` |
| `ontompo:participation_Collector_Extract` | `owl:inverseOf` | `ontompo:hasParticipant_Extract_Collector` |
| `ontompo:hasParticipant_Extract_Collector` | `rdfs:domain` | `ontompo:Extract` |
| `ontompo:hasParticipant_Extract_Collector` | `rdfs:range` | `ontompo:Collector` |
| `ontompo:hasParticipant_Extract_Collector` | `rdfs:label` | `"hasParticipant_Extract_Collector"@en` |
| `ontompo:hasParticipant_Extract_Collector` | `rdfs:comment` | `"Devolve os participantes do evento Extract que são Collector."@pt-BR` |
| `ontompo:hasParticipant_Extract_Collector` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:hasParticipant_Transform_Collector` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:hasParticipant_Transform_Collector` | `owl:inverseOf` | `ontompo:participation_Collector_Transform` |
| `ontompo:participation_Collector_Transform` | `owl:inverseOf` | `ontompo:hasParticipant_Transform_Collector` |
| `ontompo:hasParticipant_Transform_Collector` | `rdfs:domain` | `ontompo:Transform` |
| `ontompo:hasParticipant_Transform_Collector` | `rdfs:range` | `ontompo:Collector` |
| `ontompo:hasParticipant_Transform_Collector` | `rdfs:label` | `"hasParticipant_Transform_Collector"@en` |
| `ontompo:hasParticipant_Transform_Collector` | `rdfs:comment` | `"Devolve os participantes do evento Transform que são Collector."@pt-BR` |
| `ontompo:hasParticipant_Transform_Collector` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:hasParticipant_CrudOperation_CrudView` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:hasParticipant_CrudOperation_CrudView` | `owl:inverseOf` | `ontompo:participation_CrudView_CrudOperation` |
| `ontompo:participation_CrudView_CrudOperation` | `owl:inverseOf` | `ontompo:hasParticipant_CrudOperation_CrudView` |
| `ontompo:hasParticipant_CrudOperation_CrudView` | `rdfs:domain` | `ontompo:CrudOperation` |
| `ontompo:hasParticipant_CrudOperation_CrudView` | `rdfs:range` | `ontompo:CrudView` |
| `ontompo:hasParticipant_CrudOperation_CrudView` | `rdfs:label` | `"hasParticipant_CrudOperation_CrudView"@en` |
| `ontompo:hasParticipant_CrudOperation_CrudView` | `rdfs:comment` | `"Devolve os participantes do evento CrudOperation que são CrudView."@pt-BR` |
| `ontompo:hasParticipant_CrudOperation_CrudView` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:hasParticipant_Extract_DataSource` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:hasParticipant_Extract_DataSource` | `owl:inverseOf` | `ontompo:participation_DataSource_Extract` |
| `ontompo:participation_DataSource_Extract` | `owl:inverseOf` | `ontompo:hasParticipant_Extract_DataSource` |
| `ontompo:hasParticipant_Extract_DataSource` | `rdfs:domain` | `ontompo:Extract` |
| `ontompo:hasParticipant_Extract_DataSource` | `rdfs:range` | `ontompo:DataSource` |
| `ontompo:hasParticipant_Extract_DataSource` | `rdfs:label` | `"hasParticipant_Extract_DataSource"@en` |
| `ontompo:hasParticipant_Extract_DataSource` | `rdfs:comment` | `"Devolve os participantes do evento Extract que são DataSource."@pt-BR` |
| `ontompo:hasParticipant_Extract_DataSource` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:hasParticipant_Observation_Disseminator` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:hasParticipant_Observation_Disseminator` | `owl:inverseOf` | `ontompo:participation_Disseminator_Observation` |
| `ontompo:participation_Disseminator_Observation` | `owl:inverseOf` | `ontompo:hasParticipant_Observation_Disseminator` |
| `ontompo:hasParticipant_Observation_Disseminator` | `rdfs:domain` | `ontompo:Observation` |
| `ontompo:hasParticipant_Observation_Disseminator` | `rdfs:range` | `ontompo:Disseminator` |
| `ontompo:hasParticipant_Observation_Disseminator` | `rdfs:label` | `"hasParticipant_Observation_Disseminator"@en` |
| `ontompo:hasParticipant_Observation_Disseminator` | `rdfs:comment` | `"Devolve os participantes do evento Observation que são Disseminator."@pt-BR` |
| `ontompo:hasParticipant_Observation_Disseminator` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:hasParticipant_Load_Processor` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:hasParticipant_Load_Processor` | `owl:inverseOf` | `ontompo:participation_Processor_Load` |
| `ontompo:participation_Processor_Load` | `owl:inverseOf` | `ontompo:hasParticipant_Load_Processor` |
| `ontompo:hasParticipant_Load_Processor` | `rdfs:domain` | `ontompo:Load` |
| `ontompo:hasParticipant_Load_Processor` | `rdfs:range` | `ontompo:Processor` |
| `ontompo:hasParticipant_Load_Processor` | `rdfs:label` | `"hasParticipant_Load_Processor"@en` |
| `ontompo:hasParticipant_Load_Processor` | `rdfs:comment` | `"Devolve os participantes do evento Load que são Processor."@pt-BR` |
| `ontompo:hasParticipant_Load_Processor` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:hasParticipant_Transform_Processor` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:hasParticipant_Transform_Processor` | `owl:inverseOf` | `ontompo:participation_Processor_Transform` |
| `ontompo:participation_Processor_Transform` | `owl:inverseOf` | `ontompo:hasParticipant_Transform_Processor` |
| `ontompo:hasParticipant_Transform_Processor` | `rdfs:domain` | `ontompo:Transform` |
| `ontompo:hasParticipant_Transform_Processor` | `rdfs:range` | `ontompo:Processor` |
| `ontompo:hasParticipant_Transform_Processor` | `rdfs:label` | `"hasParticipant_Transform_Processor"@en` |
| `ontompo:hasParticipant_Transform_Processor` | `rdfs:comment` | `"Devolve os participantes do evento Transform que são Processor."@pt-BR` |
| `ontompo:hasParticipant_Transform_Processor` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:hasParticipant_Load_Storer` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:hasParticipant_Load_Storer` | `owl:inverseOf` | `ontompo:participation_Storer_Load` |
| `ontompo:participation_Storer_Load` | `owl:inverseOf` | `ontompo:hasParticipant_Load_Storer` |
| `ontompo:hasParticipant_Load_Storer` | `rdfs:domain` | `ontompo:Load` |
| `ontompo:hasParticipant_Load_Storer` | `rdfs:range` | `ontompo:Storer` |
| `ontompo:hasParticipant_Load_Storer` | `rdfs:label` | `"hasParticipant_Load_Storer"@en` |
| `ontompo:hasParticipant_Load_Storer` | `rdfs:comment` | `"Devolve os participantes do evento Load que são Storer."@pt-BR` |
| `ontompo:hasParticipant_Load_Storer` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:hasEventPart_EtlProcess_Extract` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:hasEventPart_EtlProcess_Extract` | `owl:inverseOf` | `ontompo:participational_Extract_EtlProcess` |
| `ontompo:participational_Extract_EtlProcess` | `owl:inverseOf` | `ontompo:hasEventPart_EtlProcess_Extract` |
| `ontompo:hasEventPart_EtlProcess_Extract` | `rdfs:domain` | `ontompo:EtlProcess` |
| `ontompo:hasEventPart_EtlProcess_Extract` | `rdfs:range` | `ontompo:Extract` |
| `ontompo:hasEventPart_EtlProcess_Extract` | `rdfs:label` | `"hasEventPart_EtlProcess_Extract"@en` |
| `ontompo:hasEventPart_EtlProcess_Extract` | `rdfs:comment` | `"Devolve as partes próprias do evento EtlProcess que são Extract."@pt-BR` |
| `ontompo:hasEventPart_EtlProcess_Extract` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:hasEventPart_EtlProcess_Load` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:hasEventPart_EtlProcess_Load` | `owl:inverseOf` | `ontompo:participational_Load_EtlProcess` |
| `ontompo:participational_Load_EtlProcess` | `owl:inverseOf` | `ontompo:hasEventPart_EtlProcess_Load` |
| `ontompo:hasEventPart_EtlProcess_Load` | `rdfs:domain` | `ontompo:EtlProcess` |
| `ontompo:hasEventPart_EtlProcess_Load` | `rdfs:range` | `ontompo:Load` |
| `ontompo:hasEventPart_EtlProcess_Load` | `rdfs:label` | `"hasEventPart_EtlProcess_Load"@en` |
| `ontompo:hasEventPart_EtlProcess_Load` | `rdfs:comment` | `"Devolve as partes próprias do evento EtlProcess que são Load."@pt-BR` |
| `ontompo:hasEventPart_EtlProcess_Load` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |
| `ontompo:hasEventPart_EtlProcess_Transform` | `rdf:type` | `owl:ObjectProperty` |
| `ontompo:hasEventPart_EtlProcess_Transform` | `owl:inverseOf` | `ontompo:participational_Transform_EtlProcess` |
| `ontompo:participational_Transform_EtlProcess` | `owl:inverseOf` | `ontompo:hasEventPart_EtlProcess_Transform` |
| `ontompo:hasEventPart_EtlProcess_Transform` | `rdfs:domain` | `ontompo:EtlProcess` |
| `ontompo:hasEventPart_EtlProcess_Transform` | `rdfs:range` | `ontompo:Transform` |
| `ontompo:hasEventPart_EtlProcess_Transform` | `rdfs:label` | `"hasEventPart_EtlProcess_Transform"@en` |
| `ontompo:hasEventPart_EtlProcess_Transform` | `rdfs:comment` | `"Devolve as partes próprias do evento EtlProcess que são Transform."@pt-BR` |
| `ontompo:hasEventPart_EtlProcess_Transform` | `rdfs:isDefinedBy` | `<https://example.org/ontompo/rodada-2>` |

## C5 — Metadados da ontologia (7)

| sujeito | predicado | objeto |
|---|---|---|
| `<https://example.org/ontompo/rodada-2>` | `dct:title` | `"OntoMPO — ontologia do Modelo para Observatórios de Projetos"@pt-BR` |
| `<https://example.org/ontompo/rodada-2>` | `dct:description` | `"Formalização do MPO revisada por análise ontológica fundamentada na UFO. Gerada a partir do modelo OntoUML pela transformação gUFO oficial e customizada por acréscimo; o acréscimo está no arquivo diff-gerado-customizado.ttl."@pt-BR` |
| `<https://example.org/ontompo/rodada-2>` | `dct:license` | `<https://creativecommons.org/licenses/by/4.0/>` |
| `<https://example.org/ontompo/rodada-2>` | `owl:versionInfo` | `"rodada-2, customizada"` |
| `<https://example.org/ontompo/rodada-2>` | `vann:preferredNamespacePrefix` | `"ontompo"` |
| `<https://example.org/ontompo/rodada-2>` | `vann:preferredNamespaceUri` | `"https://example.org/ontompo/rodada-2#"` |
| `<https://example.org/ontompo/rodada-2>` | `rdfs:comment` | `"Sem dct:creator: enquanto a revisão do artigo for duplamente anônima, declarar autoria aqui a quebraria. O IRI de exemplo é provisório e é fixado no depósito."@pt-BR` |

