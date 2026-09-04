# gUFO, como distribuída

Insumo externo, obtido e **não editado**, como todo o resto de `sources/`.

| | |
|---|---|
| IRI | `http://purl.org/nemo/gufo` |
| Resolve para | `https://nemo-ufes.github.io/gufo/gufo.ttl` |
| Versão | 1.0.0 (`owl:versionInfo`), `dct:modified` 2021-11-01 |
| Obtida em | 2026-09-04 |
| SHA-256 | `1226e62867ee4b42bbcd0b8d8304fc83b0af6749339bd96e0e68cbb4acef1852` |

## Por que uma cópia local

A OWL da OntoMPO declara `owl:imports gufo:`, e a verificação de consistência por raciocinador
(`tools/verification/raciocinador.py`) só tem o que verificar se a ontologia de fundamentação
estiver carregada junto: é dela que vêm as disjunções que dão dentes à adoção de UFO-B — sem
`gufo:Endurant` disjunto de `gufo:Event`, um indivíduo que fosse ao mesmo tempo `Person` e
`Observation` passaria despercebido.

Dereferenciar o IRI a cada execução tornaria a verificação dependente de rede e do que estiver
publicado naquele dia. A cópia fixa o insumo, e o SHA-256 acima diz exatamente qual.

Confira com:

```sh
python -c "import hashlib,pathlib;print(hashlib.sha256(pathlib.Path('sources/gufo/gufo.ttl').read_bytes()).hexdigest())"
```
