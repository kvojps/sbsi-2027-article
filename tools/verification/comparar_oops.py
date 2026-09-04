#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compara os dois relatorios do OOPS!, o do baseline e o da OWL customizada.

Uso: python tools/verification/comparar_oops.py [xml-antes] [xml-depois] [saida]

Le as duas respostas brutas do servico — nao os markdowns derivados delas — e
grava `comparacao-oops.md` em `artifacts/ontology/owl/`.

A comparacao vem em **duas leituras**, e as duas sao necessarias:

  *total*     todos os elementos que o OOPS! aponta, como ele os aponta;
  *dominio*   so os elementos no namespace da propria OntoMPO.

A segunda existe porque boa parte do que o OOPS! aponta nao e sobre o modelo. A
copia submetida tem o `owl:imports` removido — com ele o servico devolve
`unexpected_error` —, entao os termos que a gUFO empresta chegam la sem a
ontologia que os define, e os nos anonimos das restricoes nunca tem tipo
proprio. `evidencias-A1-A9.md` ja separava esses do que e achado, sobre o
baseline; aqui a separacao vira contagem.

Sai com codigo 1 se algum dos relatorios nao existir ou nao for uma resposta de
verdade.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from rodar_oops import ORDEM_IMPORTANCIA, extrair_pitfalls  # noqa: E402

ANTES_PADRAO = Path("artifacts/ontology/baseline/relatorio-oops.xml")
DEPOIS_PADRAO = Path("artifacts/ontology/owl/relatorio-oops.xml")
SAIDA_PADRAO = Path("artifacts/ontology/owl")

GUFO = "http://purl.org/nemo/gufo#"
DOMINIO = "https://example.org/ontompo/"

# A leitura de cada pitfall: o que ele significa aqui, e o que a customizacao
# fez com ele. Um codigo que aparecer em qualquer dos dois relatorios e nao
# estiver aqui faz a execucao falhar — achado orfao e defeito.
LEITURAS = {
    "P04": (
        "gUFO",
        "Elementos sem ligação com o resto. São as classes da gUFO que a **C1** declara "
        "localmente: o artefato as usa e as tipa, mas a taxonomia que as conecta fica na gUFO, "
        "onde ela deve ficar. Aparece no revisado porque antes esses termos sequer estavam "
        "declarados.",
    ),
    "P08": (
        "misto",
        "Elementos sem anotação legível — o achado **B3**. A **C2** devolve definição e rótulo "
        "preferido a todas as 44 classes e 34 propriedades do domínio. O resto são os termos "
        "que a gUFO empresta, que chegam ao serviço sem a ontologia que os define.",
    ),
    "P10": (
        "domínio",
        "Ausência de axiomas de disjunção — o achado **B4**, fechado pela **C3**.",
    ),
    "P11": (
        "gUFO",
        "Propriedade sem domínio ou alcance. É `gufo:isDerivedFrom`, cujo domínio, na gUFO, é uma "
        "expressão de classe anônima. A **C1** copia domínio e alcance quando são um termo "
        "nomeado; copiar uma expressão anônima seria trazer a gUFO para dentro do artefato, e "
        "deixar um `rdfs:domain` vazio seria pior que não declarar.",
    ),
    "P13": (
        "misto",
        "Relação sem inversa declarada. A **C4** nomeia a inversa das 34 propriedades do domínio "
        "e declara o `owl:inverseOf` nos dois sentidos; o que sobra são as propriedades da gUFO.",
    ),
    "P22": (
        "domínio",
        "Convenção de nome — o achado **B5**. **Deliberadamente não fechado**: renomear os IRIs "
        "quebraria a correspondência entre cada elemento OWL e o elemento OntoUML que o gerou, "
        "que é a garantia pela qual se usa a transformação oficial. A **C2** endereça B5 por "
        "`skos:prefLabel`, que é o que se lê.",
    ),
    "P30": (
        "heurística",
        "Classes equivalentes não declaradas. O serviço não lista elemento afetado, e a "
        "heurística procura conceitos duplicados entre ontologias reusadas. Aparece depois de a "
        "**C1** declarar os termos da gUFO ao lado dos do domínio — é consequência de as duas "
        "passarem a conviver no mesmo arquivo, não de duplicação no modelo.",
    ),
    "P34": (
        "misto",
        "Elemento usado como classe sem declaração. No baseline eram seis termos da gUFO mais "
        "sete nós anônimos; a **C1** fecha os seis. O que sobra são só nós anônimos — as "
        "restrições de cardinalidade que a transformação gUFO emite, que não têm IRI para "
        "declarar. Cresce porque a rodada 2 tem mais restrições que o *as-is*, não porque piorou.",
    ),
    "P35": (
        "gUFO",
        "Propriedade usada sem declaração. Eram três termos da gUFO; a **C1** os declara.",
    ),
    "": (
        "gUFO",
        "*Warning* do serviço, que repete em outra forma o que P34 diz sobre os termos da gUFO. "
        "Some junto com eles.",
    ),
}


