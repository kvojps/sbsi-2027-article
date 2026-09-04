# 08: Demais questões de competência

**What to build:** as seis questões de competência restantes executadas sobre o cenário instanciado,
com consultas e resultados completos prontos para o apêndice. Ao fim, a avaliação funcional do artigo
está inteira e é reproduzível por um terceiro.

As sete QCs, todas de domínio e verificáveis em instâncias, substituindo integralmente as cinco QCs
estruturais anteriores:

1. Quais *Views* são disponibilizadas por um dado `DataManager`?
2. Quais partes interessadas têm acesso a quais conteúdos de um projeto observado?
3. Que agente executou a carga de uma dada fonte de dados, e quando?
4. Quais projetos de um observatório não tiveram observações registradas em um período?
5. Que motivações levam cada tipo de ator a interagir com o observatório?
6. Dado um conteúdo divulgado, qual a cadeia de proveniência até a fonte de dados original?
7. Dois observatórios distintos que se dizem aderentes ao MPO cobrem os mesmos conceitos?

As duas últimas sustentam a contribuição: proveniência e comparabilidade entre iniciativas.

**Premissa registrada:** a QC7 exige um segundo observatório. Nesta versão ele é **sintético**,
construído para exercitar a comparação — o que cabe no prazo. Instanciar um segundo caso real
extraído da literatura seria mais convincente para o revisor e fica registrado como upgrade caso
sobre tempo antes de 11/09.

**Blocked by:** 07 (instanciação e primeira QC ponta a ponta)

**Status:** ready-for-agent

- [ ] As seis QCs restantes executadas em SPARQL sobre o cenário instanciado
- [ ] Cada uma retorna resultado não-vazio e semanticamente correto
- [ ] Nenhuma delas é respondível por uma ontologia arbitrária — todas interrogam o domínio
- [ ] QC6 devolve cadeia de proveniência completa, do conteúdo divulgado até a fonte original
- [ ] Segundo observatório sintético instanciado, suficiente para a QC7 exercitar a comparação de cobertura conceitual
- [ ] Consultas e resultados completos salvos, prontos para o apêndice — resumo não basta, foi crítica explícita no ONTOBRAS
- [ ] Divergências entre resultado esperado e obtido registradas, mesmo quando favorecem o modelo
