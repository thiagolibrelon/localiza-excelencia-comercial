"""
Indexa as transcricoes brutas em resultados/exploracao_fable/inputs_completo/loteNNN.txt
por (base_origem, cliente_id, data) -> texto completo da ligacao.

Usado por gerar_arvore_h10.py para anexar a transcricao completa (nao so o resumo da IA)
aos exemplos de cada ramo.
"""
import re
import glob

HEADER_RE = re.compile(
    r"=== LIGACAO \| Base:(?P<base>[^|]+) \| Cliente:(?P<cliente>[^|]+) \| "
    r"Data:(?P<data>[^|]+) \| Dur:(?P<dur>[^s]+)s \| Sent:(?P<sent>[^=]+)==="
)


def construir_indice(pasta="resultados/exploracao_fable/inputs_completo"):
    indice = {}
    for path in sorted(glob.glob(f"{pasta}/lote*.txt")):
        with open(path, encoding="utf-8") as f:
            conteudo = f.read()
        matches = list(HEADER_RE.finditer(conteudo))
        for i, m in enumerate(matches):
            inicio = m.start()
            fim = matches[i + 1].start() if i + 1 < len(matches) else len(conteudo)
            bloco = conteudo[inicio:fim].strip()
            chave = (
                m.group("base").strip(),
                m.group("cliente").strip(),
                m.group("data").strip(),
                m.group("dur").strip(),
            )
            indice[chave] = bloco
    return indice


if __name__ == "__main__":
    idx = construir_indice()
    print(f"Ligacoes indexadas: {len(idx)}")
    # sanity check
    for k in list(idx.keys())[:3]:
        print(k)
