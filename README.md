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
├── gufo/                    a gUFO 1.0.0, como distribuída, com o SHA-256 registrado
├── ontobras-reviews/        o artigo rejeitado e os cinco pareceres
└── sbc-template/            o template SBC, como distribuído

artifacts/                   SAÍDA — o que esta pesquisa produz
├── ontology/                o modelo, a OWL e suas verificações  → ver o README de lá
├── paper/                   esqueleto.md, secoes/, secoes-tex/, figuras/, artigo.tex
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

## O texto do artigo também é gerado

O texto mora em `artifacts/paper/secoes/*.md`, um arquivo por seção, e **só lá**. O
`artifacts/paper/secoes-tex/*.tex` é gerado dele por `tools/generation/gerar_secoes_latex.py`, e o
`artigo.tex` apenas dá `\input` nesses arquivos — editar um `.tex` de seção à mão desaparece na
próxima geração, e `verificar_port_latex.py` reprova a divergência conferindo, trecho a trecho, se o
PDF diz o que o Markdown diz. O mesmo vale para `figuras/` e para `apendice-sparql.tex`.

O que o `artigo.tex` mantém à mão é o preâmbulo, o frontmatter e os cabeçalhos de seção.

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

pip install rdflib requests owlrl
python tools/generation/customizar_owl.py                         # ticket 06
python tools/verification/raciocinador.py
python tools/verification/rodar_oops.py artifacts/ontology/owl/ontompo.ttl
python tools/verification/comparar_oops.py
python tools/generation/gerar_instancias.py                       # tickets 07 e 08 (os dois observatorios)
python tools/generation/rodar_consultas.py                        # as sete QCs, consultas/*.rq
python tools/verification/verificar_baseline.py                   # confere a checklist do 03
python tools/verification/verificar_rodada1.py                    # confere a checklist do 04
python tools/verification/verificar_rodada2.py                    # confere a checklist do 05
python tools/verification/verificar_owl.py                        # confere a checklist do 06
python tools/verification/verificar_instancia_qc.py               # confere a checklist do 07
python tools/verification/verificar_demais_qc.py                  # confere a checklist do 08

python tools/generation/gerar_deposito.py                         # monta artifacts/deposit/ (ticket 09)
python tools/verification/verificar_deposito.py                   # confere a checklist do 09
python tools/verification/verificar_analise_ontologica.py         # confere a checklist do 10
python tools/verification/verificar_seccoes_introducao_metodo.py  # confere a checklist do 11
python tools/verification/verificar_seccoes_ontologia_avaliacao_conclusao.py  # a checklist do 12

python tools/generation/gerar_secoes_latex.py                     # porta secoes/*.md -> secoes-tex/ (13)
python tools/generation/gerar_figuras.py                          # os diagramas, do modelo revisado (13)
python tools/generation/gerar_apendice_sparql.py                  # o Apendice A, das consultas (13)
cd artifacts/paper && pdflatex artigo && bibtex artigo && pdflatex artigo && pdflatex artigo && cd ../..
python tools/verification/verificar_port_latex.py                 # confere a checklist do 13
python tools/verification/controle-port-latex.py                  # controle positivo do verificador do 13
```

O PDF do artigo depende de uma distribuição LaTeX com o básico mais `geometry`, `caption`,
`titlesec`, `etoolbox`, `psnfss` com as fontes URW, `babel-portuges`, `array`, `fancyvrb`, `float` e
`pgf`; e `verificar_port_latex.py` precisa também de `pdftotext` e `pdfinfo` (poppler) para ler o PDF
compilado.

Os verificadores Python leem caminhos relativos ao diretório de trabalho: **execute-os da raiz**.
Tudo é determinístico exceto a resposta do OOPS!, que traz um identificador de requisição novo a cada
chamada — e as duas chamadas ao OOPS! precisam de rede. Detalhes em `artifacts/ontology/README.md`.
