#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifica o deposito anonimo dos artefatos contra a checklist do ticket 09.

Uso: python tools/verification/verificar_deposito.py [diretorio-do-deposito]

Le o deposito como um terceiro faria — sem importar de `tools/generation/` —,
confere que ele contem o que a checklist do ticket 09 exige, que a copia esta em
dia com a fonte, e que nenhum arquivo revela autoria, instituicao, e-mail ou
usuario. Confere, na ordem da checklist:

  1. estrutura: `README.md`, `.zenodo.json`, `MANIFEST.sha256`, `ontology/` e a
     copia local da gUFO em `gufo/`;
  2. conteudo exigido:
     - a OWL revisada (`ontology/owl/ontompo.ttl` e `.owl`) e o modelo OntoUML em
       formato aberto (`.ontouml.json` das tres camadas);
     - o diff da transformacao gUFO (`ontology/owl/diff-gerado-customizado.*`);
     - as sete consultas SPARQL com resultado completo (`.rq`, `.csv` e `.md`);
     - os relatorios do plugin OntoUML e do OOPS! nas versoes antes e depois;
     - os dados de instancia dos dois observatorios;
  3. integridade: cada arquivo listado em `MANIFEST.sha256` existe e bate o
     digest, e todo arquivo do deposito (menos o proprio manifesto) esta listado;
  4. copia em dia: `ontology/` e byte a byte igual a `artifacts/ontology/`, e
     `gufo/gufo.ttl` igual a `sources/gufo/gufo.ttl`;
  5. anonimato: nenhum arquivo de texto traz nome, instituicao, cidade, e-mail,
     usuario, `github.com`, nem a marca de autoria "proprio autor"/"the author's
     own"/primeira pessoa; nenhum caminho absoluto com nome de usuario;
  6. `.zenodo.json`: JSON valido, `creators` sem nome real e sem `affiliation`,
     `access_right` aberto, licenca declarada;
  7. `README.md` orienta a reexecucao (o script, o `pip install`, as versoes das
     ferramentas, a licenca) e `reexecutar-consultas.py` compila e so depende de
     `rdflib` e da biblioteca padrao.

