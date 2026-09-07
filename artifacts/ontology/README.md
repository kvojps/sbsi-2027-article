# Artefatos ontológicos da OntoMPO

> O mapa do repositório inteiro está em `../../README.md`; o vocabulário, em `../../CONTEXT.md`.

Este diretório guarda os artefatos da ontologia, em três camadas que convivem:

- **`baseline/`**, o modelo OntoUML reconstruído *exatamente como publicado*, sem nenhuma correção —
  a metade "antes" do antes/depois do artigo (ticket 03);
- **`rodada-1/`**, o modelo depois da primeira rodada de revisão, que corrige A1, A2, A3, A4, A8 e
  A9 (ticket 04);
- **`rodada-2/`**, o modelo depois da segunda, que adota UFO-B e UFO-C e corrige A5, A6 e A7, mais o
  achado B8 que a rodada anterior deixou endereçado a ela (ticket 05).

Ao lado delas, **`owl/`** guarda o artefato OWL propriamente dito: a OWL da rodada 2 com as
customizações aplicadas por cima, e o diff que separa o que a ferramenta gerou do que foi
acrescentado (ticket 06). Não é uma quarta rodada — é a mesma rodada 2, na camada OWL.

**`instancias/`** e **`consultas/`** guardam a avaliação funcional: os dados de instância de um
observatório real, derivados de uma publicação, um segundo observatório sintético para a
comparação, e as sete questões de competência executadas em SPARQL sobre eles. O ticket 07 abriu as
duas com uma QC ponta a ponta; o ticket 08 completa as sete e registra em `consultas/divergencias.md`
onde o resultado obtido divergiu do esperado.

As rodadas seguintes entram como diretórios irmãos. Nenhuma substitui a anterior nem o baseline: é a
comparação entre as três que dá evidência.

Os artefatos originais da pesquisa não foram localizados — não existe OWL, modelo editável nem
script em lugar algum, e o repositório citado na dissertação está 404. O baseline foi remontado a
partir dos diagramas em resolução de origem, em `../../sources/dissertation/imagens/`.

## O que tem aqui

```
artifacts/ontology/
├── evidencias-A1-A9.md            onde cada deficiência está e o que a sustenta
├── correcoes-rodada-1.md          o par antes/depois e a justificativa de cada correção
├── correcoes-rodada-2.md          o mesmo, para a adoção de UFO-B e UFO-C
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
├── rodada-1/
│   ├── ontompo-rodada-1.ontouml.json  o modelo revisado, no OntoUML Schema
│   ├── ontompo-rodada-1.ttl           a OWL da rodada, mesma transformação gUFO
│   ├── relatorio-plugin-ontouml.md    o relatório do verificador, legível
│   ├── relatorio-plugin-ontouml.json  o mesmo, bruto
│   ├── relatorio-verificador-extra.md o verificador complementar, antes contra depois
│   ├── relatorio-verificador-extra.json  o mesmo, bruto
│   ├── controle-verificacao.md        o controle, agora sobre o modelo revisado
│   └── diff-as-is-rodada-1.md         o diff estrutural, derivado dos dois modelos
├── rodada-2/
│   ├── ontompo-rodada-2.ontouml.json  o modelo com UFO-B e UFO-C, no OntoUML Schema
│   ├── ontompo-rodada-2.ttl           a OWL da rodada, mesma transformação gUFO
│   ├── relatorio-plugin-ontouml.md    o relatório do verificador, legível
│   ├── relatorio-plugin-ontouml.json  o mesmo, bruto
│   ├── relatorio-verificador-ufo-b-c.md   as nove regras estruturais, nos três modelos
│   ├── relatorio-verificador-ufo-b-c.json o mesmo, bruto
│   ├── controle-verificacao.md        o controle, agora sobre a rodada 2
│   └── diff-rodada-1-rodada-2.md      o diff estrutural entre as duas rodadas
├── owl/
│   ├── ontompo.ttl                    a OWL customizada, sobre a gerada da rodada 2
│   ├── ontompo.owl                    a mesma OWL em RDF/XML
│   ├── ontompo.oops.owl               a copia submetida ao OOPS!, sem owl:imports
│   ├── customizacoes.md               as cinco customizacoes, cada uma com sua justificativa
│   ├── diff-gerado-customizado.md     o diff entre a gerada e a customizada, legivel
│   ├── diff-gerado-customizado.ttl    o mesmo, so as triplas acrescentadas
│   ├── metricas.md                    classes, propriedades e axiomas, nos tres artefatos
│   ├── relatorio-raciocinador.md      a consistencia por raciocinador, e o controle dela
│   ├── relatorio-raciocinador.json    o mesmo, bruto
│   ├── relatorio-oops.md              o relatorio do OOPS! sobre a revisada
│   ├── relatorio-oops.xml             a resposta bruta do servico
│   └── comparacao-oops.md             o antes/depois de pitfalls, contra o baseline
├── instancias/
│   ├── observatorio.ttl              os dados de instancia do observatorio principal, Turtle deterministica
│   ├── observatorio-b.ttl            o segundo observatorio, sintetico, so para a QC7 (ticket 08)
│   └── procedencia.md               o mapa trecho-da-publicacao -> instancia e as premissas do ticket 08
└── consultas/
    ├── qc1.rq .. qc7.rq              as sete QCs em SPARQL, cada uma com a pergunta no cabecalho
    ├── qc<n>-resultado.csv           o resultado completo, cru, reaproveitavel pelo apendice
    ├── qc<n>-resultado.md            a pergunta, a consulta verbatim e a tabela do resultado
    └── divergencias.md               esperado x obtido por QC, inclusive onde a divergencia favorece o modelo
```

