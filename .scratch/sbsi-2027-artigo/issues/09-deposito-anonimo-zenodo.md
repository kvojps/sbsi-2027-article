# 09: Depósito anônimo dos artefatos

**What to build:** um depósito anônimo, público e funcional com tudo o que a pesquisa produziu, e o
link correspondente pronto para entrar no artigo. Ao fim, um revisor consegue abrir o link em janela
anônima e reexecutar as consultas.

Este ticket existe porque a ausência dele custou caro: o repositório citado no trabalho anterior
retornava 404, e dois revisores registraram que isso os impediu de avaliar os artefatos. Além disso,
"Transparência, Replicabilidade e Reprodutibilidade" é um dos cinco critérios de avaliação da trilha,
e a chamada pede depósito anônimo em repositório como Zenodo ou Figshare.

**Blocked by:** 08 (demais questões de competência)

**Status:** ready-for-human

- [ ] Depósito criado de forma **anônima**, sem revelar autoria — o processo de revisão é duplamente anônimo _(ação humana: subir o pacote no Zenodo)_
- [x] Contém a OWL revisada e o modelo OntoUML em formato aberto
- [x] Contém o diff da transformação gUFO
- [x] Contém todas as consultas SPARQL e seus resultados completos
- [x] Contém os relatórios do plugin OntoUML e do OOPS!, nas versões antes e depois
- [x] Contém os dados de instância dos dois observatórios
- [ ] Link testado em janela anônima, sem sessão autenticada, e funcionando _(ação humana)_
- [x] Nenhum arquivo do depósito contém nome, instituição, e-mail ou usuário identificável
- [ ] Link pronto para ser citado no artigo _(ação humana: entra depois de o Zenodo emitir o DOI)_

## Comments

O **pacote** do depósito está montado, verificado e pronto para subir; o que falta é ação humana no
Zenodo. Divisão:

**Feito aqui**

- `tools/generation/gerar_deposito.py` monta `artifacts/deposit/` a partir de `artifacts/ontology/`
  (ela própria gerada) e da cópia local da gUFO. O pacote tem 72 arquivos: a árvore `ontology/`
  inteira (OWL revisada e customizada, `.ontouml.json` das três camadas, diff da transformação gUFO,
  as sete QCs com `.rq`/`.csv`/`.md`, relatórios do plugin OntoUML e do OOPS! antes e depois, os dois
  observatórios), `gufo/` (gUFO 1.0.0 como distribuída, para a reexecução não depender de rede),
  `README.md` orientando quem chega do artigo, `reexecutar-consultas.py` (só precisa de `rdflib`;
  reexecuta as sete QCs e confere cada resultado contra o `.csv` gravado), `.zenodo.json` sem autoria
  e `MANIFEST.sha256`.
- `tools/verification/verificar_deposito.py` lê o pacote como terceiro (não importa de
  `tools/generation/`): estrutura, conteúdo exigido pela checklist, integridade pelo `MANIFEST`,
  cópia byte a byte em dia com `artifacts/ontology/` e `sources/gufo/`, varredura de anonimato em
  todo arquivo de texto (nomes, instituições, cidade, e-mail, ORCID, `github.com`, marca de autoria
  "próprio autor"/primeira pessoa, caminho absoluto com usuário), `.zenodo.json` bem-formado e sem
  identificação, e o `README` com o passo a passo da reexecução. 501 checagens, verde.
- **Anonimato:** a frase "trabalho anterior do próprio autor" nos cabeçalhos das QCs, em
  `procedencia.md` e num `rdfs:comment` de `observatorio.ttl` ligava a submissão anônima ao artigo de
  2022 nominal. Reescrita na fonte (`tools/generation/gerar_instancias.py` e os `qc*.rq`) para citar
  a publicação-fonte só pelo DOI, em terceira pessoa; artefatos regenerados. Os verificadores dos
  tickets 06, 07 e 08 continuam verdes.
- Reproduzir: `python tools/generation/gerar_deposito.py && python tools/verification/verificar_deposito.py`.

**Pendência humana (por isso `Status: ready-for-human`)**

1. Criar conta/registro no Zenodo **sem** dado identificável e subir o conteúdo de
   `artifacts/deposit/` (zipar preservando os caminhos, ou subir arquivo a arquivo). Os metadados de
   `.zenodo.json` podem ser colados nos campos do formulário; autor = "Anonymous".
2. Publicar e **testar o link em janela anônima**, sem sessão autenticada, baixando o pacote e
   rodando `python reexecutar-consultas.py`.
3. Levar o DOI/link para o artigo (ticket 10/12) e, se se quiser um IRI definitivo para a ontologia
   no lugar do `https://example.org/ontompo/rodada-2#`, fixá-lo então — depende do DOI, que só existe
   após o passo 2. O IRI de exemplo já é anônimo e é uma escolha permanente válida se não se quiser
   trocá-lo.
