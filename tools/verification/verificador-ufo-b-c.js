/**
 * Verificador de microteorias: o que da para medir da adocao de UFO-B e UFO-C.
 *
 * O ticket 04 mostrou que o `OntoumlVerification` devolve zero sobre o *as-is*
 * e zero sobre a rodada 1, e construiu `verificador-ufo-extra.js` para que a
 * revisao tivesse alguma diferenca medida. O ticket 05 herda o mesmo problema,
 * agravado: o plugin devolve zero tambem sobre a rodada 2, porque nenhuma das
 * suas 24 regras distingue endurante de perdurante a partir do papel que o
 * conceito tem no dominio.
 *
 * Este arquivo acrescenta as regras que faltavam para medir *esta* rodada, e
 * roda **as cinco da rodada 1 junto com elas**, sobre os tres modelos, pelo
 * mesmo caminho de codigo. E a soma que o artigo cita: a rodada 2 nao pode
 * zerar as suas regras reintroduzindo as que a rodada 1 fechou.
 *
 * As regras vem em dois tipos, e a diferenca importa para ler o relatorio:
 *
 *   - as de **medicao** disparam sobre o *as-is* e medem a distancia ate o
 *     revisado. Sao as cinco da rodada 1 mais `modelo_sem_perdurante` e
 *     `modelo_sem_relacao_temporal`, que operacionalizam o *construct deficit*
 *     de UFO-B da unica forma que nao pede julgamento de dominio: nao dizendo
 *     que `Extract` deveria ser evento, mas registrando que o modelo inteiro
 *     nao usa nenhum construto da microteoria;
 *   - as de **guarda** so podem disparar sobre um modelo que ja adotou UFO-B,
 *     e existem para que a adocao nao seja de fachada. Sobre o *as-is* elas
 *     nao tem o que dizer, entao o controle positivo delas nao pode ser o
 *     baseline: e uma mutacao do proprio modelo revisado, como em
 *     `controle-verificacao.js`. O `principal()` reprova se alguma mutacao
 *     passar despercebida.
 *
 * O que este verificador **nao** cobre, e nao tenta cobrir: A6 e A7. Que um
 * «kind» generico colapse pessoa, grupo e organizacao, e que um sistema
 * computacional nao porte momentos intencionais, sao defeitos de significado,
 * nao de forma — a mesma razao pela qual A1, A2 e A9 nao viraram regra na
 * rodada 1. Codifica-los seria escrever a resposta no gabarito. Continuam
 * sustentados por argumento ontologico explicito, em
 * `artifacts/ontology/correcoes-rodada-2.md`.
 *
 * Uso: `node tools/verification/verificador-ufo-b-c.js [diretorio-de-saida]`
 */

const fs = require('fs');
const path = require('path');

const { construirModeloAsIs } = require('../model/ontompo-as-is');
const { construirModeloRodada1 } = require('../model/ontompo-rodada-1');
const { construirModeloRodada2 } = require('../model/ontompo-rodada-2');
const { REGRAS: REGRAS_RODADA_1, aplicarRegras } = require('./verificador-ufo-extra');

const SAIDA_PADRAO = path.resolve(__dirname, '..', '..', 'artifacts', 'ontology', 'rodada-2');

/**
 * Os estereotipos de relacao que a UFO-B usa para ligar perdurantes ao resto
 * do mundo: participacao de endurante em evento, parthood entre eventos,
 * criacao e terminacao de endurante, dependencia historica, e as duas que
 * ligam evento a situacao.
 */
const RELACOES_TEMPORAIS = [
  'participation',
  'participational',
  'creation',
  'termination',
  'historicalDependence',
  'bringsAbout',
  'triggers',
];

const NATUREZAS_PERDURANTES = ['event', 'situation'];

function tipo(ponta) {
  return ponta.propertyType;
}

function nome(elemento) {
  return elemento && typeof elemento.getName === 'function' ? elemento.getName() : '(sem nome)';
}

