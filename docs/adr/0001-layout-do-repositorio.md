# 0001 — Layout do repositório: fonte, artefato e ferramenta

Depois de quatro tickets, a raiz do repositório misturava insumo e produto como irmãos indistinguíveis
— as fontes da dissertação ao lado da ontologia gerada, o template SBC ao lado do artigo — sob três
convenções de nome diferentes e sem ponto de entrada. Com dez tickets restantes, cada um produzindo
artefatos novos sem endereço definido, o custo era recorrente. Adotamos um recorte em três buckets:
**`sources/`** é insumo e não se edita, **`artifacts/`** foi produzido aqui, **`tools/`** é como se
produz.

## As quatro faces da decisão

**O recorte é simétrico.** `sources/` e `artifacts/` são irmãos explícitos, em vez de agrupar só as
entradas e deixar as saídas na raiz. Custou uma varredura de 49 caminhos, mas a regra fica enunciável
em uma frase e vale para todo caminho do repositório — inclusive os que ainda não existem.

**O esqueleto é inglês, o domínio é português.** Os buckets e seus filhos imediatos usam inglês
(`sources/dissertation/`, `artifacts/ontology/`, `tools/verification/`); abaixo disso os nomes são de
domínio e ficam em português (`rodada-1/`, `correcoes-rodada-1.md`, `ontompo-as-is.ttl`). A fronteira
não é estética: `rodada-1` está gravado no IRI `https://example.org/ontompo/rodada-1` e aparece na
prosa de doze arquivos. Anglicizar abaixo da linha quebraria o IRI para ganhar coerência de vitrine.

**`tools/model/` guarda a fonte do modelo.** `ontompo-as-is.js` e `ontompo-rodada-1.js` não são
scripts de geração: são a ontologia editável, e os `.ontouml.json` que parecem ser "o modelo" são
gerados a partir deles. Alguém vai perguntar por que a fonte de um artefato mora em `tools/` e não em
`artifacts/` — a resposta é que ela é entrada da ferramenta, não saída dela, e que tanto `generation/`
quanto `verification/` a consomem. Deixá-la em `generation/` classificaria a fonte como ferramenta de
si mesma.

**`.scratch/` foi mantido apesar do nome.** É onde vivem a spec e os catorze tickets, ou seja, a
documentação mais importante do projeto, atrás de um nome que promete rascunho e de um ponto que a
esconde. O caminho é contrato com `CLAUDE.md`, com `docs/agents/issue-tracker.md` e com as skills de
tracker e wayfinder instaladas; renomear quebraria esse contrato e as skills voltariam a escrever em
`.scratch/` de qualquer modo. A legibilidade foi comprada com um `README.md` na raiz que aponta para
lá, não com a renomeação.

## Consequências

- Editar qualquer coisa sob `sources/` é erro: aquele material é o registro do que foi publicado.
- Editar um artefato gerado à mão é erro: a correção some na próxima regeração. Corrija a fonte em
  `tools/model/` e regenere.
- Os verificadores Python leem caminhos relativos ao diretório de trabalho e precisam ser executados
  da raiz.
- `artifacts/paper/` mantém cópias de `sbc-template.sty` e `sbc.bst` vindas de `sources/sbc-template/`,
  porque o LaTeX as exige ao lado do `.tex`. Duplicação deliberada, a atualizar nos dois lugares.
- Os diretórios dos tickets 05–14 (`rodada-2/`, `owl/`, `instancias/`, `consultas/`, `figuras/`,
  `deposit/`) ficam declarados no `README.md` e nascem quando o ticket que os preenche rodar.

A mudança foi de endereço, não de conteúdo: os vinte artefatos de `artifacts/ontology/` foram
regenerados pelos caminhos novos e conferem byte a byte com os anteriores, e os quatro verificadores
das checklists 01–04 passam.
