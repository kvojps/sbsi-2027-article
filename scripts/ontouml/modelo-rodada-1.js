/**
 * Modelo OntoUML da OntoMPO apos a **primeira rodada de revisao** (ticket 04).
 *
 * Parte do modelo *as-is* (`modelo-as-is.js`) e aplica as seis correcoes que
 * nao exigem adotar novas microteorias da UFO:
 *
 *   A1  CrudOperation, que colapsava Create/Read/Update/Delete, e decomposta
 *       numa particao de quatro subkinds de relator;
 *   A2  a «componentOf» de Hardware para Software sai, e a relacao real —
 *       execucao/hospedagem — entra reificada no relator SoftwareExecution,
 *       com a material derivada dele;
 *   A3  as tres «memberOf» passam a ter o losango do lado do coletivo, e o
 *       minimo na ponta do membro sobe de zero para um;
 *   A4  a classe de dominio `Relator` vira `Reporter`;
 *   A8  Management (ternario) e Operation (quaternario) sao decompostos em
 *       relatores binarios, cada um reificando um fato nomeavel;
 *   A9  DataManager e View deixam de especializar ProjectObservatory e passam
 *       a ser componentes dele, especializando Software.
 *
 * O que NAO muda aqui, e por que: A5 (ETL como evento), A6 (taxonomia de
 * agentes) e A7 (kind sob System) sao do ticket 05, que adota UFO-B e UFO-C.
 * As definicoes ausentes (B3) e os axiomas de disjuncao fora da particao de
 * CrudOperation (B4) sao da customizacao da OWL, ticket 06.
 *
 * Convencoes identicas as de `modelo-as-is.js`: em meronimicas `source` e a
 * PARTE e `target` e o TODO; em mediacoes `source` e o RELATOR; a cardinalidade
 * de uma extremidade e o rotulo desenhado ao lado da classe daquela
 * extremidade.
 */

const { Project, OntologicalNature } = require('ontouml-js');

/** Classes do modelo revisado, agrupadas por camada. */
const CLASSES = [
  // Camada Agentes
  ['ObservatoryGroup', 'collective'],
  ['ObservatoryUser', 'role'],
  ['StakeHolder', 'role'],
  ['System', 'role'],
  ['Agent', 'kind'],
  ['Knowledge', 'kind'],
  ['Observation', 'relator'],
  ['SocialInteraction', 'relator'],
  ['Log', 'relator'],
  ['CrudOperation', 'relator'],
  // A1: as quatro operacoes que CrudOperation colapsava
  ['CreateOperation', 'subkind'],
  ['ReadOperation', 'subkind'],
  ['UpdateOperation', 'subkind'],
  ['DeleteOperation', 'subkind'],
  // Camada Estruturas - Componentes, Conteudos e Caracteristicas
  ['CrudRepository', 'role'],
  ['Project', 'kind'],
  ['Disseminator', 'role'],
  ['Reporter', 'role'], // A4: era `Relator`
  ['CrudView', 'role'],
  ['DataManager', 'role'],
  ['View', 'role'],
  // A8: Management (ternario) decomposto em dois relatores binarios
  ['ProjectDataManagement', 'relator'],
  ['ViewProvision', 'relator'],
  ['Collector', 'role'],
  ['Processor', 'role'],
  ['Storer', 'role'],
  ['Extract', 'relator'],
  ['Transform', 'relator'],
  ['Load', 'relator'],
  ['DataSource', 'kind'],
  ['ProjectObservatory', 'subkind'],
  // Camada Estruturas - Infraestrutura de TI
  ['Software', 'kind'],
  ['Service', 'kind'],
  ['Hardware', 'kind'],
  // A2 e A8: Operation (quaternario) decomposto; SoftwareExecution e tambem a
  // relacao de execucao que substitui a «componentOf» invalida
  ['SoftwareExecution', 'relator'],
  ['ServiceProvision', 'relator'],
  ['Connection', 'relator'],
  ['Network', 'kind'],
];

/**
 * A natureza ontologica dos subkinds que nao sao complexo funcional. Os quatro
 * subkinds de CrudOperation especializam um «relator» e portanto precisam da
 * natureza `relator`; sem isso a generalizacao fica com naturezas
 * incompativeis e o verificador acusa.
 */
const NATUREZAS = {
  CreateOperation: OntologicalNature.relator,
  ReadOperation: OntologicalNature.relator,
  UpdateOperation: OntologicalNature.relator,
  DeleteOperation: OntologicalNature.relator,
};

/** Generalizacoes, como [geral, especifico]. */
const GENERALIZACOES = [
  ['Agent', 'ObservatoryUser'],
  ['Agent', 'StakeHolder'],
  ['Agent', 'System'],
  // A1
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
  // A9: DataManager e View sao papeis de componentes de software, nao
  // especializacoes do observatorio
  ['Software', 'DataManager'],
  ['Software', 'View'],
  ['Software', 'ProjectObservatory'],
];

/**
 * A1: a particao de CrudOperation, como [nome, geral, especificos]. Disjunta e
 * completa — toda operacao e exatamente uma das quatro, e as quatro esgotam o
 * construto que o nome do original anunciava.
 */
