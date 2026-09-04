# Diff estrutural: rodada 1 -> rodada 2

Derivado dos dois modelos a cada execucao de `tools/generation/diff-modelos.js`. E a materia-prima dos pares antes/depois; a leitura ontologica de cada um esta em `../correcoes-rodada-2.md`.

## Contagens

| | rodada 1 | rodada 2 |
|---|---|---|
| classes | 38 | 44 |
| generalizacoes | 17 | 21 |
| conjuntos de generalizacao | 1 | 2 |
| relacoes | 32 | 35 |

## Mudancas

### Classes

| | Elemento | rodada 1 | rodada 2 |
|---|---|---|---|
| muda | `StakeHolder` | «role» | «roleMixin» |
| muda | `Agent` | «kind» | «category» |
| muda | `Observation` | «relator» | «event» |
| muda | `CrudOperation` | «relator» | «event» |
| muda | `CreateOperation` | «subkind» | «event» |
| muda | `ReadOperation` | «subkind» | «event» |
| muda | `UpdateOperation` | «subkind» | «event» |
| muda | `DeleteOperation` | «subkind» | «event» |
| muda | `Extract` | «relator» | «event» |
| muda | `Transform` | «relator» | «event» |
| muda | `Load` | «relator» | «event» |
| entra | `PhysicalAgent` | — | «category» |
| entra | `SocialAgent` | — | «category» |
| entra | `Person` | — | «kind» |
| entra | `Organization` | — | «kind» |
| entra | `ComputationalSystem` | — | «kind» |
| entra | `EtlProcess` | — | «event» |

### Generalizacoes

| | Elemento | rodada 1 | rodada 2 |
|---|---|---|---|
| sai | `ObservatoryUser -> Agent` | ObservatoryUser especializa Agent | — |
| sai | `System -> Agent` | System especializa Agent | — |
| entra | `PhysicalAgent -> Agent` | — | PhysicalAgent especializa Agent |
| entra | `SocialAgent -> Agent` | — | SocialAgent especializa Agent |
| entra | `Person -> PhysicalAgent` | — | Person especializa PhysicalAgent |
| entra | `Organization -> SocialAgent` | — | Organization especializa SocialAgent |
| entra | `ObservatoryUser -> Person` | — | ObservatoryUser especializa Person |
| entra | `System -> ComputationalSystem` | — | System especializa ComputationalSystem |

### Conjuntos de generalizacao

| | Elemento | rodada 1 | rodada 2 |
|---|---|---|---|
| entra | `agentNature` | — | Agent: PhysicalAgent, SocialAgent (disjunta, completa) |

### Relacoes

| | Elemento | rodada 1 | rodada 2 |
|---|---|---|---|
| sai | `mediation_Observation_Knowledge` | «mediation» Observation [1..*] -> Knowledge [1..*] | — |
| sai | `mediation_Observation_Agent` | «mediation» Observation [0..*] -> Agent [1] | — |
| sai | `mediation_Observation_Disseminator` | «mediation» Observation [0..*] -> Disseminator [1] | — |
| sai | `mediation_CrudOperation_Agent` | «mediation» CrudOperation [0..*] -> Agent [1] | — |
| sai | `mediation_CrudOperation_CrudView` | «mediation» CrudOperation [0..*] -> CrudView [1] | — |
| sai | `mediation_Extract_Collector` | «mediation» Extract [1..*] -> Collector [1] | — |
| sai | `mediation_Extract_DataSource` | «mediation» Extract [1..*] -> DataSource [1] | — |
| sai | `mediation_Transform_Collector` | «mediation» Transform [1..*] -> Collector [1] | — |
| sai | `mediation_Transform_Processor` | «mediation» Transform [1..*] -> Processor [1] | — |
| sai | `mediation_Load_Processor` | «mediation» Load [1..*] -> Processor [1] | — |
| sai | `mediation_Load_Storer` | «mediation» Load [1..*] -> Storer [1] | — |
| entra | `participation_Agent_Observation` | — | «participation» Agent [1] -> Observation [0..*] |
| entra | `participation_Disseminator_Observation` | — | «participation» Disseminator [1] -> Observation [0..*] |
| entra | `participation_Agent_CrudOperation` | — | «participation» Agent [1] -> CrudOperation [0..*] |
| entra | `participation_CrudView_CrudOperation` | — | «participation» CrudView [1] -> CrudOperation [0..*] |
| entra | `participation_Collector_Extract` | — | «participation» Collector [1] -> Extract [1..*] |
| entra | `participation_DataSource_Extract` | — | «participation» DataSource [1] -> Extract [1..*] |
| entra | `participation_Collector_Transform` | — | «participation» Collector [1] -> Transform [1..*] |
| entra | `participation_Processor_Transform` | — | «participation» Processor [1] -> Transform [1..*] |
| entra | `participation_Processor_Load` | — | «participation» Processor [1] -> Load [1..*] |
| entra | `participation_Storer_Load` | — | «participation» Storer [1] -> Load [1..*] |
| entra | `participational_Extract_EtlProcess` | — | «participational» Extract [1] -> EtlProcess [1] (todo) |
| entra | `participational_Transform_EtlProcess` | — | «participational» Transform [1] -> EtlProcess [1] (todo) |
| entra | `participational_Load_EtlProcess` | — | «participational» Load [1] -> EtlProcess [1] (todo) |
| entra | `creation_Knowledge_Observation` | — | «creation» Knowledge [1..*] -> Observation [1] |

