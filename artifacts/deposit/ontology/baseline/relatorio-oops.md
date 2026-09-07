# Relatorio do OOPS! sobre o modelo *as-is*

Ontologia submetida: `ontompo-as-is.ttl`, convertida para RDF/XML e enviada ao servico REST do OOPS! (`https://oops.linkeddata.es/rest`) em 2026-09-04 13:12 UTC. Resposta bruta em `relatorio-oops.xml`; a copia exata submetida, em `ontompo-as-is.oops.owl`.

A declaracao `owl:imports gufo:` foi removida da copia submetida — com ela o servico devolve `unexpected_error`. O recorte tambem e o correto: o que esta sob avaliacao e a ontologia de dominio, nao a gUFO que ela importa.

- Achados: 7
- Por nivel de importancia: Important 3, Minor 3, sem nivel 1

| Codigo | Pitfall | Importancia | Elementos afetados |
|---|---|---|---|
| `P10` | Missing disjointness | Important | 1 |
| `P34` | Untyped class | Important | 13 |
| `P35` | Untyped property | Important | 3 |
| `P08` | Missing annotations | Minor | 63 |
| `P13` | Inverse relationships not explicitly declared | Minor | 21 |
| `P22` | Using different naming conventions in the ontology | Minor | 1 |
| `` | WARNING: the following classes do not have rdf:type owl:Class or equivalent. |  |  |

## Detalhamento

### P10 — Missing disjointness (Important)

The ontology lacks disjoint axioms between classes or between properties that should be defined as disjoint. This pitfall is related with the guidelines provided in [6], [2] and [7].

### P34 — Untyped class (Important)

An ontology element is used as a class without having been explicitly declared as such using the primitives owl:Class or rdfs:Class. This pitfall is related with the common problems listed in [8].

Elementos afetados:

- `FunctionalComplex`
- `Kind`
- `http://purl.org/nemo/gufo#Relator`
- `Role`
- `SubKind`
- `VariableCollection`
- (no anonimo)
- (no anonimo)
- (no anonimo)
- (no anonimo)
- (no anonimo)
- (no anonimo)
- (no anonimo)

### P35 — Untyped property (Important)

An ontology element is used as a property without having been explicitly declared as such using the primitives rdf:Property, owl:ObjectProperty or owl:DatatypeProperty. This pitfall is related with the common problems listed in [8].

Elementos afetados:

- `isCollectionMemberOf`
- `isComponentOf`
- `mediates`

### P08 — Missing annotations (Minor)

This pitfall consists in creating an ontology element and failing to provide human readable annotations attached to it. Consequently, ontology elements lack annotation properties that label them (e.g. rdfs:label, lemon:LexicalEntry, skos:prefLabel or skos:altLabel) or that define them (e.g. rdfs:comment or dc:description). This pitfall is related to the guidelines provided in [5].

Elementos afetados:

- `FunctionalComplex`
- `http://purl.org/nemo/gufo#Relator`
- `VariableCollection`
- `Agent`
- `Collector`
- `Connection`
- `CrudOperation`
- `CrudRepository`
- `CrudView`
- `DataManager`
- `https://example.org/ontompo/as-is#DataSource`
- `Disseminator`
- `Extract`
- `Hardware`
- `Knowledge`
- `Load`
- `Log`
- `Management`
- `Network`
- `Observation`
- `ObservatoryGroup`
- `ObservatoryUser`
- `Operation`
- `Processor`
- `Project`
- `ProjectObservatory`
- `https://example.org/ontompo/as-is#Relator`
- `Service`
- `SocialInteraction`
- `Software`
- `StakeHolder`
- `Storer`
- `System`
- `Transform`
- `View`
- `componentOf_Hardware_Software`
- `mediation_Connection_Hardware`
- `mediation_Connection_Network`
- `mediation_CrudOperation_Agent`
- `mediation_CrudOperation_CrudView`
- `mediation_Extract_Collector`
- `mediation_Extract_DataSource`
- `mediation_Load_Processor`
- `mediation_Load_Storer`
- `mediation_Log_Agent`
- `mediation_Log_Relator`
- `mediation_Management_DataManager`
- `mediation_Management_Project`
- `mediation_Management_View`
- `mediation_Observation_Agent`
- `mediation_Observation_Disseminator`
- `mediation_Observation_Knowledge`
- `mediation_Operation_Hardware`
- `mediation_Operation_Network`
- `mediation_Operation_Service`
- `mediation_Operation_Software`
- `mediation_SocialInteraction_Agent`
- `mediation_SocialInteraction_Relator`
- `mediation_Transform_Collector`
- `mediation_Transform_Processor`
- `memberOf_ObservatoryGroup_ObservatoryUser`
- `memberOf_ObservatoryGroup_StakeHolder`
- `memberOf_ObservatoryGroup_System`

### P13 — Inverse relationships not explicitly declared (Minor)

This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.

### P22 — Using different naming conventions in the ontology (Minor)

The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as &quot;-&quot; or &quot;_&quot;) . Some notions about naming conventions are provided in [2].

Elementos afetados:

- `There are elements following different naming conventions as for example: https://example.org/ontompo/as-is#mediation_Transform_Collector https://example.org/ontompo/as-is#DataSource`

###  — WARNING: the following classes do not have rdf:type owl:Class or equivalent. ()



Elementos afetados:

- `FunctionalComplex`
- `http://purl.org/nemo/gufo#Relator`
- `VariableCollection`

