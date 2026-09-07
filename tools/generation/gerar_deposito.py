#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Monta o deposito anonimo dos artefatos para o Zenodo (ticket 09).

Uso: python tools/generation/gerar_deposito.py [diretorio-de-saida]

O deposito e uma copia autocontida do que a pesquisa produziu, montada para que
um revisor a abra numa janela anonima, sem sessao autenticada, e reexecute as
consultas. O script nao escreve conteudo de pesquisa: ele copia `artifacts/ontology/`
tal como esta e a copia local da gUFO de `sources/gufo/`, e acrescenta so os
arquivos de empacotamento (README, `.zenodo.json`, `MANIFEST.sha256` e o
`reexecutar-consultas.py`, este ultimo vindo de `tools/generation/deposito/`).
Se algo na arvore de ontologia precisa mudar, muda-se la — na fonte do artefato,
gerada ou nao — e regenera-se o deposito.

O que entra:

  - `ontology/`   a arvore inteira de `artifacts/ontology/` — a OWL revisada e
    customizada e o modelo OntoUML em formato aberto (`.ontouml.json`), o diff da
    transformacao gUFO (`owl/diff-gerado-customizado.*`), as sete consultas
    SPARQL com resultado completo (`consultas/`), os relatorios do plugin
    OntoUML e do OOPS! nas versoes antes e depois (`baseline/`, `rodada-2/`,
    `owl/`), e os dados de instancia dos dois observatorios (`instancias/`);
  - `gufo/`       a gUFO 1.0.0 como distribuida, que a OWL importa, para que a
    reexecucao nao dependa de rede;
  - `README.md`   orientacao para quem chega do artigo, sem contexto do
    repositorio, e o passo a passo da reexecucao;
  - `reexecutar-consultas.py`  reexecuta as sete QCs sobre os arquivos deste
    deposito e confere cada resultado contra o `.csv` gravado — so precisa de
    `rdflib`;
  - `.zenodo.json`  os metadados do deposito, sem autoria;
  - `MANIFEST.sha256`  o SHA-256 de cada arquivo, para conferir a integridade.

Anonimato: a arvore de `artifacts/ontology/` ja e redigida em terceira pessoa,
com IRIs de exemplo e sem nome, instituicao, e-mail ou usuario. Este script nao
"limpa" nada — se algo identificador entrar, e `tools/verification/verificar_deposito.py`
que reprova. Corrija a fonte, nao o deposito.
"""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
ONTOLOGIA = RAIZ / "artifacts" / "ontology"
GUFO = RAIZ / "sources" / "gufo"
SAIDA_PADRAO = RAIZ / "artifacts" / "deposit"

LICENCA = "cc-by-4.0"
DOI_FONTE_CENARIO = "10.5753/sbsi_estendido.2022.222995"

TEMPLATE_REEXECUTAR = (
    Path(__file__).resolve().parent / "deposito" / "reexecutar-consultas.py"
)


def _readme(arvore: list[str]) -> str:
    lista = "```\n" + "\n".join(arvore) + "\n```"
    return f"""\
# OntoMPO — artefatos da analise ontologica do Modelo para Observatorios de Projetos

Deposito de ciencia aberta que acompanha o artigo *OntoMPO: Ontological Analysis
and Refinement of the Model for Project Observatories*. Reune o que a pesquisa
produziu: o modelo conceitual revisado, a ontologia OWL, as verificacoes
automaticas antes e depois da revisao, e a avaliacao funcional por questoes de
competencia em SPARQL sobre um cenario instanciado.

O artigo esta em revisao duplamente anonima. Os artefatos da OntoMPO — tudo em
`ontology/` — sao anonimos por requisito: nao trazem nome, instituicao, e-mail
nem usuario de quem depositou, os IRIs sao de um dominio de exemplo
(`https://example.org/ontompo/...`) e toda fonte externa e citada em terceira
pessoa pelo seu identificador. A unica excecao e `gufo/`, que e a gUFO
redistribuida como obtida: ela traz os nomes dos **seus proprios** autores e o
endereco do **seu** repositorio, que identificam o projeto gUFO, nao quem fez
este deposito.

Alguns arquivos copiados para `ontology/` e `gufo/README.md` citam caminhos
relativos ao repositorio de origem (`tools/...`, `sources/gufo/...`). Fora do
repositorio esses caminhos nao resolvem — o ponto de entrada autocontido e o
`reexecutar-consultas.py` na raiz deste deposito.

## O que tem aqui

{lista}

## Por onde comecar

