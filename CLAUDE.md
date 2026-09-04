# sbsi-article

## Layout

`sources/` é insumo e **não se edita**; `artifacts/` foi produzido aqui; `tools/` é como se produz.

- **Artefato gerado não se edita à mão.** A fonte do modelo é `tools/model/*.js`; os `.ontouml.json`,
  `.ttl` e `.owl` em `artifacts/ontology/` derivam dela. Corrija a fonte e regenere por
  `tools/generation/`.
- **`artifacts/ontology/baseline/` não se corrige**, nunca: é a metade "antes" do antes/depois.
- **Todo ticket ganha um verificador** em `tools/verification/`, que lê o artefato como terceiro, sem
  importar do código que o gerou. Execute-os da raiz do repositório.

Mapa em `README.md`, vocabulário em `CONTEXT.md`, razões em `docs/adr/0001-layout-do-repositorio.md`.

## Agent skills

### Issue tracker

Issues live as markdown files under `.scratch/<feature-slug>/` in this repo. See `docs/agents/issue-tracker.md`.

### Triage labels

The five canonical triage roles, using their default label strings. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` and `docs/adr/` at the repo root. See `docs/agents/domain.md`.
