"""
Divide um CSV grande em pedacos menores para copiar/colar manualmente
(uso: quando nao ha USB/e-mail/nuvem disponivel para transferir o arquivo).

Como usar:
1. Ajuste ARQUIVO_ENTRADA para o nome do CSV exportado do Excel (Salvar Como > CSV UTF-8).
2. Rode: python dividir_csv.py
3. Serao gerados arquivos bloco_01.csv, bloco_02.csv, ... na mesma pasta,
   cada um com cabecalho repetido + ate LINHAS_POR_BLOCO linhas de dados.
4. Abra cada bloco_XX.csv no Bloco de Notas, selecione tudo (Ctrl+A),
   copie (Ctrl+C) e cole no chat, avisando "bloco X de N".
"""
import csv

ARQUIVO_ENTRADA = "reservas.csv"   # <-- troque para o nome real do seu arquivo
LINHAS_POR_BLOCO = 15000

with open(ARQUIVO_ENTRADA, "r", encoding="utf-8-sig", newline="") as f:
    leitor = csv.reader(f)
    cabecalho = next(leitor)
    linhas = list(leitor)

total = len(linhas)
num_blocos = (total + LINHAS_POR_BLOCO - 1) // LINHAS_POR_BLOCO

for i in range(num_blocos):
    inicio = i * LINHAS_POR_BLOCO
    fim = inicio + LINHAS_POR_BLOCO
    pedaco = linhas[inicio:fim]

    nome_saida = f"bloco_{i+1:02d}.csv"
    with open(nome_saida, "w", encoding="utf-8", newline="") as f:
        escritor = csv.writer(f)
        escritor.writerow(cabecalho)
        escritor.writerows(pedaco)

    print(f"{nome_saida}: {len(pedaco)} linhas")

print(f"\nTotal: {total} linhas em {num_blocos} blocos.")
