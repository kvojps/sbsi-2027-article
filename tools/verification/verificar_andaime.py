#!/usr/bin/env python3
"""Verifica o andaime do artigo contra a checklist do ticket 02.

Uso: python tools/verification/verificar_andaime.py [diretorio-do-artigo]

Confere quatro coisas, nesta ordem:

  1. o esqueleto Markdown tem as nove secoes, cada uma com o label do resumo
     estruturado que carrega e com o orcamento de paginas anotado, e o
     orcamento total cabe no intervalo exigido pela chamada;
  2. o scaffold LaTeX nao reintroduziu o inputenc latin1 do template original,
     tem as mesmas nove secoes na mesma ordem do esqueleto e nao carrega nome
     de autor, instituicao nem agradecimento;
  3. a bibliografia esta sa: nenhuma entrada sem os campos obrigatorios do seu
     tipo, nenhum marcador de placeholder sobrevivente, e as entradas que os
     pareceres do ONTOBRAS apontaram como incompletas agora completas;
  4. Anais do SBSI, Anais Estendidos do SBSI e iSys presentes na bibliografia.

Se houver log de compilacao ao lado do .tex, confere tambem que nenhuma chamada
de referencia ficou quebrada (o `[?]` que um parecer apontou).

Sai com codigo 1 se qualquer verificacao falhar.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

DIRETORIO_PADRAO = Path("artifacts/paper")

PAGINAS_MIN = 15
PAGINAS_MAX = 20

LABELS = [
    "Research Context",
    "Scientific and/or Practical Problem",
    "Proposed Solution and/or Analysis",
    "Related IS Theory",
    "Research Method",
    "Summary of Results",
    "Contributions and Impact to IS area",
]

# As nove secoes, na ordem. O esqueleto e o scaffold precisam concordar.
SECOES = [
    "Introdução",
    "Referencial Teórico",
    "Trabalhos Relacionados",
    "Método de Pesquisa",
    "Análise Ontológica do MPO",
    "A OntoMPO Revisada",
    "Avaliação",
    "Discussão e Limitações",
    "Conclusão e Trabalhos Futuros",
]

# Termos que quebram o anonimato da revisao duplamente anonima.
TERMOS_IDENTIFICADORES = [
    "josé ferreira",
    "santos júnior",
    "santos junior",
    "ivaldir",
    "hermano",
    "universidade de pernambuco",
    "poli.br",
    "upe.br",
    "github.com/",
    "agradecimento",
    "acknowledgment",
    "\\thanks",
]

# Chaves que os pareceres do ONTOBRAS apontaram como referencias incompletas
# (referencias 1, 7 e 8 daquele artigo), com o campo que faltava em cada uma.
CHAVES_APONTADAS = {
    "figueiredo2016papel": "school",
    "guizzardi2005ontological": "school",
    "fernandez1997methontology": "booktitle",
}

CAMPOS_OBRIGATORIOS = {
    "article": [["author"], ["title"], ["journal"], ["year"]],
    "book": [["author", "editor"], ["title"], ["publisher"], ["year"]],
    "inbook": [["author", "editor"], ["title"], ["publisher"], ["year"]],
    "incollection": [["author"], ["title"], ["booktitle"], ["publisher"], ["year"]],
    "inproceedings": [["author"], ["title"], ["booktitle"], ["year"]],
    "mastersthesis": [["author"], ["title"], ["school"], ["year"]],
    "phdthesis": [["author"], ["title"], ["school"], ["year"]],
    "techreport": [["author"], ["title"], ["institution"], ["year"]],
    "misc": [["title"], ["author", "howpublished"], ["year"]],
}

# Restos de captura automatica que ja' apareceram nesta bibliografia.
PLACEHOLDERS = [
    "sobrenome, nome",
    "local do evento",
    "sitewide atom",
    "initiative, social business",
    "author={guide, a}",
    "0000-0000",
    "todo:",
    "xxxx",
]

# O bibtex avisa quando ha' number sem volume. Prisma.com e UVserva numeram
# fasciculos sem volume; inventar um volume para calar o aviso seria trocar uma
# entrada correta por uma errada. E' o unico aviso tolerado.
TOLERADO_NO_BIBTEX = re.compile(r"there's a number but no volume")

ENTRADA_RE = re.compile(r"^@(?P<tipo>\w+)\s*\{\s*(?P<chave>[^,\s]+)\s*,", re.MULTILINE)
CAMPO_RE = re.compile(r"(?P<nome>\w+)\s*=\s*[{\"]")
LINHA_TABELA_RE = re.compile(r"^\|\s*(?P<num>\d+)\s*\|(?P<resto>.*)\|\s*$")
SECAO_TEX_RE = re.compile(r"^\\section\{(?P<nome>[^}]*)\}", re.MULTILINE)


def blocos_bib(texto: str) -> list[tuple[str, str, str]]:
    """Devolve (tipo, chave, corpo) de cada entrada, com comentarios removidos."""
    sem_comentario = "\n".join(
        linha for linha in texto.splitlines() if not linha.lstrip().startswith("%")
    )
    achados = list(ENTRADA_RE.finditer(sem_comentario))
    blocos = []
    for i, m in enumerate(achados):
        fim = achados[i + 1].start() if i + 1 < len(achados) else len(sem_comentario)
        blocos.append((m.group("tipo").lower(), m.group("chave"), sem_comentario[m.end() : fim]))
    return blocos


def verificar_esqueleto(caminho: Path) -> tuple[list[str], list[str]]:
    """Confere as nove secoes, seus labels e o orcamento. Devolve (falhas, secoes)."""
    falhas: list[str] = []
    if not caminho.exists():
        return [f"esqueleto nao encontrado em {caminho}"], []

    texto = caminho.read_text(encoding="utf-8")

    linhas = [LINHA_TABELA_RE.match(l) for l in texto.splitlines()]
    numeradas = [m for m in linhas if m]
    if len(numeradas) != len(SECOES):
        falhas.append(
            f"a tabela de orcamento tem {len(numeradas)} secoes numeradas, esperadas {len(SECOES)}"
        )

    encontradas: list[str] = []
    total = 0.0
    for m in numeradas:
        colunas = [c.strip() for c in m.group("resto").split("|")]
        if len(colunas) < 3:
            falhas.append(f"linha {m.group('num')} da tabela sem as tres colunas esperadas")
            continue
        nome, labels_da_secao, paginas = colunas[0], colunas[1], colunas[2]
        encontradas.append(nome)

        if not any(label in labels_da_secao for label in LABELS):
            falhas.append(f"secao {m.group('num')} ({nome}) sem label do resumo estruturado")

        try:
            total += float(paginas.replace(",", "."))
        except ValueError:
            falhas.append(f"secao {m.group('num')} ({nome}) sem orcamento de paginas numerico")

    if encontradas and encontradas != SECOES:
        falhas.append(f"secoes do esqueleto divergem do esperado: {encontradas}")

    # As linhas sem numero (frontmatter, declaracao, referencias, apendice) tambem
    # ocupam paginas e entram no total do artigo.
    for rotulo in ("Frontmatter", "Declaração de uso de IA generativa", "Referências", "Apêndice A"):
        m = re.search(
            r"^\|\s*—\s*\|[^|]*" + re.escape(rotulo) + r"[^|]*\|[^|]*\|\s*([\d,\.]+)\s*\|",
            texto,
            re.MULTILINE,
        )
        if not m:
            falhas.append(f"orcamento ausente para: {rotulo}")
            continue
        total += float(m.group(1).replace(",", "."))

    print(f"orcamento total do esqueleto: {total:.2f} paginas (chamada exige {PAGINAS_MIN}-{PAGINAS_MAX})")
    if not (PAGINAS_MIN <= total <= PAGINAS_MAX):
        falhas.append(f"orcamento total de {total:.2f} paginas fora do intervalo da chamada")

    ausentes = [label for label in LABELS if label not in texto]
    if ausentes:
        falhas.append(f"labels do resumo estruturado ausentes do esqueleto: {ausentes}")

    return falhas, encontradas


def verificar_scaffold(caminho: Path) -> list[str]:
    falhas: list[str] = []
    if not caminho.exists():
        return [f"scaffold LaTeX nao encontrado em {caminho}"]

    texto = caminho.read_text(encoding="utf-8")
    ativo = "\n".join(l for l in texto.splitlines() if not l.lstrip().startswith("%"))

    if "latin1" in ativo:
        falhas.append("o \\usepackage[latin1]{inputenc} do template voltou; os acentos vao quebrar")
    if "[utf8]{inputenc}" not in ativo:
        falhas.append("o scaffold nao declara \\usepackage[utf8]{inputenc}")

    secoes_tex = [m.group("nome") for m in SECAO_TEX_RE.finditer(ativo)]
    if secoes_tex != SECOES:
        falhas.append(f"secoes do scaffold divergem do esperado: {secoes_tex}")

    for macro, esperado in (("author", "\\author{}"), ("address", "\\address{}")):
        if esperado not in ativo:
            falhas.append(f"\\{macro} nao esta vazio no scaffold; a revisao e' duplamente anonima")

    baixo = ativo.lower()
    achados = [t for t in TERMOS_IDENTIFICADORES if t in baixo]
    if achados:
        falhas.append(f"scaffold contem identificacao de autoria/instituicao: {achados}")

    if "\\bibliography{referencias}" not in ativo:
        falhas.append("o scaffold nao aponta para a bibliografia referencias.bib")
    if "\\bibliographystyle{sbc}" not in ativo:
        falhas.append("o scaffold nao usa o estilo bibliografico sbc")

    return falhas


def verificar_bibliografia(caminho: Path) -> list[str]:
    falhas: list[str] = []
    if not caminho.exists():
        return [f"bibliografia nao encontrada em {caminho}"]

    texto = caminho.read_text(encoding="utf-8")
    blocos = blocos_bib(texto)
    print(f"bibliografia: {len(blocos)} entradas")

    chaves = {chave for _, chave, _ in blocos}
    if len(chaves) != len(blocos):
        falhas.append("ha' chaves duplicadas na bibliografia")

    for tipo, chave, corpo in blocos:
        campos = {m.group("nome").lower() for m in CAMPO_RE.finditer(corpo)}
        exigidos = CAMPOS_OBRIGATORIOS.get(tipo)
        if exigidos is None:
            falhas.append(f"{chave}: tipo @{tipo} desconhecido por esta verificacao")
            continue
        for alternativas in exigidos:
            if not campos & set(alternativas):
                falhas.append(f"{chave} (@{tipo}): entrada incompleta, falta {' ou '.join(alternativas)}")

    # O cabecalho comentado do .bib cita nominalmente "Anais do SBSI", "Anais
    # Estendidos" e "iSys" ao explicar o que foi portado. Toda busca por
    # conteudo tem de correr sobre o corpo sem comentarios, ou o arquivo passa
    # a atestar a si mesmo.
    corpo_ativo = "\n".join(
        l for l in texto.splitlines() if not l.lstrip().startswith("%")
    ).lower()
    corpo_sem_espaco = re.sub(r"\s+", "", corpo_ativo)
    for marcador in PLACEHOLDERS:
        if marcador in corpo_ativo or re.sub(r"\s+", "", marcador) in corpo_sem_espaco:
            falhas.append(f"placeholder sobrevivente na bibliografia: {marcador!r}")

    for chave, campo in CHAVES_APONTADAS.items():
        bloco = next((c for t, k, c in blocos if k == chave), None)
        if bloco is None:
            falhas.append(f"{chave}: entrada apontada como incompleta pelos pareceres esta' ausente")
        elif campo not in {m.group("nome").lower() for m in CAMPO_RE.finditer(bloco)}:
            falhas.append(f"{chave}: continua sem o campo {campo} que os pareceres cobraram")

    exigencias_da_chamada = {
        "Anais do SBSI": r"anais do \{?[ivx]+\}? simp",
        "Anais Estendidos do SBSI": r"anais estendidos",
        "iSys": r"isys",
    }
    for rotulo, padrao in exigencias_da_chamada.items():
        if not re.search(padrao, corpo_ativo):
            falhas.append(f"bibliografia sem entrada de {rotulo}, exigida pela chamada")

    return falhas


def verificar_compilacao(diretorio: Path) -> list[str]:
    """Se houver log de compilacao, confere que nenhuma chamada ficou quebrada."""
    falhas: list[str] = []
    log = diretorio / "artigo.log"
    if not log.exists():
        print("aviso: artigo.log ausente; a compilacao nao foi conferida por este script")
        return falhas

    texto = log.read_text(encoding="utf-8", errors="replace")
    if "Citation" in texto and "undefined" in texto:
        for m in re.finditer(r"Citation `([^']+)' on page \d+ undefined", texto):
            falhas.append(f"chamada quebrada ([?]) para a citacao {m.group(1)!r}")
    if re.search(r"^! ", texto, re.MULTILINE):
        falhas.append("a compilacao registrou erro de LaTeX (linha iniciada por '!') em artigo.log")

    blg = diretorio / "artigo.blg"
    if blg.exists():
        texto_blg = blg.read_text(encoding="utf-8", errors="replace")
        for linha in texto_blg.splitlines():
            if linha.startswith("Warning--") or linha.startswith("I couldn't"):
                if TOLERADO_NO_BIBTEX.search(linha):
                    continue
                falhas.append(f"bibtex reclamou: {linha.strip()}")
    else:
        print("aviso: artigo.blg ausente; o bibtex nao foi conferido por este script")

    return falhas


def main() -> int:
    diretorio = Path(sys.argv[1]) if len(sys.argv) > 1 else DIRETORIO_PADRAO

    falhas: list[str] = []
    falhas_esqueleto, _ = verificar_esqueleto(diretorio / "esqueleto.md")
    falhas += falhas_esqueleto
    falhas += verificar_scaffold(diretorio / "artigo.tex")
    falhas += verificar_bibliografia(diretorio / "referencias.bib")
    falhas += verificar_compilacao(diretorio)

    if falhas:
        print(f"FALHOU ({len(falhas)}):")
        for f in falhas:
            print(f"  - {f}")
        return 1
    print("OK: andaime conforme a checklist do ticket 02")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
