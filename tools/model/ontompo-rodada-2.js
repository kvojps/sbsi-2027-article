/**
 * Modelo OntoUML da OntoMPO apos a **segunda rodada de revisao** (ticket 05).
 *
 * Parte do modelo da rodada 1 (`ontompo-rodada-1.js`) e adota as duas
 * microteorias da UFO que a formalizacao publicada abdicou:
 *
 *   A5  Extract, Transform e Load deixam de ser «relator» endurante e viram
 *       «event». As mediacoes que os ligavam a Collector, Processor, Storer e
 *       DataSource viram «participation», e os tres passam a ser partes
 *       proprias de um evento maior, `EtlProcess`, por «participational»;
 *   A6  `Agent` deixa de ser um «kind» generico e vira a «category» nao-sortal
 *       da UFO-C, particionada em `PhysicalAgent` e `SocialAgent`, com
 *       `Person` e `Organization` como os sortais ultimos que faltavam;
 *   A7  `System` ganha o kind subjacente que a propria dissertacao aponta como
 *       ausente — `ComputationalSystem` — e deixa de especializar `Agent`, que
 *       em UFO-C e o que porta momentos intencionais.
 *
 * Junto com A5 caem os dois construtos que a rodada 1 registrou como
 * endereçados a esta:
 *
 *   B8  `Observation`, o relator ternario que sobrou do verificador
 *       complementar, vira «event»; o `Knowledge` que ele mediava passa a ser
 *       criado nele, por «creation»;
 *   A1' `CrudOperation` e as quatro operacoes da particao viram «event». A
 *       rodada 1 separou os tipos e registrou por escrito que a leitura
 *       eventiva dependia de UFO-B e era desta rodada.
 *
 * O que NAO muda aqui, e por que: `SocialInteraction` e `Log` continuam
 * «relator». Aplicar o mesmo teste a eles e o que produz o achado novo desta
 * rodada, registrado como B9 em `artifacts/ontology/correcoes-rodada-2.md`, e
 * corrigi-lo exigiria decidir o que o material de origem nao diz. As
 * definicoes ausentes (B3) e os axiomas de disjuncao fora das duas particoes
 * (B4) continuam sendo da customizacao da OWL, ticket 06.
 *
 * Convencoes identicas as das rodadas anteriores: em meronimicas `source` e a
 * PARTE e `target` e o TODO; em mediacoes `source` e o RELATOR; em
 * participacoes `source` e o PARTICIPANTE endurante e `target` e o EVENTO — a
 * direcao que a gUFO exige, porque `gufo:participatedIn` vai do endurante para
 * o evento. A cardinalidade de uma extremidade e o rotulo desenhado ao lado da
 * classe daquela extremidade.
 */

const { Project, OntologicalNature } = require('ontouml-js');

/** Classes do modelo revisado, agrupadas por camada. */
const CLASSES = [
  // Camada Agentes — a taxonomia UFO-C de A6 e A7
  ['Agent', 'category'],
  ['PhysicalAgent', 'category'],
  ['SocialAgent', 'category'],
  ['Person', 'kind'],
  ['Organization', 'kind'],
  ['ComputationalSystem', 'kind'], // A7: o kind subjacente ao papel `System`
  ['ObservatoryGroup', 'collective'],
  ['ObservatoryUser', 'role'],
  ['StakeHolder', 'roleMixin'], // A6: individuo, grupo ou organizacao
  ['System', 'role'],
  ['Knowledge', 'kind'],
  ['Observation', 'event'], // B8
  ['SocialInteraction', 'relator'],
  ['Log', 'relator'],
  ['CrudOperation', 'event'], // A1, completada sob UFO-B
  ['CreateOperation', 'event'],
  ['ReadOperation', 'event'],
  ['UpdateOperation', 'event'],
  ['DeleteOperation', 'event'],
  // Camada Estruturas - Componentes, Conteudos e Caracteristicas
  ['CrudRepository', 'role'],
  ['Project', 'kind'],
  ['Disseminator', 'role'],
  ['Reporter', 'role'],
  ['CrudView', 'role'],
  ['DataManager', 'role'],
  ['View', 'role'],
  ['ProjectDataManagement', 'relator'],
  ['ViewProvision', 'relator'],
  ['Collector', 'role'],
  ['Processor', 'role'],
  ['Storer', 'role'],
  // A5: o ETL como evento complexo e suas tres partes proprias
  ['EtlProcess', 'event'],
  ['Extract', 'event'],
  ['Transform', 'event'],
  ['Load', 'event'],
  ['DataSource', 'kind'],
  ['ProjectObservatory', 'subkind'],
  // Camada Estruturas - Infraestrutura de TI
  ['Software', 'kind'],
  ['Service', 'kind'],
  ['Hardware', 'kind'],
  ['SoftwareExecution', 'relator'],
  ['ServiceProvision', 'relator'],
  ['Connection', 'relator'],
  ['Network', 'kind'],
];

