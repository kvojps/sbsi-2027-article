#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Controle positivo do verificador do ticket 13.

Uso: python tools/verification/controle-port-latex.py

Um relatorio vazio so' e' interpretavel se alguem provar que o instrumento
dispara — e' a regra que o proprio artigo defende, e vale para o verificador do
ticket 13 como vale para o plugin OntoUML. Este script aplica, uma por vez,
mutacoes deliberadas a uma **copia** de `artifacts/paper/`, roda
`verificar_port_latex.py` sobre a copia e exige que cada uma seja acusada, com a
mensagem esperada.

Nada aqui toca o diretorio de trabalho: cada mutacao vive numa copia temporaria
que some ao fim. Exige `pdflatex`, e cada mutacao custa uma compilacao, entao a
execucao inteira leva alguns minutos.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
ARTIGO = RAIZ / "artifacts" / "paper"
VERIFICADOR = RAIZ / "tools" / "verification" / "verificar_port_latex.py"
IMAGEM_DA_FONTE = RAIZ / "sources" / "dissertation" / "imagens" / "onto_mpo.png"


def _troca(caminho: Path, antigo: str, novo: str) -> None:
    texto = caminho.read_text(encoding="utf-8")
    if antigo not in texto:
        raise SystemExit(f"mutacao impossivel: {antigo[:60]!r} nao esta em {caminho.name}")
    caminho.write_text(texto.replace(antigo, novo, 1), encoding="utf-8")


# Cada mutacao: nome, funcao que a aplica na copia, e o trecho que a acusacao
# precisa conter.
def mutacoes() -> list[tuple[str, callable, str]]:
    def nocite(d: Path) -> None:
        _troca(d / "artigo.tex", r"\bibliographystyle{sbc}", "\\nocite{*}\n\\bibliographystyle{sbc}")

    def latin1(d: Path) -> None:
        # A regressao historica: o template traz as duas, nesta ordem, e a
        # segunda vence. Nao se troca o fontenc — acrescenta-se o latin1.
        _troca(
            d / "artigo.tex",
            r"\usepackage[utf8]{inputenc}",
            "\\usepackage[utf8]{inputenc}\n\\usepackage[latin1]{inputenc}",
        )

    def sem_fontenc(d: Path) -> None:
        _troca(d / "artigo.tex", "\\usepackage[T1]{fontenc}\n", "")

    def texto_editado_a_mao(d: Path) -> None:
        alvo = d / "secoes-tex" / "01-introducao.tex"
        _troca(alvo, "Organizações realizam sua estratégia", "As organizações realizam a estratégia")

    def classe_inventada(d: Path) -> None:
        _troca(d / "figuras" / "ontompo-integrado.tex", "(nDataSource)", "(nDataSourceX)")

    def classe_ausente(d: Path) -> None:
        alvo = d / "figuras" / "ontompo-integrado.tex"
        texto = alvo.read_text(encoding="utf-8")
        linhas = [l for l in texto.split("\n") if "(nKnowledge)" not in l]
        alvo.write_text("\n".join(linhas), encoding="utf-8")

    def ligacao_inventada(d: Path) -> None:
        _troca(
            d / "figuras" / "ontompo-integrado.tex",
            r"\draw[gen] (nPerson) -- (nPhysicalAgent);",
            r"\draw[gen] (nPerson) -- (nNetwork);",
        )

    def figura_ilegivel(d: Path) -> None:
        alvo = d / "figuras" / "ontompo-integrado.tex"
        alvo.write_text(
            alvo.read_text(encoding="utf-8").replace("\\fontsize{5}", "\\fontsize{4}"),
            encoding="utf-8",
        )

    def figura_larga(d: Path) -> None:
        alvo = d / "figuras" / "ontompo-integrado.tex"
        texto = alvo.read_text(encoding="utf-8")
        # empurra a coluna mais a direita para fora da mancha
        texto = re.sub(r"at \(12\.25,", "at (16.00,", texto)
        alvo.write_text(texto, encoding="utf-8")

    def imagem_do_modelo_antigo(d: Path) -> None:
        _troca(
            d / "artigo.tex",
            r"\input{secoes-tex/06-ontompo-revisada}",
            "\\includegraphics[width=\\textwidth]{onto_mpo}\n\\input{secoes-tex/06-ontompo-revisada}",
        )

    def imagem_copiada(d: Path) -> None:
        shutil.copy(IMAGEM_DA_FONTE, d / "figuras" / "onto_mpo.png")

    def abstract_divergente(d: Path) -> None:
        _troca(d / "artigo.tex", "observe a set of projects and", "observe several projects and")

    def label_removido(d: Path) -> None:
        _troca(d / "artigo.tex", r"\textbf{Related IS Theory.}", r"\textbf{Theory.}")

    def secao_fora_de_ordem(d: Path) -> None:
        alvo = d / "artigo.tex"
        texto = alvo.read_text(encoding="utf-8")
        texto = texto.replace(r"\section{Avaliação}", r"\section{Zzz Avaliação}")
        alvo.write_text(texto, encoding="utf-8")

    def remissao_removida(d: Path) -> None:
        alvo = d / "apendice-sparql.tex"
        texto = alvo.read_text(encoding="utf-8")
        texto = re.sub(r"reexecutar-consultas\.py", "algum script", texto)
        alvo.write_text(texto, encoding="utf-8")

    def contagem_de_linhas_trocada(d: Path) -> None:
        alvo = d / "apendice-sparql.tex"
        texto = alvo.read_text(encoding="utf-8")
        alvo.write_text(texto.replace("QC7 (31)", "QC7 (99)"), encoding="utf-8")

    def consulta_transcrita(d: Path) -> None:
        _troca(d / "apendice-sparql.tex", "SELECT ?conceito", "SELECT ?conceitoX")

    def citacao_quebrada(d: Path) -> None:
        _troca(d / "secoes-tex" / "04-metodo.tex", r"\cite{hevner2004design,", r"\cite{hevnerXXXX,")

    def artigo_longo_demais(d: Path) -> None:
        recheio = "\n\n".join(
            "Parágrafo de enchimento para estourar o limite de páginas da chamada, "
            "repetido para ocupar espaço suficiente e provar que a contagem dispara. " * 6
            for _ in range(28)
        )
        _troca(d / "artigo.tex", r"\bibliographystyle{sbc}", recheio + "\n\\bibliographystyle{sbc}")

    def declaracao_de_ia_removida(d: Path) -> None:
        alvo = d / "artigo.tex"
        texto = alvo.read_text(encoding="utf-8")
        texto = texto.replace("\\section*{Declaração de Uso de IA Generativa}\n", "")
        texto = texto.replace("\\input{secoes-tex/declaracao-ia}\n", "")
        alvo.write_text(texto, encoding="utf-8")

    def veiculo_da_chamada_removido(d: Path) -> None:
        # tira a unica citacao aos Anais Estendidos: a entrada continua no .bib,
        # mas some da bibliografia impressa.
        for tex in (d / "secoes-tex").glob("*.tex"):
            texto = tex.read_text(encoding="utf-8")
            if "sbsi_estendido" in texto:
                tex.write_text(re.sub(r"\\cite\{sbsi_estendido\}", "", texto), encoding="utf-8")

    return [
        ("nocite provisorio de volta", nocite, "nocite"),
        ("latin1 do template de volta", latin1, "latin1"),
        ("sem fontenc: acento vira glifo sobreposto", sem_fontenc, "acento"),
        ("texto do .tex editado a mao", texto_editado_a_mao, "nao estao no PDF"),
        ("figura com classe inventada", classe_inventada, "nao existe no modelo revisado"),
        ("figura sem uma classe do modelo", classe_ausente, "nao mostra"),
        ("figura com ligacao que o modelo nao tem", ligacao_inventada, "ligacao que o modelo"),
        ("figura abaixo do piso de legibilidade", figura_ilegivel, "abaixo do piso"),
        ("figura mais larga que a mancha", figura_larga, "sangra"),
        ("imagem do modelo antigo incluida", imagem_do_modelo_antigo, "imagem pronta"),
        ("imagem da dissertacao copiada", imagem_copiada, "nao e' TikZ gerado"),
        ("abstract divergente do JEMS3", abstract_divergente, "diverge do texto congelado"),
        ("label do resumo estruturado removido", label_removido, "label"),
        ("secao renomeada", secao_fora_de_ordem, "divergem do esqueleto"),
        ("remissao ao deposito sem o script", remissao_removida, "reexecuta"),
        ("contagem de linhas de uma QC trocada", contagem_de_linhas_trocada, "linhas de QC7"),
        ("consulta transcrita em vez de reproduzida", consulta_transcrita, "transcreve"),
        ("citacao sem entrada no .bib", citacao_quebrada, "sem entrada"),
        ("artigo acima de 20 paginas", artigo_longo_demais, "paginas"),
        ("declaracao de IA removida", declaracao_de_ia_removida, "IA generativa"),
        ("veiculo da chamada sem citacao", veiculo_da_chamada_removido, "Anais Estendidos"),
    ]


