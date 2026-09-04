#!/usr/bin/env python3
"""Verifica a linha de base ontologica contra a checklist do ticket 03.

Uso: python scripts/verificar_baseline.py [diretorio-ontologia]

Confere sete coisas, na ordem da checklist do ticket:

  1. o modelo *as-is* existe no formato de intercambio do plugin OntoUML;
  2. o modelo reconstruido corresponde ao publicado — mesmas classes, mesmos
     estereotipos, mesmas generalizacoes e mesmas relacoes com as mesmas
     multiplicidades e extremidades de agregacao, defeitos incluidos;
  3. a OWL de baseline foi gerada a partir dele;
  4. o relatorio do verificador OntoUML esta em arquivo, e o controle que o
     torna interpretavel tambem;
  5. o relatorio do OOPS! esta em arquivo e e uma resposta de verdade;
  6. cada uma das nove deficiencias A1-A9 tem seccao propria no documento de
     evidencias **e** esta de fato presente na estrutura do modelo;
  7. o que as ferramentas apontaram alem de A1-A9 ficou registrado.

A tabela de conferencia da verificacao 2 e uma **segunda leitura independente**
dos diagramas, transcrita aqui a partir das mesmas imagens que serviram de
fonte para `scripts/ontouml/modelo-as-is.js`. A duplicacao e o teste: se as
duas leituras divergirem, uma das duas esta errada e a verificacao reprova.

Sai com codigo 1 se qualquer verificacao falhar.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import rdflib
except ImportError:  # pragma: no cover - dependencia ausente
    print("ERRO: rdflib ausente. Rode: pip install rdflib")
    sys.exit(1)

DIRETORIO_PADRAO = Path("ontologia")

GUFO = "http://purl.org/nemo/gufo#"

# --------------------------------------------------------------------------
# Segunda leitura dos diagramas. NAO importar de scripts/ontouml/: o valor
# desta tabela esta em ela ter sido transcrita de novo, das imagens.
# --------------------------------------------------------------------------

CLASSES_ESPERADAS = {
    "ObservatoryGroup": "collective",
    "ObservatoryUser": "role",
    "StakeHolder": "role",
    "System": "role",
    "Agent": "kind",
    "Knowledge": "kind",
    "Observation": "relator",
    "SocialInteraction": "relator",
    "Log": "relator",
    "CrudOperation": "relator",
    "CrudRepository": "role",
    "Project": "kind",
    "Disseminator": "role",
    "Relator": "role",
    "CrudView": "role",
    "DataManager": "role",
    "Management": "relator",
    "View": "role",
    "Collector": "role",
    "Processor": "role",
    "Storer": "role",
    "Extract": "relator",
    "Transform": "relator",
    "Load": "relator",
    "DataSource": "kind",
    "ProjectObservatory": "subkind",
    "Software": "kind",
    "Service": "kind",
    "Hardware": "kind",
    "Operation": "relator",
    "Connection": "relator",
    "Network": "kind",
}

GENERALIZACOES_ESPERADAS = {
    ("Agent", "ObservatoryUser"),
    ("Agent", "StakeHolder"),
    ("Agent", "System"),
    ("DataManager", "CrudRepository"),
    ("DataManager", "Collector"),
    ("DataManager", "Processor"),
    ("DataManager", "Storer"),
    ("View", "Disseminator"),
    ("View", "Relator"),
    ("View", "CrudView"),
    ("ProjectObservatory", "DataManager"),
    ("ProjectObservatory", "View"),
    ("Software", "ProjectObservatory"),
}

# (estereotipo, origem, cardOrigem, aggrOrigem, destino, cardDestino, aggrDestino)
RELACOES_ESPERADAS = {
    ("memberOf", "ObservatoryGroup", "1", "NONE", "ObservatoryUser", "0..*", "SHARED"),
    ("memberOf", "ObservatoryGroup", "1", "NONE", "StakeHolder", "0..*", "SHARED"),
    ("memberOf", "ObservatoryGroup", "1", "NONE", "System", "0..*", "NONE"),
    ("componentOf", "Hardware", "1..*", "NONE", "Software", "1..*", "COMPOSITE"),
    ("mediation", "Observation", "1..*", "NONE", "Knowledge", "1..*", "NONE"),
    ("mediation", "Observation", "0..*", "NONE", "Agent", "1", "NONE"),
    ("mediation", "Observation", "0..*", "NONE", "Disseminator", "1", "NONE"),
    ("mediation", "SocialInteraction", "0..*", "NONE", "Agent", "1", "NONE"),
    ("mediation", "SocialInteraction", "0..*", "NONE", "Relator", "1", "NONE"),
    ("mediation", "Log", "0..*", "NONE", "Agent", "1", "NONE"),
    ("mediation", "Log", "0..*", "NONE", "Relator", "1", "NONE"),
    ("mediation", "CrudOperation", "0..*", "NONE", "Agent", "1", "NONE"),
    ("mediation", "CrudOperation", "0..*", "NONE", "CrudView", "1", "NONE"),
    ("mediation", "Management", "0..*", "NONE", "Project", "1", "NONE"),
    ("mediation", "Management", "0..*", "NONE", "DataManager", "1", "NONE"),
    ("mediation", "Management", "0..*", "NONE", "View", "1", "NONE"),
    ("mediation", "Extract", "1..*", "NONE", "Collector", "1", "NONE"),
    ("mediation", "Extract", "1..*", "NONE", "DataSource", "1", "NONE"),
    ("mediation", "Transform", "1..*", "NONE", "Collector", "1", "NONE"),
    ("mediation", "Transform", "1..*", "NONE", "Processor", "1", "NONE"),
    ("mediation", "Load", "1..*", "NONE", "Processor", "1", "NONE"),
    ("mediation", "Load", "1..*", "NONE", "Storer", "1", "NONE"),
    ("mediation", "Operation", "0..*", "NONE", "Software", "0..*", "NONE"),
    ("mediation", "Operation", "0..*", "NONE", "Service", "1", "NONE"),
    ("mediation", "Operation", "0..*", "NONE", "Hardware", "0..*", "NONE"),
    ("mediation", "Operation", "0..*", "NONE", "Network", "0..*", "NONE"),
    ("mediation", "Connection", "0..*", "NONE", "Hardware", "1", "NONE"),
    ("mediation", "Connection", "0..*", "NONE", "Network", "1", "NONE"),
}

DEFICIENCIAS = [f"A{numero}" for numero in range(1, 10)]


class Resultado:
    def __init__(self) -> None:
        self.falhas: list[str] = []

    def exigir(self, condicao: bool, mensagem: str) -> bool:
        if not condicao:
            self.falhas.append(mensagem)
        return condicao


# --------------------------------------------------------------------------
# Leitura do modelo
# --------------------------------------------------------------------------


class Modelo:
    """Visao do JSON do OntoUML Schema em termos de nome, e nao de id."""

    def __init__(self, dados: dict) -> None:
        conteudo = dados["model"]["contents"]
        self.classes = {c["name"]: c for c in conteudo if c["type"] == "Class"}
        self.relacoes = [r for r in conteudo if r["type"] == "Relation"]
        self.generalizacoes = [g for g in conteudo if g["type"] == "Generalization"]
        self._por_id = {c["id"]: c["name"] for c in self.classes.values()}

    def nome_de(self, referencia) -> str:
        if isinstance(referencia, dict):
            return self._por_id.get(referencia.get("id"), referencia.get("id", "?"))
        return self._por_id.get(referencia, str(referencia))

    def estereotipo(self, nome: str) -> str | None:
        classe = self.classes.get(nome)
        return classe.get("stereotype") if classe else None

    def pares_de_generalizacao(self) -> set[tuple[str, str]]:
        return {
            (self.nome_de(g["general"]), self.nome_de(g["specific"])) for g in self.generalizacoes
        }

    def tuplas_de_relacao(self) -> set[tuple]:
        tuplas = set()
        for relacao in self.relacoes:
            origem, destino = relacao["properties"]
            tuplas.add(
                (
                    relacao.get("stereotype"),
                    self.nome_de(origem["propertyType"]),
                    origem["cardinality"],
                    origem.get("aggregationKind") or "NONE",
                    self.nome_de(destino["propertyType"]),
                    destino["cardinality"],
                    destino.get("aggregationKind") or "NONE",
                )
            )
        return tuplas

    def mediacoes_de(self, relator: str) -> list[tuple[str, str]]:
        """[(mediado, cardinalidade do mediado)] das mediacoes de um relator."""
        saida = []
        for relacao in self.relacoes:
            if relacao.get("stereotype") != "mediation":
                continue
            origem, destino = relacao["properties"]
            if self.nome_de(origem["propertyType"]) == relator:
                saida.append((self.nome_de(destino["propertyType"]), destino["cardinality"]))
        return saida

    def ancestrais(self, nome: str) -> set[str]:
        pares = self.pares_de_generalizacao()
        vistos: set[str] = set()
        fronteira = [nome]
        while fronteira:
            atual = fronteira.pop()
            for geral, especifico in pares:
                if especifico == atual and geral not in vistos:
                    vistos.add(geral)
                    fronteira.append(geral)
        return vistos

    def atributos_totais(self) -> int:
        return sum(len(c.get("properties") or []) for c in self.classes.values())


# --------------------------------------------------------------------------
# Verificacoes
# --------------------------------------------------------------------------


def verificar_modelo_existe(caminho: Path, resultado: Resultado) -> Modelo | None:
    if not resultado.exigir(caminho.exists(), f"{caminho} nao existe"):
        return None
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    if not resultado.exigir(
        dados.get("type") == "Project" and isinstance(dados.get("model"), dict),
        f"{caminho} nao esta no OntoUML Schema (esperado type=Project com um model)",
    ):
        return None
    return Modelo(dados)


def verificar_corresponde_ao_publicado(modelo: Modelo, resultado: Resultado) -> None:
    encontradas = {nome: classe.get("stereotype") for nome, classe in modelo.classes.items()}

    faltando = set(CLASSES_ESPERADAS) - set(encontradas)
    sobrando = set(encontradas) - set(CLASSES_ESPERADAS)
    resultado.exigir(not faltando, f"classes ausentes no modelo: {sorted(faltando)}")
    resultado.exigir(not sobrando, f"classes a mais no modelo: {sorted(sobrando)}")
    for nome, esperado in CLASSES_ESPERADAS.items():
        if nome in encontradas:
            resultado.exigir(
                encontradas[nome] == esperado,
                f"estereotipo de {nome}: esperado «{esperado}», encontrado «{encontradas[nome]}»",
            )

    generalizacoes = modelo.pares_de_generalizacao()
    resultado.exigir(
        generalizacoes == GENERALIZACOES_ESPERADAS,
        "generalizacoes divergem dos diagramas: "
        f"faltam {sorted(GENERALIZACOES_ESPERADAS - generalizacoes)}, "
        f"sobram {sorted(generalizacoes - GENERALIZACOES_ESPERADAS)}",
    )

    relacoes = modelo.tuplas_de_relacao()
    faltando_rel = RELACOES_ESPERADAS - relacoes
    sobrando_rel = relacoes - RELACOES_ESPERADAS
    resultado.exigir(
        not faltando_rel, f"relacoes ausentes ou com pontas diferentes: {sorted(faltando_rel)}"
    )
    resultado.exigir(not sobrando_rel, f"relacoes a mais no modelo: {sorted(sobrando_rel)}")

    resultado.exigir(
        modelo.atributos_totais() == 0,
        "o modelo publicado nao tem atributo nenhum; o reconstruido ganhou "
        f"{modelo.atributos_totais()}",
    )


def verificar_owl(caminho: Path, modelo: Modelo, resultado: Resultado) -> None:
    if not resultado.exigir(caminho.exists(), f"{caminho} nao existe"):
        return
    grafo = rdflib.Graph()
    grafo.parse(caminho.as_posix(), format="turtle")

    resultado.exigir(
        (None, rdflib.OWL.imports, rdflib.URIRef(f"{GUFO}")) in grafo,
        "a OWL de baseline nao importa a gUFO",
    )

    classes_owl = {
        str(sujeito).rsplit("#", 1)[-1]
        for sujeito in grafo.subjects(rdflib.RDF.type, rdflib.OWL.Class)
        if isinstance(sujeito, rdflib.URIRef) and GUFO not in str(sujeito)
    }
    faltando = set(modelo.classes) - classes_owl
    resultado.exigir(
        not faltando, f"classes do modelo que nao chegaram a OWL de baseline: {sorted(faltando)}"
    )

    # Os dois defeitos meronimicos precisam sobreviver a transformacao: e neles
    # que a evidencia de A2 e A3 fica machine-readable.
    def propriedade(nome: str):
        return next(
            (
                s
                for s in grafo.subjects(rdflib.RDF.type, rdflib.OWL.ObjectProperty)
                if str(s).endswith(f"#{nome}")
            ),
            None,
        )

    componente = propriedade("componentOf_Hardware_Software")
    if resultado.exigir(componente is not None, "A2 nao sobreviveu a transformacao gUFO"):
        dominio = grafo.value(componente, rdflib.RDFS.domain)
        alcance = grafo.value(componente, rdflib.RDFS.range)
        resultado.exigir(
            str(dominio).endswith("#Hardware") and str(alcance).endswith("#Software"),
            f"A2 na OWL: esperado Hardware -> Software, encontrado {dominio} -> {alcance}",
        )

    membro = propriedade("memberOf_ObservatoryGroup_ObservatoryUser")
    if resultado.exigir(membro is not None, "A3 nao sobreviveu a transformacao gUFO"):
        dominio = grafo.value(membro, rdflib.RDFS.domain)
        alcance = grafo.value(membro, rdflib.RDFS.range)
        resultado.exigir(
            str(dominio).endswith("#ObservatoryGroup") and str(alcance).endswith("#ObservatoryUser"),
            f"A3 na OWL: esperado ObservatoryGroup -> ObservatoryUser, "
            f"encontrado {dominio} -> {alcance}",
        )


def verificar_relatorio_plugin(diretorio: Path, resultado: Resultado) -> None:
    markdown = diretorio / "relatorio-plugin-ontouml.md"
    bruto = diretorio / "relatorio-plugin-ontouml.json"
    resultado.exigir(markdown.exists(), f"{markdown} nao existe")
    if not resultado.exigir(bruto.exists(), f"{bruto} nao existe"):
        return
    problemas = json.loads(bruto.read_text(encoding="utf-8"))
    resultado.exigir(isinstance(problemas, list), f"{bruto} nao e uma lista de problemas")

    controle = diretorio / "controle-verificacao.md"
    if resultado.exigir(
        controle.exists(),
        f"{controle} nao existe; sem ele um relatorio vazio do verificador e ininterpretavel",
    ):
        texto = controle.read_text(encoding="utf-8")
        resultado.exigir(
            "**NAO**" not in texto,
            "o controle registra mutacao nao detectada: o relatorio do verificador nao "
            "pode ser interpretado",
        )
        resultado.exigir(
            texto.count("| sim |") >= 3,
            "o controle precisa de ao menos tres mutacoes detectadas",
        )


def verificar_relatorio_oops(diretorio: Path, resultado: Resultado) -> set[str]:
    markdown = diretorio / "relatorio-oops.md"
    bruto = diretorio / "relatorio-oops.xml"
    resultado.exigir(markdown.exists(), f"{markdown} nao existe")
    if not resultado.exigir(bruto.exists(), f"{bruto} nao existe"):
        return set()

    texto = bruto.read_text(encoding="utf-8")
    resultado.exigir(
        "unexpected_error" not in texto,
        f"{bruto} guarda um erro do servico, nao um relatorio",
    )
    codigos = set(re.findall(r"hasCode[^>]*>(P\d+)<", texto))
    resultado.exigir(bool(codigos), f"{bruto} nao traz nenhum pitfall identificado")
    return codigos


def verificar_evidencias(caminho: Path, codigos_oops: set[str], resultado: Resultado) -> None:
    if not resultado.exigir(caminho.exists(), f"{caminho} nao existe"):
        return
    texto = caminho.read_text(encoding="utf-8")

    for deficiencia in DEFICIENCIAS:
        resultado.exigir(
            re.search(rf"^## {deficiencia} — ", texto, re.MULTILINE) is not None,
            f"{deficiencia} nao tem seccao propria em {caminho.name}",
        )

    resultado.exigir(
        "## Achados além de A1–A9" in texto,
        f"{caminho.name} nao registra os achados fora de A1-A9",
    )
    for codigo in sorted(codigos_oops):
        resultado.exigir(
            codigo in texto,
            f"o pitfall {codigo} do OOPS! nao esta enderecado em {caminho.name} — "
            "achado orfao e defeito",
        )


def verificar_defeitos_presentes(modelo: Modelo, resultado: Resultado) -> None:
    """Os nove defeitos tem de estar no modelo. Reconstrucao que corrige nao serve."""

    # A1: um unico CrudOperation «relator», sem nada que discrimine a operacao.
    resultado.exigir(modelo.estereotipo("CrudOperation") == "relator", "A1: CrudOperation sumiu")
    resultado.exigir(
        not [g for g in modelo.pares_de_generalizacao() if g[0] == "CrudOperation"],
        "A1: CrudOperation ganhou especializacoes; o defeito e justamente nao ter",
    )

    # A2 e A3 sao conferidos contra a OWL em verificar_owl; aqui, a extremidade
    # de agregacao, que so o JSON carrega.
    meronimicas = [
        r for r in modelo.relacoes if r.get("stereotype") in ("memberOf", "componentOf")
    ]
    com_todo_papel = [
        r
        for r in meronimicas
        if r["properties"][1].get("aggregationKind") in ("SHARED", "COMPOSITE")
        and modelo.estereotipo(modelo.nome_de(r["properties"][1]["propertyType"])) == "role"
    ]
    resultado.exigir(
        len(com_todo_papel) >= 2,
        "A3: nenhuma «memberOf» com o todo do lado do «role»; o defeito nao esta no modelo",
    )
    sem_agregacao = [
        r
        for r in meronimicas
        if r["properties"][0].get("aggregationKind", "NONE") in (None, "NONE")
        and r["properties"][1].get("aggregationKind", "NONE") in (None, "NONE")
    ]
    resultado.exigir(
        len(sem_agregacao) == 1,
        f"B2: esperada exatamente uma meronimica sem todo nem parte, achadas {len(sem_agregacao)}",
    )

    # A4: classe de dominio chamada Relator, que nao e «relator».
    resultado.exigir(
        modelo.estereotipo("Relator") == "role",
        "A4: a classe Relator sumiu ou deixou de ser «role»",
    )

    # A5: ETL como relator endurante, e nenhum evento em lugar nenhum.
    for etapa in ("Extract", "Transform", "Load"):
        resultado.exigir(
            modelo.estereotipo(etapa) == "relator", f"A5: {etapa} deixou de ser «relator»"
        )
    resultado.exigir(
        not [c for c in modelo.classes.values() if c.get("stereotype") == "event"],
        "A5: o modelo ganhou eventos; o baseline nao tem nenhum",
    )

    # A6: Agent generico, sem distincao fisico/social.
    resultado.exigir(modelo.estereotipo("Agent") == "kind", "A6: Agent deixou de ser «kind»")
    resultado.exigir(
        not ({"Person", "Organization", "SocialAgent", "PhysicalAgent"} & set(modelo.classes)),
        "A6: o modelo ganhou taxonomia UFO-C; o baseline nao tem",
    )

    # A7: System e «role» e o unico sortal ultimo acima dele e Agent.
    resultado.exigir(modelo.estereotipo("System") == "role", "A7: System deixou de ser «role»")
    resultado.exigir(
        modelo.ancestrais("System") == {"Agent"},
        f"A7: ancestrais de System mudaram: {sorted(modelo.ancestrais('System'))}",
    )

    # A8: relatores n-arios, e o minimo zero na ponta mediada (B1).
    resultado.exigir(
        len(modelo.mediacoes_de("Management")) >= 3,
        "A8: Management deixou de ser n-ario",
    )
    resultado.exigir(
        len(modelo.mediacoes_de("Operation")) >= 4,
        "A8: Operation deixou de ser n-ario",
    )
    minimo_zero = [
        (relator, mediado)
        for relator in modelo.classes
        for mediado, cardinalidade in modelo.mediacoes_de(relator)
        if cardinalidade.split("..")[0] == "0"
    ]
    resultado.exigir(
        len(minimo_zero) == 3,
        f"B1: esperadas tres mediacoes com minimo zero na ponta mediada, achadas "
        f"{len(minimo_zero)}: {minimo_zero}",
    )

    # A9: a cadeia Software > ProjectObservatory > DataManager/View.
    for geral, especifico in (
        ("Software", "ProjectObservatory"),
        ("ProjectObservatory", "DataManager"),
        ("ProjectObservatory", "View"),
    ):
        resultado.exigir(
            (geral, especifico) in modelo.pares_de_generalizacao(),
            f"A9: {especifico} deixou de especializar {geral}",
        )


def main() -> int:
    diretorio = Path(sys.argv[1]) if len(sys.argv) > 1 else DIRETORIO_PADRAO
    baseline = diretorio / "baseline"
    resultado = Resultado()

    modelo = verificar_modelo_existe(baseline / "ontompo-as-is.ontouml.json", resultado)
    if modelo is not None:
        verificar_corresponde_ao_publicado(modelo, resultado)
        verificar_owl(baseline / "ontompo-as-is.ttl", modelo, resultado)
        verificar_defeitos_presentes(modelo, resultado)

    verificar_relatorio_plugin(baseline, resultado)
    codigos_oops = verificar_relatorio_oops(baseline, resultado)
    if modelo is not None:
        verificar_evidencias(diretorio / "evidencias-A1-A9.md", codigos_oops, resultado)

    for falha in resultado.falhas:
        print(f"FALHA: {falha}")

    if resultado.falhas:
        print(f"\n{len(resultado.falhas)} verificacao(oes) reprovada(s).")
        return 1
    print("Linha de base conferida: modelo, OWL, dois relatorios, controle e evidencias.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
