/**
 * Diff estrutural entre o modelo *as-is* e o da rodada 1.
 *
 * A secao de analise ontologica do artigo precisa de um par antes/depois por
 * correcao. Escrever esses pares a mao convida a divergencia: o modelo muda, a
 * tabela nao. Aqui eles sao derivados dos dois modelos a cada execucao, de
 * modo que `artifacts/ontology/correcoes-rodada-1.md` possa argumentar sobre uma
 * tabela que nao pode estar errada sobre os fatos.
 *
 * Uso: `node tools/generation/diff-modelos.js [arquivo-de-saida]`
 */

const fs = require('fs');
const path = require('path');

const { construirModeloAsIs } = require('../model/ontompo-as-is');
const { construirModeloRodada1 } = require('../model/ontompo-rodada-1');

const SAIDA_PADRAO = path.resolve(
  __dirname,
  '..',
  '..',
  'artifacts',
  'ontology',
  'rodada-1',
  'diff-as-is-rodada-1.md',
);

function classes(projeto) {
  return new Map(
    projeto.getAllClasses().map((classe) => [classe.getName(), `«${classe.stereotype}»`]),
  );
}

function generalizacoes(projeto) {
  return new Map(
    projeto
      .getAllGeneralizations()
      .map((g) => [
        `${g.specific.getName()} -> ${g.general.getName()}`,
        `${g.specific.getName()} especializa ${g.general.getName()}`,
      ]),
  );
}

function relacoes(projeto) {
  return new Map(
    projeto.getAllRelations().map((relacao) => {
      const [origem, destino] = relacao.properties;
      const losango = (ponta) =>
        ponta.aggregationKind && ponta.aggregationKind !== 'NONE' ? ' (todo)' : '';
      return [
        relacao.getName(),
        `«${relacao.stereotype}» ${origem.propertyType.getName()} ` +
          `[${origem.cardinality.value}]${losango(origem)} -> ` +
          `${destino.propertyType.getName()} [${destino.cardinality.value}]${losango(destino)}`,
      ];
    }),
  );
}

function conjuntos(projeto) {
  return new Map(
    projeto.getAllGeneralizationSets().map((conjunto) => {
      const especificos = conjunto.getSpecifics().map((c) => c.getName());
      const geral = conjunto.getGeneral().getName();
      const qualificadores = [
        conjunto.isDisjoint ? 'disjunta' : 'sobreposta',
        conjunto.isComplete ? 'completa' : 'incompleta',
      ].join(', ');
      return [conjunto.getName(), `${geral}: ${especificos.join(', ')} (${qualificadores})`];
    }),
  );
}

function secaoDeDiff(titulo, antes, depois) {
  const removidos = [...antes.keys()].filter((chave) => !depois.has(chave));
  const acrescentados = [...depois.keys()].filter((chave) => !antes.has(chave));
  const alterados = [...antes.keys()].filter(
    (chave) => depois.has(chave) && antes.get(chave) !== depois.get(chave),
  );

  const linhas = [`### ${titulo}`, ''];
  if (removidos.length + acrescentados.length + alterados.length === 0) {
    linhas.push('Sem mudanca.', '');
    return linhas;
  }
  linhas.push('| | Elemento | *as-is* | rodada 1 |', '|---|---|---|---|');
  for (const chave of removidos) {
    linhas.push(`| sai | \`${chave}\` | ${antes.get(chave)} | — |`);
  }
  for (const chave of alterados) {
    linhas.push(`| muda | \`${chave}\` | ${antes.get(chave)} | ${depois.get(chave)} |`);
  }
  for (const chave of acrescentados) {
    linhas.push(`| entra | \`${chave}\` | — | ${depois.get(chave)} |`);
  }
  linhas.push('');
  return linhas;
}

function principal() {
  const caminhoSaida = process.argv[2] ? path.resolve(process.argv[2]) : SAIDA_PADRAO;

  const antes = construirModeloAsIs();
  const depois = construirModeloRodada1();

  const linhas = [
    '# Diff estrutural: *as-is* -> rodada 1',
    '',
    'Derivado dos dois modelos a cada execucao de `tools/generation/diff-modelos.js`. E a ' +
      'materia-prima dos pares antes/depois; a leitura ontologica de cada um esta em ' +
      '`../correcoes-rodada-1.md`.',
    '',
    '## Contagens',
    '',
    '| | *as-is* | rodada 1 |',
    '|---|---|---|',
    `| classes | ${antes.getAllClasses().length} | ${depois.getAllClasses().length} |`,
    `| generalizacoes | ${antes.getAllGeneralizations().length} | ${depois.getAllGeneralizations().length} |`,
    `| conjuntos de generalizacao | ${antes.getAllGeneralizationSets().length} | ${depois.getAllGeneralizationSets().length} |`,
    `| relacoes | ${antes.getAllRelations().length} | ${depois.getAllRelations().length} |`,
    '',
    '## Mudancas',
    '',
    ...secaoDeDiff('Classes', classes(antes), classes(depois)),
    ...secaoDeDiff('Generalizacoes', generalizacoes(antes), generalizacoes(depois)),
    ...secaoDeDiff('Conjuntos de generalizacao', conjuntos(antes), conjuntos(depois)),
    ...secaoDeDiff('Relacoes', relacoes(antes), relacoes(depois)),
  ];

  fs.mkdirSync(path.dirname(caminhoSaida), { recursive: true });
  fs.writeFileSync(caminhoSaida, `${linhas.join('\n')}\n`, 'utf-8');
  console.log(`diff -> ${caminhoSaida}`);
}

principal();
