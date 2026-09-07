#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifica as demais seis questoes de competencia — QC2 a QC7 (checklist do ticket 08).

Uso: python tools/verification/verificar_demais_qc.py [diretorio-ontologia]

O ticket 07 abriu a avaliacao funcional com a QC1 ponta a ponta. O ticket 08
completa as sete: as seis restantes executadas em SPARQL sobre o cenario
instanciado, com um segundo observatorio sintetico para a QC7.

Este verificador **nao importa** de `tools/generation/`: ele reabre os
artefatos e re-executa cada consulta com a sua propria rdflib, como faria um
terceiro. Confere, na ordem da checklist do ticket:

  1. as seis consultas existem, sao SELECT validas e tem ORDER BY total — todas
     as variaveis do ORDER BY estao no SELECT e a tupla delas e unica por linha,
     o que e o que torna o `.csv` salvo reproduzivel byte a byte;
  2. cada uma devolve resultado nao-vazio sobre o cenario completo;
  3. nenhuma e respondivel por uma ontologia arbitraria — cada uma cita o
     vocabulario de dominio que interroga, e dois controles negativos mostram
     que, sem a ontologia revisada *ou* sem os dados do observatorio, a consulta
     devolve zero linha, enquanto uma consulta estrutural devolve linhas sobre a
     gUFO sozinha;
  4. a QC6 devolve a cadeia de proveniencia completa, do conteudo divulgado ate
     a fonte — cada linha tem todos os nos e os vinculos entre eles conferem no
     grafo;
  5. o segundo observatorio esta instanciado, importa a rodada 2, e a QC7
     devolve conceitos cobertos so por um dos dois — a comparacao e exercitada;
  6. consultas e resultados estao salvos completos e reproduziveis: o `.csv`
     sai identico byte a byte da re-execucao independente, e o `.md` traz a
     consulta verbatim, a contagem certa e o conteudo das linhas;
  7. as divergencias entre esperado e obtido estao registradas em
     `divergencias.md`, uma por QC;
  8. nenhuma mencao identificadora ao autor, e nenhuma primeira pessoa, nos
     artefatos novos (o segundo observatorio, as consultas, as divergencias);
  9. `procedencia.md` registra as premissas do ticket 08 e como reproduzir.

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
NS_OBSB = "https://example.org/ontompo/instancia-observatorio-b#"
IRI_OBSB = URIRef("https://example.org/ontompo/instancia-observatorio-b")
ONTOMPO = rdflib.Namespace(NS_ONTOMPO)
OBS = rdflib.Namespace(NS_OBS)
OBSB = rdflib.Namespace(NS_OBSB)
GUFO = rdflib.Namespace("http://purl.org/nemo/gufo#")

CONSULTA_ESTRUTURAL = "SELECT ?s ?o WHERE { ?s <http://www.w3.org/2000/01/rdf-schema#subClassOf> ?o }"

# Termos de dominio que cada consulta tem de citar para nao ser generica.
TERMOS_DE_DOMINIO = {
    "qc2": (
        "ontompo:SocialInteraction",
        "ontompo:mediation_SocialInteraction_Reporter",
        "ontompo:StakeHolder",
        "ontompo:ProjectDataManagement",
        "ontompo:View",
    ),
    "qc3": (
        "ontompo:DataSource",
        "ontompo:participational_Extract_EtlProcess",
        "ontompo:Load",
        "gufo:participatedIn",
        "ontompo:DataManager",
    ),
    "qc4": (
        "ontompo:ProjectObservatory",
        "ontompo:ProjectDataManagement",
        "ontompo:participation_Disseminator_Observation",
        "ontompo:Software",
    ),
    "qc5": (
        "ontompo:SocialInteraction",
        "ontompo:mediation_SocialInteraction_Agent",
        "ontompo:Agent",
    ),
    "qc6": (
        "ontompo:Disseminator",
        "ontompo:participation_Storer_Load",
        "ontompo:participational_Load_EtlProcess",
        "ontompo:participation_DataSource_Extract",
        "ontompo:DataSource",
    ),
    "qc7": (
        "owl:Class",
        "skos:prefLabel",
        "rdfs:subClassOf*",
        "instancia-observatorio-b#",
    ),
}

