/**
 * Controle do verificador: prova que o relatorio vazio do baseline e um
 * resultado, e nao um cano entupido.
 *
 * O `OntoumlVerification` nao acusa nenhum problema no modelo *as-is*. Sozinha,
 * essa saida e ambigua — nao distingue "o modelo passa nas 24 regras" de "a
 * verificacao nem chegou a rodar". Este script desfaz a ambiguidade: aplica
 * mutacoes conhecidas ao mesmo modelo e exige que cada uma seja acusada com o
 * codigo esperado.
 *
 * Uso: `node scripts/ontouml/controle-verificacao.js [arquivo-de-saida]`
 * Sai com codigo 1 se alguma mutacao passar despercebida.
 */

const fs = require('fs');
const path = require('path');

const { OntoumlVerification } = require('ontouml-js');
const { construirModeloAsIs } = require('./modelo-as-is');

const SAIDA_PADRAO = path.resolve(__dirname, '..', '..', 'ontologia', 'baseline', 'controle-verificacao.md');

function classe(projeto, nome) {
  const encontrada = projeto.getAllClasses().find((c) => c.getName() === nome);
  if (!encontrada) throw new Error(`classe ${nome} nao existe no modelo as-is`);
  return encontrada;
}

const MUTACOES = [
  {
    nome: 'System perde a generalizacao para Agent',
    esperado: 'class_missing_identity_provider',
    porque: 'um sortal sem sortal ultimo acima dele fica sem principio de identidade',
    aplicar(projeto) {
      const alvo = classe(projeto, 'System');
      const generalizacao = projeto
        .getAllGeneralizations()
        .find((g) => g.specific === alvo && g.general.getName() === 'Agent');
      projeto.model.removeContent(generalizacao);
    },
  },
  {
    nome: 'Software passa a especializar View',
    esperado: 'generalization_incompatible_class_rigidity',
    porque: 'um tipo rigido nao pode especializar um tipo antirrigido',
    aplicar(projeto) {
      projeto.model.createGeneralization(classe(projeto, 'View'), classe(projeto, 'Software'));
    },
  },
  {
    nome: 'ProjectObservatory passa a especializar tambem Project',
    esperado: 'class_multiple_identity_providers',
    porque: 'duas ancestralidades ate sortais ultimos distintos dao dois principios de identidade',
    aplicar(projeto) {
      projeto.model.createGeneralization(classe(projeto, 'Project'), classe(projeto, 'ProjectObservatory'));
    },
  },
];

function principal() {
  const caminhoSaida = process.argv[2] ? path.resolve(process.argv[2]) : SAIDA_PADRAO;

  const semMutacao = OntoumlVerification.verify(construirModeloAsIs());

  const resultados = MUTACOES.map((mutacao) => {
    const projeto = construirModeloAsIs();
    mutacao.aplicar(projeto);
    const problemas = OntoumlVerification.verify(projeto);
    const codigos = problemas.map((p) => p.code);
    return { ...mutacao, codigos, detectada: codigos.includes(mutacao.esperado) };
  });

  const linhas = [
    '# Controle do verificador OntoUML',
    '',
    'O relatorio do plugin sobre o modelo *as-is* nao acusa nenhum problema. Este controle ' +
      'existe para que esse zero seja lido como resultado, e nao como falha de execucao: as ' +
      'mutacoes abaixo sao aplicadas ao mesmo modelo, pelo mesmo caminho de codigo, e cada ' +
      'uma precisa ser acusada com o codigo esperado.',
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
  linhas.push('Reproduzir com `node scripts/ontouml/controle-verificacao.js`.');
  linhas.push('');

  fs.mkdirSync(path.dirname(caminhoSaida), { recursive: true });
  fs.writeFileSync(caminhoSaida, linhas.join('\n'), 'utf-8');

  const falhas = resultados.filter((r) => !r.detectada);
  for (const resultado of resultados) {
    console.log(`${resultado.detectada ? 'ok  ' : 'FALHA'} ${resultado.nome} -> [${resultado.codigos.join(', ')}]`);
  }
  console.log(`controle -> ${caminhoSaida}`);

  if (falhas.length > 0) {
    console.log(`${falhas.length} mutacao(oes) nao detectada(s): o relatorio vazio do baseline nao pode ser interpretado.`);
    process.exitCode = 1;
  }
}

principal();