/**
 * As naturezas ontologicas que nao sao o padrao do criador.
 *
 * Os nao-sortais da camada de agentes precisam declarar quais naturezas seus
 * individuos podem ter, e a declaracao nao e decorativa: a verificacao exige
 * que as naturezas do geral contenham as do especifico. `Agent` admite
 * complexo funcional e coletivo porque o proprio Apendice A da dissertacao
 * enumera *individuo, grupo ou organizacao* como partes interessadas — tres
 * principios de identidade, que e exatamente o que um «kind» nao pode
 * fornecer.
 */
const NATUREZAS = {
  Agent: [OntologicalNature.functional_complex, OntologicalNature.collective],
  PhysicalAgent: [OntologicalNature.functional_complex],
  SocialAgent: [OntologicalNature.functional_complex, OntologicalNature.collective],
  StakeHolder: [OntologicalNature.functional_complex, OntologicalNature.collective],
};

/** Generalizacoes, como [geral, especifico]. */
const GENERALIZACOES = [
  // A6: a taxonomia UFO-C
  ['Agent', 'PhysicalAgent'],
  ['Agent', 'SocialAgent'],
  ['Agent', 'StakeHolder'],
  ['PhysicalAgent', 'Person'],
  ['SocialAgent', 'Organization'],
  ['Person', 'ObservatoryUser'],
  // A7: o papel `System` sob o kind que o fundamenta, fora de `Agent`
  ['ComputationalSystem', 'System'],
  // A1, agora entre eventos
  ['CrudOperation', 'CreateOperation'],
  ['CrudOperation', 'ReadOperation'],
  ['CrudOperation', 'UpdateOperation'],
  ['CrudOperation', 'DeleteOperation'],
  ['DataManager', 'CrudRepository'],
  ['DataManager', 'Collector'],
  ['DataManager', 'Processor'],
  ['DataManager', 'Storer'],
  ['View', 'Disseminator'],
  ['View', 'Reporter'],
  ['View', 'CrudView'],
  ['Software', 'DataManager'],
  ['Software', 'View'],
  ['Software', 'ProjectObservatory'],
];

/**
 * Particoes, como [nome, geral, especificos]. As duas sao disjuntas e
 * completas.
 *
 * `agentNature` e a particao da UFO-C: todo agente e fisico ou social, e nao
 * os dois. `crudOperationType` e a da rodada 1, que sobrevive a mudanca de
 * estereotipo — separar os quatro tipos nao dependia de eles serem endurantes.
 */
const PARTICOES = [
  ['agentNature', 'Agent', ['PhysicalAgent', 'SocialAgent']],
  [
    'crudOperationType',
    'CrudOperation',
    ['CreateOperation', 'ReadOperation', 'UpdateOperation', 'DeleteOperation'],
  ],
];