def classificar(elemento: str) -> str:
    if elemento.startswith(DOMINIO):
        return "domínio"
    if elemento.startswith(GUFO):
        return "gUFO"
    if "#" in elemento or "/" in elemento:
        return "externo"
    return "anônimo"


def _quantidade(achado: dict) -> int:
    """O numero que o servico declara; cai para o tamanho da lista se faltar."""
    try:
        return int(achado["quantidade"])
    except (TypeError, ValueError):
        return len(achado["elementos"])


def _por_codigo(achados: list[dict]) -> dict[str, dict]:
    tabela = {}
    for achado in achados:
        elementos = achado["elementos"]
        # `listou` so vale quando ha IRI para classificar. Alguns pitfalls vem
        # sem elemento nenhum (P10, P13, P30) e o P22 vem com uma frase em prosa
        # no lugar do elemento — nos tres casos a coluna de dominio seria um
        # zero que parece resultado e nao e.
        com_iri = [e for e in elementos if classificar(e) != "anônimo"]
        tabela[achado["codigo"]] = {
            "nome": achado["nome"],
            "importancia": achado["importancia"],
            "total": _quantidade(achado),
            "dominio": sum(1 for e in com_iri if classificar(e) == "domínio"),
            "listou": bool(com_iri),
        }
    return tabela


