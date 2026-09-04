# Artefatos ontológicos da OntoMPO

Este diretório guarda os artefatos da ontologia. Hoje contém apenas a **linha de base**: o modelo
OntoUML reconstruído *exatamente como publicado*, sem nenhuma correção, e as verificações
automáticas rodadas sobre ele. É a metade "antes" do antes/depois do artigo. O modelo revisado é do
ticket 04 e vai conviver aqui, ao lado do baseline, não no lugar dele.

Os artefatos originais da pesquisa não foram localizados — não existe OWL, modelo editável nem
script em lugar algum, e o repositório citado na dissertação está 404. O baseline foi remontado a
partir dos diagramas em resolução de origem, em `../Mestrado___OntoMPO/imagens/`.

## O que tem aqui

```
ontologia/
├── evidencias-A1-A9.md            onde cada deficiência está e o que a sustenta
└── baseline/
    ├── ontompo-as-is.ontouml.json  o modelo, no OntoUML Schema
    ├── ontompo-as-is.ttl           a OWL de baseline, transformação gUFO
    ├── ontompo-as-is.owl           a mesma OWL em RDF/XML
    ├── ontompo-as-is.oops.owl      a cópia submetida ao OOPS!, sem owl:imports
    ├── relatorio-plugin-ontouml.md o relatório do verificador, legível
    ├── relatorio-plugin-ontouml.json  o mesmo, bruto
    ├── relatorio-oops.md           o relatório do OOPS!, legível
    ├── relatorio-oops.xml          a resposta bruta do serviço
    └── controle-verificacao.md     o controle que torna interpretável o relatório vazio
```

**Comece por `evidencias-A1-A9.md`.** Ele carrega a leitura dos relatórios; os relatórios sozinhos
não dizem o que importa.

## Como reproduzir

```sh
cd scripts/ontouml && npm ci && cd ../..
node scripts/ontouml/gerar-baseline.js       # modelo, verificação e OWL
node scripts/ontouml/controle-verificacao.js # controle do verificador
pip install rdflib requests
python scripts/rodar_oops.py                 # OOPS! (precisa de rede)
python scripts/verificar_baseline.py         # confere a checklist do ticket 03
```

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

Não é um modelo bom, e não deve ser corrigido aqui. Toda tentação de "arrumar de passagem" um
estereótipo, uma multiplicidade ou um nome destrói o valor deste diretório, que é servir de termo de
comparação. Correção é o ticket 04.

## Anonimato

Os IRIs usam `https://example.org/ontompo/as-is`, que é deliberadamente um domínio de exemplo. O IRI
definitivo entra no ticket 09, junto com o depósito, e precisa continuar não identificando autoria
nem instituição enquanto a revisão for duplamente anônima.
