#!/usr/bin/env python3
"""Roda o OOPS! sobre uma ontologia e salva o relatorio.

Uso: python scripts/rodar_oops.py [caminho-do-ttl] [diretorio-de-saida]

O OOPS! (OntOlogy Pitfall Scanner!) so aceita RDF/XML no servico REST, entao a
Turtle produzida pela transformacao gUFO e convertida com a rdflib antes do
envio. Sao gravados tres arquivos ao lado do modelo:

  - `<nome>.owl`            o baseline em RDF/XML, completo;
  - `<nome>.oops.owl`       a copia efetivamente submetida, sem o `owl:imports`,
                            para que a execucao possa ser repetida byte a byte;
  - `relatorio-oops.xml`    a resposta bruta do servico;
  - `relatorio-oops.md`     o mesmo conteudo em tabela legivel.

A declaracao `owl:imports gufo:` e removida da copia enviada. Com ela presente o
servico devolve `unexpected_error` — tenta dereferenciar a gUFO e desiste. A
remocao tambem e o recorte correto: o que esta sob avaliacao e a ontologia de
dominio, nao a ontologia de fundamentacao que ela importa. Os dois arquivos sao
gravados, o completo e o submetido, para que a diferenca fique visivel.

Sai com codigo 1 se a chamada falhar. Uma falha de rede nao e mascarada: sem
resposta do servico nao ha relatorio, e o ticket 03 pede o relatorio em arquivo.
"""

from __future__ import annotations

import hashlib
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

try:
    import rdflib
    import requests
except ImportError as erro:  # pragma: no cover - dependencia ausente
    print(f"ERRO: dependencia ausente ({erro.name}). Rode: pip install rdflib requests")
    sys.exit(1)

TTL_PADRAO = Path("ontologia/baseline/ontompo-as-is.ttl")
ENDPOINT = "https://oops.linkeddata.es/rest"
TEMPO_LIMITE_S = 300

OOPS = "http://oops.linkeddata.es/def#"
RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"

# Ordem de gravidade que o OOPS! usa nos seus proprios relatorios.
ORDEM_IMPORTANCIA = {"Critical": 0, "Important": 1, "Minor": 2}


def carregar(caminho_ttl: Path) -> rdflib.Graph:
    grafo = rdflib.Graph()
    grafo.parse(caminho_ttl.as_posix(), format="turtle")
    return _normalizado(grafo)


def _rotulo(grafo: rdflib.Graph, no: rdflib.term.BNode, rotulos: dict) -> str | None:
    """Rotulo derivado do conteudo do no, ou None se algum filho ainda nao tem rotulo."""
    partes = []
    for predicado, objeto in grafo.predicate_objects(no):
        if isinstance(objeto, rdflib.term.BNode):
            if objeto not in rotulos:
                return None
            partes.append(f"{predicado} {rotulos[objeto]}")
        else:
            partes.append(f"{predicado} {objeto}")
    assinatura = chr(10).join(sorted(partes))
    return f"n{hashlib.sha1(assinatura.encode('utf-8')).hexdigest()[:20]}"


def _normalizado(grafo: rdflib.Graph) -> rdflib.Graph:
    """Copia do grafo com nos anonimos rotulados de forma deterministica.

    A rdflib sorteia o rotulo dos nos anonimos a cada execucao, e a Turtle da
    transformacao gUFO tem uma restricao anonima por mediacao. Sem isto, dois
    `gerar-baseline` seguidos produziriam RDF/XML diferentes sem que nada no
    modelo tivesse mudado, e o diff contra o modelo revisado do ticket 04 seria
    ilegivel. O `to_canonical_graph` da propria rdflib nao serve: ele desempata
    nos isomorfos por sorteio e nao e estavel entre execucoes.

    O rotulo e o hash do conteudo do no, resolvido de dentro para fora — as
    restricoes do gUFO aninham um nivel, em `owl:onProperty [ owl:inverseOf ... ]`.
    Dois nos de conteudo identico colidiriam; a colisao e detectada e falha,
    em vez de fundir silenciosamente dois nos distintos.
    """
    anonimos = {t for tripla in grafo for t in tripla if isinstance(t, rdflib.term.BNode)}
    rotulos: dict = {}
    while len(rotulos) < len(anonimos):
        avancou = False
        for no in anonimos - set(rotulos):
            rotulo = _rotulo(grafo, no, rotulos)
            if rotulo is not None:
                rotulos[no] = rotulo
                avancou = True
        if not avancou:
            raise RuntimeError("ciclo entre nos anonimos: rotulacao deterministica nao converge")

    if len(set(rotulos.values())) != len(rotulos):
        raise RuntimeError("colisao de rotulo entre nos anonimos")

    normalizado = rdflib.Graph()
    for prefixo, iri in grafo.namespaces():
        normalizado.bind(prefixo, iri)
    def substituir(termo):
        return rdflib.term.BNode(rotulos[termo]) if isinstance(termo, rdflib.term.BNode) else termo

    triplas = [tuple(substituir(termo) for termo in tripla) for tripla in grafo]
    for tripla in sorted(triplas, key=lambda t: (str(t[0]), str(t[1]), str(t[2]))):
        normalizado.add(tripla)
    return normalizado


