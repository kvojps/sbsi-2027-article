#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifica o port para LaTeX, as figuras e a paginacao (checklist do ticket 13).

Uso: python tools/verification/verificar_port_latex.py [diretorio-do-artigo]

O que o ticket 13 entrega e' o PDF: o texto das secoes portado para o template
SBC, as figuras regeradas a partir do **modelo revisado**, o Apendice A e a
extensao dentro do intervalo que a chamada exige. Este verificador compila o
artigo numa copia e confronta o PDF resultante com as fontes que deveriam
te-lo produzido, sem importar de nenhum gerador:

  1. **compila**, no ciclo `pdflatex -> bibtex -> pdflatex -> pdflatex`, sem
     nenhum erro de LaTeX e sem citacao indefinida;
  2. **os acentos sobrevivem a extracao de texto**. Nao basta o PDF sair certo
     aos olhos: e' sobre o texto extraido que a varredura de anonimato do ticket
     14 trabalha, e sem `fontenc` o pdflatex compoe cada acento como glifo
     sobreposto e a extracao devolve `Introduc,a~o`;
  3. **o PDF diz o que o Markdown diz.** O texto mora em `secoes/*.md`, e e' de
     la' que os verificadores dos tickets 10 a 12 o conferem; aqui, cada trecho
     de cada paragrafo daqueles arquivos e' procurado no texto extraido do PDF.
     E' o que impede o port de envelhecer: corrigir o Markdown e esquecer de
     regerar reprova, e editar o `.tex` gerado a mao tambem;
  4. **nenhuma figura vem do modelo antigo.** As imagens disponiveis sao do
     modelo anterior a analise, e reaproveita-las publicaria diagramas que
     contradizem a secao 5 — o artigo mostraria os defeitos ao lado da
     afirmacao de que foram corrigidos. Entao: nenhum `\\includegraphics`
     aponta para fora de `figuras/`, nenhum arquivo do diretorio do artigo e'
     copia byte a byte de uma imagem da dissertacao, e cada classe, relacao e
     generalizacao desenhada existe no `ontompo-rodada-2.ontouml.json` — com as
     44 classes do modelo presentes no diagrama integrado;
  5. **as figuras sao legiveis no tamanho impresso**: nenhum corpo declarado no
     TikZ desce abaixo do piso, e a caixa mais larga cabe na largura do texto;
  6. **a bibliografia compila** — o `\\nocite{*}` provisorio do scaffold saiu,
     toda chave citada tem entrada, nenhuma chamada sai como `[?]`, nenhuma
     entrada da bibliografia impressa esta' incompleta, e os veiculos que a
     chamada exige estao entre os citados, e nao apenas no `.bib`;
  7. **o frontmatter bate com o registro congelado no JEMS3**, bloco a bloco:
     depois de 14/09/2026 o registro nao muda mais, e uma divergencia entre PDF
     e registro e' achado de conformidade. Os sete labels aparecem nomeados no
     abstract e no resumo, e as palavras-chave em ingles estao no PDF;
  8. **a estrutura de secoes reflete os sete labels**: as nove secoes saem no
     PDF na ordem do esqueleto, e cada label e' carregado por ao menos uma;
  9. **o Apendice A** traz as consultas e resultados completos ou a remissao
     explicita ao deposito, e o que ele mostra da consulta e' o arquivo `.rq`,
     nao uma transcricao;
 10. **a extensao esta entre 15 e 20 paginas**, contada no PDF renderizado.
     Regra de desk reject nos dois sentidos.

Sai com codigo 1 se qualquer verificacao falhar.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ARTIGO_PADRAO = Path("artifacts/paper")
MODELO = Path("artifacts/ontology/rodada-2/ontompo-rodada-2.ontouml.json")
CONSULTAS = Path("artifacts/ontology/consultas")
REGISTRO_JEMS3 = Path("artifacts/submission/jems3-pacote-registro.md")
IMAGENS_DA_FONTE = Path("sources/dissertation")

PAGINAS_MIN = 15
PAGINAS_MAX = 20

