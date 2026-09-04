# 02: Andaime do artigo

**What to build:** a estrutura vazia porém completa em que o texto vai ser escrito, de modo que
nenhum ticket de escrita precise decidir formato, seção ou bibliografia. Ao fim deste ticket existe
um esqueleto em Markdown com as nove seções nomeadas e o orçamento de páginas anotado em cada uma,
um scaffold LaTeX que **compila em branco** no template SBC, e a bibliografia portada e sã.

É o prefactoring do trabalho: torna fácil cada ticket de escrita que vem depois.

**Blocked by:** None (can start immediately)

**Status:** ready-for-agent

- [ ] Esqueleto Markdown com as nove seções, cada uma anotada com o label do resumo estruturado que ela carrega e com o orçamento de páginas previsto
- [ ] Scaffold LaTeX derivado do template SBC compila sem erro e produz PDF
- [ ] O `\usepackage[latin1]{inputenc}` duplicado do template original está removido, mantido apenas o `utf8` — sem isso os acentos quebram
- [ ] Bibliografia da dissertação portada, com as entradas que os pareceres apontaram como incompletas agora completas
- [ ] Nenhuma referência com chamada quebrada do tipo `[?]` sobrevive
- [ ] Entradas de Anais do SBSI, Anais Estendidos do SBSI e iSys presentes na bibliografia, conforme pede a chamada
- [ ] O scaffold não contém nome de autor, instituição nem agradecimento