# QC2 a QC6 se prendem ao namespace do observatorio principal; a QC7 atravessa os
# dois. As demais so deixam de valer sem os dados do principal.
QC_DO_PRINCIPAL = ("qc2", "qc3", "qc4", "qc5", "qc6")

IDENTIFICADORES = re.compile(
    r"pernambuco|garanhuns|quixad|\bcear[áa]\b|\bUPE\b|\bUFC\b|op-?upe|kvojps|"
    r"ivaldir|jeferson|\bvieira\b|santos\s+j[úu]nior|ferreira\s+dos\s+santos|"
    r"\bjos[ée]\s+ferreira\b|@upe\.br|@gmail|github\.com",
    re.IGNORECASE,
)
PRIMEIRA_PESSOA = re.compile(
    r"\bnoss[oa]s?\b|\b(eu|meu|minha|meus|minhas)\b|\b\w{2,}[aeií]mos\b",
    re.IGNORECASE,
)


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
    chave = tuple(caminho.as_posix() for caminho in caminhos)
    grafo = _CACHE_GRAFO.get(chave)
    if grafo is None:
        grafo = rdflib.Graph()
        for caminho in caminhos:
            grafo.parse(caminho.as_posix(), format="turtle")
        _CACHE_GRAFO[chave] = grafo
    return grafo


def _termo(termo) -> str:
    if termo is None:
        return ""
    if isinstance(termo, rdflib.BNode):
        return f"_:{termo}"
    return str(termo)


def _linhas(grafo: rdflib.Graph, texto: str) -> tuple[list[str], list[tuple[str, ...]]]:
    """Re-executa a consulta na ordem que o ORDER BY dela define — nao reimposta aqui."""
    resultado = grafo.query(texto)
    variaveis = [str(v) for v in resultado.vars]
    linhas = [tuple(_termo(linha[v]) for v in resultado.vars) for linha in resultado]
    return variaveis, linhas


def _csv(variaveis: list[str], linhas: list[tuple[str, ...]]) -> str:
    buffer = io.StringIO()
    escritor = csv.writer(buffer, lineterminator="\n")
    escritor.writerow(variaveis)
    escritor.writerows(linhas)
    return buffer.getvalue()


def _coluna(variaveis: list[str], linhas: list[tuple[str, ...]], nome: str) -> list[str]:
    idx = variaveis.index(nome)
    return [linha[idx] for linha in linhas]


# --------------------------------------------------------------------------- #


def _grafo_completo(diretorio: Path) -> rdflib.Graph:
    return _grafo(
        diretorio / "owl" / "ontompo.ttl",
        GUFO_LOCAL,
        diretorio / "instancias" / "observatorio.ttl",
        diretorio / "instancias" / "observatorio-b.ttl",
    )


def verificar_arquivos_e_forma(diretorio: Path, res: Resultado) -> dict[str, str]:
    """Cada consulta existe, e SELECT valida, tem ORDER BY. Devolve o texto de cada .rq."""
    textos: dict[str, str] = {}
    for qc in ("qc2", "qc3", "qc4", "qc5", "qc6", "qc7"):
        rq = diretorio / "consultas" / f"{qc}.rq"
        csv_saida = diretorio / "consultas" / f"{qc}-resultado.csv"
        md_saida = diretorio / "consultas" / f"{qc}-resultado.md"
        faltou = False
        for caminho in (rq, csv_saida, md_saida):
            if not res.exigir(caminho.exists(), f"{caminho} nao existe"):
                faltou = True
        if faltou:
            continue
        texto = _ler(rq)
        try:
            prepareQuery(texto)
        except Exception as erro:  # noqa: BLE001
            res.exigir(False, f"{qc}.rq nao e SPARQL valido: {erro}")
            continue
        res.exigir("SELECT" in texto.upper(), f"{qc}.rq nao e uma SELECT")
        res.exigir("ORDER BY" in texto.upper(), f"{qc}.rq nao tem ORDER BY — ordem nao reproduzivel")
        textos[qc] = texto
    return textos


