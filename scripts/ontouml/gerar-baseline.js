/**
 * Gera os artefatos de baseline do ticket 03 a partir do modelo *as-is*.
 *
 * A maquinaria esta em `gerar.js`, compartilhada com as rodadas de revisao,
 * para que os artefatos das duas metades do antes/depois saiam pelo mesmo
 * caminho de codigo — se a geracao mudar, muda para os dois.
 *
 * Uso: `node scripts/ontouml/gerar-baseline.js [diretorio-de-saida]`
 */

const path = require('path');

const { gerar } = require('./gerar');
const { construirModeloAsIs } = require('./modelo-as-is');

const SAIDA_PADRAO = path.resolve(__dirname, '..', '..', 'ontologia', 'baseline');

const LIMITACOES =
  'O conjunto de regras do verificador tem 24 codigos, todos sobre estereotipos de ' +
  'classe, provedores de identidade, naturezas e generalizacoes. **Nenhum deles trata ' +
  'de restricoes meronimicas** — nao ha regra que exija que o todo de uma «memberOf» ' +
  'seja um coletivo, nem que uma «componentOf» ligue complexos funcionais. Deficiencias ' +
  'dessa classe, como A2 e A3, precisam ser sustentadas por argumento ontologico ' +
  'explicito; estao em `../evidencias-A1-A9.md`. As que sao estruturais o bastante para ' +
  'virar regra estao no verificador complementar, em `../rodada-1/` — sobre este mesmo ' +
  'modelo ele acusa dez.';

gerar({
  construir: construirModeloAsIs,
  diretorioSaida: process.argv[2] ? path.resolve(process.argv[2]) : SAIDA_PADRAO,
  nomeDoArquivo: 'ontompo-as-is',
  idDoProjeto: 'ontompo-as-is',
  iriBase: 'https://example.org/ontompo/as-is',
  descricaoDoModelo: 'o modelo *as-is*',
  limitacoes: LIMITACOES,
  contarConjuntos: false,
});
