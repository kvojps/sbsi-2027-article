/**
 * Reconstrucao do modelo OntoUML da OntoMPO **exatamente como publicado**.
 *
 * Fonte: os diagramas em resolucao de origem da dissertacao, em
 * `sources/dissertation/imagens/`. O diagrama integrado `mpo_formalization.png`
 * e superconjunto dos tres diagramas por camada e foi a fonte primaria; os
 * diagramas por camada (`mpo_agents_formalization.png`,
 * `mpo_structures_observatory_formalization.png` e
 * `mpo_structures_observatory_infra_formalization.png`) foram lidos em
 * ampliacao para desempatar extremidades de agregacao e multiplicidades que o
 * diagrama integrado renderiza em poucos pixels.
 *
 * NADA e corrigido aqui. Os nove defeitos A1-A9 do spec, e tudo o mais que os
 * diagramas trazem, sao reproduzidos como estao. Este arquivo e a metade
 * "antes" do antes/depois do artigo; a metade "depois" e do ticket 04.
 *
 * Convencoes da ontouml-js usadas abaixo:
 *
 *   - `criarGeneralizacao(geral, especifico)`;
 *   - em relacoes meronimicas, `source` e a PARTE e `target` e o TODO (a
 *     extremidade de agregacao fica no `target`);
 *   - em mediacoes, `source` e o RELATOR e `target` e o mediado;
 *   - a cardinalidade de uma extremidade e o rotulo desenhado ao lado da
 *     classe daquela extremidade, como no UML.
 */

const { Project, AggregationKind } = require('ontouml-js');

/** Classes do modelo, na ordem em que aparecem no diagrama integrado. */
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
  // Camada Estruturas - subcamadas Componentes, Conteudos e Caracteristicas
  ['CrudRepository', 'role'],
  ['Project', 'kind'],
  ['Disseminator', 'role'],
  ['Relator', 'role'],
  ['CrudView', 'role'],
  ['DataManager', 'role'],
  ['Management', 'relator'],
  ['View', 'role'],
  ['Collector', 'role'],
  ['Processor', 'role'],
  ['Storer', 'role'],
  ['Extract', 'relator'],
  ['Transform', 'relator'],
  ['Load', 'relator'],
  ['DataSource', 'kind'],
  ['ProjectObservatory', 'subkind'],
  // Camada Estruturas - subcamada Infraestrutura de TI
  ['Software', 'kind'],
  ['Service', 'kind'],
  ['Hardware', 'kind'],
  ['Operation', 'relator'],
  ['Connection', 'relator'],
  ['Network', 'kind'],
];

/** Generalizacoes, como [geral, especifico]. */
const GENERALIZACOES = [
  ['Agent', 'ObservatoryUser'],
  ['Agent', 'StakeHolder'],
  ['Agent', 'System'],
  ['DataManager', 'CrudRepository'],
  ['DataManager', 'Collector'],
  ['DataManager', 'Processor'],
  ['DataManager', 'Storer'],
  ['View', 'Disseminator'],
  ['View', 'Relator'],
  ['View', 'CrudView'],
  ['ProjectObservatory', 'DataManager'],
  ['ProjectObservatory', 'View'],
  ['Software', 'ProjectObservatory'],
];

/**
 * Relacoes meronimicas, como [estereotipo, parte, cardParte, todo, cardTodo].
 *
 * As tres primeiras sao a evidencia de A3 e as duas primeiras a de A2. Repare
 * que o losango das relacoes com ObservatoryGroup esta desenhado do lado do
 * papel, e nao do lado do coletivo: o todo declarado e `ObservatoryUser` /
 * `StakeHolder`, e a parte declarada e `ObservatoryGroup`.
 */
const MERONIMICAS = [
  ['memberOf', 'ObservatoryGroup', '1', 'ObservatoryUser', '0..*'],
  ['memberOf', 'ObservatoryGroup', '1', 'StakeHolder', '0..*'],
  ['componentOf', 'Hardware', '1..*', 'Software', '1..*'],
];

/**
 * A terceira «MemberOf» da camada de agentes, entre ObservatoryGroup e System,
 * e desenhada **sem losango em nenhuma das duas pontas**: carrega o
 * estereotipo de agregacao sem designar todo nem parte. Nao e um descuido de
 * transcricao — o recorte ampliado de `mpo_agents_formalization.png` mostra a
 * linha chegando limpa na caixa de System. Fica registrada como esta.
 */
