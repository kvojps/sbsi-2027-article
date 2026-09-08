# 8. Discussão e Limitações

<!--
Superfície de escrita da seção 8. Convenções em `06-ontompo-revisada.md`; conferência em
`tools/verification/verificar_seccoes_ontologia_avaliacao_conclusao.py`.

Esta seção traz **lições**, e um parecer do ONTOBRAS criticou exatamente a conclusão que resumia
resultados no lugar delas. O verificador reprova se os números que a §7 relata reaparecerem aqui.
-->

**A subdeterminação não se manifesta como contradição, e é por isso que ela escapa.** Nenhum dos
desvios contraria uma frase do modelo de referência; cada um decorre de decisão que o texto não toma
e que quem formaliza tem de tomar. O ponto de abertura tem forma reconhecível: um verbo de relação
que admite mais de uma leitura ontológica, uma enumeração de coisas com identidades distintas
tratada como categoria única, um mesmo fenômeno nomeado como componente e como ação sem que se diga
qual dos dois vira elemento formal. Reconhecer essa forma é o que o procedimento oferece a quem for
auditar outro modelo em prosa — não uma lista de defeitos a procurar, mas os lugares onde eles
nascem, que seguem abertos para o próximo formalizador.

**As ferramentas atestam conformidade, e conformidade não é adequação.** O verificador de
conformidade à UFO nada encontrou na formalização defeituosa, e nada encontraria: as deficiências
mais consequentes — um construto que colapsa ações de pós-condições distintas, uma composição que
confunde execução com parte, uma hierarquia que faz de cada interface um observatório — são defeitos
de significado, fora do alcance de qualquer regra sintática. A lição é de método: um relatório vazio
só é interpretável se alguém provar que o instrumento dispara, e o limite de cada um precisa ser
declarado junto com o resultado. A recíproca vale: um relator ternário que duas leituras manuais
deixaram passar foi achado pela ferramenta. A análise humana erra por familiaridade com o texto, a
ferramenta por não o ler, e é a combinação que sustenta o resultado.

**A instanciação expõe o que o argumento não expõe.** As questões de competência foram feitas para
validar, e o que fizeram de mais útil foi diagnosticar: revelaram que não há vínculo entre a
observação e o projeto que ela concerne, que a proveniência para no gerenciamento responsável e que
a motivação só é dizível como anotação — nenhuma delas apareceu na leitura do modelo nem nos
relatórios das ferramentas. Perguntar ao artefato o que o domínio precisa saber é diagnóstico, e
usá-lo cedo custa menos que descobri-lo depois da implantação.

**O que isso diz sobre modelos de referência descritos em prosa.** As definições existiam: o
apêndice da conceituação define 53 termos, e nenhum chegou ao modelo formal. Publicá-lo sem os
artefatos intermediários que o produziram devolve ao leitor a tarefa de reconstruir as decisões, e é
aí que as interpretações divergem. Publicar a conceituação ao lado do modelo fecha boa parte da
abertura; dizer o tipo ontológico de cada relação enunciada fecha o resto.

Seis limitações precisam ser declaradas. **Não houve validação com especialistas**, e a ausência
pesa contra um pano de fundo específico: o modelo analisado foi avaliado, na literatura, por grupos
focais e por estudos de caso múltiplos publicados nos Anais do SBSI [vieira2022evaluating,
vieira2023survey]. Esse é o padrão do domínio, e este trabalho não o cumpre: o que oferece no lugar
atesta capacidade de resposta e conformidade, não aceitação pela comunidade. **Há um formalizador**,
e o que se demonstra é que o modelo de referência **permite** os desvios, não que outro os
cometeria; superá-lo exige formalizações independentes (§9). **O segundo observatório da comparação
é sintético**, e a assimetria é em parte por construção.

**O artefato tem lacunas registradas**, nenhuma corrigida em silêncio: a camada de atributos que a
conceituação especifica não existe no modelo; um relator segue candidato a evento; e o coletivo do
observatório reúne membros de naturezas incompatíveis. A **verificação de consistência é do perfil
OWL 2 RL**, escolhido por não exigir máquina virtual Java, e ele não avalia cardinalidade
qualificada em posição de superclasse — o que a transformação gera das multiplicidades. Por fim,
**ficaram fora de escopo, por decisão de pesquisa**, a implantação operacional em produção, a
axiomatização pesada com regras e cadeias de papéis, e o alinhamento a ontologias externas: cada um
alteraria o que o artefato pode afirmar, e nenhum é afirmado aqui.