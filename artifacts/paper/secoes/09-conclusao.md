# 9. Conclusão e Trabalhos Futuros

<!--
Superfície de escrita da seção 9. Convenções em `06-ontompo-revisada.md`; conferência em
`tools/verification/verificar_seccoes_ontologia_avaliacao_conclusao.py`.

Aqui vai a contribuição para SI e o trabalho futuro — não o resumo dos resultados, que é da §7, nem
as lições, que são da §8.
-->

Submeter um modelo conceitual de referência do domínio de observatórios de projetos a uma análise
fundamentada na UFO expôs nove deficiências representacionais na formalização publicada desse
modelo, classificadas pela tipologia da Representation Theory e rastreadas até o ponto do texto que
as permitiu, e o artefato revisado foi transformado em OWL, instanciado e interrogado por questões
de competência do domínio.

Para Sistemas de Informação, três coisas ficam. A primeira é uma **base semântica verificável para
auditar aderência**: uma organização que declara seguir o modelo de referência passa a poder mostrar
em que a aderência consiste, porque cada conceito tem definição e compromisso ontológico explícitos,
e a comparação entre duas iniciativas deixa de depender de coincidência terminológica — é o que a
sétima questão de competência demonstra ao medir, e não argumentar, a divergência entre dois
observatórios. A segunda é **rastreabilidade de proveniência para prestação de contas**: com o ciclo
de extração, transformação e carga representado como acontecimento, com participantes e com tempo,
torna-se possível percorrer o caminho do conteúdo divulgado até a origem do dado e dizer quem
respondeu por cada etapa, que é o que a legislação de acesso à informação cobra de quem publica
[L12527]. A terceira é o **procedimento**, reusável fora deste caso: reconstruir a formalização como
linha de base, confrontar cada compromisso formal com o trecho que o originou, exigir de todo achado
o duplo teste — a violação ontológica e a abertura no texto —, classificá-lo por uma tipologia
estabelecida e publicar o antes e o depois como artefatos reexecutáveis.

É o Desafio 3 do II GranDSI-Br, *Eco(Sistemas²) de Informação* [araujo2025grandsi], atendido no
ponto em que ele é mais duro: a integração entre iniciativas depende de um acordo conceitual que,
enquanto o modelo de referência permanecer só em prosa, ninguém consegue auditar.

Quatro direções continuam o trabalho. A primeira é um **estudo comparativo entre observatórios
reais**, que substitua o cenário sintético por iniciativas da literatura e meça a divergência entre
implantações. A segunda é o **alinhamento com ontologias de gerenciamento de projetos**, que ligaria
o projeto observado ao mesmo projeto visto por quem o executa. A terceira ataca o limite de um único
formalizador: **formalizações independentes** do mesmo modelo, por equipes que não se comuniquem,
mostrariam se os pontos de abertura identificados aqui produzem divergência de fato, e não apenas se
a permitem. A quarta é a integração com **modelos de linguagem** como direção, e não como resultado:
uma ontologia com definições e compromissos explícitos é insumo para extração assistida sobre
documentação de observatórios, e o que se oferece a essa agenda é o artefato.