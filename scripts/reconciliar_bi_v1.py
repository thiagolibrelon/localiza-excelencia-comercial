"""Gera a planilha de reconciliacao do BI v1: os valores que cada medida DAX deve mostrar quando o relatorio for aberto com os
dados de setembro de 2026. Calcula tudo do CSV (pandas), nunca do Power BI, entao serve de gabarito independente.

COMO USAR:
  python reconciliar_bi_v1.py "Consulta Power Bi - Copia.csv" [--saida missao_4T26/bi/reconciliacao.csv]

Saida: reconciliacao.csv com uma linha por conferencia (id, pagina, medida, periodo, filtro adicional, valor esperado, tolerancia,
como conferir) e duas colunas em branco (valor_no_bi, confere) para preencher durante a validacao de 02 a 06/10.
So agregados: nenhum nome de vendedor, codigo de cliente ou trecho de transcricao sai deste script.

Convencoes (as mesmas de Fato_Ligacoes.m): janela do baseline = 01/09 a 22/09 (a duracao so existe ate 22/09), BaseKPI = classificada pelo GPT
com duracao, K2/K4/K5/K6 usam toda ligacao classificada pelo GPT (nao dependem de duracao).
"""
import argparse
import csv
from pathlib import Path

import numpy as np
import pandas as pd

from auditoria_dados_missao import FIM_DURACAO, NEGOCIACAO, carregar

INI = "2026-09-01"
SAIDA_PADRAO = Path(__file__).resolve().parent.parent / "missao_4T26" / "bi" / "reconciliacao.csv"