def main() -> int:
    if shutil.which("pdflatex") is None:
        print("FALHOU: sem pdflatex, o controle positivo nao pode rodar")
        return 1

    escapadas: list[str] = []
    casos = mutacoes()
    for i, (nome, aplicar, esperado) in enumerate(casos, start=1):
        with tempfile.TemporaryDirectory() as tmp:
            copia = Path(tmp) / "paper"
            shutil.copytree(ARTIGO, copia)
            for lixo in copia.glob("artigo.*"):
                if lixo.suffix in {".aux", ".bbl", ".blg", ".log", ".pdf", ".out"}:
                    lixo.unlink()
            aplicar(copia)
            saida = subprocess.run(
                [sys.executable, str(VERIFICADOR), str(copia)],
                cwd=RAIZ,
                capture_output=True,
                text=True,
            )
            acusou = saida.returncode != 0
            certo = acusou and (not esperado or esperado in saida.stdout)
            print(f"[{i:>2}/{len(casos)}] {'ok ' if certo else 'ESCAPOU'} {nome}")
            if not certo:
                escapadas.append(nome)
                for linha in saida.stdout.splitlines()[-6:]:
                    print(f"          {linha}")

    if escapadas:
        print(f"\nFALHOU: {len(escapadas)} mutacao(oes) nao acusada(s):")
        for nome in escapadas:
            print(f"  - {nome}")
        return 1
    print(f"\nOK: as {len(casos)} mutacoes foram todas acusadas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
