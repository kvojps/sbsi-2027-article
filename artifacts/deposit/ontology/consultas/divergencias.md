# Divergências entre o resultado esperado e o obtido — QC2 a QC7

Cada questão de competência foi executada sobre o cenário instanciado com uma expectativa escrita
antes da execução. Este documento registra onde o resultado obtido divergiu dessa expectativa,
**inclusive quando a divergência favorece o modelo** — foi crítica explícita dos pareceres do
ONTOBRAS que a avaliação anterior só mostrava o que dava certo.

O critério: uma divergência é tudo o que a consulta devolveu (ou deixou de devolver) e que a leitura
ingênua da pergunta não previa. Nenhuma delas invalida a QC; várias apontam limite do modelo
revisado, e é esse o valor de registrá-las.

## QC2 — partes interessadas e conteúdos

**Esperado.** Para cada parte interessada, os conteúdos do observatório a que ela tem acesso, e o
projeto observado a que cada conteúdo se refere.

**Obtido.** Quatro linhas, todas com conteúdo do tipo `Reporter` e todas apontando para o mesmo
projeto (`projetoExtensaoComunitaria`).

**Divergência — contra o modelo.** O único vínculo que a OntoMPO tem entre um agente e um conteúdo é
o relator `SocialInteraction`, e ele medeia `Agent` e **`Reporter`** — visões de relacionamento. O
acesso a conteúdo **disseminado** (`Disseminator`) não tem vínculo próprio: só é representável de
forma indireta pelo evento `Observation`, que o modelo enquadra como criação de conhecimento, não
como acesso. A QC2, portanto, responde sobre as visões de relacionamento; «acesso a conteúdo» num
sentido mais amplo é limite do modelo, não do cenário.

**Divergência — do cenário.** Todas as linhas apontam para um só projeto porque só
`projetoExtensaoComunitaria` está sob o gerenciador que disponibiliza as visões de relacionamento;
`projetoPesquisaAplicada` está com o módulo de coleta. É consistente, mas o resultado não exercita
partes interessadas de projetos diferentes — exercitaria com um segundo gerenciador de conteúdo, que
o cenário não tem.

## QC3 — quem executou a carga, e quando

**Esperado.** Para cada fonte de dados, o agente que executou a carga correspondente e a data.

**Obtido.** Quatro linhas: duas fontes × dois papéis (`Processor` e `Storer`), executor sempre
`gerenciadorDeConteudo`, datas 06/03/2023 e 11/09/2023.

**Divergência — contra o modelo.** «Que **agente**» sugere uma pessoa. A OntoMPO revisada não tem
participação entre `Agent` (pessoa) e os eventos de ETL: os participantes de `Load` são os papéis
`Processor` e `Storer`, desempenhados por um componente de software. A responsabilização de uma
pessoa por uma ação corre pelo relator `Log`, que a rodada 2 **não** converteu em evento (registrado
como B9 em `correcoes-rodada-2.md`) e que não toca a cadeia de ETL. O «quem» que o modelo entrega é,
portanto, o componente de gerenciamento de dados no papel em que participou — não um agente humano.

**Divergência — de forma.** A mesma carga aparece em duas linhas, uma por papel (`Processor`,
`Storer`), porque os dois participam do mesmo `Load`. Não é erro; é o modelo dizendo que a carga tem
dois participantes.

**Sobre o «quando».** A data está em `gufo:hasEndPointInXSDDate` sobre o `Load`. O modelo revisado
continua **sem tipar atributo temporal próprio** (B6, em aberto): o carimbo é metadado de instância
sobre o evento, usando a propriedade que `gufo:Event` já provê. A adoção de UFO-B (A5) é o que
tornou o `Load` um evento onde essa propriedade se aplica — antes, com o ETL como relator endurante,
não havia onde pôr a data.

## QC4 — projetos sem observação num período

**Esperado.** Os projetos do observatório sem nenhuma observação registrada no período consultado.

**Obtido.** Uma linha: `projetoPesquisaAplicada`.

**Divergência — contra o modelo.** A OntoMPO revisada **não tem relação entre `Observation` (ou o
`Knowledge` que ela cria) e `Project`**. «Projetos sem observação» só é respondível roteando por
fora: `Observation` → `Disseminator` (participante) → `ViewProvision` → `DataManager` →
`ProjectDataManagement` → `Project`. Esse caminho só distingue um projeto do outro porque o cenário
dá a cada um um gerenciador diferente; num modelo fiel, a observação apontaria para o projeto que
ela concerne. A QC funciona, e ao funcionar expõe a lacuna.