function naturezas(classe) {
  return classe.restrictedTo || [];
}

function ehEvento(classe) {
  return naturezas(classe).includes('event');
}

/** A classe e seus ancestrais por generalizacao, incluindo ela propria. */
function comAncestrais(projeto, classe) {
  const alcancadas = new Set([classe]);
  let mudou = true;
  while (mudou) {
    mudou = false;
    for (const generalizacao of projeto.getAllGeneralizations()) {
      if (alcancadas.has(generalizacao.specific) && !alcancadas.has(generalizacao.general)) {
        alcancadas.add(generalizacao.general);
        mudou = true;
      }
    }
  }
  return alcancadas;
}

const REGRAS = [
  {
    codigo: 'modelo_sem_perdurante',
    severidade: 'error',
    tipo: 'medicao',
    titulo: 'o modelo nao declara nenhum perdurante',
    fundamento:
      'A UFO parte da divisao entre endurantes, que estao inteiramente presentes a cada ' +
      'instante em que existem, e perdurantes, que se desdobram no tempo e tem partes ' +
      'temporais. Um modelo sem nenhuma classe de natureza evento ou situacao nao ' +
      'representa mudanca: nao tem onde dizer o que aconteceu, quando, nem em que ordem. ' +
      'A regra nao afirma que este ou aquele conceito deveria ser evento — isso e ' +
      'julgamento de dominio, e esta no argumento de A5. Ela registra que a metade ' +
      'perdurante do vocabulario esta inteira ausente, que e o *construct deficit* na ' +
      'sua forma verificavel.',
    aplicar(projeto) {
      const perdurantes = projeto
        .getAllClasses()
        .filter((classe) => naturezas(classe).some((n) => NATUREZAS_PERDURANTES.includes(n)));
      if (perdurantes.length > 0) return [];
      return [
        {
          elemento: nome(projeto.model),
          descricao:
            `nenhuma das ${projeto.getAllClasses().length} classes tem natureza evento ou ` +
            'situacao: a UFO-B nao foi adotada',
        },
      ];
    },
  },
  {
    codigo: 'modelo_sem_relacao_temporal',
    severidade: 'error',
    tipo: 'medicao',
    titulo: 'o modelo nao declara nenhuma relacao da UFO-B',
    fundamento:
      'Declarar eventos e metade da adocao; a outra e liga-los ao mundo. Sem ' +
      '«participation», «participational», «creation», «termination», ' +
      '«historicalDependence», «bringsAbout» ou «triggers», nada no modelo diz quem ' +
      'participou de que, o que passou a existir e o que deixou de existir. E uma regra ' +
      'independente da anterior: um modelo pode ter eventos e nao liga-los a nada, e e ' +
      'exatamente esse o caso que a adocao de fachada produz.',
    aplicar(projeto) {
      const temporais = projeto
        .getAllRelations()
        .filter((relacao) => RELACOES_TEMPORAIS.includes(relacao.stereotype));
      if (temporais.length > 0) return [];
      return [
        {
          elemento: nome(projeto.model),
          descricao:
            `nenhuma das ${projeto.getAllRelations().length} relacoes tem estereotipo da ` +
            'UFO-B: nao ha participacao, criacao nem terminacao no modelo',
        },
      ];
    },
  },
  {
    codigo: 'evento_sem_participante',
    severidade: 'error',
    tipo: 'guarda',
    titulo: 'tipo de evento sem nenhum participante declarado',
    fundamento:
      'Um evento em UFO-B existe pela participacao dos endurantes que o compoem: nao ha ' +
      'evento sem participante. Um tipo de evento que nao esta na ponta de nenhuma ' +
      '«participation», «participational», «creation» ou «termination» — nem por ' +
      'heranca de um tipo mais geral — e um evento de que nada participa, o que e uma ' +
      'troca de estereotipo sem adocao de microteoria.',
    aplicar(projeto) {
      const achados = [];
      for (const classe of projeto.getAllClasses()) {
        if (!ehEvento(classe)) continue;
        const familia = comAncestrais(projeto, classe);
        const ligada = projeto
          .getAllRelations()
          .some(
            (relacao) =>
              RELACOES_TEMPORAIS.includes(relacao.stereotype) &&
              relacao.properties.some((ponta) => familia.has(tipo(ponta))),
          );
        if (!ligada) {
          achados.push({
            elemento: classe.getName(),
            descricao: '«event» sem participacao, criacao ou terminacao, propria ou herdada',
          });
        }
      }
      return achados;
    },
  },
  {
    codigo: 'participacao_invertida',
    severidade: 'error',
    tipo: 'guarda',
    titulo: 'participacao com o evento na ponta do participante',
    fundamento:
      'A «participation» vai do endurante que participa para o evento de que ele ' +
      'participa, e a transformacao gUFO a escreve como `gufo:participatedIn` com ' +
      'aquele dominio e aquele alcance. Invertida, a OWL afirma que o evento participa ' +
      'do endurante — uma assercao que nenhum raciocinador recusa e que nenhum leitor ' +
      'entende. Vale o mesmo para a «creation», que vai do criado para o evento que o ' +
      'criou.',
    aplicar(projeto) {
      const achados = [];
      for (const relacao of projeto.getAllRelations()) {
        if (relacao.stereotype !== 'participation' && relacao.stereotype !== 'creation') continue;
        const origem = tipo(relacao.getSourceEnd());
        const destino = tipo(relacao.getTargetEnd());
        if (ehEvento(origem) || !ehEvento(destino)) {
          achados.push({
            elemento: relacao.getName(),
            descricao:
              `«${relacao.stereotype}» de \`${nome(origem)}\` para \`${nome(destino)}\`: ` +
              'o evento tem de estar na ponta de destino',
          });
        }
      }
      return achados;
    },
  },
];

