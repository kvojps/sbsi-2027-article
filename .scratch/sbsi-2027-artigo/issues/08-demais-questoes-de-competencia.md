# 08: Demais questões de competência

**What to build:** as seis questões de competência restantes executadas sobre o cenário instanciado,
com consultas e resultados completos prontos para o apêndice. Ao fim, a avaliação funcional do artigo
está inteira e é reproduzível por um terceiro.

As sete QCs, todas de domínio e verificáveis em instâncias, substituindo integralmente as cinco QCs
estruturais anteriores:

1. Quais *Views* são disponibilizadas por um dado `DataManager`?
2. Quais partes interessadas têm acesso a quais conteúdos de um projeto observado?
3. Que agente executou a carga de uma dada fonte de dados, e quando?
4. Quais projetos de um observatório não tiveram observações registradas em um período?
5. Que motivações levam cada tipo de ator a interagir com o observatório?
6. Dado um conteúdo divulgado, qual a cadeia de proveniência até a fonte de dados original?
7. Dois observatórios distintos que se dizem aderentes ao MPO cobrem os mesmos conceitos?

As duas últimas sustentam a contribuição: proveniência e comparabilidade entre iniciativas.

**Premissa registrada:** a QC7 exige um segundo observatório. Nesta versão ele é **sintético**,
construído para exercitar a comparação — o que cabe no prazo. Instanciar um segundo caso real
extraído da literatura seria mais convincente para o revisor e fica registrado como upgrade caso
sobre tempo antes de 11/09.

**Blocked by:** 07 (instanciação e primeira QC ponta a ponta)

**Status:** resolved

- [x] As seis QCs restantes executadas em SPARQL sobre o cenário instanciado
- [x] Cada uma retorna resultado não-vazio e semanticamente correto
- [x] Nenhuma delas é respondível por uma ontologia arbitrária — todas interrogam o domínio
- [x] QC6 devolve cadeia de proveniência completa, do conteúdo divulgado até a fonte original
- [x] Segundo observatório sintético instanciado, suficiente para a QC7 exercitar a comparação de cobertura conceitual
- [x] Consultas e resultados completos salvos, prontos para o apêndice — resumo não basta, foi crítica explícita no ONTOBRAS
- [x] Divergências entre resultado esperado e obtido registradas, mesmo quando favorecem o modelo

## Answer

As seis QCs restantes estão em `artifacts/ontology/consultas/qc2.rq` … `qc7.rq`, cada uma com a
pergunta no cabeçalho e o resultado completo em `qc<n>-resultado.csv` e `.md` (gerados por
`tools/generation/rodar_consultas.py`). Todas devolvem resultado não-vazio sobre o cenário
instanciado:

| QC | Pergunta | Linhas | Como interroga o domínio |
|---|---|---|---|
| QC2 | Partes interessadas × conteúdos de um projeto observado | 4 | percorre `SocialInteraction` (Agent–Reporter), `ViewProvision` e `ProjectDataManagement` |
| QC3 | Que agente executou a carga de uma dada fonte, e quando | 4 | `DataSource` → `Extract` → `EtlProcess` → `Load`, participante `Storer`/`Processor`, `gufo:hasEndPointInXSDDate` |
| QC4 | Projetos de um observatório sem observação num período | 1 | `Observation` datada, roteada por `Disseminator`/`ViewProvision`/`ProjectDataManagement`; `FILTER NOT EXISTS` |
| QC5 | Motivações por tipo de ator | 7 | agrupa por subtipo de `Agent` (taxonomia da rodada 2), motivação em `dct:description` do `SocialInteraction` |
| QC6 | Cadeia de proveniência de um conteúdo divulgado até a fonte | 4 | `Disseminator` → `ViewProvision` → `Storer`/`Load` → `EtlProcess` → `Extract` → `DataSource`, nó a nó |
| QC7 | Dois observatórios aderentes ao MPO cobrem os mesmos conceitos? | 31 | conta, por conceito da OntoMPO, instâncias de cada observatório via `rdfs:subClassOf*` |

**Domínio, não estrutura.** `verificar_demais_qc.py` prova por controle negativo que cada consulta
depende da ontologia revisada *e* dos dados do observatório: sem uma ou outra, zero linha; uma
consulta de `subClassOf` devolve linhas sobre a gUFO sozinha, as sete QCs não.

**QC7 — o segundo observatório.** `artifacts/ontology/instancias/observatorio-b.ttl`, sintético (um
observatório municipal de obras públicas, sem fonte na literatura, sem `dct:creator`). Cobre de
propósito um recorte diferente: tem `Organization`/`SocialAgent`, não tem `Reporter`,
`SocialInteraction`, `Observation`, `Knowledge`, `ObservatoryGroup` nem `StakeHolder`. A QC7 devolve
**8 conceitos** em que os dois divergem, apesar de ambos se dizerem aderentes ao MPO — a
subdeterminação tornada verificável. A premissa (segundo caso sintético, não real) está registrada
no ticket e em `procedencia.md`; um segundo caso real fica como *upgrade*.

**Divergências.** `artifacts/ontology/consultas/divergencias.md`, uma seção por QC, com o esperado e
o obtido. As que apontam limite do modelo revisado — sem relação `Observation`→`Project` (QC4), sem
classe de motivação (QC5), sem participação `Agent`(pessoa)→ETL (QC3), cadeia de proveniência que
abre em leque (QC6) — estão registradas contra o modelo, não escondidas.

**Premissas no cenário principal.** Ao `observatorio.ttl` do ticket 07 (22 indivíduos) somam-se 30:
a cadeia de ETL das duas fontes com carimbo de tempo, o módulo de coleta `gerenciadorDeColeta`, dois
projetos-exemplo, duas observações datadas, três partes interessadas e sete interações com motivação.
O que vai além do que a publicação documenta — a segunda fonte, o módulo de coleta, os nomes de
projeto, as datas — está marcado como premissa em `procedencia.md`. A QC1 do ticket 07 continua
devolvendo as mesmas 8 linhas.

**Verificador.** `tools/verification/verificar_demais_qc.py`, 271 checagens, lê os artefatos como
terceiro e re-executa as seis consultas com a própria `rdflib`. Confere a cadeia da QC6 vínculo a
vínculo, a divergência da QC7 nos dois sentidos, o CSV byte a byte contra a re-execução, e varre os
artefatos novos por menção identificadora e primeira pessoa. `verificar_instancia_qc.py` (ticket 07)
continua passando.
