"""
Gera para_gpt.txt com as transcricoes formatadas para colar no ChatGPT.
Execute: python gerar_para_gpt.py
"""

import json
import glob
import os
from datetime import datetime

# Pasta com os arquivos de cliente
PASTA = r"C:\Users\quase\Documents\Ligacoes"
SAIDA = os.path.join(PASTA, "para_gpt.txt")

# Limite de ligacoes por arquivo (None = todas)
LIMITE_LIGACOES = None

# Colapsar turns consecutivos do mesmo speaker (reduz tokens ~40%)
COLAPSAR_TURNS = True


def colapsar_conversa(conversa):
    """Junta falas consecutivas do mesmo speaker."""
    if not conversa:
        return []
    result = []
    speaker_atual, texto_atual = conversa[0]
    for speaker, texto in conversa[1:]:
        if speaker == speaker_atual:
            texto_atual = texto_atual.rstrip() + " " + texto.strip()
        else:
            result.append((speaker_atual, texto_atual.strip()))
            speaker_atual, texto_atual = speaker, texto
    result.append((speaker_atual, texto_atual.strip()))
    return result


def formatar_ligacao(lig, numero):
    """Formata uma ligacao para texto legivel."""
    data = lig.get("data", "")
    try:
        dt = datetime.fromisoformat(data.replace("Z", "+00:00"))
        data_fmt = dt.strftime("%d/%m/%Y %H:%M")
    except Exception:
        data_fmt = data

    duracao = lig.get("duracao", 0)
    sentimento = lig.get("sentimento", "")
    conversa = lig.get("conversa", [])

    if COLAPSAR_TURNS:
        conversa = colapsar_conversa(conversa)

    # Remover turns muito curtos (ruido do STT)
    conversa = [(s, t) for s, t in conversa if len(t.strip()) > 2]

    linhas = [
        f"--- LIGACAO {numero} ---",
        f"DATA: {data_fmt}",
        f"DURACAO: {duracao}s",
        f"SENTIMENTO: {sentimento}",
        "",
        "CONVERSA:",
    ]

    for speaker, texto in conversa:
        nome = "VENDEDOR" if speaker == "A" else "CLIENTE"
        linhas.append(f"{nome}: {texto}")

    linhas.append("")
    return "\n".join(linhas)


def processar_arquivo(caminho):
    """Le um arquivo JSON e retorna o bloco formatado."""
    with open(caminho, encoding="utf-8") as f:
        dados = json.load(f)

    if not dados:
        return ""

    cliente_id = dados[0].get("cliente", os.path.basename(caminho))

    ligacoes = dados
    if LIMITE_LIGACOES:
        ligacoes = dados[:LIMITE_LIGACOES]

    blocos = [
        "=" * 60,
        f"CLIENTE: {cliente_id}",
        f"TOTAL DE LIGACOES: {len(dados)}",
        "",
    ]

    for i, lig in enumerate(ligacoes, 1):
        blocos.append(formatar_ligacao(lig, i))

    return "\n".join(blocos)


def main():
    # Pega todos os arquivos cliente_*.json
    padrao = os.path.join(PASTA, "cliente_*.json")
    arquivos = sorted(glob.glob(padrao))

    if not arquivos:
        print(f"Nenhum arquivo encontrado em: {PASTA}")
        print("Execute primeiro o Descompac.py para gerar os arquivos por cliente.")
        return

    print(f"Encontrados {len(arquivos)} arquivos de clientes.")

    blocos_totais = []
    total_ligacoes = 0

    for arq in arquivos:
        try:
            bloco = processar_arquivo(arq)
            if bloco:
                blocos_totais.append(bloco)
                with open(arq, encoding="utf-8") as f:
                    dados = json.load(f)
                n = min(len(dados), LIMITE_LIGACOES) if LIMITE_LIGACOES else len(dados)
                total_ligacoes += n
                print(f"  OK: {os.path.basename(arq)} ({n} ligacoes)")
        except Exception as e:
            print(f"  ERRO em {os.path.basename(arq)}: {e}")

    conteudo = "\n\n".join(blocos_totais)

    with open(SAIDA, "w", encoding="utf-8") as f:
        f.write(conteudo)

    tamanho_kb = os.path.getsize(SAIDA) / 1024
    print(f"\nArquivo gerado: {SAIDA}")
    print(f"Total de ligacoes: {total_ligacoes}")
    print(f"Tamanho: {tamanho_kb:.1f} KB")
    print("\nCole o conteudo de para_gpt.txt no ChatGPT junto com o prompt de analise.")

    # Aviso se passar de ~100KB
    if tamanho_kb > 100:
        print(f"\nAVISO: arquivo grande ({tamanho_kb:.0f} KB).")
        print("Se o ChatGPT travar, ajuste LIMITE_LIGACOES = 5 no topo do script")
        print("para processar menos ligacoes por vez, ou rode um cliente por vez.")


if __name__ == "__main__":
    main()
