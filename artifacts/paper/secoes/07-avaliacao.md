# 7. Avaliação

<!--
Superfície de escrita da seção 7. Convenções em `06-ontompo-revisada.md`; conferência em
`tools/verification/verificar_seccoes_ontologia_avaliacao_conclusao.py`.

Esta seção relata **resultados**; o desenho da avaliação e a razão de cada frente são da §4, e o
verificador reprova a repetição. Todo número é conferido contra o artefato: as linhas de cada QC
contra `artifacts/ontology/consultas/qc*-resultado.csv`, os totais das ferramentas contra os
relatórios do plugin, do verificador estrutural e do OOPS!.
-->

## 7.1. As questões de competência sobre o cenário instanciado

A instanciação deriva cada indivíduo de um trecho identificado da publicação do cenário
[sbsi_estendido]: o observatório e seu gerenciamento de conteúdo, as oito funcionalidades, os três
perfis de usuário levantados com 25 participantes e o sistema institucional que não se integra a
ele. O que foi acrescentado está declarado item a item — uma segunda fonte de dados, a cadeia de ETL
com carimbos de tempo, um segundo componente de gerenciamento, dois projetos-exemplo e duas
observações datadas —, e o mapa entre trecho e indivíduo acompanha o depósito. A comparação da QC7
exigiu um observatório municipal de obras públicas cujo caráter sintético é limitação declarada
(§8). As sete consultas retornaram resultado não-vazio e semanticamente correto (Tabela 3), e
nenhuma interroga a arquitetura do artefato: todas percorrem construtos que a revisão introduziu
para responder a uma pergunta do domínio, e a última coluna diz qual.

**Tabela 3. As sete questões de competência sobre o cenário instanciado.**

| | Pergunta | Linhas | Construto de que depende |
|---|---|---|---|
| QC1 | Que interfaces um gerenciamento provê? | 8 | `ViewProvision`, de A9 |
| QC2 | Quem acessa que conteúdo de um projeto? | 4 | `StakeHolder` «roleMixin», de A6 |
| QC3 | Quem carregou uma fonte, e quando? | 4 | o ETL como evento, de A5 |
| QC4 | Que projetos ficaram sem observação? | 1 | `Observation` como evento, de B8 |
| QC5 | Que motivações movem cada tipo de ator? | 7 | a taxonomia de `Agent`, de A6 e A7 |
| QC6 | Qual a proveniência de um conteúdo? | 4 | a parthood de `EtlProcess`, de A5 |
| QC7 | Dois observatórios cobrem o mesmo? | 31 | as classes revisadas, com a C2 |

As consultas e seus resultados completos estão no Apêndice A e, na íntegra, no depósito aberto, com
um script que as reexecuta e confere cada uma contra o arquivo gravado — sumarizá-los aqui seria
devolver ao leitor a avaliação irreproduzível que este trabalho critica.

**As divergências foram registradas, inclusive as que desfavorecem o artefato.** Cada questão correu
contra expectativa escrita antes, e quatro apontam limite do modelo revisado. O único vínculo entre
agente e conteúdo é o relator que medeia agente e interface de relacionamento, e a QC2 responde
sobre esse recorte, não sobre acesso amplo. Na QC3, quem participa da carga são papéis de um
componente de software, não pessoa. A QC4 só distingue um projeto do outro porque o cenário dá a
cada um um gerenciamento diferente. E a cadeia da QC6 abre em leque: entrega todos os processos de
ETL do gerenciamento responsável, não o que produziu o conteúdo.

A QC7 sustenta a tese, e o resultado era esperado: dos 31 conceitos que ao menos uma das iniciativas
instancia, **23 são comuns e oito divergem** — conhecimento, grupo do observatório, interação
social, observação, parte interessada e relacionamento aparecem só no primeiro; agente social e
organização, só no segundo. Duas iniciativas aderentes ao mesmo modelo cobrem recortes conceituais
distintos, e a divergência deixou de ser argumento para virar medida.

## 7.2. Conformidade à UFO, antes e depois

O verificador de conformidade sintática e semântica devolve **zero problema sobre os três modelos**,
inclusive sobre a linha de base defeituosa, e apresentar esse zero como efeito da revisão seria
enganoso: nenhuma das suas 24 regras alcança restrição meronímica, aridade de relator ou a distinção
entre endurante e perdurante. O que ele atesta, e não é pouco, é que a revisão trocou dois
estereótipos por camada inteira sem quebrar nenhuma das regras que ele tem; quatro mutações
conhecidas mostram que ele acusaria se elas quebrassem.

A distância entre os modelos é medida por nove regras estruturais escritas para esta análise, que
operacionalizam restrições fora daquele alcance e correm sobre os três modelos pelo mesmo caminho de
código, e cai de **12 na linha de base para 3 depois da primeira rodada e 0 depois da segunda**:
somem as relações de membro com o coletivo na ponta errada, a meronímica sem extremidade declarada,
as mediações com mínimo zero, a colisão de nome com o metaconceito, os relatores acima de binário e
as duas regras da ausência da microteoria de eventos. Sete delas medem, e têm por controle positivo
a própria linha de base — a execução reprova se alguma deixar de disparar ali. As outras duas vigiam
um evento sem participante e uma participação invertida, que só a revisão produz; seu controle é uma
mutação do revisado, acusada nas duas.

## 7.3. *Pitfalls* na OWL, antes e depois

As duas execuções do detector de *pitfalls* [poveda2014oops] submetem a mesma coisa pelo mesmo
caminho de código, e é essa igualdade que os torna comparáveis. O total de elementos apontados cai
de **105 para 56**, e a leitura do artefato de domínio é mais nítida: entre os elementos que o
serviço lista, os que pertencem à OntoMPO caem de **60 para zero** — eram todos ausências de
anotação, fechadas pela C2. Dois *pitfalls* ficam fora dessa contagem porque o serviço não lista os
elementos afetados: a convenção de nome, deliberadamente não fechada, e a ausência de inversa
declarada, que cai de 21 para 7 — o número de propriedades emprestadas da gUFO que o arquivo
declara, o que sustenta ler o resto como sendo delas.

A diferença entre as leituras não é ruído, e o custo precisa estar escrito: ao declarar localmente
os termos da ontologia de fundamentação, a C1 os transforma em elementos que o serviço passa a
avaliar — sem anotação própria, sem ligação com o restante e, num caso, sem domínio nomeado. Fechar
isso exigiria embutir a gUFO no arquivo, que é o que a importação existe para evitar. Pela mesma
razão, o *pitfall* de classe não tipada sobe de 13 para 16: some a metade nomeada e sobra a anônima.
Por fim, os dois artefatos OWL são **consistentes**: um raciocinador do perfil OWL 2 RL não encontra
contradição em nenhum deles, e oito mutações confirmam que ele acusaria — quatro nos dois e quatro
só no customizado, medida do conteúdo lógico que a customização acrescentou (§8).