def verificar_ordem_total(diretorio: Path, textos: dict[str, str], res: Resultado) -> None:
    """ORDER BY total: `rodar_consultas.py` nao reordena as linhas, entao o `.csv`
    salvo so e reproduzivel se o ORDER BY da consulta impuser uma ordem total.
    Substring de "ORDER BY" nao basta — aqui a tupla das variaveis do ORDER BY e
    conferida como chave unica sobre o resultado real.
    """
    grafo = _grafo_completo(diretorio)
    for qc, texto in textos.items():
        m = re.search(r"ORDER\s+BY\s+(.+?)\s*$", texto, re.IGNORECASE | re.MULTILINE)
        if not res.exigir(m is not None, f"{qc}.rq: nao foi possivel ler a clausula ORDER BY"):
            continue
        vars_ordem = re.findall(r"\?(\w+)", m.group(1))
        res.exigir(bool(vars_ordem), f"{qc}.rq: ORDER BY sem variavel")
        variaveis, linhas = _linhas(grafo, texto)
        fora = [v for v in vars_ordem if v not in variaveis]
        res.exigir(
            not fora,
            f"{qc}.rq: ORDER BY usa {fora} que nao esta(o) no SELECT — nao conferivel",
        )
        if fora or not linhas:
            continue
        idx = [variaveis.index(v) for v in vars_ordem]
        chaves = [tuple(linha[i] for i in idx) for linha in linhas]
        res.exigir(
            len(set(chaves)) == len(linhas),
            f"{qc}.rq: ORDER BY nao e ordem total sobre o resultado — "
            f"{len(linhas) - len(set(chaves))} linha(s) empatam em todas as chaves, "
            "e a ordem entre elas nao e reproduzivel",
        )


def verificar_dominio(diretorio: Path, textos: dict[str, str], res: Resultado) -> None:
    grafo = _grafo_completo(diretorio)
    so_gufo = _grafo(GUFO_LOCAL)
    _v, estrutural_no_gufo = _linhas(so_gufo, CONSULTA_ESTRUTURAL)
    res.exigir(bool(estrutural_no_gufo), "controle: consulta estrutural nao devolve nada sobre a gUFO")

    ontologia = diretorio / "owl" / "ontompo.ttl"
    obs_a = diretorio / "instancias" / "observatorio.ttl"
    obs_b = diretorio / "instancias" / "observatorio-b.ttl"

    for qc, texto in textos.items():
        for termo in TERMOS_DE_DOMINIO[qc]:
            res.exigir(termo in texto, f"{qc}.rq nao cita {termo}: precisa interrogar o dominio")

        _v, linhas = _linhas(grafo, texto)
        res.exigir(bool(linhas), f"{qc} devolve zero linha sobre o cenario completo")

        sem_ontologia = _grafo(GUFO_LOCAL, obs_a, obs_b)
        _v, linhas_sem_ontologia = _linhas(sem_ontologia, texto)
        res.exigir(
            not linhas_sem_ontologia,
            f"controle negativo falhou: {qc} devolve linhas sem a ontologia revisada",
        )

        if qc in QC_DO_PRINCIPAL:
            sem_instancia = _grafo(ontologia, GUFO_LOCAL, obs_b)
            _v, linhas_sem_instancia = _linhas(sem_instancia, texto)
            res.exigir(
                not linhas_sem_instancia,
                f"controle negativo falhou: {qc} devolve linhas sem os dados do observatorio principal",
            )
        else:  # qc7
            sem_instancias = _grafo(ontologia, GUFO_LOCAL)
            _v, linhas_sem_instancias = _linhas(sem_instancias, texto)
            res.exigir(
                not linhas_sem_instancias,
                "controle negativo falhou: qc7 devolve linhas sem nenhum dado de observatorio",
            )

        _v, qc_no_gufo = _linhas(so_gufo, texto)
        res.exigir(
            not qc_no_gufo,
            f"o contraste estrutural falhou: {qc} devolve linhas sobre a gUFO sozinha — e estrutural",
        )


