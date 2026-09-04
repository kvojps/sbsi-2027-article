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

**Status:** resolved

- [x] OWL gerada a partir do modelo revisado pela transformação gUFO oficial
- [x] Customizações aplicadas sobre o artefato gerado, cada uma com justificativa escrita
- [x] Diff entre o gerado e o customizado preservado em arquivo, legível por terceiros
- [x] A OWL passa em verificação de consistência por raciocinador
- [x] OOPS! executado sobre a versão revisada; relatório salvo
- [x] Comparação quantitativa com o relatório OOPS! do baseline registrada
- [x] Métricas do artefato revisado registradas: classes, propriedades de objeto, propriedades de dados, axiomas

## Answer

A customização é **aditiva por regra**: nenhuma tripla que a transformação gUFO produziu foi
removida ou alterada, e o acréscimo está gravado inteiro em
`artifacts/ontology/owl/diff-gerado-customizado.ttl`. É isso que responde às duas pontas da crítica
sem depender de prosa — a preservação semântica vira contenência de grafos, e
`tools/verification/verificar_owl.py` confere que gerado mais acréscimo dá exatamente o customizado.
A decisão e o preço que ela cobra estão em `docs/adr/0002-customizacao-aditiva-da-owl.md`.

São cinco customizações, cada uma com justificativa em `artifacts/ontology/owl/customizacoes.md`:
C1 declara localmente os termos que a gUFO empresta; C2 devolve as definições e os rótulos preferidos
(achados B3 e B5); C3 declara as disjunções que a UFO já obriga (B4); C4 nomeia a inversa de cada
propriedade; C5 dá título, licença e prefixo, sem autoria.

Os números: 636 triplas geradas mais 648 acrescentadas. O raciocinador não acha inconsistência nos
dois artefatos, e das oito mutações de controle, quatro só são acusadas depois da customização — é a
medida do que ela acrescentou de conteúdo lógico. No OOPS!, contando só elementos no namespace da
OntoMPO, os apontados caem de 60 para 0; a leitura completa, com o que subiu e por quê, está em
`artifacts/ontology/owl/comparacao-oops.md`.

O único *pitfall* de domínio que sobrou é P22, de convenção de nome, **deliberadamente não fechado**:
renomear os IRIs quebraria a correspondência entre cada elemento OWL e o elemento OntoUML que o
gerou, que é a única razão de usar a transformação oficial. B5 foi endereçado por `skos:prefLabel`.

Fica declarado como limitação que o raciocinador é `owlrl`, no perfil OWL 2 RL — o único disponível
sem Java —, e que as 31 restrições de cardinalidade qualificada da transformação ficam fora desse
perfil. Está escrito em `artifacts/ontology/owl/relatorio-raciocinador.md`.
