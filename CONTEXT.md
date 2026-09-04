# OntoMPO

Análise ontológica do Modelo para Observatórios de Projetos, fundamentada na UFO e classificada por
uma teoria de Sistemas de Informação, e o modelo revisado que ela produz. Este glossário fixa os
termos que o artigo, os tickets e os artefatos usam com um sentido próprio.

## Language

### O domínio

**Observatório de projetos**:
Estrutura sociotécnica que coleta, integra e divulga informação sobre um conjunto de projetos
observados, para dar transparência e prestação de contas a partes interessadas externas.
_Avoid_: PMO, escritório de projetos — o PMO gerencia projetos; o observatório observa e divulga.
_Avoid_: monitoramento de projetos — é uma das funções, não o todo.

**Projeto observado**:
O projeto sobre o qual um observatório divulga informação. Não é gerenciado pelo observatório.

**MPO**:
Modelo para Observatórios de Projetos, descrito em linguagem natural na literatura. É o **objeto de
estudo** deste trabalho, não sua contribuição.
_Avoid_: "o modelo", sozinho — ambíguo com a OntoMPO.

**OntoMPO**:
A formalização ontológica do MPO. Neste trabalho, especificamente o modelo **revisado**, resultante
da análise.

### A análise

**Deficiência**:
Uma falha representacional da **formalização publicada** do MPO, exposta pela análise ontológica. São
nove, identificadas de **A1** a **A9**, cada uma com classificação BWW, [[traço]] até o MPO e
correção. Toda deficiência aparece em três lugares — modelo revisado, relatório de verificação e
texto da análise; deficiência órfã é defeito.
_Avoid_: "deficiência do MPO" — o MPO é prosa, e não contém `CrudOperation`, composição de software
por hardware nem hierarquia de `DataManager` sob observatório; esses são estereótipos e relações
escolhidos na formalização. Atribuí-los ao MPO é falsificável por quem abrir a fonte.
_Avoid_: erro, bug — é achado do método, não falha de execução.

**Traço**:
O caminho registrado de cada deficiência até o ponto do MPO que a permitiu. Sem traço, o achado é
conserto de erro próprio; com traço, é evidência de que o MPO **subdetermina sua própria
formalização** — que é a contribuição. Toda deficiência tem um.

**Subdeterminação**:
A propriedade do MPO que o trabalho demonstra: descrito em linguagem natural, ele não fixa a
interpretação em nove pontos, e formalizações aderentes a ele podem divergir entre si. É o que
converte "duas iniciativas podem se declarar aderentes com interpretações incompatíveis" de
afirmação em demonstração. Limite a declarar: n=1 formalizador — demonstra-se que o MPO permite os
desvios, não que outro formalizador os cometeria.

**Achado**:
Uma deficiência apresentada como resultado do trabalho, no par antes/depois com justificativa
ontológica.

**Tipologia BWW**:
O vocabulário da Representation Theory (Wand & Weber) que classifica cada deficiência: *construct
overload*, *construct redundancy*, *construct excess*, *construct deficit*. É o que converte "achamos
defeitos" em classificação por teoria estabelecida de SI.

### Os artefatos

**Baseline**:
O modelo OntoUML reconstruído *exatamente como publicado*, sem nenhuma correção. É a metade "antes"
do antes/depois, e por isso **não se corrige** — arrumá-lo destrói seu valor como termo de comparação.
_Avoid_: modelo original — o original não foi localizado; o baseline é uma reconstrução.

**As-is**:
Sinônimo de baseline, usado nos nomes de arquivo (`ontompo-as-is.*`).

**Rodada**:
Uma iteração de revisão do modelo, em diretório próprio (`rodada-1/`, `rodada-2/`). Rodadas se
acumulam como irmãs; nenhuma substitui a anterior, porque é a comparação entre elas que dá evidência.

**Fonte do modelo**:
Os arquivos JavaScript em `tools/model/` que constroem o modelo. São a ontologia editável; os
`.ontouml.json`, `.ttl` e `.owl` são derivados deles.
_Avoid_: chamar o `.ontouml.json` de "o modelo" — ele é saída.

