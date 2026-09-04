# 03: Linha de base — modelo *as-is* e sua verificação

**What to build:** a metade "antes" de todo antes/depois do artigo. Reconstruir o modelo OntoUML
**exatamente como ele está hoje**, sem corrigir nada, gerar uma OWL de baseline, e rodar as
verificações automáticas para registrar por escrito quais violações o modelo atual apresenta.

Reconstruir o modelo defeituoso pode parecer contraintuitivo, mas é o que dá evidência objetiva aos
nove achados: sem relatório de baseline, a afirmação "encontramos deficiências representacionais"
não passa de opinião do autor — que foi precisamente a crítica de fragilidade da inspeção manual
feita no ONTOBRAS.

Fontes: os diagramas em resolução de origem e o Apêndice A da dissertação, com glossário de 53
termos, 17 conceitos, atributos, constantes, verbos, condições e fórmulas.

**Blocked by:** None (can start immediately)

**Status:** resolved

- [x] Modelo OntoUML *as-is* reconstruído em ferramenta que suporte o plugin de verificação
- [x] O modelo reconstruído corresponde ao publicado: mesmas classes, estereótipos e relações, defeitos incluídos
- [x] OWL de baseline gerada a partir dele
- [x] Relatório do plugin OntoUML sobre o baseline, salvo em arquivo
- [x] Relatório do OOPS! sobre o baseline, salvo em arquivo
- [x] Cada uma das nove deficiências A1–A9 está confirmada por evidência: apontada por um dos relatórios ou justificada por argumento ontológico explícito quando a ferramenta não a detecta
- [x] Deficiências que as ferramentas apontarem e que não estejam em A1–A9 ficam registradas — podem virar achados adicionais

## Comments

Baseline entregue em `artifacts/ontology/`: o modelo *as-is* em `baseline/ontompo-as-is.ontouml.json`, a OWL
em `.ttl` e `.owl`, os dois relatórios, o controle do verificador, e a leitura de tudo isso em
`evidencias-A1-A9.md`. O ferramental está em `tools/` e `tools/verification/rodar_oops.py`, e a
conferência da checklist em `tools/verification/verificar_baseline.py`.

**Como o modelo foi remontado.** A fonte primária foi `mpo_formalization.png`, o diagrama integrado
da dissertação, que é superconjunto dos três por camada. Os diagramas por camada foram lidos em
ampliação para desempatar o que o integrado renderiza em poucos pixels — extremidade de agregação e
multiplicidade. Saíram 32 classes, 13 generalizações e 28 relações, sem nenhum atributo, porque o
modelo publicado não tem nenhum.

**Ferramenta.** Não há Visual Paradigm nesta máquina, e não havia como instalar o plugin. A saída foi
a `ontouml-js` 0.5.0, que é o próprio motor que o plugin invoca: mesma `OntoumlVerification`, mesma
`Ontouml2Gufo`, e o JSON gerado está no OntoUML Schema, o formato de intercâmbio do plugin — o modelo
abre no Visual Paradigm sem conversão. A 0.5.0 é a última versão que ainda expõe as duas; a 1.0.0
removeu ambas.

**O resultado que muda o plano do artigo: nenhuma das duas ferramentas acusa nenhum dos nove
achados.** O verificador devolve zero problemas. O OOPS! devolve sete, todos de higiene de OWL —
anotação, disjunção, convenção de nome —, nenhum sobre fundamentação ontológica. As 24 regras do
verificador tratam de estereótipo, provedor de identidade, natureza e generalização; nenhuma trata de
mereologia, de aridade de relator, de endurante versus perdurante ou de sobrecarga de construto.

Para que esse zero não fosse confundido com falha de execução, `controle-verificacao.js` aplica três
mutações conhecidas ao mesmo modelo, pelo mesmo caminho de código, e exige que cada uma seja acusada
com o código esperado. As três são. O zero é resultado.

Duas consequências, e a segunda é a que aperta:

- A seção de análise ontológica não pode apresentar A1–A9 como saída de ferramenta. A evidência
  objetiva é a estrutura do modelo reconstruído, que está depositada e é machine-readable, mais o
  argumento ontológico explícito de cada achado.
- O antes/depois por ferramenta que o ticket 04 vai produzir mede higiene de OWL, não correção
  ontológica. O resumo registrado no JEMS3 promete "relatórios automáticos melhorados", o que continua
  verdadeiro pelo P08 e pelo P10 — mas prometer mais do que isso no corpo do artigo é convite a
  parecer.

**A3 está errado no spec.** O spec descreve A3 como `«CompOf»` ligando `ObservatoryUser` a
`ObservatoryGroup`. Nos diagramas, em resolução de origem, o estereótipo é `«MemberOf»` nas três
relações — tanto no diagrama da camada de agentes quanto no integrado. O defeito existe, mas é a
direção: o losango está desenhado do lado do «role», de modo que o modelo declara o coletivo como
*parte* do papel. A inversão sobrevive à transformação e vira asserção OWL, com
`gufo:isCollectionMemberOf` indo de `ObservatoryGroup` para `ObservatoryUser`. Quem escrever a seção
precisa usar esta descrição; a do spec é falsificável por qualquer revisor que abra a dissertação.
Anotado para o ticket 10.

**Um achado novo, e ele se sustenta sozinho.** Três das quatro mediações de `Operation` têm mínimo
zero na ponta mediada. Uma «mediation» é dependência existencial: o mínimo na ponta mediada tem de
ser ao menos 1. O modelo portanto admite uma `Operation` que medeia um `Service` e mais nada — um
relator que não reifica relação alguma. É estrutural, machine-checkable a partir do JSON, e não
coberto por nenhuma das 24 regras. Está registrado como B1 e é candidato a décimo achado.

Outros seis ficaram registrados como B2 a B7, entre eles a `«MemberOf»` que não designa todo nem
parte, os 63 elementos sem definição apontados pelo P08 — contra 53 termos definidos no Apêndice A,
que nunca chegaram ao modelo — e a ausência completa da camada de atributos.

Três saídas do OOPS! **não** são achados e estão marcadas como tal: P34, P35 e o *warning* final são
efeito de remover o `owl:imports gufo:` da cópia submetida, sem o que o serviço devolve
`unexpected_error`; e o P13 é efeito da opção `createInverses: false` na transformação.

**Reprodutibilidade.** Os identificadores da `ontouml-js` e os rótulos de nó anônimo da `rdflib` são
sorteados a cada execução. Ambos foram fixados de forma determinística, senão cada `gerar-baseline`
produziria artefatos diferentes sem que nada tivesse mudado, e o diff contra o modelo revisado do
ticket 04 seria ilegível. O `to_canonical_graph` da rdflib não serve: desempata nós isomorfos por
sorteio e falha uma em cada cinco execuções. Só `relatorio-oops.xml` muda entre execuções, porque o
serviço carimba um identificador de requisição novo.

**Conferência.** `tools/verification/verificar_baseline.py` reprova quando o modelo diverge da segunda leitura
dos diagramas — transcrita de novo, das imagens, e deliberadamente não importada de
`modelo-as-is.js` —, quando um defeito é corrigido de passagem, quando A2 ou A3 não sobrevivem à
transformação gUFO, quando falta seção de alguma das nove deficiências, quando o controle registra
mutação não detectada, quando o XML do OOPS! guarda um erro em vez de um relatório, e quando um
pitfall apontado pela ferramenta fica sem endereço no documento de evidências. As treze verificações
foram exercitadas contra cópias deliberadamente quebradas do baseline antes de a checagem ser
considerada pronta.