const MERONIMICA_SEM_AGREGACAO = ['memberOf', 'ObservatoryGroup', '1', 'System', '0..*'];

/** Mediacoes, como [relator, cardRelator, mediado, cardMediado]. */
const MEDIACOES = [
  // Camada Agentes
  ['Observation', '1..*', 'Knowledge', '1..*'],
  ['Observation', '0..*', 'Agent', '1'],
  ['Observation', '0..*', 'Disseminator', '1'],
  ['SocialInteraction', '0..*', 'Agent', '1'],
  ['SocialInteraction', '0..*', 'Relator', '1'],
  ['Log', '0..*', 'Agent', '1'],
  ['Log', '0..*', 'Relator', '1'],
  ['CrudOperation', '0..*', 'Agent', '1'],
  ['CrudOperation', '0..*', 'CrudView', '1'],
  // Camada Estruturas - organizacao do observatorio
  ['Management', '0..*', 'Project', '1'],
  ['Management', '0..*', 'DataManager', '1'],
  ['Management', '0..*', 'View', '1'],
  ['Extract', '1..*', 'Collector', '1'],
  ['Extract', '1..*', 'DataSource', '1'],
  ['Transform', '1..*', 'Collector', '1'],
  ['Transform', '1..*', 'Processor', '1'],
  ['Load', '1..*', 'Processor', '1'],
  ['Load', '1..*', 'Storer', '1'],
  // Camada Estruturas - infraestrutura de TI
  ['Operation', '0..*', 'Software', '0..*'],
  ['Operation', '0..*', 'Service', '1'],
  ['Operation', '0..*', 'Hardware', '0..*'],
  ['Operation', '0..*', 'Network', '0..*'],
  ['Connection', '0..*', 'Hardware', '1'],
  ['Connection', '0..*', 'Network', '1'],
];

const CRIADOR_POR_ESTEREOTIPO = {
  kind: 'createKind',
  subkind: 'createSubkind',
  role: 'createRole',
  collective: 'createCollective',
  relator: 'createRelator',
};

/**
 * Nomeia uma relacao. Os diagramas publicados nao trazem nome em nenhuma
 * associacao — so o estereotipo. Um nome deterministico e derivado das pontas
 * para que a transformacao gUFO produza IRIs estaveis entre execucoes, o que
 * torna o diff entre o baseline e o modelo revisado legivel. A ausencia de
 * nomes no original fica registrada no relatorio de evidencias.
 */
function nomeDaRelacao(estereotipo, origem, destino) {
  return `${estereotipo}_${origem}_${destino}`;
}

function construirModeloAsIs() {
  const projeto = new Project();
  projeto.setName('OntoMPO (as-is)');
  const modelo = projeto.createModel();
  modelo.setName('OntoMPO');

  const porNome = {};
  for (const [nome, estereotipo] of CLASSES) {
    porNome[nome] = modelo[CRIADOR_POR_ESTEREOTIPO[estereotipo]](nome);
  }

  for (const [geral, especifico] of GENERALIZACOES) {
    modelo.createGeneralization(porNome[geral], porNome[especifico]);
  }

  for (const [estereotipo, parte, cardParte, todo, cardTodo] of MERONIMICAS) {
    const criador = estereotipo === 'memberOf' ? 'createMemberOfRelation' : 'createComponentOfRelation';
    const relacao = modelo[criador](porNome[parte], porNome[todo], nomeDaRelacao(estereotipo, parte, todo));
    relacao.getSourceEnd().cardinality.value = cardParte;
    relacao.getTargetEnd().cardinality.value = cardTodo;
  }

  {
    const [estereotipo, parte, cardParte, todo, cardTodo] = MERONIMICA_SEM_AGREGACAO;
    const relacao = modelo.createMemberOfRelation(
      porNome[parte],
      porNome[todo],
      nomeDaRelacao(estereotipo, parte, todo),
    );
    relacao.getSourceEnd().cardinality.value = cardParte;
    relacao.getTargetEnd().cardinality.value = cardTodo;
    relacao.getTargetEnd().aggregationKind = AggregationKind.NONE;
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

  return projeto;
}

module.exports = {
  CLASSES,
  GENERALIZACOES,
  MERONIMICAS,
  MERONIMICA_SEM_AGREGACAO,
  MEDIACOES,
  construirModeloAsIs,
};
