# Spec — Artigo para a Trilha de Pesquisa do SBSI 2027 (TP-SI)

Status: ready-for-agent

Veículo: XXIII Simpósio Brasileiro de Sistemas de Informação, Trilha de Pesquisa em SI.
Registro no JEMS3 em 08/09/2026; upload do PDF em 14/09/2026; evento presencial em Campo Grande/MS,
17–20/05/2027.

---

## Problem Statement

O autor tem uma pesquisa concluída — a OntoMPO, formalização ontológica do Modelo para Observatórios
de Projetos (MPO) — que foi **rejeitada no ONTOBRAS 2026** por cinco pareceres convergentes. A
crítica central não foi de execução, foi de **contribuição**: o artigo formalizou o MPO exatamente
como descrito na literatura, sem análise ontológica crítica, sem refinamento do modelo original e
sem insight conceitual novo. Somam-se a isso três falhas que quatro ou cinco revisores apontaram
independentemente: questões de competência que interrogam a arquitetura do modelo em vez do
conhecimento do domínio, uma avaliação que só confirma que o OWL reflete a hierarquia desenhada, e
um repositório de artefatos que retornava 404.

Levar esse mesmo material ao SBSI reproduz a rejeição, agora agravada: a TP-SI é um fórum de
Sistemas de Informação e cobra, além de tudo o que o ONTOBRAS cobrou, ancoragem em teoria de SI,
posicionamento no tripé Pessoas–Processos–Tecnologias, alinhamento explícito ao II GranDSI-Br e
evidência de relevância organizacional. O artigo atual não atende a nenhum desses quatro pontos.

Há ainda um problema material: **os artefatos da pesquisa não foram localizados**. Não existe OWL,
modelo OntoUML editável nem script em lugar algum da máquina, e o repositório GitHub citado na
dissertação está 404. Sem eles não há avaliação executável nem depósito de ciência aberta — e
"Transparência, Replicabilidade e Reprodutibilidade" é um dos cinco critérios de avaliação da trilha.

## Solution

Reposicionar a contribuição: o artigo deixa de apresentar **o MPO formalizado** e passa a apresentar
**o que uma análise ontológica revelou sobre o MPO**, entregando como artefato o modelo **revisado**.

A tese passa a ser: modelos conceituais de referência descritos em linguagem natural carregam
deficiências representacionais sistemáticas e invisíveis a quem os aplica; submeter o MPO a uma
análise fundamentada na UFO expôs nove deficiências — sobrecarga de construto, relações mereológicas
inválidas, colapso semântico, ausência de microteorias — que permaneciam latentes e que permitem a
duas iniciativas se declararem aderentes ao MPO adotando interpretações semanticamente
incompatíveis.

Essa virada resolve simultaneamente o problema científico e o problema retórico: cada defeito
apontado pelos revisores do ONTOBRAS deixa de ser uma falha do trabalho e passa a ser um **achado do
método**, apresentado como antes/depois com justificativa ontológica. O que era passivo vira ativo.

A ancoragem em SI vem da **Representation Theory (Wand & Weber)**, que fornece o vocabulário para
classificar os achados — *construct overload*, *redundancy*, *excess*, *deficit* — e converte "achamos
defeitos" em "classificamos deficiências representacionais segundo uma teoria estabelecida de SI".
O envelope metodológico é **Design Science Research**, com a **Methontology** como método de
construção do artefato; como o próprio MPO foi construído sob DSR e evoluído por focus groups, o
artigo se posiciona como continuação de um ciclo DSR já em curso, e não como um trabalho paralelo.

## User Stories

### Revisores e coordenação da trilha