/** Todas as regras aplicadas ao relatorio, na ordem em que os tickets as criaram. */
const TODAS_AS_REGRAS = [
  ...REGRAS_RODADA_1.map((regra) => ({ ...regra, tipo: 'medicao', origem: 'rodada 1' })),
  ...REGRAS.map((regra) => ({ ...regra, origem: 'rodada 2' })),
];

// --------------------------------------------------------------------------
// Controle das regras de guarda
// --------------------------------------------------------------------------

function classe(projeto, nomeDaClasse) {
  const encontrada = projeto.getAllClasses().find((c) => c.getName() === nomeDaClasse);
  if (!encontrada) throw new Error(`classe ${nomeDaClasse} nao existe no modelo`);
  return encontrada;
}

function relacao(projeto, nomeDaRelacao) {
  const encontrada = projeto.getAllRelations().find((r) => r.getName() === nomeDaRelacao);
  if (!encontrada) throw new Error(`relacao ${nomeDaRelacao} nao existe no modelo`);
  return encontrada;
}

/**
 * As mutacoes que provam que as regras de guarda disparam. Cada uma desfaz, no
 * modelo da rodada 2, exatamente o que a regra protege.
 */
const MUTACOES = [
  {
    nome: 'Observation perde as tres relacoes que a ligam a seus participantes',
    esperado: 'evento_sem_participante',
    porque: 'um tipo de evento de que nada participa nao e um evento adotado, e um rotulo',
    aplicar(projeto) {
      const alvo = classe(projeto, 'Observation');
      for (const r of projeto.getAllRelations()) {
        if (r.properties.some((ponta) => tipo(ponta) === alvo)) {
          projeto.model.removeContent(r);
        }
      }
    },
  },
  {
    nome: 'a participacao de Collector em Extract tem as pontas trocadas',
    esperado: 'participacao_invertida',
    porque: 'invertida, a gUFO passa a afirmar que a extracao participa do coletor',
    aplicar(projeto) {
      const alvo = relacao(projeto, 'participation_Collector_Extract');
      const [origem, destino] = alvo.properties;
      const antes = origem.propertyType;
      origem.propertyType = destino.propertyType;
      destino.propertyType = antes;
    },
  },
];

