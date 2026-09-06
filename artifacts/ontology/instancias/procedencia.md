# Procedência dos dados de instância do observatório

Este documento liga cada indivíduo de `observatorio.ttl` ao trecho da publicação de onde ele foi
derivado, para que um terceiro com a publicação em mãos possa conferir a instanciação linha a linha.

O arquivo `observatorio.ttl` é **gerado** por `tools/generation/gerar_instancias.py` e não se edita à
mão; a fonte editável é o script, e este mapa acompanha as duas.

## A fonte

> Observatório de Projetos de Pesquisa e Extensão. *Anais Estendidos do XVIII Simpósio Brasileiro de
> Sistemas de Informação (SBSI 2022)*, SBC, 2022, p. 41–44.
> DOI [10.5753/sbsi_estendido.2022.222995](https://doi.org/10.5753/sbsi_estendido.2022.222995).

É **trabalho anterior do próprio autor**. Toda menção — nos IRIs, nos rótulos, nos comentários e
neste texto — é em **terceira pessoa**, e nada identifica autoria, instituição ou localidade. O IRI
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

## O que deliberadamente não foi instanciado

- **A cadeia de ETL e proveniência** (`DataSource`, `Extract`, `Transform`, `Load`, `Load` com
  carimbo de tempo). A publicação descreve um protótipo cuja coleta é o cadastro manual de projetos,
  não um pipeline de ETL, e não documenta cargas concretas com data e responsável. QC3 e QC6, que
  exigem essa cadeia, ficam para o ticket 08, que registra a premissa.
- **Projetos, pessoas e cargas nomeados.** A publicação documenta um protótipo e a sua avaliação,
  não uma implantação operacional com um acervo de projetos. Instanciar nomes seria inventar dados
  que a fonte não traz.
- **O segundo observatório** da QC7, que o ticket 08 constrói como cenário sintético.

## Como reproduzir

```sh
python tools/generation/gerar_instancias.py          # regera observatorio.ttl
python tools/generation/rodar_consultas.py           # executa consultas/*.rq
python tools/verification/verificar_instancia_qc.py  # confere a checklist do ticket 07
```
