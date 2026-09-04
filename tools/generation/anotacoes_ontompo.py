#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""As definicoes que a formalizacao publicada perdeu no caminho.

Insumo da customizacao C2 (`customizar_owl.py`). Fecha o achado **B3**,
registrado em `artifacts/ontology/evidencias-A1-A9.md`: o OOPS! acusa 63
elementos sem nenhuma anotacao legivel no modelo *as-is*, enquanto o **Apendice
A da conceituacao do MPO define 53 termos**, com definicao, sinonimos,
instancias e atributos. As definicoes existiam e nao chegaram ao modelo — a
conceituacao da Methontology foi feita e depois descartada na formalizacao.

O texto dos verbetes vai para dentro da OWL e e lido por terceiros, entao vem
acentuado, ao contrario dos comentarios do ferramental.

Cada verbete traz a **origem**, e a origem e o que da valor ao verbete:

  `glossario`  o texto vem do glossario do Apendice A, condensado e ajustado ao
               recorte da classe. E a maioria, e e o que sustenta a afirmacao de
               que as definicoes ja existiam;
  `modelo`     o conceito esta no modelo publicado e nao tem verbete proprio no
               glossario; a definicao foi redigida a partir do papel que ele
               ocupa nos diagramas;
  `revisao`    o conceito nao existia no modelo publicado — foi introduzido por
               uma das rodadas de revisao, e a definicao nasce com ele.