1. `ontology/evidencias-A1-A9.md` — as nove deficiencias representacionais que a
   analise expos na formalizacao publicada, cada uma com classificacao pela
   Representation Theory (Wand & Weber), rastro ate o modelo de referencia e
   correcao.
2. `ontology/correcoes-rodada-1.md` e `ontology/correcoes-rodada-2.md` — o par
   antes/depois de cada correcao, com a justificativa fundamentada na UFO. A
   rodada 1 corrige A1–A4, A8 e A9; a rodada 2 adota UFO-B e UFO-C e corrige
   A5–A7.
3. `ontology/owl/customizacoes.md` — as cinco customizacoes aplicadas por cima
   da transformacao gUFO, e `ontology/owl/diff-gerado-customizado.ttl`, o
   conjunto exato de triplas acrescentadas.
4. `ontology/README.md` — o mapa completo dos artefatos e o que mede o
   antes/depois.

## As verificacoes, antes e depois

| Instrumento | Antes (baseline) | Depois (revisado) |
|---|---|---|
| Plugin OntoUML | `ontology/baseline/relatorio-plugin-ontouml.md` | `ontology/rodada-2/relatorio-plugin-ontouml.md` |
| Verificadores estruturais UFO | `ontology/rodada-1/relatorio-verificador-extra.md` | `ontology/rodada-2/relatorio-verificador-ufo-b-c.md` |
| OOPS! | `ontology/baseline/relatorio-oops.md` | `ontology/owl/relatorio-oops.md` |
| Comparacao OOPS! consolidada | — | `ontology/owl/comparacao-oops.md` |
| Raciocinador (consistencia) | — | `ontology/owl/relatorio-raciocinador.md` |

## Reexecutar as sete consultas SPARQL

As consultas estao em `ontology/consultas/qc1.rq` .. `qc7.rq`; o resultado
completo, cru, esta ao lado em `qcN-resultado.csv`, e a pergunta com a tabela em
`qcN-resultado.md`.

Para reexecutar numa maquina sem sessao autenticada e sem nada deste
repositorio, so com Python:

```sh
python -m venv .venv && . .venv/bin/activate      # ou .venv\\Scripts\\activate no Windows
pip install "rdflib>=7,<8"
python reexecutar-consultas.py
```

O script carrega, num unico grafo, a OWL revisada (`ontology/owl/ontompo.ttl`),
a gUFO local (`gufo/gufo.ttl`, que a OWL importa) e os dados de instancia dos
dois observatorios, roda cada consulta e confere o resultado, linha a linha,
contra o `.csv` gravado. As consultas andam so sobre triplas afirmadas — sem
raciocinador.

Onde o resultado obtido diverge do esperado — inclusive onde a divergencia
favorece o modelo revisado — esta registrado em
`ontology/consultas/divergencias.md`.

## O cenario de instancia

`ontology/instancias/observatorio.ttl` deriva de uma publicacao de terceiros nos
Anais Estendidos do XVIII SBSI (2022), DOI {DOI_FONTE_CENARIO}, referida em
terceira pessoa; o mapa trecho-da-publicacao -> individuo esta em
`ontology/instancias/procedencia.md`. `observatorio-b.ttl` e um segundo
observatorio, sintetico, construido apenas para a QC7 comparar a cobertura
conceitual de duas iniciativas.

## Ferramentas e versoes

| Ferramenta | Versao | Papel |
|---|---|---|
| `ontouml-js` | 0.5.0 | construcao do modelo, verificacao e transformacao `Ontouml2Gufo` |
| OOPS! | servico REST em `oops.linkeddata.es/rest` | pitfalls de OWL |
| `rdflib` | 7.x | Turtle -> RDF/XML, customizacao da OWL e execucao das consultas |
| `owlrl` | 7.x | raciocinador, perfil OWL 2 RL |
| gUFO | 1.0.0 (`gufo/`, SHA-256 em `gufo/README.md`) | ontologia de fundamentacao importada pela OWL |

## Licenca