**Customização (da OWL)**:
O que foi acrescentado à OWL **por cima** do que a transformação gUFO gerou — definições, disjunções,
inversas nomeadas, metadados. São cinco, C1 a C5, cada uma com justificativa escrita em
`artifacts/ontology/owl/customizacoes.md`. É **aditiva por regra**: nenhuma tripla gerada é removida
ou alterada, e é essa contenção que torna a preservação semântica verificável em vez de afirmada. Ver
`docs/adr/0002-customizacao-aditiva-da-owl.md`.
_Avoid_: "correção da OWL" — correção é do modelo e vai numa rodada; customização é da camada OWL.

**Acréscimo**:
O conjunto exato de triplas que a customização soma ao gerado, gravado em
`artifacts/ontology/owl/diff-gerado-customizado.ttl`. Gerado mais acréscimo é, tripla a tripla, o
customizado — e o verificador do ticket 06 confere isso a cada execução.

### A avaliação

**QC (questão de competência)**:
Uma pergunta que a ontologia deve saber responder, verificada por consulta SPARQL sobre instâncias.
São sete. Uma QC legítima exercita o **conhecimento do domínio**; uma que interroga a arquitetura do
modelo — recuperar todo `subClassOf`, listar as `owl:ObjectProperty` — testa a implementação e não
conta.

**Seam**:
Um ponto onde o artefato é exercitado por fora. A **seam primária** é a ontologia instanciada e
consultada por SPARQL, e é a única que valida as afirmações substantivas. As **secundárias** são as
verificações automáticas (plugin OntoUML, OOPS!), que atestam conformidade, não substância. A **de
conformidade** é a chamada do evento tratada como checklist.

**Controle de verificação**:
Execução deliberada de um verificador sobre um modelo com defeitos conhecidos, para provar que ele
dispara. Sem controle positivo, um relatório vazio sobre o modelo revisado não é interpretável — pode
significar "sem problemas" ou "regra que nunca dispara".

**Regra de medição / regra de guarda**:
Os dois tipos de regra dos verificadores estruturais. Uma **regra de medição** dispara sobre o
baseline e mede a distância até o revisado; seu controle positivo é o próprio baseline. Uma **regra
de guarda** vigia um construto que só a revisão introduziu — um evento sem participante, uma
participação invertida — e por isso não tem o que dizer sobre o baseline; seu controle positivo é uma
mutação do modelo revisado. Cobrar de uma regra de guarda que dispare sobre o baseline a tornaria
impossível; dispensar as duas do controle tornaria o zero do revisado ininterpretável.

**Verificador**:
Script que confere a checklist de um ticket, em `tools/verification/`. Um por ticket. Lê o artefato
como terceiro, sem importar do código que o gerou — a duplicação é o teste.

### O veículo

**TP-SI**:
Trilha de Pesquisa em Sistemas de Informação do SBSI, o fórum-alvo. Cobre cinco critérios: Novidade,
Rigor, Relevância, Transparência/Reprodutibilidade e Apresentação.

**Submissão**:
O registro do trabalho no **JEMS3** — título, resumo estruturado, palavras-chave, PDF. Prazos duros e
irreversíveis.

**Depósito**:
A publicação **anônima** dos artefatos em repositório aberto (Zenodo), citada no artigo por link.
Coisa distinta da submissão: outro destino, outro conteúdo, outro requisito.
_Avoid_: usar "submissão" e "depósito" como sinônimos.

**GranDSI-Br**:
A agenda nacional de desafios de pesquisa em SI. O trabalho se alinha ao Desafio 3, "Eco(Sistemas²) de
Informação".

### Método e fundamentação

**UFO**:
Unified Foundational Ontology. **UFO-A** trata de endurantes; **UFO-B**, de eventos e sua participação
temporal; **UFO-C**, de agentes, distinguindo os físicos dos sociais.

**gUFO**:
A implementação leve da UFO em OWL, alvo da transformação oficial que converte o modelo OntoUML.

**DSR**:
Design Science Research, o envelope metodológico. O próprio MPO foi construído sob DSR, então este
trabalho se posiciona como continuação de um ciclo em curso.

**Methontology**:
O método de construção do artefato ontológico, escolhido frente a LOT e NeOn.
