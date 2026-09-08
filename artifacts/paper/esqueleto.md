# Esqueleto do artigo — SBSI 2027, Trilha de Pesquisa em SI

Estrutura vazia porém completa em que o texto vai ser escrito. Nenhum ticket de escrita precisa
decidir formato, seção ou bibliografia: tudo isso está fixado aqui.

- **Título (congelado no ticket 01):** *OntoMPO: Ontological Analysis and Refinement of the Model for
  Project Observatories*
- **Corpo:** português. **Título, resumo estruturado e palavras-chave:** inglês.
- **Bibliografia:** `artifacts/paper/referencias.bib`. Não criar entradas novas sem antes conferir se já
  existe uma com a mesma obra.
- **Scaffold LaTeX:** `artifacts/paper/artigo.tex`. Os nomes de seção aqui e lá são os mesmos, na mesma ordem.
- **Anonimato:** sem nome de autor, instituição, agradecimento, financiador ou link identificável.
  Trabalhos do próprio autor citados em terceira pessoa desde o primeiro rascunho.

## Como compilar e conferir

Serve qualquer distribuição LaTeX com o básico mais `geometry`, `caption`, `titlesec`, `etoolbox`,
`psnfss` com as fontes URW (`times`, `helvetic`, `courier`, `symbol`), `babel-portuges`, `array`,
`fancyvrb`, `float` e `pgf`. Foi compilado em MiKTeX (ticket 02) e em TeX Live (ticket 13). De
dentro de `artifacts/paper/`:

```
pdflatex artigo && bibtex artigo && pdflatex artigo && pdflatex artigo
```

O `sbc-template.sty` e o `sbc.bst` estão copiados neste diretório de propósito: assim `artifacts/paper/` sobe
para o Overleaf inteiro, sem depender de `sources/sbc-template/`.

A conferência automática do andaime é `python tools/verification/verificar_andaime.py`. Ela lê o esqueleto, o
scaffold, a bibliografia e — se existirem — os logs de compilação, e reprova quando o `latin1` do
template volta, quando os nomes de seção divergem entre este arquivo e o `.tex`, quando o orçamento
sai do intervalo de 15 a 20 páginas, quando uma entrada da bibliografia perde um campo obrigatório
do seu tipo, quando um placeholder sobrevive ou quando uma citação fica sem entrada no `.bib`.

## Onde mora o texto

O esqueleto é o plano; o texto de cada seção mora em `secoes/`, um arquivo por seção — e continua
morando só lá. O ticket 13 **gera** `secoes-tex/NN-*.tex` a partir desses arquivos, por
`tools/generation/gerar_secoes_latex.py`, e o `artigo.tex` apenas dá `\input` neles: editar um
`.tex` de seção à mão não adianta, porque a próxima geração desfaz e o verificador do ticket 13
reprova a divergência. Corrija o Markdown e regere.

O que o `artigo.tex` mantém à mão é o preâmbulo, o frontmatter, os cabeçalhos de seção e o Apêndice
A. As figuras saem de `tools/generation/gerar_figuras.py`, a partir do modelo revisado, e o Apêndice
A de `tools/generation/gerar_apendice_sparql.py`, a partir das consultas — nenhum dos dois se edita
à mão tampouco.

## Orçamento de páginas

A chamada rejeita sumariamente abaixo de 15 e acima de 20 páginas. **Os números abaixo são medidos,
não estimados**: saem do porte compilado do ticket 13, bloco a bloco, e cada um é o valor medido mais
duas centésimas. Somam **19,97 páginas**, e o PDF fecha em 20 —
19,72 de conteúdo, sob um teto de 20,00.