Os artefatos da OntoMPO estao sob **Creative Commons Attribution 4.0**
(`https://creativecommons.org/licenses/by/4.0/`). A gUFO em `gufo/` e
redistribuida como obtida; sua licenca e a do projeto gUFO.
"""


def listar_arquivos(base: Path) -> list[Path]:
    return sorted(p for p in base.rglob("*") if p.is_file())


def escrever(caminho: Path, texto: str) -> None:
    caminho.write_text(texto, encoding="utf-8", newline="\n")


def main() -> int:
    saida = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else SAIDA_PADRAO

    for exigido in (ONTOLOGIA, GUFO / "gufo.ttl", GUFO / "README.md"):
        if not exigido.exists():
            print(f"FALTA: {exigido} — gere os artefatos antes (ver artifacts/ontology/README.md)")
            return 1

    if saida.exists():
        shutil.rmtree(saida)
    saida.mkdir(parents=True)

    shutil.copytree(ONTOLOGIA, saida / "ontology")
    (saida / "gufo").mkdir()
    shutil.copy2(GUFO / "gufo.ttl", saida / "gufo" / "gufo.ttl")
    shutil.copy2(GUFO / "README.md", saida / "gufo" / "README.md")

    escrever(
        saida / "reexecutar-consultas.py",
        TEMPLATE_REEXECUTAR.read_text(encoding="utf-8"),
    )

    zenodo = {
        "title": "OntoMPO: artifacts of the ontological analysis and refinement "
                 "of the Model for Project Observatories",
        "upload_type": "dataset",
        "description": (
            "Open-science deposit accompanying a double-blind submission. Contains the "
            "revised OntoUML conceptual model in an open format, the OWL ontology produced "
            "by the gUFO transformation plus its additive customization and the diff between "
            "them, the OntoUML-plugin and OOPS! verification reports before and after the "
            "revision, the seven SPARQL competency questions with complete results, and the "
            "instance data of two observatories. Anonymous by requirement: no author, "
            "affiliation, e-mail or handle; example-domain IRIs; external sources cited in "
            "the third person."
        ),
        "access_right": "open",
        "license": LICENCA,
        "creators": [{"name": "Anonymous"}],
        "keywords": [
            "project observatory",
            "ontological analysis",
            "Unified Foundational Ontology",
            "Representation Theory",
            "conceptual modeling",
            "OntoUML",
            "OWL",
            "competency questions",
            "Design Science Research",
        ],
        "related_identifiers": [
            {
                "identifier": f"https://doi.org/{DOI_FONTE_CENARIO}",
                "relation": "references",
                "scheme": "doi",
                "resource_type": "publication-conferencepaper",
            }
        ],
        "notes": (
            "The instance scenario in ontology/instancias/observatorio.ttl derives from the "
            "publication with DOI " + DOI_FONTE_CENARIO + ", cited in the third person. "
            "gUFO under gufo/ is redistributed as obtained."
        ),
    }
    escrever(saida / ".zenodo.json", json.dumps(zenodo, ensure_ascii=False, indent=2) + "\n")

    escrever(saida / "README.md", _readme(_arvore_resumida(saida)))

    manifesto = []
    for p in listar_arquivos(saida):
        rel = p.relative_to(saida).as_posix()
        if rel == "MANIFEST.sha256":
            continue
        digest = hashlib.sha256(p.read_bytes()).hexdigest()
        manifesto.append(f"{digest}  {rel}")
    escrever(saida / "MANIFEST.sha256", "\n".join(manifesto) + "\n")

    n = len(manifesto)
    print(f"deposito montado em {saida}")
    print(f"{n} arquivos, MANIFEST.sha256 gravado")
    print("confira com: python tools/verification/verificar_deposito.py")
    return 0


GLOSSA_TOPO = {
    "ontology": "a arvore de artefatos da pesquisa",
    "gufo": "gUFO 1.0.0 como distribuida (gufo.ttl, README.md)",
    "reexecutar-consultas.py": "reexecuta as sete QCs e confere contra o .csv gravado",
    "README.md": "este arquivo",
    ".zenodo.json": "metadados do deposito, sem autoria",
    "MANIFEST.sha256": "SHA-256 de cada arquivo do deposito",
}


def _arvore_resumida(saida: Path) -> list[str]:
    """Visao curta da arvore para o README, derivada do que ja esta em disco mais
    os dois arquivos de empacotamento que ainda serao escritos (README.md e
    MANIFEST.sha256)."""
    nomes = {p.name for p in saida.iterdir()} | {"README.md", "MANIFEST.sha256"}
    entradas = []
    for nome in sorted(nomes):
        alvo = saida / nome
        rotulo = GLOSSA_TOPO.get(nome, "")
        if alvo.is_dir():
            n = sum(1 for x in alvo.rglob("*") if x.is_file())
            entradas.append((f"{nome}/", f"{rotulo} ({n} arquivos)"))
        else:
            entradas.append((nome, rotulo))
    larg = max(len(e[0]) for e in entradas)
    return ["deposit/"] + [f"  {nome:<{larg}}  {rotulo}" for nome, rotulo in entradas]


if __name__ == "__main__":
    raise SystemExit(main())