const PARTICOES = [
  [
    'crudOperationType',
    'CrudOperation',
    ['CreateOperation', 'ReadOperation', 'UpdateOperation', 'DeleteOperation'],
  ],
];

/**
 * Meronimicas, como [estereotipo, parte, cardParte, todo, cardTodo].
 *
 * A3: nas tres «memberOf» o todo agora e `ObservatoryGroup`, o coletivo, e o
 * minimo na ponta do membro e 1 — um coletivo sem membro nenhum nao e um
 * coletivo. A `1` do lado do grupo e a que os diagramas trazem e foi mantida.
 *
 * A9: `DataManager` e `View` viram componentes do observatorio. «componentOf»
 * entre complexos funcionais, com o todo em `ProjectObservatory`.
 */
const MERONIMICAS = [
  ['memberOf', 'ObservatoryUser', '1..*', 'ObservatoryGroup', '1'],
  ['memberOf', 'StakeHolder', '1..*', 'ObservatoryGroup', '1'],
  ['memberOf', 'System', '1..*', 'ObservatoryGroup', '1'],
  ['componentOf', 'DataManager', '1..*', 'ProjectObservatory', '1'],
  ['componentOf', 'View', '1..*', 'ProjectObservatory', '1'],
];

/** Mediacoes, como [relator, cardRelator, mediado, cardMediado]. */
const MEDIACOES = [
  // Camada Agentes
  ['Observation', '1..*', 'Knowledge', '1..*'],
  ['Observation', '0..*', 'Agent', '1'],
  ['Observation', '0..*', 'Disseminator', '1'],
  ['SocialInteraction', '0..*', 'Agent', '1'],
  ['SocialInteraction', '0..*', 'Reporter', '1'],
  ['Log', '0..*', 'Agent', '1'],
  ['Log', '0..*', 'Reporter', '1'],
  ['CrudOperation', '0..*', 'Agent', '1'],
  ['CrudOperation', '0..*', 'CrudView', '1'],
  // Camada Estruturas - organizacao do observatorio
  ['ProjectDataManagement', '0..*', 'DataManager', '1'],
  ['ProjectDataManagement', '0..*', 'Project', '1'],
  ['ViewProvision', '0..*', 'DataManager', '1'],
  ['ViewProvision', '0..*', 'View', '1'],
  ['Extract', '1..*', 'Collector', '1'],
  ['Extract', '1..*', 'DataSource', '1'],
  ['Transform', '1..*', 'Collector', '1'],
  ['Transform', '1..*', 'Processor', '1'],
  ['Load', '1..*', 'Processor', '1'],
  ['Load', '1..*', 'Storer', '1'],
  // Camada Estruturas - infraestrutura de TI.
  //
  // O `1..*` na ponta do relator diz o que a «componentOf» de A2 dizia errado:
  // um software depende de hardware para se manifestar, e portanto participa
  // de ao menos uma execucao. O `0..*` na ponta de Hardware desfaz o resto do
  // defeito — hardware que nao executa software nenhum (um switch, um nobreak)
  // volta a caber no dominio. O mesmo par vale para o servico, que so existe
  // provido, e para o software, que pode nao prover nenhum.
  ['SoftwareExecution', '1..*', 'Software', '1'],
  ['SoftwareExecution', '0..*', 'Hardware', '1'],
  ['ServiceProvision', '1..*', 'Service', '1'],
  ['ServiceProvision', '0..*', 'Software', '1'],
  ['Connection', '0..*', 'Hardware', '1'],
  ['Connection', '0..*', 'Network', '1'],
];

/**
 * A2: a relacao que substitui a «componentOf» invalida. Uma material entre
 * `Software` e `Hardware`, derivada do relator `SoftwareExecution` — o
 * hardware executa o software, nao o compoe. Como [origem, cardOrigem,
 * destino, cardDestino, relatorQueADeriva].
 */
const MATERIAIS = [['Software', '0..*', 'Hardware', '1..*', 'SoftwareExecution']];

const CRIADOR_POR_ESTEREOTIPO = {
  kind: 'createKind',
  subkind: 'createSubkind',
  role: 'createRole',
  collective: 'createCollective',
  relator: 'createRelator',
};

/** Mesma regra de nomeacao do baseline, para que os IRIs sejam comparaveis. */
function nomeDaRelacao(estereotipo, origem, destino) {
  return `${estereotipo}_${origem}_${destino}`;
}

function construirModeloRodada1() {
  const projeto = new Project();
  projeto.setName('OntoMPO (revisado, rodada 1)');
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

  for (const [relator, cardRelator, mediado, cardMediado] of MEDIACOES) {
    const relacao = modelo.createMediationRelation(
      porNome[relator],
      porNome[mediado],
      nomeDaRelacao('mediation', relator, mediado),
    );
    relacao.getSourceEnd().cardinality.value = cardRelator;
    relacao.getTargetEnd().cardinality.value = cardMediado;
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
  MATERIAIS,
  construirModeloRodada1,
};