def verificar_resultado_salvo(diretorio: Path, textos: dict[str, str], res: Resultado) -> None:
    grafo = _grafo_completo(diretorio)
    for qc, texto in textos.items():
        variaveis, linhas = _linhas(grafo, texto)
        csv_reexec = _csv(variaveis, linhas).encode("utf-8")
        csv_salvo = (diretorio / "consultas" / f"{qc}-resultado.csv").read_bytes()
        res.exigir(
            csv_reexec == csv_salvo,
            f"{qc}-resultado.csv nao confere byte a byte com a re-execucao independente",
        )
        md = _ler(diretorio / "consultas" / f"{qc}-resultado.md")
        res.exigir(
            texto.rstrip("\n") in md,
            f"{qc}-resultado.md nao traz a consulta verbatim — resumo nao basta para o apendice",
        )
        res.exigir(
            f"{len(linhas)} linha(s)" in md,
            f"{qc}-resultado.md nao registra as {len(linhas)} linhas do resultado",
        )
        # o conteudo das linhas, nao so a contagem: cada celula nao-IRI e nao-vazia aparece
        faltando = [
            celula
            for linha in linhas
            for celula in linha
            if celula and not celula.startswith("http") and celula.replace("\\|", "|") not in md
        ]
        res.exigir(
            not faltando,
            f"{qc}-resultado.md nao lista todo o conteudo do resultado: falta {faltando[:3]}",
        )


def verificar_qc6_cadeia(diretorio: Path, textos: dict[str, str], res: Resultado) -> None:
    if "qc6" not in textos:
        return
    grafo = _grafo_completo(diretorio)
    so_obs_a = _grafo(diretorio / "instancias" / "observatorio.ttl")
    variaveis, linhas = _linhas(grafo, textos["qc6"])

    esperadas = ["conteudo", "gerenciamento", "carga", "quando", "processoEtl", "extracao", "fonte"]
    res.exigir(
        all(v in variaveis for v in esperadas),
        f"qc6 nao devolve a cadeia inteira: variaveis {variaveis}",
    )
    res.exigir(bool(linhas), "qc6 nao devolve cadeia nenhuma")

    for linha in linhas:
        registro = dict(zip(variaveis, linha))
        for no in esperadas:
            res.exigir(bool(registro.get(no)), f"qc6: uma linha tem o no «{no}» vazio — cadeia incompleta")
        conteudo = URIRef(registro["conteudo"])
        carga = URIRef(registro["carga"])
        processo = URIRef(registro["processoEtl"])
        extracao = URIRef(registro["extracao"])
        fonte = URIRef(registro["fonte"])
        res.exigir(
            (conteudo, RDF.type, ONTOMPO.Disseminator) in so_obs_a,
            f"qc6: {registro['conteudo']} nao e uma Disseminator na instancia",
        )
        res.exigir(
            (fonte, RDF.type, ONTOMPO.DataSource) in so_obs_a,
            f"qc6: {registro['fonte']} nao e uma DataSource na instancia",
        )
        res.exigir(
            (carga, ONTOMPO.participational_Load_EtlProcess, processo) in so_obs_a,
            "qc6: a carga da linha nao e parte propria do EtlProcess apontado",
        )
        res.exigir(
            (extracao, ONTOMPO.participational_Extract_EtlProcess, processo) in so_obs_a,
            "qc6: a extracao da linha nao e parte propria do mesmo EtlProcess",
        )
        res.exigir(
            (fonte, ONTOMPO.participation_DataSource_Extract, extracao) in so_obs_a,
            "qc6: a fonte da linha nao participou da extracao apontada",
        )


