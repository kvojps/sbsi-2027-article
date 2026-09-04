# Relatorio do plugin OntoUML sobre o modelo revisado (rodada 2)

Verificacao sintatica e semantica contra a UFO, executada pelo `OntoumlVerification` da `ontouml-js` 0.5.0 — o mesmo motor que o plugin OntoUML para o Visual Paradigm invoca. Saida bruta em `relatorio-plugin-ontouml.json`.

- Classes verificadas: 44
- Relacoes verificadas: 35
- Generalizacoes verificadas: 21
- Conjuntos de generalizacao verificados: 2
- Problemas encontrados: 0

Nenhum problema encontrado.

## O que este relatorio nao cobre

O verificador devolve zero sobre este modelo, como devolvia sobre o *as-is* e sobre a rodada 1. Suas 24 regras tratam de estereotipo, provedor de identidade, natureza e generalizacao, e **nao ha regra que distinga endurante de perdurante** a partir do papel do conceito no dominio — que e exatamente o que A5 e o achado B8 sao. O que este relatorio garante e mais estreito e vale dizer: a adocao de UFO-B e UFO-C nao introduziu nenhuma violacao das regras que ele de fato tem, e elas nao sao poucas aqui, porque a rodada troca dois estereotipos de classe por camada inteira — «kind» por «category» na camada de agentes, «relator» por «event» no ETL — e cada troca mexe com natureza, sortalidade e rigidez nas generalizacoes vizinhas. Quem mede a rodada e o verificador de microteorias, em `relatorio-verificador-ufo-b-c.md`.
