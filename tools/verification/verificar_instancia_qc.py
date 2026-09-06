#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifica a instanciacao e a primeira questao de competencia (checklist do ticket 07).

Uso: python tools/verification/verificar_instancia_qc.py [diretorio-ontologia]

Confere, na ordem da checklist do ticket:

  1. os dados de instancia do observatorio carregam na ontologia revisada — o
     arquivo faz parse junto de `owl/ontompo.ttl` e da gUFO, importa a rodada 2,
     e todo individuo tem por tipo uma classe que a ontologia declara;
  2. uma QC de dominio foi escolhida e executada ponta a ponta — a consulta
     `consultas/qc1.rq` e uma SELECT valida, e o resultado esta salvo em `.csv`
     e em `.md`;
  3. a consulta interroga o dominio, nao a estrutura: ela cita o vocabulario da
     OntoMPO (o relator `ViewProvision`, o `DataManager` alvo), e **nao passa se
     puder ser respondida por qualquer ontologia** — dois controles negativos
     mostram que, sem a ontologia revisada *ou* sem os dados do observatorio, a
     mesma consulta devolve zero linha, enquanto uma consulta estrutural devolve
     linhas sobre a gUFO sozinha;
  4. o resultado e nao-vazio e semanticamente correto: o conjunto de Views
     devolvido e exatamente o das Views componentes do observatorio, uma por
     funcionalidade que a publicacao documenta, e cada papel e um subtipo de
     `View`;
  5. consulta e resultado estao salvos em formato reaproveitavel: re-executando
     a consulta com codigo proprio e comparando os bytes crus, o `.csv` sai
     identico, e o `.md` traz a consulta verbatim e a contagem certa;
  6. nenhuma mencao identificadora ao autor sobrevive nos dados, nas consultas
     ou na procedencia;
  7. o percurso e reproduzivel por um terceiro a partir dos artefatos salvos —
     este verificador **nao importa** de `tools/generation/`: ele reabre os
     arquivos e re-executa a consulta com a sua propria rdflib.