// --------------------------------------------------------------------------
// Relatorio
// --------------------------------------------------------------------------

const MODELOS = [
  ['as-is', construirModeloAsIs],
  ['rodada-1', construirModeloRodada1],
  ['rodada-2', construirModeloRodada2],
];

function contarPorRegra(problemas) {
  const contagem = Object.fromEntries(TODAS_AS_REGRAS.map((regra) => [regra.codigo, 0]));
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

function relatorioEmMarkdown(porModelo, controles) {
  const contagens = Object.fromEntries(
    MODELOS.map(([rotulo]) => [rotulo, contarPorRegra(porModelo[rotulo])]),
  );

  const linhas = [
    '# Verificador de microteorias: *as-is*, rodada 1 e rodada 2',
    '',
    'As regras abaixo operacionalizam restricoes da UFO que as 24 do plugin OntoUML nao ' +
      'cobrem. As cinco da rodada 1 (ticket 04) e as quatro da rodada 2 (ticket 05) sao ' +
      'aplicadas aos tres modelos pelo mesmo caminho de codigo. Saida bruta em ' +
      '`relatorio-verificador-ufo-b-c.json`; o codigo das regras esta em ' +
      '`tools/verification/verificador-ufo-extra.js` e ' +
      '`tools/verification/verificador-ufo-b-c.js`.',
    '',
    '## Diferenca medida',
    '',
    '| Regra | Tipo | Severidade | *as-is* | rodada 1 | rodada 2 |',
    '|---|---|---|---|---|---|',
  ];
  for (const regra of TODAS_AS_REGRAS) {
    linhas.push(
      `| \`${regra.codigo}\` | ${regra.tipo} | ${regra.severidade} | ` +
        `${contagens['as-is'][regra.codigo]} | ${contagens['rodada-1'][regra.codigo]} | ` +
        `${contagens['rodada-2'][regra.codigo]} |`,
    );
  }
  linhas.push(
    `| **total** | | | **${porModelo['as-is'].length}** | ` +
      `**${porModelo['rodada-1'].length}** | **${porModelo['rodada-2'].length}** |`,
  );
  linhas.push('');
  linhas.push(
    'O verificador do plugin OntoUML devolve zero sobre os tres modelos. E por isso que ' +
      'este segundo instrumento existe, e por isso que ele cresce junto com as rodadas: ' +
      'uma rodada que zerasse as suas regras reintroduzindo as da anterior apareceria ' +
      'aqui.',
  );
  linhas.push('');
  linhas.push('## As regras da rodada 2');
  linhas.push('');
  for (const regra of REGRAS) {
    linhas.push(`### \`${regra.codigo}\` — ${regra.titulo}`);
    linhas.push('');
    linhas.push(`*Regra de ${regra.tipo}.* ${regra.fundamento}`);
    linhas.push('');
  }
  linhas.push(
    'As cinco da rodada 1 estao documentadas em `../rodada-1/relatorio-verificador-extra.md`.',
  );
  linhas.push('');

  for (const [rotulo] of MODELOS) {
    linhas.push(`## Achados no modelo ${rotulo === 'as-is' ? '*as-is*' : rotulo}`);
    linhas.push('');
    linhas.push(...tabelaDeProblemas(porModelo[rotulo]));
    linhas.push('');
  }

  linhas.push('## Controle');
  linhas.push('');
  linhas.push(
    'Uma regra que nunca dispara nao mede nada. As regras de medicao tem como controle ' +
      'positivo o proprio *as-is*, sobre o qual as sete disparam, e a execucao reprova se ' +
      'alguma deixar de disparar. As regras de guarda nao podem ter esse controle — sobre ' +
      'um modelo sem UFO-B elas nao tem o que verificar —, entao o controle delas e uma ' +
      'mutacao do modelo da rodada 2, aplicada pelo mesmo caminho de codigo, como em ' +
      '`controle-verificacao.md`.',
  );
  linhas.push('');
  linhas.push('| Mutacao | Codigo esperado | Por que deveria falhar | Acusada |');
  linhas.push('|---|---|---|---|');
  for (const controle of controles) {
    linhas.push(
      `| ${controle.nome} | \`${controle.esperado}\` | ${controle.porque} | ` +
        `${controle.detectada ? 'sim' : '**NAO**'} |`,
    );
  }
  linhas.push('');
  linhas.push('Reproduzir com `node tools/verification/verificador-ufo-b-c.js`.');
  linhas.push('');
  return linhas.join('\n');
}

function principal() {
  const diretorioSaida = process.argv[2] ? path.resolve(process.argv[2]) : SAIDA_PADRAO;
  fs.mkdirSync(diretorioSaida, { recursive: true });

  const porModelo = Object.fromEntries(
    MODELOS.map(([rotulo, construir]) => [rotulo, aplicarRegras(TODAS_AS_REGRAS, construir())]),
  );

  const controles = MUTACOES.map((mutacao) => {
    const projeto = construirModeloRodada2();
    mutacao.aplicar(projeto);
    const codigos = aplicarRegras(TODAS_AS_REGRAS, projeto).map((p) => p.code);
    return { ...mutacao, detectada: codigos.includes(mutacao.esperado) };
  });

  fs.writeFileSync(
    path.join(diretorioSaida, 'relatorio-verificador-ufo-b-c.json'),
    `${JSON.stringify(porModelo, null, 2)}\n`,
    'utf-8',
  );
  fs.writeFileSync(
    path.join(diretorioSaida, 'relatorio-verificador-ufo-b-c.md'),
    relatorioEmMarkdown(porModelo, controles),
    'utf-8',
  );

  const contagens = Object.fromEntries(
    MODELOS.map(([rotulo]) => [rotulo, contarPorRegra(porModelo[rotulo])]),
  );
  for (const [rotulo] of MODELOS) {
    console.log(`${rotulo.padEnd(8)} -> ${porModelo[rotulo].length} problema(s)`);
  }
  for (const regra of TODAS_AS_REGRAS) {
    console.log(
      `  ${regra.codigo}: ${contagens['as-is'][regra.codigo]} -> ` +
        `${contagens['rodada-1'][regra.codigo]} -> ${contagens['rodada-2'][regra.codigo]}`,
    );
  }
  for (const controle of controles) {
    console.log(`${controle.detectada ? 'ok   ' : 'FALHA'} ${controle.nome}`);
  }

  const vacuas = TODAS_AS_REGRAS.filter(
    (regra) => regra.tipo === 'medicao' && contagens['as-is'][regra.codigo] === 0,
  );
  if (vacuas.length > 0) {
    console.log(
      `regra(s) de medicao que nao disparam sobre o as-is: ${vacuas.map((r) => r.codigo).join(', ')} — ` +
        'sem controle positivo, o zero da rodada 2 nao e interpretavel.',
    );
    process.exitCode = 1;
  }
  const naoDetectadas = controles.filter((controle) => !controle.detectada);
  if (naoDetectadas.length > 0) {
    console.log(
      `${naoDetectadas.length} mutacao(oes) nao detectada(s): as regras de guarda nao estao provadas.`,
    );
    process.exitCode = 1;
  }
  if (porModelo['rodada-2'].length > porModelo['rodada-1'].length) {
    console.log('a rodada 2 tem mais problemas que a rodada 1.');
    process.exitCode = 1;
  }
}

if (require.main === module) {
  principal();
}

module.exports = { REGRAS, TODAS_AS_REGRAS };
