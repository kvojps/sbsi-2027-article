# 05: Adoção de UFO-B e UFO-C (A5–A7)

**What to build:** a rodada de revisão mais profunda, que traz para o modelo as microteorias da UFO
que a versão anterior abdicou. Era a crítica mais forte recebida no ONTOBRAS — de que não usar UFO-B
e UFO-C não torna a ontologia leve, mas conceitualmente incompleta ou colapsada — e, sob o
enquadramento deste artigo, vira achado de primeira linha.

Deficiências desta rodada:

- **A5** ETL modelado como «relator», que é endurante, em vez de evento: perde a natureza temporal e as transformações — *construct deficit* de UFO-B
- **A6** `Agent` como «Kind» genérico, sem a distinção da UFO-C entre agentes físicos e sociais — *construct deficit* de UFO-C
- **A7** `System` como «role» sem o kind subjacente explicitado; a própria dissertação admite a simplificação e a aponta como trabalho futuro

Junto com esta rodada cai a defesa de "lightweight ontology": ela não sobrevive à adoção das
microteorias e, como argumento, já era passivo — um revisor a usou para dizer que a etapa OntoUML
foi desperdício, outro para dizer que a ontologia estava incompleta.

**Blocked by:** 04 (correções estruturais)

**Status:** resolved

- [x] Extract, Transform e Load modelados como eventos UFO-B, com participação temporal explícita
- [x] As relações que o modelo anterior expressava via mediação continuam representadas, agora pela participação dos eventos
- [x] Taxonomia UFO-C distinguindo agentes físicos de agentes sociais e de sistemas
- [x] Kind subjacente ao papel `System` explicitado
- [x] Nenhum resquício da justificativa de ontologia leve permanece no modelo ou nas notas
- [x] Plugin OntoUML re-executado; relatório salvo e comparável ao das rodadas anteriores
- [x] Cada correção tem registrado o par antes/depois que a seção de análise vai usar

## Comments

Rodada entregue em `artifacts/ontology/rodada-2/`: o modelo revisado em
`ontompo-rodada-2.ontouml.json`, a OWL em `.ttl`, o relatório do plugin, o relatório do verificador
de microteorias, o controle e o diff estrutural contra a rodada 1. A leitura de tudo isso, com o par
antes/depois e a justificativa ontológica de cada correção, está em
`artifacts/ontology/correcoes-rodada-2.md`. O ferramental novo é `tools/model/ontompo-rodada-2.js`,
`gerar-rodada-2.js` e `verificador-ufo-b-c.js`, mais `tools/verification/verificar_rodada2.py` para a
conferência da checklist; `diff-modelos.js` e `controle-verificacao.js` ganharam a rodada 2 sem
mudar o que produzem para as anteriores.

**O que foi feito em cada correção.** A5: `Extract`, `Transform` e `Load` viram «event», as seis
mediações viram seis «participation» — com as mesmas multiplicidades, trocadas de lado junto com as
pontas —, e entra `EtlProcess`, o evento complexo do qual as três são partes próprias por
«participational». A6: `Agent` deixa de ser «kind» e vira «category» não-sortal, particionada em
`PhysicalAgent` e `SocialAgent`, com `Person` e `Organization` como os sortais últimos que faltavam;
`StakeHolder` vira «roleMixin», porque o glossário do Apêndice A define parte interessada como
"indivíduo, grupo ou organização" e um papel sortal só admite um princípio de identidade; e
`ObservatoryUser` passa a ser papel de `Person`. A7: entra `ComputationalSystem` «kind», `System`
passa a ser papel dele e deixa de descender de `Agent` — em UFO-C agente é o que porta momentos
intencionais, e um sistema que fornece um serviço não crê, não pretende e não se compromete.

**Dois construtos que a rodada 1 endereçou a esta, e por isso entraram.** B8, o relator ternário
`Observation` que sobrou do verificador complementar, vira «event»: `Agent` e `Disseminator`
participam dele, e `Knowledge` passa a ser **criado** nele, por «creation» — a distinção entre
participante e produto é da UFO-B e não tinha como ser feita com uma mediação, que trata os três
relata como iguais. E `CrudOperation` com as quatro operações da partição, porque o documento da
rodada 1 registrou por escrito, sob A1, que a leitura eventiva "depende de UFO-B e é do ticket 05".
A partição sobrevive à troca de estereótipo; separar os quatro tipos nunca dependeu de eles serem
endurantes.