Sai com codigo 1 se qualquer verificacao falhar.
"""

from __future__ import annotations

import csv
import io
import re
import sys
from pathlib import Path

try:
    import rdflib
    from rdflib import OWL, RDF, RDFS, URIRef
    from rdflib.plugins.sparql import prepareQuery
except ImportError as erro:  # pragma: no cover - dependencia ausente
    print(f"ERRO: dependencia ausente ({erro.name}). Rode: pip install rdflib")
    sys.exit(1)

ONTOLOGIA_PADRAO = Path("artifacts/ontology")
GUFO_LOCAL = Path("sources/gufo/gufo.ttl")

NS_ONTOMPO = "https://example.org/ontompo/rodada-2#"
IRI_ONTOMPO = URIRef("https://example.org/ontompo/rodada-2")
NS_OBS = "https://example.org/ontompo/instancia-observatorio#"
IRI_OBS = URIRef("https://example.org/ontompo/instancia-observatorio")
OBS = rdflib.Namespace(NS_OBS)
ONTOMPO = rdflib.Namespace(NS_ONTOMPO)

DOI_FONTE = "10.5753/sbsi_estendido.2022.222995"

# Papeis de View e seus rotulos preferidos em pt-BR, transcritos da ontologia
# revisada — nao lidos dela, para que uma divergencia acuse.
PAPEIS_DE_VIEW = {"CrudView": "Visão CRUD", "Disseminator": "Disseminação", "Reporter": "Relacionamento"}

# Individuos cujo nome local tem de aparecer em procedencia.md, um a um. Os oito
# relatores `disponibilizacaoDe_*` ficam de fora da lista porque procedencia.md
# os descreve por padrao; a presenca do padrao e conferida a parte.
TIPOS_RASTREADOS = {
    "ProjectObservatory",
    "DataManager",
    "CrudView",
    "Disseminator",
    "Reporter",
    "ObservatoryUser",
    "System",
}

# Qualquer um destes num artefato do cenario reprova a verificacao de anonimato.
IDENTIFICADORES = re.compile(
    r"pernambuco|garanhuns|quixad|\bcear[áa]\b|\bUPE\b|\bUFC\b|op-?upe|kvojps|"
    r"ivaldir|jeferson|\bvieira\b|santos\s+j[úu]nior|ferreira\s+dos\s+santos|"
    r"\bjos[ée]\s+ferreira\b|@upe\.br|@gmail|github\.com",
    re.IGNORECASE,
)
# Marcas de primeira pessoa: os pronomes/possessivos e a desinencia -mos de
# primeira pessoa do plural (desenvolvemos, realizamos, adotamos, propomos...),
# que e como o autor descreveria o proprio trabalho anterior.
PRIMEIRA_PESSOA = re.compile(
    r"\bnoss[oa]s?\b|\b(eu|meu|minha|meus|minhas)\b|\b\w{2,}[aeií]mos\b",
    re.IGNORECASE,
)

CONSULTA_ESTRUTURAL = "SELECT ?s ?o WHERE { ?s <http://www.w3.org/2000/01/rdf-schema#subClassOf> ?o }"


class Resultado:
    def __init__(self) -> None:
        self.falhas: list[str] = []
        self.checagens = 0

    def exigir(self, condicao: bool, mensagem: str) -> bool:
        self.checagens += 1
        if not condicao:
            self.falhas.append(mensagem)
        return bool(condicao)


def _ler(caminho: Path) -> str:
    return caminho.read_text(encoding="utf-8")


_CACHE_GRAFO: dict[tuple[str, ...], rdflib.Graph] = {}


def _grafo(*caminhos: Path) -> rdflib.Graph:
    """Grafo com um ou mais Turtles carregados.

    Memoizado por combinacao de caminhos: as mesmas combinacoes (gUFO sozinha, a
    ontologia com a gUFO, o cenario inteiro) sao consultadas por varias
    verificacoes, e reparsear a gUFO a cada uma custa. Os grafos nunca sao
    modificados depois de carregados — so consultados —, entao compartilha-los e
    seguro.
    """
    chave = tuple(caminho.as_posix() for caminho in caminhos)
    grafo = _CACHE_GRAFO.get(chave)
    if grafo is None:
        grafo = rdflib.Graph()
        for caminho in caminhos:
            grafo.parse(caminho.as_posix(), format="turtle")
        _CACHE_GRAFO[chave] = grafo
    return grafo


def _nome_local(iri: URIRef) -> str:
    return str(iri).rsplit("#", 1)[-1]


def _linhas_da_consulta(grafo: rdflib.Graph, texto: str) -> tuple[list[str], list[tuple[str, ...]]]:
    """Re-executa a consulta com codigo proprio, na ordem que o ORDER BY dela define.

    A ordem nao e reimposta aqui: o `rodar_consultas.py` tambem confia no
    `ORDER BY` da consulta, e a comparacao byte a byte do CSV so fecha se os dois
    lados usarem a mesma ordem.
    """
    resultado = grafo.query(texto)
    variaveis = [str(v) for v in resultado.vars]
    linhas = [tuple(_termo(linha[v]) for v in resultado.vars) for linha in resultado]
    return variaveis, linhas


def _termo(termo) -> str:
    if termo is None:
        return ""
    if isinstance(termo, rdflib.BNode):
        return f"_:{termo}"
    return str(termo)


def _csv(variaveis: list[str], linhas: list[tuple[str, ...]]) -> str:
    buffer = io.StringIO()
    escritor = csv.writer(buffer, lineterminator="\n")
    escritor.writerow(variaveis)
    escritor.writerows(linhas)
    return buffer.getvalue()


# --------------------------------------------------------------------------- #


def verificar_carrega(diretorio: Path, resultado: Resultado):
    instancia = diretorio / "instancias" / "observatorio.ttl"
    ontologia = diretorio / "owl" / "ontompo.ttl"
    for caminho in (instancia, ontologia, GUFO_LOCAL):
        if not resultado.exigir(caminho.exists(), f"{caminho} nao existe"):
            return None

    try:
        grafo = _grafo(ontologia, GUFO_LOCAL, instancia)
    except Exception as erro:  # noqa: BLE001 - qualquer erro de parse conta
        resultado.exigir(False, f"os tres arquivos nao carregam juntos: {erro}")
        return None

    so_instancia = _grafo(instancia)
    resultado.exigir(
        (IRI_OBS, OWL.imports, IRI_ONTOMPO) in so_instancia,
        "os dados de instancia nao declaram owl:imports da rodada 2",
    )
    resultado.exigir(
        not list(so_instancia.objects(IRI_OBS, rdflib.term.URIRef("http://purl.org/dc/terms/creator"))),
        "os dados de instancia declaram dct:creator: a revisao e duplamente anonima",
    )

    classes_ontompo = {
        s for s in _grafo(ontologia).subjects(RDF.type, OWL.Class) if isinstance(s, URIRef)
    }
    individuos = {
        s
        for s in so_instancia.subjects(RDF.type, None)
        if isinstance(s, URIRef) and str(s).startswith(NS_OBS) and s != IRI_OBS
    }
    resultado.exigir(len(individuos) >= 10, f"so ha {len(individuos)} individuos: cenario raso demais")
    for individuo in sorted(individuos, key=str):
        tipos_dominio = [
            t
            for t in so_instancia.objects(individuo, RDF.type)
            if isinstance(t, URIRef) and str(t).startswith(NS_ONTOMPO)
        ]
        resultado.exigir(
            bool(tipos_dominio),
            f"{_nome_local(individuo)} nao tem tipo no namespace da OntoMPO",
        )
        for tipo in tipos_dominio:
            resultado.exigir(
                tipo in classes_ontompo,
                f"{_nome_local(individuo)} e do tipo {_nome_local(tipo)}, que a ontologia revisada "
                "nao declara como owl:Class",
            )
    return grafo, so_instancia, individuos


def verificar_procedencia(diretorio: Path, individuos: set, resultado: Resultado) -> None:
    procedencia = diretorio / "instancias" / "procedencia.md"
    if not resultado.exigir(procedencia.exists(), f"{procedencia} nao existe"):
        return
    texto = _ler(procedencia)
    resultado.exigir(DOI_FONTE in texto, "procedencia.md nao cita o DOI da publicacao-fonte")
    resultado.exigir(
        "terceira pessoa" in texto,
        "procedencia.md nao registra que a fonte e referida em terceira pessoa",
    )
    resultado.exigir(
        "disponibilizacaoDe_" in texto and "ViewProvision" in texto,
        "procedencia.md nao descreve o padrao dos relatores ViewProvision",
    )
    for comando in (
        "gerar_instancias.py",
        "rodar_consultas.py",
        "verificar_instancia_qc.py",
    ):
        resultado.exigir(comando in texto, f"procedencia.md nao diz como reproduzir ({comando})")

    so_instancia = _grafo(diretorio / "instancias" / "observatorio.ttl")
    for individuo in sorted(individuos, key=str):
        tipos = {_nome_local(t) for t in so_instancia.objects(individuo, RDF.type)}
        if tipos & TIPOS_RASTREADOS:
            resultado.exigir(
                _nome_local(individuo) in texto,
                f"{_nome_local(individuo)} nao aparece em procedencia.md — instancia orfa",
            )


def verificar_consulta_existe(diretorio: Path, resultado: Resultado) -> str | None:
    rq = diretorio / "consultas" / "qc1.rq"
    csv_saida = diretorio / "consultas" / "qc1-resultado.csv"
    md_saida = diretorio / "consultas" / "qc1-resultado.md"
    for caminho in (rq, csv_saida, md_saida):
        if not resultado.exigir(caminho.exists(), f"{caminho} nao existe"):
            return None
    texto = _ler(rq)
    try:
        prepareQuery(texto)
    except Exception as erro:  # noqa: BLE001
        resultado.exigir(False, f"qc1.rq nao e uma consulta SPARQL valida: {erro}")
        return None
    resultado.exigir("SELECT" in texto.upper(), "qc1.rq nao e uma SELECT")
    return texto


def verificar_consulta_de_dominio(
    diretorio: Path, grafo_completo: rdflib.Graph, texto_consulta: str, resultado: Resultado
) -> None:
    for termo in (
        "ontompo:ViewProvision",
        "ontompo:mediation_ViewProvision_DataManager",
        "ontompo:View",
        "obs:gerenciadorDeConteudo",
    ):
        resultado.exigir(
            termo in texto_consulta,
            f"qc1.rq nao cita {termo}: a consulta precisa interrogar o vocabulario de dominio",
        )

    _vars, linhas = _linhas_da_consulta(grafo_completo, texto_consulta)
    resultado.exigir(bool(linhas), "qc1 devolve zero linha sobre o cenario completo")

    ontologia = diretorio / "owl" / "ontompo.ttl"
    instancia = diretorio / "instancias" / "observatorio.ttl"

    sem_instancia = _grafo(ontologia, GUFO_LOCAL)
    _v, linhas_sem_instancia = _linhas_da_consulta(sem_instancia, texto_consulta)
    resultado.exigir(
        not linhas_sem_instancia,
        "controle negativo falhou: qc1 devolve linhas sem os dados do observatorio — "
        "a consulta nao depende do cenario",
    )

    sem_ontologia = _grafo(GUFO_LOCAL, instancia)
    _v, linhas_sem_ontologia = _linhas_da_consulta(sem_ontologia, texto_consulta)
    resultado.exigir(
        not linhas_sem_ontologia,
        "controle negativo falhou: qc1 devolve linhas sem a ontologia revisada — "
        "a consulta nao depende da estrutura que a analise introduziu",
    )

    so_gufo = _grafo(GUFO_LOCAL)
    _v, qc1_no_gufo = _linhas_da_consulta(so_gufo, texto_consulta)
    _v, estrutural_no_gufo = _linhas_da_consulta(so_gufo, CONSULTA_ESTRUTURAL)
    resultado.exigir(
        not qc1_no_gufo and bool(estrutural_no_gufo),
        "o contraste estrutural falhou: uma consulta de subClassOf devolve linhas sobre a gUFO "
        "sozinha e a qc1 deveria devolver zero — se as duas se comportam igual, a qc1 e estrutural",
    )


def verificar_resultado_semantico(
    diretorio: Path, grafo_completo: rdflib.Graph, texto_consulta: str, resultado: Resultado
) -> None:
    variaveis, linhas = _linhas_da_consulta(grafo_completo, texto_consulta)
    resultado.exigir(
        variaveis == ["view", "rotuloView", "papel", "rotuloPapel"],
        f"as variaveis da qc1 mudaram: {variaveis}",
    )

    so_instancia = _grafo(diretorio / "instancias" / "observatorio.ttl")
    views_componentes = {
        str(v)
        for v in so_instancia.subjects(ONTOMPO.componentOf_View_ProjectObservatory, OBS.observatorio)
    }
    provisoes = {
        str(p)
        for p in so_instancia.subjects(
            ONTOMPO.mediation_ViewProvision_DataManager, OBS.gerenciadorDeConteudo
        )
    }
    views_no_resultado = {linha[0] for linha in linhas}

    resultado.exigir(
        views_no_resultado == views_componentes,
        "as Views devolvidas nao sao exatamente as Views componentes do observatorio: "
        f"faltam {views_componentes - views_no_resultado or '—'}, "
        f"sobram {views_no_resultado - views_componentes or '—'}",
    )
    resultado.exigir(
        len(linhas) == len(provisoes) == len(views_componentes),
        f"contagem inconsistente: {len(linhas)} linhas, {len(provisoes)} relatores, "
        f"{len(views_componentes)} Views componentes",
    )
    resultado.exigir(len(linhas) >= 5, f"so {len(linhas)} linhas: cenario raso demais para um tracer")

    papeis = {linha[2].rsplit("#", 1)[-1] for linha in linhas}
    rotulos_papel = {linha[3] for linha in linhas}
    resultado.exigir(
        papeis <= set(PAPEIS_DE_VIEW),
        f"a qc1 devolveu um papel que nao e subtipo de View: {papeis - set(PAPEIS_DE_VIEW)}",
    )
    resultado.exigir(
        len(papeis) >= 2,
        "a qc1 devolveu um so papel: o cenario nao exercita a distincao entre visoes",
    )
    resultado.exigir(
        rotulos_papel <= set(PAPEIS_DE_VIEW.values()),
        f"rotulo de papel inesperado: {rotulos_papel - set(PAPEIS_DE_VIEW.values())}",
    )

    procedencia = _ler(diretorio / "instancias" / "procedencia.md")
    for linha in linhas:
        resultado.exigir(
            linha[1] in procedencia,
            f"a View «{linha[1]}» devolvida pela qc1 nao esta documentada em procedencia.md",
        )


def verificar_resultado_salvo(
    diretorio: Path, grafo_completo: rdflib.Graph, texto_consulta: str, resultado: Resultado
) -> None:
    variaveis, linhas = _linhas_da_consulta(grafo_completo, texto_consulta)
    csv_reexecutado = _csv(variaveis, linhas).encode("utf-8")
    csv_salvo = (diretorio / "consultas" / "qc1-resultado.csv").read_bytes()
    resultado.exigir(
        csv_reexecutado == csv_salvo,
        "qc1-resultado.csv nao confere byte a byte com a re-execucao independente da consulta — "
        "o resultado salvo nao e reproduzivel",
    )

    md = _ler(diretorio / "consultas" / "qc1-resultado.md")
    resultado.exigir(
        texto_consulta.rstrip("\n") in md,
        "qc1-resultado.md nao traz a consulta verbatim — resumo nao basta para o apendice",
    )
    resultado.exigir(
        f"{len(linhas)} linha(s)" in md,
        f"qc1-resultado.md nao registra as {len(linhas)} linhas do resultado",
    )
    for linha in linhas:
        resultado.exigir(
            linha[1] in md,
            f"qc1-resultado.md nao lista a View «{linha[1]}» — resultado incompleto",
        )


def verificar_anonimato(diretorio: Path, resultado: Resultado) -> None:
    alvos = [
        diretorio / "instancias" / "observatorio.ttl",
        diretorio / "instancias" / "procedencia.md",
    ]
    alvos += sorted((diretorio / "consultas").glob("*"))
    for caminho in alvos:
        if not caminho.is_file():
            continue
        texto = _ler(caminho)
        achado = IDENTIFICADORES.search(texto)
        resultado.exigir(
            achado is None,
            f"{caminho.name} traz uma mencao identificadora: «{achado.group(0) if achado else ''}»",
        )

    for caminho in (
        diretorio / "instancias" / "procedencia.md",
        diretorio / "instancias" / "observatorio.ttl",
    ):
        achado = PRIMEIRA_PESSOA.search(_ler(caminho))
        resultado.exigir(
            achado is None,
            f"{caminho.name} usa primeira pessoa («{achado.group(0) if achado else ''}»): "
            "o cenario e trabalho anterior e vai em terceira pessoa",
        )


def main() -> int:
    diretorio = Path(sys.argv[1]) if len(sys.argv) > 1 else ONTOLOGIA_PADRAO
    resultado = Resultado()

    carregado = verificar_carrega(diretorio, resultado)
    texto_consulta = verificar_consulta_existe(diretorio, resultado)

    if carregado is not None and texto_consulta is not None:
        grafo_completo, _so_instancia, individuos = carregado
        verificar_procedencia(diretorio, individuos, resultado)
        verificar_consulta_de_dominio(diretorio, grafo_completo, texto_consulta, resultado)
        verificar_resultado_semantico(diretorio, grafo_completo, texto_consulta, resultado)
        verificar_resultado_salvo(diretorio, grafo_completo, texto_consulta, resultado)

    verificar_anonimato(diretorio, resultado)

    print(f"verificacoes: {resultado.checagens}")
    if resultado.falhas:
        print(f"FALHOU: {len(resultado.falhas)} problema(s)")
        for falha in resultado.falhas:
            print(f"  - {falha}")
        return 1
    print("OK: a checklist do ticket 07 esta cumprida")
    return 0


if __name__ == "__main__":
    sys.exit(main())
