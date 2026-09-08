# 12: Seções da ontologia revisada, avaliação, discussão e conclusão

**What to build:** o fechamento do texto. Apresenta o artefato revisado e como ele foi obtido,
relata a avaliação com evidência reproduzível, discute o que se aprendeu e declara os limites do
trabalho. Ao fim, o artigo está escrito por inteiro em Markdown.

Duas críticas do ONTOBRAS dependem especificamente deste ticket: a de que a conclusão resumia
resultados em vez de discutir lições aprendidas e limitações, e a de que a avaliação era apresentada
apenas de forma sumarizada, o que a tornava irreproduzível.

**Blocked by:** 08 (demais questões de competência), 10 (seção de análise ontológica), 11 (introdução a método)

**Status:** resolved

- [x] Ontologia revisada apresentada, com os conceitos descritos e não apenas listados
- [x] Caminho do OntoUML ao OWL descrito, incluindo a transformação gUFO e o que foi customizado sobre o gerado
- [x] Métricas do artefato reportadas
- [x] Avaliação relatada nas três frentes: questões de competência sobre o cenário instanciado, verificação pelo plugin e OOPS!, com números antes e depois
- [x] Consultas e resultados completos referenciados em apêndice ou no depósito, nunca só resumidos
- [x] Cenário de instanciação descrito em terceira pessoa, sem identificar o autor
- [x] Discussão traz lições aprendidas, não repetição de resultados
- [x] Limitações declaradas, entre elas a ausência de sessão de validação com especialistas e o uso de um observatório sintético na comparação
- [x] Trabalhos futuros incluem estudo comparativo entre observatórios reais e alinhamento com ontologias de gerenciamento de projetos
- [x] Declaração explícita de uso de IA generativa, nomeando ferramentas e onde foram empregadas, conforme o Código de Conduta da SBC
- [x] Cabe no orçamento de páginas previsto

## Comments

Texto em `artifacts/paper/secoes/06-ontompo-revisada.md`, `07-avaliacao.md`,
`08-discussao-limitacoes.md`, `09-conclusao.md` e `declaracao-ia.md` — um arquivo por superfície,
como nos tickets 10 e 11, e o `<!-- conteúdo: ticket 12 -->` de cada uma virou ponteiro para o
arquivo. Conferência: `python tools/verification/verificar_seccoes_ontologia_avaliacao_conclusao.py`.
Com isso o corpo do artigo está inteiro escrito; falta do ticket 13 o frontmatter, o Apêndice A e as
figuras.

**A declaração de IA não tem nome (`declaracao-ia.md`, sem número).** Ela não é seção numerada — no
`.tex` entra como `\section*` entre a conclusão e as referências —, e dar-lhe `10-` sugeriria uma
décima seção que o esqueleto não tem. O verificador lê o orçamento dela pela linha da tabela cujo
número é `—`, e não pelo número da seção.

**Nenhum número deste trecho foi escrito à mão.** O verificador é quem confere cada um contra o
artefato que o produziu, sem importar do código que o gerou: as métricas da Tabela 2 célula a célula
contra `artifacts/ontology/owl/metricas.md`; as 44 classes, 35 relações e 21 generalizações contra o
relatório do plugin; as linhas de cada QC contra o `qc*-resultado.csv` correspondente; os 31/23/8 da
QC7 recontados do próprio CSV, coluna a coluna; o 12→3→0 contra o relatório do verificador
estrutural; o 105→56 e o 60→0 contra `comparacao-oops.md`. Trocar um número no texto e não no
artefato reprova, e é o que impede o resumo congelado no JEMS3 de divergir do PDF.

**"Descritos e não apenas listados" virou medida, e não leitura.** A regra é a razão entre prosa e
identificador: uma listagem de conceitos fica em três ou quatro palavras por identificador, e o piso
aqui é doze — a §6 mede dezoito. Junto vão duas guardas: todo conceito entre crases tem de existir no
`ontompo-rodada-2.ontouml.json` (conceito inventado reprova) e o vocabulário de estereótipos tem de
estar presente, porque é ele que separa descrever de enumerar. O controle positivo tem uma mutação
que troca a §6 pela lista dos 44 nomes, e ela é acusada.