**A medição precisou de um instrumento novo, e o critério dele mudou de forma.** O plugin devolve
zero sobre os três modelos: nenhuma das suas 24 regras distingue endurante de perdurante a partir do
papel do conceito no domínio. `verificador-ufo-b-c.js` acrescenta quatro regras e aplica **as nove**
— as cinco da rodada 1 junto com elas — aos três modelos, para que uma rodada não possa zerar as
suas reintroduzindo as da anterior. A diferença medida é **12 no as-is, 3 na rodada 1, 0 na rodada
2**.

Duas das quatro são de **medição** e disparam sobre o baseline: `modelo_sem_perdurante` e
`modelo_sem_relacao_temporal`. Nenhuma delas afirma que `Extract` deveria ser evento — isso é
julgamento de domínio; elas registram que o modelo inteiro não usa nenhum construto da microteoria,
que é o *construct deficit* na forma computável.

As outras duas são de **guarda** — `evento_sem_participante` e `participacao_invertida` — e só podem
disparar sobre um modelo que já adotou UFO-B. Cobrar delas o controle da rodada 1, disparar sobre o
baseline, as tornaria impossíveis; dispensá-las de controle deixaria o zero sem sentido. O controle
delas é uma mutação do próprio modelo revisado, como em `controle-verificacao.js`: remover as três
relações de `Observation` tem de produzir `evento_sem_participante`, e trocar as pontas de
`participation_Collector_Extract` tem de produzir `participacao_invertida`. A distinção entrou no
`CONTEXT.md`.

**A6 e A7 não viraram regra, e isso é deliberado.** Mesma razão pela qual A1, A2 e A9 não viraram na
rodada 1: que um «kind» genérico colapse pessoa, grupo e organização, e que um sistema computacional
não porte momentos intencionais, são defeitos de significado, não de forma. Continuam sustentados
por argumento ontológico explícito.

**O controle do plugin ganhou uma mutação a mais, escolhida pela rodada.** Fazer `Extract`
especializar `Collector` produz `generalization_incompatible_natures`: o plugin não sabe dizer que o
ETL deveria ser evento, mas sabe recusar um perdurante especializando um endurante. Vale registrar
no artigo pelo contraste — a ferramenta policia a fronteira depois que alguém a desenha, e não
antes.

**Dois achados novos, e os dois vieram de aplicar o critério a sério.** **B9**: o teste que converteu
o ETL alcança `SocialInteraction`, que é um evento comunicativo em UFO-C e continua «relator». Não
foi convertido porque `Log` está no mesmo par de mediações e **não** é evento — um registro de log é
endurante —, e decidir se `SocialInteraction` é o evento de interagir ou o registro daquela
interação exige do Apêndice A uma distinção que ele não faz. **B10**: depois de A7, `System` não é
agente e continua declarado membro do mesmo coletivo de que `ObservatoryUser` e `StakeHolder` são
membros; a tensão não existia enquanto tudo era `Agent`, e é a UFO-C que a torna visível. É também a
razão de `ObservatoryGroup` **não** ter sido colocado sob `SocialAgent`, embora um grupo seja o
exemplo canônico de agente social: declará-lo agente enquanto ele tem sistemas por membros trocaria
uma tensão silenciosa por uma contradição explícita. Os dois vão para o ticket 07, onde a
instanciação força a escolha.

**A defesa de "lightweight ontology" caiu.** Ela não sobrevive à adoção das microteorias, e não
sobrava nada dela no modelo nem nas notas — a varredura de `verificar_rodada2.py` confirma e passa a
reprovar se voltar. A exceção é literal e delimitada: a seção de `correcoes-rodada-2.md` que
registra o abandono pode nomeá-la; qualquer menção fora dela reprova.

**Conferência.** `tools/verification/verificar_rodada2.py` reprova quando o modelo diverge do que o
ticket pediu, quando qualquer uma das correções é desfeita, quando o baseline **ou a rodada 1** são
corrigidos de passagem — a rodada 1 é a metade "antes" desta —, quando alguma relação que a mediação
expressava deixa de estar representada pela participação com as mesmas multiplicidades, quando as
correções não sobrevivem à transformação gUFO, quando alguma regra de medição deixa de disparar
sobre o baseline ou alguma de guarda fica sem controle por mutação, quando a rodada não mede
melhora, quando uma correção fica sem par antes/depois ou sem justificativa, quando um achado
remanescente fica sem endereço, e quando um resquício da defesa de ontologia leve reaparece. As
verificações foram exercitadas contra nove cópias deliberadamente quebradas antes de a checagem ser
considerada pronta.

**OOPS! continua sem ser reexecutado**, pela mesma razão do ticket 04: o antes/depois de *pitfalls*
de OWL é do ticket 06, junto com a customização, e a OWL desta rodada ainda vai mudar lá.