1. Como coordenadora da TP-SI, quero que o PDF esteja entre 15 e 20 páginas no template SBC, para que o artigo não seja sumariamente rejeitado sem revisão.
2. Como coordenadora da TP-SI, quero título, resumo estruturado e palavras-chave em inglês tanto no JEMS3 quanto no PDF, para que a submissão seja válida mesmo com o corpo em português.
3. Como coordenadora da TP-SI, quero o resumo estruturado com os sete labels nomeados e em até 300 palavras, para que a submissão cumpra o formato exigido.
4. Como coordenadora da TP-SI, quero que os sete labels se reflitam na estrutura de seções do texto, para que haja coesão entre resumo e artigo.
5. Como coordenadora da TP-SI, quero um PDF sem qualquer identificação de autoria, instituição, agradecimento ou link, para que a revisão duplamente anônima se mantenha íntegra.
6. Como coordenadora da TP-SI, quero que o uso de IA generativa esteja declarado explicitamente, para que o Código de Conduta da SBC seja cumprido.
7. Como revisor avaliando **Novidade**, quero identificar com clareza o que este trabalho traz que o estado da arte não tem, para que eu possa julgar a originalidade.
8. Como revisor avaliando **Novidade**, quero que a contribuição não seja a mera transcrição de um modelo já publicado, para que o artigo justifique sua existência.
9. Como revisor avaliando **Rigor**, quero ver o desenho de pesquisa explicitado e justificado frente a alternativas, para que eu confie nos procedimentos.
10. Como revisor avaliando **Rigor**, quero que cada decisão de modelagem ontológica venha com justificativa fundamentada na UFO, para que eu possa contestá-la ou aceitá-la com base em argumento.
11. Como revisor avaliando **Relevância**, quero ver o domínio de aplicação e o problema organizacional apontados explicitamente, para que eu avalie a pertinência à área de SI.
12. Como revisor avaliando **Relevância**, quero ver o trabalho situado no tripé Pessoas–Processos–Tecnologias, para que eu confirme que é pesquisa de SI e não de Computação isolada.
13. Como revisor avaliando **Relevância**, quero ver a contribuição conectada a um desafio nomeado do II GranDSI-Br, para que eu enxergue o impacto na agenda nacional da área.
14. Como revisor avaliando **Relevância**, quero ver referências a Anais do SBSI, Anais Estendidos e iSys, para que o trabalho dialogue com a comunidade brasileira.
15. Como revisor avaliando **Transparência e Reprodutibilidade**, quero acessar os artefatos por um link anônimo funcional, para que eu possa inspecionar o que foi produzido.
16. Como revisor avaliando **Transparência e Reprodutibilidade**, quero as consultas e seus resultados completos, e não resumidos, para que eu possa reexecutá-los.
17. Como revisor avaliando **Apresentação**, quero seções sem redundância entre si, para que a leitura não repita o mesmo conteúdo três vezes.
18. Como revisor avaliando **Apresentação**, quero referências completas e sem chamadas quebradas, para que o texto não transmita descuido editorial.
19. Como revisor cético quanto à validação, quero uma avaliação que exercite o conhecimento do domínio, e não apenas a estrutura do artefato, para que eu acredite que a ontologia serve para algo.
20. Como revisor cético, quero que as limitações sejam declaradas pelos próprios autores, para que eu não precise descobri-las sozinho.

### Leitores e pesquisadores

21. Como pesquisador de SI que nunca leu sobre o MPO, quero uma descrição autocontida do modelo e de seus conceitos, para que eu entenda o artigo sem consultar as referências originais.
22. Como pesquisador de SI, quero entender o que são observatórios de projetos e como se distinguem de PMOs e de monitoramento de projetos, para que eu situe o trabalho num campo que reconheço.
23. Como pesquisador de SI, quero saber qual teoria de SI sustenta a análise, para que eu possa avaliar e reusar o arcabouço teórico.
24. Como pesquisador de modelagem conceitual, quero ver as deficiências representacionais classificadas por uma tipologia estabelecida, para que os achados sejam comparáveis a outros estudos.
25. Como pesquisador de ontologias, quero ver o antes e o depois de cada decisão revisada, para que eu julgue se a revisão melhorou o modelo.
26. Como pesquisador de ontologias, quero saber como o modelo OntoUML virou OWL, para que eu confie que a semântica foi preservada.
27. Como pesquisador de ontologias, quero os relatórios das verificações automáticas antes e depois, para que eu veja a melhoria de forma objetiva.
28. Como pesquisador que quer estender o trabalho, quero a ontologia depositada em formato aberto, para que eu parta dela em vez de reconstruí-la.
29. Como autor do MPO, quero que as críticas ao meu modelo venham acompanhadas de correção construtiva, para que o resultado seja evolução e não desqualificação.
30. Como pesquisador do sul global, quero ver meu veículo de publicação citado, para que a produção regional seja reconhecida.

### Praticantes

31. Como gestor que vai projetar um observatório de projetos, quero um vocabulário conceitual sem ambiguidade, para que minha equipe não interprete o mesmo termo de duas formas.
32. Como gestor de um observatório existente, quero saber se minha implementação é de fato aderente ao MPO, para que a declaração de aderência signifique algo verificável.
33. Como gestor público sujeito à Lei de Acesso à Informação, quero que o observatório dê rastreabilidade da informação divulgada, para que eu sustente a prestação de contas.
34. Como analista comparando duas iniciativas de observatório, quero uma base semântica comum, para que a comparação não dependa de coincidência terminológica.
35. Como responsável por dados de um observatório, quero saber quem executou cada carga de dados e quando, para que haja responsabilização sobre o conteúdo publicado.
36. Como parte interessada num projeto observado, quero saber a que conteúdos tenho acesso, para que eu use o observatório de forma efetiva.
37. Como desenvolvedor integrando sistemas a um observatório, quero contratos semânticos explícitos, para que a integração não dependa de convenção implícita.

