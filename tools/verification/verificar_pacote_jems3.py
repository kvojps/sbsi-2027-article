#!/usr/bin/env python3
"""Verifica o pacote de registro no JEMS3 contra a checklist do ticket 01.

Uso: python tools/verification/verificar_pacote_jems3.py [caminho-do-pacote]

O pacote e' um markdown com campos delimitados por marcadores HTML:

    <!-- campo: titulo -->
    ```text
    ...
    ```

Sai com codigo 1 se qualquer verificacao falhar.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

PACOTE_PADRAO = Path("artifacts/submission/jems3-pacote-registro.md")

TITULO_ESPERADO = (
    "OntoMPO: Ontological Analysis and Refinement of the "
    "Model for Project Observatories"
)

LABELS = [
    "Research Context",
    "Scientific and/or Practical Problem",
    "Proposed Solution and/or Analysis",
    "Related IS Theory",
    "Research Method",
    "Summary of Results",
    "Contributions and Impact to IS area",
]

TOPICOS_ESPERADOS = [
    "transparência e accountability em SI",
    "SI para gestão de dados, informação e conhecimento",
    "paradigmas, modelagem, design, engenharia e avaliação de SI",
    "SI organizacionais",
]

LIMITE_PALAVRAS = 300

# Termos que quebram o anonimato da revisao duplamente anonima.
TERMOS_IDENTIFICADORES = [
    "josé ferreira",
    "santos júnior",
    "santos junior",
    "ivaldir",
    "cleyton",
    "universidade de pernambuco",
    "poli.br",
    "@",
    "github.com",
    "our previous",
    "in our earlier",
]

CAMPO_RE = re.compile(
    r"<!--\s*campo:\s*(?P<nome>[a-z0-9\-]+)\s*-->\s*```[a-z]*\n(?P<corpo>.*?)```",
    re.DOTALL,
)

PALAVRA_RE = re.compile(r"[0-9A-Za-zÀ-ÿ]")

# O JEMS3 nao publica sua regra de contagem. O limite e' cobrado sobre a contagem
# mais severa plausivel — hifens e barras tambem separam palavras — de modo que
# passar aqui garante folga sob qualquer contador.
SEPARADOR_ESTRITO_RE = re.compile(r"[\s/\-—:;,.]+")


def extrair_campos(texto: str) -> dict[str, str]:
    return {m.group("nome"): m.group("corpo").strip() for m in CAMPO_RE.finditer(texto)}


def contar_palavras(texto: str) -> int:
    limpo = texto.replace("*", " ").replace("#", " ")
    return sum(1 for token in limpo.split() if PALAVRA_RE.search(token))


def contar_palavras_estrito(texto: str) -> int:
    limpo = texto.replace("*", " ").replace("#", " ")
    tokens = SEPARADOR_ESTRITO_RE.split(limpo)
    return sum(1 for token in tokens if PALAVRA_RE.search(token))


def fatiar_por_label(resumo: str) -> dict[str, str]:
    """Devolve o trecho de texto que segue cada label, ate o proximo label."""
    posicoes = []
    for label in LABELS:
        idx = resumo.find(label)
        if idx == -1:
            continue
        posicoes.append((idx, label))
    posicoes.sort()
    fatias: dict[str, str] = {}
    for i, (idx, label) in enumerate(posicoes):
        fim = posicoes[i + 1][0] if i + 1 < len(posicoes) else len(resumo)
        fatias[label] = resumo[idx + len(label) : fim]
    return fatias


def verificar(caminho: Path) -> list[str]:
    falhas: list[str] = []

    if not caminho.exists():
        return [f"pacote nao encontrado em {caminho}"]

    texto = caminho.read_text(encoding="utf-8")
    campos = extrair_campos(texto)

    for nome in ("titulo", "resumo", "palavras-chave", "topicos"):
        if nome not in campos:
            falhas.append(f"campo ausente: {nome}")
    if falhas:
        return falhas

    titulo = campos["titulo"]
    if titulo != TITULO_ESPERADO:
        falhas.append(f"titulo divergente: {titulo!r}")

    resumo = campos["resumo"]

    palavras = contar_palavras(resumo)
    estrito = contar_palavras_estrito(resumo)
    print(f"resumo: {palavras} palavras (contagem estrita: {estrito}; limite {LIMITE_PALAVRAS})")
    if estrito > LIMITE_PALAVRAS:
        falhas.append(
            f"resumo com {estrito} palavras na contagem estrita, acima do limite de {LIMITE_PALAVRAS}"
        )

    ausentes = [label for label in LABELS if label not in resumo]
    if ausentes:
        falhas.append(f"labels ausentes no resumo: {ausentes}")

    ordem = [resumo.find(label) for label in LABELS if label in resumo]
    if ordem != sorted(ordem):
        falhas.append("labels fora da ordem exigida pela chamada")

    fatias = fatiar_por_label(resumo)

    teoria = fatias.get("Related IS Theory", "")
    if "Representation Theory" not in teoria:
        falhas.append("Related IS Theory nao nomeia Representation Theory")
    if "Wand" not in teoria or "Weber" not in teoria:
        falhas.append("Related IS Theory nao credita Wand & Weber")

    solucao = fatias.get("Proposed Solution and/or Analysis", "").lower()
    if "ontological analysis" not in solucao:
        falhas.append("Proposed Solution nao declara a analise ontologica")
    if not re.search(r"(revised|refined) model", solucao):
        falhas.append("Proposed Solution nao declara o modelo revisado como artefato")
    if not re.search(r"not the formaliz|rather than the formaliz", solucao):
        falhas.append("Proposed Solution nao afasta a formalizacao do MPO como contribuicao")

    resultados = fatias.get("Summary of Results", "")
    if not re.search(
        r"\b(one|two|three|four|five|six|seven|eight|nine|ten|\d+)\s+representational\s+deficienc",
        resultados,
        re.IGNORECASE,
    ):
        falhas.append("Summary of Results nao quantifica as deficiencias representacionais")

    baixo = resumo.lower()
    achados = [termo for termo in TERMOS_IDENTIFICADORES if termo in baixo]
    if achados:
        falhas.append(f"resumo contem identificacao de autoria/instituicao: {achados}")

    palavras_chave = [p.strip() for p in campos["palavras-chave"].split(";") if p.strip()]
    if len(palavras_chave) < 3:
        falhas.append("menos de tres palavras-chave definidas")
    if re.search(r"[À-ÿ]", campos["palavras-chave"]):
        falhas.append("palavras-chave nao estao em ingles")

    topicos = campos["topicos"].lower()
    faltando = [t for t in TOPICOS_ESPERADOS if t.lower() not in topicos]
    if faltando:
        falhas.append(f"topicos ausentes: {faltando}")

    return falhas


def main() -> int:
    caminho = Path(sys.argv[1]) if len(sys.argv) > 1 else PACOTE_PADRAO
    falhas = verificar(caminho)
    if falhas:
        print(f"FALHOU ({len(falhas)}):")
        for f in falhas:
            print(f"  - {f}")
        return 1
    print("OK: pacote de registro conforme a checklist do ticket 01")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
