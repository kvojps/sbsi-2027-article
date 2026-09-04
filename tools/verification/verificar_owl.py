#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifica a transformacao gUFO e a customizacao contra a checklist do ticket 06.

Uso: python tools/verification/verificar_owl.py [diretorio-ontologia]

Confere sete coisas, na ordem da checklist do ticket:

  1. a OWL do modelo revisado saiu da transformacao gUFO oficial, e o artefato
     customizado a contem inteira;
  2. cada customizacao tem justificativa escrita, e nenhuma esta orfa — toda
     customizacao aparece no diff e em `customizacoes.md`;
  3. o diff esta em arquivo nas duas formas, legivel e crua, e a crua fecha a
     conta: gerado mais acrescimo e exatamente o customizado;
  4. a OWL customizada passa em verificacao de consistencia por raciocinador —
     rodado **aqui**, nao lido do relatorio —, e o relatorio salvo concorda;
  5. o OOPS! foi executado sobre a versao revisada e o relatorio e uma resposta
     de verdade;
  6. a comparacao com o relatorio do baseline esta registrada, e nenhum pitfall
     de nenhum dos dois relatorios ficou sem leitura;
  7. as metricas do artefato revisado estao registradas, e batem com o que se
     mede do arquivo.

Mais o que o layout do repositorio exige: os tres achados que as rodadas
anteriores enderecaram a este ticket (B3, B4, B5) tem de estar tratados por
escrito, o modelo gerado nao pode ter sido mexido, e o artefato nao pode
identificar autoria enquanto a revisao for duplamente anonima.

Como os demais verificadores, **le os artefatos como terceiro**: nao importa
nada de `tools/generation/`, e recalcula do arquivo o que vai conferir. A
tabela de anotacoes e a conta de axiomas sao transcritas do enunciado, nao
importadas — se a geracao mudar de regra sem que o ticket mude, a duplicacao
acusa.

Sai com codigo 1 se qualquer verificacao falhar.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

import rdflib
from rdflib import RDF, RDFS, OWL, Literal, Namespace, URIRef

try:
    import owlrl
except ImportError as erro:  # pragma: no cover - dependencia ausente
    print(f"ERRO: dependencia ausente ({erro.name}). Rode: pip install rdflib owlrl")
    sys.exit(1)

ONTOLOGIA_PADRAO = Path("artifacts/ontology")
GUFO_LOCAL = Path("sources/gufo/gufo.ttl")
GUFO_README = Path("sources/gufo/README.md")

GUFO = Namespace("http://purl.org/nemo/gufo#")
SKOS = Namespace("http://www.w3.org/2004/02/skos/core#")
DCT = Namespace("http://purl.org/dc/terms/")
VANN = Namespace("http://purl.org/vocab/vann/")

ONTOLOGIA_IRI = URIRef("https://example.org/ontompo/rodada-2")
NS_DOMINIO = "https://example.org/ontompo/rodada-2#"

# Transcritos do enunciado do ticket, nao importados de `customizar_owl.py`.
CUSTOMIZACOES = ["C1", "C2", "C3", "C4", "C5"]
ACHADOS_ENDERECADOS = ["B3", "B4", "B5"]
METRICAS_EXIGIDAS = [
    "classes nomeadas",
    "propriedades de objeto",
    "propriedades de dados",
    "axiomas",
]
PREDICADOS_DE_ANOTACAO = {
    RDFS.label,
    RDFS.comment,
    RDFS.isDefinedBy,
    SKOS.prefLabel,
    OWL.versionInfo,
    DCT.title,
    DCT.description,
    DCT.license,
    DCT.rights,
    VANN.preferredNamespacePrefix,
    VANN.preferredNamespaceUri,
}

ERRO_OWLRL = URIRef("http://www.daml.org/2002/03/agents/agent-ont#error")


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


def _grafo(caminho: Path) -> rdflib.Graph:
    grafo = rdflib.Graph()
    grafo.parse(caminho.as_posix(), format="turtle")
    return grafo


