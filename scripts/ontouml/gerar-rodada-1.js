/**
 * Gera os artefatos da primeira rodada de revisao (ticket 04), pelo mesmo
 * caminho de codigo que gera o baseline — e essa igualdade que torna os dois
 * relatorios comparaveis.
 *
 * A OWL sai aqui em Turtle porque as correcoes de A2 e A3 precisam ser
 * conferidas na OWL, e nao so no JSON; a OWL definitiva do artefato revisado,
 * com as customizacoes e o diff, e do ticket 06.
 *
 * Uso: `node scripts/ontouml/gerar-rodada-1.js [diretorio-de-saida]`
 */

const path = require('path');

const { gerar } = require('./gerar');
const { construirModeloRodada1 } = require('./modelo-rodada-1');

const SAIDA_PADRAO = path.resolve(__dirname, '..', '..', 'ontologia', 'rodada-1');

const LIMITACOES =
  'O verificador devolve zero sobre este modelo, como devolvia sobre o *as-is*: nenhuma ' +
  'das seis deficiencias corrigidas nesta rodada esta ao alcance das suas 24 regras, que ' +
  'tratam de estereotipo, provedor de identidade, natureza e generalizacao. **O zero de ' +
  'antes e o zero de depois nao medem a revisao** — quem a mede e o verificador ' +
  'complementar, em `relatorio-verificador-extra.md`, cujas cinco regras acusam dez ' +
  'problemas no *as-is* e um aqui. O que este relatorio garante e que a revisao nao ' +
  'introduziu nenhuma violacao das regras que o plugin de fato tem.';

gerar({
  construir: construirModeloRodada1,
  diretorioSaida: process.argv[2] ? path.resolve(process.argv[2]) : SAIDA_PADRAO,
  nomeDoArquivo: 'ontompo-rodada-1',
  idDoProjeto: 'ontompo-rodada-1',
  iriBase: 'https://example.org/ontompo/rodada-1',
  descricaoDoModelo: 'o modelo revisado (rodada 1)',
  limitacoes: LIMITACOES,
  contarConjuntos: true,
});
