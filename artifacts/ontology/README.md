# Artefatos ontológicos da OntoMPO

> O mapa do repositório inteiro está em `../../README.md`; o vocabulário, em `../../CONTEXT.md`.

Este diretório guarda os artefatos da ontologia, em duas metades que convivem:

- **`baseline/`**, o modelo OntoUML reconstruído *exatamente como publicado*, sem nenhuma correção —
  a metade "antes" do antes/depois do artigo (ticket 03);
- **`rodada-1/`**, o modelo depois da primeira rodada de revisão, que corrige A1, A2, A3, A4, A8 e
  A9 (ticket 04).

As rodadas seguintes entram como diretórios irmãos. Nenhuma substitui o baseline: é a comparação que
dá evidência.

Os artefatos originais da pesquisa não foram localizados — não existe OWL, modelo editável nem
script em lugar algum, e o repositório citado na dissertação está 404. O baseline foi remontado a
partir dos diagramas em resolução de origem, em `../../sources/dissertation/imagens/`.

## O que tem aqui

```
artifacts/ontology/
├── evidencias-A1-A9.md            onde cada deficiência está e o que a sustenta
├── correcoes-rodada-1.md          o par antes/depois e a justificativa de cada correção
├── baseline/
│   ├── ontompo-as-is.ontouml.json  o modelo, no OntoUML Schema
│   ├── ontompo-as-is.ttl           a OWL de baseline, transformação gUFO
│   ├── ontompo-as-is.owl           a mesma OWL em RDF/XML
│   ├── ontompo-as-is.oops.owl      a cópia submetida ao OOPS!, sem owl:imports
│   ├── relatorio-plugin-ontouml.md o relatório do verificador, legível
│   ├── relatorio-plugin-ontouml.json  o mesmo, bruto
│   ├── relatorio-oops.md           o relatório do OOPS!, legível
│   ├── relatorio-oops.xml          a resposta bruta do serviço
│   └── controle-verificacao.md     o controle que torna interpretável o relatório vazio
└── rodada-1/
    ├── ontompo-rodada-1.ontouml.json  o modelo revisado, no OntoUML Schema
    ├── ontompo-rodada-1.ttl           a OWL da rodada, mesma transformação gUFO
    ├── relatorio-plugin-ontouml.md    o relatório do verificador, legível
    ├── relatorio-plugin-ontouml.json  o mesmo, bruto
    ├── relatorio-verificador-extra.md o verificador complementar, antes contra depois
    ├── relatorio-verificador-extra.json  o mesmo, bruto
    ├── controle-verificacao.md        o controle, agora sobre o modelo revisado
    └── diff-as-is-rodada-1.md         o diff estrutural, derivado dos dois modelos
```

Os endereços já reservados para o que vem a seguir, cada um criado pelo ticket que o preenche:
`rodada-2/` (ticket 05, UFO-B e UFO-C), `owl/` (ticket 06, a OWL customizada e o diff da
transformação), `instancias/` (ticket 07, os dados dos dois observatórios) e `consultas/`
(tickets 07 e 08, as sete QCs com resultados completos). Ver `../../docs/adr/0001-layout-do-repositorio.md`.

**Comece por `evidencias-A1-A9.md` e `correcoes-rodada-1.md`.** Eles carregam a leitura dos
relatórios; os relatórios sozinhos não dizem o que importa.

## A medição do antes/depois

O verificador do plugin OntoUML devolve **zero problemas sobre os dois modelos**: as deficiências
A1–A9 estão todas fora do alcance das suas 24 regras, que tratam de estereótipo, provedor de
identidade, natureza e generalização. Zero contra zero não mede revisão.

Quem mede é o verificador complementar, `tools/verification/verificador-ufo-extra.js`, com cinco regras
estruturais que operacionalizam restrições da UFO fora daquele conjunto — mereologia, dependência
existencial da mediação, aridade de relator e colisão com metaconceito. Sobre o baseline ele acusa
**dez**; sobre a rodada 1, **um**, um *warning* que está endereçado. Cada uma das cinco dispara no
baseline, e a execução reprova se alguma deixar de disparar: sem controle positivo, o zero do
revisado não seria interpretável.

## Como reproduzir

```sh
cd tools && npm ci && cd ..

# linha de base (ticket 03)
node tools/generation/gerar-baseline.js                           # modelo, verificação e OWL
node tools/verification/controle-verificacao.js                   # controle do verificador

# rodada 1 (ticket 04)
node tools/generation/gerar-rodada-1.js                           # modelo, verificação e OWL
node tools/verification/controle-verificacao.js --modelo=rodada-1 # controle sobre o revisado
node tools/verification/verificador-ufo-extra.js                  # as cinco regras, antes e depois
node tools/generation/diff-modelos.js                             # o diff estrutural

pip install rdflib requests
python tools/verification/rodar_oops.py                           # OOPS! sobre o baseline (precisa de rede)
python tools/verification/verificar_baseline.py                   # confere a checklist do ticket 03
python tools/verification/verificar_rodada1.py                    # confere a checklist do ticket 04
```

O OOPS! ainda não foi executado sobre o modelo revisado: o antes/depois de *pitfalls* de OWL é do
ticket 06, junto com a customização da OWL, e rodá-lo sobre uma OWL que ainda vai mudar produziria
um número que aquele ticket invalidaria.

Tudo é determinístico exceto a resposta do OOPS!, que traz um identificador de requisição novo a cada
chamada: `relatorio-oops.xml` muda de conteúdo a cada execução mesmo sem nada ter mudado no modelo.
Os demais arquivos são byte a byte idênticos entre execuções — os identificadores da `ontouml-js` e
os rótulos de nó anônimo da `rdflib`, que são sorteados, foram fixados de forma determinística
justamente para isso.

## Ferramentas

| Ferramenta | Versão | Papel |
|---|---|---|
| `ontouml-js` | 0.5.0 | construção do modelo, `OntoumlVerification` e `Ontouml2Gufo` |
| OOPS! | serviço REST em `oops.linkeddata.es/rest` | *pitfalls* de OWL |
| `rdflib` | 7.x | Turtle → RDF/XML |

A `ontouml-js` 0.5.0 é a última versão que ainda expõe `OntoumlVerification` e `Ontouml2Gufo`; a
1.0.0 removeu as duas. É o mesmo motor que o plugin OntoUML para o Visual Paradigm invoca, e o JSON
gerado está no formato de intercâmbio do plugin — o modelo abre no Visual Paradigm sem conversão.

## O que o baseline não é

Não é um modelo bom, e não deve ser corrigido. Toda tentação de "arrumar de passagem" um estereótipo,
uma multiplicidade ou um nome destrói o valor de `baseline/`, que é servir de termo de comparação —
`verificar_rodada1.py` reprova se o baseline for mexido. Correção vai em `rodada-1/` e nas rodadas
seguintes.

## Anonimato

Os IRIs usam `https://example.org/ontompo/as-is` e `https://example.org/ontompo/rodada-1`, que são
deliberadamente de um domínio de exemplo. O IRI definitivo entra no ticket 09, junto com o depósito,
e precisa continuar não identificando autoria nem instituição enquanto a revisão for duplamente
anônima.
