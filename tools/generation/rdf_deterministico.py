#!/usr/bin/env python3
"""Leitura e serializacao de RDF com nos anonimos deterministicos.

A rdflib sorteia o rotulo dos nos anonimos a cada execucao, e a Turtle da
transformacao gUFO tem uma restricao anonima por mediacao, por participacao e
por particao. Sem normalizacao, dois `gerar-baseline` seguidos produziriam
RDF/XML diferentes sem que nada no modelo tivesse mudado — e tanto o diff entre
as rodadas quanto o diff entre a OWL gerada e a customizada (ticket 06) ficariam
ilegiveis.

O `to_canonical_graph` da propria rdflib nao serve: ele desempata nos isomorfos
por sorteio e nao e estavel entre execucoes.

Rotular os nos anonimos, porem, nao basta: o `Memory` da rdflib nao percorre as
triplas na ordem em que foram inseridas, e o serializador RDF/XML escreve na
ordem em que percorre. Duas execucoes produziam o mesmo grafo em ordens
diferentes. Por isso o grafo devolvido aqui e um `GrafoOrdenado`, que percorre
ordenado.

Usado por `customizar_owl.py` e por `../verification/rodar_oops.py`.
"""

from __future__ import annotations

import hashlib
from pathlib import Path

import rdflib


def _termo(termo) -> tuple[str, str, str]:
    """Chave de ordenacao de um termo.

    O texto sozinho nao basta: `"Hardware"@pt-BR` e `"Hardware"@en` tem o mesmo
    `str()`, empatam, e o desempate cai na ordem em que a rdflib devolveu as
    triplas — que nao e estavel entre execucoes. A lingua e o tipo entram na
    chave para que o empate nao exista.
    """
    if isinstance(termo, rdflib.term.Literal):
        return (str(termo), termo.language or "", str(termo.datatype or ""))
    return (str(termo), "", "")


def _chave(tripla):
    return tuple(_termo(termo) for termo in tripla)


class GrafoOrdenado(rdflib.Graph):
    """Grafo que percorre as triplas em ordem, para que a serializacao seja estavel.

    O serializador RDF/XML da rdflib escreve os sujeitos na ordem em que
    `store.subjects()` os devolve, e todos os acessos do `Graph` — `subjects`,
    `predicate_objects` — passam por `triples`. Ordenar aqui ordena todos.
    """

    def triples(self, triple):  # noqa: D102 - contrato herdado da rdflib
        yield from sorted(super().triples(triple), key=_chave)


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


def _rotulos_por_conteudo(grafo: rdflib.Graph, anonimos: set) -> dict:
    """Rotula cada no anonimo pelo hash do seu conteudo, de dentro para fora."""
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
    return rotulos


def _marca(termo, rotulos: dict) -> str:
    return rotulos.get(termo, "?") if isinstance(termo, rdflib.term.BNode) else str(termo)


def _rotulos_por_conteudo_e_contexto(grafo: rdflib.Graph, anonimos: set) -> dict:
    """Rotula considerando tambem quem aponta para o no, por refinamento iterativo.

    Necessario quando dois nos anonimos tem conteudo identico e mesmo assim sao
    distintos. Acontece nas particoes: a transformacao gUFO emite a mesma lista
    de especificos duas vezes, uma como `owl:members` do `owl:AllDisjointClasses`
    e outra como `owl:unionOf` da `owl:equivalentClass`. As duas listas tem
    celulas de conteudo igual e pais diferentes, e e o pai que as separa.

    Cada rodada refina a particao anterior; para quando ela para de refinar, o
    que basta para uma cadeia de listas de qualquer comprimento.
    """
    rotulos = {no: "n0" for no in anonimos}
    for _ in range(len(anonimos) + 1):
        novos = {}
        for no in anonimos:
            saindo = sorted(
                f"{predicado} > {_marca(objeto, rotulos)}"
                for predicado, objeto in grafo.predicate_objects(no)
            )
            entrando = sorted(
                f"{_marca(sujeito, rotulos)} > {predicado}"
                for sujeito, predicado in grafo.subject_predicates(no)
            )
            assinatura = chr(10).join([rotulos[no], *saindo, "--", *entrando])
            novos[no] = f"n{hashlib.sha1(assinatura.encode('utf-8')).hexdigest()[:20]}"
        if len(set(novos.values())) == len(set(rotulos.values())):
            return novos
        rotulos = novos
    return rotulos


def normalizado(grafo: rdflib.Graph) -> rdflib.Graph:
    """Copia do grafo com nos anonimos rotulados de forma deterministica.

    O rotulo e o hash do conteudo do no, resolvido de dentro para fora — as
    restricoes do gUFO aninham um nivel, em `owl:onProperty [ owl:inverseOf ... ]`.
    Quando o conteudo nao basta para distinguir dois nos, a rotulacao passa a
    considerar tambem quem aponta para eles. Fundir os dois seria mais simples e
    esta errado: sao duas celulas de lista distintas, e uma delas some.

    Se nem isso separar, falha — melhor uma execucao que para do que um artefato
    com um no a menos.
    """
    anonimos = {t for tripla in grafo for t in tripla if isinstance(t, rdflib.term.BNode)}
    rotulos = _rotulos_por_conteudo(grafo, anonimos)
    if len(set(rotulos.values())) != len(rotulos):
        rotulos = _rotulos_por_conteudo_e_contexto(grafo, anonimos)
    if len(set(rotulos.values())) != len(rotulos):
        raise RuntimeError("colisao de rotulo entre nos anonimos")

    def substituir(termo):
        return rdflib.term.BNode(rotulos[termo]) if isinstance(termo, rdflib.term.BNode) else termo

    resultado = GrafoOrdenado()
    for prefixo, iri in grafo.namespaces():
        resultado.bind(prefixo, iri)
    for tripla in grafo:
        resultado.add(tuple(substituir(termo) for termo in tripla))
    return resultado


def carregar(caminho_ttl: Path) -> rdflib.Graph:
    """Le uma Turtle e devolve o grafo ja normalizado."""
    grafo = rdflib.Graph()
    grafo.parse(caminho_ttl.as_posix(), format="turtle")
    return normalizado(grafo)


def sem_importacoes(grafo: rdflib.Graph) -> rdflib.Graph:
    """Copia do grafo sem `owl:imports`, que faz o servico do OOPS! falhar."""
    recorte = GrafoOrdenado()
    for prefixo, iri in grafo.namespaces():
        recorte.bind(prefixo, iri)
    for tripla in grafo:
        if tripla[1] != rdflib.OWL.imports:
            recorte.add(tripla)
    return recorte