/** Meronimicas, como [estereotipo, parte, cardParte, todo, cardTodo]. */
const MERONIMICAS = [
  ['memberOf', 'ObservatoryUser', '1..*', 'ObservatoryGroup', '1'],
  ['memberOf', 'StakeHolder', '1..*', 'ObservatoryGroup', '1'],
  ['memberOf', 'System', '1..*', 'ObservatoryGroup', '1'],
  ['componentOf', 'DataManager', '1..*', 'ProjectObservatory', '1'],
  ['componentOf', 'View', '1..*', 'ProjectObservatory', '1'],
];

/**
 * Mediacoes, como [relator, cardRelator, mediado, cardMediado].
 *
 * Sobram nove, contra vinte na rodada 1: as onze que ligavam `Observation`,
 * `CrudOperation`, `Extract`, `Transform` e `Load` aos seus relata viraram
 * participacao ou criacao, porque o que esses cinco construtos reificavam nao
 * era um vinculo entre endurantes, era um acontecimento.
 */
const MEDIACOES = [
  ['SocialInteraction', '0..*', 'Agent', '1'],
  ['SocialInteraction', '0..*', 'Reporter', '1'],
  ['Log', '0..*', 'Agent', '1'],
  ['Log', '0..*', 'Reporter', '1'],
  ['ProjectDataManagement', '0..*', 'DataManager', '1'],
  ['ProjectDataManagement', '0..*', 'Project', '1'],
  ['ViewProvision', '0..*', 'DataManager', '1'],
  ['ViewProvision', '0..*', 'View', '1'],
  ['SoftwareExecution', '1..*', 'Software', '1'],
  ['SoftwareExecution', '0..*', 'Hardware', '1'],
  ['ServiceProvision', '1..*', 'Service', '1'],
  ['ServiceProvision', '0..*', 'Software', '1'],
  ['Connection', '0..*', 'Hardware', '1'],
  ['Connection', '0..*', 'Network', '1'],
];

/**
 * Participacoes, como [participante, cardParticipante, evento, cardEvento].
 *
 * Cada uma substitui, ponta a ponta, uma mediacao da rodada 1: onde havia
 * `[relator, cardRelator, mediado, cardMediado]` ha agora
 * `[mediado, cardMediado, evento, cardRelator]`. As multiplicidades sao as
 * mesmas, invertidas de lado junto com as pontas, de modo que o que a mediacao
 * afirmava continua afirmado — o `1..*` do lado do evento diz que um coletor
 * so e coletor porque participou de ao menos uma extracao, que era o que a
 * dependencia existencial da mediacao dizia.
 */
const PARTICIPACOES = [
  ['Agent', '1', 'Observation', '0..*'],
  ['Disseminator', '1', 'Observation', '0..*'],
  ['Agent', '1', 'CrudOperation', '0..*'],
  ['CrudView', '1', 'CrudOperation', '0..*'],
  ['Collector', '1', 'Extract', '1..*'],
  ['DataSource', '1', 'Extract', '1..*'],
  ['Collector', '1', 'Transform', '1..*'],
  ['Processor', '1', 'Transform', '1..*'],
  ['Processor', '1', 'Load', '1..*'],
  ['Storer', '1', 'Load', '1..*'],
];

/**
 * Participacionais, como [parteEvento, cardParte, eventoTodo, cardTodo]. E a
 * parthood entre eventos: `EtlProcess` tem exatamente uma extracao, uma
 * transformacao e uma carga como partes proprias, e cada uma pertence a um
 * unico processo.
 *
 * E ela que da a QC6 — a cadeia de proveniencia de um conteudo divulgado ate a
 * fonte de dados — um caminho a percorrer: da fonte, pela extracao, ate o
 * armazenamento, dentro de um mesmo acontecimento.
 */
const PARTICIPACIONAIS = [
  ['Extract', '1', 'EtlProcess', '1'],
  ['Transform', '1', 'EtlProcess', '1'],
  ['Load', '1', 'EtlProcess', '1'],
];

/**
 * Criacoes, como [criado, cardCriado, evento, cardEvento]. `Knowledge` nao
 * participa da observacao: ele passa a existir nela. A mediacao da rodada 1
 * nao tinha como dizer isso.
 */