O ticket 07 abriu `consultas/` com a QC1 ponta a ponta; o ticket 08 completa as sete — QC2 a QC7
sobre o cenario instanciado, com o segundo observatorio para a QC7 exercitar a comparacao de
cobertura. Ver `../../docs/adr/0001-layout-do-repositorio.md`.

**Comece por `evidencias-A1-A9.md`, `correcoes-rodada-1.md` e `correcoes-rodada-2.md`, e depois
por `owl/customizacoes.md`.** Eles carregam a leitura dos relatórios; os relatórios sozinhos não
dizem o que importa.

## A medição do antes/depois

O verificador do plugin OntoUML devolve **zero problemas sobre os três modelos**: as deficiências
A1–A9 estão todas fora do alcance das suas 24 regras, que tratam de estereótipo, provedor de
identidade, natureza e generalização. Zero contra zero não mede revisão.

Quem mede são os dois verificadores estruturais, que operacionalizam restrições da UFO fora daquele
conjunto e crescem junto com as rodadas:

| Instrumento | O que acrescenta | *as-is* | rodada 1 | rodada 2 |
|---|---|---|---|---|
| `verificador-ufo-extra.js` (ticket 04) | mereologia, dependência existencial, aridade, colisão de nome | 10 | 1 | — |
| `verificador-ufo-b-c.js` (ticket 05) | as cinco acima **mais** ausência de UFO-B e guarda da adoção | 12 | 3 | 0 |

O segundo aplica as nove regras aos três modelos, e não só às suas próprias: uma rodada que zerasse
as regras novas reintroduzindo as que a anterior fechou apareceria ali.

Na camada OWL a medição é outra, e são duas. O **OOPS!** roda sobre o baseline e sobre a customizada,
pelo mesmo caminho de código, e a comparação está em `owl/comparacao-oops.md`: contando só elementos
no namespace da OntoMPO, os apontados caem de **60 para 0**. O **raciocinador** confere consistência
e traz a sua própria bateria de mutações, em `owl/relatorio-raciocinador.md`; metade delas só é
acusada depois da customização, e é essa metade que mede o que ela acrescentou de conteúdo lógico.

As regras vêm em dois tipos. As de **medição** disparam sobre o baseline, e a execução reprova se
alguma deixar de disparar — sem controle positivo, o zero do revisado não seria interpretável. As de
**guarda** só podem disparar sobre um modelo que já adotou a microteoria; o controle positivo delas
é uma mutação do próprio modelo revisado, e a execução reprova se a mutação passar despercebida.

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

# rodada 2 (ticket 05)
node tools/generation/gerar-rodada-2.js                           # modelo, verificação e OWL
node tools/verification/controle-verificacao.js --modelo=rodada-2 # controle sobre a rodada 2
node tools/verification/verificador-ufo-b-c.js                    # as nove regras, nos três modelos
node tools/generation/diff-modelos.js --de=rodada-1 --para=rodada-2

pip install rdflib requests owlrl