Sai com codigo 1 se qualquer verificacao falhar.
"""

from __future__ import annotations

import ast
import hashlib
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
DEPOSITO_PADRAO = RAIZ / "artifacts" / "deposit"
ONTOLOGIA_FONTE = RAIZ / "artifacts" / "ontology"
GUFO_FONTE = RAIZ / "sources" / "gufo" / "gufo.ttl"

DOI_FONTE_CENARIO = "10.5753/sbsi_estendido.2022.222995"

# Estrutura e conteudo exigidos pela checklist do ticket 09. Caminhos relativos
# a raiz do deposito.
ESTRUTURA = [
    "README.md",
    ".zenodo.json",
    "MANIFEST.sha256",
    "reexecutar-consultas.py",
    "gufo/gufo.ttl",
]

CONTEUDO_EXIGIDO = {
    "OWL revisada": [
        "ontology/owl/ontompo.ttl",
        "ontology/owl/ontompo.owl",
    ],
    "modelo OntoUML em formato aberto": [
        "ontology/baseline/ontompo-as-is.ontouml.json",
        "ontology/rodada-1/ontompo-rodada-1.ontouml.json",
        "ontology/rodada-2/ontompo-rodada-2.ontouml.json",
    ],
    "diff da transformacao gUFO": [
        "ontology/owl/diff-gerado-customizado.ttl",
        "ontology/owl/diff-gerado-customizado.md",
    ],
    "relatorios do plugin OntoUML, antes e depois": [
        "ontology/baseline/relatorio-plugin-ontouml.md",
        "ontology/baseline/relatorio-plugin-ontouml.json",
        "ontology/rodada-2/relatorio-plugin-ontouml.md",
        "ontology/rodada-2/relatorio-plugin-ontouml.json",
    ],
    "relatorios do OOPS!, antes e depois": [
        "ontology/baseline/relatorio-oops.md",
        "ontology/baseline/relatorio-oops.xml",
        "ontology/owl/relatorio-oops.md",
        "ontology/owl/relatorio-oops.xml",
        "ontology/owl/comparacao-oops.md",
    ],
    "dados de instancia dos dois observatorios": [
        "ontology/instancias/observatorio.ttl",
        "ontology/instancias/observatorio-b.ttl",
        "ontology/instancias/procedencia.md",
    ],
}

CONSULTAS = [f"qc{n}" for n in range(1, 8)]

# Termos que quebram a revisao duplamente anonima. Uniao dos conjuntos ja usados
# em verificar_instancia_qc.py e verificar_demais_qc.py, mais e-mail e ORCID
# genericos. Estes tres verificadores mantem cada um a sua copia da lista de
# propósito — nenhum importa do outro nem de tools/generation/ ("a duplicacao e o
# teste", CONTEXT.md); ao acrescentar um termo a redigir, acrescente nos tres.
IDENTIFICADORES = re.compile(
    r"pernambuco|garanhuns|quixad|recife|\bcear[aá]\b|\bUPE\b|\bUFC\b|\bUFPE\b|"
    r"op-?upe|kvojps|ivaldir|jeferson|jos[eé]\s+ferreira|santos\s+j[uú]nior|"
    r"ferreira\s+dos\s+santos|\bhermano\b|perrelli|\bmoura\b|cleyton|"
    r"\bvieira\b|universidade\s+(de|federal)|@upe\.br|@gmail|@hotmail|@outlook|"
    r"github\.com|gitlab\.com|bitbucket\.org|orcid\.org|"
    r"\b\d{4}-\d{4}-\d{4}-\d{3}[\dxX]\b",
    re.IGNORECASE,
)

# Marca de autoria: dizer que o cenario/ a dissertacao e "do proprio autor", ou
# primeira pessoa, liga a submissao anonima a um trabalho nominal.
MARCA_AUTORIA = re.compile(
    r"pr[oó]pri[oa]\s+autor|the\s+author'?s\s+own|our\s+(previous|earlier|prior)\s+work|"
    r"nossa\s+an[aá]lise|\bnoss[oa]s?\b|\b(meu|minha|meus|minhas)\b",
    re.IGNORECASE,
)

# Caminho absoluto com nome de usuario (Windows ou POSIX).
CAMINHO_USUARIO = re.compile(r"[A-Za-z]:\\Users\\|/home/[a-z][-a-z0-9_]*|/Users/[A-Za-z]")

# Primeira pessoa do plural pela desinencia -mos, aplicada so aos arquivos do
# cenario, como fazem os verificadores dos tickets 07 e 08 — fora deles o padrao
# acusaria "maximos", "legitimos" e afins.
PRIMEIRA_PESSOA_MOS = re.compile(r"\bn[aeií]mos\b|\b\w{3,}[aeií]mos\b", re.IGNORECASE)
PRIMEIRA_PESSOA_MOS_ESCOPO = ("ontology/instancias/", "ontology/consultas/")

EXTENSOES_TEXTO = {
    ".md", ".txt", ".ttl", ".owl", ".rq", ".json", ".xml", ".csv", ".py", ".sha256",
}
# "maximos"/"minimos"/"legitimos"/"otimos" e afins: 1a pessoa do plural so por
# acidente. Fora do escopo do cenario, sao ruido.
FALSOS_MOS = re.compile(
    r"^(m[aá]xim|m[ií]nim|leg[ií]tim|[oó]tim|[ií]ntim|pr[oó]xim|anim|"
    r"organism|mecanism|abism)", re.IGNORECASE
)


class Resultado:
    def __init__(self) -> None:
        self.falhas: list[str] = []
        self.checagens = 0

    def exigir(self, condicao: object, mensagem: str) -> bool:
        self.checagens += 1
        if not condicao:
            self.falhas.append(mensagem)
        return bool(condicao)


def arquivos_do_deposito(raiz: Path) -> list[Path]:
    return sorted(p for p in raiz.rglob("*") if p.is_file())


def ler_texto(caminho: Path) -> str | None:
    try:
        return caminho.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None


def verificar_estrutura(dep: Path, res: Resultado) -> None:
    for rel in ESTRUTURA:
        res.exigir((dep / rel).is_file(), f"falta {rel}")
    res.exigir((dep / "ontology").is_dir(), "falta a arvore ontology/")


def verificar_conteudo(dep: Path, res: Resultado) -> None:
    for rotulo, caminhos in CONTEUDO_EXIGIDO.items():
        for rel in caminhos:
            alvo = dep / rel
            res.exigir(
                alvo.is_file() and alvo.stat().st_size > 0,
                f"{rotulo}: falta ou esta vazio {rel}",
            )
    for qc in CONSULTAS:
        for sufixo in (".rq", "-resultado.csv", "-resultado.md"):
            rel = f"ontology/consultas/{qc}{sufixo}"
            alvo = dep / rel
            res.exigir(
                alvo.is_file() and alvo.stat().st_size > 0,
                f"consultas SPARQL: falta ou esta vazio {rel}",
            )
    # resultado "completo, nao resumido": o .md tem de trazer a consulta verbatim
    # e ao menos uma linha de tabela alem do cabecalho.
    for qc in CONSULTAS:
        md = ler_texto(dep / f"ontology/consultas/{qc}-resultado.md") or ""
        res.exigir("```sparql" in md, f"{qc}-resultado.md nao traz a consulta verbatim")
        res.exigir(
            md.count("\n|") >= 3,
            f"{qc}-resultado.md nao traz a tabela de resultado completa",
        )


def verificar_manifesto(dep: Path, res: Resultado) -> None:
    manifesto = dep / "MANIFEST.sha256"
    texto = ler_texto(manifesto)
    if not res.exigir(texto, "MANIFEST.sha256 ausente ou ilegivel"):
        return

    listados: dict[str, str] = {}
    for linha in texto.splitlines():
        linha = linha.strip()
        if not linha:
            continue
        partes = linha.split("  ", 1)
        if not res.exigir(len(partes) == 2, f"linha malformada no manifesto: {linha!r}"):
            continue
        digest, rel = partes
        listados[rel] = digest

    presentes = {
        p.relative_to(dep).as_posix()
        for p in arquivos_do_deposito(dep)
        if p.name != "MANIFEST.sha256"
    }

    for rel in sorted(presentes - listados.keys()):
        res.exigir(False, f"arquivo do deposito fora do manifesto: {rel}")
    for rel in sorted(listados.keys() - presentes):
        res.exigir(False, f"manifesto lista arquivo inexistente: {rel}")

    for rel in sorted(listados.keys() & presentes):
        real = hashlib.sha256((dep / rel).read_bytes()).hexdigest()
        res.exigir(
            real == listados[rel],
            f"digest divergente para {rel}: manifesto {listados[rel][:12]}…, "
            f"arquivo {real[:12]}…",
        )


def verificar_copia_em_dia(dep: Path, res: Resultado) -> None:
    if not ONTOLOGIA_FONTE.is_dir():
        res.exigir(False, f"fonte {ONTOLOGIA_FONTE} nao encontrada para comparar")
        return

    fonte = {
        p.relative_to(ONTOLOGIA_FONTE).as_posix(): p
        for p in ONTOLOGIA_FONTE.rglob("*")
        if p.is_file()
    }
    copia = {
        p.relative_to(dep / "ontology").as_posix(): p
        for p in (dep / "ontology").rglob("*")
        if p.is_file()
    }
    for rel in sorted(set(fonte) - set(copia)):
        res.exigir(False, f"ontology/{rel} esta na fonte e falta no deposito — copia velha")
    for rel in sorted(set(copia) - set(fonte)):
        res.exigir(False, f"ontology/{rel} esta no deposito e nao na fonte — copia velha")
    for rel in sorted(set(fonte) & set(copia)):
        res.exigir(
            fonte[rel].read_bytes() == copia[rel].read_bytes(),
            f"ontology/{rel} diverge da fonte — regenere o deposito",
        )

    if GUFO_FONTE.is_file():
        res.exigir(
            GUFO_FONTE.read_bytes() == (dep / "gufo" / "gufo.ttl").read_bytes(),
            "gufo/gufo.ttl diverge de sources/gufo/gufo.ttl",
        )


def verificar_anonimato(dep: Path, res: Resultado) -> None:
    for caminho in arquivos_do_deposito(dep):
        rel = caminho.relative_to(dep).as_posix()
        if caminho.suffix.lower() not in EXTENSOES_TEXTO:
            continue
        texto = ler_texto(caminho)
        if texto is None:
            continue

        # `gufo/gufo.ttl` e a gUFO redistribuida verbatim: traz os nomes dos seus
        # proprios autores e o URL do seu repositorio, que nao dizem nada sobre
        # quem depositou. So ela escapa da lista de identificadores — a
        # integridade dela e garantida por verificar_copia_em_dia (byte a byte
        # contra sources/gufo/gufo.ttl) e pelo SHA-256 em gufo/README.md. Todo o
        # resto, `gufo/README.md` inclusive, passa pela varredura inteira.
        if rel != "gufo/gufo.ttl":
            achado = IDENTIFICADORES.search(texto)
            res.exigir(
                achado is None,
                f"{rel} traz mencao identificadora: «{achado.group(0) if achado else ''}»",
            )

        achado = MARCA_AUTORIA.search(texto)
        res.exigir(
            achado is None,
            f"{rel} traz marca de autoria/primeira pessoa: «{achado.group(0) if achado else ''}»",
        )

        achado = CAMINHO_USUARIO.search(texto)
        res.exigir(
            achado is None,
            f"{rel} traz caminho absoluto com usuario: «{achado.group(0) if achado else ''}»",
        )

        if rel.startswith(PRIMEIRA_PESSOA_MOS_ESCOPO):
            for m in PRIMEIRA_PESSOA_MOS.finditer(texto):
                if FALSOS_MOS.match(m.group(0)):
                    continue
                res.exigir(
                    False,
                    f"{rel} usa primeira pessoa do plural: «{m.group(0)}» — "
                    "o cenario vai em terceira pessoa",
                )
                break


def verificar_zenodo(dep: Path, res: Resultado) -> None:
    texto = ler_texto(dep / ".zenodo.json")
    if not res.exigir(texto, ".zenodo.json ausente ou ilegivel"):
        return
    try:
        meta = json.loads(texto)
    except json.JSONDecodeError as erro:
        res.exigir(False, f".zenodo.json nao e JSON valido: {erro}")
        return

    res.exigir(meta.get("title"), ".zenodo.json sem title")
    res.exigir(meta.get("description"), ".zenodo.json sem description")
    res.exigir(meta.get("license"), ".zenodo.json sem license")
    res.exigir(
        meta.get("access_right") == "open",
        ".zenodo.json: access_right nao e 'open'",
    )

    criadores = meta.get("creators")
    if res.exigir(
        isinstance(criadores, list) and criadores,
        ".zenodo.json sem creators",
    ):
        for c in criadores:
            nome = (c.get("name") or "").strip().lower()
            res.exigir(
                nome in {"anonymous", "anonymous author", "anonimo", "anônimo"},
                f".zenodo.json: creator identificavel «{c.get('name')}»",
            )
            res.exigir(
                not c.get("affiliation"),
                f".zenodo.json: creator com affiliation «{c.get('affiliation')}»",
            )
            res.exigir(
                not c.get("orcid"),
                ".zenodo.json: creator com orcid",
            )

    # o texto livre do .zenodo.json tambem passa pela varredura de anonimato em
    # verificar_anonimato; aqui so a estrutura.


def verificar_readme(dep: Path, res: Resultado) -> None:
    texto = ler_texto(dep / "README.md")
    if not res.exigir(texto, "README.md ausente ou ilegivel"):
        return
    for marca, msg in [
        ("reexecutar-consultas.py", "README nao aponta o script de reexecucao"),
        ("pip install", "README nao diz como instalar a dependencia"),
        ("rdflib", "README nao nomeia a dependencia rdflib"),
        ("ontouml-js", "README nao registra as ferramentas usadas"),
        ("creativecommons.org/licenses/by/4.0", "README nao declara a licenca CC BY 4.0"),
        ("terceira pessoa", "README nao registra que a fonte externa vai em terceira pessoa"),
        (DOI_FONTE_CENARIO, "README nao cita o DOI da publicacao-fonte do cenario"),
    ]:
        res.exigir(marca in texto, msg)
    # A tabela de ferramentas tem de trazer numero de versao — sem pinar o valor
    # exato aqui, que ja mora no README e em tools/package.json.
    res.exigir(
        re.search(r"\bontouml-js\b.*?\b\d+\.\d+\.\d+\b", texto, re.DOTALL) is not None,
        "README nao fixa a versao da ontouml-js na tabela de ferramentas",
    )


def verificar_reexecutar(dep: Path, res: Resultado) -> None:
    caminho = dep / "reexecutar-consultas.py"
    texto = ler_texto(caminho)
    if not res.exigir(texto, "reexecutar-consultas.py ausente ou ilegivel"):
        return
    try:
        arvore = ast.parse(texto)
    except SyntaxError as erro:
        res.exigir(False, f"reexecutar-consultas.py nao compila: {erro}")
        return

    importados: set[str] = set()
    for no in ast.walk(arvore):
        if isinstance(no, ast.Import):
            importados.update(a.name.split(".")[0] for a in no.names)
        elif isinstance(no, ast.ImportFrom) and no.module:
            importados.add(no.module.split(".")[0])

    permitidos = {
        "rdflib", "csv", "sys", "pathlib", "__future__",
    }
    estranhos = importados - permitidos
    res.exigir(
        not estranhos,
        f"reexecutar-consultas.py importa alem de rdflib e da stdlib: {sorted(estranhos)}",
    )
    res.exigir(
        "rdflib" in importados,
        "reexecutar-consultas.py nao usa rdflib — nao reexecuta as consultas",
    )


def verificar(dep: Path) -> list[str]:
    res = Resultado()
    if not dep.is_dir():
        return [f"deposito nao encontrado em {dep} — rode tools/generation/gerar_deposito.py"]

    verificar_estrutura(dep, res)
    verificar_conteudo(dep, res)
    verificar_manifesto(dep, res)
    verificar_copia_em_dia(dep, res)
    verificar_anonimato(dep, res)
    verificar_zenodo(dep, res)
    verificar_readme(dep, res)
    verificar_reexecutar(dep, res)

    print(f"verificacoes: {res.checagens}")
    return res.falhas


def main() -> int:
    dep = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEPOSITO_PADRAO
    falhas = verificar(dep)
    if falhas:
        print(f"FALHOU ({len(falhas)}):")
        for f in falhas:
            print(f"  - {f}")
        return 1
    print("OK: o deposito cumpre a checklist do ticket 09")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
