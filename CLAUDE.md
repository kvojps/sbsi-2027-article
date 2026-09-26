# sbsi-article

## Layout

`sources/` é insumo e **não se edita**; `artifacts/` foi produzido aqui; `tools/` é como se produz.

- **Artefato gerado não se edita à mão.** A fonte do modelo é `tools/model/*.js`; os `.ontouml.json`,
  `.ttl` e `.owl` em `artifacts/ontology/` derivam dela. Corrija a fonte e regenere por
  `tools/generation/`.
- **`artifacts/ontology/baseline/` não se corrige**, nunca: é a metade "antes" do antes/depois.
- **Todo ticket ganha um verificador** em `tools/verification/`, que lê o artefato como terceiro, sem
  importar do código que o gerou. Execute-os da raiz do repositório.

## Gerar LaTeX e PDF do artigo

O Markdown em `artifacts/paper/secoes/` é a fonte do texto. Para gerar os arquivos LaTeX em
`artifacts/paper/secoes-tex/`, execute da raiz:

```sh
python3 tools/generation/gerar_secoes_latex.py
```

Não edite `secoes-tex/*.tex` à mão. Para gerar `artifacts/paper/artigo.pdf`, execute o ciclo abaixo:

```sh
TEXLIVE_BIN=/home/kvojps/texlive/2026/bin/x86_64-linux
cd artifacts/paper
"$TEXLIVE_BIN/pdflatex" -interaction=nonstopmode artigo.tex
"$TEXLIVE_BIN/bibtex" artigo
"$TEXLIVE_BIN/pdflatex" -interaction=nonstopmode artigo.tex
"$TEXLIVE_BIN/pdflatex" -interaction=nonstopmode artigo.tex
```

A instalação TeX Live não entra automaticamente no `PATH`. Para conferir o PDF gerado, volte à raiz
e rode:

```sh
TEXLIVE_BIN=/home/kvojps/texlive/2026/bin/x86_64-linux \
  PATH="$TEXLIVE_BIN:$PATH" python3 tools/verification/verificar_port_latex.py
```

Mapa em `README.md`, vocabulário em `CONTEXT.md`, razões em `docs/adr/0001-layout-do-repositorio.md`.

## Agent skills

### Issue tracker

Issues live as markdown files under `.scratch/<feature-slug>/` in this repo. See `docs/agents/issue-tracker.md`.

### Triage labels

The five canonical triage roles, using their default label strings. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
