# 13: Port para LaTeX, figuras e paginação

**What to build:** o PDF do artigo, compilando no template SBC, com as figuras refletindo o modelo
revisado e a extensão dentro do intervalo exigido. Ao fim existe um PDF que poderia ser submetido,
faltando apenas a conferência de conformidade.

Cuidado com as figuras: as imagens disponíveis são do modelo **antigo**. Reaproveitá-las como estão
publicaria diagramas que contradizem a seção de análise — o artigo mostraria os defeitos ao lado da
afirmação de que foram corrigidos.

A extensão é regra de desk reject nos dois sentidos: menos de 15 páginas rejeita tanto quanto mais
de 20. Se apertar, o corte previsto é mover os diagramas por camada para o depósito e manter no
artigo o diagrama integrado.

**Blocked by:** 12 (ontologia revisada, avaliação e conclusão)

**Status:** resolved

- [x] Texto portado do Markdown para o template SBC, compilando sem erro
- [x] Acentuação correta no PDF gerado
- [x] Figuras regeradas a partir do modelo revisado; nenhuma figura do modelo antigo sobrevive fora de um par antes/depois deliberado
- [x] Figuras legíveis no tamanho impresso
- [x] Bibliografia compilando, sem chamadas quebradas e sem entradas incompletas
- [x] Título, resumo estruturado e palavras-chave em inglês no PDF, com os sete labels nomeados
- [x] Estrutura de seções refletindo os sete labels do resumo estruturado
- [x] PDF com no mínimo 15 e no máximo 20 páginas, contando referências, apêndices, figuras e tabelas
- [x] Apêndice com as consultas SPARQL e resultados completos, ou remissão explícita ao depósito

## Comments

**O PDF fecha em 20 páginas**, sem um erro de LaTeX e sem aviso de citação indefinida. Conferência:
`python tools/verification/verificar_port_latex.py` (146 verificações), com controle positivo em
`python tools/verification/controle-port-latex.py` (21 mutações, todas acusadas).

**O texto não foi transcrito, foi portado por gerador.** Copiar 9.300 palavras para o `.tex` criaria
uma segunda cópia do texto, e duas cópias divergem: uma correção feita no Markdown depois do port
sairia do PDF sem que nada acusasse, e os verificadores dos tickets 10 a 12 — que leem o Markdown —
continuariam aprovando um PDF que não corresponde mais ao que eles conferiram.
`tools/generation/gerar_secoes_latex.py` gera `secoes-tex/NN-*.tex` de `secoes/NN-*.md`, e o
`artigo.tex` só dá `\input`. O verificador fecha o laço pelo outro lado, sem importar do gerador:
extrai o texto do PDF compilado e procura nele, um a um, os 123 trechos de prosa dos dez arquivos
Markdown. Editar o `.tex` à mão reprova; esquecer de regerar, também.

**O orçamento de páginas do esqueleto era inexequível, e o ticket teve de renegociá-lo.** Ele somava
18,50 páginas e nunca reservou uma linha para figura alguma; dava 1,50 página a uma bibliografia que
mede 2,77 com as 37 entradas que o texto cita; e orçava 1,00 para um frontmatter que precisa carregar
o abstract estruturado em inglês *e* o resumo em português, e mede 1,18. O texto escrito até o ticket
12 compilava em **22 páginas** — rejeição sem revisão. O corte previsto pela spec, mover os diagramas
por camada para o depósito, valia 0,5 página e não bastava.

Fechar o intervalo custou **1.400 palavras**, cortadas em §1 a §9 com os verificadores dos tickets
10, 11 e 12 rodando a cada passada — nenhum item de checklist se perdeu, e as 106, 153 e 227
verificações deles continuam passando. O resumo em português foi condensado a 176 palavras, por ser
tradução e não conteúdo novo: é a única página e meia do artigo que não custa argumento. E os sete
labels do abstract passaram a correr no mesmo parágrafo em vez de um por parágrafo — mesmo texto,
0,15 página de `\parskip` a menos.

**A medida por seção oscilava quase uma página, e a culpa era dos flutuantes.** Tabela e figura
atravessavam a fronteira entre §6 e §7 conforme o texto mudava, de modo que cortar palavras não
derrubava o total: só mudava de lugar. Com `[H]` — o pacote `float` — cada uma fica onde é
declarada, a medida por seção virou estável e o corte passou a converter em página. O mesmo
diagnóstico explica o Apêndice A: o `BVerbatim` é caixa indivisível, e quando a consulta não cabia
no que restava da página ia inteira para a seguinte, deixando meia página em branco; trocado por
`Verbatim`, que quebra, o artigo caiu de 21 para 20 páginas.

**A tabela de orçamento agora traz números medidos, não estimados**, cada um duas centésimas acima
do que o bloco mede hoje, somando 19,97 sob o teto de 20. A folga é de 0,03 página, e isso é a
informação: qualquer parágrafo acrescentado daqui em diante reprova o verificador da seção antes de
chegar ao PDF. **Acrescentar texto exige cortar na mesma passada.**

**Os três verificadores de seção mediam com o porte errado.** O `_para_latex` dos tickets 10 a 12 era
um porte grosseiro, escrito quando o `.tex` real não existia, e erra por não flutuar tabela nem
quebrar célula: media §4 em 1,95 página onde o porte real mede 1,35, e §8 em 1,84 onde o real mede
1,02. Eles ganharam `_medir_no_porte`, que compila o `artigo.tex` com marcas e lê a distância entre
elas; o porte grosseiro sobrevive como reserva para quem rodar os três sem o ticket 13 pronto. Foi
o que fez os três voltarem a passar sem afrouxar nenhuma regra.

