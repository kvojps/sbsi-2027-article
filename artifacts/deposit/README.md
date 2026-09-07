# OntoMPO — artefatos da analise ontologica do Modelo para Observatorios de Projetos

Deposito de ciencia aberta que acompanha o artigo *OntoMPO: Ontological Analysis
and Refinement of the Model for Project Observatories*. Reune o que a pesquisa
produziu: o modelo conceitual revisado, a ontologia OWL, as verificacoes
automaticas antes e depois da revisao, e a avaliacao funcional por questoes de
competencia em SPARQL sobre um cenario instanciado.

O artigo esta em revisao duplamente anonima. Os artefatos da OntoMPO — tudo em
`ontology/` — sao anonimos por requisito: nao trazem nome, instituicao, e-mail
nem usuario de quem depositou, os IRIs sao de um dominio de exemplo
(`https://example.org/ontompo/...`) e toda fonte externa e citada em terceira
pessoa pelo seu identificador. A unica excecao e `gufo/`, que e a gUFO
redistribuida como obtida: ela traz os nomes dos **seus proprios** autores e o
endereco do **seu** repositorio, que identificam o projeto gUFO, nao quem fez
este deposito.

Alguns arquivos copiados para `ontology/` e `gufo/README.md` citam caminhos
relativos ao repositorio de origem (`tools/...`, `sources/gufo/...`). Fora do
repositorio esses caminhos nao resolvem — o ponto de entrada autocontido e o
`reexecutar-consultas.py` na raiz deste deposito.

## O que tem aqui

```
deposit/
  .zenodo.json             metadados do deposito, sem autoria
  MANIFEST.sha256          SHA-256 de cada arquivo do deposito
  README.md                este arquivo
  gufo/                    gUFO 1.0.0 como distribuida (gufo.ttl, README.md) (2 arquivos)
  ontology/                a arvore de artefatos da pesquisa (66 arquivos)
  reexecutar-consultas.py  reexecuta as sete QCs e confere contra o .csv gravado
```

## Por onde comecar

1. `ontology/evidencias-A1-A9.md` — as nove deficiencias representacionais que a
   analise expos na formalizacao publicada, cada uma com classificacao pela
   Representation Theory (Wand & Weber), rastro ate o modelo de referencia e
   correcao.
2. `ontology/correcoes-rodada-1.md` e `ontology/correcoes-rodada-2.md` — o par
   antes/depois de cada correcao, com a justificativa fundamentada na UFO. A
   rodada 1 corrige A1–A4, A8 e A9; a rodada 2 adota UFO-B e UFO-C e corrige
   A5–A7.
3. `ontology/owl/customizacoes.md` — as cinco customizacoes aplicadas por cima
   da transformacao gUFO, e `ontology/owl/diff-gerado-customizado.ttl`, o
   conjunto exato de triplas acrescentadas.
4. `ontology/README.md` — o mapa completo dos artefatos e o que mede o
   antes/depois.

## As verificacoes, antes e depois

| Instrumento | Antes (baseline) | Depois (revisado) |
|---|---|---|
| Plugin OntoUML | `ontology/baseline/relatorio-plugin-ontouml.md` | `ontology/rodada-2/relatorio-plugin-ontouml.md` |
| Verificadores estruturais UFO | `ontology/rodada-1/relatorio-verificador-extra.md` | `ontology/rodada-2/relatorio-verificador-ufo-b-c.md` |
| OOPS! | `ontology/baseline/relatorio-oops.md` | `ontology/owl/relatorio-oops.md` |
| Comparacao OOPS! consolidada | — | `ontology/owl/comparacao-oops.md` |
| Raciocinador (consistencia) | — | `ontology/owl/relatorio-raciocinador.md` |

## Reexecutar as sete consultas SPARQL

As consultas estao em `ontology/consultas/qc1.rq` .. `qc7.rq`; o resultado
completo, cru, esta ao lado em `qcN-resultado.csv`, e a pergunta com a tabela em
`qcN-resultado.md`.

Para reexecutar numa maquina sem sessao autenticada e sem nada deste
repositorio, so com Python:

```sh
python -m venv .venv && . .venv/bin/activate      # ou .venv\Scripts\activate no Windows
pip install "rdflib>=7,<8"
python reexecutar-consultas.py
```

O script carrega, num unico grafo, a OWL revisada (`ontology/owl/ontompo.ttl`),
a gUFO local (`gufo/gufo.ttl`, que a OWL importa) e os dados de instancia dos
dois observatorios, roda cada consulta e confere o resultado, linha a linha,
contra o `.csv` gravado. As consultas andam so sobre triplas afirmadas — sem
raciocinador.

Onde o resultado obtido diverge do esperado — inclusive onde a divergencia
favorece o modelo revisado — esta registrado em
`ontology/consultas/divergencias.md`.

## O cenario de instancia

`ontology/instancias/observatorio.ttl` deriva de uma publicacao de terceiros nos
Anais Estendidos do XVIII SBSI (2022), DOI 10.5753/sbsi_estendido.2022.222995, referida em
terceira pessoa; o mapa trecho-da-publicacao -> individuo esta em
`ontology/instancias/procedencia.md`. `observatorio-b.ttl` e um segundo
observatorio, sintetico, construido apenas para a QC7 comparar a cobertura
conceitual de duas iniciativas.

## Ferramentas e versoes

| Ferramenta | Versao | Papel |
|---|---|---|
| `ontouml-js` | 0.5.0 | construcao do modelo, verificacao e transformacao `Ontouml2Gufo` |
| OOPS! | servico REST em `oops.linkeddata.es/rest` | pitfalls de OWL |
| `rdflib` | 7.x | Turtle -> RDF/XML, customizacao da OWL e execucao das consultas |
| `owlrl` | 7.x | raciocinador, perfil OWL 2 RL |
| gUFO | 1.0.0 (`gufo/`, SHA-256 em `gufo/README.md`) | ontologia de fundamentacao importada pela OWL |

## Licenca

Os artefatos da OntoMPO estao sob **Creative Commons Attribution 4.0**
(`https://creativecommons.org/licenses/by/4.0/`). A gUFO em `gufo/` e
redistribuida como obtida; sua licenca e a do projeto gUFO.
