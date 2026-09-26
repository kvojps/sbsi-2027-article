# 16: Perguntas de pesquisa, respostas e calibração da evidência

**What to build:** tornar explícita a cadeia inferencial do artigo: quais aberturas do MPO permitem
desvios ontológicos na formalização e o que a OntoMPO revisada é capaz de representar e consultar.
As perguntas de pesquisa organizam introdução, método, análise, avaliação e conclusão sem criar
resultados novos.

O artigo afirma corretamente, na §5, que n=1 demonstra permissão e não frequência. Essa cautela não
é reproduzida com a mesma nitidez no resumo, na introdução e na conclusão, onde “aderência
verificável” e “rastreabilidade para prestação de contas” podem soar como validação em produção. A
revisão precisa manter o alcance real: capacidade demonstrada em artefato e cenário, não eficácia
organizacional comprovada.

**Blocked by:** 15 (posicionamento e lacuna delimitada)

**Status:** done

- [x] Introdução formula RQ1: quais pontos de abertura do MPO permitem compromissos ontológicos incompatíveis na formalização?
- [x] Introdução formula RQ2: que capacidades de representação, consulta e comparação a OntoMPO revisada demonstra no cenário avaliado?
- [x] Método associa cada passo de reconstrução, leitura, qualificação e classificação à RQ1
- [x] Método associa questões de competência, verificações antes/depois e controles positivos à RQ2, distinguindo suas funções probatórias
- [x] Tabela A1--A9 explicita, para cada achado, fonte textual, decisão da formalização, problema ontológico e correção
- [x] Avaliação separa evidência de capacidade do artefato, conformidade estrutural e qualidade de implementação OWL; relatório vazio de ferramenta não é apresentado como validação substantiva
- [x] QC7 é apresentada como comparação de cobertura conceitual em cenário controlado, e não como prova de aderência de observatórios reais
- [x] Discussão e conclusão usam verbos calibrados: “permite”, “torna possível”, “demonstra no cenário” e “oferece base para”, quando apropriado
- [x] Limitações incluem formalizador único, segundo observatório sintético, ausência de validação com especialistas e ausência de implantação operacional
- [x] Resumo e metadados congelados no JEMS3 não são alterados sem ação humana de registro; qualquer ajuste permitido limita-se ao corpo do PDF

## Comments

As RQs não devem burocratizar o artigo. Duas frases no final da introdução e respostas diretas na
conclusão bastam. Elas resolvem uma fragilidade de apresentação: hoje o leitor encontra o critério
de achado no método e o limite n=1 somente ao fim da análise, tarde demais para interpretar a tese.

RQ1 não pergunta se o MPO “tem nove defeitos”. As deficiências são da formalização publicada; a
pergunta é sobre os pontos nos quais o MPO e a conceituação não impõem uma interpretação. RQ2 não
pergunta se a ontologia é “válida”, pois a avaliação não sustenta esse predicado global.

O resumo em inglês foi congelado no JEMS3 e o `artigo.tex` o compara literalmente ao registro. Não
alterar título, resumo ou palavras-chave neste issue. Caso o texto congelado exija correção, abrir
ação humana específica e avaliar o efeito na submissão antes de modificar qualquer fonte.