def sem_importacoes(grafo: rdflib.Graph) -> rdflib.Graph:
    """Copia do grafo sem `owl:imports`, que faz o servico do OOPS! falhar."""
    recorte = rdflib.Graph()
    for prefixo, iri in grafo.namespaces():
        recorte.bind(prefixo, iri)
    for tripla in grafo:
        if tripla[1] != rdflib.OWL.imports:
            recorte.add(tripla)
    return recorte


def consultar_oops(rdf_xml: str) -> str:
    corpo = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        "<OOPSRequest>\n"
        "<OntologyURI></OntologyURI>\n"
        f"<OntologyContent><![CDATA[{rdf_xml}]]></OntologyContent>\n"
        "<Pitfalls></Pitfalls>\n"
        "<OutputFormat>RDF/XML</OutputFormat>\n"
        "</OOPSRequest>"
    )
    resposta = requests.post(
        ENDPOINT,
        data=corpo.encode("utf-8"),
        headers={"Content-Type": "application/xml;charset=UTF-8"},
        timeout=TEMPO_LIMITE_S,
    )
    resposta.raise_for_status()
    return resposta.text


def _texto(no: ET.Element, tag: str) -> str | None:
    filho = no.find(f"{{{OOPS}}}{tag}")
    return filho.text if filho is not None else None


def _textos(no: ET.Element, tag: str) -> list[str]:
    return [f.text for f in no.findall(f"{{{OOPS}}}{tag}") if f.text]


def extrair_pitfalls(xml_resposta: str) -> list[dict]:
    raiz = ET.fromstring(xml_resposta)
    achados = []
    for descricao in raiz.findall(f"{{{RDF}}}Description"):
        tipos = {t.get(f"{{{RDF}}}resource") for t in descricao.findall(f"{{{RDF}}}type")}
        if f"{OOPS}pitfall" not in tipos and f"{OOPS}warning" not in tipos:
            continue
        achados.append(
            {
                "tipo": "pitfall" if f"{OOPS}pitfall" in tipos else "warning",
                "codigo": _texto(descricao, "hasCode") or "",
                "nome": (_texto(descricao, "hasName") or "").strip(),
                "descricao": (_texto(descricao, "hasDescription") or "").strip(),
                "importancia": _texto(descricao, "hasImportanceLevel") or "",
                "elementos": sorted(
                    _textos(descricao, "hasAffectedElement"),
                    key=lambda elemento: (not _e_iri(elemento), elemento),
                ),
                "quantidade": _texto(descricao, "hasNumberAffectedElements") or "",
            }
        )
    achados.sort(
        key=lambda a: (ORDEM_IMPORTANCIA.get(a["importancia"], 9), a["codigo"], a["nome"])
    )
    return achados


def _e_iri(elemento: str) -> bool:
    """O OOPS! devolve um id interno proprio, e nao um IRI, para nos anonimos."""
    return "#" in elemento or "/" in elemento


def nome_curto(iri: str) -> str:
    for separador in ("#", "/"):
        if separador in iri:
            return iri.rsplit(separador, 1)[-1] or iri
    return iri


def _nomes_ambiguos(achados: list[dict]) -> set[str]:
    """Nomes curtos que o relatorio nao pode encurtar sem virar mentira.

    A colisao entre `ontompo:Relator`, a classe de dominio, e `gufo:Relator`, o
    metaconceito da UFO, e o achado A4 — e aparece justamente aqui, com os dois
    IRIs listados como elementos afetados pelo mesmo pitfall. Encurtar os dois
    para `Relator` apagaria a evidencia.
    """
    por_nome: dict[str, set[str]] = {}
    for achado in achados:
        for elemento in achado["elementos"]:
            if _e_iri(elemento):
                por_nome.setdefault(nome_curto(elemento), set()).add(elemento)
    return {nome for nome, iris in por_nome.items() if len(iris) > 1}


