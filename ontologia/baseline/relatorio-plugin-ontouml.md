# Relatorio do plugin OntoUML sobre o modelo *as-is*

Verificacao sintatica e semantica contra a UFO, executada pelo `OntoumlVerification` da `ontouml-js` 0.5.0 — o mesmo motor que o plugin OntoUML para o Visual Paradigm invoca. Saida bruta em `relatorio-plugin-ontouml.json`.

- Classes verificadas: 32
- Relacoes verificadas: 28
- Generalizacoes verificadas: 13
- Problemas encontrados: 0

Nenhum problema encontrado.

## O que este relatorio nao cobre

O conjunto de regras do verificador tem 24 codigos, todos sobre estereotipos de classe, provedores de identidade, naturezas e generalizacoes. **Nenhum deles trata de restricoes meronimicas** — nao ha regra que exija que o todo de uma «memberOf» seja um coletivo, nem que uma «componentOf» ligue complexos funcionais. Deficiencias dessa classe, como A2 e A3, precisam ser sustentadas por argumento ontologico explicito; estao em `../evidencias-A1-A9.md`.
