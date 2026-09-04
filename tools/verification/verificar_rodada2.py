#!/usr/bin/env python3
"""Verifica a segunda rodada de revisao contra a checklist do ticket 05.

Uso: python tools/verification/verificar_rodada2.py [diretorio-ontologia]

Confere nove coisas, na ordem da checklist do ticket:

  1. o modelo revisado existe no formato de intercambio do plugin OntoUML;
  2. ele corresponde ao projetado — classes, estereotipos, naturezas dos
     nao-sortais e dos eventos, generalizacoes, as duas particoes e as relacoes
     com suas multiplicidades e extremidades de agregacao;
  3. A5: Extract, Transform e Load sao eventos, nenhuma mediacao sobrevive
     neles, e cada mediacao da rodada 1 tem a participacao que a substitui,
     ponta a ponta e multiplicidade a multiplicidade;
  4. A6 e A7: a taxonomia UFO-C esta la, `System` tem kind proprio e deixou de
     descender de `Agent`, e os dois achados que a rodada 1 endereçou a esta —
     B8 (`Observation`) e a leitura eventiva de A1 — estao fechados;
  5. as duas metades anteriores continuam intactas: nem o baseline nem a
     rodada 1 podem ter sido "arrumados" de passagem;
  6. o relatorio do plugin foi salvo e e comparavel ao das rodadas anteriores,
     com o controle que o torna interpretavel;
  7. o verificador de microteorias mede a diferenca nos tres modelos, suas
     regras de medicao disparam sobre o baseline, suas regras de guarda estao
     provadas por mutacao, e a rodada 2 nao tem erro remanescente;
  8. cada correcao tem par antes/depois e justificativa em
     `correcoes-rodada-2.md`, e nenhum resquicio da defesa de ontologia leve
     sobrevive no modelo ou nas notas;
  9. as correcoes sobrevivem a transformacao gUFO.

Como em `verificar_rodada1.py`, a tabela de conferencia da verificacao 2 e
transcrita a partir do enunciado do ticket e **nao** importada de
`tools/model/ontompo-rodada-2.js`: se o modelo derivar do que o ticket pediu, a
duplicacao acusa.

Sai com codigo 1 se qualquer verificacao falhar.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from verificar_baseline import GUFO, Modelo, Resultado  # noqa: E402
from verificar_rodada1 import ModeloComParticoes  # noqa: E402

try:
    import rdflib
except ImportError:  # pragma: no cover - dependencia ausente
    print("ERRO: rdflib ausente. Rode: pip install rdflib")
    sys.exit(1)

DIRETORIO_PADRAO = Path("artifacts/ontology")

# --------------------------------------------------------------------------
# O modelo que o ticket 05 pediu, transcrito do enunciado.
# --------------------------------------------------------------------------

CLASSES_ESPERADAS = {
    # Camada Agentes — a taxonomia UFO-C de A6 e A7
    "Agent": "category",
    "PhysicalAgent": "category",
    "SocialAgent": "category",
    "Person": "kind",
    "Organization": "kind",
    "ComputationalSystem": "kind",
    "ObservatoryGroup": "collective",
    "ObservatoryUser": "role",
    "StakeHolder": "roleMixin",
    "System": "role",
    "Knowledge": "kind",
    "Observation": "event",  # B8
    "SocialInteraction": "relator",
    "Log": "relator",
    "CrudOperation": "event",  # A1 sob UFO-B
    "CreateOperation": "event",
    "ReadOperation": "event",
    "UpdateOperation": "event",
    "DeleteOperation": "event",
    # Camada Estruturas
    "CrudRepository": "role",
    "Project": "kind",
    "Disseminator": "role",
    "Reporter": "role",
    "CrudView": "role",
    "DataManager": "role",
    "View": "role",
    "ProjectDataManagement": "relator",
    "ViewProvision": "relator",
    "Collector": "role",
    "Processor": "role",
    "Storer": "role",
    "EtlProcess": "event",  # A5
    "Extract": "event",
    "Transform": "event",
    "Load": "event",
    "DataSource": "kind",
    "ProjectObservatory": "subkind",
    # Camada Infraestrutura
    "Software": "kind",
    "Service": "kind",
    "Hardware": "kind",
    "SoftwareExecution": "relator",
    "ServiceProvision": "relator",
    "Connection": "relator",
    "Network": "kind",
}

# As naturezas que o ticket exige declaradas: os nao-sortais da camada de
# agentes e os eventos. Sem elas a verificacao de naturezas compativeis nas
# generalizacoes nao tem o que comparar.
NATUREZAS_ESPERADAS = {
    "Agent": ["functional-complex", "collective"],
    "PhysicalAgent": ["functional-complex"],
    "SocialAgent": ["functional-complex", "collective"],
    "StakeHolder": ["functional-complex", "collective"],
    "Observation": ["event"],
    "CrudOperation": ["event"],
    "CreateOperation": ["event"],
    "ReadOperation": ["event"],
    "UpdateOperation": ["event"],
    "DeleteOperation": ["event"],
    "EtlProcess": ["event"],
    "Extract": ["event"],
    "Transform": ["event"],
    "Load": ["event"],
}

GENERALIZACOES_ESPERADAS = {
    ("Agent", "PhysicalAgent"),
    ("Agent", "SocialAgent"),
    ("Agent", "StakeHolder"),
    ("PhysicalAgent", "Person"),
    ("SocialAgent", "Organization"),
    ("Person", "ObservatoryUser"),
    ("ComputationalSystem", "System"),
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
    ("mediation", "SocialInteraction", "0..*", "NONE", "Agent", "1", "NONE"),
    ("mediation", "SocialInteraction", "0..*", "NONE", "Reporter", "1", "NONE"),
    ("mediation", "Log", "0..*", "NONE", "Agent", "1", "NONE"),
    ("mediation", "Log", "0..*", "NONE", "Reporter", "1", "NONE"),
    ("mediation", "ProjectDataManagement", "0..*", "NONE", "DataManager", "1", "NONE"),
    ("mediation", "ProjectDataManagement", "0..*", "NONE", "Project", "1", "NONE"),
    ("mediation", "ViewProvision", "0..*", "NONE", "DataManager", "1", "NONE"),
    ("mediation", "ViewProvision", "0..*", "NONE", "View", "1", "NONE"),
    ("mediation", "SoftwareExecution", "1..*", "NONE", "Software", "1", "NONE"),
    ("mediation", "SoftwareExecution", "0..*", "NONE", "Hardware", "1", "NONE"),
    ("mediation", "ServiceProvision", "1..*", "NONE", "Service", "1", "NONE"),
    ("mediation", "ServiceProvision", "0..*", "NONE", "Software", "1", "NONE"),
    ("mediation", "Connection", "0..*", "NONE", "Hardware", "1", "NONE"),
    ("mediation", "Connection", "0..*", "NONE", "Network", "1", "NONE"),
    ("participation", "Agent", "1", "NONE", "Observation", "0..*", "NONE"),
    ("participation", "Disseminator", "1", "NONE", "Observation", "0..*", "NONE"),
    ("participation", "Agent", "1", "NONE", "CrudOperation", "0..*", "NONE"),
    ("participation", "CrudView", "1", "NONE", "CrudOperation", "0..*", "NONE"),
    ("participation", "Collector", "1", "NONE", "Extract", "1..*", "NONE"),
    ("participation", "DataSource", "1", "NONE", "Extract", "1..*", "NONE"),
    ("participation", "Collector", "1", "NONE", "Transform", "1..*", "NONE"),
    ("participation", "Processor", "1", "NONE", "Transform", "1..*", "NONE"),
    ("participation", "Processor", "1", "NONE", "Load", "1..*", "NONE"),
    ("participation", "Storer", "1", "NONE", "Load", "1..*", "NONE"),
    ("participational", "Extract", "1", "NONE", "EtlProcess", "1", "COMPOSITE"),
    ("participational", "Transform", "1", "NONE", "EtlProcess", "1", "COMPOSITE"),
    ("participational", "Load", "1", "NONE", "EtlProcess", "1", "COMPOSITE"),
    ("creation", "Knowledge", "1..*", "NONE", "Observation", "1", "NONE"),
    ("material", "Software", "0..*", "NONE", "Hardware", "1..*", "NONE"),
    (
        "derivation",
        "material_Software_Hardware",
        "0..*",
        "NONE",
        "SoftwareExecution",
        "0..*",
        "NONE",
    ),
}

PARTICOES_ESPERADAS = {
    "agentNature": {"general": "Agent", "specifics": {"PhysicalAgent", "SocialAgent"}},
    "crudOperationType": {
        "general": "CrudOperation",
        "specifics": {
            "CreateOperation",
            "ReadOperation",
            "UpdateOperation",
            "DeleteOperation",
        },
    },
}

# As mediacoes da rodada 1 que viraram participacao, e a participacao que
# substitui cada uma. O par e o que sustenta a segunda linha da checklist: as
# relacoes que o modelo anterior expressava via mediacao continuam
# representadas.
MEDIACOES_SUBSTITUIDAS = [
    # (relator, cardRelator, mediado, cardMediado) -> (participante, evento)
    (("Observation", "0..*", "Agent", "1"), ("Agent", "Observation")),
    (("Observation", "0..*", "Disseminator", "1"), ("Disseminator", "Observation")),
    (("CrudOperation", "0..*", "Agent", "1"), ("Agent", "CrudOperation")),
    (("CrudOperation", "0..*", "CrudView", "1"), ("CrudView", "CrudOperation")),
    (("Extract", "1..*", "Collector", "1"), ("Collector", "Extract")),
    (("Extract", "1..*", "DataSource", "1"), ("DataSource", "Extract")),
    (("Transform", "1..*", "Collector", "1"), ("Collector", "Transform")),
    (("Transform", "1..*", "Processor", "1"), ("Processor", "Transform")),
    (("Load", "1..*", "Processor", "1"), ("Processor", "Load")),
    (("Load", "1..*", "Storer", "1"), ("Storer", "Load")),
]

CORRECOES = ["A5", "A6", "A7", "B8", "A1"]

REGRAS_MEDICAO = [
    "memberof_whole_not_collective",
    "parthood_ends_undeclared",
    "mediation_optional_relatum",
    "class_name_collides_with_metaconcept",
    "relator_arity_above_binary",
    "modelo_sem_perdurante",
    "modelo_sem_relacao_temporal",
]

REGRAS_GUARDA = ["evento_sem_participante", "participacao_invertida"]

# A defesa que o ticket manda apagar. `leve` sozinho nao serve como padrao: a
# gUFO e descrita como "implementacao leve da UFO" em varios lugares, e essa
# frase e sobre a ferramenta, nao sobre a ontologia produzida aqui.
RESQUICIOS_DE_ONTOLOGIA_LEVE = [
    re.compile(r"lightweight ontolog", re.IGNORECASE),
    re.compile(r"ontologia[s]? lev(e|es)", re.IGNORECASE),
]


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

    for nome, esperadas in NATUREZAS_ESPERADAS.items():
        declaradas = (modelo.classes.get(nome) or {}).get("restrictedTo")
        resultado.exigir(
            declaradas == esperadas,
            f"naturezas de {nome}: esperado {esperadas}, encontrado {declaradas}",
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

    particoes = {p["name"]: p for p in modelo.particoes()}
    resultado.exigir(
        set(particoes) == set(PARTICOES_ESPERADAS),
        f"esperadas as particoes {sorted(PARTICOES_ESPERADAS)}, achadas {sorted(particoes)}",
    )
    for nome, esperada in PARTICOES_ESPERADAS.items():
        particao = particoes.get(nome)
        if not resultado.exigir(particao is not None, f"a particao {nome} nao existe"):
            continue
        resultado.exigir(
            particao["general"] == esperada["general"]
            and particao["specifics"] == esperada["specifics"],
            f"a particao {nome} divergiu: {particao}",
        )
        resultado.exigir(
            bool(particao["isDisjoint"]) and bool(particao["isComplete"]),
            f"a particao {nome} precisa ser disjunta e completa",
        )


def verificar_ufo_b(modelo: ModeloComParticoes, resultado: Resultado) -> None:
    """A5, B8 e a leitura eventiva de A1: o que virou evento, e o que ficou."""

    eventos = {
        nome
        for nome, classe in modelo.classes.items()
        if classe.get("restrictedTo") == ["event"]
    }
    for nome in ("Extract", "Transform", "Load", "EtlProcess", "Observation", "CrudOperation"):
        resultado.exigir(nome in eventos, f"A5/B8: {nome} precisa ser um evento de natureza event")

    # Nenhum dos eventos pode ter sobrado como relator de alguma mediacao.
    for nome in eventos:
        resultado.exigir(
            not modelo.mediacoes_de(nome),
            f"A5: {nome} virou evento mas continua mediando {modelo.mediacoes_de(nome)}",
        )
    mediados = {
        modelo.nome_de(r["properties"][1]["propertyType"])
        for r in modelo.relacoes_por_estereotipo("mediation")
    }
    resultado.exigir(
        not (mediados & eventos),
        f"A5: eventos ainda aparecem como mediados: {sorted(mediados & eventos)}",
    )

    # Cada mediacao da rodada 1 tem a participacao que a substitui.
    participacoes = {
        (
            modelo.nome_de(r["properties"][0]["propertyType"]),
            modelo.nome_de(r["properties"][1]["propertyType"]),
        ): (r["properties"][0]["cardinality"], r["properties"][1]["cardinality"])
        for r in modelo.relacoes_por_estereotipo("participation")
    }
    for (relator, card_relator, mediado, card_mediado), par in MEDIACOES_SUBSTITUIDAS:
        cardinalidades = participacoes.get(par)
        resultado.exigir(
            cardinalidades == (card_mediado, card_relator),
            f"A5: a mediacao «{relator}»-«{mediado}» da rodada 1 nao tem a participacao que a "
            f"substitui com as mesmas multiplicidades: esperado "
            f"{(card_mediado, card_relator)}, encontrado {cardinalidades}",
        )

    # O ETL e um evento complexo: as tres fases sao partes proprias dele.
    for fase in ("Extract", "Transform", "Load"):
        resultado.exigir(
            modelo.tem_relacao("participational", fase, "EtlProcess"),
            f"A5: falta a «participational» de {fase} para EtlProcess",
        )

    # B8: o conhecimento passa a ser criado na observacao, e nao mediado por ela.
    resultado.exigir(
        modelo.tem_relacao("creation", "Knowledge", "Observation"),
        "B8: falta a «creation» de Knowledge em Observation",
    )
    relatores_n_arios = {
        nome: modelo.mediacoes_de(nome)
        for nome, classe in modelo.classes.items()
        if classe.get("stereotype") == "relator" and len(modelo.mediacoes_de(nome)) > 2
    }
    resultado.exigir(
        not relatores_n_arios,
        f"B8: ainda ha relator mediando mais de dois relata: {relatores_n_arios}",
    )

    # A1 sob UFO-B: as quatro operacoes acompanham o tipo geral.
    for operacao in ("CreateOperation", "ReadOperation", "UpdateOperation", "DeleteOperation"):
        resultado.exigir(
            operacao in eventos,
            f"A1: {operacao} precisa acompanhar CrudOperation e virar evento",
        )


def verificar_ufo_c(modelo: ModeloComParticoes, resultado: Resultado) -> None:
    """A6 e A7: a taxonomia de agentes e o kind sob `System`."""

    # A6: `Agent` deixa de ser o «kind» que fornecia identidade a tudo.
    resultado.exigir(
        modelo.estereotipo("Agent") == "category",
        f"A6: Agent precisa ser «category», e «{modelo.estereotipo('Agent')}»",
    )
    for kind in ("Person", "Organization"):
        resultado.exigir(
            modelo.estereotipo(kind) == "kind",
            f"A6: falta o sortal ultimo {kind}",
        )
    resultado.exigir(
        modelo.ancestrais("Person") == {"PhysicalAgent", "Agent"},
        f"A6: Person deveria ser agente fisico, e tem ancestrais {sorted(modelo.ancestrais('Person'))}",
    )
    resultado.exigir(
        modelo.ancestrais("Organization") == {"SocialAgent", "Agent"},
        "A6: Organization deveria ser agente social, e tem ancestrais "
        f"{sorted(modelo.ancestrais('Organization'))}",
    )
    resultado.exigir(
        modelo.estereotipo("StakeHolder") == "roleMixin"
        and modelo.ancestrais("StakeHolder") == {"Agent"},
        "A6: StakeHolder precisa ser um «roleMixin» sob Agent — individuo, grupo ou organizacao "
        "sao tres principios de identidade, e um papel sortal so admite um",
    )
    resultado.exigir(
        modelo.ancestrais("ObservatoryUser") == {"Person", "PhysicalAgent", "Agent"},
        "A6: ObservatoryUser precisa ter Person como provedor de identidade, e tem "
        f"{sorted(modelo.ancestrais('ObservatoryUser'))}",
    )

    # A7: o kind subjacente ao papel `System`, e a saida de `System` de sob `Agent`.
    resultado.exigir(
        modelo.estereotipo("ComputationalSystem") == "kind",
        "A7: falta o «kind» ComputationalSystem, o sortal ultimo que a dissertacao admite "
        "nao ter explicitado",
    )
    resultado.exigir(
        modelo.ancestrais("System") == {"ComputationalSystem"},
        f"A7: os ancestrais de System deveriam ser so ComputationalSystem, sao "
        f"{sorted(modelo.ancestrais('System'))}",
    )
    resultado.exigir(
        "Agent" not in modelo.ancestrais("System"),
        "A7: System ainda descende de Agent — em UFO-C um agente porta momentos intencionais, "
        "e um sistema que fornece um servico nao cre, nao pretende e nao se compromete",
    )


def verificar_metades_anteriores_intactas(diretorio: Path, resultado: Resultado) -> None:
    """Nem o baseline nem a rodada 1 podem ter sido corrigidos de passagem."""
    baseline = diretorio / "baseline" / "ontompo-as-is.ontouml.json"
    if resultado.exigir(baseline.exists(), f"{baseline} nao existe"):
        antes = Modelo(json.loads(baseline.read_text(encoding="utf-8")))
        resultado.exigir(
            antes.estereotipo("Relator") == "role"
            and antes.estereotipo("Agent") == "kind"
            and antes.estereotipo("Extract") == "relator",
            'o baseline foi corrigido de passagem: a metade "antes" perdeu seus defeitos',
        )
        resultado.exigir(
            len(antes.classes) == 32 and len(antes.relacoes) == 28,
            f"o baseline mudou de tamanho: {len(antes.classes)} classes, "
            f"{len(antes.relacoes)} relacoes",
        )

    rodada1 = diretorio / "rodada-1" / "ontompo-rodada-1.ontouml.json"
    if resultado.exigir(rodada1.exists(), f"{rodada1} nao existe"):
        anterior = Modelo(json.loads(rodada1.read_text(encoding="utf-8")))
        resultado.exigir(
            anterior.estereotipo("Agent") == "kind"
            and anterior.estereotipo("Extract") == "relator"
            and anterior.estereotipo("Observation") == "relator",
            "a rodada 1 foi alterada de passagem: ela e a metade 'antes' desta rodada e "
            "precisa continuar sem UFO-B nem UFO-C",
        )
        resultado.exigir(
            len(anterior.classes) == 38 and len(anterior.relacoes) == 32,
            f"a rodada 1 mudou de tamanho: {len(anterior.classes)} classes, "
            f"{len(anterior.relacoes)} relacoes",
        )


def verificar_relatorio_plugin(diretorio: Path, resultado: Resultado) -> None:
    rodada = diretorio / "rodada-2"
    bruto = rodada / "relatorio-plugin-ontouml.json"
    resultado.exigir((rodada / "relatorio-plugin-ontouml.md").exists(), "falta o relatorio .md")
    if not resultado.exigir(bruto.exists(), f"{bruto} nao existe"):
        return
    problemas = json.loads(bruto.read_text(encoding="utf-8"))
    resultado.exigir(isinstance(problemas, list), f"{bruto} nao e uma lista de problemas")

    for anterior in ("baseline", "rodada-1"):
        referencia = diretorio / anterior / "relatorio-plugin-ontouml.json"
        if resultado.exigir(
            referencia.exists(), f"sem o relatorio de {anterior} nao ha com o que comparar"
        ):
            do_anterior = json.loads(referencia.read_text(encoding="utf-8"))
            resultado.exigir(
                len(problemas) <= len(do_anterior),
                f"o plugin acusa mais na rodada 2 ({len(problemas)}) que em {anterior} "
                f"({len(do_anterior)})",
            )

    controle = rodada / "controle-verificacao.md"
    if resultado.exigir(
        controle.exists(),
        f"{controle} nao existe; sem ele um relatorio vazio do verificador e ininterpretavel",
    ):
        texto = controle.read_text(encoding="utf-8")
        resultado.exigir(
            "**NAO**" not in texto, "o controle da rodada 2 registra mutacao nao detectada"
        )
        resultado.exigir(
            texto.count("| sim |") >= 4,
            "o controle da rodada 2 precisa de ao menos quatro mutacoes detectadas, uma delas "
            "sobre os construtos que a rodada introduziu",
        )
        resultado.exigir(
            "generalization_incompatible_natures" in texto,
            "o controle da rodada 2 precisa exercitar a fronteira endurante/perdurante, que e "
            "o que a rodada mexeu",
        )


def verificar_verificador_microteorias(diretorio: Path, resultado: Resultado) -> None:
    rodada = diretorio / "rodada-2"
    bruto = rodada / "relatorio-verificador-ufo-b-c.json"
    relatorio_md = rodada / "relatorio-verificador-ufo-b-c.md"
    resultado.exigir(relatorio_md.exists(), "falta o relatorio do verificador de microteorias")
    if not resultado.exigir(bruto.exists(), f"{bruto} nao existe"):
        return

    relatorio = json.loads(bruto.read_text(encoding="utf-8"))
    as_is = relatorio.get("as-is", [])
    rodada1 = relatorio.get("rodada-1", [])
    rodada2 = relatorio.get("rodada-2", [])

    resultado.exigir(
        len(rodada2) < len(rodada1) < len(as_is),
        f"a medicao precisa cair a cada rodada: {len(as_is)} -> {len(rodada1)} -> {len(rodada2)}",
    )

    disparadas = {problema["code"] for problema in as_is}
    for regra in REGRAS_MEDICAO:
        resultado.exigir(
            regra in disparadas,
            f"a regra de medicao {regra} nao dispara nem sobre o baseline: sem controle "
            "positivo, o zero da rodada 2 nao e interpretavel",
        )

    erros = [problema for problema in rodada2 if problema["severity"] == "error"]
    resultado.exigir(
        not erros,
        f"a rodada 2 ainda tem erro no verificador de microteorias: "
        f"{[(p['code'], p['element']) for p in erros]}",
    )

    if relatorio_md.exists():
        texto = relatorio_md.read_text(encoding="utf-8")
        resultado.exigir(
            "**NAO**" not in texto,
            "o controle por mutacao do verificador de microteorias registra regra nao disparada",
        )
        for regra in REGRAS_GUARDA:
            resultado.exigir(
                regra in texto,
                f"a regra de guarda {regra} nao aparece no relatorio; uma regra de guarda sem "
                "controle por mutacao nao esta provada",
            )


def verificar_correcoes_documentadas(diretorio: Path, resultado: Resultado) -> None:
    caminho = diretorio / "correcoes-rodada-2.md"
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
        f"{caminho.name} nao registra a diferenca medida entre as rodadas",
    )

    bruto = diretorio / "rodada-2" / "relatorio-verificador-ufo-b-c.json"
    if bruto.exists():
        remanescentes = json.loads(bruto.read_text(encoding="utf-8")).get("rodada-2", [])
        for problema in remanescentes:
            resultado.exigir(
                problema["element"] in texto,
                f"o achado remanescente sobre `{problema['element']}` nao esta enderecado em "
                f"{caminho.name} — achado orfao e defeito",
            )


def verificar_sem_ontologia_leve(diretorio: Path, resultado: Resultado) -> None:
    """A defesa de ontologia leve nao sobrevive a adocao das microteorias.

    A varredura e literal, e por isso precisa de uma excecao literal: o
    documento desta rodada tem de poder *nomear* a defesa para registrar que
    ela caiu. A excecao nao e o arquivo inteiro — e a seccao que faz esse
    registro. Uma mencao fora dela reprova como qualquer outra.
    """
    alvos = sorted(diretorio.rglob("*.md")) + sorted(Path("tools/model").glob("*.js"))
    if not resultado.exigir(alvos, "nao ha modelo nem notas para varrer"):
        return

    correcoes = diretorio / "correcoes-rodada-2.md"
    abandono = ""
    if correcoes.exists():
        secao = re.search(
            r"^## O que esta rodada abandona junto$.*?(?=^## |\Z)",
            correcoes.read_text(encoding="utf-8"),
            re.MULTILINE | re.DOTALL,
        )
        resultado.exigir(
            secao is not None,
            f"{correcoes.name} nao registra o abandono da defesa de ontologia leve",
        )
        abandono = secao.group(0) if secao else ""

    for alvo in alvos:
        texto = alvo.read_text(encoding="utf-8")
        if alvo.resolve() == correcoes.resolve():
            texto = texto.replace(abandono, "")
        for padrao in RESQUICIOS_DE_ONTOLOGIA_LEVE:
            achado = padrao.search(texto)
            resultado.exigir(
                achado is None,
                f"resquicio da defesa de ontologia leve em {alvo}: "
                f"{achado.group(0) if achado else ''}",
            )


def verificar_owl(caminho: Path, modelo: ModeloComParticoes, resultado: Resultado) -> None:
    if not resultado.exigir(caminho.exists(), f"{caminho} nao existe"):
        return
    grafo = rdflib.Graph()
    grafo.parse(caminho.as_posix(), format="turtle")

    resultado.exigir(
        (None, rdflib.OWL.imports, rdflib.URIRef(f"{GUFO}")) in grafo,
        "a OWL da rodada 2 nao importa a gUFO",
    )

    classes_owl = {
        str(sujeito).rsplit("#", 1)[-1]
        for sujeito in grafo.subjects(rdflib.RDF.type, rdflib.OWL.Class)
        if isinstance(sujeito, rdflib.URIRef) and GUFO not in str(sujeito)
    }
    faltando = set(modelo.classes) - classes_owl
    resultado.exigir(
        not faltando, f"classes do modelo que nao chegaram a OWL da rodada 2: {sorted(faltando)}"
    )

    def local(sujeito) -> str:
        return str(sujeito).rsplit("#", 1)[-1]

    def propriedade(nome: str):
        return next(
            (
                s
                for s in grafo.subjects(rdflib.RDF.type, rdflib.OWL.ObjectProperty)
                if str(s).endswith(f"#{nome}")
            ),
            None,
        )

    # A5 e B8: os eventos chegam como gufo:Event.
    eventos_owl = {
        local(s)
        for s in grafo.subjects(rdflib.RDF.type, rdflib.URIRef(f"{GUFO}EventType"))
        if GUFO not in str(s)
    }
    for nome in ("Extract", "Transform", "Load", "EtlProcess", "Observation", "CrudOperation"):
        resultado.exigir(
            nome in eventos_owl, f"A5/B8: {nome} nao chegou a OWL como tipo de evento"
        )

    # A5: a participacao substitui a mediacao, na direcao que a gUFO exige.
    participou = rdflib.URIRef(f"{GUFO}participatedIn")
    participacoes = list(grafo.subjects(rdflib.RDFS.subPropertyOf, participou))
    resultado.exigir(
        len(participacoes) == 10,
        f"A5: esperadas dez participacoes na OWL, achadas {len(participacoes)}",
    )
    for propriedade_participacao in participacoes:
        alcance = grafo.value(propriedade_participacao, rdflib.RDFS.range)
        dominio = grafo.value(propriedade_participacao, rdflib.RDFS.domain)
        resultado.exigir(
            local(alcance) in eventos_owl and local(dominio) not in eventos_owl,
            f"A5: {local(propriedade_participacao)} tem as pontas trocadas na OWL: "
            f"{local(dominio)} -> {local(alcance)}",
        )
    for nome, esperado in (
        ("participation_Collector_Extract", ("Collector", "Extract")),
        ("participation_DataSource_Extract", ("DataSource", "Extract")),
        ("participation_Agent_Observation", ("Agent", "Observation")),
    ):
        alvo = propriedade(nome)
        if resultado.exigir(alvo is not None, f"A5: {nome} nao chegou a OWL"):
            resultado.exigir(
                (local(grafo.value(alvo, rdflib.RDFS.domain)), local(grafo.value(alvo, rdflib.RDFS.range)))
                == esperado,
                f"A5: {nome} nao vai de {esperado[0]} para {esperado[1]} na OWL",
            )

    # A5: nenhuma mediacao sobra apontando para um evento.
    medeia = rdflib.URIRef(f"{GUFO}mediates")
    for propriedade_mediacao in grafo.subjects(rdflib.RDFS.subPropertyOf, medeia):
        dominio = local(grafo.value(propriedade_mediacao, rdflib.RDFS.domain))
        alcance = local(grafo.value(propriedade_mediacao, rdflib.RDFS.range))
        resultado.exigir(
            dominio not in eventos_owl and alcance not in eventos_owl,
            f"A5: a mediacao {local(propriedade_mediacao)} ainda toca um evento",
        )

    # A5: o ETL e um evento complexo na OWL.
    parte_de_evento = rdflib.URIRef(f"{GUFO}isEventProperPartOf")
    partes = {local(s) for s in grafo.subjects(rdflib.RDFS.subPropertyOf, parte_de_evento)}
    for fase in ("Extract", "Transform", "Load"):
        resultado.exigir(
            f"participational_{fase}_EtlProcess" in partes,
            f"A5: a parthood de {fase} em EtlProcess nao chegou a OWL",
        )

    # B8: o conhecimento e criado na observacao.
    criado_em = rdflib.URIRef(f"{GUFO}wasCreatedIn")
    resultado.exigir(
        (None, rdflib.RDFS.subPropertyOf, criado_em) in grafo,
        "B8: nenhuma `gufo:wasCreatedIn` chegou a OWL",
    )

    # A6: a taxonomia de agentes chega como categoria nao-sortal.
    categorias = {
        local(s)
        for s in grafo.subjects(rdflib.RDF.type, rdflib.URIRef(f"{GUFO}Category"))
        if GUFO not in str(s)
    }
    for nome in ("Agent", "PhysicalAgent", "SocialAgent"):
        resultado.exigir(nome in categorias, f"A6: {nome} nao chegou a OWL como `gufo:Category`")
    resultado.exigir(
        (
            rdflib.URIRef(f"{caminho_base(grafo)}Agent"),
            rdflib.RDF.type,
            rdflib.URIRef(f"{GUFO}Kind"),
        )
        not in grafo,
        "A6: Agent continua sendo um `gufo:Kind` na OWL",
    )

    # A7: System nao e mais subclasse de Agent.
    sistema = next((s for s in grafo.subjects() if str(s).endswith("#System")), None)
    if sistema is not None:
        supertipos = {local(o) for o in grafo.objects(sistema, rdflib.RDFS.subClassOf)}
        resultado.exigir(
            "Agent" not in supertipos and "ComputationalSystem" in supertipos,
            f"A7: os supertipos de System na OWL sao {sorted(supertipos)}",
        )

    # As duas particoes chegam como disjuncao.
    disjuncoes = list(grafo.subjects(rdflib.RDF.type, rdflib.OWL.AllDisjointClasses))
    resultado.exigir(
        len(disjuncoes) >= 2,
        f"esperadas ao menos duas disjuncoes na OWL (agentNature e crudOperationType), "
        f"achadas {len(disjuncoes)}",
    )


def caminho_base(grafo: rdflib.Graph) -> str:
    for prefixo, iri in grafo.namespaces():
        if prefixo == "ontompo":
            return str(iri)
    return ""


def main() -> int:
    diretorio = Path(sys.argv[1]) if len(sys.argv) > 1 else DIRETORIO_PADRAO
    rodada = diretorio / "rodada-2"
    resultado = Resultado()

    modelo = carregar_modelo(rodada / "ontompo-rodada-2.ontouml.json", resultado)
    if modelo is not None:
        verificar_corresponde_ao_projetado(modelo, resultado)
        verificar_ufo_b(modelo, resultado)
        verificar_ufo_c(modelo, resultado)
        verificar_owl(rodada / "ontompo-rodada-2.ttl", modelo, resultado)

    verificar_metades_anteriores_intactas(diretorio, resultado)
    verificar_relatorio_plugin(diretorio, resultado)
    verificar_verificador_microteorias(diretorio, resultado)
    verificar_correcoes_documentadas(diretorio, resultado)
    verificar_sem_ontologia_leve(diretorio, resultado)

    for falha in resultado.falhas:
        print(f"FALHA: {falha}")

    if resultado.falhas:
        print(f"\n{len(resultado.falhas)} verificacao(oes) reprovada(s).")
        return 1
    print(
        "Rodada 2 conferida: UFO-B e UFO-C adotadas, duas metades anteriores intactas, "
        "dois relatorios, controle por mutacao e pares antes/depois."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