# Os nove nomes de secao, na ordem do esqueleto, e os labels que cada uma
# carrega. Sao os mesmos do andaime (ticket 02) — a duplicacao e' deliberada:
# se divergirem, os dois verificadores dizem, e nenhum depende do outro.
SECOES = (
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

LABELS = (
    "Research Context",
    "Scientific and/or Practical Problem",
    "Proposed Solution and/or Analysis",
    "Related IS Theory",
    "Research Method",
    "Summary of Results",
    "Contributions and Impact to IS area",
)

# Palavras acentuadas que precisam sair inteiras da extracao de texto, e os
# restos que denunciam a composicao por glifo sobreposto.
ACENTOS_ESPERADOS = (
    "Introdução",
    "Referencial Teórico",
    "Método de Pesquisa",
    "Análise Ontológica",
    "Avaliação",
    "Discussão e Limitações",
    "Conclusão",
    "Referências",
    "Apêndice",
)
ACENTOS_QUEBRADOS = ("Introduc", "c,a~o", "Ã§", "Ã£", "\ufffd")

# Piso de corpo dentro das figuras, em pontos. Abaixo disso a caixa nao se le'
# no tamanho impresso.
CORPO_MINIMO_PT = 5.0

# Largura util do texto no template SBC: A4 (21cm) menos 3cm de cada margem.
LARGURA_TEXTO_CM = 15.0

QCS = tuple(f"qc{i}" for i in range(1, 8))

# Veiculos que a chamada exige, e o padrao que os reconhece na bibliografia
# **impressa** — nao basta a entrada existir no `.bib` se o texto nao a cita.
VEICULOS_DA_CHAMADA = {
    "Anais do SBSI": r"anais do \{?[ivx]+\}? simp",
    "Anais Estendidos do SBSI": r"anais estendidos",
    "iSys": r"isys",
    "II GranDSI-Br": r"grandsi",
}

# O unico aviso do bibtex que o ticket 02 declarou tolerado.
AVISO_TOLERADO = re.compile(r"there's a number but no volume")

CITACAO_NO_MARKDOWN = re.compile(
    r"\[[A-Za-z][A-Za-z0-9_]*(?:\s*,\s*[A-Za-z][A-Za-z0-9_]*)*\]", re.S
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
    # `errors="replace"`: o `.log` do pdflatex mistura codificacoes (nomes de
    # arquivo do sistema, avisos do proprio TeX) e nao e' utf-8 valido.
    try:
        return caminho.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _compacta(texto: str) -> str:
    """Reduz um texto a comparar: sem espaco, sem hifen, minusculo.

    A hifenizacao de fim de linha do LaTeX quebra palavra no meio, e a extracao
    de texto ora mantem o hifen ora nao; comparar sem espaco e sem hifen tira as
    duas fontes de ruido sem afrouxar a comparacao — um trecho de seis palavras
    nao coincide por acaso.
    """
    texto = texto.replace("\u00ad", "").replace("²", "2")
    texto = re.sub(r"[“”]", '"', texto).replace("«", "").replace("»", "")
    return re.sub(r"[\s\-\u2013\u2014]+", "", texto).lower()


# --------------------------------------------------------------------------
# 1. compilacao
# --------------------------------------------------------------------------


def compilar(diretorio: Path) -> dict | None:
    """Compila o artigo numa copia e devolve log, texto extraido e paginas."""
    if any(shutil.which(x) is None for x in ("pdflatex", "bibtex", "pdftotext", "pdfinfo")):
        return None
    with tempfile.TemporaryDirectory() as tmp:
        destino = Path(tmp)
        for item in diretorio.iterdir():
            if item.suffix in {".aux", ".bbl", ".blg", ".log", ".pdf", ".out"}:
                continue
            if item.is_dir():
                shutil.copytree(item, destino / item.name)
            else:
                shutil.copy(item, destino / item.name)
        ambiente = {**os.environ, "max_print_line": "1000"}
        for passo in ("pdflatex", "bibtex", "pdflatex", "pdflatex"):
            argumentos = (
                [passo, "artigo"]
                if passo == "bibtex"
                else [passo, "-interaction=nonstopmode", "artigo.tex"]
            )
            subprocess.run(argumentos, cwd=destino, capture_output=True, env=ambiente)
        pdf = destino / "artigo.pdf"
        if not pdf.exists():
            return {"log": _ler(destino / "artigo.log"), "pdf": None}
        extraido = subprocess.run(
            ["pdftotext", "-nopgbrk", str(pdf), "-"], capture_output=True, text=True
        ).stdout
        paginas = subprocess.run(
            ["pdfinfo", str(pdf)], capture_output=True, text=True
        ).stdout
        contagem = re.search(r"Pages:\s+(\d+)", paginas)
        return {
            "log": _ler(destino / "artigo.log"),
            "blg": _ler(destino / "artigo.blg"),
            "bbl": _ler(destino / "artigo.bbl"),
            "texto": extraido,
            "paginas": int(contagem.group(1)) if contagem else None,
            "pdf": True,
        }


def verificar_compilacao(saida: dict, res: Resultado) -> None:
    log = saida.get("log", "")
    if not res.exigir(saida.get("pdf"), "a compilacao nao produziu artigo.pdf"):
        for linha in re.findall(r"(?m)^!.*$", log)[:5]:
            res.falhas.append(f"  erro de LaTeX: {linha.strip()}")
        return

    erros = re.findall(r"(?m)^!.*$", log)
    res.exigir(not erros, f"a compilacao registrou erro de LaTeX: {erros[:3]}")

    indefinidas = re.findall(r"Citation `([^']+)' on page \d+ undefined", log)
    res.exigir(
        not indefinidas,
        f"citacao sem entrada no .bib, sai como [?] no PDF: {sorted(set(indefinidas))}",
    )
    res.exigir(
        "There were undefined references" not in log,
        "a compilacao reclamou de referencia indefinida",
    )
    res.exigir(
        "[?]" not in saida.get("texto", ""),
        "o PDF traz uma chamada quebrada [?]",
    )

    for linha in saida.get("blg", "").splitlines():
        if linha.startswith(("Warning--", "I couldn't")) and not AVISO_TOLERADO.search(linha):
            res.exigir(False, f"bibtex reclamou: {linha.strip()}")


def verificar_acentos(texto: str, res: Resultado) -> None:
    for palavra in ACENTOS_ESPERADOS:
        res.exigir(
            palavra in texto,
            f"a extracao de texto do PDF nao devolve {palavra!r} com os acentos inteiros",
        )
    for resto in ACENTOS_QUEBRADOS:
        res.exigir(
            resto not in texto,
            f"a extracao de texto traz {resto!r}: acento composto como glifo sobreposto",
        )


# --------------------------------------------------------------------------
# 2. o PDF diz o que o Markdown diz
# --------------------------------------------------------------------------


def trechos_do_markdown(markdown: str) -> list[str]:
    """Os trechos de prosa de uma secao, quebrados nas citacoes.

    Citacao vira `[Autor et al. ano]` no PDF, e comparar com a chave do Markdown
    seria comparar coisas diferentes: o trecho e' partido nela e cada pedaco
    conferido por si.
    """
    markdown = re.sub(r"<!--.*?-->", "", markdown, flags=re.DOTALL)
    markdown = re.sub(r"```.*?```", "", markdown, flags=re.DOTALL)
    trechos: list[str] = []
    for paragrafo in markdown.split("\n\n"):
        paragrafo = paragrafo.strip()
        if not paragrafo or paragrafo.startswith("#") or paragrafo.lstrip().startswith("|"):
            continue
        paragrafo = re.sub(r"^\s*-\s+", "", paragrafo, flags=re.MULTILINE)
        paragrafo = paragrafo.replace("**", "").replace("*", "").replace("`", "")
        for pedaco in CITACAO_NO_MARKDOWN.sub("\x00", paragrafo).split("\x00"):
            if len(pedaco.split()) >= 6:
                trechos.append(pedaco.strip())
    return trechos


def verificar_fidelidade(diretorio: Path, texto_pdf: str, res: Resultado) -> None:
    compacto = _compacta(texto_pdf)
    fontes = sorted((diretorio / "secoes").glob("*.md"))
    if not res.exigir(bool(fontes), "nao ha secoes/*.md para conferir contra o PDF"):
        return
    total = 0
    for fonte in fontes:
        ausentes = []
        for trecho in trechos_do_markdown(_ler(fonte)):
            total += 1
            if _compacta(trecho).strip(".,;:") not in compacto:
                ausentes.append(trecho)
        detalhe = (
            f"{fonte.name}: {len(ausentes)} trecho(s) do Markdown nao estao no PDF — o port "
            f"envelheceu ou o .tex foi editado a mao. Primeiro: {ausentes[0][:90]!r}"
            if ausentes
            else ""
        )
        res.exigir(not ausentes, detalhe)
    print(f"trechos do Markdown conferidos no PDF: {total}")


# --------------------------------------------------------------------------
# 3. figuras
# --------------------------------------------------------------------------


def elementos_do_modelo(caminho: Path) -> dict | None:
    if not caminho.exists():
        return None
    conteudo = json.loads(caminho.read_text(encoding="utf-8"))["model"]["contents"]
    por_id = {x["id"]: x for x in conteudo}
    classes = {x["name"] for x in conteudo if x["type"] == "Class"}
    arestas = set()
    for x in conteudo:
        if x["type"] == "Generalization":
            arestas.add(
                frozenset(
                    (por_id[x["specific"]["id"]]["name"], por_id[x["general"]["id"]]["name"])
                )
            )
        elif x["type"] == "Relation":
            pontas = [por_id.get(p["propertyType"]["id"]) for p in x["properties"]]
            nomes = [p["name"] for p in pontas if p and p["type"] == "Class"]
            if len(nomes) == 2:
                arestas.add(frozenset(nomes))
    return {"classes": classes, "arestas": arestas}


def medir_figura(diretorio: Path, figura: Path) -> tuple[float, float] | None:
    """Compila a figura sozinha no template e devolve (largura, largura do texto) em cm.

    Medir compilando, e nao somando as coordenadas do TikZ, porque o que sangra
    para fora da mancha e' a caixa desenhada — rotulo de legenda inclusive —, e
    so' o TeX sabe quanto ela mede depois de composta.
    """
    if shutil.which("pdflatex") is None:
        return None
    prova = "\n".join((
        r"\documentclass[12pt]{article}",
        r"\usepackage{sbc-template}",
        r"\usepackage[utf8]{inputenc}",
        r"\usepackage[T1]{fontenc}",
        r"\usepackage[brazilian]{babel}",
        r"\usepackage{tikz}",
        r"\usetikzlibrary{positioning,fit,backgrounds,arrows.meta,calc}",
        r"\newsavebox\caixa",
        r"\begin{document}",
        r"\sbox\caixa{\input{" + figura.stem + "}}",
        r"\typeout{MEDIDA \the\wd\caixa\space de \the\textwidth}",
        r"\end{document}",
    ))
    with tempfile.TemporaryDirectory() as tmp:
        destino = Path(tmp)
        shutil.copy(figura, destino / figura.name)
        shutil.copy(diretorio / "sbc-template.sty", destino / "sbc-template.sty")
        (destino / "prova.tex").write_text(prova, encoding="utf-8")
        ambiente = {**os.environ, "max_print_line": "1000"}
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "prova.tex"],
            cwd=destino,
            capture_output=True,
            env=ambiente,
        )
        log = _ler(destino / "prova.log")
    achado = re.search(r"MEDIDA ([\d.]+)pt de ([\d.]+)pt", log)
    if not achado:
        return None
    ponto_em_cm = 2.54 / 72.27
    return float(achado.group(1)) * ponto_em_cm, float(achado.group(2)) * ponto_em_cm