const CRIACOES = [['Knowledge', '1..*', 'Observation', '1']];

/** Materiais, como [origem, cardOrigem, destino, cardDestino, relatorQueADeriva]. */
const MATERIAIS = [['Software', '0..*', 'Hardware', '1..*', 'SoftwareExecution']];

const CRIADOR_POR_ESTEREOTIPO = {
  kind: 'createKind',
  subkind: 'createSubkind',
  role: 'createRole',
  roleMixin: 'createRoleMixin',
  category: 'createCategory',
  collective: 'createCollective',
  relator: 'createRelator',
  event: 'createEvent',
};

/** Mesma regra de nomeacao das rodadas anteriores, para que os IRIs comparem. */
function nomeDaRelacao(estereotipo, origem, destino) {
  return `${estereotipo}_${origem}_${destino}`;
}

function construirModeloRodada2() {
  const projeto = new Project();
  projeto.setName('OntoMPO (revisado, rodada 2)');
  const modelo = projeto.createModel();
  modelo.setName('OntoMPO');

  const porNome = {};
  for (const [nome, estereotipo] of CLASSES) {
    const criador = CRIADOR_POR_ESTEREOTIPO[estereotipo];
    porNome[nome] =
      NATUREZAS[nome] !== undefined ? modelo[criador](nome, NATUREZAS[nome]) : modelo[criador](nome);
  }

  const generalizacoesPorPar = {};
  for (const [geral, especifico] of GENERALIZACOES) {
    generalizacoesPorPar[`${geral}|${especifico}`] = modelo.createGeneralization(
      porNome[geral],
      porNome[especifico],
    );
  }

  for (const [nome, geral, especificos] of PARTICOES) {
    modelo.createPartition(
      especificos.map((especifico) => generalizacoesPorPar[`${geral}|${especifico}`]),
      null,
      nome,
    );
  }

  for (const [estereotipo, parte, cardParte, todo, cardTodo] of MERONIMICAS) {
    const criador =
      estereotipo === 'memberOf' ? 'createMemberOfRelation' : 'createComponentOfRelation';
    const relacao = modelo[criador](
      porNome[parte],
      porNome[todo],
      nomeDaRelacao(estereotipo, parte, todo),
    );
    relacao.getSourceEnd().cardinality.value = cardParte;
    relacao.getTargetEnd().cardinality.value = cardTodo;
  }

  const BINARIAS = [
    ['createMediationRelation', 'mediation', MEDIACOES],
    ['createParticipationRelation', 'participation', PARTICIPACOES],
    ['createParticipationalRelation', 'participational', PARTICIPACIONAIS],
    ['createCreationRelation', 'creation', CRIACOES],
  ];
  for (const [criador, estereotipo, tuplas] of BINARIAS) {
    for (const [origem, cardOrigem, destino, cardDestino] of tuplas) {
      const relacao = modelo[criador](
        porNome[origem],
        porNome[destino],
        nomeDaRelacao(estereotipo, origem, destino),
      );
      relacao.getSourceEnd().cardinality.value = cardOrigem;
      relacao.getTargetEnd().cardinality.value = cardDestino;
    }
  }

  for (const [origem, cardOrigem, destino, cardDestino, relator] of MATERIAIS) {
    const material = modelo.createMaterialRelation(
      porNome[origem],
      porNome[destino],
      nomeDaRelacao('material', origem, destino),
    );
    material.getSourceEnd().cardinality.value = cardOrigem;
    material.getTargetEnd().cardinality.value = cardDestino;
    modelo.createDerivationRelation(
      material,
      porNome[relator],
      nomeDaRelacao('derivation', `${origem}_${destino}`, relator),
    );
  }

  return projeto;
}

module.exports = {
  CLASSES,
  GENERALIZACOES,
  PARTICOES,
  MERONIMICAS,
  MEDIACOES,
  PARTICIPACOES,
  PARTICIPACIONAIS,
  CRIACOES,
  MATERIAIS,
  construirModeloRodada2,
};
