# Relatorio do plugin OntoUML sobre o modelo revisado (rodada 1)

Verificacao sintatica e semantica contra a UFO, executada pelo `OntoumlVerification` da `ontouml-js` 0.5.0 — o mesmo motor que o plugin OntoUML para o Visual Paradigm invoca. Saida bruta em `relatorio-plugin-ontouml.json`.

- Classes verificadas: 38
- Relacoes verificadas: 32
- Generalizacoes verificadas: 17
- Conjuntos de generalizacao verificados: 1
- Problemas encontrados: 0

Nenhum problema encontrado.

## O que este relatorio nao cobre

O verificador devolve zero sobre este modelo, como devolvia sobre o *as-is*: nenhuma das seis deficiencias corrigidas nesta rodada esta ao alcance das suas 24 regras, que tratam de estereotipo, provedor de identidade, natureza e generalizacao. **O zero de antes e o zero de depois nao medem a revisao** — quem a mede e o verificador complementar, em `relatorio-verificador-extra.md`, cujas cinco regras acusam dez problemas no *as-is* e um aqui. O que este relatorio garante e que a revisao nao introduziu nenhuma violacao das regras que o plugin de fato tem.