def verificar_qc7_segundo_observatorio(diretorio: Path, textos: dict[str, str], res: Resultado) -> None:
    obs_b = diretorio / "instancias" / "observatorio-b.ttl"
    if not res.exigir(obs_b.exists(), f"{obs_b} nao existe — a QC7 precisa do segundo observatorio"):
        return
    so_obs_b = _grafo(obs_b)
    res.exigir(
        (IRI_OBSB, OWL.imports, IRI_ONTOMPO) in so_obs_b,
        "o segundo observatorio nao declara owl:imports da rodada 2",
    )
    res.exigir(
        not list(so_obs_b.objects(IRI_OBSB, URIRef("http://purl.org/dc/terms/creator"))),
        "o segundo observatorio declara dct:creator: a revisao e duplamente anonima",
    )
    classes_ontompo = {
        s for s in _grafo(diretorio / "owl" / "ontompo.ttl").subjects(RDF.type, OWL.Class)
        if isinstance(s, URIRef)
    }
    individuos_b = {
        s for s in so_obs_b.subjects(RDF.type, None)
        if isinstance(s, URIRef) and str(s).startswith(NS_OBSB) and s != IRI_OBSB
    }
    res.exigir(len(individuos_b) >= 10, f"segundo observatorio raso: so {len(individuos_b)} individuos")
    for individuo in sorted(individuos_b, key=str):
        tipos = [
            t for t in so_obs_b.objects(individuo, RDF.type)
            if isinstance(t, URIRef) and str(t).startswith(NS_ONTOMPO)
        ]
        res.exigir(bool(tipos), f"{individuo} do segundo observatorio nao tem tipo no namespace da OntoMPO")
        for tipo in tipos:
            res.exigir(
                tipo in classes_ontompo,
                f"{individuo} e do tipo {tipo}, que a ontologia revisada nao declara",
            )

    if "qc7" not in textos:
        return
    grafo = _grafo_completo(diretorio)
    variaveis, linhas = _linhas(grafo, textos["qc7"])
    res.exigir(
        variaveis == ["conceito", "rotuloConceito", "instanciasA", "instanciasB"],
        f"as variaveis da qc7 mudaram: {variaveis}",
    )
    pares = [(int(linha[2]), int(linha[3])) for linha in linhas]
    so_a = [c for a, b in pares if (c := (a > 0 and b == 0))]
    so_b = [c for a, b in pares if (c := (b > 0 and a == 0))]
    compartilhados = [c for a, b in pares if (c := (a > 0 and b > 0))]
    res.exigir(len(so_a) >= 1, "qc7: nenhum conceito coberto so pelo observatorio principal — sem divergencia")
    res.exigir(len(so_b) >= 1, "qc7: nenhum conceito coberto so pelo segundo observatorio — sem divergencia")
    res.exigir(len(compartilhados) >= 1, "qc7: nenhum conceito compartilhado — os cenarios nao se comparam")


def verificar_qcs_semantica(diretorio: Path, textos: dict[str, str], res: Resultado) -> None:
    grafo = _grafo_completo(diretorio)
    so_obs_a = _grafo(diretorio / "instancias" / "observatorio.ttl")

    if "qc2" in textos:
        variaveis, linhas = _linhas(grafo, textos["qc2"])
        for parte in _coluna(variaveis, linhas, "parte"):
            res.exigir(
                (URIRef(parte), RDF.type, ONTOMPO.StakeHolder) in so_obs_a,
                f"qc2: {parte} nao e uma StakeHolder na instancia",
            )
        for conteudo in _coluna(variaveis, linhas, "conteudo"):
            res.exigir(
                (URIRef(conteudo), RDF.type, ONTOMPO.Reporter) in so_obs_a,
                f"qc2: {conteudo} nao e um Reporter — o vinculo SocialInteraction so medeia Reporter",
            )

    if "qc3" in textos:
        variaveis, linhas = _linhas(grafo, textos["qc3"])
        fontes = set(_coluna(variaveis, linhas, "fonte"))
        res.exigir(len(fontes) >= 2, "qc3: menos de duas fontes — «uma dada fonte» nao e exercitado")
        for quando in _coluna(variaveis, linhas, "quando"):
            res.exigir(
                re.fullmatch(r"\d{4}-\d{2}-\d{2}", quando) is not None,
                f"qc3: «{quando}» nao e uma data — o «quando» nao foi respondido",
            )
        for fonte in fontes:
            res.exigir(
                (URIRef(fonte), RDF.type, ONTOMPO.DataSource) in so_obs_a,
                f"qc3: {fonte} nao e uma DataSource na instancia",
            )

    if "qc4" in textos:
        variaveis, linhas = _linhas(grafo, textos["qc4"])
        devolvidos = set(_coluna(variaveis, linhas, "projeto"))
        todos_projetos = {
            str(s) for s in so_obs_a.subjects(RDF.type, ONTOMPO.Project)
        }
        res.exigir(bool(devolvidos), "qc4: resultado vazio")
        res.exigir(
            devolvidos < todos_projetos,
            "qc4: devolveu todos os projetos — a consulta nao discrimina por observacao no periodo",
        )
        for projeto in devolvidos:
            res.exigir(
                (URIRef(projeto), RDF.type, ONTOMPO.Project) in so_obs_a,
                f"qc4: {projeto} nao e um Project na instancia",
            )

    if "qc5" in textos:
        variaveis, linhas = _linhas(grafo, textos["qc5"])
        tipos = set(_coluna(variaveis, linhas, "tipoAtor"))
        res.exigir(len(tipos) >= 2, "qc5: um so tipo de ator — «cada tipo» nao e exercitado")
        for motivacao in _coluna(variaveis, linhas, "motivacao"):
            res.exigir(bool(motivacao.strip()), "qc5: uma linha tem motivacao vazia")

    if "qc6" in textos:
        variaveis, linhas = _linhas(grafo, textos["qc6"])
        res.exigir(len(linhas) >= 2, "qc6: menos de duas cadeias — o cenario e raso demais")