### Autor

38. Como autor, quero reaproveitar o texto e as figuras da dissertação onde couber, para que o esforço de escrita caiba em onze dias.
39. Como autor, quero que cada crítica dos pareceres do ONTOBRAS tenha um endereço explícito no novo artigo, para que nenhuma volte a aparecer.
40. Como autor, quero uma varredura de anonimato antes da submissão, para que o artigo não seja rejeitado por um deslize de redação.

## Decisões de pesquisa

**Enquadramento.** A contribuição declarada é a análise ontológica do MPO e o modelo revisado dela
resultante — não a formalização do MPO. O título anuncia isso: *OntoMPO: Ontological Analysis and
Refinement of the Model for Project Observatories*.

**Teoria de SI.** Representation Theory / BWW (Wand & Weber) como teoria principal, usada
operacionalmente para classificar os achados. Organizational Information Processing Theory
(Galbraith) citada na motivação, para explicar por que observatórios existem.

**Desenho de pesquisa.** Design Science Research como envelope; Methontology como método de
construção do artefato, posicionada frente a LOT e NeOn. A escolha é justificada, entre outras
razões, pela continuidade com o ciclo DSR sob o qual o próprio MPO foi construído e evoluído.

**Abandono da defesa de "lightweight ontology".** Passou a ser passivo: um revisor a usou para
argumentar que a etapa OntoUML foi desperdício, outro para argumentar que ela não torna a ontologia
leve, mas conceitualmente incompleta. Sob o novo enquadramento a defesa perde função.

**Adoção de UFO-B e UFO-C.** Processos de ETL passam a ser modelados como eventos com participação
temporal; a camada de agentes passa a distinguir agentes físicos de sociais. Era a crítica mais
forte de um dos pareceres e, sob o novo enquadramento, é achado de primeira linha.

**Achados a produzir.** Nove deficiências, cada uma com classificação BWW e correção:

| # | Deficiência | Classificação | Correção |
|---|---|---|---|
| A1 | `CrudOperation` colapsa Create/Update/Delete, de pós-condições distintas | *construct overload* | Decompor |
| A2 | `Software` como composição de `Hardware` | *construct excess* / mereologia inválida | Execução/hospedagem |
| A3 | `«CompOf»` ligando `ObservatoryUser` a `ObservatoryGroup` («Collective») | violação de restrição UFO | `«MemberOf»` |
| A4 | Classe de domínio nomeada `Relator`, colidindo com o metaconceito da UFO | *construct redundancy* terminológica | Renomear |
| A5 | ETL como «relator» endurante em vez de evento | *construct deficit* (UFO-B) | Eventos UFO-B |
| A6 | `Agent` como «Kind» genérico, sem distinção físico/social | *construct deficit* (UFO-C) | Taxonomia UFO-C |
| A7 | `System` como «role» sem kind subjacente explícito | *construct deficit* | Explicitar o kind |
| A8 | `Management`/`Operation` como relators n-ários não justificados | ambiguidade de aridade | Justificar ou decompor |
| A9 | `ProjectObservatory` especializa `Software` e é especializado por `DataManager`/`View` | confusão de princípio de identidade | Revisar hierarquia |

**Transformação OntoUML→OWL.** Híbrida: geração via transformação gUFO com ferramenta oficial,
customização sobre o gerado, e publicação do diff. Elimina a crítica de tradução manual sem garantia
de preservação semântica e, no mesmo passo, entrega a verificação pelo plugin OntoUML.

**Reconstrução dos artefatos.** O modelo é remodelado a partir dos diagramas e do Apêndice A da
dissertação, já aplicando A1–A9. Não é retrabalho: a revisão ontológica exigiria remodelar de todo
modo.

**Cenário de instanciação.** Um observatório de projetos de pesquisa e extensão de uma universidade
pública brasileira, documentado nos Anais Estendidos do SBSI. É trabalho anterior do próprio autor,
portanto **citado obrigatoriamente em terceira pessoa**.

**Alinhamento ao GranDSI-Br.** Principal: Desafio 3, "Eco(Sistemas²) de Informação" —
interoperabilidade semântica entre iniciativas de observatório. Secundário: Desafio 2, "SI
Inteligentes sob a Perspectiva Sociotécnica".

**Estrutura e orçamento.** Nove seções mapeadas aos sete labels do resumo estruturado, somando 15 a
20 páginas; a seção de análise ontológica é nova e concentra a contribuição. Diagramas por camada
migram para o depósito se a contagem de páginas apertar; o diagrama integrado permanece no artigo.

## Decisões de verificação

