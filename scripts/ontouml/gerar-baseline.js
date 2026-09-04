/**
 * Gera os artefatos de baseline do ticket 03 a partir do modelo *as-is*:
 *
 *   1. `ontompo-as-is.ontouml.json` — o modelo no OntoUML Schema, que e o
 *      formato de intercambio do plugin OntoUML para o Visual Paradigm;
 *   2. `relatorio-plugin-ontouml.json` e `.md` — a saida da verificacao
 *      sintatica e semantica contra a UFO, que e o mesmo motor que o plugin
 *      executa (`OntoumlVerification`, da ontouml-js);
 *   3. `ontompo-as-is.ttl` — a OWL de baseline, pela transformacao gUFO
 *      oficial (`Ontouml2Gufo`, da mesma biblioteca).
 *
 * Uso: `node scripts/ontouml/gerar-baseline.js [diretorio-de-saida]`
 *
 * Os identificadores dos elementos sao reescritos de forma deterministica
 * antes da serializacao. A ontouml-js gera ids aleatorios, e sem isso cada
 * execucao produziria um JSON diferente do anterior sem que nada no modelo
 * tivesse mudado — o que inviabiliza tanto o diff contra o modelo revisado do
 * ticket 04 quanto a conferencia de que o deposito corresponde ao que o artigo
 * descreve.
 */

const fs = require('fs');
const path = require('path');

const { OntoumlVerification, Ontouml2Gufo } = require('ontouml-js');
const { construirModeloAsIs } = require('./modelo-as-is');

const SAIDA_PADRAO = path.resolve(__dirname, '..', '..', 'ontologia', 'baseline');

const IRI_BASE = 'https://example.org/ontompo/as-is';
const PREFIXO_BASE = 'ontompo';

/** Reescreve os ids aleatorios da ontouml-js por ids derivados dos nomes. */
function fixarIdentificadores(projeto) {
  projeto.id = 'ontompo-as-is';
  const modelo = projeto.model;
  modelo.id = 'pkg_OntoMPO';

  for (const classe of projeto.getAllClasses()) {
    classe.id = `cls_${classe.getName()}`;
  }

  for (const relacao of projeto.getAllRelations()) {
    relacao.id = `rel_${relacao.getName()}`;
    relacao.properties.forEach((ponta, indice) => {
      ponta.id = `end_${relacao.getName()}_${indice}`;
    });
  }

  for (const generalizacao of projeto.getAllGeneralizations()) {
    generalizacao.id = `gen_${generalizacao.general.getName()}_${generalizacao.specific.getName()}`;
  }
}

/** Falha cedo se alguma multiplicidade transcrita dos diagramas for invalida. */
function conferirCardinalidades(projeto) {
  const invalidas = [];
  for (const relacao of projeto.getAllRelations()) {
    for (const ponta of relacao.properties) {
      if (!ponta.cardinality.isValid()) {
        invalidas.push(`${relacao.getName()} / ${ponta.propertyType.getName()}: ${ponta.cardinality.value}`);
      }
    }
  }
  if (invalidas.length > 0) {
    throw new Error(`Multiplicidades invalidas:\n  ${invalidas.join('\n  ')}`);
  }
}

function nomeDoElemento(dados) {
  if (!dados || !dados.source) return '(projeto)';
  const fonte = dados.source;
  const nome = typeof fonte.name === 'string' ? fonte.name : fonte.name && fonte.name.en;
  return nome || fonte.id || '(sem nome)';
}