def _triplas_comparaveis(grafo: rdflib.Graph) -> set[tuple[str, str, str]]:
    """As triplas com cada no anonimo trocado pela assinatura do seu conteudo.

    A conteinencia precisa sobreviver a reserializacao, que renomeia no
    anonimo, e nao pode depender do nome. Trocar todo no anonimo por um curinga
    unico seria facil e fraco: as 40 restricoes de cardinalidade do artefato
    virariam a mesma coisa, e perder uma delas passaria despercebido. A
    assinatura e o hash do conteudo do no, resolvido para dentro, que distingue
    uma restricao da outra.

    Vale porque a customizacao nunca acrescenta tripla *a* um no anonimo que ja
    existia — so cria os seus. O conteudo dos nos do gerado e o mesmo nos dois
    grafos, e por isso as assinaturas batem.
    """

    def marca(termo, visitados: frozenset) -> str:
        if not isinstance(termo, rdflib.term.BNode):
            return str(termo)
        if termo in visitados:
            return "[ciclo]"
        adiante = visitados | {termo}
        partes = sorted(
            f"{p} {marca(o, adiante)}" for p, o in grafo.predicate_objects(termo)
        )
        return f"[{hashlib.sha1(chr(10).join(partes).encode('utf-8')).hexdigest()[:20]}]"

    return {
        (marca(s, frozenset()), str(p), marca(o, frozenset())) for s, p, o in grafo
    }


def verificar_transformacao_e_conteinencia(
    diretorio: Path, resultado: Resultado
) -> tuple[rdflib.Graph, rdflib.Graph] | None:
    gerada = diretorio / "rodada-2" / "ontompo-rodada-2.ttl"
    customizada = diretorio / "owl" / "ontompo.ttl"
    acrescimo = diretorio / "owl" / "diff-gerado-customizado.ttl"

    for caminho in (gerada, customizada, acrescimo):
        if not resultado.exigir(caminho.exists(), f"{caminho} nao existe"):
            return None

    grafo_gerado = _grafo(gerada)
    grafo_customizado = _grafo(customizada)
    grafo_acrescimo = _grafo(acrescimo)

    resultado.exigir(
        (ONTOLOGIA_IRI, OWL.imports, URIRef(str(GUFO))) in grafo_customizado,
        "a OWL customizada nao importa a gUFO: nao e mais a saida da transformacao oficial",
    )
    resultado.exigir(
        len(list(grafo_gerado.subjects(RDF.type, GUFO.Kind))) > 0,
        "a OWL gerada nao usa os estereotipos da gUFO: nao veio da transformacao oficial",
    )

    do_gerado = _triplas_comparaveis(grafo_gerado)
    do_customizado = _triplas_comparaveis(grafo_customizado)
    perdidas = do_gerado - do_customizado
    resultado.exigir(
        not perdidas,
        f"a customizacao nao e aditiva: {len(perdidas)} tripla(s) da transformacao sumiram — "
        "a preservacao semantica deixa de ser verificavel",
    )

    soma = do_gerado | _triplas_comparaveis(grafo_acrescimo)
    resultado.exigir(
        soma == do_customizado,
        f"gerado + acrescimo nao da o customizado: {len(soma ^ do_customizado)} tripla(s) de "
        "diferenca — o diff nao descreve o que foi feito",
    )
    resultado.exigir(
        len(grafo_customizado) > len(grafo_gerado),
        "a customizacao nao acrescentou nada",
    )
    return grafo_gerado, grafo_customizado


def verificar_justificativas(diretorio: Path, resultado: Resultado) -> None:
    customizacoes = diretorio / "owl" / "customizacoes.md"
    diff = diretorio / "owl" / "diff-gerado-customizado.md"
    if not resultado.exigir(customizacoes.exists(), f"{customizacoes} nao existe"):
        return
    if not resultado.exigir(diff.exists(), f"{diff} nao existe"):
        return

    texto = _ler(customizacoes)
    texto_diff = _ler(diff)
    for identificador in CUSTOMIZACOES:
        secao = re.search(rf"^## {identificador} — (.+)$", texto, re.MULTILINE)
        if not resultado.exigir(
            secao is not None, f"{identificador} nao tem seccao propria em customizacoes.md"
        ):
            continue
        corpo = texto[secao.end() :].split("\n## ")[0]
        resultado.exigir(
            "**O que faz.**" in corpo,
            f"{identificador} nao diz o que faz",
        )
        resultado.exigir(
            "**Por que.**" in corpo and len(corpo.split("**Por que.**")[1].strip()) > 200,
            f"{identificador} nao tem justificativa escrita — customizacao sem razao nao conta",
        )
        resultado.exigir(
            f"## {identificador} — " in texto_diff,
            f"{identificador} nao aparece no diff: customizacao orfa e defeito",
        )

    resultado.exigir(
        "não foi customizado" in texto,
        "customizacoes.md nao registra o que deliberadamente nao foi customizado",
    )
    for achado in ACHADOS_ENDERECADOS:
        resultado.exigir(
            f"**{achado}**" in texto,
            f"{achado} foi enderecado a este ticket pelas rodadas anteriores e nao aparece em "
            "customizacoes.md",
        )

    resultado.exigir(
        "Removidas: **0**" in texto_diff and "Alteradas: **0**" in texto_diff,
        "o diff nao afirma que nada foi removido nem alterado",
    )


