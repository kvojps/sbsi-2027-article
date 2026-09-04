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

**Status:** ready-for-agent

- [ ] Modelo OntoUML *as-is* reconstruído em ferramenta que suporte o plugin de verificação
- [ ] O modelo reconstruído corresponde ao publicado: mesmas classes, estereótipos e relações, defeitos incluídos
- [ ] OWL de baseline gerada a partir dele
- [ ] Relatório do plugin OntoUML sobre o baseline, salvo em arquivo
- [ ] Relatório do OOPS! sobre o baseline, salvo em arquivo
- [ ] Cada uma das nove deficiências A1–A9 está confirmada por evidência: apontada por um dos relatórios ou justificada por argumento ontológico explícito quando a ferramenta não a detecta
- [ ] Deficiências que as ferramentas apontarem e que não estejam em A1–A9 ficam registradas — podem virar achados adicionais