**As figuras são desenhadas, não reaproveitadas.** `tools/generation/gerar_figuras.py` lê
`ontompo-rodada-2.ontouml.json` e emite TikZ: o diagrama integrado, com as 44 classes, as 21
generalizações e as 35 relações, e os três por camada. Do modelo vêm os nomes, os estereótipos e as
ligações; da ferramenta vem só onde cada caixa fica — o `.ontouml.json` não carrega posição, o campo
`diagrams` é nulo. A geração aborta se as duas listas divergirem: classe posicionada que não existe
no modelo, ou classe do modelo sem posição.

O verificador confere o TikZ gravado contra o modelo sem importar do gerador — classe inventada,
ligação que o modelo não tem e classe do modelo ausente do integrado são as três acusações — e mede
a legibilidade de dois jeitos: nenhum corpo declarado abaixo de 5pt, e a figura **compilada sozinha**
no template não pode passar da largura da mancha. Foi essa segunda medida que pegou um erro real:
somando coordenadas a figura media 14,84cm e parecia caber, mas composta media 15,19 contra 15,00 —
o rótulo da legenda sangrava para fora. As colunas encolheram de 2,50 para 2,45cm.

**Nenhuma imagem do modelo antigo sobrevive**, e há duas guardas para isso: o artigo não tem
`\includegraphics` algum, e nenhum arquivo do diretório do artigo é cópia byte a byte de uma imagem
de `sources/dissertation/` — comparação por SHA-256, porque renomear o arquivo não muda o conteúdo.
Os diagramas por camada foram para `artifacts/deposit/figuras/`, como a spec previu, e o
`gerar_deposito.py` os copia de lá.

**O abstract do `.tex` divergia do registro congelado no JEMS3, e o port corrigiu.** O texto do
scaffold era o do ticket 02; o do registro foi reescrito no commit `1e5fb70`, quando a análise passou
a atribuir as deficiências à formalização publicada e não ao MPO, e o `.tex` ficou para trás. Depois
de 14/09/2026 o registro não pode mais ser alterado, então quem cede é o PDF. O verificador compara
os sete blocos um a um, com espaços e hifenização normalizados.

**O Apêndice A faz as duas coisas que a checklist admite.** As sete consultas somam 273 linhas e não
cabem na página orçada: vai na íntegra a QC7 — a que sustenta a contribuição — e a remissão ao
depósito nomeia arquivo por arquivo (`qcN.rq`, `qcN-resultado.csv`, `divergencias.md`) e o script que
reexecuta e confere cada uma. Nenhum número foi digitado: as contagens de linha saem dos `.csv` e o
corpo da consulta sai do `.rq`, e o verificador reprova se o apêndice transcrever em vez de
reproduzir.

**Controle positivo: 21 mutações, uma por vez, sobre uma cópia do diretório do artigo** —
`\nocite{*}` de volta, `latin1` de volta, `fontenc` removido, `.tex` de seção editado à mão, classe
inventada na figura, classe do modelo ausente, ligação inexistente, corpo abaixo do piso, figura mais
larga que a mancha, imagem do modelo antigo incluída, imagem da dissertação copiada, abstract
divergente do JEMS3, label do resumo removido, seção renomeada, remissão sem o script, contagem de
linhas de uma QC trocada, consulta transcrita, citação sem entrada no `.bib`, artigo acima de 20
páginas, declaração de IA removida e veículo da chamada sem citação. Todas acusadas.

Uma delas mostrou uma regra fraca. A mutação do `latin1` escapou na primeira execução porque o
verificador só olhava o efeito — e o `pdflatex` moderno recusa a segunda opção de `inputenc` com um
erro, mas ainda compõe os acentos certos. Ele passou a **nomear** a regressão no preâmbulo, em vez
de deixá-la aparecer como "erro de LaTeX" genérico.

**O `/code-review` achou oito coisas, todas corrigidas.** A que importava era de
reprodutibilidade: `gerar_deposito.py` pulava as figuras em silêncio quando `artifacts/paper/figuras/`
ainda não existia — que é o estado de um checkout limpo seguindo a ordem que o README documentava,
com o depósito (09) antes das figuras (13). O depósito publicado sairia sem os diagramas por camada,
justamente o que o corte de paginação mandou para lá, e `verificar_deposito.py` aprovava assim mesmo.
Agora o gerador aborta com a instrução do que rodar — e aborta **antes** do `rmtree`, para não deixar
o depósito destruído —, o verificador exige `figuras/` e os três arquivos, e o README põe
`gerar_figuras.py` antes de `gerar_deposito.py`.

As outras sete: `pdfinfo` e `bibtex` usados sem entrar na guarda de disponibilidade (o verificador
morria com *traceback* em vez da mensagem); `_medir_no_porte` lendo `medida.log` sem conferir se
existe, contra o que o próprio docstring promete; as três faixas de camada da figura **sobrepostas em
0,14 cm**, o que fazia as três lerem como uma tira contínua — era o `GAP_ENTRE_CAMADAS` menor que a
soma das bordas, e a figura existe para separá-las; o contador de tabelas avançando em tabela sem
legenda, o que faria a próxima legendada abortar com o número errado; o verificador contando linhas
de resultado por linha física enquanto o gerador conta por registro de CSV; os comentários de
orçamento do `artigo.tex` ainda com os números pré-corte, que é o que um contribuidor lê antes de
acrescentar parágrafo; e a anotação de retorno de `porta`.

Corrigir o sexto introduziu um erro que a suíte pegou na hora: o `import csv` novo colidia com uma
variável local chamada `csv` na mesma função.

**Duas pendências, ambas do ticket 14.** O depósito ainda não tem DOI, então §6, §7 e o Apêndice A
remetem a ele por nome e não por link — o endereço entra quando o ticket 09 sair da pendência humana.
E a declaração de uso de IA continua precisando da conferência de quem assina.