def relatorio_em_markdown(achados: list[dict], caminho_ttl: Path, momento: str) -> str:
    ambiguos = _nomes_ambiguos(achados)
    linhas = [
        "# Relatorio do OOPS! sobre o modelo *as-is*",
        "",
        f"Ontologia submetida: `{caminho_ttl.name}`, convertida para RDF/XML e enviada ao "
        f"servico REST do OOPS! (`{ENDPOINT}`) em {momento}. Resposta bruta em "
        "`relatorio-oops.xml`; a copia exata submetida, em "
        f"`{caminho_ttl.stem}.oops.owl`.",
        "",
        "A declaracao `owl:imports gufo:` foi removida da copia submetida — com ela o "
        "servico devolve `unexpected_error`. O recorte tambem e o correto: o que esta "
        "sob avaliacao e a ontologia de dominio, nao a gUFO que ela importa.",
        "",
        f"- Achados: {len(achados)}",
    ]
    por_importancia: dict[str, int] = {}
    for achado in achados:
        por_importancia[achado["importancia"]] = por_importancia.get(achado["importancia"], 0) + 1
    if por_importancia:
        resumo = ", ".join(
            f"{nivel or 'sem nivel'} {quantidade}"
            for nivel, quantidade in sorted(
                por_importancia.items(), key=lambda par: ORDEM_IMPORTANCIA.get(par[0], 9)
            )
        )
        linhas.append(f"- Por nivel de importancia: {resumo}")
    linhas.append("")

    if not achados:
        linhas.append("Nenhum pitfall encontrado.")
        return "\n".join(linhas) + "\n"

    linhas.append("| Codigo | Pitfall | Importancia | Elementos afetados |")
    linhas.append("|---|---|---|---|")
    for achado in achados:
        linhas.append(
            f"| `{achado['codigo']}` | {achado['nome']} | {achado['importancia']} | "
            f"{achado['quantidade']} |"
        )
    linhas.append("")
    linhas.append("## Detalhamento")
    linhas.append("")
    for achado in achados:
        linhas.append(f"### {achado['codigo']} — {achado['nome']} ({achado['importancia']})")
        linhas.append("")
        linhas.append(achado["descricao"])
        linhas.append("")
        if achado["elementos"]:
            linhas.append("Elementos afetados:")
            linhas.append("")
            for elemento in achado["elementos"]:
                if not _e_iri(elemento):
                    linhas.append("- (no anonimo)")
                elif nome_curto(elemento) in ambiguos:
                    linhas.append(f"- `{elemento}`")
                else:
                    linhas.append(f"- `{nome_curto(elemento)}`")
            linhas.append("")
    return "\n".join(linhas) + "\n"


def main() -> int:
    caminho_ttl = Path(sys.argv[1]) if len(sys.argv) > 1 else TTL_PADRAO
    diretorio_saida = Path(sys.argv[2]) if len(sys.argv) > 2 else caminho_ttl.parent

    if not caminho_ttl.exists():
        print(f"ERRO: {caminho_ttl} nao existe. Rode antes: node scripts/ontouml/gerar-baseline.js")
        return 1

    diretorio_saida.mkdir(parents=True, exist_ok=True)

    grafo = carregar(caminho_ttl)
    caminho_owl = diretorio_saida / f"{caminho_ttl.stem}.owl"
    caminho_owl.write_text(grafo.serialize(format="xml"), encoding="utf-8")

    rdf_xml = sem_importacoes(grafo).serialize(format="xml")
    caminho_submetido = diretorio_saida / f"{caminho_ttl.stem}.oops.owl"
    caminho_submetido.write_text(rdf_xml, encoding="utf-8")

    momento = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    try:
        resposta = consultar_oops(rdf_xml)
    except requests.RequestException as erro:
        print(f"ERRO: chamada ao OOPS! falhou: {erro}")
        return 1

    (diretorio_saida / "relatorio-oops.xml").write_text(resposta, encoding="utf-8")
    achados = extrair_pitfalls(resposta)
    (diretorio_saida / "relatorio-oops.md").write_text(
        relatorio_em_markdown(achados, caminho_ttl, momento), encoding="utf-8"
    )

    print(f"RDF/XML completa  -> {caminho_owl}")
    print(f"RDF/XML submetida -> {caminho_submetido}")
    print(f"achados do OOPS!  -> {len(achados)}")
    for achado in achados:
        print(f"  [{achado['importancia']}] {achado['codigo']} {achado['nome']} ({achado['quantidade']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