**O orçamento de 18,50 páginas que este arquivo trazia até o ticket 13 era inexequível**, e não por
pouco: ele nunca reservou uma linha para figura alguma, e dava 1,50 página a uma bibliografia que
mede 2,77 com as 37 entradas que o texto cita. Somadas as duas omissões ao frontmatter — que precisa
carregar o abstract estruturado em inglês *e* o resumo em português, e mede 1,18 —, o texto escrito
até o ticket 12 compilava em 22 páginas: rejeição sem revisão. Fechar o intervalo custou **1.400
palavras**, cortadas em §1 a §9 com os verificadores dos tickets 10, 11 e 12 rodando a cada passada,
de modo que nenhum item de checklist se perdeu; o resumo em português foi condensado a 176 palavras,
por ser tradução e não conteúdo novo; e as três tabelas e a figura passaram a `[H]`, fixas, porque
flutuando elas atravessavam a fronteira entre seções e faziam a medida por seção oscilar quase uma
página.

A linha da seção 6 inclui a Figura 1: o diagrama entra fixo dentro dela, e não flutuando, então a
meia página que ele ocupa é dela. O corte previsto pela spec — mover os diagramas por camada para o
depósito e manter no artigo o diagrama integrado — foi aplicado: `figuras/camada-*.tex` existem, são gerados do mesmo modelo, e não
entram no PDF.

| # | Seção | Label do resumo estruturado | Páginas |
|---|-------|-----------------------------|---------|
| — | Frontmatter (título, abstract estruturado, resumo, palavras-chave) | todos os sete | 1,18 |
| 1 | Introdução | Research Context; Scientific and/or Practical Problem | 1,26 |
| 2 | Referencial Teórico | Research Context; Related IS Theory | 2,29 |
| 3 | Trabalhos Relacionados | Research Context | 0,80 |
| 4 | Método de Pesquisa | Research Method | 1,37 |
| 5 | Análise Ontológica do MPO | Proposed Solution and/or Analysis | 3,43 |
| 6 | A OntoMPO Revisada | Proposed Solution and/or Analysis | 2,34 |
| 7 | Avaliação | Research Method; Summary of Results | 1,67 |
| 8 | Discussão e Limitações | Summary of Results; Contributions and Impact to IS area | 1,05 |
| 9 | Conclusão e Trabalhos Futuros | Contributions and Impact to IS area | 0,84 |
| — | Declaração de uso de IA generativa | — | 0,32 |
| — | Referências | — | 2,77 |
| — | Apêndice A — Consultas SPARQL e resultados completos | — | 0,65 |
| | **Total** | | **19,97** |

**A folga que resta é de 0,03 página, e isso é a informação,
não um detalhe de contabilidade.** Cada bloco tem duas centésimas acima do que mede hoje, o que faz
do orçamento um alarme: qualquer parágrafo acrescentado reprova o verificador da seção antes de
chegar ao PDF. Acrescentar texto a partir daqui exige cortar em outro lugar na mesma passada.

A seção 5 não é candidata a corte: é onde a contribuição mora. O texto escrito mede **3,41 páginas**
no porte compilado, dentro do que a tabela lhe dá.

Os sete labels do resumo estruturado, na ordem exigida pela chamada: *Research Context*; *Scientific
and/or Practical Problem*; *Proposed Solution and/or Analysis*; *Related IS Theory*; *Research
Method*; *Summary of Results*; *Contributions and Impact to IS area*. Cada um deles aparece em pelo
menos uma seção da tabela acima — é isso que dá coesão entre resumo e corpo.

---

## Frontmatter

*Labels: todos os sete. Orçamento: 1,18 página. Ticket 13.*

Título, abstract estruturado em inglês (texto congelado em `artifacts/submission/jems3-pacote-registro.md`,
campo `resumo`), resumo em português e palavras-chave. Sem autores, sem instituição.

O abstract em inglês do PDF tem de ser **idêntico** ao registrado no JEMS3 — o registro congela em
14/09/2026 e uma divergência entre PDF e registro é achado de conformidade.

**Feito (ticket 13).** O abstract e o resumo estão no `artigo.tex`, mantidos à mão; o abstract em
inglês é cópia literal do texto congelado, e o verificador do ticket 13 compara os dois bloco a
bloco. Os sete labels correm no mesmo parágrafo, e não um por parágrafo: o texto é o mesmo e a
forma economiza 0,15 página de `\parskip`.