def relatorio(antes: dict[str, dict], depois: dict[str, dict]) -> str:
    codigos = sorted(
        set(antes) | set(depois),
        key=lambda c: (
            ORDEM_IMPORTANCIA.get(
                (antes.get(c) or depois.get(c))["importancia"],
                9,
            ),
            c,
        ),
    )
    linhas = [
        "# OOPS!: o baseline contra a OWL revisada e customizada",
        "",
        "Derivado das duas respostas brutas do serviço a cada execução de "
        "`tools/verification/comparar_oops.py`. O *antes* é "
        "`../baseline/relatorio-oops.xml`, sobre o modelo *as-is*; o *depois* é "
        "`relatorio-oops.xml`, sobre `ontompo.ttl`.",
        "",
        "As duas execuções passam pelo mesmo caminho de código, `rodar_oops.py`, e submetem a "
        "mesma coisa: a ontologia em RDF/XML, sem o `owl:imports`. É essa igualdade que torna os "
        "números comparáveis.",
        "",
        "## Contagem",
        "",
        "| Código | *Pitfall* | Importância | antes | depois | antes (domínio) | depois (domínio) |",
        "|---|---|---|---|---|---|---|",
    ]
    for codigo in codigos:
        a = antes.get(codigo)
        d = depois.get(codigo)
        referencia = a or d
        rotulo = f"`{codigo}`" if codigo else "*warning*"

        def celula(dados, chave):
            if dados is None:
                return "—"
            if chave == "dominio" and not dados["listou"]:
                return "n/d"
            return str(dados[chave])

        linhas.append(
            f"| {rotulo} | {referencia['nome']} | {referencia['importancia'] or '—'} | "
            f"{celula(a, 'total')} | {celula(d, 'total')} | "
            f"{celula(a, 'dominio')} | {celula(d, 'dominio')} |"
        )
    total_antes = sum(v["total"] for v in antes.values())
    total_depois = sum(v["total"] for v in depois.values())
    dominio_antes = sum(v["dominio"] for v in antes.values())
    dominio_depois = sum(v["dominio"] for v in depois.values())
    linhas.append(
        f"| | **total** | | **{total_antes}** | **{total_depois}** | "
        f"**{dominio_antes}** | **{dominio_depois}** |"
    )
    linhas.append("")
    linhas.append(
        "`n/d` onde o serviço devolve a contagem sem listar os elementos, e por isso não se pode "
        "separar o que é do domínio. `—` onde o *pitfall* não aparece naquele relatório."
    )
    linhas.append("")
    linhas.append("## Como ler cada linha")
    linhas.append("")
    for codigo in codigos:
        classe, texto = LEITURAS[codigo]
        rotulo = f"`{codigo}`" if codigo else "*warning*"
        linhas.append(f"- **{rotulo}** ({classe}) — {texto}")
    linhas.append("")
    linhas.append("## O que os números dizem")
    linhas.append("")
    linhas.append(
        "Na leitura *domínio*, que é a que fala do modelo, os elementos apontados caem de "
        f"**{dominio_antes}** para **{dominio_depois}**. Os 60 do baseline eram todos de `P08`, "
        "as definições ausentes; nenhum elemento da OntoMPO sobrou apontado."
    )
    linhas.append("")
    linhas.append(
        "Dois *pitfalls* ficam de fora dessa contagem porque o serviço não lista elementos para "
        "eles. Um é `P22`, o único que a customização decidiu deliberadamente não fechar, com a "
        "razão escrita em `customizacoes.md`. O outro é `P13`, que cai de 21 para 7 — e sete é "
        "exatamente o número de propriedades da gUFO que a **C1** declara no arquivo, o que "
        "sustenta a leitura de que o que sobra é delas e não do domínio. É inferência pela "
        "contagem, não elemento listado, e vale dito assim."
    )
    linhas.append("")
    linhas.append(
        "Na leitura *total* a queda é menor, e a diferença não é ruído: a **C1** declara no "
        "arquivo os termos que a gUFO empresta, e um termo declarado passa a ser um elemento que "
        "o OOPS! avalia — sem anotação própria (P08), sem ligação com o resto (P04), sem domínio "
        "quando o da gUFO é anônimo (P11). São termos da ontologia de fundamentação, avaliados "
        "fora dela. Trocar essa avaliação por uma melhor exigiria inlinear a gUFO no artefato, "
        "que é precisamente o que `owl:imports` existe para evitar."
    )
    linhas.append("")
    linhas.append(
        "O `P34` cresce de 13 para 16 pelo mesmo tipo de razão, na direção oposta: some a metade "
        "nomeada, que era da gUFO, e sobra só a anônima — as restrições de cardinalidade, que a "
        "rodada 2 tem em maior número que o *as-is* porque tem mais participações."
    )
    linhas.append("")
    return "\n".join(linhas) + "\n"


def main() -> int:
    antes_xml = Path(sys.argv[1]) if len(sys.argv) > 1 else ANTES_PADRAO
    depois_xml = Path(sys.argv[2]) if len(sys.argv) > 2 else DEPOIS_PADRAO
    saida = Path(sys.argv[3]) if len(sys.argv) > 3 else SAIDA_PADRAO

    for caminho in (antes_xml, depois_xml):
        if not caminho.exists():
            print(f"ERRO: {caminho} nao existe. Rode antes: python tools/verification/rodar_oops.py")
            return 1
        if "unexpected_error" in caminho.read_text(encoding="utf-8"):
            print(f"ERRO: {caminho} guarda um erro do servico, nao um relatorio")
            return 1

    antes = _por_codigo(extrair_pitfalls(antes_xml.read_text(encoding="utf-8")))
    depois = _por_codigo(extrair_pitfalls(depois_xml.read_text(encoding="utf-8")))

    orfaos = sorted((set(antes) | set(depois)) - set(LEITURAS))
    if orfaos:
        print(f"ERRO: pitfall sem leitura em LEITURAS: {orfaos}")
        return 1

    saida.mkdir(parents=True, exist_ok=True)
    (saida / "comparacao-oops.md").write_text(relatorio(antes, depois), encoding="utf-8")

    print(f"comparacao -> {saida / 'comparacao-oops.md'}")
    for codigo in sorted(set(antes) | set(depois)):
        a = antes.get(codigo, {}).get("total", 0)
        d = depois.get(codigo, {}).get("total", 0)
        print(f"  {codigo or '(warning)':6} {a:3} -> {d:3}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
