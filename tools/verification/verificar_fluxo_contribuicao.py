#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Confere o fluxo de contribuição e o orçamento do ticket 17.

Uso: python3 tools/verification/verificar_fluxo_contribuicao.py [diretorio-do-artigo]

A reestruturação conserva as nove seções para manter estáveis os artefatos e a
numeração, mas torna §§2--3 um bloco argumentativo único. Este verificador não
mede o PDF (essa é a responsabilidade de verificar_port_latex.py): confere o
contrato editorial que deve ser preservado antes de mover ou condensar texto.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


ARTIGO_PADRAO = Path("artifacts/paper")

ORCAMENTOS = {
    "1": 1.20,
    "2": 1.70,
    "3": 0.80,
    "4": 1.45,
    "5": 3.65,
    "6": 2.25,
    "7": 1.95,
    "8": 1.25,
    "9": 0.80,
}

SECOES_TEX = (
    "Introdução",
    "Referencial Teórico",
    "Trabalhos Relacionados",
    "Método de Pesquisa",
    "Análise Ontológica do MPO",
    "A OntoMPO Revisada",
    "Avaliação",
    "Discussão e Limitações",
    "Conclusão e Trabalhos Futuros",
)


def ler(caminho: Path) -> str:
    try:
        return caminho.read_text(encoding="utf-8")
    except OSError:
        return ""


def exigir(condicao: bool, mensagem: str, falhas: list[str]) -> None:
    if not condicao:
        falhas.append(mensagem)


def orcamentos_do_esqueleto(texto: str) -> dict[str, float]:
    achados: dict[str, float] = {}
    for linha in texto.splitlines():
        m = re.match(r"^\|\s*(\d+)\s*\|.*\|\s*([\d,]+)\s*\|\s*$", linha)
        if m:
            achados[m.group(1)] = float(m.group(2).replace(",", "."))
    return achados


def main() -> int:
    diretorio = Path(sys.argv[1]) if len(sys.argv) > 1 else ARTIGO_PADRAO
    esqueleto = ler(diretorio / "esqueleto.md")
    tex = ler(diretorio / "artigo.tex")
    secoes = diretorio / "secoes"
    falhas: list[str] = []

    encontrados = orcamentos_do_esqueleto(esqueleto)
    exigir(encontrados == ORCAMENTOS, "orçamento das nove seções diverge da redistribuição do ticket 17", falhas)
    exigir(abs(sum(encontrados.values()) - 15.05) < 0.001, "o corpo não soma 15,05 páginas", falhas)
    exigir(
        "problema → lacuna → desenho → achados → artefato → avaliação → implicações" in esqueleto,
        "o esqueleto não declara o fluxo de contribuição", falhas,
    )
    exigir("§§2--3 funcionam como um só bloco argumentativo" in esqueleto,
           "o esqueleto não integra fundamentos e trabalhos relacionados", falhas)

    nomes_tex = tuple(re.findall(r"^\\section\{([^}]+)\}", tex, re.MULTILINE))
    exigir(nomes_tex == SECOES_TEX, "a ordem ou os nomes das nove seções divergem do esqueleto", falhas)
    exigir("Bloco integrado de fundamentos e trabalhos relacionados" in tex,
           "o scaffold LaTeX não documenta o bloco integrado §§2--3", falhas)

    introducao = ler(secoes / "01-introducao.md")
    relacionados = ler(secoes / "03-trabalhos-relacionados.md")
    metodo = ler(secoes / "04-metodo.md")
    for termo in ("RQ1", "RQ2", "As três contribuições", "A §2 apresenta as bases"):
        exigir(termo in introducao, f"a introdução não entrega «{termo}» antes dos fundamentos", falhas)
    quadro = relacionados.find("Quadro comparativo")
    lacuna = relacionados.find("A lacuna é positiva e delimitada")
    exigir(quadro >= 0 and lacuna > quadro,
           "a lacuna delimitada precisa encerrar §3, depois do quadro comparativo", falhas)
    exigir("próxima seção explicita o desenho" in relacionados,
           "§3 não faz a transição da lacuna para o desenho", falhas)
    for termo in ("O procedimento da análise teve quatro passos", "contou como deficiência", "A avaliação foi desenhada"):
        exigir(termo in metodo, f"o método não explicita «{termo}»", falhas)

    if falhas:
        print("FALHOU:")
        for falha in falhas:
            print(f"- {falha}")
        return 1
    print("OK: fluxo problema → lacuna → desenho → achados → artefato → avaliação → implicações")
    print("OK: orçamento do corpo 15,05 páginas; §§2--3 integradas sem renumeração")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
