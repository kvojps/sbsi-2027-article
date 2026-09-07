# Consistência da OWL, por raciocinador

Derivado dos artefatos a cada execução de `tools/verification/raciocinador.py`, com a gUFO local de `sources/gufo/`. Saída bruta em `relatorio-raciocinador.json`.

## Consistência

| Artefato | Triplas (com a gUFO) | Inconsistências |
|---|---|---|
| gerada | 1401 | 0 |
| customizada | 1992 | 0 |

As duas são consistentes. A customização não introduziu contradição: era o risco real da **C3**, que declara disjuntos dezoito «kind» de uma vez.

## Controle positivo

Cada linha é uma mutação aplicada aos dois artefatos, e cada uma tem de dar o resultado esperado. As quatro primeiras são acusadas nos dois, porque violam algo que a transformação ou a gUFO já afirmavam; as quatro últimas só no customizado, e é isso que a customização acrescentou de conteúdo lógico.

| Mutação | gerada | customizada | O que a sustenta |
|---|---|---|---|
| um indivíduo que é `PhysicalAgent` e `SocialAgent` | acusada | acusada | a partição `agentNature`, que a adoção de UFO-C (A6) introduziu e a transformação carrega para o OWL |
| um indivíduo que é `CreateOperation` e `DeleteOperation` | acusada | acusada | a partição `crudOperationType`, que a decomposição de A1 introduziu |
| um indivíduo que é `Person` e `Observation` | acusada | acusada | `gufo:Endurant` disjunto de `gufo:Event`, na ontologia de fundamentação — é o que dá dentes à adoção de UFO-B (A5, B8): antes da rodada 2, `Observation` era um relator endurante e a mutação passaria |
| uma `Observation` da qual um `Load` participa como agente | acusada | acusada | o domínio de `participation_Agent_Observation` é `Agent`, endurante, e `Load` é evento — mostra que domínio e alcance gerados têm consequência, e não são decoração |
| um indivíduo que é `Project` e `DataSource` | não acusada | acusada | a disjunção entre «kind» acrescentada pela **C3** — dois princípios de identidade distintos não valem para o mesmo indivíduo. `Person` e `Organization` não serviriam de controle aqui: a partição `agentNature` já os separava |
| um indivíduo que é `Hardware` e `Network` | não acusada | acusada | a mesma disjunção entre «kind» da **C3**, agora na camada de infraestrutura |
| um `DataManager` que é o próprio `ProjectObservatory` | não acusada | acusada | a disjunção entre os subtipos de `Software` acrescentada pela **C3**, que fecha o que sobrou de A9 |
| uma `Observation` que tem um `Load` por participante | não acusada | acusada | a inversa nomeada acrescentada pela **C4**: no artefato gerado a propriedade não existe, e a mutação não diz nada |

Todos os controles deram o esperado, o que torna interpretável o zero da tabela acima.

## O que esta verificação não cobre

O raciocinador é o `owlrl`, que implementa o perfil **OWL 2 RL** sobre a rdflib.
Foi escolhido porque é o único disponível sem uma máquina virtual Java — o HermiT e o Pellet, que a
`owlready2` empacota, exigem uma. A escolha tem preço, e ele precisa estar escrito:

- **Restrições de cardinalidade qualificada ficam fora do perfil.** O artefato tem 40
  `owl:Restriction`, das quais 24 com `owl:minQualifiedCardinality` e 7 com
  `owl:qualifiedCardinality`, todas em posição de superclasse — que é onde o OWL 2 RL não as
  avalia. Um indivíduo que violasse uma dessas cardinalidades passaria por aqui. É a maior lacuna
  desta verificação, e ela cobre justamente o que a transformação gUFO gera a partir das
  multiplicidades do modelo OntoUML.
- **A verificação é sobre a base de conhecimento, não sobre a satisfatibilidade dos conceitos.** Um
  raciocinador DL diria se alguma classe é necessariamente vazia mesmo sem instância nenhuma; o
  OWL 2 RL só acusa quando há um indivíduo que viola. É por isso que cada mutação introduz um
  indivíduo: sem ele, não há o que acusar.
- **As anotações da C2 e as declarações da C1 não têm conteúdo lógico**, e por isso não têm controle
  positivo aqui. Não é omissão: não há o que um raciocinador possa dizer sobre um `rdfs:comment`. O
  que mede a C1 é o relatório do OOPS!, onde P34 e P35 caem; o que mede a C2 é o mesmo relatório,
  onde P08 cai.

O que a verificação cobre, dito com precisão: **nenhuma disjunção, subsunção, domínio ou alcance
declarado nos dois artefatos entra em contradição com os demais nem com a gUFO**, e a bateria de
mutações mostra que a verificação acusaria se entrasse.