def verificar_figuras(diretorio: Path, res: Resultado) -> None:
    modelo = elementos_do_modelo(MODELO)
    if not res.exigir(modelo is not None, f"{MODELO} ausente: as figuras nao podem ser conferidas"):
        return

    figuras = sorted((diretorio / "figuras").glob("*.tex"))
    if not res.exigir(bool(figuras), "nao ha figuras em figuras/*.tex"):
        return

    integrada = diretorio / "figuras" / "ontompo-integrado.tex"
    res.exigir(integrada.exists(), "o diagrama integrado nao existe; o esqueleto o mantem no artigo")

    for figura in figuras:
        corpo = _ler(figura)
        nomes = set(re.findall(r"\\node\[classe\] \(n([A-Za-z0-9]+)\)", corpo))
        inventadas = nomes - modelo["classes"]
        res.exigir(
            not inventadas,
            f"{figura.name}: desenha classe que nao existe no modelo revisado: {sorted(inventadas)}",
        )
        arestas = {
            frozenset(par)
            for par in re.findall(r"\\draw\[\w+\] \(n([A-Za-z0-9]+)\) -- \(n([A-Za-z0-9]+)\);", corpo)
        }
        invalidas = arestas - modelo["arestas"]
        res.exigir(
            not invalidas,
            f"{figura.name}: desenha ligacao que o modelo revisado nao tem: "
            f"{[sorted(p) for p in sorted(invalidas, key=sorted)][:3]}",
        )
        corpos = [float(m) for m in re.findall(r"\\fontsize\{([\d.]+)\}", corpo)]
        res.exigir(
            bool(corpos) and min(corpos) >= CORPO_MINIMO_PT,
            f"{figura.name}: corpo de {min(corpos) if corpos else 0}pt na figura, "
            f"abaixo do piso de {CORPO_MINIMO_PT}pt para leitura impressa",
        )
        medida = medir_figura(diretorio, figura)
        if res.exigir(
            medida is not None,
            f"{figura.name}: nao compila sozinha no template SBC",
        ):
            largura, texto = medida
            res.exigir(
                largura <= texto + 0.01,
                f"{figura.name}: mede {largura:.2f}cm e a largura do texto no template e' "
                f"{texto:.2f}cm — a figura sangra para fora da mancha",
            )

    nomes_integrada = set(re.findall(r"\\node\[classe\] \(n([A-Za-z0-9]+)\)", _ler(integrada)))
    faltando = modelo["classes"] - nomes_integrada
    res.exigir(
        not faltando,
        f"o diagrama integrado nao mostra {len(faltando)} classe(s) do modelo revisado: "
        f"{sorted(faltando)[:6]}",
    )
    print(f"figuras: {len(figuras)}, {len(nomes_integrada)} classes no diagrama integrado")


