# 11: Seções de introdução, referencial, trabalhos relacionados e método

**What to build:** a primeira metade do artigo, que estabelece o problema, dá ao leitor tudo o que
ele precisa saber para acompanhar a análise e justifica o desenho de pesquisa. Ao fim, um
pesquisador de SI que nunca ouviu falar do MPO consegue ler o artigo até a seção de análise sem
consultar nenhuma referência.

Cinco críticas do ONTOBRAS são endereçadas aqui: o artigo não ser autocontido; a terminologia de
nicho não posicionada frente a gerenciamento e monitoramento de projetos; a redundância entre seções
que repetiam MPO e Methontology; a falta de posicionamento frente a metodologias mais recentes; e a
ausência de ancoragem teórica.

O texto pode partir do material da dissertação, que já está em português — mas com a redundância
cortada e sem qualquer resquício da defesa de ontologia leve.

**Blocked by:** 02 (andaime do artigo)

**Status:** resolved

- [x] Introdução situa o trabalho no tripé Pessoas, Processos e Procedimentos, e Tecnologias
- [x] Domínio de aplicação e problema organizacional apontados explicitamente
- [x] Contribuição conectada ao II GranDSI-Br, nomeando o Desafio 3, "Eco(Sistemas²) de Informação", e secundariamente o Desafio 2
- [x] MPO descrito de forma autocontida: as três dimensões, suas subdimensões e os conceitos que a análise vai discutir
- [x] Observatórios de projetos posicionados frente a gerenciamento e monitoramento de projetos e a PMOs, respondendo à crítica de terminologia de nicho
- [x] Representation Theory apresentada como teoria de SI que sustenta a análise, com sua tipologia de deficiências
- [x] Organizational Information Processing Theory citada na motivação
- [x] Trabalhos relacionados situando o artigo frente a ontologias em contextos de observatório
- [x] Método: Design Science Research como envelope e Methontology como método de construção, posicionada frente a LOT e NeOn
- [x] Continuidade com o ciclo DSR sob o qual o próprio MPO foi construído e evoluído explicitada
- [x] Nenhum conteúdo repetido entre seções
- [x] Referências a Anais do SBSI, Anais Estendidos e iSys presentes
- [x] Nenhuma menção identificadora ao autor; trabalhos do próprio autor citados em terceira pessoa
- [x] Cabe no orçamento de páginas previsto

## Comments

Texto em `artifacts/paper/secoes/01-introducao.md`, `02-referencial.md`,
`03-trabalhos-relacionados.md` e `04-metodo.md` — um arquivo por seção, como a seção 5 do ticket 10,
e o `<!-- conteúdo: ticket 11 -->` de cada uma virou ponteiro para o arquivo. Conferência:
`python tools/verification/verificar_seccoes_introducao_metodo.py`.

**As cinco críticas do ONTOBRAS têm endereço fixo no texto.** Terminologia de nicho: §2.1 demarca o
observatório frente a gerenciamento de projetos, a monitoramento e controle e a PMO, e diz o que
muda em cada caso — audiência, autoridade e escopo —, em vez de trocar o nome do domínio.
Autocontenção: §2.2 descreve as três dimensões, as cinco subdimensões e os elementos que a §5
discute, de modo que o leitor chega à análise sem abrir a fonte. Ancoragem teórica: §2.3 traz a
Representation Theory com as quatro deficiências e o escopo do que ela classifica — o *mapeamento*
entre gramática e ontologia —, e a §1 ancora a motivação na OIPT. Metodologias recentes: §4 posiciona
a Methontology frente à NeOn e à LOT dizendo por que a força de cada uma não é exercida aqui, e não
apenas que a Methontology é consagrada. Redundância: a Methontology só é descrita na §4, e o
verificador reprova se a palavra aparecer nas seções 1 a 3.

**A redundância virou regra automática, e não revisão de leitura.** Nenhuma sequência de doze
palavras pode reaparecer em duas seções — a §5 entra na comparação —, e nenhuma citação verbatim da
fonte pode ser reusada entre elas. A primeira versão comparava frase com frase e deixava passar o
mesmo trecho com a pontuação final trocada; o controle positivo pegou isso, e a comparação passou a
ser por sequência de palavras, sem pontuação nem caixa.

**A paginação é estimada aqui, e medida onde houver pdflatex.** O verificador compila como o do
ticket 10 quando `pdflatex` existe; sem ele, cai numa estimativa por linhas — 48 linhas de 14 pt por
página, 93 caracteres por linha, na geometria que o `sbc-template.sty` fixa — **calibrada pela medida
compilada da seção 5**, que o esqueleto registra. A régua é um texto real deste artigo, e não um
palpite: as quatro seções somam 5,60 das 5,75 páginas orçadas, cada uma dentro do seu orçamento.
A margem inicial era de menos de 1% na seção 2, fina demais para uma estimativa: o texto foi
encurtado até cada seção ter folga de alguns pontos percentuais, porque o número definitivo é do
porte compilado do ticket 13.

**A regra de atribuição da seção 5 vale aqui também.** Um rascunho da seção 3 escreveu "o conjunto
de deficiências do modelo de referência" — a mesma alegação falsificável que o `CONTEXT.md` manda
evitar, uma casa adiante: as deficiências são da formalização publicada, e o modelo de referência é
o que as permitiu. O verificador passou a reprovar essa atribuição nas quatro seções, como o do
ticket 10 já fazia na seção 5.

**O anonimato do `.bib` não é decisão deste ticket.** As quatro seções não trazem menção
identificadora e citam trabalhos do próprio autor em terceira pessoa, que é o que a checklist pede;
as entradas de `referencias.bib` desses trabalhos continuam nomeando seus autores, como em qualquer
autocitação sob revisão duplamente anônima. A decisão é do ticket 02, que registra no cabeçalho do
`.bib` por que `sbsi_estendido` e `junior2022opupe` ficaram e `junior2024tcc` saiu, e a varredura
final é do ticket 14.

**Controle positivo.** Treze mutações deliberadas foram aplicadas a uma cópia do diretório do artigo,
uma por vez, e cada uma foi acusada: Desafio 3 sem nome, NeOn fora do método, UFO-B fora do
referencial, Methontology descrita no referencial, chave fora do `.bib`, primeira pessoa, citação
curva inventada, trecho da §5 copiado com pontuação trocada, citação da fonte reusada entre seções,
seção inflada além do orçamento, seção ausente, OIPT removida da motivação, gerenciamento de
projetos sem posicionamento e deficiência atribuída ao modelo de referência.
