# 07: Instanciação e primeira questão de competência ponta a ponta

**What to build:** o *tracer bullet* do trabalho. Uma única questão de competência atravessando todo
o caminho — modelo revisado, OWL, dados de instância de um observatório real, consulta SPARQL,
resultado documentado — provando que o percurso inteiro funciona antes de escalar para as demais.

Cenário: um observatório de projetos de pesquisa e extensão de uma universidade pública brasileira,
documentado nos Anais Estendidos do SBSI. **É trabalho anterior do próprio autor: toda menção, no
código, nos dados e no texto, deve ser em terceira pessoa**, jamais como "nosso trabalho anterior".

A QC escolhida para o tracer deve ser de domínio e verificável em instâncias, não estrutural. A
avaliação anterior falhou exatamente aqui: usava consultas que devolveriam a mesma forma para
qualquer ontologia, testando a implementação em vez do domínio.

**Blocked by:** 06 (transformação gUFO e OWL revisada)

**Status:** ready-for-agent

- [ ] Dados de instância do observatório carregados na ontologia revisada, derivados do que a publicação documenta
- [ ] Uma QC de domínio escolhida e executada em SPARQL ponta a ponta
- [ ] A consulta interroga conhecimento do domínio, não a estrutura do artefato — não passa se puder ser respondida por qualquer ontologia
- [ ] Resultado não-vazio e semanticamente correto, conferido contra o que a fonte documenta
- [ ] Consulta e resultado completos salvos em formato reaproveitável pelo apêndice
- [ ] Nenhuma menção identificadora ao autor nos dados, nos comentários ou nos rótulos
- [ ] O percurso está reproduzível por um terceiro a partir dos artefatos salvos