---

## 1. Introdução

*Labels: Research Context; Scientific and/or Practical Problem. Orçamento: 1,26 página. Ticket 11.*

**Texto escrito:** `secoes/01-introducao.md`. Conferência (as quatro seções de uma vez):
`python tools/verification/verificar_seccoes_introducao_metodo.py`.

Deve entregar:

- Situar o trabalho no tripé Pessoas, Processos e Tecnologias.
- Domínio de aplicação e problema organizacional apontados explicitamente.
- A motivação de por que observatórios existem, ancorada em Organizational Information Processing
  Theory.
- A tese: modelos conceituais de referência em linguagem natural carregam deficiências
  representacionais sistemáticas e invisíveis a quem os aplica.
- Contribuição conectada ao II GranDSI-Br, nomeando o Desafio 3, "Eco(Sistemas²) de Informação", e
  secundariamente o Desafio 2, "SI Inteligentes sob a Perspectiva Sociotécnica".
- Declaração explícita da contribuição: a análise ontológica e o modelo revisado — não a
  formalização do MPO.
- Mapa do artigo.

<!-- conteúdo: secoes/01-introducao.md (ticket 11) -->

---

## 2. Referencial Teórico

*Labels: Research Context; Related IS Theory. Orçamento: 2,29 páginas. Ticket 11.*

**Texto escrito:** `secoes/02-referencial.md`.

Deve entregar:

- **2.1 Observatórios de projetos** — o que são; posicionados frente a gerenciamento de projetos, a
  monitoramento de projetos e a PMOs. Responde à crítica de terminologia de nicho.
- **2.2 O MPO** — descrição autocontida: as três dimensões, suas subdimensões e os conceitos que a
  análise da seção 5 vai discutir. Um leitor que nunca ouviu falar do MPO precisa acompanhar o resto
  do artigo sem consultar as referências originais.
- **2.3 Representation Theory** — a teoria de SI que sustenta a análise, com sua tipologia:
  *construct overload*, *redundancy*, *excess*, *deficit*.
- **2.4 UFO e OntoUML** — o necessário para acompanhar as decisões de modelagem, incluindo UFO-A,
  UFO-B e UFO-C.

Sem nenhum resquício da defesa de "lightweight ontology" — foi abandonada pela spec. Sem repetir na
seção 4 o que for dito aqui sobre Methontology: a redundância entre seções foi crítica explícita de
um parecer.

<!-- conteúdo: secoes/02-referencial.md (ticket 11) -->

---

## 3. Trabalhos Relacionados

*Label: Research Context. Orçamento: 0,80 página. Ticket 11.*

**Texto escrito:** `secoes/03-trabalhos-relacionados.md`.

Deve entregar:

- Ontologias em contextos de observatório (virtual, solar-terrestre, ambiental, de saúde).
- Análises ontológicas de modelos conceituais fundamentadas em UFO ou em BWW.
- O que este trabalho faz que nenhum deles faz — a lacuna precisa ficar nomeada, não implícita, para
  o revisor que avalia **Novidade**.

<!-- conteúdo: secoes/03-trabalhos-relacionados.md (ticket 11) -->

---

## 4. Método de Pesquisa

*Label: Research Method. Orçamento: 1,37 página. Ticket 11.*

**Texto escrito:** `secoes/04-metodo.md`.

Deve entregar:

- Design Science Research como envelope, e a continuidade com o ciclo DSR sob o qual o próprio MPO
  foi construído e evoluído por focus groups e estudos de caso.
- Methontology como método de construção do artefato, **posicionada frente a LOT e NeOn** — a
  escolha justificada, não apenas declarada.
- O procedimento da análise ontológica: como o MPO foi lido, o que contou como deficiência, como
  cada achado foi classificado na tipologia de Representation Theory.
- O desenho da avaliação, nas três frentes, com a razão de cada uma.

<!-- conteúdo: secoes/04-metodo.md (ticket 11) -->

---

