"""
Gera a arvore de decisao H10 (upsell B5 + qualidade do Challenger + fechamento/abertura P9)
a partir do CONSOLIDADO_LIGACOES.csv (100% da base, P1+P2+P5+P6+P9+P10).

Saidas em "Analise RMR-H10/":
  - dados_arvore_H10.csv      -> base anotada com a coluna 'ramo' (e 'sub_ramo' quando aplicavel)
  - arvore_decisao_H10.md     -> a arvore em texto + tabela + leitura
  - exemplos_por_ramo.md      -> pelo menos 5 exemplos reais de cada ramo
"""
import pandas as pd
from indexar_transcricoes import construir_indice

CSV_IN = "resultados/consolidado/CONSOLIDADO_LIGACOES.csv"
OUT_DIR = "Analise RMR-H10"

print("Indexando transcricoes brutas...")
INDICE_TRANSCRICOES = construir_indice()
print(f"{len(INDICE_TRANSCRICOES)} transcricoes indexadas.\n")

FECHOU = ["fechou_novo", "fechou_upsell", "fechou_renovacao"]

df = pd.read_csv(CSV_IN, dtype={"cliente_id": str})
df["fechou"] = df["p1_desfecho"].isin(FECHOU)
df["b5"] = df["p1_B5"] == "SIM"
df["op6"] = df["p6_oportunidades_perdidas"].astype(str).str.contains("OP6", na=False)


def ramo_principal(row):
    if pd.isna(row["p1_B5"]):
        return "0_sem_dado_B5"
    if row["b5"]:
        if row["p5_qualidade"] == "alta":
            return "6_B5sim_ChallengerAlta"
        else:
            return "7_B5sim_ChallengerFraco_ruido"
    else:
        q = row["p5_qualidade"]
        if q == "alta":
            return "1_B5nao_ChallengerAlta"
        elif q == "media":
            return "2_B5nao_ChallengerMedia"
        elif q == "baixa":
            return "3_B5nao_ChallengerBaixa"
        else:
            if row["op6"]:
                return "4_B5nao_SemChallenger_comOP6"
            else:
                return "5_B5nao_SemChallenger_semOP6"


df["ramo"] = df.apply(ramo_principal, axis=1)


def sub_ramo_fechamento(row):
    if row["ramo"] != "6_B5sim_ChallengerAlta":
        return ""
    if row["p9_tipo_fechamento"] == "FC1":
        return "FC1_com_data"
    if row["p9_tipo_fechamento"] == "FC3":
        return "FC3_qualquer_coisa"
    return ""


def sub_ramo_abertura(row):
    if row["ramo"] != "6_B5sim_ChallengerAlta":
        return ""
    if row["p9_tipo_abertura"] == "AB1":
        return "AB1_relacional"
    if row["p9_tipo_abertura"] == "AB4":
        return "AB4_reativa"
    return ""


df["sub_ramo_fechamento"] = df.apply(sub_ramo_fechamento, axis=1)
df["sub_ramo_abertura"] = df.apply(sub_ramo_abertura, axis=1)

# ---------- 1) CSV anotado ----------
cols_export = [
    "segment_id", "base_origem", "cliente_id", "data", "duracao_s", "sentimento",
    "p1_desfecho", "fechou", "p1_intencao_entrada", "p1_tentativa_comercial",
    "p1_B5", "p1_score_comercial",
    "p2_tipo", "p2_subtipo", "p2_quem_iniciou",
    "p5_teve_challenger", "p5_codigos_challenger", "p5_qualidade", "p5_frase_resumo", "p5_resultado_imediato",
    "p6_oportunidades_perdidas", "p6_descricao_curta", "p6_valor_potencial_reais",
    "p9_tipo_abertura", "p9_tipo_fechamento", "p9_proximo_passo_claro", "p9_prazo_definido",
    "ramo", "sub_ramo_fechamento", "sub_ramo_abertura",
]
df[cols_export].to_csv(f"{OUT_DIR}/dados_arvore_H10.csv", index=False, encoding="utf-8-sig")

# ---------- 2) resumo por ramo (pra conferir os numeros do MD) ----------
resumo = df.groupby("ramo").agg(n=("fechou", "size"), fechou=("fechou", "sum"))
resumo["taxa_pct"] = (100 * resumo["fechou"] / resumo["n"]).round(1)
resumo = resumo.sort_index()
print(resumo)

top = df[df["ramo"] == "6_B5sim_ChallengerAlta"]
for col in ["sub_ramo_fechamento", "sub_ramo_abertura"]:
    sub = top[top[col] != ""].groupby(col).agg(n=("fechou", "size"), fechou=("fechou", "sum"))
    sub["taxa_pct"] = (100 * sub["fechou"] / sub["n"]).round(1)
    print(sub)


