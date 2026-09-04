# OntoMPO — artigo para o SBSI 2027 (Trilha de Pesquisa)

Análise ontológica do **MPO** (Modelo para Observatórios de Projetos) fundamentada na UFO, e o modelo
revisado que ela produziu. A contribuição não é formalizar o MPO — é o que a análise revelou sobre
ele. Ver `.scratch/sbsi-2027-artigo/spec.md`.

## A regra de layout

> **`sources/`** é insumo e **não se edita**. **`artifacts/`** foi produzido aqui. **`tools/`** é como
> se produz.

Todo caminho do repositório cai em um dos três. O que não cai é plano (`.scratch/`) ou convenção
(`docs/`).

```
sources/                     ENTRADA — somente leitura
├── dissertation/            fontes LaTeX, imagens e PDF da dissertação
├── ontobras-reviews/        o artigo rejeitado e os cinco pareceres
└── sbc-template/            o template SBC, como distribuído

artifacts/                   SAÍDA — o que esta pesquisa produz
├── ontology/                o modelo e suas verificações  → ver o README de lá
├── paper/                   esqueleto.md, artigo.tex, referencias.bib
├── deposit/                 o pacote do Zenodo anônimo (ticket 09)
└── submission/              o pacote de registro no JEMS3

tools/                       FERRAMENTA — raiz npm única
├── model/                   a fonte editável do modelo (é código, ver abaixo)
├── generation/              produz o que está em artifacts/ontology/
└── verification/            um verificador por ticket

.scratch/sbsi-2027-artigo/   spec.md e os 14 tickets
docs/adr/                    as decisões de arquitetura
CONTEXT.md                   o glossário do domínio
```

## Por onde começar

1. **`CONTEXT.md`** — o vocabulário. *MPO*, *baseline*, *rodada*, *deficiência*, *QC*, *seam*.
2. **`.scratch/sbsi-2027-artigo/spec.md`** — o que é o artigo, e por que ele existe nesta forma.
3. **`.scratch/sbsi-2027-artigo/issues/`** — os 14 tickets, na ordem. O `Status:` de cada um diz onde
   o trabalho está.
4. **`artifacts/ontology/README.md`** — os artefatos, o que mede o antes/depois, e como reproduzir.

## O modelo editável é código

`tools/model/ontompo-as-is.js`, `ontompo-rodada-1.js` e `ontompo-rodada-2.js` **são a ontologia**. Os
`.ontouml.json`, `.ttl` e `.owl` em `artifacts/ontology/` são gerados a partir deles e não se editam à
mão: uma correção feita no artefato desaparece na próxima regeração. Corrija a fonte e regenere.

Por isso a fonte do modelo mora em `tools/model/` e não junto dos artefatos — é entrada da ferramenta,
não saída dela. Ver `docs/adr/0001-layout-do-repositorio.md`.

## Duas cópias deliberadas

`artifacts/paper/` contém cópias de `sbc-template.sty` e `sbc.bst`, originárias de
`sources/sbc-template/`. O LaTeX exige esses arquivos ao lado do `.tex`, então a duplicação é
intencional e o diretório do artigo é autocontido. Ao atualizar o template, atualize as duas.

## Reproduzir

```sh
cd tools && npm ci && cd ..

node tools/generation/gerar-baseline.js                           # ticket 03
node tools/generation/gerar-rodada-1.js                           # ticket 04
node tools/generation/gerar-rodada-2.js                           # ticket 05
node tools/generation/diff-modelos.js
node tools/generation/diff-modelos.js --de=rodada-1 --para=rodada-2
node tools/verification/controle-verificacao.js
node tools/verification/controle-verificacao.js --modelo=rodada-1
node tools/verification/controle-verificacao.js --modelo=rodada-2
node tools/verification/verificador-ufo-extra.js
node tools/verification/verificador-ufo-b-c.js

pip install rdflib requests
python tools/verification/verificar_baseline.py                   # confere a checklist do 03
python tools/verification/verificar_rodada1.py                    # confere a checklist do 04
python tools/verification/verificar_rodada2.py                    # confere a checklist do 05
```

Os verificadores Python leem caminhos relativos ao diretório de trabalho: **execute-os da raiz**.
Tudo é determinístico exceto a resposta do OOPS!, que traz um identificador de requisição novo a cada
chamada. Detalhes em `artifacts/ontology/README.md`.
