/**
 * Verificador complementar: as restricoes da UFO que o plugin OntoUML nao tem.
 *
 * O ticket 03 estabeleceu que o `OntoumlVerification` devolve zero problemas
 * sobre o modelo *as-is*, e por que: suas 24 regras tratam de estereotipo,
 * provedor de identidade, natureza e generalizacao, e nenhuma trata de
 * mereologia, de aridade de relator ou de colisao terminologica. Sem um
 * segundo instrumento, o antes/depois desta rodada nao teria como ser medido —
 * zero antes, zero depois — e o ticket 04 pede diferenca medida, nao afirmada.
 *
 * Este arquivo fecha essa lacuna com cinco regras. Cada uma e:
 *
 *   - **estrutural**, computada do proprio modelo, sem julgamento de dominio;
 *   - **fundamentada**, com a restricao da UFO que ela operacionaliza escrita
 *     junto;
 *   - **nao vacua**, e o modelo *as-is* e a prova disso: as cinco disparam
 *     sobre ele. O `principal()` abaixo reprova se alguma nao disparar, pela
 *     mesma razao que `controle-verificacao.js` existe — regra que nunca
 *     dispara nao mede nada.
 *
 * O que este verificador **nao** cobre, e nao tenta cobrir: A1, A2 e A9. Uma
 * sobrecarga de construto, uma mereologia semanticamente invalida entre dois
 * complexos funcionais e uma taxonomia que confunde principio de identidade
 * sao defeitos de significado, nao de forma; codificar cada uma como regra
 * seria escrever a resposta no gabarito. Continuam sustentadas por argumento
 * ontologico explicito, em `artifacts/ontology/correcoes-rodada-1.md`.
 *
 * Uso: `node tools/verification/verificador-ufo-extra.js [diretorio-de-saida]`
 */

const fs = require('fs');
const path = require('path');

const { construirModeloAsIs } = require('../model/ontompo-as-is');
const { construirModeloRodada1 } = require('../model/ontompo-rodada-1');

const SAIDA_PADRAO = path.resolve(__dirname, '..', '..', 'artifacts', 'ontology', 'rodada-1');

const MERONIMICAS = ['memberOf', 'componentOf', 'subCollectionOf', 'subQuantityOf'];

/**
 * Os metaconceitos da UFO e da gUFO cujos nomes uma classe de dominio nao pode
 * tomar. A lista e a dos estereotipos de classe da OntoUML mais as categorias
 * de fundamentacao que a gUFO publica como classes.
 *
 * `Subkind` e `SubKind` estao os dois de proposito, e nao por descuido: a
 * OntoUML escreve o estereotipo «subkind» e a gUFO publica a classe
 * `gufo:SubKind`. Colidir com qualquer uma das duas grafias e colisao.
 */
const METACONCEITOS = [
  'Kind',
  'Subkind',
  'SubKind',
  'Role',
  'Phase',
  'Category',
  'Mixin',
  'RoleMixin',
  'PhaseMixin',
  'Relator',
  'Mode',
  'Quality',
  'Quantity',
  'Collective',
  'Event',
  'Situation',
  'Type',
  'Endurant',
  'Perdurant',
  'Object',
  'FunctionalComplex',
  'IntrinsicMode',
  'ExtrinsicMode',
];

function pontas(relacao) {
  return { origem: relacao.getSourceEnd(), destino: relacao.getTargetEnd() };
}

function tipo(ponta) {
  return ponta.propertyType;
}

function nome(elemento) {
  return elemento && typeof elemento.getName === 'function' ? elemento.getName() : '(sem nome)';
}

function ehTodo(ponta) {
  return ponta.aggregationKind === 'SHARED' || ponta.aggregationKind === 'COMPOSITE';
}

