# Relatorio do OOPS! sobre a OWL customizada do modelo revisado

Ontologia submetida: `ontompo.ttl`, convertida para RDF/XML e enviada ao servico REST do OOPS! (`https://oops.linkeddata.es/rest`) em 2026-09-04 19:20 UTC. Resposta bruta em `relatorio-oops.xml`; a copia exata submetida, em `ontompo.oops.owl`.

A declaracao `owl:imports gufo:` foi removida da copia submetida — com ela o servico devolve `unexpected_error`. O recorte tambem e o correto: o que esta sob avaliacao e a ontologia de dominio, nao a gUFO que ela importa.

- Achados: 7
- Por nivel de importancia: Important 3, Minor 4

| Codigo | Pitfall | Importancia | Elementos afetados |
|---|---|---|---|
| `P11` | Missing domain or range in properties | Important | 1 |
| `P30` | Equivalent classes not explicitly declared | Important | 1 |
| `P34` | Untyped class | Important | 16 |
| `P04` | Creating unconnected ontology elements | Minor | 8 |
| `P08` | Missing annotations | Minor | 22 |
| `P13` | Inverse relationships not explicitly declared | Minor | 7 |
| `P22` | Using different naming conventions in the ontology | Minor | 1 |

## Detalhamento

### P11 — Missing domain or range in properties (Important)

Object and/or datatype properties without domain or range (or none of them) are included in the ontology.

Elementos afetados:

- `isDerivedFrom`

### P30 — Equivalent classes not explicitly declared (Important)

This pitfall consists in missing the definition of equivalent classes (owl:equivalentClass) in case of duplicated concepts. When an ontology reuses terms from other ontologies, classes that have the same meaning should be defined as equivalent in order to benefit the interoperability between both ontologies.

### P34 — Untyped class (Important)

An ontology element is used as a class without having been explicitly declared as such using the primitives owl:Class or rdfs:Class. This pitfall is related with the common problems listed in [8].

Elementos afetados:

- (no anonimo)
- (no anonimo)
- (no anonimo)
- (no anonimo)
- (no anonimo)
- (no anonimo)
- (no anonimo)
- (no anonimo)
- (no anonimo)
- (no anonimo)
- (no anonimo)
- (no anonimo)
- (no anonimo)
- (no anonimo)
- (no anonimo)
- (no anonimo)

### P04 — Creating unconnected ontology elements (Minor)

Ontology elements (classes, object properties and datatype properties) are created isolated, with no relation to the rest of the ontology.

Elementos afetados:

- `Category`
- `http://purl.org/nemo/gufo#EventType`
- `Kind`
- `MaterialRelationshipType`
- `Role`
- `RoleMixin`
- `SubKind`
- `VariableCollection`

### P08 — Missing annotations (Minor)

This pitfall consists in creating an ontology element and failing to provide human readable annotations attached to it. Consequently, ontology elements lack annotation properties that label them (e.g. rdfs:label, lemon:LexicalEntry, skos:prefLabel or skos:altLabel) or that define them (e.g. rdfs:comment or dc:description). This pitfall is related to the guidelines provided in [5].

Elementos afetados:

- `Category`
- `Collection`
- `Endurant`
- `EndurantType`
- `Event`
- `http://purl.org/nemo/gufo#EventType`
- `FunctionalComplex`
- `Kind`
- `MaterialRelationshipType`
- `Object`
- `Relator`
- `Role`
- `RoleMixin`
- `SubKind`
- `VariableCollection`
- `isCollectionMemberOf`
- `isComponentOf`
- `isDerivedFrom`
- `isEventProperPartOf`
- `mediates`
- `participatedIn`
- `wasCreatedIn`

### P13 — Inverse relationships not explicitly declared (Minor)

This pitfall appears when any relationship (except for those that are defined as symmetric properties using owl:SymmetricProperty) does not have an inverse relationship (owl:inverseOf) defined within the ontology.

### P22 — Using different naming conventions in the ontology (Minor)

The ontology elements are not named following the same convention (for example CamelCase or use of delimiters as &quot;-&quot; or &quot;_&quot;) . Some notions about naming conventions are provided in [2].

Elementos afetados:

- `There are elements following different naming conventions as for example: https://example.org/ontompo/rodada-2#mediatedBy_Reporter_SocialInteraction http://purl.org/nemo/gufo#EventType`

