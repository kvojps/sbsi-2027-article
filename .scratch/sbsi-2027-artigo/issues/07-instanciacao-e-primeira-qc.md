# 07: Instanciação e primeira questão de competência ponta a ponta

**What to build:** o *tracer bullet* do trabalho. Uma única questão de competência atravessando todo
o caminho — modelo revisado, OWL, dados de instância de um observatório real, consulta SPARQL,
resultado documentado — provando que o percurso inteiro funciona antes de escalar para as demais.

Cenário: um observatório de projetos de pesquisa e extensão de uma universidade pública brasileira,
documentado nos Anais Estendidos do SBSI. **É trabalho anterior do próprio autor: toda menção, no
código, nos dados e no texto, deve ser em terceira pessoa**, jamais como "nosso trabalho anterior".

A QC escolhida para o tracer deve ser de domínio e verificável em instâncias, não estrutural. A
avaliação anterior falhou exatamente aqui: usava consultas que devolveriam a mesma forma para
qualquer ontologia, testando a implementação em vez do domínio.

**Blocked by:** 06 (transformação gUFO e OWL revisada)

**Status:** resolved

- [x] Dados de instância do observatório carregados na ontologia revisada, derivados do que a publicação documenta
- [x] Uma QC de domínio escolhida e executada em SPARQL ponta a ponta
- [x] A consulta interroga conhecimento do domínio, não a estrutura do artefato — não passa se puder ser respondida por qualquer ontologia
- [x] Resultado não-vazio e semanticamente correto, conferido contra o que a fonte documenta
- [x] Consulta e resultado completos salvos em formato reaproveitável pelo apêndice
- [x] Nenhuma menção identificadora ao autor nos dados, nos comentários ou nos rótulos
- [x] O percurso está reproduzível por um terceiro a partir dos artefatos salvos

## Answer

O *tracer* é a **QC1 — "Quais *Views* são disponibilizadas por um dado `DataManager`?"**. É a QC que
`artifacts/ontology/evidencias-A1-A9.md` aponta como impossível de responder sobre o baseline: lá
cada `View` especializa `ProjectObservatory` e a pergunta vira "quais observatórios um observatório
disponibiliza". A correção de A9 (composição no lugar de especialização, com o relator
`ViewProvision`) é justamente o que a torna respondível — então a QC1 exercita, ponta a ponta, um
achado da análise.

**Cenário.** Um observatório de projetos de pesquisa e extensão de uma universidade pública
brasileira, descrito nos *Anais Estendidos do XVIII SBSI* (2022), DOI
`10.5753/sbsi_estendido.2022.222995` — trabalho anterior do próprio autor, referido em terceira
pessoa. `artifacts/ontology/instancias/procedencia.md` liga cada um dos 22 indivíduos a um trecho da
publicação: o observatório (protótipo WordPress), o seu gerenciamento de conteúdo, as oito
funcionalidades da seção 4.1 como `View` no papel que lhes cabe (`CrudView`, `Disseminator`,
`Reporter`), os três perfis de ator da *survey* e o sistema de gestão de projetos citado como
externo. A cadeia de ETL/proveniência fica para o ticket 08, porque a publicação documenta um
protótipo de coleta manual, não um *pipeline*.

**Artefatos.** `instancias/observatorio.ttl` (gerado por `tools/generation/gerar_instancias.py`),
`consultas/qc1.rq`, e o resultado completo em `consultas/qc1-resultado.csv` e `.md` (gerados por
`tools/generation/rodar_consultas.py`). A QC1 devolve **8 linhas**: as oito visões do observatório,
agrupadas em três papéis — `Disseminação` (2), `Visão CRUD` (3), `Relacionamento` (3).

**Verificador.** `tools/verification/verificar_instancia_qc.py`, 116 checagens, lê os artefatos como
terceiro e re-executa a consulta com a própria `rdflib`. Prova que a consulta é de domínio por dois
controles negativos — sem os dados do observatório *ou* sem a ontologia revisada, a QC1 devolve zero
linha — e por um contraste: uma consulta de `subClassOf` devolve linhas sobre a gUFO sozinha, a QC1
não. Confere o resultado salvo byte a byte contra a re-execução, e varre `instancias/` e `consultas/`
por menção identificadora e por primeira pessoa.