def verificar_ausencia_do_modelo_antigo(diretorio: Path, res: Resultado) -> None:
    """Nenhuma imagem do modelo anterior a analise sobrevive no artigo."""
    fonte = _ler(diretorio / "artigo.tex") + "".join(
        _ler(p) for p in sorted((diretorio / "secoes-tex").glob("*.tex"))
    )
    incluidas = re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]*)\}", fonte)
    res.exigir(
        not incluidas,
        f"o artigo inclui imagem pronta: {incluidas}. As figuras do artigo sao geradas do "
        "modelo revisado; imagem do modelo antigo contradiz a secao 5",
    )
    entradas = {p.name for p in (diretorio / "figuras").glob("*")} if (diretorio / "figuras").is_dir() else set()
    res.exigir(
        all(e.endswith(".tex") for e in entradas),
        f"figuras/ tem arquivo que nao e' TikZ gerado: "
        f"{sorted(e for e in entradas if not e.endswith('.tex'))}",
    )

    if not IMAGENS_DA_FONTE.is_dir():
        return
    digests = set()
    for imagem in IMAGENS_DA_FONTE.rglob("*"):
        if imagem.is_file() and imagem.suffix.lower() in {".png", ".jpg", ".jpeg", ".pdf", ".eps"}:
            digests.add(hashlib.sha256(imagem.read_bytes()).hexdigest())
    copiadas = []
    for arquivo in diretorio.rglob("*"):
        if arquivo.is_file() and arquivo.suffix.lower() in {".png", ".jpg", ".jpeg", ".eps"}:
            if hashlib.sha256(arquivo.read_bytes()).hexdigest() in digests:
                copiadas.append(arquivo.name)
    res.exigir(
        not copiadas,
        f"imagem da dissertacao copiada para o diretorio do artigo: {copiadas}",
    )