def verificar_raciocinador(diretorio: Path, grafo: rdflib.Graph, resultado: Resultado) -> None:
    if not resultado.exigir(GUFO_LOCAL.exists(), f"{GUFO_LOCAL} nao existe"):
        return

    fechado = rdflib.Graph()
    for tripla in grafo:
        fechado.add(tripla)
    gufo = _grafo(GUFO_LOCAL)
    for tripla in gufo:
        fechado.add(tripla)
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics).expand(fechado)
    inconsistencias = sorted({str(o) for o in fechado.objects(None, ERRO_OWLRL)})
    resultado.exigir(
        not inconsistencias,
        f"a OWL customizada e inconsistente: {inconsistencias[:3]}",
    )

    relatorio = diretorio / "owl" / "relatorio-raciocinador.json"
    if not resultado.exigir(relatorio.exists(), f"{relatorio} nao existe"):
        return
    dados = json.loads(_ler(relatorio))
    resultado.exigir(
        dados["artefatos"]["customizada"]["inconsistencias"] == [],
        "o relatorio do raciocinador registra inconsistencia na OWL customizada",
    )
    resultado.exigir(
        not dados["falhas"],
        f"o relatorio do raciocinador registra {len(dados.get('falhas', []))} falha(s)",
    )
    controles = dados["controles"]
    resultado.exigir(
        len(controles) >= 5,
        "menos de cinco controles positivos: o zero da consistencia fica pouco sustentado",
    )
    resultado.exigir(
        all(c["customizada"] for c in controles),
        "algum controle positivo nao foi acusado na OWL customizada — sem ele, um relatorio "
        "vazio pode significar raciocinador que nunca acusa",
    )
    resultado.exigir(
        any(c["customizada"] and not c["gerada"] for c in controles),
        "nenhum controle separa o customizado do gerado: a customizacao nao teria acrescentado "
        "conteudo logico nenhum",
    )
    resultado.exigir(
        "não cobre" in _ler(diretorio / "owl" / "relatorio-raciocinador.md"),
        "o relatorio do raciocinador nao declara o que a verificacao nao cobre",
    )


def _pitfalls(xml: str) -> set[str]:
    return set(re.findall(r"hasCode[^>]*>(P\d+)<", xml))


def verificar_oops(diretorio: Path, resultado: Resultado) -> None:
    depois_xml = diretorio / "owl" / "relatorio-oops.xml"
    depois_md = diretorio / "owl" / "relatorio-oops.md"
    antes_xml = diretorio / "baseline" / "relatorio-oops.xml"
    comparacao = diretorio / "owl" / "comparacao-oops.md"

    for caminho in (depois_xml, depois_md, antes_xml, comparacao):
        if not resultado.exigir(caminho.exists(), f"{caminho} nao existe"):
            return

    texto_depois = _ler(depois_xml)
    resultado.exigir(
        "unexpected_error" not in texto_depois,
        f"{depois_xml} guarda um erro do servico, nao um relatorio",
    )
    codigos_depois = _pitfalls(texto_depois)
    codigos_antes = _pitfalls(_ler(antes_xml))
    resultado.exigir(bool(codigos_depois), f"{depois_xml} nao traz nenhum pitfall identificado")

    texto_comparacao = _ler(comparacao)
    for codigo in sorted(codigos_antes | codigos_depois):
        resultado.exigir(
            f"**`{codigo}`**" in texto_comparacao,
            f"o pitfall {codigo} nao tem leitura em comparacao-oops.md — achado orfao e defeito",
        )
    for codigo in sorted(codigos_antes - codigos_depois):
        resultado.exigir(
            codigo in texto_comparacao,
            f"o pitfall {codigo}, que o baseline tinha e o revisado nao tem, sumiu tambem da "
            "comparacao: a melhoria precisa estar registrada",
        )
    resultado.exigir(
        "P08" in codigos_antes and "P10" in codigos_antes,
        "o relatorio do baseline mudou: a comparacao deixaria de ser com a mesma metade 'antes'",
    )