def wilson(k, n, z=1.96):
    p = k / n
    den = 1 + z * z / n
    cen = p + z * z / (2 * n)
    am = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (cen - am) / den, (cen + am) / den


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--saida", default=str(SAIDA_PADRAO))
    a = ap.parse_args()
    cru, s = carregar(a.csv)
    s["classe"] = np.where(~s["comp"], "IGNORAR", np.where(s["falou_secretaria_eletronica_b"] == True, "SECRETARIA", np.where(
        s["resumo_analise"].isna(), "SEM ANALISE", np.where(
            (s["objetivo_atingido_b"] == True) & ((s["demanda_venda_eminente_boleano_b"] == True) | (s["nota_demanda_venda_n"] >= 8)
                                                  | ((s["oportunidades_boleano_b"] == True) & (s["nota_oportunidades_n"] >= 7))), "POSITIVA",
            np.where(s["objetivo_atingido_b"] == True, "INFORMATIVA", "DETRATORA")))))
    s["base"] = s["gpt"] & s["dur"].notna()
    s["tipoNeg"] = s["p2_tipo"].isin(NEGOCIACAO)
    s["fv"] = s["fech"] | (s["venda_b"] == True)
    w = s[(s["dt"] >= INI) & (s["dt"] <= FIM_DURACAO)]            # janela do baseline
    b = w[w["base"]]                                              # BaseKPI na janela
    g = w[w["gpt"]]                                               # classificadas GPT na janela
    gem = w[w["comp"] & w["dur"].notna() & w["resumo_analise"].notna()]
    linhas = []

    def add(i, pag, medida, periodo, extra, valor, fmt, tol, como):
        linhas.append([i, pag, medida, periodo, extra, None if valor is None else round(float(valor), 4), fmt, tol, como, "", ""])

    P = "01/09–22/09"
    T = "31/08–30/09 (todo o arquivo)"
    seg = b["dur"].sum()
    # ---- Modelo e carga
    add("M01", "Modelo", "Tentativas", T, "", len(s), "inteiro", 0, "Cartão de linhas da Fato (COUNTROWS)")
    add("M02", "Modelo", "Tentativas", "31/08", "", int((s["dt"] == "2026-08-31").sum()), "inteiro", 0, "Segmentação por data = 31/08. Linhas de 31/08 NÃO somem (M-02)")
    add("M03", "Modelo", "Atendidas (Completed)", T, "", int(s["comp"].sum()), "inteiro", 0, "Funil de status")
    add("M04", "Modelo", "id_transcricao duplicado", T, "", len(s) - s["id_transcricao"].nunique(), "inteiro", 0, "Diagnostico_Pipeline, linha 4")
    add("M05", "Modelo", "Linhas com Data diferente da data UTC original", T, "", 0, "inteiro", 0, "Teste único (M-06): comparar Fato[Data] com a coluna Data da consulta antiga")
    for c, v in s["classe"].value_counts().items():
        add("M06-" + c[:4], "Modelo", f"ClasseLigacao = {c}", T, "", int(v), "inteiro", 0, "Matriz Classe_Legada x ClasseLigacao")
    add("M07", "Modelo", "Classe_Legada = DETRATORA (= DETRATORA + SEM ANALISE novas)", T, "", int((s["Classificação tipo de ligação"] == "DETRATORA").sum()), "inteiro", 0, "M-01: 1.854 + 657")
    add("M08", "Modelo", "Classe_Legada = IGNORAR (= IGNORAR + SECRETARIA novas)", T, "", int((s["Classificação tipo de ligação"] == "IGNORAR").sum()), "inteiro", 0, "M-09: 12.582 + 318")
    add("M09", "Modelo", "Completed sem classificação GPT", T, "", int((s["comp"] & s["fonte_classificacao"].isna()).sum()), "inteiro", 0, "Diagnostico_Pipeline, linha 7")
    add("M10", "Modelo", "Completed sem análise Gemini", T, "", int((s["comp"] & s["resumo_analise"].isna()).sum()), "inteiro", 0, "Diagnostico_Pipeline, linha 6")
    add("M11", "Modelo", "Completed sem duração", "23/09–30/09", "", int((s["comp"] & s["dur"].isna() & (s["dt"] > FIM_DURACAO)).sum()), "inteiro", 0, "Diagnostico_Pipeline, linha 8 (duração parou em 22/09)")

    add("K01", "3 Mês", "Ligacoes Base KPI", P, "", len(b), "inteiro", 0, "Cartão")
    add("K02", "3 Mês", "Horas Base KPI", P, "", seg / 3600, "0,0 h", 0.05, "Cartão")
    add("K03", "3 Mês", "Dias Uteis com Dado", P, "", b["dt"].nunique(), "inteiro", 0, "15 dias úteis (07/09 é feriado)")
    add("K04", "3 Mês", "K1 Carga Operacional", P, "", b.loc[b["op"], "dur"].sum() / seg, "0,0%", 0.0005, "Cartão principal")
    add("K05", "3 Mês", "K1a Com Problema", P, "", b.loc[b["prob"], "dur"].sum() / seg, "0,0%", 0.0005, "Barra empilhada de alocação")
    add("K06", "3 Mês", "K1b Operacional Sem Problema", P, "", (b.loc[b["op"], "dur"].sum() - b.loc[b["prob"], "dur"].sum()) / seg, "0,0%", 0.0005, "Barra empilhada de alocação")
    add("K07", "3 Mês", "K7 Negociacao", P, "", b.loc[b["neg"], "dur"].sum() / seg, "0,0%", 0.0005, "Barra empilhada de alocação")
    add("K08", "3 Mês", "K8 Relacionamento", P, "", b.loc[b["p2_tipo"].isin(["relacionamento_sem_demanda", "onboarding"]) & ~b["op"], "dur"].sum() / seg, "0,0%", 0.0005, "Barra empilhada")
    add("K09", "3 Mês", "K9 Sem Conteudo", P, "", b.loc[b["p2_tipo"].eq("sem_conteudo") & ~b["op"], "dur"].sum() / seg, "0,0%", 0.0005, "Barra empilhada")
    add("K10", "3 Mês", "K1 Gemini Suporte (régua Aletheia)", P, "", gem.loc[gem["categoria_principal"] == "Suporte", "dur"].sum() / gem["dur"].sum(), "0,0%", 0.0005, "Cartão da 2ª régua")
    add("K11", "3 Mês", "Horas Operacionais", P, "", b.loc[b["op"], "dur"].sum() / 3600, "0,0 h", 0.05, "Cartão")

    # ---- Problemas
    pg = g[g["prob"]]
    tp, ts_ = b.loc[b["prob"], "dur"].mean(), b.loc[~b["prob"], "dur"].mean()
    add("P01", "4 Problemas", "Ligacoes Problema (GPT)", P, "", len(pg), "inteiro", 0, "Cartão")
    add("P02", "4 Problemas", "K2 Pendencias", P, "", int((pg["p3_foi_resolvido_na_ligacao"] != "SIM").sum()), "inteiro", 0, "Cartão")
    add("P03", "4 Problemas", "K2 por dia útil", P, "", (pg["p3_foi_resolvido_na_ligacao"] != "SIM").sum() / g["dt"].nunique(), "0,0", 0.05, "Cartão (698 ÷ 15 dias)")
    add("P04", "4 Problemas", "K4 Resolucao na Ligacao", P, "", (pg["p3_foi_resolvido_na_ligacao"] == "SIM").mean(), "0,0%", 0.0005, "Cartão")
    cp = g[g["prob"] & g["cod"].notna()]
    vc = cp["cod"].value_counts()
    add("P05", "4 Problemas", "K5 Reincidencia", P, "", vc[vc >= 2].sum() / vc.sum(), "0,0%", 0.0005, "Cartão")
    add("P06", "4 Problemas", "K6 Taxa de Problema (todas GPT)", P, "", g["prob"].mean(), "0,0%", 0.0005, "Cartão. Com a base de duração (3.546) o valor é 18,8%; o BI usa todas as GPT")
    add("P07", "4 Problemas", "TMA Problema (s)", P, "", tp, "0 s", 0.5, "Cartão")
    add("P08", "4 Problemas", "TMA Sem Problema (s)", P, "", ts_, "0 s", 0.5, "Cartão")
    add("P09", "4 Problemas", "Razao TMA", P, "", tp / ts_, "0,0x", 0.01, "Cartão")
    add("P10", "4 Problemas", "K3 Horas Excedentes", P, "", int(b["prob"].sum()) * (tp - ts_) / 3600, "0,0 h", 0.1, "Cartão (≈ 37 h em 15 dias úteis)")
    par = b[b["prob"]].groupby("p3_problema_principal")["dur"].sum().sort_values(ascending=False)
    for cod in par.index[:3]:
        add("P11-" + cod, "4 Problemas", f"Share Codigo no Problema ({cod})", P, f"Dim_Problema = {cod}", par[cod] / par.sum(), "0,0%", 0.0005, "Pareto (barras)")
    add("P12", "4 Problemas", "Pareto Acumulado até o 3º código", P, "", par.iloc[:3].sum() / par.sum(), "0,0%", 0.0005, "Pareto (linha acumulada): P1+P2+P13")
    for tl in ("Inbound", "Outbound"):
        add("P13-" + tl[:3], "4 Problemas", f"K6 por tipo_ligacao ({tl}) — base com duração", P, f"tipo_ligacao = {tl}", b.loc[b["tipo_ligacao"] == tl, "prob"].mean(), "0,0%", 0.0005, "Colunas de origem. Base BaseKPI")
    add("P14", "4 Problemas", "% dos problemas que são Outbound — base com duração", P, "", b.loc[b["prob"], "tipo_ligacao"].eq("Outbound").mean(), "0,0%", 0.0005, "Cartão/rótulo")

    # ---- Carteiras
    gc = g
    cart = gc.groupby("CARTEIRA").size()
    elig = cart[cart >= 40].index
    def k1c(c):
        x = b[b["CARTEIRA"] == c]
        return x.loc[x["op"], "dur"].sum() / x["dur"].sum()
    add("C01", "5 Carteiras", "Carteiras elegíveis (≥ 40 ligações GPT)", P, "Param_MinLigacoes = 40", len(elig), "inteiro", 0, "Contagem de carteiras no visual")
    add("C02", "5 Carteiras", "K1 Mediana Carteiras", P, "Param_MinLigacoes = 40", np.median([k1c(c) for c in elig]), "0,0%", 0.0005, "Linha de referência")
    for c in sorted(elig)[:3]:
        x = b[b["CARTEIRA"] == c]
        add("C03-" + c, "5 Carteiras", f"K1 Carga Operacional ({c})", P, f"Dim_Carteira = {c}", k1c(c), "0,0%", 0.0005, "Barra da carteira")
        add("C04-" + c, "5 Carteiras", f"Ligacoes GPT ({c})", P, f"Dim_Carteira = {c}", len(g[g["CARTEIRA"] == c]), "inteiro", 0, "Tooltip")
    for d_, x in sorted(g.groupby("DISTRITAL")):
        bb = b[b["DISTRITAL"] == d_]
        add("C05-" + d_, "5 Carteiras", f"K1 Carga Operacional ({d_})", P, f"Dim_Carteira[DISTRITAL] = {d_}", bb.loc[bb["op"], "dur"].sum() / bb["dur"].sum(), "0,0%", 0.0005, "Coluna por distrital")
    cc = s[s["cod"].notna()].groupby("cod")["dur"].sum().sort_values(ascending=False)
    add("C06", "5 Carteiras", "Clientes distintos com código", T, "", len(cc), "inteiro", 0, "DISTINCTCOUNT(CodigoCliente8) sem em branco")
    for q in (1, 10):
        add(f"C07-{q}", "5 Carteiras", f"Pct Tempo Top {q}% Clientes", T, f"Param_TopPct = {q}", cc.head(max(1, int(len(cc) * q / 100))).sum() / cc.sum(), "0,0%", 0.0005, "Barras de concentração")

    # ---- Tempo e ritmo
    nz = w[w["gpt"] & w["tipoNeg"] & w["dur"].notna()]
    for f_, (lo, hi) in {"< 2 min": (0, 120), "2–5 min": (120, 300), "5–8 min": (300, 480), "8–12 min": (480, 720), "> 12 min": (720, 1e9)}.items():
        x = nz[(nz["dur"] > lo) & (nz["dur"] <= hi)]
        k, n_ = int(x["fv"].sum()), len(x)
        l_, h_ = wilson(k, n_)
        add("T01-" + f_[:3].strip(), "6 Tempo", f"Ligacoes Negociacao ({f_})", P, f"Dim_FaixaDuracao = {f_}", n_, "inteiro", 0, "Tooltip da faixa")
        add("T02-" + f_[:3].strip(), "6 Tempo", f"Taxa de Fechamento ({f_})", P, f"Dim_FaixaDuracao = {f_}", k / n_, "0,0%", 0.0005, "Coluna com barra de erro")
        add("T03-" + f_[:3].strip(), "6 Tempo", f"Taxa Fechamento IC Inferior ({f_})", P, f"Dim_FaixaDuracao = {f_}", l_, "0,0%", 0.0005, "Barra de erro inferior (Wilson 95%, z = 1,96)")
        add("T03s-" + f_[:3].strip(), "6 Tempo", f"Taxa Fechamento IC Superior ({f_})", P, f"Dim_FaixaDuracao = {f_}", h_, "0,0%", 0.0005, "Barra de erro superior")
        add("T04-" + f_[:3].strip(), "6 Tempo", f"Fechamentos por Hora ({f_})", P, f"Dim_FaixaDuracao = {f_}", k / (x["dur"].sum() / 3600), "0,00", 0.005, "Coluna fechamentos/h")
    st = s["status"].value_counts(normalize=True)
    for k_ in ("Completed", "Sem Sucesso", "Open"):
        add("T05-" + k_[:4], "6 Tempo", f"% de tentativas com status {k_}", T, f"status = {k_}", st[k_], "0,0%", 0.0005, "Funil")
    h15 = s[s["hora"] == 15]
    add("T06", "6 Tempo", "Taxa Atendimento às 15h", T, "Fato[Hora] = 15", h15["comp"].mean(), "0,0%", 0.0005, "Gráfico de atendimento por hora (valida o fuso: vale do almoço 12–13h)")
    add("T07", "6 Tempo", "Tentativas às 15h", T, "Fato[Hora] = 15", len(h15), "inteiro", 0, "Mesmo gráfico")
    vd = s.groupby(["matricula_ev_createdby", "dt"]).agg(t=("comp", "size"), c=("comp", "sum")).reset_index()
    vd["dow"] = vd["dt"].dt.dayofweek
    for dow, nome in ((0, "segunda"), (4, "sexta")):
        add("T08-" + nome[:3], "6 Tempo", f"Tentativas por Vendedor por Dia ({nome})", T, f"DiaSemanaNum = {dow + 1}", vd.loc[vd["dow"] == dow, "t"].mean(), "0,0", 0.05, "Capacidade por dia da semana (sexta ≈ −29%)")
    o = s[s["tipo_ligacao"].eq("Outbound") & s["cod"].notna()].sort_values(["cod", "ts"])
    cl = o.groupby("cod").agg(tent=("comp", "size"), ok=("comp", "max"), ult=("ts", "max"))
    nunca = cl[~cl["ok"]]
    o["nt"] = o.groupby("cod").cumcount() + 1
    add("T09", "6 Tempo (v1.1)", "Clientes Outbound", T, "", len(cl), "inteiro", 0, "Cliente_Contato")
    add("T10", "6 Tempo (v1.1)", "Clientes Uma Tentativa Sem Sucesso (última tentativa até 22/09)", T, "Dias_Recontato = 7",
        int(((nunca["tent"] == 1) & (nunca["ult"] <= "2026-09-23")).sum()), "inteiro", 0, "≈ 900 conversas/mês se a 2ª tentativa for feita")
    for nt_ in (1, 2, 3, 4):
        add(f"T11-{nt_}", "6 Tempo (v1.1)", f"Taxa Atendimento na tentativa {nt_}", T, f"Tentativa_Seq = {nt_}", o.loc[o["nt"] == nt_, "comp"].mean(), "0,0%", 0.0005, "Cadência")
    ac = s[s["comp"] & s["resumo_analise"].notna() & s["cod"].notna()].copy()
    ac["sug"] = ac["sug"]
    dev = ac[(ac["necessidade_nova_visita_boleano_b"] == True) & ac["sug"].notna() & (ac["sug"] <= "2026-09-30") & (ac["sug"] > ac["dt"])].copy()
    m = dev.merge(s[s["cod"].notna()][["cod", "ts", "dt"]], on="cod", suffixes=("", "_n"))
    m = m[m["ts_n"] > m["ts"]]
    m["np"] = m["dt_n"] <= m["sug"] + pd.Timedelta(days=2)
    dev["np"] = dev["id_transcricao"].map(m.groupby("id_transcricao")["np"].max()).fillna(False)
    add("T12", "6 Tempo (v1.1)", "Retornos Devidos", T, "data sugerida já vencida", len(dev), "inteiro", 0, "Retornos_Devidos")
    add("T13", "6 Tempo (v1.1)", "Retorno no Prazo %", T, "", dev["np"].mean(), "0,0%", 0.0005, "Retornos_Devidos")

    # ---- Competências
    add("S01", "7 Competências", "Taxa Challenger", T, "EhGPT", s.loc[s["gpt"], "ch"].mean(), "0,0%", 0.0005, "Escada Challenger")
    for nome, col in (("Taxa Trouxe Dado", "p5_trouxe_dado"), ("Taxa Conectou Situacao", "p5_conectou_situacao"), ("Taxa Cliente Reagiu", "p5_cliente_reagiu")):
        x = s.loc[s["gpt"], col]
        add("S02-" + col[3:7], "7 Competências", nome, T, "EhGPT, sem em branco", (x == "SIM").sum() / x.notna().sum(), "0,0%", 0.0005, "Escada Challenger")
    for nome, col in (("SPIN Situacao", "nota_spin_situacao_n"), ("SPIN Problema", "nota_spin_problema_n"), ("SPIN Implicacao", "nota_spin_implicacao_n"), ("SPIN Necessidade", "nota_spin_necessidade_solucao_n")):
        add("S03-" + nome[5:8], "7 Competências", nome, T, "", s[col].mean(), "0,00", 0.005, "Barras SPIN (média 1–5)")
    x = s["nota_spin_implicacao_n"].dropna()
    add("S04", "7 Competências", "SPIN Implicacao Nota 1 %", T, "", (x == 1).mean(), "0,0%", 0.0005, "Cartão")
    add("S05", "7 Competências", "Falou com Decisor %", T, "", s["falou_tomador_decisao_b"].mean(), "0,0%", 0.0005, "Cartão")

    # ---- Qualidade do dado
    comp = w[w["comp"]]
    add("Q01", "8 Qualidade", "C1 Cobertura Classificacao", P, "", comp["fonte_classificacao"].notna().mean(), "0,0%", 0.0005, "Linha diária C1 (meta ≥ 95%)")
    add("Q02", "8 Qualidade", "C2 Cobertura Duracao", P, "", comp["dur"].notna().mean(), "0,0%", 0.0005, "Linha diária C2")
    c2 = s[s["comp"] & (s["dt"] > FIM_DURACAO)]
    add("Q03", "8 Qualidade", "C2 Cobertura Duracao", "23/09–30/09", "", c2["dur"].notna().mean(), "0,0%", 0.0005, "Cai a 0% depois de 22/09")
    c1 = s[s["comp"] & (s["dt"] >= "2026-09-28")]
    add("Q04", "8 Qualidade", "C1 Cobertura Classificacao", "28/09–30/09", "", c1["fonte_classificacao"].notna().mean(), "0,0%", 0.0005, "Cai a 0% em 28–30/09")

    # ---- Série diária e semanal (pontos de controle)
    for d_ in ("2026-09-02", "2026-09-15", "2026-09-22"):
        x = w[w["dt"] == d_]
        xb, xg = x[x["base"]], x[x["comp"] & x["dur"].notna() & x["resumo_analise"].notna()]
        add("D01-" + d_[-5:], "1 Dia", "K1 Carga Operacional", d_, "", xb.loc[xb["op"], "dur"].sum() / xb["dur"].sum(), "0,0%", 0.0005, "Linha diária K1 (GPT)")
        add("D02-" + d_[-5:], "1 Dia", "K1 Gemini Suporte", d_, "", xg.loc[xg["categoria_principal"] == "Suporte", "dur"].sum() / xg["dur"].sum(), "0,0%", 0.0005, "Linha diária K1 (Gemini)")
        add("D03-" + d_[-5:], "1 Dia", "K2 Pendencias", d_, "", int((x["gpt"] & x["prob"] & (x["p3_foi_resolvido_na_ligacao"] != "SIM")).sum()), "inteiro", 0, "Cartão de pendências")
    s2 = s[(s["dt"] >= INI) & (s["dt"] <= "2026-09-30")]
    s2 = s2.assign(sem=s2["dt"].dt.to_period("W").astype(str))
    for sem, x in s2.groupby("sem"):
        xb = x[x["base"]]
        if len(xb) == 0:
            continue
        add("W01-" + sem[:10], "2 Semana", "K1 Carga Operacional", sem, "Dim_Calendario[SemanaInicio]", xb.loc[xb["op"], "dur"].sum() / xb["dur"].sum(), "0,0%", 0.0005, "Colunas semanais")
        add("W02-" + sem[:10], "2 Semana", "K7 Negociacao", sem, "Dim_Calendario[SemanaInicio]", xb.loc[xb["neg"], "dur"].sum() / xb["dur"].sum(), "0,0%", 0.0005, "Colunas semanais")
        add("W03-" + sem[:10], "2 Semana", "Horas Base KPI", sem, "Dim_Calendario[SemanaInicio]", xb["dur"].sum() / 3600, "0,0 h", 0.05, "Colunas semanais")
        add("W04-" + sem[:10], "2 Semana", "K2 Pendencias", sem, "Dim_Calendario[SemanaInicio]", int((x["gpt"] & x["prob"] & (x["p3_foi_resolvido_na_ligacao"] != "SIM")).sum()), "inteiro", 0, "Matriz semanal (inclui 23–25/09 sem duração)")

    # ---- Página 9 · Meu painel (exemplo: carteira S1I05A; relatório do vendedor, v1.2)
    cs = "S1I05A"
    me = s[s["CARTEIRA"] == cs]
    bm = b[b["CARTEIRA"] == cs]
    k1m = bm.loc[bm["op"], "dur"].sum() / bm["dur"].sum()
    gp = g[(g["CARTEIRA"] == cs) & g["prob"]]
    pend_cli = gp[gp["cod"].notna() & (gp["p3_foi_resolvido_na_ligacao"] != "SIM")]["cod"].nunique()
    cl_ = me[me["comp"] & me["classe"].isin(["POSITIVA", "INFORMATIVA", "DETRATORA"])]
    aa = s[s["comp"] & s["resumo_analise"].notna() & s["cod"].notna() & (s["CARTEIRA"] == cs)]
    dv = aa[(aa["necessidade_nova_visita_boleano_b"] == True) & aa["sug"].notna() & (aa["sug"] <= "2026-09-30") & (aa["sug"] > aa["dt"])].copy()
    mm_ = dv.merge(s[s["cod"].notna()][["cod", "ts", "dt"]], on="cod", suffixes=("", "_n"))
    mm_ = mm_[mm_["ts_n"] > mm_["ts"]]
    mm_["np"] = mm_["dt_n"] <= mm_["sug"] + pd.Timedelta(days=2)
    dv["np"] = dv["id_transcricao"].map(mm_.groupby("id_transcricao")["np"].max()).fillna(False).astype(bool)
    oo = me[me["tipo_ligacao"].eq("Outbound") & me["cod"].notna()]
    c2_ = oo.groupby("cod").agg(tent=("comp", "size"), ok=("comp", "max"), ult=("ts", "max"))
    PC = f"Dim_Carteira = {cs}"
    add("V01", "9 Meu painel", "K7 Negociacao", P, PC, bm.loc[bm["neg"], "dur"].sum() / bm["dur"].sum(), "0,0%", 0.0005, "Cartão 9.1")
    add("V02", "9 Meu painel", "K7 Time", P, "(sem filtro de carteira)", b.loc[b["neg"], "dur"].sum() / b["dur"].sum(), "0,0%", 0.0005, "Apoio do 9.1 (Resumo_Time)")
    add("V03", "9 Meu painel", "K1 Carga Operacional", P, PC, k1m, "0,0%", 0.0005, "Cartão 9.2")
    add("V04", "9 Meu painel", "K1 Time", P, "(sem filtro de carteira)", b.loc[b["op"], "dur"].sum() / b["dur"].sum(), "0,0%", 0.0005, "Apoio do 9.2 (Resumo_Time)")
    add("V05", "9 Meu painel", "Taxa Atendimento", T, PC, me["comp"].mean(), "0,0%", 0.0005, "Cartão 9.3 · período 31/08–30/09")
    add("V06", "9 Meu painel", "Tentativas", T, PC, len(me), "inteiro", 0, "Cartão 9.3")
    add("V07", "9 Meu painel", "K2 Pendencias", P, PC, int((gp["p3_foi_resolvido_na_ligacao"] != "SIM").sum()), "inteiro", 0, "Cartão 9.4")
    add("V08", "9 Meu painel", "Clientes com Pendencia", P, PC, pend_cli, "inteiro", 0, "Chip do 9.9")
    add("V09", "9 Meu painel", "Pct Conversas Detratoras", T, PC, (cl_["classe"] == "DETRATORA").mean(), "0,0%", 0.0005, "Cartão 9.5 · período 31/08–30/09")
    sc_ = s[s["comp"] & s["classe"].isin(["POSITIVA", "INFORMATIVA", "DETRATORA"])]
    add("V10", "9 Meu painel", "Pct Conversas Detratoras Time", T, "(sem filtro de carteira)", (sc_["classe"] == "DETRATORA").mean(), "0,0%", 0.0005, "Apoio do 9.5 (Resumo_Time)")
    add("V11", "9 Meu painel", "Clientes Retorno Vencido", T, PC, dv.loc[~dv["np"], "cod"].nunique(), "inteiro", 0, "Chip do 9.9 · exige Retornos_Devidos")
    add("V12", "9 Meu painel", "Clientes Sem 2a Tentativa", T, PC, int(((c2_["tent"] == 1) & (~c2_["ok"]) & (c2_["ult"] <= "2026-09-23")).sum()), "inteiro", 0, "Chip do 9.9")

    saida = Path(a.saida)
    saida.parent.mkdir(parents=True, exist_ok=True)
    with saida.open("w", encoding="utf-8-sig", newline="") as f:
        wr = csv.writer(f, delimiter=";")
        wr.writerow(["id", "pagina", "medida", "periodo", "filtro_adicional", "esperado", "formato", "tolerancia_abs", "como_conferir", "valor_no_bi", "confere"])
        def fmt_val(l):
            v = l[5]
            if v is None:
                return ""
            return str(int(v)) if l[6] == "inteiro" else str(v).replace(".", ",")
        wr.writerows([[fmt_val(l) if i == 5 else (str(v).replace(".", ",") if i == 7 else v) for i, v in enumerate(l)] for l in linhas])
    print("ok", saida, len(linhas), "conferências")


if __name__ == "__main__":
    main()