# --------------------------------------------------------------------------
# 4. bibliografia
# --------------------------------------------------------------------------


def verificar_preambulo(diretorio: Path, res: Resultado) -> None:
    """As duas opcoes de codificacao de que os acentos dependem.

    O template SBC traz `utf8` e `latin1` nesta ordem, e o segundo vence: com ele
    todo acento do corpo em portugues quebra. O ticket 02 o removeu; se voltar,
    o pdflatex ainda reclama de opcao repetida, mas a mensagem nao diz o que
    aconteceu — esta verificacao diz.
    """
    ativo = "\n".join(
        l for l in _ler(diretorio / "artigo.tex").splitlines() if not l.lstrip().startswith("%")
    )
    res.exigir(
        "latin1" not in ativo,
        "o \\usepackage[latin1]{inputenc} do template voltou; os acentos do corpo em "
        "portugues quebram",
    )
    res.exigir(
        "[utf8]{inputenc}" in ativo,
        "o artigo nao declara \\usepackage[utf8]{inputenc}",
    )
    res.exigir(
        "{fontenc}" in ativo,
        "o artigo nao declara fontenc; sem ele a extracao de texto do PDF devolve "
        "acento como glifo sobreposto, e e' sobre ela que o ticket 14 trabalha",
    )


def verificar_bibliografia(diretorio: Path, saida: dict, res: Resultado) -> None:
    tex = _ler(diretorio / "artigo.tex")
    ativo = "\n".join(l for l in tex.splitlines() if not l.lstrip().startswith("%"))
    res.exigir(
        "\\nocite{*}" not in ativo,
        "o \\nocite{*} provisorio do scaffold sobreviveu: a bibliografia traz entrada nao citada",
    )

    corpo = ativo + "".join(
        _ler(p) for p in sorted((diretorio / "secoes-tex").glob("*.tex"))
    )
    citadas = set()
    for grupo in re.findall(r"\\cite\{([^}]*)\}", corpo):
        citadas.update(c.strip() for c in grupo.split(","))
    res.exigir(bool(citadas), "o artigo nao cita nenhuma entrada da bibliografia")

    bib = _ler(diretorio / "referencias.bib")
    chaves = set(re.findall(r"(?m)^@\w+\{([^,]+),", bib))
    orfas = citadas - chaves
    res.exigir(not orfas, f"chave citada sem entrada no referencias.bib: {sorted(orfas)}")

    impressas = set(re.findall(r"\\bibitem\[[^\]]*\]\{([^}]*)\}", saida.get("bbl", "")))
    res.exigir(
        impressas == citadas,
        f"a bibliografia impressa diverge do que o texto cita: "
        f"so' na impressa {sorted(impressas - citadas)}, so' no texto {sorted(citadas - impressas)}",
    )

    bbl_min = saida.get("bbl", "").lower()
    for rotulo, padrao in VEICULOS_DA_CHAMADA.items():
        res.exigir(
            re.search(padrao, bbl_min) is not None,
            f"a bibliografia impressa nao traz {rotulo}, exigido pela chamada",
        )
    print(f"bibliografia impressa: {len(impressas)} entradas citadas")


