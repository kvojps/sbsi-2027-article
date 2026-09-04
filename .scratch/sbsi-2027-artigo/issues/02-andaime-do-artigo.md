# 02: Andaime do artigo

**What to build:** a estrutura vazia porém completa em que o texto vai ser escrito, de modo que
nenhum ticket de escrita precise decidir formato, seção ou bibliografia. Ao fim deste ticket existe
um esqueleto em Markdown com as nove seções nomeadas e o orçamento de páginas anotado em cada uma,
um scaffold LaTeX que **compila em branco** no template SBC, e a bibliografia portada e sã.

É o prefactoring do trabalho: torna fácil cada ticket de escrita que vem depois.

**Blocked by:** None (can start immediately)

**Status:** resolved

- [x] Esqueleto Markdown com as nove seções, cada uma anotada com o label do resumo estruturado que ela carrega e com o orçamento de páginas previsto
- [x] Scaffold LaTeX derivado do template SBC compila sem erro e produz PDF
- [x] O `\usepackage[latin1]{inputenc}` duplicado do template original está removido, mantido apenas o `utf8` — sem isso os acentos quebram
- [x] Bibliografia da dissertação portada, com as entradas que os pareceres apontaram como incompletas agora completas
- [x] Nenhuma referência com chamada quebrada do tipo `[?]` sobrevive
- [x] Entradas de Anais do SBSI, Anais Estendidos do SBSI e iSys presentes na bibliografia, conforme pede a chamada
- [x] O scaffold não contém nome de autor, instituição nem agradecimento

## Comments

Andaime entregue em `artifacts/paper/`: `esqueleto.md` (a superfície de escrita), `artigo.tex` (o scaffold),
`referencias.bib` (a bibliografia) e cópias de `sbc-template.sty` e `sbc.bst`, para que o diretório
suba inteiro para o Overleaf sem depender de `sources/sbc-template/`.

**Compilação.** Não havia toolchain LaTeX na máquina. MiKTeX foi instalado (`winget install
MiKTeX.MiKTeX`, escopo de usuário) com instalação de pacotes sob demanda ligada. O ciclo
`pdflatex → bibtex → pdflatex → pdflatex` fecha sem um único warning de LaTeX e produz um PDF de 7
páginas — scaffold em branco mais a bibliografia inteira. Os metadados do PDF não trazem autor nem
título, o que já ajuda o ticket 14.

**Orçamento de páginas.** As nove seções mais frontmatter, declaração de IA, referências e apêndice
somam 18,0 páginas: 2,0 de folga sob o teto de 20 e 3,0 acima do piso de 15. A folga é deliberada,
porque estourar em qualquer direção é rejeição sem revisão. A seção 5, análise ontológica, leva 3,25
páginas e está marcada como não-candidata a corte.

**Três desvios do template original, todos comentados no cabeçalho do `.tex`:**

- O `\usepackage[latin1]{inputenc}` duplicado saiu, como o ticket pede.
- `\usepackage[T1]{fontenc}` entrou. Sem ele o pdflatex compõe cada acento como glifo sobreposto: o
  PDF sai certo aos olhos, mas a extração de texto devolve `Introduc,a~o`. É sobre o texto extraído
  que a varredura de anonimato do ticket 14 trabalha, então valia corrigir agora.
- A opção de babel passou de `brazil`, deprecada e ruidosa no log, para `brazilian`.

O bloco de título foi reduzido para não deixar linha de autor nem marcador de instituição: `\author`
e `\address` ficam vazios e o `\@maketitle` do sbc-template foi redefinido para omitir as duas
linhas.

**Bibliografia: 73 entradas.** As 50 da dissertação que sobreviveram, mais 23 novas exigidas pelo
novo enquadramento — Representation Theory (Wand & Weber, Weber, Recker et al.), OIPT (Galbraith),
DSR (Hevner, Peffers), LOT e NeOn para o posicionamento da Methontology, gUFO, OOPS!, UFO 2022, o II
GranDSI-Br e as entradas de veículo brasileiro.

As três que os pareceres apontaram como incompletas estão completas: `figueiredo2016papel` virou
`@mastersthesis` com instituição e tipo; `fernandez1997methontology` ganhou evento, local, editora e
páginas; e `guizzardi2005ontological`, que sequer existia na bibliografia da dissertação, foi
acrescentada.

Além dessas, entradas malformadas por artefato de captura foram reconstruídas — autor `Sitewide
ATOM`, autor `Initiative, Social Business`, autor `Guide, A` para o PMBOK, e a entrada de turismo com
o nome do periódico dentro do campo de título.

**Duas entradas da dissertação não foram portadas**, e a razão está registrada no cabeçalho do
`.bib`: `jose2024cisti` tinha literalmente `Sobrenome, Nome` no campo de autor e `Local do evento` no
de endereço, e a publicação não foi localizada para completá-la; `junior2024tcc` é TCC não publicado
do próprio autor e identificaria a autoria numa revisão duplamente anônima. O conteúdo das duas está
coberto por `sbsi_estendido` e `junior2022opupe`.

**Conferência automática** em `tools/verification/verificar_andaime.py`, no mesmo formato de
`verificar_pacote_jems3.py`. Ela reprova quando o `latin1` volta, quando os nomes de seção divergem
entre `esqueleto.md` e `artigo.tex`, quando o orçamento sai do intervalo de 15 a 20, quando uma
entrada perde um campo obrigatório do seu tipo, quando um placeholder sobrevive, quando falta
veículo exigido pela chamada, quando o scaffold ganha autoria, e — quando os logs existem — quando
uma citação fica sem entrada no `.bib`. Cada uma dessas verificações foi exercitada contra uma cópia
deliberadamente quebrada do andaime antes de ser considerada pronta; a primeira versão da checagem
de veículo passava indevidamente porque casava com o próprio cabeçalho comentado do `.bib`, e foi
corrigida para ler só o corpo.

O único aviso tolerado do bibtex é `there's a number but no volume`, em `sakata2013construccao` e
`keever2017decada`. Prisma.com e UVserva numeram fascículos sem volume; inventar um volume para calar
o aviso trocaria uma entrada correta por uma errada.

**Para os tickets seguintes.** O `\nocite{*}` no `.tex` é provisório e existe só para forçar todas as
73 entradas a passarem pelo `sbc.bst` agora, e não na véspera da submissão — o ticket 13 o remove
quando as citações reais existirem. O `resumo` em português está vazio, com TODO para o ticket 13: o
corpo é em português, então o template SBC pede abstract e resumo, e esse texto ainda não foi escrito
em lugar nenhum. O abstract em inglês é cópia literal do texto congelado em
`artifacts/submission/jems3-pacote-registro.md` e não deve divergir dele.