**A §8 não pode repetir os números da §7**, que era a crítica do parecer sobre a conclusão. O
verificador reprova se algum dos resultados relatados na avaliação reaparecer na discussão; foi essa
regra que forçou a discussão a falar de lições — a forma dos pontos de abertura, o que um relatório
vazio de ferramenta atesta e o que não atesta, a instanciação como diagnóstico e o que o caso diz
sobre modelos de referência publicados sem sua conceituação.

**A regra de redundância do ticket 11 valia com o dobro de superfícies.** Nenhuma sequência de doze
palavras pode reaparecer em duas seções, e agora as nove entram na comparação. Ela pegou três
reincidências reais durante a escrita: a descrição do cenário instanciado repetida da §4 na §7, o
limite das 24 regras do plugin repetido da §5 na §7, e o parágrafo do Desafio 3 quase idêntico ao da
§1 na §9 — as três reescritas. O desenho da avaliação continua exclusivo da §4: o verificador reprova
se "Methontology" ou "Design Science Research" aparecerem no fechamento.

**A paginação apertou, e o orçamento não foi renegociado.** O primeiro rascunho media 6,99 das 5,50
páginas orçadas. Cortar 1,6 página sem perder item de checklist levou várias passadas — nenhuma
mexeu no orçamento do esqueleto, porque a folga que resta (1,5) é do corte previsto para o ticket 13.
As cinco superfícies fecham em 5,39 de 5,50, cada uma dentro do seu orçamento e com margem de alguns
pontos percentuais, como no ticket 11. O número definitivo continua sendo o do porte compilado.

**A declaração de IA tem uma pendência humana, e ela está marcada no arquivo.** O texto descreve o
uso que este repositório registra — ferramenta nomeada, três frentes de emprego e três pontos de
não-emprego —, mas quem assina o artigo é que responde por ela: o ticket 14 confere se corresponde ao
uso efetivo antes da submissão. Nomear a ferramenta é exigência do Código de Conduta e não fere o
anonimato.

**O depósito ainda não tem DOI**, e por isso a §6 e a §7 remetem a ele por nome, sem link. Os dois
comentários de bastidor dizem onde o endereço entra quando o ticket 09 sair da pendência humana.

**Controle positivo.** Trinta e quatro mutações deliberadas foram aplicadas a uma cópia do diretório
do artigo, uma por vez, e cada uma foi acusada: métrica que não bate com o artefato, tabela de
métricas ausente, conceito inventado, contagem de classes errada, §6 reduzida a lista, regra aditiva
omitida, customização sem menção, número de linhas de uma QC trocado, QC ausente da tabela, remissão
ao apêndice removida, divergências não registradas, total do OOPS! errado, total estrutural errado,
controle positivo omitido, cenário sintético não declarado, número da §7 repetido na §8, limitação
dos especialistas removida, pano de fundo dos grupos focais removido, lições sem destaque, trabalho
futuro ausente, LLM apresentado como resultado, Desafio 3 sem nome, proveniência fora da conclusão,
declaração sem nomear ferramenta, sem o Código de Conduta e sem delimitar o não-uso, primeira pessoa,
menção identificadora, citação curva inventada, chave fora do `.bib`, trecho da §5 copiado, método
redescrito na §7, seção além do orçamento e seção ausente.

Duas das mutações mostraram que a regra era fraca demais e a apertaram. "Divergências não
registradas" passava porque a palavra *divergência* aparece de qualquer forma no relato da QC7, que
devolve divergência por desenho: a regra passou a exigir que ela apareça junto da expectativa contra
a qual foi medida. "Controle positivo omitido" passava porque a expressão sobrevivia num parágrafo
enquanto sumia do outro: a regra passou a exigir também a mutação que o materializa.