O rotulo preferido em portugues e o termo do glossario, o que reata o
identificador ao vocabulario do dominio. O rotulo preferido em ingles e onde o
achado **B5** (convencao de nome) e endereçado: `Stakeholder` com h minusculo,
`CRUD` como acronimo, `Data Source` separado. O IRI **nao** muda — ver a
justificativa da C2 em `artifacts/ontology/owl/customizacoes.md`.
"""

from __future__ import annotations

# nome da classe -> (definicao pt-BR, rotulo pt-BR, rotulo en, origem)
CLASSES: dict[str, tuple[str, str, str, str]] = {
    # Camada Agentes — a taxonomia UFO-C introduzida por A6 e A7
    "Agent": (
        "Categoria não-sortal que reúne tudo o que porta intenções e age no contexto de um "
        "observatório de projetos, seja um agente físico ou um agente social.",
        "Agente",
        "Agent",
        "revisao",
    ),
    "PhysicalAgent": (
        "Agente cuja existência é a de um objeto físico concreto — no domínio do observatório, "
        "o indivíduo humano.",
        "Agente físico",
        "Physical Agent",
        "revisao",
    ),
    "SocialAgent": (
        "Agente cuja existência depende de uma construção social: organizações e grupos que "
        "agem como um só.",
        "Agente social",
        "Social Agent",
        "revisao",
    ),
    "Person": (
        "Ser humano que participa de um observatório de projetos, em qualquer papel.",
        "Pessoa",
        "Person",
        "revisao",
    ),
    "Organization": (
        "Instituição à qual uma parte interessada pertence, e que pode ela própria afetar ou ser "
        "afetada pelos projetos observados.",
        "Organização",
        "Organization",
        "glossario",
    ),
    "ComputationalSystem": (
        "Sistema computacional, tomado como o tipo que fornece princípio de identidade aos "
        "sistemas que interagem com o observatório.",
        "Sistema computacional",
        "Computational System",
        "revisao",
    ),
    "ObservatoryGroup": (
        "Coletivo de agentes reunidos em torno de um observatório de projetos: a equipe "
        "responsável pelo gerenciamento, manutenção e operação do observatório, seus usuários e "
        "os sistemas que com ele trocam.",
        "Grupo do observatório",
        "Observatory Group",
        "glossario",
    ),
    "ObservatoryUser": (
        "Ator humano que desfruta das utilidades que um observatório de projetos proporciona.",
        "Usuário do observatório",
        "Observatory User",
        "glossario",
    ),
    "StakeHolder": (
        "Indivíduo, grupo ou organização que pode afetar ou ser afetado por uma decisão, "
        "atividade ou resultado de um projeto observado.",
        "Parte interessada",
        "Stakeholder",
        "glossario",
    ),
    "System": (
        "Ator não-humano: sistema computacional externo ao ambiente do observatório que executa "
        "alguma ação ou fornece algum serviço a ele.",
        "Sistema",
        "System",
        "glossario",
    ),
    "Knowledge": (
        "Conhecimento sobre os projetos observados, adquirido e construído a partir do conteúdo "
        "que o observatório disponibiliza.",
        "Conhecimento",
        "Knowledge",
        "glossario",
    ),
    "Observation": (
        "Evento em que um agente observa o conteúdo divulgado pelo observatório e no qual passa a "
        "existir conhecimento sobre os projetos observados.",
        "Observação",
        "Observation",
        "modelo",
    ),
    "SocialInteraction": (
        "Vínculo de interação entre os agentes de um observatório de projetos e entre eles e o "
        "conteúdo dele.",
        "Interação social",
        "Social Interaction",
        "glossario",
    ),
    "Log": (
        "Registro que responsabiliza um agente por suas ações no contexto do observatório, e que "
        "sustenta a auditoria dessas ações.",
        "Registro de auditoria",
        "Log",
        "glossario",
    ),
    "CrudOperation": (
        "Evento de operação sobre um repositório de dados do observatório.",
        "Operação CRUD",
        "CRUD Operation",
        "revisao",
    ),
    "CreateOperation": (
        "Operação CRUD que faz passar a existir um registro que não existia.",
        "Operação de criação",
        "CRUD Create Operation",
        "revisao",
    ),
    "ReadOperation": (
        "Operação CRUD que consulta um registro sem alterá-lo.",
        "Operação de leitura",
        "CRUD Read Operation",
        "revisao",
    ),
    "UpdateOperation": (
        "Operação CRUD que altera o conteúdo de um registro que já existia.",
        "Operação de atualização",
        "CRUD Update Operation",
        "revisao",
    ),
    "DeleteOperation": (
        "Operação CRUD que faz deixar de existir um registro.",
        "Operação de exclusão",
        "CRUD Delete Operation",
        "revisao",
    ),
    # Camada Estruturas — Componentes e Conteudos
    "CrudRepository": (
        "Papel do gerenciamento de dados quando ele expõe um repositório sobre o qual operações "
        "CRUD são executadas.",
        "Repositório CRUD",
        "CRUD Repository",
        "modelo",
    ),
    "Project": (
        "Projeto observado: aquele sobre o qual o observatório reúne e divulga dados, informação e "
        "conhecimento, e que ele não gerencia.",
        "Projeto",
        "Project",
        "glossario",
    ),
    "Disseminator": (
        "Papel do software quando divulga análises e reflexões sobre os dados dos projetos "
        "observados, segundo as diretrizes de acesso e segurança do observatório.",
        "Disseminação",
        "Disseminator",
        "glossario",
    ),
    "Reporter": (
        "Papel do software quando coordena os relacionamentos entre os usuários, a interação "
        "deles com os projetos e com o observatório, e o relacionamento do observatório com "
        "outros sistemas.",
        "Relacionamento",
        "Reporter",
        "glossario",
    ),
    "CrudView": (
        "Papel da visão quando é por ela que uma operação CRUD sobre o repositório é disparada.",
        "Visão CRUD",
        "CRUD View",
        "modelo",
    ),
    "DataManager": (
        "Ferramentas de software necessárias para que o observatório organize, gerencie e "
        "processe os dados relacionados aos projetos observados.",
        "Gerenciamento de dados",
        "Data Manager",
        "glossario",
    ),
    "View": (
        "Papel do software quando apresenta ao usuário o conteúdo do observatório de projetos.",
        "Visão",
        "View",
        "modelo",
    ),
    "ProjectDataManagement": (
        "Vínculo pelo qual um gerenciamento de dados responde pelos dados de um projeto "
        "observado.",
        "Gerência de dados de projeto",
        "Project Data Management",
        "revisao",
    ),
    "ViewProvision": (
        "Vínculo pelo qual um gerenciamento de dados disponibiliza uma visão.",
        "Disponibilização de visão",
        "View Provision",
        "revisao",
    ),
    "Collector": (
        "Papel do gerenciamento de dados quando captura, de forma interna ou externa, os dados "
        "dos projetos observados.",
        "Coleta",
        "Collector",
        "glossario",
    ),
    "Processor": (
        "Papel do gerenciamento de dados quando trata e converte os dados brutos dos projetos em "
        "uma forma mais significativa.",
        "Processamento",
        "Processor",
        "glossario",
    ),
    "Storer": (
        "Papel do gerenciamento de dados quando armazena os dados coletados sobre os projetos, "
        "mantendo a referência aos dados brutos de origem.",
        "Armazenamento",
        "Storer",
        "glossario",
    ),
    "EtlProcess": (
        "Evento complexo que leva os dados da fonte até o repositório do observatório, e do qual "
        "a extração, a transformação e a carga são partes próprias.",
        "Processo de ETL",
        "ETL Process",
        "revisao",
    ),
    "Extract": (
        "Evento de identificação e coleta dos dados e informações relevantes sobre os projetos "
        "observados e suas temáticas.",
        "Extração",
        "Extract",
        "glossario",
    ),
    "Transform": (
        "Evento de transformação e modelagem dos dados coletados pelo observatório de projetos.",
        "Transformação",
        "Transform",
        "glossario",
    ),
    "Load": (
        "Evento de armazenamento, em um repositório, dos dados coletados e transformados sobre os "
        "projetos observados.",
        "Carga",
        "Load",
        "glossario",
    ),
    "DataSource": (
        "Origem principal dos dados coletados: sistemas internos, partes interessadas externas, "
        "bases de dados abertas ou sensores.",
        "Fonte de dados",
        "Data Source",
        "glossario",
    ),
    "ProjectObservatory": (
        "Observatório de projetos: o software que coleta, integra e divulga informação sobre um "
        "conjunto de projetos observados, para dar transparência e prestação de contas a partes "
        "interessadas externas.",
        "Observatório de projetos",
        "Project Observatory",
        "glossario",
    ),
    # Camada Estruturas — Infraestrutura de TI
    "Software": (
        "Aplicações que possibilitam a execução dos processos executados pelos observatórios de "
        "projetos.",
        "Software",
        "Software",
        "glossario",
    ),
    "Service": (
        "Serviços executados por terceiros para estruturar, operar e manter a infraestrutura de "
        "TI de um observatório de projetos.",
        "Serviço",
        "Service",
        "glossario",
    ),
    "Hardware": (
        "Equipamento físico de tecnologia da informação utilizado nos processos executados pelos "
        "observatórios de projetos.",
        "Hardware",
        "Hardware",
        "glossario",
    ),
    "SoftwareExecution": (
        "Vínculo pelo qual um software é executado sobre um hardware. Substitui a composição "
        "inválida entre os dois, corrigida em A2.",
        "Execução de software",
        "Software Execution",
        "revisao",
    ),
    "ServiceProvision": (
        "Vínculo pelo qual um serviço é prestado a um software do observatório de projetos.",
        "Prestação de serviço",
        "Service Provision",
        "revisao",
    ),
    "Connection": (
        "Vínculo pelo qual um hardware do observatório se liga a uma rede.",
        "Conexão",
        "Connection",
        "modelo",
    ),
    "Network": (
        "Componentes que possibilitam a comunicação, o gerenciamento e as operações de rede entre "
        "um observatório de projetos e os sistemas internos e externos das organizações.",
        "Rede",
        "Network",
        "glossario",
    ),
}

# Como cada estereotipo de relacao e descrito, no direto e no inverso. O nome da
# propriedade gerada e `<estereotipo>_<origem>_<destino>`; o do inverso vem do
# token da terceira coluna, em `<token>_<destino>_<origem>`.
ESTEREOTIPOS: dict[str, tuple[str, str, str]] = {
    "mediation": (
        "Liga o relator {origem} ao {destino} que ele medeia. Uma mediação da UFO é dependência "
        "existencial: não há {origem} sem o {destino}.",
        "Liga o {origem} ao relator {destino} que o medeia.",
        "mediatedBy",
    ),
    "memberOf": (
        "Declara {origem} como membro do coletivo {destino}.",
        "Devolve os membros do coletivo {origem} que são {destino}.",
        "hasMember",
    ),
    "componentOf": (
        "Declara {origem} como componente do complexo funcional {destino}.",
        "Devolve os componentes de {origem} que são {destino}.",
        "hasComponent",
    ),
    "participation": (
        "Registra a participação de {origem} no evento {destino}.",
        "Devolve os participantes do evento {origem} que são {destino}.",
        "hasParticipant",
    ),
    "participational": (
        "Declara o evento {origem} como parte própria do evento {destino}.",
        "Devolve as partes próprias do evento {origem} que são {destino}.",
        "hasEventPart",
    ),
    "creation": (
        "Declara que {origem} passa a existir no evento {destino}.",
        "Devolve o que passou a existir no evento {origem}, e é {destino}.",
        "created",
    ),
    "material": (
        "Relação material entre {origem} e {destino}, derivada do relator que a fundamenta.",
        "Relação material entre {origem} e {destino}, no sentido inverso ao gerado.",
        "inverseMaterial",
    ),
}
