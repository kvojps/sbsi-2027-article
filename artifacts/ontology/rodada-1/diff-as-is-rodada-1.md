# Diff estrutural: *as-is* -> rodada 1

Derivado dos dois modelos a cada execucao de `tools/generation/diff-modelos.js`. E a materia-prima dos pares antes/depois; a leitura ontologica de cada um esta em `../correcoes-rodada-1.md`.

## Contagens

| | *as-is* | rodada 1 |
|---|---|---|
| classes | 32 | 38 |
| generalizacoes | 13 | 17 |
| conjuntos de generalizacao | 0 | 1 |
| relacoes | 28 | 32 |

## Mudancas

### Classes

| | Elemento | *as-is* | rodada 1 |
|---|---|---|---|
| sai | `Relator` | «role» | — |
| sai | `Management` | «relator» | — |
| sai | `Operation` | «relator» | — |
| entra | `CreateOperation` | — | «subkind» |
| entra | `ReadOperation` | — | «subkind» |
| entra | `UpdateOperation` | — | «subkind» |
| entra | `DeleteOperation` | — | «subkind» |
| entra | `Reporter` | — | «role» |
| entra | `ProjectDataManagement` | — | «relator» |
| entra | `ViewProvision` | — | «relator» |
| entra | `SoftwareExecution` | — | «relator» |
| entra | `ServiceProvision` | — | «relator» |

### Generalizacoes

| | Elemento | *as-is* | rodada 1 |
|---|---|---|---|
| sai | `Relator -> View` | Relator especializa View | — |
| sai | `DataManager -> ProjectObservatory` | DataManager especializa ProjectObservatory | — |
| sai | `View -> ProjectObservatory` | View especializa ProjectObservatory | — |
| entra | `CreateOperation -> CrudOperation` | — | CreateOperation especializa CrudOperation |
| entra | `ReadOperation -> CrudOperation` | — | ReadOperation especializa CrudOperation |
| entra | `UpdateOperation -> CrudOperation` | — | UpdateOperation especializa CrudOperation |
| entra | `DeleteOperation -> CrudOperation` | — | DeleteOperation especializa CrudOperation |
| entra | `Reporter -> View` | — | Reporter especializa View |
| entra | `DataManager -> Software` | — | DataManager especializa Software |
| entra | `View -> Software` | — | View especializa Software |

### Conjuntos de generalizacao

| | Elemento | *as-is* | rodada 1 |
|---|---|---|---|
| entra | `crudOperationType` | — | CrudOperation: CreateOperation, ReadOperation, UpdateOperation, DeleteOperation (disjunta, completa) |

### Relacoes

| | Elemento | *as-is* | rodada 1 |
|---|---|---|---|
| sai | `memberOf_ObservatoryGroup_ObservatoryUser` | «memberOf» ObservatoryGroup [1] -> ObservatoryUser [0..*] (todo) | — |
| sai | `memberOf_ObservatoryGroup_StakeHolder` | «memberOf» ObservatoryGroup [1] -> StakeHolder [0..*] (todo) | — |
| sai | `componentOf_Hardware_Software` | «componentOf» Hardware [1..*] -> Software [1..*] (todo) | — |
| sai | `memberOf_ObservatoryGroup_System` | «memberOf» ObservatoryGroup [1] -> System [0..*] | — |
| sai | `mediation_SocialInteraction_Relator` | «mediation» SocialInteraction [0..*] -> Relator [1] | — |
| sai | `mediation_Log_Relator` | «mediation» Log [0..*] -> Relator [1] | — |
| sai | `mediation_Management_Project` | «mediation» Management [0..*] -> Project [1] | — |
| sai | `mediation_Management_DataManager` | «mediation» Management [0..*] -> DataManager [1] | — |
| sai | `mediation_Management_View` | «mediation» Management [0..*] -> View [1] | — |
| sai | `mediation_Operation_Software` | «mediation» Operation [0..*] -> Software [0..*] | — |
| sai | `mediation_Operation_Service` | «mediation» Operation [0..*] -> Service [1] | — |
| sai | `mediation_Operation_Hardware` | «mediation» Operation [0..*] -> Hardware [0..*] | — |
| sai | `mediation_Operation_Network` | «mediation» Operation [0..*] -> Network [0..*] | — |
| entra | `memberOf_ObservatoryUser_ObservatoryGroup` | — | «memberOf» ObservatoryUser [1..*] -> ObservatoryGroup [1] (todo) |
| entra | `memberOf_StakeHolder_ObservatoryGroup` | — | «memberOf» StakeHolder [1..*] -> ObservatoryGroup [1] (todo) |
| entra | `memberOf_System_ObservatoryGroup` | — | «memberOf» System [1..*] -> ObservatoryGroup [1] (todo) |
| entra | `componentOf_DataManager_ProjectObservatory` | — | «componentOf» DataManager [1..*] -> ProjectObservatory [1] (todo) |
| entra | `componentOf_View_ProjectObservatory` | — | «componentOf» View [1..*] -> ProjectObservatory [1] (todo) |
| entra | `mediation_SocialInteraction_Reporter` | — | «mediation» SocialInteraction [0..*] -> Reporter [1] |
| entra | `mediation_Log_Reporter` | — | «mediation» Log [0..*] -> Reporter [1] |
| entra | `mediation_ProjectDataManagement_DataManager` | — | «mediation» ProjectDataManagement [0..*] -> DataManager [1] |
| entra | `mediation_ProjectDataManagement_Project` | — | «mediation» ProjectDataManagement [0..*] -> Project [1] |
| entra | `mediation_ViewProvision_DataManager` | — | «mediation» ViewProvision [0..*] -> DataManager [1] |
| entra | `mediation_ViewProvision_View` | — | «mediation» ViewProvision [0..*] -> View [1] |
| entra | `mediation_SoftwareExecution_Software` | — | «mediation» SoftwareExecution [1..*] -> Software [1] |
| entra | `mediation_SoftwareExecution_Hardware` | — | «mediation» SoftwareExecution [0..*] -> Hardware [1] |
| entra | `mediation_ServiceProvision_Service` | — | «mediation» ServiceProvision [1..*] -> Service [1] |
| entra | `mediation_ServiceProvision_Software` | — | «mediation» ServiceProvision [0..*] -> Software [1] |
| entra | `material_Software_Hardware` | — | «material» Software [0..*] -> Hardware [1..*] |
| entra | `derivation_Software_Hardware_SoftwareExecution` | — | «derivation» material_Software_Hardware [0..*] -> SoftwareExecution [0..*] |