# ---------- 3) exemplos_por_ramo.md ----------
RAMO_LABEL = {
    "0_sem_dado_B5": "Sem dado de B5 (P1 não resolveu essa ligação)",
    "1_B5nao_ChallengerAlta": "Não tentou upsell, mas usou Challenger de alta qualidade",
    "2_B5nao_ChallengerMedia": "Não tentou upsell, Challenger de qualidade média",
    "3_B5nao_ChallengerBaixa": "Não tentou upsell, Challenger de baixa qualidade (malfeito)",
    "4_B5nao_SemChallenger_comOP6": "Não tentou upsell, sem Challenger — mas havia oportunidade óbvia (OP6)",
    "5_B5nao_SemChallenger_semOP6": "Não tentou upsell, sem Challenger, sem oportunidade aparente (padrão do time)",
    "6_B5sim_ChallengerAlta": "Upsell + Challenger de alta qualidade — a combinação vencedora (H10)",
    "7_B5sim_ChallengerFraco_ruido": "Tentou upsell mas sem Challenger de qualidade (amostra pequena, ruído)",
}
SUB_LABEL = {
    "FC1_com_data": "Dentro do ramo vencedor, fechou com FC1 (compromisso com data)",
    "FC3_qualquer_coisa": "Dentro do ramo vencedor, fechou com FC3 (\"qualquer coisa me chama\")",
    "AB1_relacional": "Dentro do ramo vencedor, abriu a ligação de forma relacional (AB1)",
    "AB4_reativa": "Dentro do ramo vencedor, abriu a ligação de forma reativa (AB4, amostra pequena)",
}


def formatar_exemplo(row):
    header = (
        f"#### Cliente {row['cliente_id']} · {row['base_origem']} · {row['data']} · {int(row['duracao_s'])}s\n\n"
        f"**Desfecho:** `{row['p1_desfecho']}`" + (" — **FECHOU**" if row["fechou"] else "") + "  \n"
    )
    resumo = str(row.get("p5_frase_resumo", "")).strip()
    if resumo and resumo.lower() not in ("nenhum", "nan"):
        header += f"**Challenger (resumo IA):** {resumo}  \n"
    desc_op = str(row.get("p6_descricao_curta", "")).strip()
    if desc_op and desc_op.lower() not in ("nenhum", "nan"):
        header += f"**Oportunidade perdida ({row['p6_oportunidades_perdidas']}):** {desc_op}  \n"
    header += (
        f"**Abertura:** `{row.get('p9_tipo_abertura', '-')}` · **Fechamento:** `{row.get('p9_tipo_fechamento', '-')}` · "
        f"**Score comercial:** {row.get('p1_score_comercial', '-')}\n"
    )

    chave = (row["base_origem"], row["cliente_id"], str(row["data"]), str(int(row["duracao_s"])))
    transcricao = INDICE_TRANSCRICOES.get(chave)
    if transcricao:
        corpo = "\n**Transcrição completa:**\n\n```\n" + transcricao + "\n```\n"
    else:
        corpo = "\n_Transcrição não encontrada no índice (ligação pode ter ficado fora dos 175 lotes)._\n"
    return header + corpo


def selecionar_exemplos(sub_df, n=5):
    sub_df = sub_df.copy()
    tem_texto = sub_df["p5_frase_resumo"].astype(str).str.lower().ne("nenhum") & sub_df["p5_frase_resumo"].notna()
    tem_texto |= sub_df["p6_descricao_curta"].astype(str).str.lower().ne("nan") & sub_df["p6_descricao_curta"].notna()
    ordenado = pd.concat([sub_df[tem_texto], sub_df[~tem_texto]])
    return ordenado.drop_duplicates(subset="cliente_id").head(n)


linhas_md = ["# Exemplos reais por ramo — árvore de decisão H10\n",
             "Gerado automaticamente a partir de `dados_arvore_H10.csv`. Pelo menos 5 ligações reais por ramo "
             "(quando o ramo tem 5 ou mais registros), priorizando as que têm resumo textual do Challenger ou "
             "da oportunidade perdida.\n"]

for ramo_key in sorted(df["ramo"].unique()):
    sub_df = df[df["ramo"] == ramo_key]
    n_total = len(sub_df)
    taxa = 100 * sub_df["fechou"].sum() / n_total if n_total else 0
    linhas_md.append(f"\n---\n\n## Ramo: {RAMO_LABEL.get(ramo_key, ramo_key)}")
    linhas_md.append(f"`{ramo_key}` · n={n_total} · taxa de fechamento={taxa:.1f}%\n")
    exemplos = selecionar_exemplos(sub_df, n=5)
    if exemplos.empty:
        linhas_md.append("_Sem exemplos disponíveis._\n")
        continue
    for _, row in exemplos.iterrows():
        linhas_md.append(f"\n{formatar_exemplo(row)}\n")

linhas_md.append("\n---\n\n## Sub-ramos do ramo vencedor (6_B5sim_ChallengerAlta)\n")
for col, key_prefix in [("sub_ramo_fechamento", ""), ("sub_ramo_abertura", "")]:
    for sub_key in [v for v in top[col].unique() if v]:
        sub_df = top[top[col] == sub_key]
        n_total = len(sub_df)
        taxa = 100 * sub_df["fechou"].sum() / n_total if n_total else 0
        linhas_md.append(f"\n### {SUB_LABEL.get(sub_key, sub_key)}")
        linhas_md.append(f"`{sub_key}` · n={n_total} · taxa de fechamento={taxa:.1f}%\n")
        exemplos = selecionar_exemplos(sub_df, n=5)
        for _, row in exemplos.iterrows():
            linhas_md.append(f"\n{formatar_exemplo(row)}\n")

with open(f"{OUT_DIR}/exemplos_por_ramo.md", "w", encoding="utf-8") as f:
    f.write("\n".join(linhas_md))

print(f"\nOK - {OUT_DIR}/exemplos_por_ramo.md escrito.")
print("OK - dados_arvore_H10.csv escrito.")
