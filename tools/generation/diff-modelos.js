/**
 * Diff estrutural entre dois modelos da OntoMPO.
 *
 * A secao de analise ontologica do artigo precisa de um par antes/depois por
 * correcao. Escrever esses pares a mao convida a divergencia: o modelo muda, a
 * tabela nao. Aqui eles sao derivados dos dois modelos a cada execucao, de
 * modo que `artifacts/ontology/correcoes-rodada-N.md` possa argumentar sobre
 * uma tabela que nao pode estar errada sobre os fatos.
 *
 * Cada rodada compara com a anterior, e nao com o baseline: o antes/depois que
 * a rodada tem de justificar e o que ela mesma mudou. A distancia acumulada
 * ate o *as-is* esta nos relatorios dos verificadores, que rodam sobre os tres
 * modelos.
 *
 * Uso: `node tools/generation/diff-modelos.js [--de=as-is] [--para=rodada-1] [arquivo-de-saida]`
 */

const fs = require('fs');
const path = require('path');

const { construirModeloAsIs } = require('../model/ontompo-as-is');
const { construirModeloRodada1 } = require('../model/ontompo-rodada-1');
const { construirModeloRodada2 } = require('../model/ontompo-rodada-2');

const MODELOS = {
  'as-is': { construir: construirModeloAsIs, rotulo: '*as-is*' },
  'rodada-1': { construir: construirModeloRodada1, rotulo: 'rodada 1' },
  'rodada-2': { construir: construirModeloRodada2, rotulo: 'rodada 2' },
};

const RAIZ = path.resolve(__dirname, '..', '..');

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

function secaoDeDiff(titulo, antes, depois, rotulos) {
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
  linhas.push(`| | Elemento | ${rotulos.antes} | ${rotulos.depois} |`, '|---|---|---|---|');
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
  const argumentos = process.argv.slice(2);
  const opcao = (prefixo, padrao) =>
    (argumentos.find((a) => a.startsWith(`${prefixo}=`)) || `=${padrao}`).split('=')[1];

  const de = opcao('--de', 'as-is');
  const para = opcao('--para', 'rodada-1');
  for (const escolha of [de, para]) {
    if (!MODELOS[escolha]) {
      console.log(`modelo desconhecido: ${escolha}. Use ${Object.keys(MODELOS).join(', ')}.`);
      process.exitCode = 1;
      return;
    }
  }

  const posicional = argumentos.find((a) => !a.startsWith('--'));
  const caminhoSaida = posicional
    ? path.resolve(posicional)
    : path.join(RAIZ, 'artifacts', 'ontology', para, `diff-${de}-${para}.md`);

  const rotulos = { antes: MODELOS[de].rotulo, depois: MODELOS[para].rotulo };
  const antes = MODELOS[de].construir();
  const depois = MODELOS[para].construir();

  const linhas = [
    `# Diff estrutural: ${rotulos.antes} -> ${rotulos.depois}`,
    '',
    'Derivado dos dois modelos a cada execucao de `tools/generation/diff-modelos.js`. E a ' +
      'materia-prima dos pares antes/depois; a leitura ontologica de cada um esta em ' +
      `\`../correcoes-${para}.md\`.`,
    '',
    '## Contagens',
    '',
    `| | ${rotulos.antes} | ${rotulos.depois} |`,
    '|---|---|---|',
    `| classes | ${antes.getAllClasses().length} | ${depois.getAllClasses().length} |`,
    `| generalizacoes | ${antes.getAllGeneralizations().length} | ${depois.getAllGeneralizations().length} |`,
    `| conjuntos de generalizacao | ${antes.getAllGeneralizationSets().length} | ${depois.getAllGeneralizationSets().length} |`,
    `| relacoes | ${antes.getAllRelations().length} | ${depois.getAllRelations().length} |`,
    '',
    '## Mudancas',
    '',
    ...secaoDeDiff('Classes', classes(antes), classes(depois), rotulos),
    ...secaoDeDiff('Generalizacoes', generalizacoes(antes), generalizacoes(depois), rotulos),
    ...secaoDeDiff('Conjuntos de generalizacao', conjuntos(antes), conjuntos(depois), rotulos),
    ...secaoDeDiff('Relacoes', relacoes(antes), relacoes(depois), rotulos),
  ];

  fs.mkdirSync(path.dirname(caminhoSaida), { recursive: true });
  fs.writeFileSync(caminhoSaida, `${linhas.join('\n')}\n`, 'utf-8');
  console.log(`diff -> ${caminhoSaida}`);
}

principal();
