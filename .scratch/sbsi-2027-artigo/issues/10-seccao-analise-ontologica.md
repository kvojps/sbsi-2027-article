# 10: Seção de análise ontológica do MPO

**What to build:** a seção que carrega a contribuição do artigo e que não existia no trabalho
rejeitado. Apresenta as nove deficiências representacionais encontradas na **formalização publicada**
do MPO, cada uma classificada pelo vocabulário da Representation Theory, exibida como antes/depois
com justificativa ontológica e **traçada até o ponto do MPO que a permitiu**.

É esta seção que separa o artigo aceito do artigo rejeitado. O parecer decisivo do ONTOBRAS dizia que
formalizar o MPO exatamente como proposto na literatura, sem análise crítica nem refinamento, não
constitui contribuição suficiente. A resposta não é argumentar contra: é produzir a análise.

**Onde as deficiências estão, e onde não estão.** As nove são falhas da formalização, não do MPO em
linguagem natural. O MPO é prosa: três dimensões, subdimensões e elementos. Não tem `CrudOperation`,
não diz que software é composto de hardware, não hierarquiza `DataManager` sob observatório — esses
são estereótipos e relações escolhidos na etapa de formalização, e a dissertação os enuncia como
decisão de modelagem. Escrever "deficiência do MPO" é entregar ao revisor uma alegação falsificável
em um parágrafo, do mesmo tipo que o `«CompOf»` do spec que virou `«MemberOf»` no diagrama.

**O que sustenta a contribuição, então.** Que o MPO **subdetermina sua própria formalização**. Uma
formalização sistemática, seguindo Methontology, produziu nove desvios, e cada um cai num ponto em
que o MPO não fixa a interpretação — A5 é o caso mais nítido, porque o MPO descreve Processos como
perspectiva *dinâmica* e a formalização os tornou relatores endurantes, contradizendo a fonte. É
isso que converte "duas iniciativas podem se declarar aderentes com interpretações incompatíveis" de
afirmação em demonstração: a demonstração é uma tentativa real de formalizar.

O tom importa. O objeto de análise é trabalho publicado, citado em terceira pessoa, e a correção é
construtiva — o resultado deve ser evolução do MPO, não desqualificação dele nem autoflagelo sobre a
formalização anterior.

**Blocked by:** 02 (andaime do artigo), 05 (adoção de UFO-B e UFO-C)

**Status:** resolved

- [x] As nove deficiências A1–A9 apresentadas, cada uma com o que foi observado, por que é uma deficiência e como foi corrigida
- [x] Cada deficiência localizada na formalização publicada, e em nenhum lugar do texto atribuída ao MPO em linguagem natural
- [x] Cada deficiência traçada até o ponto do MPO que a permitiu — deficiência sem traço é conserto de erro próprio, não achado
- [x] A subdeterminação do MPO pela sua formalização declarada como o resultado, e não a lista de defeitos
- [x] Cada uma classificada em *construct overload*, *redundancy*, *excess* ou *deficit*, ou justificada quando não couber na tipologia
- [x] Antes/depois visível para as deficiências cuja correção muda o diagrama
- [x] Cada correção fundamentada em argumento ontológico da UFO, não em preferência de modelagem
- [x] Evidência das ferramentas citada onde ela existe, com a diferença entre os relatórios antes e depois
- [x] Explicitado o que decorre disso para o domínio: por que duas iniciativas podiam se declarar aderentes ao MPO com interpretações incompatíveis
- [x] Deficiências detectadas pelas ferramentas além de A1–A9 incorporadas ou descartadas com justificativa
- [x] Limite n=1 declarado: demonstra-se que o MPO permite os desvios, não que outro formalizador os cometeria
- [x] Nenhuma menção identificadora ao autor e nenhum resquício da defesa de ontologia leve
- [x] Cabe no orçamento de páginas previsto para a seção — com o orçamento revisto de 3,25 para 3,75, ver abaixo

## Comments

Texto em `artifacts/paper/secoes/05-analise-ontologica.md`. O esqueleto do ticket 02 é o plano; o
texto de cada seção passa a morar em `secoes/`, um arquivo por seção, e é de lá que o ticket 13 porta
para o `.tex`. O `<!-- conteúdo: ticket 10 -->` da seção 5 virou ponteiro para o arquivo.

**Os traços não existiam, e são o trabalho novo deste ticket.** `evidencias-A1-A9.md` já localizava
cada deficiência no baseline, e as duas rodadas já tinham antes/depois com justificativa da UFO. O
que faltava era o traço: o ponto do MPO em que a interpretação fica aberta e que permitiu o desvio.
Cada um foi buscado na fonte e ancorado numa citação verbatim. Cinco tipos de abertura dão a
estrutura da seção, e é isso que a torna um argumento e não uma lista:

| Abertura no MPO | Deficiências |
|---|---|
| agrupa elementos em subdimensões sem dizer o que agrupar é | A9, A2 |
| enuncia relações em frases que ligam três ou quatro elementos | A8, A3 |
| chama Processos de dinâmicos e nomeia o mesmo fenômeno como componente e como verbo | A5, A1 |
| enumera indivíduo, grupo e organização como o mesmo ator | A6, A7 |
| não fixa léxico na língua da formalização | A4 |

A5 é o traço mais forte, como o ticket previa: o MPO chama Processos de “perspectiva dinâmica” e a
formalização os tornou relatores endurantes — o oposto do que a fonte declara, sem contrariar
nenhuma frase dela.

**A distinção MPO/conceituação foi necessária e está no texto.** O Apêndice A da dissertação é a
*conceituação da formalização*, não o MPO; citá-lo como se fosse o MPO seria o mesmo erro que o
ticket manda evitar, uma casa adiante. A abertura da seção separa os dois, e os traços dizem qual dos
dois estão citando. Que a abertura sobreviva à conceituação — um glossário cuja coluna de relações é
prosa — reforça o argumento em vez de enfraquecê-lo.

**O enunciado de A3 no esqueleto foi corrigido.** Ele repetia a descrição do *spec* — «CompOf»
ligando `ObservatoryUser` a `ObservatoryGroup` —, que `evidencias-A1-A9.md` já registrara como
falsificável: nos diagramas publicados o estereótipo é «MemberOf» e o defeito é a direção. A tabela
do esqueleto agora diz o que o modelo diz, para que nenhum ticket seguinte a copie errada.

**Orçamento: 3,25 → 3,75, com a diferença saindo da folga.** O texto mede **3,51 páginas** num porte
provisório para o template SBC, compilado, não estimado. Chegar a 3,25 exigiria cortar a evidência
das ferramentas ou os achados fora da lista, ambos itens desta checklist. O esqueleto registra a
mudança e a razão; a folga do artigo cai de 2,0 para 1,5 e o total vai a 18,5, dentro do intervalo da
chamada — `verificar_andaime.py` continua passando. O número definitivo é do ticket 13.

**A referência da formalização analisada está omitida**, com a omissão declarada em uma frase no
texto: citá-la nomeia a autoria numa revisão duplamente anônima, e a bibliografia do ticket 02 já
tinha excluído a entrada pela mesma razão. Fica endereçado ao ticket 14, que decide a forma anônima
da citação.

**Verificação: `tools/verification/verificar_analise_ontologica.py`, 105 checagens.** Ela lê o texto
como terceiro e o confronta com a fonte e com os artefatos, em vez de reler o que o texto diz de si:

- **toda aspa curva é citação verbatim**, e cada uma é procurada, com espaços normalizados e sem
  distinguir caixa, em `sources/dissertation/`. É o que torna o traço falsificável — citação
  inventada reprova. As de LaTeX (`\textbf{...}`) são normalizadas antes da comparação;
- a afirmação de que o acrônimo CRUD não ocorre no MPO nem na conceituação é conferida contra
  `fundamentacao.tex` e `apendices.tex` — e só contra eles, porque `resultados.tex` descreve a
  formalização, onde `CrudManager` de fato aparece;
- todo identificador entre crases existe no baseline ou na rodada 2: o texto não pode citar construto
  que nenhum dos dois modelos tem;
- os números são recontados dos artefatos — a divergência da QC7 (oito contra vinte e três) sai do
  `.csv` linha a linha, as nove regras saem do relatório, o zero do plugin sai do JSON;
- os dez achados fora de A1–A9 são contados nos artefatos da ontologia, e as disposições declaradas
  na seção têm de somar exatamente esse total: nenhum achado fica sem destino;
- a paginação é **medida**: o texto é portado para o template SBC, compilado com pdflatex e contado
  em páginas inteiras mais a fração ocupada na última, contra o orçamento que o esqueleto declara.
  Sem pdflatex a verificação avisa e segue;
- e as regras de tom: nenhuma atribuição da deficiência ao MPO em linguagem natural, nenhuma menção
  identificadora, nenhuma primeira pessoa, nenhum resquício de ontologia leve.

**Controle positivo.** Quinze mutações deliberadas foram aplicadas a uma cópia do texto, uma por vez,
e cada uma foi acusada com a mensagem esperada: citação inventada, linha da tabela removida, traço
esvaziado, identificador inexistente, deficiência atribuída ao MPO, achado extra sem destino, número
da QC7 trocado, limite n=1 removido, primeira pessoa, resquício de ontologia leve, antes/depois
removido, argumento sem referência, texto inflado além do orçamento, subseção sem citação e chave
bibliográfica fora do `.bib`. A primeira versão da checagem de citação por subseção passava
indevidamente porque a subseção tinha duas citações e a mutação só removia uma — a mutação foi
corrigida para tirar todas.