function relatorioDaVerificacaoEmMarkdown(problemas, projeto) {
  const linhas = [];
  linhas.push('# Relatorio do plugin OntoUML sobre o modelo *as-is*');
  linhas.push('');
  linhas.push(
    'Verificacao sintatica e semantica contra a UFO, executada pelo `OntoumlVerification` ' +
      'da `ontouml-js` 0.5.0 — o mesmo motor que o plugin OntoUML para o Visual Paradigm ' +
      'invoca. Saida bruta em `relatorio-plugin-ontouml.json`.',
  );
  linhas.push('');
  linhas.push(`- Classes verificadas: ${projeto.getAllClasses().length}`);
  linhas.push(`- Relacoes verificadas: ${projeto.getAllRelations().length}`);
  linhas.push(`- Generalizacoes verificadas: ${projeto.getAllGeneralizations().length}`);
  linhas.push(`- Problemas encontrados: ${problemas.length}`);
  linhas.push('');

  if (problemas.length === 0) {
    linhas.push('Nenhum problema encontrado.');
  } else {
    const porSeveridade = {};
    for (const problema of problemas) {
      porSeveridade[problema.severity] = (porSeveridade[problema.severity] || 0) + 1;
    }
    linhas.push(
      `Por severidade: ${Object.entries(porSeveridade)
        .map(([severidade, quantidade]) => `${severidade} ${quantidade}`)
        .join(', ')}.`,
    );
    linhas.push('');
    linhas.push('| # | Severidade | Codigo | Elemento | Descricao |');
    linhas.push('|---|---|---|---|---|');
    problemas.forEach((problema, indice) => {
      const descricao = String(problema.description || problema.title).replace(/\|/g, '\\|');
      linhas.push(
        `| ${indice + 1} | ${problema.severity} | \`${problema.code}\` | ` +
          `${nomeDoElemento(problema.data)} | ${descricao} |`,
      );
    });
  }

  linhas.push('');
  linhas.push('## O que este relatorio nao cobre');
  linhas.push('');
  linhas.push(
    'O conjunto de regras do verificador tem 24 codigos, todos sobre estereotipos de ' +
      'classe, provedores de identidade, naturezas e generalizacoes. **Nenhum deles trata ' +
      'de restricoes meronimicas** — nao ha regra que exija que o todo de uma «memberOf» ' +
      'seja um coletivo, nem que uma «componentOf» ligue complexos funcionais. Deficiencias ' +
      'dessa classe, como A2 e A3, precisam ser sustentadas por argumento ontologico ' +
      'explicito; estao em `../evidencias-A1-A9.md`.',
  );
  linhas.push('');
  return linhas.join('\n');
}

function principal() {
  const diretorioSaida = process.argv[2] ? path.resolve(process.argv[2]) : SAIDA_PADRAO;
  fs.mkdirSync(diretorioSaida, { recursive: true });

  const projeto = construirModeloAsIs();
  conferirCardinalidades(projeto);
  fixarIdentificadores(projeto);

  const caminhoModelo = path.join(diretorioSaida, 'ontompo-as-is.ontouml.json');
  fs.writeFileSync(caminhoModelo, `${JSON.stringify(projeto, null, 2)}\n`, 'utf-8');

  const problemas = OntoumlVerification.verify(projeto);
  fs.writeFileSync(
    path.join(diretorioSaida, 'relatorio-plugin-ontouml.json'),
    `${JSON.stringify(problemas, null, 2)}\n`,
    'utf-8',
  );
  fs.writeFileSync(
    path.join(diretorioSaida, 'relatorio-plugin-ontouml.md'),
    relatorioDaVerificacaoEmMarkdown(problemas, projeto),
    'utf-8',
  );

  const transformacao = new Ontouml2Gufo(projeto, {
    baseIri: IRI_BASE,
    basePrefix: PREFIXO_BASE,
    format: 'Turtle',
    uriFormatBy: 'name',
    createObjectProperty: true,
    createInverses: false,
    prefixPackages: false,
  });
  transformacao.transform();

  const problemasGufo = transformacao.getIssues() || [];
  fs.writeFileSync(path.join(diretorioSaida, 'ontompo-as-is.ttl'), transformacao.getOwlCode(), 'utf-8');

  console.log(`modelo OntoUML   -> ${caminhoModelo}`);
  console.log(`classes ${projeto.getAllClasses().length}, relacoes ${projeto.getAllRelations().length}, generalizacoes ${projeto.getAllGeneralizations().length}`);
  console.log(`verificacao      -> ${problemas.length} problema(s)`);
  for (const problema of problemas) {
    console.log(`  [${problema.severity}] ${problema.code}: ${nomeDoElemento(problema.data)}`);
  }
  console.log(`transformacao gUFO -> ${problemasGufo.length} problema(s)`);
  for (const problema of problemasGufo) {
    console.log(`  ${JSON.stringify(problema)}`);
  }
}

principal();