# --------------------------------------------------------------------------
# 5. frontmatter e estrutura
# --------------------------------------------------------------------------


def blocos_do_registro(registro: str) -> dict[str, str]:
    """Os sete blocos do resumo congelado no JEMS3, por label."""
    achado = re.search(r"<!-- campo: resumo -->\s*```text\n(.*?)```", registro, re.DOTALL)
    if not achado:
        return {}
    blocos = {}
    for label in LABELS:
        m = re.search(
            re.escape(label) + r"\.\s*(.*?)(?=(?:" + "|".join(re.escape(x) for x in LABELS) + r")\.|\Z)",
            achado.group(1),
            re.DOTALL,
        )
        if m:
            blocos[label] = m.group(1)
    return blocos


def verificar_frontmatter(diretorio: Path, texto_pdf: str, res: Resultado) -> None:
    tex = _ler(diretorio / "artigo.tex")
    abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", tex, re.DOTALL)
    resumo = re.search(r"\\begin\{resumo\}(.*?)\\end\{resumo\}", tex, re.DOTALL)
    if not res.exigir(abstract is not None, "o artigo nao tem abstract"):
        return
    if not res.exigir(resumo is not None, "o artigo nao tem resumo em portugues"):
        return

    for label in LABELS:
        res.exigir(
            label in abstract.group(1),
            f"o abstract estruturado nao nomeia o label {label!r}",
        )
        res.exigir(
            _compacta(label) in _compacta(texto_pdf),
            f"o label {label!r} nao aparece no PDF renderizado",
        )

    registro = _ler(REGISTRO_JEMS3)
    blocos = blocos_do_registro(registro)
    if res.exigir(
        len(blocos) == len(LABELS),
        f"o registro do JEMS3 nao traz os sete blocos do resumo ({len(blocos)} lidos)",
    ):
        corpo = re.sub(r"\\textbf\{[^}]*\}", " ", abstract.group(1))
        corpo = re.sub(r"\\&", "&", corpo)
        for label, bloco in blocos.items():
            res.exigir(
                _compacta(bloco) in _compacta(corpo),
                f"o bloco {label!r} do abstract diverge do texto congelado no JEMS3; "
                "o registro nao pode mais ser alterado depois de 14/09/2026",
            )

    palavras = len(re.sub(r"\\[a-zA-Z]+\{?|\}", " ", abstract.group(1)).split())
    res.exigir(
        palavras <= 340,
        f"o abstract tem {palavras} palavras contando os sete labels; o limite da chamada e' 300 "
        "para o resumo",
    )
    res.exigir(
        "Keywords" in abstract.group(1),
        "as palavras-chave em ingles nao estao no frontmatter do PDF",
    )
    res.exigir(
        "Palavras-chave" in resumo.group(1),
        "as palavras-chave em portugues nao estao no resumo",
    )
    # O resumo em portugues espelha os sete blocos, com os labels traduzidos.
    res.exigir(
        len(re.findall(r"\\textbf\{[^}]*\}", resumo.group(1))) >= len(LABELS) + 1,
        "o resumo em portugues nao espelha os sete labels do resumo estruturado",
    )