**Sobre o período.** O filtro de data (`2023-01-01` a `2023-06-30`) exclui a observação de
15/09/2023 e mantém a de 10/04/2023, então `projetoExtensaoComunitaria` — observado em abril — sai do
resultado. Com o período aberto para 2023 inteiro o resultado é o mesmo; com o período restrito ao
segundo semestre, `projetoExtensaoComunitaria` também entraria.

## QC5 — motivações por tipo de ator

**Esperado.** Para cada tipo de ator, as motivações que o levam a interagir com o observatório.

**Obtido.** Sete linhas, agrupadas em dois tipos: `Parte interessada` (quatro) e `Usuário do
observatório` (três).

**Divergência — contra o modelo.** O «tipo de ator» é resposta legítima do modelo: a taxonomia de
`Agent` da rodada 2 (A6) é o que o torna uma pergunta com resposta. A **motivação**, não: a OntoMPO
revisada não tem classe para motivação, objetivo ou qualquer momento intencional da UFO-C — a
axiomatização de momentos intencionais ficou fora de escopo por decisão de pesquisa (`spec.md`). A
motivação é carregada em `dct:description` sobre o relator `SocialInteraction`. Metade da QC é
estrutural; a outra metade é anotação de instância.

## QC6 — cadeia de proveniência de um conteúdo divulgado

**Esperado.** Dado um conteúdo divulgado, a cadeia de proveniência até a fonte de dados original,
nó a nó.

**Obtido.** Quatro linhas — dois conteúdos disseminados, cada um com **duas** cadeias completas
(uma por `EtlProcess` do gerenciador), até duas fontes distintas.

**Divergência — contra o modelo.** A cadeia **abre em leque**. O modelo revisado não liga uma `View`
ao `Load`/`EtlProcess` específico que produziu o dado dela: liga o conteúdo ao gerenciador que o
disponibiliza (`ViewProvision`), e o gerenciador aos processos de ETL de que participou
(`participation_Storer_Load`). A proveniência que o modelo entrega é «todos os ETL que o gerenciador
responsável executou», não «o ETL que gerou este conteúdo». Cada linha é uma cadeia completa —
conteúdo → gerenciamento → carga → data → processo de ETL → extração → fonte —, mas não há
correspondência 1:1 entre conteúdo e fonte. É o limite que a QC6 expõe, e é honesto: com o cenário
atual o modelo não sabe estreitar mais.

**O que está certo.** A cadeia passa pela `Extract` (que tem `DataSource`), não pela `Transform`
(que não tem) — a parthood de evento (`participational_*_EtlProcess`) é o que dá o caminho, e ela
liga a extração daquela fonte, a transformação e a carga a um mesmo acontecimento.

## QC7 — cobertura conceitual de dois observatórios

**Esperado (leitura ingênua).** Dois observatórios que se dizem aderentes ao MPO deveriam cobrir os
mesmos conceitos.

**Obtido.** Trinta e uma linhas. Vinte e três conceitos são cobertos pelos dois; **oito divergem**:
`Conhecimento`, `Grupo do observatório`, `Interação social`, `Observação`, `Parte interessada` e
`Relacionamento` (`Reporter`) só no cenário principal; `Agente social` e `Organização` só no
sintético.

**Divergência — a favor da tese.** É o resultado que a QC7 existe para produzir, e está registrado
aqui para deixar claro que era **esperado do desenho**, não um acidente: aderência declarada ao MPO
não garante cobertura conceitual comum, e é isso que a contribuição do artigo — a subdeterminação do
modelo — afirma. A divergência foi tornada verificável por consulta em vez de argumentada.

**Divergência — contra a força da evidência.** O segundo observatório é **sintético**, construído
para esta comparação; a assimetria é, em parte, por construção. Um segundo caso **real**, extraído da
literatura, seria mais convincente para o revisor. Fica registrado como *upgrade* no ticket 08 caso
sobre tempo antes de 11/09.

**Nota de contagem.** As contagens usam `rdfs:subClassOf*`, então um indivíduo conta para o seu tipo
e para todos os supertipos — um `ObservatoryUser` conta em `Usuário do observatório`, `Pessoa`,
`Agente físico` e `Agente`. Os números são de cobertura, não de indivíduos distintos por conceito.