def verificar_divergencias(diretorio: Path, res: Resultado) -> None:
    caminho = diretorio / "consultas" / "divergencias.md"
    if not res.exigir(caminho.exists(), f"{caminho} nao existe"):
        return
    texto = _ler(caminho)
    res.exigir(len(texto) > 2000, "divergencias.md e curto demais para registrar seis QCs")
    for qc in ("QC2", "QC3", "QC4", "QC5", "QC6", "QC7"):
        res.exigir(qc in texto, f"divergencias.md nao registra a {qc}")
    for marca in ("Esperado", "Obtido", "Divergência"):
        res.exigir(marca in texto, f"divergencias.md nao usa a marca «{marca}»")


def verificar_procedencia(diretorio: Path, res: Resultado) -> None:
    caminho = diretorio / "instancias" / "procedencia.md"
    if not res.exigir(caminho.exists(), f"{caminho} nao existe"):
        return
    texto = _ler(caminho)
    for marca in (
        "observatorio-b",
        "gerenciadorDeColeta",
        "verificar_demais_qc.py",
        "fontePlanilhaDadosAbertos",
        "Premissa",
        "sintético",
    ):
        res.exigir(marca in texto, f"procedencia.md nao registra «{marca}»")


def verificar_anonimato(diretorio: Path, res: Resultado) -> None:
    novos = [
        diretorio / "instancias" / "observatorio-b.ttl",
        diretorio / "consultas" / "divergencias.md",
    ]
    novos += sorted((diretorio / "consultas").glob("qc[2-7]*"))
    for caminho in novos:
        if not caminho.is_file():
            continue
        texto = _ler(caminho)
        achado = IDENTIFICADORES.search(texto)
        res.exigir(
            achado is None,
            f"{caminho.name} traz mencao identificadora: «{achado.group(0) if achado else ''}»",
        )
    for caminho in (
        diretorio / "instancias" / "observatorio-b.ttl",
        diretorio / "consultas" / "divergencias.md",
    ):
        achado = PRIMEIRA_PESSOA.search(_ler(caminho))
        res.exigir(
            achado is None,
            f"{caminho.name} usa primeira pessoa («{achado.group(0) if achado else ''}»): "
            "o cenario vai em terceira pessoa",
        )


def main() -> int:
    diretorio = Path(sys.argv[1]) if len(sys.argv) > 1 else ONTOLOGIA_PADRAO
    res = Resultado()

    textos = verificar_arquivos_e_forma(diretorio, res)
    if textos:
        verificar_ordem_total(diretorio, textos, res)
        verificar_dominio(diretorio, textos, res)
        verificar_resultado_salvo(diretorio, textos, res)
        verificar_qc6_cadeia(diretorio, textos, res)
        verificar_qc7_segundo_observatorio(diretorio, textos, res)
        verificar_qcs_semantica(diretorio, textos, res)
    verificar_divergencias(diretorio, res)
    verificar_procedencia(diretorio, res)
    verificar_anonimato(diretorio, res)

    print(f"verificacoes: {res.checagens}")
    if res.falhas:
        print(f"FALHOU: {len(res.falhas)} problema(s)")
        for falha in res.falhas:
            print(f"  - {falha}")
        return 1
    print("OK: a checklist do ticket 08 esta cumprida")
    return 0


if __name__ == "__main__":
    sys.exit(main())
