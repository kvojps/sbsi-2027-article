#!/usr/bin/env python3
"""Verifica a primeira rodada de revisao contra a checklist do ticket 04.

Uso: python tools/verification/verificar_rodada1.py [diretorio-ontologia]

Confere oito coisas, na ordem da checklist do ticket:

  1. o modelo revisado existe no formato de intercambio do plugin OntoUML;
  2. ele corresponde ao projetado — classes, estereotipos, generalizacoes, a
     particao de CrudOperation e as relacoes com suas multiplicidades e
     extremidades de agregacao;
  3. cada uma das seis correcoes esta de fato aplicada, e o defeito
     correspondente do baseline nao esta mais la;
  4. o baseline continua intacto: revisar o modelo revisado nao pode ter
     "arrumado" a metade "antes" do antes/depois;
  5. o relatorio do plugin foi salvo para a rodada e e comparavel ao do
     baseline, com o controle que o torna interpretavel;
  6. o verificador complementar mede a diferenca, todas as suas regras disparam
     sobre o baseline, e a rodada nao tem nenhum erro remanescente;
  7. cada correcao tem par antes/depois registrado em `correcoes-rodada-1.md`,
     e o achado que sobra tem endereco;
  8. as correcoes de A2, A3, A4 e A9 sobrevivem a transformacao gUFO.

A tabela de conferencia da verificacao 2 e transcrita aqui a partir do
enunciado do ticket, e **nao** importada de `tools/model/ontompo-rodada-1.js`.
Nao e uma leitura independente como a do ticket 03 — nao ha diagrama publicado
do modelo revisado para reler — mas mantem a mesma propriedade util: se o
modelo derivar do que o ticket pediu, a duplicacao acusa.

Sai com codigo 1 se qualquer verificacao falhar.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from verificar_baseline import GUFO, Modelo, Resultado  # noqa: E402

try:
    import rdflib
except ImportError:  # pragma: no cover - dependencia ausente
    print("ERRO: rdflib ausente. Rode: pip install rdflib")
    sys.exit(1)

DIRETORIO_PADRAO = Path("artifacts/ontology")

# --------------------------------------------------------------------------
# O modelo que o ticket 04 pediu, transcrito do enunciado.
# --------------------------------------------------------------------------

CLASSES_ESPERADAS = {
    # Camada Agentes
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
    # A1
    "CreateOperation": "subkind",
    "ReadOperation": "subkind",
    "UpdateOperation": "subkind",
    "DeleteOperation": "subkind",
    # Camada Estruturas
    "CrudRepository": "role",
    "Project": "kind",
    "Disseminator": "role",
    "Reporter": "role",  # A4
    "CrudView": "role",
    "DataManager": "role",
    "View": "role",
    "ProjectDataManagement": "relator",  # A8
    "ViewProvision": "relator",  # A8
    "Collector": "role",
    "Processor": "role",
    "Storer": "role",
    "Extract": "relator",
    "Transform": "relator",
    "Load": "relator",
    "DataSource": "kind",
    "ProjectObservatory": "subkind",
    # Camada Infraestrutura
    "Software": "kind",
    "Service": "kind",
    "Hardware": "kind",
    "SoftwareExecution": "relator",  # A2 e A8
    "ServiceProvision": "relator",  # A8
    "Connection": "relator",
    "Network": "kind",
}

GENERALIZACOES_ESPERADAS = {
    ("Agent", "ObservatoryUser"),
    ("Agent", "StakeHolder"),
    ("Agent", "System"),
    ("CrudOperation", "CreateOperation"),
    ("CrudOperation", "ReadOperation"),
    ("CrudOperation", "UpdateOperation"),
    ("CrudOperation", "DeleteOperation"),
    ("DataManager", "CrudRepository"),
    ("DataManager", "Collector"),
    ("DataManager", "Processor"),
    ("DataManager", "Storer"),
    ("View", "Disseminator"),
    ("View", "Reporter"),
    ("View", "CrudView"),
    ("Software", "DataManager"),
    ("Software", "View"),
    ("Software", "ProjectObservatory"),
}

# (estereotipo, origem, cardOrigem, aggrOrigem, destino, cardDestino, aggrDestino)
RELACOES_ESPERADAS = {
    ("memberOf", "ObservatoryUser", "1..*", "NONE", "ObservatoryGroup", "1", "SHARED"),
    ("memberOf", "StakeHolder", "1..*", "NONE", "ObservatoryGroup", "1", "SHARED"),
    ("memberOf", "System", "1..*", "NONE", "ObservatoryGroup", "1", "SHARED"),
    ("componentOf", "DataManager", "1..*", "NONE", "ProjectObservatory", "1", "COMPOSITE"),
    ("componentOf", "View", "1..*", "NONE", "ProjectObservatory", "1", "COMPOSITE"),
    ("mediation", "Observation", "1..*", "NONE", "Knowledge", "1..*", "NONE"),
    ("mediation", "Observation", "0..*", "NONE", "Agent", "1", "NONE"),
    ("mediation", "Observation", "0..*", "NONE", "Disseminator", "1", "NONE"),
    ("mediation", "SocialInteraction", "0..*", "NONE", "Agent", "1", "NONE"),
    ("mediation", "SocialInteraction", "0..*", "NONE", "Reporter", "1", "NONE"),
    ("mediation", "Log", "0..*", "NONE", "Agent", "1", "NONE"),
    ("mediation", "Log", "0..*", "NONE", "Reporter", "1", "NONE"),
    ("mediation", "CrudOperation", "0..*", "NONE", "Agent", "1", "NONE"),
    ("mediation", "CrudOperation", "0..*", "NONE", "CrudView", "1", "NONE"),
    ("mediation", "ProjectDataManagement", "0..*", "NONE", "DataManager", "1", "NONE"),
    ("mediation", "ProjectDataManagement", "0..*", "NONE", "Project", "1", "NONE"),
    ("mediation", "ViewProvision", "0..*", "NONE", "DataManager", "1", "NONE"),
    ("mediation", "ViewProvision", "0..*", "NONE", "View", "1", "NONE"),
    ("mediation", "Extract", "1..*", "NONE", "Collector", "1", "NONE"),
    ("mediation", "Extract", "1..*", "NONE", "DataSource", "1", "NONE"),
    ("mediation", "Transform", "1..*", "NONE", "Collector", "1", "NONE"),
    ("mediation", "Transform", "1..*", "NONE", "Processor", "1", "NONE"),
    ("mediation", "Load", "1..*", "NONE", "Processor", "1", "NONE"),
    ("mediation", "Load", "1..*", "NONE", "Storer", "1", "NONE"),
    ("mediation", "SoftwareExecution", "1..*", "NONE", "Software", "1", "NONE"),
    ("mediation", "SoftwareExecution", "0..*", "NONE", "Hardware", "1", "NONE"),
    ("mediation", "ServiceProvision", "1..*", "NONE", "Service", "1", "NONE"),
    ("mediation", "ServiceProvision", "0..*", "NONE", "Software", "1", "NONE"),
    ("mediation", "Connection", "0..*", "NONE", "Hardware", "1", "NONE"),
    ("mediation", "Connection", "0..*", "NONE", "Network", "1", "NONE"),
    ("material", "Software", "0..*", "NONE", "Hardware", "1..*", "NONE"),
    ("derivation", "material_Software_Hardware", "0..*", "NONE", "SoftwareExecution", "0..*", "NONE"),
}

PARTICAO_ESPERADA = {
    "name": "crudOperationType",
    "general": "CrudOperation",
    "specifics": {"CreateOperation", "ReadOperation", "UpdateOperation", "DeleteOperation"},
}

CORRECOES = ["A1", "A2", "A3", "A4", "A8", "A9"]

# As cinco regras do verificador complementar, transcritas do ticket: as quatro
# de severidade `error` precisam zerar na rodada 1.
REGRAS_EXTRA = [
    "memberof_whole_not_collective",
    "parthood_ends_undeclared",
    "mediation_optional_relatum",
    "class_name_collides_with_metaconcept",
    "relator_arity_above_binary",
]


class ModeloComParticoes(Modelo):
    """`Modelo` mais os conjuntos de generalizacao e as relacoes como relata.

    O baseline nao tem particao nem «derivation», entao `Modelo` so resolve
    identificador de classe. Uma «derivation» tem uma *relacao* numa das
    pontas, e sem isso ela apareceria pelo id cru.
    """

    def __init__(self, dados: dict) -> None:
        super().__init__(dados)
        self.conjuntos = [
            c for c in dados["model"]["contents"] if c["type"] == "GeneralizationSet"
        ]
        self._generalizacao_por_id = {g["id"]: g for g in self.generalizacoes}
        self._por_id.update({r["id"]: r["name"] for r in self.relacoes})

    def particoes(self) -> list[dict]:
        saida = []
        for conjunto in self.conjuntos:
            generalizacoes = [
                self._generalizacao_por_id[referencia["id"]]
                for referencia in conjunto.get("generalizations") or []
                if referencia["id"] in self._generalizacao_por_id
            ]
            gerais = {self.nome_de(g["general"]) for g in generalizacoes}
            saida.append(
                {
                    "name": conjunto.get("name"),
                    "general": next(iter(gerais)) if len(gerais) == 1 else None,
                    "specifics": {self.nome_de(g["specific"]) for g in generalizacoes},
                    "isDisjoint": conjunto.get("isDisjoint"),
                    "isComplete": conjunto.get("isComplete"),
                }
            )
        return saida

    def relacoes_por_estereotipo(self, estereotipo: str) -> list[dict]:
        return [r for r in self.relacoes if r.get("stereotype") == estereotipo]

    def tem_relacao(self, estereotipo: str, origem: str, destino: str) -> bool:
        for relacao in self.relacoes_por_estereotipo(estereotipo):
            pontas = relacao["properties"]
            if (
                self.nome_de(pontas[0]["propertyType"]) == origem
                and self.nome_de(pontas[1]["propertyType"]) == destino
            ):
                return True
        return False


# --------------------------------------------------------------------------
# Verificacoes
# --------------------------------------------------------------------------


def carregar_modelo(caminho: Path, resultado: Resultado) -> ModeloComParticoes | None:
    if not resultado.exigir(caminho.exists(), f"{caminho} nao existe"):
        return None
    dados = json.loads(caminho.read_text(encoding="utf-8"))
    if not resultado.exigir(
        dados.get("type") == "Project" and isinstance(dados.get("model"), dict),
        f"{caminho} nao esta no OntoUML Schema (esperado type=Project com um model)",
    ):
        return None
    return ModeloComParticoes(dados)


def verificar_corresponde_ao_projetado(
    modelo: ModeloComParticoes, resultado: Resultado
) -> None:
    encontradas = {nome: classe.get("stereotype") for nome, classe in modelo.classes.items()}

    faltando = set(CLASSES_ESPERADAS) - set(encontradas)
    sobrando = set(encontradas) - set(CLASSES_ESPERADAS)
    resultado.exigir(not faltando, f"classes ausentes no modelo revisado: {sorted(faltando)}")
    resultado.exigir(not sobrando, f"classes a mais no modelo revisado: {sorted(sobrando)}")
    for nome, esperado in CLASSES_ESPERADAS.items():
        if nome in encontradas:
            resultado.exigir(
                encontradas[nome] == esperado,
                f"estereotipo de {nome}: esperado «{esperado}», encontrado «{encontradas[nome]}»",
            )

    generalizacoes = modelo.pares_de_generalizacao()
    resultado.exigir(
        generalizacoes == GENERALIZACOES_ESPERADAS,
        "generalizacoes divergem do projetado: "
        f"faltam {sorted(GENERALIZACOES_ESPERADAS - generalizacoes)}, "
        f"sobram {sorted(generalizacoes - GENERALIZACOES_ESPERADAS)}",
    )

    relacoes = modelo.tuplas_de_relacao()
    faltando_rel = RELACOES_ESPERADAS - relacoes
    sobrando_rel = relacoes - RELACOES_ESPERADAS
    resultado.exigir(
        not faltando_rel, f"relacoes ausentes ou com pontas diferentes: {sorted(faltando_rel)}"
    )
    resultado.exigir(not sobrando_rel, f"relacoes a mais no modelo revisado: {sorted(sobrando_rel)}")

    particoes = modelo.particoes()
    if resultado.exigir(
        len(particoes) == 1, f"esperada exatamente uma particao, achadas {len(particoes)}"
    ):
        particao = particoes[0]
        resultado.exigir(
            particao["name"] == PARTICAO_ESPERADA["name"]
            and particao["general"] == PARTICAO_ESPERADA["general"]
            and particao["specifics"] == PARTICAO_ESPERADA["specifics"],
            f"a particao de CrudOperation divergiu: {particao}",
        )
        resultado.exigir(
            bool(particao["isDisjoint"]) and bool(particao["isComplete"]),
            "A1: a particao de CrudOperation precisa ser disjunta e completa",
        )


def verificar_correcoes_aplicadas(modelo: ModeloComParticoes, resultado: Resultado) -> None:
    """As seis correcoes, cada uma conferida pelo que mudou e pelo que sumiu."""

    # A1: CrudOperation deixou de ser o construto unico.
    especificos = {g[1] for g in modelo.pares_de_generalizacao() if g[0] == "CrudOperation"}
    resultado.exigir(
        len(especificos) == 4,
        f"A1: CrudOperation precisa ter as quatro operacoes abaixo dela, tem {sorted(especificos)}",
    )
    for operacao in ("CreateOperation", "ReadOperation", "UpdateOperation", "DeleteOperation"):
        resultado.exigir(
            (modelo.classes.get(operacao) or {}).get("restrictedTo") == ["relator"],
            f"A1: {operacao} precisa ter natureza relator, para especializar um «relator»",
        )

    # A2: a «componentOf» invalida sumiu e a execucao entrou reificada.
    resultado.exigir(
        not modelo.tem_relacao("componentOf", "Hardware", "Software"),
        "A2: a «componentOf» de Hardware para Software ainda esta no modelo",
    )
    resultado.exigir(
        modelo.estereotipo("SoftwareExecution") == "relator"
        and {m[0] for m in modelo.mediacoes_de("SoftwareExecution")} == {"Software", "Hardware"},
        "A2: SoftwareExecution precisa mediar exatamente Software e Hardware",
    )
    resultado.exigir(
        modelo.tem_relacao("material", "Software", "Hardware")
        and modelo.tem_relacao("derivation", "material_Software_Hardware", "SoftwareExecution"),
        "A2: falta a material Software-Hardware derivada de SoftwareExecution",
    )

    # A3: as tres «memberOf» com o coletivo como todo.
    memberof = modelo.relacoes_por_estereotipo("memberOf")
    resultado.exigir(len(memberof) == 3, f"A3: esperadas tres «memberOf», achadas {len(memberof)}")
    for relacao in memberof:
        parte, todo = relacao["properties"]
        nome_todo = modelo.nome_de(todo["propertyType"])
        resultado.exigir(
            nome_todo == "ObservatoryGroup"
            and modelo.estereotipo(nome_todo) == "collective"
            and todo.get("aggregationKind") in ("SHARED", "COMPOSITE"),
            f"A3: em {relacao.get('name')} o todo declarado nao e o coletivo",
        )
        resultado.exigir(
            parte["cardinality"].split("..")[0] != "0",
            f"A3: {relacao.get('name')} admite um coletivo sem membro nenhum",
        )

    # A4: nenhuma classe de dominio com nome de metaconceito da UFO.
    resultado.exigir(
        "Relator" not in modelo.classes and "Reporter" in modelo.classes,
        "A4: a classe de dominio `Relator` precisa ter virado `Reporter`",
    )
    resultado.exigir(
        {g for g in modelo.pares_de_generalizacao() if g[1] == "Reporter"} == {("View", "Reporter")},
        "A4: Reporter precisa ocupar o lugar que `Relator` ocupava, sob View",
    )
    for relator in ("SocialInteraction", "Log"):
        resultado.exigir(
            "Reporter" in {m[0] for m in modelo.mediacoes_de(relator)},
            f"A4: {relator} deixou de mediar o antigo `Relator`",
        )

    # A8: nenhum relator introduzido ou mantido pela rodada e n-ario, e nenhuma
    # mediacao tem minimo zero na ponta mediada.
    resultado.exigir(
        "Management" not in modelo.classes and "Operation" not in modelo.classes,
        "A8: Management e Operation precisam ter sido decompostos",
    )
    for relator, mediados in (
        ("ProjectDataManagement", {"DataManager", "Project"}),
        ("ViewProvision", {"DataManager", "View"}),
        ("SoftwareExecution", {"Software", "Hardware"}),
        ("ServiceProvision", {"Service", "Software"}),
    ):
        resultado.exigir(
            {m[0] for m in modelo.mediacoes_de(relator)} == mediados,
            f"A8: {relator} deveria mediar {sorted(mediados)}",
        )
    minimo_zero = [
        (relator, mediado)
        for relator in modelo.classes
        for mediado, cardinalidade in modelo.mediacoes_de(relator)
        if cardinalidade.split("..")[0] == "0"
    ]
    resultado.exigir(
        not minimo_zero,
        f"B1: mediacoes com minimo zero na ponta mediada sobreviveram: {minimo_zero}",
    )

    # A9: DataManager e View sao componentes do observatorio, nao especializacoes.
    for papel in ("DataManager", "View"):
        resultado.exigir(
            ("ProjectObservatory", papel) not in modelo.pares_de_generalizacao(),
            f"A9: {papel} ainda especializa ProjectObservatory",
        )
        resultado.exigir(
            modelo.ancestrais(papel) == {"Software"},
            f"A9: os ancestrais de {papel} deveriam ser so Software, sao "
            f"{sorted(modelo.ancestrais(papel))}",
        )
        resultado.exigir(
            modelo.tem_relacao("componentOf", papel, "ProjectObservatory"),
            f"A9: falta a «componentOf» de {papel} para ProjectObservatory",
        )
    resultado.exigir(
        "ProjectObservatory" not in modelo.ancestrais("Reporter"),
        "A9: cada visao continua sendo um observatorio inteiro",
    )


def verificar_baseline_intacto(caminho: Path, resultado: Resultado) -> None:
    """A metade "antes" nao pode ter sido corrigida de passagem."""
    if not resultado.exigir(caminho.exists(), f"{caminho} nao existe"):
        return
    baseline = Modelo(json.loads(caminho.read_text(encoding="utf-8")))
    resultado.exigir(
        baseline.estereotipo("Relator") == "role",
        "o baseline perdeu a classe `Relator`: a metade \"antes\" foi corrigida de passagem",
    )
    resultado.exigir(
        "Management" in baseline.classes and "Operation" in baseline.classes,
        "o baseline perdeu Management ou Operation",
    )
    resultado.exigir(
        ("ProjectObservatory", "DataManager") in baseline.pares_de_generalizacao(),
        "o baseline perdeu a hierarquia defeituosa de A9",
    )
    resultado.exigir(
        len(baseline.classes) == 32 and len(baseline.relacoes) == 28,
        f"o baseline mudou de tamanho: {len(baseline.classes)} classes, "
        f"{len(baseline.relacoes)} relacoes",
    )


def verificar_relatorio_plugin(diretorio: Path, baseline: Path, resultado: Resultado) -> None:
    bruto = diretorio / "relatorio-plugin-ontouml.json"
    resultado.exigir((diretorio / "relatorio-plugin-ontouml.md").exists(), "falta o relatorio .md")
    if not resultado.exigir(bruto.exists(), f"{bruto} nao existe"):
        return
    problemas = json.loads(bruto.read_text(encoding="utf-8"))
    resultado.exigir(isinstance(problemas, list), f"{bruto} nao e uma lista de problemas")

    referencia = baseline / "relatorio-plugin-ontouml.json"
    if resultado.exigir(
        referencia.exists(), "sem o relatorio do baseline nao ha com o que comparar"
    ):
        do_baseline = json.loads(referencia.read_text(encoding="utf-8"))
        resultado.exigir(
            len(problemas) <= len(do_baseline),
            f"o plugin acusa mais na rodada 1 ({len(problemas)}) que no baseline "
            f"({len(do_baseline)})",
        )

    controle = diretorio / "controle-verificacao.md"
    if resultado.exigir(
        controle.exists(),
        f"{controle} nao existe; sem ele um relatorio vazio do verificador e ininterpretavel",
    ):
        texto = controle.read_text(encoding="utf-8")
        resultado.exigir(
            "**NAO**" not in texto,
            "o controle da rodada 1 registra mutacao nao detectada",
        )
        resultado.exigir(
            texto.count("| sim |") >= 3,
            "o controle da rodada 1 precisa de ao menos tres mutacoes detectadas",
        )


def verificar_verificador_extra(diretorio: Path, resultado: Resultado) -> None:
    """A diferenca precisa estar medida, e o instrumento precisa nao ser vacuo."""
    bruto = diretorio / "relatorio-verificador-extra.json"
    resultado.exigir(
        (diretorio / "relatorio-verificador-extra.md").exists(),
        "falta o relatorio do verificador complementar em markdown",
    )
    if not resultado.exigir(bruto.exists(), f"{bruto} nao existe"):
        return

    relatorio = json.loads(bruto.read_text(encoding="utf-8"))
    antes = relatorio.get("as-is", [])
    depois = relatorio.get("rodada-1", [])

    resultado.exigir(
        len(depois) < len(antes),
        f"a rodada 1 precisa ter menos violacoes que o baseline: {len(antes)} -> {len(depois)}",
    )

    disparadas = {problema["code"] for problema in antes}
    for regra in REGRAS_EXTRA:
        resultado.exigir(
            regra in disparadas,
            f"a regra {regra} nao dispara nem sobre o baseline: sem controle positivo, "
            "o zero da rodada 1 nao e interpretavel",
        )

    erros = [problema for problema in depois if problema["severity"] == "error"]
    resultado.exigir(
        not erros,
        f"a rodada 1 ainda tem erro no verificador complementar: "
        f"{[(p['code'], p['element']) for p in erros]}",
    )


def verificar_correcoes_documentadas(caminho: Path, diretorio: Path, resultado: Resultado) -> None:
    if not resultado.exigir(caminho.exists(), f"{caminho} nao existe"):
        return
    texto = caminho.read_text(encoding="utf-8")

    for correcao in CORRECOES:
        secao = re.search(rf"^## {correcao} — .*?(?=^## |\Z)", texto, re.MULTILINE | re.DOTALL)
        if not resultado.exigir(
            secao is not None, f"{correcao} nao tem seccao propria em {caminho.name}"
        ):
            continue
        corpo = secao.group(0)
        resultado.exigir(
            "**Antes.**" in corpo and "**Depois.**" in corpo,
            f"{correcao} nao registra o par antes/depois",
        )
        resultado.exigir(
            "**Justificativa.**" in corpo,
            f"{correcao} nao registra a justificativa ontologica",
        )

    resultado.exigir(
        "A diferença, medida" in texto,
        f"{caminho.name} nao registra a diferenca medida entre baseline e rodada 1",
    )

    # Todo achado que sobra no verificador complementar precisa ter endereco.
    bruto = diretorio / "relatorio-verificador-extra.json"
    if bruto.exists():
        remanescentes = json.loads(bruto.read_text(encoding="utf-8")).get("rodada-1", [])
        for problema in remanescentes:
            resultado.exigir(
                problema["element"] in texto,
                f"o achado remanescente sobre `{problema['element']}` nao esta enderecado em "
                f"{caminho.name} — achado orfao e defeito",
            )


def verificar_owl(caminho: Path, modelo: ModeloComParticoes, resultado: Resultado) -> None:
    if not resultado.exigir(caminho.exists(), f"{caminho} nao existe"):
        return
    grafo = rdflib.Graph()
    grafo.parse(caminho.as_posix(), format="turtle")

    resultado.exigir(
        (None, rdflib.OWL.imports, rdflib.URIRef(f"{GUFO}")) in grafo,
        "a OWL da rodada 1 nao importa a gUFO",
    )

    classes_owl = {
        str(sujeito).rsplit("#", 1)[-1]
        for sujeito in grafo.subjects(rdflib.RDF.type, rdflib.OWL.Class)
        if isinstance(sujeito, rdflib.URIRef) and GUFO not in str(sujeito)
    }
    faltando = set(modelo.classes) - classes_owl
    resultado.exigir(
        not faltando, f"classes do modelo que nao chegaram a OWL da rodada 1: {sorted(faltando)}"
    )

    def propriedade(nome: str):
        return next(
            (
                s
                for s in grafo.subjects(rdflib.RDF.type, rdflib.OWL.ObjectProperty)
                if str(s).endswith(f"#{nome}")
            ),
            None,
        )

    # A2: nenhuma assercao de composicao entre hardware e software sobrevive.
    componente = rdflib.URIRef(f"{GUFO}isComponentOf")
    for propriedade_composicao in grafo.subjects(rdflib.RDFS.subPropertyOf, componente):
        dominio = str(grafo.value(propriedade_composicao, rdflib.RDFS.domain))
        alcance = str(grafo.value(propriedade_composicao, rdflib.RDFS.range))
        resultado.exigir(
            not (dominio.endswith("#Hardware") and alcance.endswith("#Software")),
            "A2: a composicao de Hardware em Software sobreviveu a transformacao gUFO",
        )

    # A3: a direcao da pertinencia esta endireitada na OWL.
    membro = propriedade("memberOf_ObservatoryUser_ObservatoryGroup")
    if resultado.exigir(membro is not None, "A3: a «memberOf» corrigida nao chegou a OWL"):
        dominio = grafo.value(membro, rdflib.RDFS.domain)
        alcance = grafo.value(membro, rdflib.RDFS.range)
        resultado.exigir(
            str(dominio).endswith("#ObservatoryUser")
            and str(alcance).endswith("#ObservatoryGroup"),
            f"A3 na OWL: esperado ObservatoryUser -> ObservatoryGroup, "
            f"encontrado {dominio} -> {alcance}",
        )

    # A4: o unico `Relator` no grafo e o da gUFO.
    homonimos = [
        str(sujeito)
        for sujeito in grafo.subjects()
        if isinstance(sujeito, rdflib.URIRef)
        and str(sujeito).endswith("#Relator")
        and GUFO not in str(sujeito)
    ]
    resultado.exigir(not homonimos, f"A4: `Relator` de dominio ainda esta na OWL: {homonimos}")

    # A9: as duas «componentOf» novas chegaram, e a especializacao velha nao.
    for papel in ("DataManager", "View"):
        parte = propriedade(f"componentOf_{papel}_ProjectObservatory")
        resultado.exigir(
            parte is not None, f"A9: a «componentOf» de {papel} nao chegou a OWL"
        )
        sujeito = next(
            (s for s in grafo.subjects() if str(s).endswith(f"#{papel}")),
            None,
        )
        if sujeito is not None:
            supertipos = {str(o) for o in grafo.objects(sujeito, rdflib.RDFS.subClassOf)}
            resultado.exigir(
                not any(s.endswith("#ProjectObservatory") for s in supertipos),
                f"A9: {papel} ainda e subclasse de ProjectObservatory na OWL",
            )

    # A1: a particao chegou como disjuncao.
    resultado.exigir(
        (None, rdflib.RDF.type, rdflib.OWL.AllDisjointClasses) in grafo,
        "A1: a particao de CrudOperation nao virou disjuncao na OWL",
    )


def main() -> int:
    diretorio = Path(sys.argv[1]) if len(sys.argv) > 1 else DIRETORIO_PADRAO
    rodada = diretorio / "rodada-1"
    baseline = diretorio / "baseline"
    resultado = Resultado()

    modelo = carregar_modelo(rodada / "ontompo-rodada-1.ontouml.json", resultado)
    if modelo is not None:
        verificar_corresponde_ao_projetado(modelo, resultado)
        verificar_correcoes_aplicadas(modelo, resultado)
        verificar_owl(rodada / "ontompo-rodada-1.ttl", modelo, resultado)

    verificar_baseline_intacto(baseline / "ontompo-as-is.ontouml.json", resultado)
    verificar_relatorio_plugin(rodada, baseline, resultado)
    verificar_verificador_extra(rodada, resultado)
    verificar_correcoes_documentadas(diretorio / "correcoes-rodada-1.md", rodada, resultado)

    for falha in resultado.falhas:
        print(f"FALHA: {falha}")

    if resultado.falhas:
        print(f"\n{len(resultado.falhas)} verificacao(oes) reprovada(s).")
        return 1
    print(
        "Rodada 1 conferida: modelo revisado, seis correcoes, baseline intacto, "
        "dois relatorios, controle e pares antes/depois."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
