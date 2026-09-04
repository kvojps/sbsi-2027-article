# Pacote de registro no JEMS3 — SBSI 2027, Trilha de Pesquisa em SI

Material pronto para o preenchimento do formulário de registro no JEMS3. Cada campo abaixo é
copiado tal como está para o campo correspondente do formulário; nada precisa ser reescrito.

**Prazo de registro:** 08/09/2026. **Congelamento:** depois de 14/09/2026 não é possível alterar
título, resumo, tópicos ou autoria, nem retirar o artigo do processo. O que for registrado aqui vale
para todo o ciclo, incluindo o rebuttal.

**A submissão em si é ação humana.** Este arquivo é o insumo; o registro no JEMS3 é feito pelo autor.

Conferência automática: `python tools/verification/verificar_pacote_jems3.py`

---

## 1. Título (campo *Title*)

<!-- campo: titulo -->
```text
OntoMPO: Ontological Analysis and Refinement of the Model for Project Observatories
```

O título anuncia a contribuição reposicionada: o que a análise ontológica revelou sobre o MPO e o
modelo revisado dela resultante — não a formalização do MPO. A análise é *do* MPO, conduzida
**através** da formalização publicada; o título continua correto sob esse enquadramento.

---

## 2. Resumo estruturado (campo *Abstract*)

Sete labels nomeados, em inglês, dentro do limite de 300 palavras.

<!-- campo: resumo -->
```text
Research Context. Project observatories observe a set of projects and disseminate information about them to sustain transparency and accountability. The Model for Project Observatories (MPO), the reference conceptual model of this domain, is described in natural language and has been formalized in OntoUML and OWL by published work.

Scientific and/or Practical Problem. Natural-language reference models underdetermine their own formalization. Two initiatives may declare adherence to MPO while adopting semantically incompatible interpretations, so adherence is unverifiable and comparison between observatories rests on terminological coincidence.

Proposed Solution and/or Analysis. MPO is submitted to an ontological analysis grounded in the Unified Foundational Ontology and conducted through its published formalization: each deficiency is located in that artifact and traced to where MPO leaves the interpretation open. The revised model is the contribution, not the formalization of MPO.

Related IS Theory. Representation Theory (Wand & Weber) supplies the typology that classifies every finding: construct overload, redundancy, excess and deficit.

Research Method. Design Science Research frames the work, continuing the cycle that produced MPO; Methontology guides construction. The published model is reconstructed as a baseline, revised, transformed into OWL through gUFO, instantiated over an observatory scenario and interrogated by seven domain competency questions in SPARQL, verified before and after revision.

Summary of Results. Nine representational deficiencies were exposed in the published formalization, spanning construct overload, invalid mereology, semantic collapse and missing event and agent microtheories, each classified, traced to MPO and corrected. Every competency question returned correct answers, and verification reports improved between runs.

Contributions and Impact to IS area. The work delivers a verifiable basis for auditing adherence to MPO, provenance traceability for accountability, and a reusable procedure for auditing natural-language reference models, addressing semantic interoperability among information ecosystems, a named challenge of the Brazilian IS agenda.
```

Notas de redação, para o caso de o campo precisar ser reaberto antes de 14/09:

- **Onde estão as deficiências.** As nove são falhas da *formalização publicada*, não do MPO em
  linguagem natural. O MPO descreve três dimensões, subdimensões e elementos em prosa; ele não
  contém `CrudOperation`, não declara software como composto de hardware nem hierarquiza
  `DataManager` sob observatório. Esses são estereótipos e relações escolhidos na etapa de
  formalização — a dissertação os enuncia como decisão de modelagem. Atribuir as nove ao MPO é
  falsificável por qualquer revisor que abra a fonte do MPO e não as encontre lá.
- **O que sustenta a contribuição, então.** Não é "o MPO é defeituoso": é que o MPO **subdetermina
  sua própria formalização**. Uma formalização sistemática, seguindo Methontology, produziu nove
  desvios, e cada um cai num ponto em que o MPO não fixa a interpretação. Isso converte o campo
  *Problem* — duas iniciativas aderentes com interpretações incompatíveis — de afirmação em
  demonstração, porque a demonstração é uma tentativa real de formalizar.
- **Cada deficiência precisa do seu traço até o MPO.** Sem esse traço, o achado é conserto de erro
  próprio; com ele, é evidência sobre o modelo de referência. É critério de aceite do ticket 10.
- **Limitação a declarar no artigo.** n=1: um formalizador. Não se demonstra que outro cometeria os
  mesmos desvios, apenas que o MPO os permite.
- **Objeto de análise em terceira pessoa.** A formalização analisada é trabalho publicado, citado
  como de terceiros — o que a revisão duplamente anônima exige de qualquer forma.
- *Proposed Solution and/or Analysis* declara explicitamente a análise ontológica e o modelo revisado
  como contribuição, e nega a formalização do MPO — é a virada que responde à rejeição no ONTOBRAS.
- *Related IS Theory* nomeia Representation Theory (Wand & Weber) e a usa operacionalmente, como
  tipologia de classificação, e não como citação decorativa.
- *Summary of Results* quantifica os achados: nove deficiências representacionais, localizadas na
  formalização publicada.
- *Summary of Results* fala no passado sobre resultados que os tickets 06 a 08 ainda vão produzir.
  É o normal em registro antecipado, mas vira compromisso: se alguma questão de competência voltar
  vazia ou os relatórios não melhorarem, o resumo congelado passa a divergir do PDF. Tratar como
  critério de aceite dos tickets 07 e 08.
- Sem nome de autor, instituição, financiador, link ou ferramenta que identifique. O cenário de
  instanciação aparece em terceira pessoa, como "an observatory scenario".

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
