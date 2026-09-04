/**
 * Controle do verificador: prova que o relatorio vazio do plugin e um
 * resultado, e nao um cano entupido.
 *
 * O `OntoumlVerification` nao acusa nenhum problema — nem no modelo *as-is*
 * nem no revisado. Sozinha, essa saida e ambigua: nao distingue "o modelo
 * passa nas 24 regras" de "a verificacao nem chegou a rodar". Este script
 * desfaz a ambiguidade: aplica mutacoes conhecidas ao mesmo modelo, pelo mesmo
 * caminho de codigo, e exige que cada uma seja acusada com o codigo esperado.
 *
 * Uso: `node tools/verification/controle-verificacao.js [--modelo=as-is|rodada-1] [saida]`
 * Sai com codigo 1 se alguma mutacao passar despercebida.
 */

const fs = require('fs');
const path = require('path');

const { OntoumlVerification } = require('ontouml-js');
const { construirModeloAsIs } = require('../model/ontompo-as-is');
const { construirModeloRodada1 } = require('../model/ontompo-rodada-1');

const RAIZ = path.resolve(__dirname, '..', '..');

function classe(projeto, nome) {
  const encontrada = projeto.getAllClasses().find((c) => c.getName() === nome);
  if (!encontrada) throw new Error(`classe ${nome} nao existe no modelo`);
  return encontrada;
}

/** Remove a generalizacao de `especifico` para `geral`. */
function removerGeneralizacao(projeto, geral, especifico) {
  const alvo = classe(projeto, especifico);
  const generalizacao = projeto
    .getAllGeneralizations()
    .find((g) => g.specific === alvo && g.general.getName() === geral);
  projeto.model.removeContent(generalizacao);
}

const MUTACAO_SEM_PROVEDOR = {
  nome: 'System perde a generalizacao para Agent',
  esperado: 'class_missing_identity_provider',
  porque: 'um sortal sem sortal ultimo acima dele fica sem principio de identidade',
  aplicar: (projeto) => removerGeneralizacao(projeto, 'Agent', 'System'),
};

const MUTACAO_DOIS_PROVEDORES = {
  nome: 'ProjectObservatory passa a especializar tambem Project',
  esperado: 'class_multiple_identity_providers',
  porque: 'duas ancestralidades ate sortais ultimos distintos dao dois principios de identidade',
  aplicar(projeto) {
    projeto.model.createGeneralization(
      classe(projeto, 'Project'),
      classe(projeto, 'ProjectObservatory'),
    );
  },
};

const MODELOS = {
  'as-is': {
    construir: construirModeloAsIs,
    saida: path.join(RAIZ, 'artifacts', 'ontology', 'baseline', 'controle-verificacao.md'),
    descricao: 'o modelo *as-is*',
    mutacoes: [
      MUTACAO_SEM_PROVEDOR,
      {
        nome: 'Software passa a especializar View',
        esperado: 'generalization_incompatible_class_rigidity',
        porque: 'um tipo rigido nao pode especializar um tipo antirrigido',
        aplicar(projeto) {
          projeto.model.createGeneralization(classe(projeto, 'View'), classe(projeto, 'Software'));
        },
      },
      MUTACAO_DOIS_PROVEDORES,
    ],
  },
  'rodada-1': {
    construir: construirModeloRodada1,
    saida: path.join(RAIZ, 'artifacts', 'ontology', 'rodada-1', 'controle-verificacao.md'),
    descricao: 'o modelo revisado (rodada 1)',
    mutacoes: [
      MUTACAO_SEM_PROVEDOR,
      {
        // A do baseline nao serve aqui: depois de A9, `View` ja especializa
        // `Software`, e a mutacao fecharia um ciclo em vez de violar rigidez.
        nome: 'Hardware passa a especializar DataManager',
        esperado: 'generalization_incompatible_class_rigidity',
        porque: 'um tipo rigido nao pode especializar um tipo antirrigido',
        aplicar(projeto) {
          projeto.model.createGeneralization(
            classe(projeto, 'DataManager'),
            classe(projeto, 'Hardware'),
          );
        },
      },
      MUTACAO_DOIS_PROVEDORES,
    ],
  },
};

function principal() {
  const argumentos = process.argv.slice(2);
  const escolha = (argumentos.find((a) => a.startsWith('--modelo=')) || '').split('=')[1] || 'as-is';
  const configuracao = MODELOS[escolha];
  if (!configuracao) {
    console.log(`modelo desconhecido: ${escolha}. Use ${Object.keys(MODELOS).join(' ou ')}.`);
    process.exitCode = 1;
    return;
  }

  const posicional = argumentos.find((a) => !a.startsWith('--'));
  const caminhoSaida = posicional ? path.resolve(posicional) : configuracao.saida;

  const semMutacao = OntoumlVerification.verify(configuracao.construir());

  const resultados = configuracao.mutacoes.map((mutacao) => {
    const projeto = configuracao.construir();
    mutacao.aplicar(projeto);
    const problemas = OntoumlVerification.verify(projeto);
    const codigos = problemas.map((p) => p.code);
    return { ...mutacao, codigos, detectada: codigos.includes(mutacao.esperado) };
  });

  const linhas = [
    '# Controle do verificador OntoUML',
    '',
    `O relatorio do plugin sobre ${configuracao.descricao} nao acusa nenhum problema. Este ` +
      'controle existe para que esse zero seja lido como resultado, e nao como falha de ' +
      'execucao: as mutacoes abaixo sao aplicadas ao mesmo modelo, pelo mesmo caminho de ' +
      'codigo, e cada uma precisa ser acusada com o codigo esperado.',
    '',
    `Modelo sem mutacao: ${semMutacao.length} problema(s).`,
    '',
    '| Mutacao | Codigo esperado | Por que deveria falhar | Acusada |',
    '|---|---|---|---|',
  ];
  for (const resultado of resultados) {
    linhas.push(
      `| ${resultado.nome} | \`${resultado.esperado}\` | ${resultado.porque} | ` +
        `${resultado.detectada ? 'sim' : '**NAO**'} |`,
    );
  }
  linhas.push('');
  linhas.push(
    `Reproduzir com \`node tools/verification/controle-verificacao.js --modelo=${escolha}\`.`,
  );
  linhas.push('');

  fs.mkdirSync(path.dirname(caminhoSaida), { recursive: true });
  fs.writeFileSync(caminhoSaida, linhas.join('\n'), 'utf-8');

  const falhas = resultados.filter((r) => !r.detectada);
  for (const resultado of resultados) {
    console.log(
      `${resultado.detectada ? 'ok  ' : 'FALHA'} ${resultado.nome} -> [${resultado.codigos.join(', ')}]`,
    );
  }
  console.log(`controle -> ${caminhoSaida}`);

  if (falhas.length > 0) {
    console.log(
      `${falhas.length} mutacao(oes) nao detectada(s): o relatorio vazio do verificador nao pode ser interpretado.`,
    );
    process.exitCode = 1;
  }
}

principal();
