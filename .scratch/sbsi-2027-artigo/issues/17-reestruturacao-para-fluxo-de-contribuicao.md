# 17: Reestruturação para fluxo de contribuição

**What to build:** reorganizar o corpo para que a narrativa siga problema → lacuna → desenho →
achados → artefato → avaliação → implicações. A estrutura de nove seções funciona, mas separa
demais fundamentação e trabalhos relacionados e deixa a contribuição comparativa aparecer tarde.

O objetivo não é reescrever o artigo nem aumentar o limite de 20 páginas. É redistribuir o espaço
atual de 15,05 páginas do corpo, preservando artefatos, verificadores e a correspondência dos sete
labels do resumo estruturado.

**Blocked by:** 15 (posicionamento e lacuna delimitada), 16 (perguntas de pesquisa e calibração da
evidência)

**Status:** ready

- [ ] Novo esqueleto aprovado e refletido em Markdown, LaTeX e verificadores antes de mover texto
- [ ] Introdução contém problema, RQs, contribuições e mapa do artigo em aproximadamente 1,20 página
- [ ] Fundamentos e trabalhos relacionados tornam-se um bloco integrado de aproximadamente 2,50 páginas, encerrado pela lacuna delimitada
- [ ] Método explicita desenho, critério de achado e estratégia de avaliação em aproximadamente 1,45 página
- [ ] Análise ontológica preserva a Tabela A1--A9 e recebe aproximadamente 3,65 páginas, sem perder os traços à fonte
- [ ] OntoMPO revisada mantém diagrama, decisões ontológicas e transformação em aproximadamente 2,25 páginas
- [ ] Avaliação recebe aproximadamente 1,95 página para evidência das QCs, comparações antes/depois e interpretação dos controles
- [ ] Discussão e limitações recebem aproximadamente 1,25 página; conclusão, aproximadamente 0,80 página
- [ ] Orçamentos do frontmatter, declaração, referências e apêndice são recalculados por compilação; total final fica entre 15 e 20 páginas
- [ ] Os sete labels do resumo estruturado continuam refletidos em ao menos uma seção do corpo
- [ ] Geradores e verificadores são atualizados, e a suíte de conferência passa após a reestruturação

## Comments

Distribuição proposta para o corpo: 1,20 + 2,50 + 1,45 + 3,65 + 2,25 + 1,95 + 1,25 + 0,80 =
15,05 páginas. Portanto, esta alteração não requer nova folga; ela apenas move 0,59 página do bloco
fundacional, 0,09 da apresentação do artefato e 0,04 da conclusão para análise, avaliação e
discussão.

Há duas opções de implementação. A preferida é fundir §§2 e 3 em “Fundamentos e trabalhos
relacionados” e renumerar as seções seguintes. A conservadora mantém a numeração atual, mas termina
a §3 com o quadro comparativo e move RQs para §1. Escolher a primeira somente se a alteração nos
verificadores for pequena; a segunda preserva o andaime e é suficiente para corrigir a leitura.

O título e o resumo estruturado já estão congelados no registro JEMS3. Este issue não os modifica;
o ganho vem da ordem do corpo e da precisão das alegações, não de alterar metadados de submissão.
