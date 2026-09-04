/**
 * A maquinaria comum de geracao de artefatos, usada pelo baseline (ticket 03)
 * e por cada rodada de revisao. Para cada modelo produz:
 *
 *   1. `<nome>.ontouml.json` — o modelo no OntoUML Schema, que e o formato de
 *      intercambio do plugin OntoUML para o Visual Paradigm;
 *   2. `relatorio-plugin-ontouml.json` e `.md` — a saida da verificacao
 *      sintatica e semantica contra a UFO, pelo mesmo motor que o plugin
 *      executa (`OntoumlVerification`, da ontouml-js);
 *   3. `<nome>.ttl` — a OWL pela transformacao gUFO oficial (`Ontouml2Gufo`).
 *
 * Os identificadores dos elementos sao reescritos de forma deterministica
 * antes da serializacao. A ontouml-js gera ids aleatorios, e sem isso cada
 * execucao produziria um JSON diferente do anterior sem que nada no modelo
 * tivesse mudado — o que inviabiliza tanto o diff entre as rodadas quanto a
 * conferencia de que o deposito corresponde ao que o artigo descreve.
 */

const fs = require('fs');
const path = require('path');

const { OntoumlVerification, Ontouml2Gufo } = require('ontouml-js');

const PREFIXO_BASE = 'ontompo';

/** Reescreve os ids aleatorios da ontouml-js por ids derivados dos nomes. */
function fixarIdentificadores(projeto, idDoProjeto) {
  projeto.id = idDoProjeto;
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

  for (const conjunto of projeto.getAllGeneralizationSets()) {
    conjunto.id = `gs_${conjunto.getName()}`;
  }
}

/** Falha cedo se alguma multiplicidade transcrita dos diagramas for invalida. */
function conferirCardinalidades(projeto) {
  const invalidas = [];
  for (const relacao of projeto.getAllRelations()) {
    for (const ponta of relacao.properties) {
      if (!ponta.cardinality.isValid()) {
        invalidas.push(
          `${relacao.getName()} / ${ponta.propertyType.getName()}: ${ponta.cardinality.value}`,
        );
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

function relatorioDaVerificacaoEmMarkdown(problemas, projeto, opcoes) {
  const linhas = [];
  linhas.push(`# Relatorio do plugin OntoUML sobre ${opcoes.descricaoDoModelo}`);
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
  if (opcoes.contarConjuntos) {
    linhas.push(
      `- Conjuntos de generalizacao verificados: ${projeto.getAllGeneralizationSets().length}`,
    );
  }
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
  linhas.push(opcoes.limitacoes);
  linhas.push('');
  return linhas.join('\n');
}

/**
 * Gera os tres artefatos de um modelo.
 *
 * @param opcoes.construir        funcao que devolve o `Project` da ontouml-js
 * @param opcoes.diretorioSaida   onde escrever
 * @param opcoes.nomeDoArquivo    prefixo de `<nome>.ontouml.json` e `<nome>.ttl`
 * @param opcoes.idDoProjeto      id deterministico do projeto
 * @param opcoes.iriBase          IRI base da transformacao gUFO
 * @param opcoes.descricaoDoModelo  como o relatorio se refere ao modelo
 * @param opcoes.limitacoes       o paragrafo "o que este relatorio nao cobre"
 * @param opcoes.contarConjuntos  se o relatorio deve contar conjuntos de generalizacao
 */
function gerar(opcoes) {
  fs.mkdirSync(opcoes.diretorioSaida, { recursive: true });

  const projeto = opcoes.construir();
  conferirCardinalidades(projeto);
  fixarIdentificadores(projeto, opcoes.idDoProjeto);

  const caminhoModelo = path.join(opcoes.diretorioSaida, `${opcoes.nomeDoArquivo}.ontouml.json`);
  fs.writeFileSync(caminhoModelo, `${JSON.stringify(projeto, null, 2)}\n`, 'utf-8');

  const problemas = OntoumlVerification.verify(projeto);
  fs.writeFileSync(
    path.join(opcoes.diretorioSaida, 'relatorio-plugin-ontouml.json'),
    `${JSON.stringify(problemas, null, 2)}\n`,
    'utf-8',
  );
  fs.writeFileSync(
    path.join(opcoes.diretorioSaida, 'relatorio-plugin-ontouml.md'),
    relatorioDaVerificacaoEmMarkdown(problemas, projeto, opcoes),
    'utf-8',
  );

  const transformacao = new Ontouml2Gufo(projeto, {
    baseIri: opcoes.iriBase,
    basePrefix: PREFIXO_BASE,
    format: 'Turtle',
    uriFormatBy: 'name',
    createObjectProperty: true,
    createInverses: false,
    prefixPackages: false,
  });
  transformacao.transform();

  const problemasGufo = transformacao.getIssues() || [];
  fs.writeFileSync(
    path.join(opcoes.diretorioSaida, `${opcoes.nomeDoArquivo}.ttl`),
    transformacao.getOwlCode(),
    'utf-8',
  );

  console.log(`modelo OntoUML   -> ${caminhoModelo}`);
  console.log(
    `classes ${projeto.getAllClasses().length}, relacoes ${projeto.getAllRelations().length}, ` +
      `generalizacoes ${projeto.getAllGeneralizations().length}`,
  );
  console.log(`verificacao      -> ${problemas.length} problema(s)`);
  for (const problema of problemas) {
    console.log(`  [${problema.severity}] ${problema.code}: ${nomeDoElemento(problema.data)}`);
  }
  console.log(`transformacao gUFO -> ${problemasGufo.length} problema(s)`);
  for (const problema of problemasGufo) {
    console.log(`  ${JSON.stringify(problema)}`);
  }
}

module.exports = { gerar };