const REGRAS = [
  {
    codigo: 'memberof_whole_not_collective',
    severidade: 'error',
    titulo: 'o todo de uma «memberOf» tem de ser um coletivo',
    fundamento:
      'Em UFO, «memberOf» e a parthood entre um coletivo e seus membros: o todo e uma ' +
      'colecao e a parte e membro dela. Um todo que nao e coletivo torna a relacao ' +
      'ininterpretavel e, na gUFO, produz uma assercao `isCollectionMemberOf` invertida.',
    aplicar(projeto) {
      const achados = [];
      for (const relacao of projeto.getAllRelations()) {
        if (relacao.stereotype !== 'memberOf') continue;
        const { origem, destino } = pontas(relacao);
        for (const ponta of [origem, destino]) {
          if (!ehTodo(ponta)) continue;
          const classe = tipo(ponta);
          if (!(classe.restrictedTo || []).includes('collective')) {
            achados.push({
              elemento: relacao.getName(),
              descricao:
                `o todo declarado e \`${nome(classe)}\`, de natureza ` +
                `${(classe.restrictedTo || []).join('/') || 'indefinida'}, e nao um coletivo`,
            });
          }
        }
      }
      return achados;
    },
  },
  {
    codigo: 'parthood_ends_undeclared',
    severidade: 'error',
    titulo: 'relacao meronimica sem todo nem parte declarados',
    fundamento:
      'Uma relacao de parthood so significa alguma coisa depois de dito qual ponta e o ' +
      'todo. Sem extremidade de agregacao em nenhuma das duas, a relacao carrega o ' +
      'estereotipo mereologico sem exercer nenhuma restricao mereologica.',
    aplicar(projeto) {
      const achados = [];
      for (const relacao of projeto.getAllRelations()) {
        if (!MERONIMICAS.includes(relacao.stereotype)) continue;
        const { origem, destino } = pontas(relacao);
        if (!ehTodo(origem) && !ehTodo(destino)) {
          achados.push({
            elemento: relacao.getName(),
            descricao: `«${relacao.stereotype}» sem losango em nenhuma das duas pontas`,
          });
        }
      }
      return achados;
    },
  },
  {
    codigo: 'mediation_optional_relatum',
    severidade: 'error',
    titulo: 'mediacao com minimo zero na ponta mediada',
    fundamento:
      'Uma «mediation» e dependencia existencial: o relator nao existe sem o mediado. ' +
      'Minimo zero na ponta mediada admite um relator que nao conecta aquele relatum, ' +
      'isto e, um relator que pode nao reificar relacao nenhuma.',
    aplicar(projeto) {
      const achados = [];
      for (const relacao of projeto.getAllRelations()) {
        if (relacao.stereotype !== 'mediation') continue;
        const { origem, destino } = pontas(relacao);
        if (destino.cardinality.getLowerBoundAsNumber() === 0) {
          achados.push({
            elemento: relacao.getName(),
            descricao:
              `${nome(tipo(origem))} medeia ${nome(tipo(destino))} com ` +
              `\`${destino.cardinality.value}\` na ponta mediada`,
          });
        }
      }
      return achados;
    },
  },
  {
    codigo: 'class_name_collides_with_metaconcept',
    severidade: 'error',
    titulo: 'classe de dominio com nome de metaconceito da UFO',
    fundamento:
      'O nome de uma classe de dominio e o de uma categoria de fundamentacao passam a ' +
      'designar coisas diferentes no mesmo documento. Na OWL a colisao fica literal: ' +
      '`gufo:Relator` e `ontompo:Relator` convivem no mesmo grafo.',
    aplicar(projeto) {
      const achados = [];
      for (const classe of projeto.getAllClasses()) {
        if (METACONCEITOS.includes(classe.getName())) {
          achados.push({
            elemento: classe.getName(),
            descricao: `«${classe.stereotype}» de dominio homonima do metaconceito da UFO`,
          });
        }
      }
      return achados;
    },
  },
  {
    codigo: 'relator_arity_above_binary',
    severidade: 'warning',
    titulo: 'relator n-ario sem fato relacional nomeado',
    fundamento:
      'A aridade de um relator decorre do fato relacional que ele reifica. Um relator ' +
      'que medeia mais de dois relata pode estar reificando um fato genuinamente ' +
      'n-ario ou varios fatos binarios colapsados num construto so — e o modelo, ' +
      'sozinho, nao distingue os dois casos. Severidade *warning*: o achado e um ' +
      'pedido de justificativa, nao um veredito.',
    aplicar(projeto) {
      const achados = [];
      for (const classe of projeto.getAllClasses()) {
        if (classe.stereotype !== 'relator') continue;
        const mediados = projeto
          .getAllRelations()
          .filter((r) => r.stereotype === 'mediation' && tipo(r.getSourceEnd()) === classe)
          .map((r) => nome(tipo(r.getTargetEnd())));
        if (mediados.length > 2) {
          achados.push({
            elemento: classe.getName(),
            descricao: `medeia ${mediados.length} relata: ${mediados.join(', ')}`,
          });
        }
      }
      return achados;
    },
  },
];

/**
 * Roda um conjunto de regras sobre um projeto e devolve a lista achatada de
 * achados. Fica generico sobre as regras porque o verificador de microteorias
 * do ticket 05 aplica as cinco daqui e as suas proprias pelo mesmo caminho de
 * codigo — se a forma do achado mudar, muda para os dois relatorios.
 */
function aplicarRegras(regras, projeto) {
  const problemas = [];
  for (const regra of regras) {
    for (const achado of regra.aplicar(projeto)) {
      problemas.push({
        code: regra.codigo,
        severity: regra.severidade,
        element: achado.elemento,
        description: achado.descricao,
      });
    }
  }
  return problemas;
}

/** Roda as cinco regras sobre um projeto e devolve a lista achatada de achados. */
function verificar(projeto) {
  return aplicarRegras(REGRAS, projeto);
}

function contarPorRegra(problemas) {
  const contagem = Object.fromEntries(REGRAS.map((regra) => [regra.codigo, 0]));
  for (const problema of problemas) contagem[problema.code] += 1;
  return contagem;
}

