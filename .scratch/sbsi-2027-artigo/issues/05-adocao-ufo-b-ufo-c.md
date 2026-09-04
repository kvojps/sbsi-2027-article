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

**Status:** ready-for-agent

- [ ] Extract, Transform e Load modelados como eventos UFO-B, com participação temporal explícita
- [ ] As relações que o modelo anterior expressava via mediação continuam representadas, agora pela participação dos eventos
- [ ] Taxonomia UFO-C distinguindo agentes físicos de agentes sociais e de sistemas
- [ ] Kind subjacente ao papel `System` explicitado
- [ ] Nenhum resquício da justificativa de ontologia leve permanece no modelo ou nas notas
- [ ] Plugin OntoUML re-executado; relatório salvo e comparável ao das rodadas anteriores
- [ ] Cada correção tem registrado o par antes/depois que a seção de análise vai usar