def verificar_metricas(diretorio: Path, grafo: rdflib.Graph, resultado: Resultado) -> None:
    metricas = diretorio / "owl" / "metricas.md"
    if not resultado.exigir(metricas.exists(), f"{metricas} nao existe"):
        return
    texto = _ler(metricas)

    def do_arquivo(tipo: URIRef) -> int:
        return len(
            {
                s
                for s in grafo.subjects(RDF.type, tipo)
                if isinstance(s, URIRef) and str(s).startswith(NS_DOMINIO)
            }
        )

    medido = {
        "classes nomeadas": do_arquivo(OWL.Class),
        "propriedades de objeto": do_arquivo(OWL.ObjectProperty),
        "propriedades de dados": do_arquivo(OWL.DatatypeProperty),
        "axiomas": sum(1 for _s, p, _o in grafo if p not in PREDICADOS_DE_ANOTACAO),
    }

    for rotulo in METRICAS_EXIGIDAS:
        linha = re.search(rf"^\| {re.escape(rotulo)}[^|]*\|(.+)\|\s*$", texto, re.MULTILINE)
        if not resultado.exigir(linha is not None, f"metricas.md nao registra «{rotulo}»"):
            continue
        celulas = [c.strip() for c in linha.group(1).split("|") if c.strip()]
        if not resultado.exigir(
            len(celulas) >= 3,
            f"a linha «{rotulo}» de metricas.md nao tem as tres colunas de comparacao",
        ):
            continue
        registrado = celulas[-1]
        resultado.exigir(
            registrado == str(medido[rotulo]),
            f"metricas.md registra {registrado} para «{rotulo}» e o arquivo tem "
            f"{medido[rotulo]}",
        )

    resultado.exigir(
        medido["propriedades de dados"] == 0 and "B6" in texto,
        "o artefato nao tem propriedade de dados e metricas.md nao explica por que — "
        "zero sem leitura nao e metrica",
    )


def verificar_anonimato_e_insumo(diretorio: Path, grafo: rdflib.Graph, resultado: Resultado) -> None:
    resultado.exigir(
        not list(grafo.objects(ONTOLOGIA_IRI, DCT.creator)),
        "a OWL declara autoria: a revisao e duplamente anonima",
    )
    resultado.exigir(
        bool(list(grafo.objects(ONTOLOGIA_IRI, DCT.license))),
        "a OWL nao declara licenca, e o deposito aberto exige uma",
    )
    resultado.exigir(
        any(
            isinstance(o, Literal) and o.language == "pt-BR"
            for o in grafo.objects(None, RDFS.comment)
        ),
        "nenhuma definicao em portugues sobreviveu ao artefato: B3 continuaria aberto",
    )

    if not resultado.exigir(GUFO_README.exists(), f"{GUFO_README} nao existe"):
        return
    esperado = re.search(r"`([0-9a-f]{64})`", _ler(GUFO_README))
    if not resultado.exigir(
        esperado is not None, "sources/gufo/README.md nao registra o SHA-256 da copia"
    ):
        return
    obtido = hashlib.sha256(GUFO_LOCAL.read_bytes()).hexdigest()
    resultado.exigir(
        obtido == esperado.group(1),
        f"a copia local da gUFO nao confere com o SHA-256 registrado: {obtido}",
    )


def main() -> int:
    diretorio = Path(sys.argv[1]) if len(sys.argv) > 1 else ONTOLOGIA_PADRAO
    resultado = Resultado()

    grafos = verificar_transformacao_e_conteinencia(diretorio, resultado)
    verificar_justificativas(diretorio, resultado)
    verificar_oops(diretorio, resultado)
    if grafos is not None:
        _gerado, customizado = grafos
        verificar_raciocinador(diretorio, customizado, resultado)
        verificar_metricas(diretorio, customizado, resultado)
        verificar_anonimato_e_insumo(diretorio, customizado, resultado)

    print(f"verificacoes: {resultado.checagens}")
    if resultado.falhas:
        print(f"FALHOU: {len(resultado.falhas)} problema(s)")
        for falha in resultado.falhas:
            print(f"  - {falha}")
        return 1
    print("OK: a checklist do ticket 06 esta cumprida")
    return 0


if __name__ == "__main__":
    sys.exit(main())