def verificar_estrutura(diretorio: Path, texto_pdf: str, res: Resultado) -> None:
    tex = _ler(diretorio / "artigo.tex")
    ativo = "\n".join(l for l in tex.splitlines() if not l.lstrip().startswith("%"))
    no_tex = re.findall(r"(?m)^\\section\{([^}]*)\}", ativo)
    res.exigir(
        tuple(no_tex) == SECOES,
        f"as secoes do artigo divergem do esqueleto: {no_tex}",
    )

    posicao = -1
    for i, nome in enumerate(SECOES, start=1):
        cabecalho = f"{i}. {nome}"
        onde = texto_pdf.find(cabecalho)
        res.exigir(onde >= 0, f"a secao {cabecalho!r} nao aparece no PDF renderizado")
        if onde >= 0:
            res.exigir(
                onde > posicao,
                f"a secao {cabecalho!r} sai fora de ordem no PDF",
            )
            posicao = max(posicao, onde)

    esqueleto = _ler(diretorio / "esqueleto.md")
    for label in LABELS:
        linhas = [
            l for l in esqueleto.splitlines() if l.strip().startswith("|") and label in l
        ]
        res.exigir(
            bool(linhas),
            f"nenhuma secao do esqueleto carrega o label {label!r}: resumo e corpo sem coesao",
        )

    res.exigir(
        "Declaração de Uso de IA Generativa" in texto_pdf,
        "a declaracao de uso de IA generativa nao aparece no PDF",
    )


# --------------------------------------------------------------------------
# 6. apendice A
# --------------------------------------------------------------------------


