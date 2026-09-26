# 5. Análise Ontológica do MPO

<!--
Superfície de escrita da seção 5, no orçamento que `../esqueleto.md` declara para ela.
O ticket 13 porta este arquivo para `../artigo.tex`.

Convenções que `tools/verification/verificar_analise_ontologica.py` confere:

  - aspas curvas “…” marcam citação **verbatim** da fonte, e só isso. Cada ocorrência é
    procurada, com espaços normalizados, em `sources/dissertation/`;
  - «…» marcam estereótipo de OntoUML, nunca citação;
  - a Tabela 1 traz os nove achados, cada um com fonte textual, decisão de formalização,
    problema ontológico, correção e classificação;
  - nada no texto atribui as deficiências ao MPO em linguagem natural.
-->

As nove deficiências desta seção são falhas de uma formalização publicada do MPO, trabalho de
terceiros reconstruído como linha de base no artefato suplementar anônimo, e não do MPO. O MPO é
prosa: três dimensões, suas subdimensões e os elementos de cada uma [vieira2021model,
farias2025conceptual]. Ele não contém `CrudOperation`, não declara software composto de hardware e não
hierarquiza `DataManager` sob observatório: estereótipos e relações são escolhas da formalização.
Onde é preciso distinguir, o texto separa o MPO da conceituação da formalização, um glossário de 53
termos cuja coluna de relações é redigida em prosa. A linha de base é a reconstrução desse
modelo publicado em OntoUML.

Cada uma das nove deficiências decorre de um ponto em que o MPO não fixa a interpretação. A Tabela 1
explicita a cadeia fonte--decisão--problema--correção e mostra que **o MPO subdetermina sua própria
formalização**. Uma tentativa sistemática de formalizá-lo, sob Methontology
[fernandez1997methontology], produziu nove desvios sem contrariar o modelo em ponto algum; sem esse
traço, a deficiência seria apenas a correção de um erro próprio. Seis são classificadas pela tipologia de
Representation Theory [wand1993ontological, recker2011ontological]; A3, A8 e A9 ficam fora dela
porque a tipologia classifica o *mapeamento* entre gramática e ontologia, e as três violam restrição
interna de uma gramática já ontologicamente fundamentada.

**Tabela 1. Cadeia de evidência dos nove achados na formalização publicada do MPO.**

| # | Fonte textual | Decisão da formalização | Problema ontológico | Correção | Classificação |
|---|---|---|---|---|---|
| A1 | Responsabilizar atores por suas ações | `CrudOperation` único para criar, ler, atualizar e excluir | Ações incompatíveis colapsadas | Quatro eventos disjuntos | *overload* |
| A2 | Infraestrutura “suporta” software e serviços | `Hardware` como parte de `Software` | Verbo não fixa parthood | `SoftwareExecution` relacional | *excess* |
| A3 | Agentes incluem indivíduo, grupo e sistema | Coletivo na ponta da parte de «memberOf» | Todo e membro invertidos | Inverter as três relações | fora: restrição da UFO |
| A4 | Componente que coordena relacionamentos | Classe `Relator` | Homônimo de metaconceito UFO | Renomear para `Reporter` | *redundancy* |
| A5 | Processos dão perspectiva dinâmica | ETL como «relator» | Processo sem tempo ou participantes | Eventos e participações | *deficit* (UFO-B) |
| A6 | Parte interessada: indivíduo, grupo ou organização | `Agent` como «kind» único | Identidades distintas sob um sortal | Categoria e `StakeHolder` «roleMixin» | *deficit* (UFO-C) |
| A7 | Sistema é ator não humano participante | `System` sob `Agent` | Sistema não implica intencionalidade | `ComputationalSystem` como sortal | *deficit* (UFO-C) |
| A8 | Gerenciamento viabiliza coleta, processamento e armazenamento | `Management` e `Operation` n-ários | Fato relacional e aridade indeterminados | Relatores binários nomeados | fora: aridade |
| A9 | Componentes agrupam gerenciamento e visão | Observatório como subtipo de software; papéis abaixo | Componentes viram observatórios inteiros | Papéis de software em composição | fora: identidade |

## 5.1. O agrupamento lido como taxonomia (A9, A2)

Componentes, subdimensão irmã de Conteúdos e Características, “compreendem os elementos associados à
coleta, ao tratamento, ao processamento e à disponibilização dos dados”: o MPO agrupa, e não diz o
que agrupar significa ontologicamente. A formalização leu o agrupamento como especialização, e disso
resulta que cada visão e cada disseminador **é um observatório inteiro**, embora a QC1 pressuponha
muitas visões por observatório:

```
antes                                     depois
Software «kind»                           Software «kind»
  +- ProjectObservatory «subkind»           +- ProjectObservatory «subkind»
       +- DataManager «role»                +- DataManager «role» -+ «componentOf»
       +- View «role»                       +- View «role» -------+--> ProjectObservatory
```

A correção substitui especialização por composição: ambos passam a ser papéis de `Software`, que lhes
fornece princípio de identidade, e partes do observatório por «componentOf» [guizzardi2005ontological]. O
mesmo silêncio produziu A2: a conceituação liga os elementos de infraestrutura por “Suporta
Serviços, Gerenciamento de dados e Software”, verbo que admite leitura como parthood, dependência ou
execução, e a formalização escolheu «componentOf». Mas trocar o hardware sob uma aplicação não a
torna outra aplicação: o vínculo é de manifestação, reificado no relator `SoftwareExecution`.

## 5.2. A relação enunciada em prosa lida como fato único (A8, A3)

O MPO liga três ou quatro elementos por frase. Por exemplo, o gerenciamento de dados “Viabiliza a
Coleta, Processamento e Armazenamento dos dados”, sem nomeá-los como fatos de aridade fixa. A
formalização reificou cada frase num relator: `Management` medeia projeto, gerenciador e visão;
`Operation`, software, serviço, hardware e rede. A aridade deveria decorrer do fato reificado
[guizzardi2005ontological], e nenhum sobrevive ao teste: três das quatro mediações de `Operation`
admitem zero na ponta mediada, o que contradiz a dependência existencial da mediação. A correção os
decompõe em relatores binários nomeados, e revela que a quarta ponta de `Operation` era redundante
com `Connection`.

A3 decorre da mesma abertura na dimensão Agentes, cujos atores “incluem os agentes que participam do
observatório, sejam eles indivíduos, grupos organizacionais ou sistemas computacionais”, sem dizer o
que liga o indivíduo ao grupo. As três «memberOf» puseram o losango do lado do papel, e a OWL gerada afirma que
o grupo é membro do usuário, tornando a mesma classe coleção e complexo funcional. «memberOf» exige o
coletivo no todo: a correção inverte as três e eleva de 0 para 1 o mínimo do lado do membro.

## 5.3. A perspectiva dinâmica lida como vínculo endurante (A5, A1)

O MPO descreve Processos como o que fornece “uma perspectiva dinâmica de seu funcionamento”, e é aqui
que a subdeterminação se torna mais nítida: a formalização produziu o oposto do que a fonte declara sem
contrariar nenhuma frase dela. O modelo nomeia o mesmo fenômeno duas vezes, como componente (Coleta,
Processamento, Armazenamento) e como verbo (Coletar, Tratar, Armazenar), cada verbo realizado “por
meio do componente de Coleta”, e não diz qual dos dois vira elemento formal. A formalização levou os
verbos ao diagrama estrutural como relatores; mas relatores são endurantes, sem partes temporais,
enquanto extrair, transformar e carregar têm início, fim e participantes [guizzardi2008grounding], e
sem evento não há *quando*: a QC3 era irrespondível por construção. A correção torna os três eventos,
converte as seis mediações em participações e as reúne por parthood no evento complexo `EtlProcess`,
que dá à QC6 uma cadeia de proveniência a percorrer.

A1 é o mesmo desvio na escala da ação. O MPO exige “Responsabilizar os atores do observatório de
projetos por suas ações no contexto do observatório”, mas não individua a ação sobre o dado. Além disso, o
acrônimo CRUD não ocorre em ponto algum do modelo nem da conceituação. Precisando de ações
auditáveis, a formalização importou o vocabulário da prática de implementação e o colapsou num
relator único; mas criar, atualizar e excluir têm pós-condições incompatíveis, e ler não tem
pós-condição alguma: um construto gramatical para quatro construtos ontológicos é sobrecarga no
sentido estrito [wand1993ontological]. A correção os separa em quatro tipos disjuntos e exaustivos
e, com UFO-B, os trata como eventos.

## 5.4. A enumeração lida como tipo único (A6, A7), e o termo sem léxico (A4)