function tabelaDeProblemas(problemas) {
  if (problemas.length === 0) return ['Nenhum problema encontrado.'];
  const linhas = ['| # | Severidade | Codigo | Elemento | Descricao |', '|---|---|---|---|---|'];
  problemas.forEach((problema, indice) => {
    linhas.push(
      `| ${indice + 1} | ${problema.severity} | \`${problema.code}\` | ` +
        `\`${problema.element}\` | ${problema.description.replace(/\|/g, '\\|')} |`,
    );
  });
  return linhas;
}

function relatorioEmMarkdown(antes, depois) {
  const contagemAntes = contarPorRegra(antes);
  const contagemDepois = contarPorRegra(depois);

  const linhas = [
    '# Verificador complementar: *as-is* contra rodada 1',
    '',
    'As cinco regras abaixo operacionalizam restricoes da UFO que as 24 do plugin OntoUML ' +
      'nao cobrem. Sao aplicadas ao mesmo modelo, pelo mesmo caminho de codigo, antes e ' +
      'depois da primeira rodada de revisao. Saida bruta em ' +
      '`relatorio-verificador-extra.json`; o codigo das regras esta em ' +
      '`tools/verification/verificador-ufo-extra.js`.',
    '',
    '## Diferenca medida',
    '',
    '| Regra | Severidade | *as-is* | rodada 1 |',
    '|---|---|---|---|',
  ];
  for (const regra of REGRAS) {
    linhas.push(
      `| \`${regra.codigo}\` | ${regra.severidade} | ${contagemAntes[regra.codigo]} | ` +
        `${contagemDepois[regra.codigo]} |`,
    );
  }
  linhas.push(`| **total** | | **${antes.length}** | **${depois.length}** |`);
  linhas.push('');
  linhas.push(
    'Para comparacao, o verificador do plugin OntoUML devolve zero problemas sobre os dois ' +
      'modelos: as deficiencias desta rodada estao todas fora do alcance das 24 regras dele. ' +
      'E por isso que este segundo instrumento existe.',
  );
  linhas.push('');
  linhas.push('## As regras');
  linhas.push('');
  for (const regra of REGRAS) {
    linhas.push(`### \`${regra.codigo}\` — ${regra.titulo}`);
    linhas.push('');
    linhas.push(regra.fundamento);
    linhas.push('');
  }
  linhas.push('## Achados no modelo *as-is*');
  linhas.push('');
  linhas.push(...tabelaDeProblemas(antes));
  linhas.push('');
  linhas.push('## Achados no modelo da rodada 1');
  linhas.push('');
  linhas.push(...tabelaDeProblemas(depois));
  linhas.push('');
  linhas.push('## Controle');
  linhas.push('');
  linhas.push(
    'Uma regra que nunca dispara nao mede nada. As cinco disparam sobre o modelo *as-is*, ' +
      'e a execucao reprova se alguma delas deixar de disparar — o zero da rodada 1 e ' +
      'resultado, e nao ausencia de instrumento.',
  );
  linhas.push('');
  return linhas.join('\n');
}

function principal() {
  const diretorioSaida = process.argv[2] ? path.resolve(process.argv[2]) : SAIDA_PADRAO;
  fs.mkdirSync(diretorioSaida, { recursive: true });

  const antes = verificar(construirModeloAsIs());
  const depois = verificar(construirModeloRodada1());

  fs.writeFileSync(
    path.join(diretorioSaida, 'relatorio-verificador-extra.json'),
    `${JSON.stringify({ 'as-is': antes, 'rodada-1': depois }, null, 2)}\n`,
    'utf-8',
  );
  fs.writeFileSync(
    path.join(diretorioSaida, 'relatorio-verificador-extra.md'),
    relatorioEmMarkdown(antes, depois),
    'utf-8',
  );

  const contagemAntes = contarPorRegra(antes);
  console.log(`as-is    -> ${antes.length} problema(s)`);
  console.log(`rodada 1 -> ${depois.length} problema(s)`);
  for (const regra of REGRAS) {
    console.log(
      `  ${regra.codigo}: ${contagemAntes[regra.codigo]} -> ${contarPorRegra(depois)[regra.codigo]}`,
    );
  }

  const vacuas = REGRAS.filter((regra) => contagemAntes[regra.codigo] === 0);
  if (vacuas.length > 0) {
    console.log(
      `regra(s) que nao disparam nem sobre o as-is: ${vacuas.map((r) => r.codigo).join(', ')} — ` +
        'sem controle positivo, o zero da rodada 1 nao e interpretavel.',
    );
    process.exitCode = 1;
  }
  if (depois.length > antes.length) {
    console.log('a rodada 1 tem mais problemas que o baseline.');
    process.exitCode = 1;
  }
}

if (require.main === module) {
  principal();
}

module.exports = { REGRAS, aplicarRegras, verificar };