def verificar_apendice(diretorio: Path, texto_pdf: str, res: Resultado) -> None:
    apendice = _ler(diretorio / "apendice-sparql.tex")
    if not res.exigir(bool(apendice), "o Apendice A nao existe"):
        return
    res.exigir(
        "Apêndice A" in texto_pdf,
        "o Apendice A nao aparece no PDF renderizado",
    )

    inteiro = re.search(r"\\begin\{Verbatim\}[^\n]*\n(.*?)\\end\{Verbatim\}", apendice, re.DOTALL)
    remissao = "depósito" in apendice or "deposito" in apendice
    res.exigir(
        inteiro is not None or remissao,
        "o Apendice A nao traz as consultas nem remete explicitamente ao deposito",
    )

    if inteiro is not None:
        mostrada = inteiro.group(1)
        casou = False
        for qc in QCS:
            bruto = _ler(CONSULTAS / f"{qc}.rq")
            corpo = "\n".join(
                l for l in bruto.split("\n") if not l.startswith("#")
            ).strip("\n")
            if corpo and _compacta(corpo) == _compacta(mostrada.strip("\n")):
                casou = True
        res.exigir(
            casou,
            "a consulta impressa no Apendice A nao e' nenhum dos .rq gravados: "
            "o apendice transcreve em vez de reproduzir",
        )

    if remissao:
        for qc in QCS:
            resultado = CONSULTAS / f"{qc}-resultado.csv"
            res.exigir(
                resultado.exists(),
                f"o Apendice A remete ao deposito, mas {resultado} nao existe",
            )
        # Contar registros de CSV, e nao linhas fisicas: um campo entre aspas
        # pode conter quebra de linha, e as duas contagens divergiriam para um
        # resultado perfeitamente valido.
        linhas = []
        for qc in QCS:
            with (CONSULTAS / f"{qc}-resultado.csv").open(encoding="utf-8", newline="") as f:
                linhas.append(max(sum(1 for _ in csv.reader(f)) - 1, 0))
        for qc, n in zip(QCS, linhas):
            res.exigir(
                f"{qc.upper()} ({n})" in apendice,
                f"o Apendice A nao declara as {n} linhas de {qc.upper()}, ou declara outro numero "
                "que o .csv nao sustenta",
            )
        res.exigir(
            "reexecutar-consultas.py" in apendice,
            "a remissao ao deposito nao nomeia o script que reexecuta as consultas",
        )


# --------------------------------------------------------------------------
# 7. paginacao
# --------------------------------------------------------------------------


def verificar_paginacao(saida: dict, res: Resultado) -> None:
    paginas = saida.get("paginas")
    if not res.exigir(paginas is not None, "nao foi possivel contar as paginas do PDF"):
        return
    print(f"paginas do PDF: {paginas} (a chamada exige de {PAGINAS_MIN} a {PAGINAS_MAX})")
    res.exigir(
        PAGINAS_MIN <= paginas <= PAGINAS_MAX,
        f"o PDF tem {paginas} paginas e a chamada rejeita sumariamente fora de "
        f"{PAGINAS_MIN}-{PAGINAS_MAX}",
    )


def main() -> int:
    diretorio = Path(sys.argv[1]) if len(sys.argv) > 1 else ARTIGO_PADRAO
    res = Resultado()

    if not res.exigir((diretorio / "artigo.tex").exists(), f"{diretorio}/artigo.tex ausente"):
        print(f"FALHOU: {res.falhas[-1]}")
        return 1

    saida = compilar(diretorio)
    if saida is None:
        print(
            "FALHOU: falta pdflatex, bibtex, pdftotext ou pdfinfo; o ticket 13 nao pode "
            "ser conferido"
        )
        return 1

    verificar_preambulo(diretorio, res)
    verificar_compilacao(saida, res)
    texto_pdf = saida.get("texto", "")
    if saida.get("pdf"):
        verificar_acentos(texto_pdf, res)
        verificar_fidelidade(diretorio, texto_pdf, res)
        verificar_bibliografia(diretorio, saida, res)
        verificar_frontmatter(diretorio, texto_pdf, res)
        verificar_estrutura(diretorio, texto_pdf, res)
        verificar_apendice(diretorio, texto_pdf, res)
        verificar_paginacao(saida, res)
    verificar_figuras(diretorio, res)
    verificar_ausencia_do_modelo_antigo(diretorio, res)

    print(f"verificacoes: {res.checagens}")
    if res.falhas:
        print(f"FALHOU: {len(res.falhas)} problema(s)")
        for falha in res.falhas:
            if falha:
                print(f"  - {falha}")
        return 1
    print("OK: a checklist do ticket 13 esta cumprida")
    return 0


if __name__ == "__main__":
    sys.exit(main())
