# Pacote de registro no JEMS3 — SBSI 2027, Trilha de Pesquisa em SI

Material pronto para o preenchimento do formulário de registro no JEMS3. Cada campo abaixo é
copiado tal como está para o campo correspondente do formulário; nada precisa ser reescrito.

**Prazo de registro:** 08/09/2026. **Congelamento:** depois de 14/09/2026 não é possível alterar
título, resumo, tópicos ou autoria, nem retirar o artigo do processo. O que for registrado aqui vale
para todo o ciclo, incluindo o rebuttal.

**A submissão em si é ação humana.** Este arquivo é o insumo; o registro no JEMS3 é feito pelo autor.

Conferência automática: `python scripts/verificar_pacote_jems3.py`

---

## 1. Título (campo *Title*)

<!-- campo: titulo -->
```text
OntoMPO: Ontological Analysis and Refinement of the Model for Project Observatories
```

O título anuncia a contribuição reposicionada: o que a análise ontológica revelou sobre o MPO e o
modelo revisado dela resultante — não a formalização do MPO.

---

## 2. Resumo estruturado (campo *Abstract*)

Sete labels nomeados, em inglês, dentro do limite de 300 palavras.

<!-- campo: resumo -->
```text
Research Context. Project observatories are organizational units, processes or information systems that continuously observe projects, centralizing and disseminating information to sustain transparency and accountability. The Model for Project Observatories (MPO), the reference conceptual model of this domain, organizes 61 concepts in three levels and is described in natural language.

Scientific and/or Practical Problem. Natural-language reference models carry representational deficiencies invisible to those who apply them. Two initiatives may declare adherence to MPO while adopting semantically incompatible interpretations, so adherence is unverifiable and comparison between observatories rests on terminological coincidence.

Proposed Solution and/or Analysis. MPO is submitted to an ontological analysis grounded in the Unified Foundational Ontology; the resulting revised model is delivered as the artifact. The contribution is that analysis and the revised model, not the formalization of MPO as published.

Related IS Theory. Representation Theory (Wand & Weber) supplies the typology used to classify every finding: construct overload, redundancy, excess and deficit.

Research Method. Design Science Research frames the work, continuing the cycle that produced MPO; Methontology guides artifact construction. The revised OntoUML model is transformed into OWL through gUFO, instantiated over an observatory scenario from the literature and interrogated by seven domain competency questions in SPARQL, with syntactic and pitfall verification before and after revision.

Summary of Results. The analysis exposed nine representational deficiencies: construct overload, invalid mereological relations, semantic collapse and missing event and agent microtheories, each classified and corrected. Every competency question returned non-empty, semantically correct answers, and automated verification reports improved between runs.

Contributions and Impact to IS area. The work delivers a verifiable semantic basis for auditing adherence to MPO, provenance traceability for accountability, and a reusable procedure for auditing natural-language reference models, addressing semantic interoperability among information ecosystems, a named challenge of the Brazilian IS agenda.
```

Notas de redação, para o caso de o campo precisar ser reaberto antes de 14/09:

- *Proposed Solution and/or Analysis* declara explicitamente a análise ontológica e o modelo revisado
  como contribuição, e nega a formalização do MPO — é a virada que responde à rejeição no ONTOBRAS.
- *Related IS Theory* nomeia Representation Theory (Wand & Weber) e a usa operacionalmente, como
  tipologia de classificação, e não como citação decorativa.
- *Summary of Results* quantifica os achados: nove deficiências representacionais.
- *Summary of Results* fala no passado sobre resultados que os tickets 06 a 08 ainda vão produzir.
  É o normal em registro antecipado, mas vira compromisso: se alguma questão de competência voltar
  vazia ou os relatórios não melhorarem, o resumo congelado passa a divergir do PDF. Tratar como
  critério de aceite dos tickets 07 e 08.
- Sem nome de autor, instituição, financiador, link ou ferramenta que identifique. O cenário de
  instanciação aparece em terceira pessoa, como "an observatory scenario from the literature".

---

## 3. Palavras-chave (campo *Keywords*)

<!-- campo: palavras-chave -->
```text
Project Observatory; Ontological Analysis; Representation Theory; Conceptual Modeling; Design Science Research
```

---

## 4. Tópicos de interesse (campo *Topics*)

Quatro tópicos, em ordem de aderência decrescente.

<!-- campo: topicos -->
```text
1. Transparência e accountability em SI
2. SI para gestão de dados, informação e conhecimento
3. Paradigmas, modelagem, design, engenharia e avaliação de SI
4. SI organizacionais
```

Por que estes: o primeiro é o problema organizacional que o trabalho endereça; o segundo, o objeto
do observatório; o terceiro, a natureza do artefato e do método; o quarto, o contexto de aplicação.

---

## 5. Conferência antes de submeter

- [ ] Título colado no JEMS3 exatamente como acima
- [ ] Resumo colado com os sete labels visíveis; se o formulário aceitar apenas texto corrido, manter
      os labels no início de cada bloco e separar por parágrafo
- [ ] Contagem de palavras do resumo dentro de 300 (verificada pelo script)
- [ ] Palavras-chave preenchidas
- [ ] Os quatro tópicos marcados
- [ ] Nenhum campo do formulário com identificação além dos campos de autoria próprios do JEMS3