O critério de uma boa verificação aqui é o mesmo de um bom teste: **exercitar o comportamento
externo do artefato — sua capacidade de responder sobre o domínio — e não sua estrutura interna.**
A avaliação do ONTOBRAS falhou exatamente por violar isso: as duas consultas SPARQL usadas eram
genéricas (uma recuperava todo par `subClassOf`, a outra despejava todas as `owl:ObjectProperty` com
domínio e alcance) e devolveriam a mesma forma para qualquer ontologia. Elas testavam a
implementação, não o domínio. São descartadas.

**Seam primária — a ontologia revisada instanciada, consultada por SPARQL.** É o ponto mais alto
disponível e o único que valida as afirmações substantivas do artigo. Todas as sete questões de
competência atravessam essa seam. As QCs são de domínio e verificáveis em instâncias:

1. Quais *Views* são disponibilizadas por um dado `DataManager`?
2. Quais partes interessadas têm acesso a quais conteúdos de um projeto observado?
3. Que agente executou a carga de uma dada fonte de dados, e quando?
4. Quais projetos de um observatório não tiveram observações registradas em um período?
5. Que motivações levam cada tipo de ator a interagir com o observatório?
6. Dado um conteúdo divulgado, qual a cadeia de proveniência até a fonte de dados original?
7. Dois observatórios distintos que se dizem aderentes ao MPO cobrem os mesmos conceitos?

As duas últimas sustentam a contribuição: proveniência e comparabilidade entre iniciativas.
Cada QC deve retornar resultado não-vazio e semanticamente correto sobre o cenário instanciado, com
consulta e resultado completos no apêndice.

**Seams secundárias — verificação automática, não substantiva.** Plugin OntoUML para conformidade
sintática e semântica à UFO; OOPS! para pitfalls. Ambos executados **antes e depois** da revisão, de
modo que a melhoria seja demonstrada por diferença e não por afirmação. Um dos pareceres pediu o
plugin nominalmente; outro pediu OOPS!/FOOPS nominalmente.

**Seam de conformidade — a chamada como checklist.** Contagem de páginas no PDF renderizado;
varredura de anonimato no fonte e na leitura integral do PDF; presença dos sete labels; citação
explícita do GranDSI-Br; declaração de uso de IA generativa.

**Rastreabilidade dos achados.** Cada linha de A1–A9 precisa aparecer em três lugares: no modelo
revisado, no relatório do plugin e no texto da seção de análise. Achado órfão é defeito.

**Prior art.** A avaliação do MPO na literatura foi feita por focus groups com especialistas e por
estudos de caso múltiplos, ambos publicados nos Anais do SBSI. É o padrão do domínio, e a ausência
de validação com especialistas neste trabalho precisa ser declarada contra esse pano de fundo.

## Out of Scope

- **Sessão de validação com especialistas.** Inviável em onze dias; declarada como limitação
  explícita e compensada pela instanciação e pela verificação automática.
- **Estudo comparativo entre múltiplos observatórios.** A QC7 demonstra a capacidade; o estudo em si
  fica para trabalho futuro.
- **Implantação operacional** da ontologia em sistema em produção.
- **Axiomatização pesada**, regras SWRL, cadeias de papéis e inferência complexa.
- **Alinhamento com ontologias externas** de gerenciamento de projetos.
- **Integração com LLMs** — permanece como direção futura, não como resultado.
- **Renomear o domínio** para "Project Monitoring". A crítica de terminologia de nicho é endereçada
  por posicionamento no referencial, não por troca de termo: o MPO é o objeto de estudo e mudar seu
  nome descolaria o artigo da literatura que ele analisa.

## Further Notes

**O prazo é o risco dominante.** Registro no JEMS3 em 08/09, PDF em 14/09, e a reconstrução dos
artefatos está no caminho crítico. Depois de 14/09 não se altera título, resumo, tópicos, PDF ou
autoria — nem se retira o artigo do processo. O resumo estruturado e o título precisam estar
fechados até 05/09.

**Se os artefatos originais aparecerem**, a etapa de reconstrução encolhe substancialmente. Vale
procurar em backups e em outras máquinas antes de 05/09.

**Anonimato é um risco recorrente, não um passo final.** O MPO é de grupo próximo ao autor e o
cenário de instanciação é trabalho do próprio autor. Toda menção precisa ser redigida em terceira
pessoa desde o primeiro rascunho — corrigir isso no fim é mais caro e mais propenso a escapar.

**Material de origem.** As fontes LaTeX da dissertação trazem o texto integral em português, as
figuras em resolução de origem e uma bibliografia de 52 entradas, que resolve a crítica de
referências incompletas. O que não existe é a ontologia OWL, o modelo editável e os scripts.

**Conteúdo reaproveitável com corte.** O referencial teórico e a descrição do método vêm da
dissertação, mas com a redundância que um dos pareceres apontou removida, e sem nenhum resquício da
defesa de ontologia leve.