## 5. Análise Ontológica do MPO

*Label: Proposed Solution and/or Analysis. Orçamento: 3,43 páginas. Ticket 10.*

**Texto escrito:** `secoes/05-analise-ontologica.md`. Conferência:
`python tools/verification/verificar_analise_ontologica.py`.

**A seção que separa o artigo aceito do artigo rejeitado.** É a maior do artigo e não é candidata a
corte de páginas.

Deve entregar as nove deficiências, cada uma com o que foi observado, por que é uma deficiência e
como foi corrigida, com justificativa ontológica da UFO — não preferência de modelagem:

| # | Deficiência | Classificação BWW | Correção |
|---|-------------|-------------------|----------|
| A1 | `CrudOperation` colapsa Create/Update/Delete, de pós-condições distintas | *construct overload* | Decompor |
| A2 | `Software` como composição de `Hardware` | *construct excess* / mereologia inválida | Execução/hospedagem |
| A3 | `«MemberOf»` com o coletivo `ObservatoryGroup` declarado na ponta da parte | violação de restrição UFO | Inverter as pontas |
| A4 | Classe de domínio nomeada `Relator`, colidindo com o metaconceito da UFO | *construct redundancy* terminológica | Renomear |
| A5 | ETL como «relator» endurante em vez de evento | *construct deficit* (UFO-B) | Eventos UFO-B |
| A6 | `Agent` como «Kind» genérico, sem distinção físico/social | *construct deficit* (UFO-C) | Taxonomia UFO-C |
| A7 | `System` como «role» sem kind subjacente explícito | *construct deficit* | Explicitar o kind |
| A8 | `Management`/`Operation` como relators n-ários não justificados | ambiguidade de aridade | Justificar ou decompor |
| A9 | `ProjectObservatory` especializa `Software` e é especializado por `DataManager`/`View` | confusão de princípio de identidade | Revisar hierarquia |

Além disso:

- Antes/depois visível para as deficiências cuja correção muda o diagrama.
- Evidência das ferramentas citada onde ela existe, com a diferença entre os relatórios antes e
  depois.
- O que decorre disso para o domínio: por que duas iniciativas podiam se declarar aderentes ao MPO
  adotando interpretações semanticamente incompatíveis.
- Deficiências detectadas pelas ferramentas além de A1–A9 incorporadas ou descartadas com
  justificativa.

Tom: as deficiências são do modelo original e da formalização anterior; a correção é construtiva. O
resultado é evolução do MPO, não desqualificação dele.

Rastreabilidade: cada linha de A1–A9 precisa aparecer em três lugares — no modelo revisado, no
relatório do plugin e no texto desta seção. Achado órfão é defeito.

<!-- conteúdo: secoes/05-analise-ontologica.md (ticket 10) -->

---

## 6. A OntoMPO Revisada

*Label: Proposed Solution and/or Analysis. Orçamento: 2,34 páginas, a Figura 1 incluída. Ticket 12; a figura é do 13.*

Deve entregar:

- A ontologia revisada apresentada com os conceitos **descritos**, não apenas listados.
- O diagrama integrado (os diagramas por camada migram para o depósito se a paginação apertar).
- O caminho do OntoUML ao OWL: a transformação gUFO com a ferramenta oficial, o que foi customizado
  sobre o gerado e a publicação do diff.
- Métricas do artefato.

**Texto escrito:** `secoes/06-ontompo-revisada.md`. Conferência (as quatro seções e a declaração de
uma vez): `python tools/verification/verificar_seccoes_ontologia_avaliacao_conclusao.py`.

<!-- conteúdo: secoes/06-ontompo-revisada.md (ticket 12) -->

---

## 7. Avaliação

*Labels: Research Method; Summary of Results. Orçamento: 1,67 página. Ticket 12.*

Deve entregar as três frentes, nesta ordem de importância:

1. **Questões de competência sobre o cenário instanciado.** As sete QCs, cada uma com resultado
   não-vazio e semanticamente correto. Cenário descrito em terceira pessoa, sem identificar o autor.
