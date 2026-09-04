# 06: Transformação gUFO e OWL revisada

**What to build:** a OWL do modelo revisado, gerada por transformação oficial em vez de tradução
manual, com as customizações aplicadas por cima e o diff preservado. Ao fim, é possível responder à
pergunta que dois revisores fizeram — "como você garante que a semântica do OntoUML foi preservada
no OWL, e o que exatamente você acrescentou ao que a ferramenta já gera?" — apontando para
artefatos, não para afirmações.

A crítica original tinha duas pontas: a tradução manual não oferece garantia de preservação
semântica, e ferramentas já geram OWL automaticamente, de modo que a contribuição estaria na
customização — que não foi mostrada. O diff é a resposta às duas.

**Blocked by:** 05 (adoção de UFO-B e UFO-C)

**Status:** ready-for-agent

- [ ] OWL gerada a partir do modelo revisado pela transformação gUFO oficial
- [ ] Customizações aplicadas sobre o artefato gerado, cada uma com justificativa escrita
- [ ] Diff entre o gerado e o customizado preservado em arquivo, legível por terceiros
- [ ] A OWL passa em verificação de consistência por raciocinador
- [ ] OOPS! executado sobre a versão revisada; relatório salvo
- [ ] Comparação quantitativa com o relatório OOPS! do baseline registrada
- [ ] Métricas do artefato revisado registradas: classes, propriedades de objeto, propriedades de dados, axiomas