O MPO define a parte interessada como “um indivíduo, grupo ou organização que pode afetar ou ser
afetada por uma decisão, atividade ou resultado de um projeto”: três coisas com princípios de
identidade distintos, pois uma organização sobrevive à troca de todos os seus membros e uma pessoa
não é agregado de ninguém. A formalização as reuniu sob um `Agent` «kind», que fornece exatamente
**um** princípio de identidade. A correção usa a camada de não-sortais: `Agent` passa a «category»
particionada em físico e social, `Person` e `Organization` entram como os sortais que faltavam, e
`StakeHolder` passa a «roleMixin» [guizzardi2008grounding]. Com isso, *tipo de ator*, pressuposto
da QC5, vira pergunta com resposta.

Em A7 a própria fonte declara a omissão: o kind subjacente a `System` “não foi explicitado no
diagrama, constituindo uma simplificação do modelo”, mas a simplificação não era neutra. O MPO
define ator por participação: sistemas são “os atores não-humanos, aqui chamados de sistemas”,
não por intencionalidade; pendurar `System` sob `Agent` afirma que todo sistema externo é agente,
quando em UFO-C agente é o que porta momentos intencionais. O papel é legítimo; faltava o sortal que
o fundamenta, hoje `ComputationalSystem`.

Uma última abertura é lexical, e produziu A4. O MPO nomeia o componente encarregado de “Coordenar
os relacionamentos entre os Usuários e a interação desses com os projetos e o Observatório”, e não
fixa identificador para ele na língua da formalização. A classe foi batizada `Relator`, que em
português designa quem relata e, em OntoUML, uma categoria de fundamentação da UFO. Desambiguar passou a
exigir o contexto tipográfico do diagrama. A correção a renomeia para `Reporter`.

## 5.5. As ferramentas, e os achados além das nove

Nenhuma das nove resultou de ferramenta; essa distinção delimita o que cada instrumento afirma. O verificador
de conformidade à UFO devolve zero problema sobre a linha de base. Suas regras tratam de estereótipo,
identidade, natureza e generalização, e nenhuma alcança restrição meronímica, aridade de relator ou
distinção endurante/perdurante, e esse zero foi submetido a controle positivo. Quem mede a
distância entre os modelos são nove regras estruturais escritas para esta análise, reportadas com os
números antes e depois, junto à queda dos *pitfalls* de OWL [poveda2014oops], na avaliação (§7). A1,
A2 e A9 não viraram regra: são defeitos de significado, e codificá-los seria escrever a resposta no
gabarito.

Dez achados apareceram fora da lista, todos incorporados ou descartados com razão registrada.
Quatro foram absorvidos pelas correções: mediação com mínimo zero na ponta mediada (por A8),
parthood sem todo nem parte declarados (por A3), ausência de disjunção (pelas partições) e a colisão
de nomes na saída do OOPS! (por A4). Um veio do instrumento e não da inspeção: `Observation` era um
relator ternário que as duas leituras manuais não viram, resolvido como *construct deficit* de
UFO-B. O fato de a ferramenta achar o que a análise não achou sustenta a tese de que tais deficiências
permanecem latentes. Três são lacunas declaradas, e constam como limitação (§8). Duas são artefato
do pipeline, não do modelo, e foram descartadas.

## 5.6. O que decorre disso para o domínio

Um modelo de referência que não fixa a interpretação em nove pontos permite que duas iniciativas se
declarem aderentes a ele com interpretações semanticamente incompatíveis, sem que a incompatibilidade
apareça no discurso de aderência: cada uma pode ler *agrupamento* como taxonomia ou composição,
*processo* como vínculo ou evento, *ator* como tipo único ou como categoria sobre identidades
distintas, e nenhuma contraria o MPO. A análise converte essa afirmação em demonstração de dois
modos: a formalização publicada é uma tentativa real e documentada, e divergiu em nove pontos; e a
QC7, sobre dois observatórios instanciados na ontologia revisada, devolve oito conceitos cobertos
por apenas um deles contra vinte e três comuns (§7).

O limite é **n=1**: há um formalizador, e o que se demonstra é que o MPO **permite** os nove desvios,
não que outro os cometeria; generalizar exigiria formalizações independentes do mesmo modelo (§9).
O traço não depende de n: cada desvio foi localizado em um ponto de abertura do modelo, que permanece
aberto para quem vier a formalizá-lo. Nessa perspectiva, as nove correções constituem uma evolução do MPO.

<!--
ticket 13: o par antes/depois de 5.1 sai como listagem verbatim. O diagrama integrado é da seção 6,
pelo esqueleto, e esta seção não leva figura própria. A formalização analisada é localizável pela
linha de base no artefato suplementar anônimo, sem expor autoria.
-->