# OWL customizada (ticket 06)
python tools/generation/customizar_owl.py                         # a OWL, o diff e as métricas
python tools/verification/raciocinador.py                         # consistência, com controle por mutação
python tools/verification/rodar_oops.py artifacts/ontology/owl/ontompo.ttl   # OOPS! sobre a revisada (rede)
python tools/verification/comparar_oops.py                        # o antes/depois de pitfalls

# instanciacao e as sete QCs (tickets 07 e 08)
python tools/generation/gerar_instancias.py                       # observatorio.ttl e observatorio-b.ttl
python tools/generation/rodar_consultas.py                        # executa consultas/*.rq (QC1 a QC7)

# as checklists
python tools/verification/rodar_oops.py                           # OOPS! sobre o baseline (rede)
python tools/verification/verificar_baseline.py                   # confere a checklist do ticket 03
python tools/verification/verificar_rodada1.py                    # confere a checklist do ticket 04
python tools/verification/verificar_rodada2.py                    # confere a checklist do ticket 05
python tools/verification/verificar_owl.py                        # confere a checklist do ticket 06
python tools/verification/verificar_instancia_qc.py               # confere a checklist do ticket 07
python tools/verification/verificar_demais_qc.py                  # confere a checklist do ticket 08
```

As duas execuções do OOPS! precisam de rede, e é a `owl/ontompo.ttl` que vai à segunda — a OWL
customizada, não a que sai direto da transformação. Rodá-lo sobre a gerada mediria uma versão
intermediária que nenhum artefato guarda.

Tudo é determinístico exceto a resposta do OOPS!, que traz um identificador de requisição novo a cada
chamada: `relatorio-oops.xml` muda de conteúdo a cada execução mesmo sem nada ter mudado no modelo.
Os demais arquivos são byte a byte idênticos entre execuções — os identificadores da `ontouml-js` e
os rótulos de nó anônimo da `rdflib`, que são sorteados, foram fixados de forma determinística
justamente para isso, e o percurso do grafo é ordenado antes de serializar, porque o `Memory` da
`rdflib` não o percorre na ordem em que recebeu as triplas.

## Ferramentas

| Ferramenta | Versão | Papel |
|---|---|---|
| `ontouml-js` | 0.5.0 | construção do modelo, `OntoumlVerification` e `Ontouml2Gufo` |
| OOPS! | serviço REST em `oops.linkeddata.es/rest` | *pitfalls* de OWL |
| `rdflib` | 7.x | Turtle → RDF/XML, e a customização da OWL |
| `owlrl` | 7.x | raciocinador, no perfil OWL 2 RL |
| gUFO | 1.0.0, cópia em `../../sources/gufo/` | a ontologia de fundamentação que a OWL importa |

A `ontouml-js` 0.5.0 é a última versão que ainda expõe `OntoumlVerification` e `Ontouml2Gufo`; a
1.0.0 removeu as duas. É o mesmo motor que o plugin OntoUML para o Visual Paradigm invoca, e o JSON
gerado está no formato de intercâmbio do plugin — o modelo abre no Visual Paradigm sem conversão.

O `owlrl` cobre o perfil OWL 2 RL, e só ele: foi escolhido por ser o único raciocinador disponível
sem uma máquina virtual Java. O que fica de fora está escrito em `owl/relatorio-raciocinador.md`, e
não é pouco — as restrições de cardinalidade qualificada, que são justamente o que a transformação
gUFO gera a partir das multiplicidades do modelo.

## O que o baseline não é

Não é um modelo bom, e não deve ser corrigido. Toda tentação de "arrumar de passagem" um estereótipo,
uma multiplicidade ou um nome destrói o valor de `baseline/`, que é servir de termo de comparação —
`verificar_rodada1.py` e `verificar_rodada2.py` reprovam se o baseline for mexido. O mesmo vale para
`rodada-1/`, que é a metade "antes" da rodada 2. Correção vai sempre na rodada seguinte.

## Anonimato

Os IRIs usam `https://example.org/ontompo/as-is`, `.../rodada-1` e `.../rodada-2`, que são
deliberadamente de um domínio de exemplo. A OWL customizada mantém o IRI da rodada 2, porque a
customização é aditiva e trocar o IRI seria alterar o que a transformação gerou; ela declara licença
e prefixo preferido, e **não** declara `dct:creator`. O IRI definitivo entra no ticket 09, junto com o depósito,
e precisa continuar não identificando autoria nem instituição enquanto a revisão for duplamente
anônima.
