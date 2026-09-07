# Procedência dos dados de instância do observatório

Este documento liga cada indivíduo de `observatorio.ttl` ao trecho da publicação de onde ele foi
derivado, para que um terceiro com a publicação em mãos possa conferir a instanciação linha a linha.

O arquivo `observatorio.ttl` é **gerado** por `tools/generation/gerar_instancias.py` e não se edita à
mão; a fonte editável é o script, e este mapa acompanha as duas.

## A fonte

> Observatório de Projetos de Pesquisa e Extensão. *Anais Estendidos do XVIII Simpósio Brasileiro de
> Sistemas de Informação (SBSI 2022)*, SBC, 2022, p. 41–44.
> DOI [10.5753/sbsi_estendido.2022.222995](https://doi.org/10.5753/sbsi_estendido.2022.222995).

A publicação-fonte é citada **em terceira pessoa**, pelo seu DOI. Nos IRIs, nos rótulos, nos
comentários e neste texto, nada identifica autoria, instituição ou localidade. O IRI
de instância usa o domínio de exemplo `https://example.org/ontompo/instancia-observatorio#`, à
semelhança dos IRIs de exemplo da própria ontologia.

## O cenário, em terceira pessoa

A publicação descreve a concepção de um observatório de projetos de pesquisa e extensão de uma
universidade pública brasileira. O observatório é apresentado como instrumento de transparência
baseado em sistema computacional, alinhado à Lei de Acesso à Informação, e foi construído como um
protótipo funcional em WordPress (PHP e MySQL) e avaliado por uma *survey* com 25 participantes. A
universidade mantém, à parte, um sistema de gestão de projetos de pesquisa, sem integração com o
observatório.

## Mapa trecho → instância

### O observatório e o seu gerenciamento de conteúdo

| Indivíduo | Tipo na OntoMPO | O que a publicação documenta | Local |
|---|---|---|---|
| `obs:observatorio` | `ProjectObservatory` | «o desenvolvimento de um observatório de projetos» — protótipo funcional em WordPress | seções 4.1 e 4.2 |
| `obs:gerenciadorDeConteudo` | `DataManager` | «A tecnologia atrelada ao desenvolvimento do observatório foi o Wordpress, que é um sistema de gerenciamento de conteúdo que utiliza PHP e MySQL» | seção 4.2 |

`obs:gerenciadorDeConteudo` é declarado componente de `obs:observatorio`
(`ontompo:componentOf_DataManager_ProjectObservatory`), conforme a correção de A9: o gerenciamento de
dados é papel de um **componente** do observatório, não uma especialização dele.

### As oito funcionalidades da seção 4.1, cada uma como uma `View`

A seção 4.1 lista: «As principais funcionalidades identificadas para o observatório são: Manter
projetos para que possam ser acessados pela Sociedade; Consultar dados dos projetos; Realizar
download de dados brutos dos projetos; Acessar análise detalhadas dos projetos; Permitir que
usuários interajam com os projetos a partir da inclusão de comentários, reações e relatos de erro;
Cadastrar e participar de fóruns de discussão; Postar notícias em redes sociais; Cadastrar mídia
sobre os projetos.»

Cada funcionalidade vira uma `View`, no papel que a definição da OntoMPO lhe atribui: `CrudView`
quando dispara operação sobre o repositório, `Disseminator` quando divulga dados e análises,
`Reporter` quando coordena interação entre usuários ou com outros sistemas.

| Indivíduo | Rótulo (`skos:prefLabel`) | Papel (`rdfs:subClassOf ontompo:View`) | Trecho | Por que esse papel |
|---|---|---|---|---|
| `obs:manutencaoDeProjetos` | Manutenção de projetos | `CrudView` | «Manter projetos para que possam ser acessados pela Sociedade» | mantém registros no repositório de projetos |
| `obs:consultaDeDadosDosProjetos` | Consulta de dados dos projetos | `CrudView` | «Consultar dados dos projetos» | dispara leitura sobre o repositório |
| `obs:cadastroDeMidia` | Cadastro de mídia sobre os projetos | `CrudView` | «Cadastrar mídia sobre os projetos» | cria registros de mídia no repositório |
| `obs:downloadDeDadosBrutos` | Download de dados brutos dos projetos | `Disseminator` | «Realizar download de dados brutos dos projetos» | divulga os dados dos projetos ao público |
| `obs:analisesDetalhadas` | Análises detalhadas dos projetos | `Disseminator` | «Acessar análise detalhadas dos projetos»; a seção 2 cita «gráficos e tabelas» | divulga análises e reflexões sobre os dados |
| `obs:interacaoComProjetos` | Interação dos usuários com os projetos | `Reporter` | «Permitir que usuários interajam com os projetos a partir da inclusão de comentários, reações e relatos de erro» | coordena a interação dos usuários com os projetos |
| `obs:forunsDeDiscussao` | Fóruns de discussão | `Reporter` | «Cadastrar e participar de fóruns de discussão» | coordena a interação entre usuários |
| `obs:noticiasEmRedesSociais` | Publicação de notícias em redes sociais | `Reporter` | «Postar notícias em redes sociais» | coordena o relacionamento do observatório com outros sistemas |

Cada `View` é componente de `obs:observatorio`
(`ontompo:componentOf_View_ProjectObservatory`) e é disponibilizada pelo gerenciamento de conteúdo
por um relator `ontompo:ViewProvision` (`obs:disponibilizacaoDe_<funcionalidade>`), que medeia
`obs:gerenciadorDeConteudo` e a `View`. É esse relator que a QC1 percorre.

### Os perfis de ator da *survey* (seção 4.3)

| Indivíduo | Tipo | Trecho |
|---|---|---|
| `obs:usuarioEstudante` | `ObservatoryUser` | «64% foram alunos» das 25 pessoas convidadas para a avaliação |
| `obs:usuarioDocente` | `ObservatoryUser` | «12% foram professores» |
| `obs:usuarioDaSociedade` | `ObservatoryUser` | «24% que representaram a sociedade»; a seção 1 fala em aproximar «os cidadãos de projetos dos quais podem se beneficiar» |

### O sistema externo (seção 5)

| Indivíduo | Tipo | Trecho |
|---|---|---|
| `obs:sistemaDeGestaoDeProjetos` | `System` | «A universidade em questão possui um sistema para gestão de projetos de pesquisa, já o observatório é um sistema à parte que não possui integração com a ferramenta» |

## Ticket 08 — a cadeia de proveniência, as partes interessadas e o segundo observatório

O ticket 07 parou no que a publicação documenta. As seis QCs restantes exigem construtos que a
publicação não descreve como tais — uma cadeia de ETL com carimbo de tempo, partes interessadas com
motivação registrada, projetos nomeados, um segundo observatório. O ticket 08 os acrescenta ao
cenário, e o que cada acréscimo tem de premissa está marcado abaixo. Nenhum deles contradiz a fonte;
o que vai além dela está dito por extenso.

### O que deriva da publicação

| Indivíduo | Tipo na OntoMPO | O que a publicação documenta | Local |
|---|---|---|---|
| `obs:grupoDoObservatorio` | `ObservatoryGroup` | «equipe de gestão e desenvolvimento», perfis de usuário e o sistema externo, reunidos como coletivo do observatório | seções 4.2 e 4.3 |
| `obs:projetoExtensaoComunitaria` | `Project` | «Manter projetos para que possam ser acessados pela Sociedade» — projeto observado do tipo extensão | seção 4.1 |
| `obs:fonteCadastroDeProjetos` | `DataSource` | «A tecnologia atrelada ao desenvolvimento do observatório foi o Wordpress» e a funcionalidade de cadastro de projetos: a origem principal dos dados é o cadastro preenchido pela equipe e pelos coordenadores | seções 4.1 e 4.2 |
| `obs:parteInteressadaCoordenacaoDeProjeto`, `obs:parteInteressadaAgenciaDeFomento`, `obs:parteInteressadaComunidadeAtendida` | `StakeHolder` | o glossário do Apêndice A define parte interessada como «indivíduo, grupo ou organização»; a seção 1 fala em aproximar «os cidadãos de projetos dos quais podem se beneficiar» | Apêndice A; seção 1 |

Cada parte interessada é `memberOf` `obs:grupoDoObservatorio`
(`ontompo:memberOf_StakeHolder_ObservatoryGroup`), e os três perfis de usuário e o sistema externo
também passam a declarar essa participação, conforme a meronímica da rodada 2.

### As sete interações com motivação registrada (QC5)

Cada relator `obs:interacao_<ator>_<visão>` é uma `ontompo:SocialInteraction` que medeia um agente e
uma visão de relacionamento (`Reporter`), e carrega em `dct:description` a motivação daquele tipo de
ator para interagir. As motivações são redigidas a partir do papel de cada perfil na publicação —
estudantes, docentes e representantes da sociedade na seção 4.3; cidadãos que se beneficiam dos
projetos na seção 1 — e do papel de cada parte interessada no Apêndice A. A OntoMPO revisada **não
tem uma classe para motivação ou objetivo** (os momentos intencionais da UFO-C ficaram fora de
escopo, ver `spec.md`); a QC5 é respondida descrevendo a interação, e isso está registrado em
`../consultas/divergencias.md`.

### Premissa: o que vai além do que a publicação documenta

- **A segunda fonte de dados** (`obs:fontePlanilhaDadosAbertos`, `DataSource`). A publicação
  documenta coleta manual por cadastro. A segunda fonte — uma planilha de dados abertos importada
  periodicamente — é acréscimo do cenário para a QC3 e a QC6 poderem exercitar «uma **dada** fonte»,
  com mais de uma no grafo.
- **A cadeia de ETL** (`obs:processoEtl_cadastro` e `obs:processoEtl_dadosAbertos`, cada um um
  `EtlProcess` com `Extract`, `Transform` e `Load` como partes próprias). A publicação não descreve
  um *pipeline*. A cadeia é instanciada como a leitura mínima do que a coleta faz: o gerenciamento de
  conteúdo participa como `Collector`, `Processor` e `Storer`; a fonte, como `DataSource` na
  extração. O «quando» de cada carga é `gufo:hasEndPointInXSDDate` sobre o `Load` — a propriedade que
  `gufo:Event` já provê e que a análise (A5) tornou aplicável ao mover o ETL de relator para evento.
  As datas (06/03/2023 e 11/09/2023) são do cenário.
- **O módulo de coleta** (`obs:gerenciadorDeColeta`, `DataManager`, componente do observatório). A
  publicação descreve um único gerenciador de conteúdo. Este segundo componente responde pelos dados
  de um projeto cujos dados são coletados mas ainda não divulgados por nenhuma `Disseminator`, e
  existe para a QC4 poder distinguir esse projeto — sem ele, um único gerenciador ligaria toda
  observação a todo projeto e a QC4 não teria o que devolver.
- **Os projetos nomeados** (`obs:projetoExtensaoComunitaria`, `obs:projetoPesquisaAplicada`). A
  publicação documenta um protótipo e a sua avaliação, não um acervo. Os dois são projetos-exemplo,
  um por tipo que a seção 4.1 distingue (extensão acessível à Sociedade e pesquisa).
- **As observações datadas** (`obs:observacao_1`, `obs:observacao_2`, `Observation`, e o
  `obs:conhecimento_*` que cada uma cria). A publicação não registra observações concretas. As duas
  são do cenário, datadas em 10/04/2023 e 15/09/2023, e ligam um perfil de usuário a uma
  `Disseminator` do observatório.

### O segundo observatório (QC7) — `observatorio-b.ttl`

Um **observatório municipal de obras públicas, sintético**: sem fonte na literatura, sem
`dct:source` e sem `dct:creator`. Existe para a QC7 comparar a cobertura conceitual de duas
iniciativas que se dizem aderentes ao MPO. O IRI de instância usa o domínio de exemplo
`https://example.org/ontompo/instancia-observatorio-b#`, e nenhum rótulo identifica pessoa,
instituição ou município reais — a iniciativa e os seus elementos são fictícios.

Ele cobre de propósito um recorte **diferente** do cenário principal: instancia `Organization` e
`SocialAgent` (a prefeitura mantenedora), que o principal não tem, e **não** instancia `Reporter`,
`SocialInteraction`, `Observation`, `Knowledge`, `ObservatoryGroup` nem `StakeHolder`, que o
principal tem. É essa assimetria — oito conceitos — que a QC7 mede, e é a demonstração de que a
aderência declarada ao MPO não garante cobertura conceitual comum. A premissa está registrada no
ticket 08.

## Como reproduzir

```sh
python tools/generation/gerar_instancias.py           # regera observatorio.ttl e observatorio-b.ttl
python tools/generation/rodar_consultas.py            # executa consultas/*.rq (as sete QCs)
python tools/verification/verificar_instancia_qc.py   # confere a checklist do ticket 07
python tools/verification/verificar_demais_qc.py      # confere a checklist do ticket 08
```
