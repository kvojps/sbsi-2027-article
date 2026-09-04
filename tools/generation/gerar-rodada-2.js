/**
 * Gera os artefatos da segunda rodada de revisao (ticket 05), pelo mesmo
 * caminho de codigo que gera o baseline e a rodada 1 — e essa igualdade que
 * torna os tres relatorios comparaveis.
 *
 * Uso: `node tools/generation/gerar-rodada-2.js [diretorio-de-saida]`
 */

const path = require('path');

const { gerar } = require('./gerar');
const { construirModeloRodada2 } = require('../model/ontompo-rodada-2');

const SAIDA_PADRAO = path.resolve(__dirname, '..', '..', 'artifacts', 'ontology', 'rodada-2');

const LIMITACOES =
  'O verificador devolve zero sobre este modelo, como devolvia sobre o *as-is* e sobre a ' +
  'rodada 1. Suas 24 regras tratam de estereotipo, provedor de identidade, natureza e ' +
  'generalizacao, e **nao ha regra que distinga endurante de perdurante** a partir do ' +
  'papel do conceito no dominio — que e exatamente o que A5 e o achado B8 sao. O que este ' +
  'relatorio garante e mais estreito e vale dizer: a adocao de UFO-B e UFO-C nao introduziu ' +
  'nenhuma violacao das regras que ele de fato tem, e elas nao sao poucas aqui, porque a ' +
  'rodada troca dois estereotipos de classe por camada inteira — «kind» por «category» na ' +
  'camada de agentes, «relator» por «event» no ETL — e cada troca mexe com natureza, ' +
  'sortalidade e rigidez nas generalizacoes vizinhas. Quem mede a rodada e o verificador ' +
  'de microteorias, em `relatorio-verificador-ufo-b-c.md`.';

gerar({
  construir: construirModeloRodada2,
  diretorioSaida: process.argv[2] ? path.resolve(process.argv[2]) : SAIDA_PADRAO,
  nomeDoArquivo: 'ontompo-rodada-2',
  idDoProjeto: 'ontompo-rodada-2',
  iriBase: 'https://example.org/ontompo/rodada-2',
  descricaoDoModelo: 'o modelo revisado (rodada 2)',
  limitacoes: LIMITACOES,
  contarConjuntos: true,
});