2. **Plugin OntoUML** — conformidade sintática e semântica à UFO, com números antes e depois.
3. **OOPS!** — pitfalls, com números antes e depois.

Consultas e resultados **completos** referenciados no Apêndice A ou no depósito, nunca só
sumarizados: a avaliação sumarizada foi crítica explícita de um parecer.

**Texto escrito:** `secoes/07-avaliacao.md`.

<!-- conteúdo: secoes/07-avaliacao.md (ticket 12) -->

---

## 8. Discussão e Limitações

*Labels: Summary of Results; Contributions and Impact to IS area. Orçamento: 1,05 página. Ticket 12.*

Deve entregar:

- Lições aprendidas, não repetição de resultados. Um parecer criticou exatamente isso.
- O que a análise diz sobre modelos de referência em linguagem natural em geral.
- Limitações declaradas pelos próprios autores, entre elas:
  - ausência de sessão de validação com especialistas — declarada contra o pano de fundo de que a
    avaliação do MPO na literatura foi feita por focus groups e estudos de caso múltiplos;
  - uso de um observatório sintético na comparação da QC7;
  - ausência de implantação operacional e de axiomatização pesada.

**Texto escrito:** `secoes/08-discussao-limitacoes.md`.

<!-- conteúdo: secoes/08-discussao-limitacoes.md (ticket 12) -->

---

## 9. Conclusão e Trabalhos Futuros

*Label: Contributions and Impact to IS area. Orçamento: 0,84 página. Ticket 12.*

Deve entregar:

- A contribuição para SI: base semântica verificável para auditar aderência ao MPO, rastreabilidade
  de proveniência para prestação de contas, e um procedimento reusável para auditar modelos de
  referência descritos em linguagem natural.
- Trabalhos futuros: estudo comparativo entre observatórios reais, alinhamento com ontologias de
  gerenciamento de projetos, e integração com LLMs como direção — não como resultado.

**Texto escrito:** `secoes/09-conclusao.md`.

<!-- conteúdo: secoes/09-conclusao.md (ticket 12) -->

---

## Declaração de uso de IA generativa

*Orçamento: 0,32 página. Ticket 12.*

Exigida pelo Código de Conduta da SBC. Nomear as ferramentas e onde foram empregadas. Sem
identificar autoria. Não é seção numerada: entra no `.tex` como `\section*`, depois da conclusão.

**Texto escrito:** `secoes/declaracao-ia.md`.

<!-- conteúdo: secoes/declaracao-ia.md (ticket 12) -->

---

## Referências

*Orçamento: 2,77 páginas.*

Geradas por BibTeX de `artifacts/paper/referencias.bib` com o estilo `sbc`. Precisam estar presentes, pela
chamada e pelos pareceres:

- Anais do SBSI;
- Anais Estendidos do SBSI;
- iSys — Revista Brasileira de Sistemas de Informação;
- II GranDSI-Br.

Nenhuma chamada quebrada do tipo `[?]` sobrevive.

---

## Apêndice A — Consultas SPARQL e resultados completos

*Orçamento: 0,65 página. Ticket 13.*

As sete consultas e seus resultados completos, ou remissão explícita ao depósito anônimo quando não
couberem. O link do depósito precisa ser anônimo e funcional — o repositório 404 foi crítica de um
parecer.

**Feito (ticket 13).** As sete somam 273 linhas e não cabem na página orçada, então o apêndice faz
as duas coisas que a checklist admite: traz a QC7 na íntegra — a consulta de que a contribuição
depende — e remete ao depósito, nomeando `ontology/consultas/qcN.rq`, `qcN-resultado.csv`,
`divergencias.md` e o `reexecutar-consultas.py` que confere cada uma contra o arquivo gravado.
Gerado por `tools/generation/gerar_apendice_sparql.py`: o corpo da consulta sai do `.rq` e as
contagens de linha, dos `.csv`. O DOI do depósito entra quando o ticket 09 sair da pendência
humana.
