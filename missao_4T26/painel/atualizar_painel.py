"""Atualiza o painel da venda interna (DVINT): lê o CSV exportado da consulta e grava dados.js na pasta do painel.

COMO USAR (no seu computador, com Python 3 + pandas):
  python atualizar_painel.py
      sem argumentos: abre uma janela para escolher o CSV (ou a pasta com os CSVs) e outra para a pasta do painel
      (a pasta sincronizada do SharePoint, onde ficam painel.html e "Abrir painel.bat"). Lembra as escolhas para a próxima vez.
  python atualizar_painel.py --entrada "C:\\...\\Consulta Power Bi.csv" --saida "C:\\...\\Painel DVINT\\Gestao"

ENTRADA: o CSV da consulta (mesmo formato de colunas do arquivo de setembro, separador ";"). Pode ser um arquivo só
  (acumulado) ou uma pasta com vários CSVs: as linhas são juntadas e uma ligação (id_transcricao) repetida fica com a
  versão do arquivo mais recente. Colunas opcionais que faltarem viram "sem dado" no painel, sem interromper.

SAÍDA: <pasta do painel>/dados.js — números agregados por dia e carteira, mais uma tabela por cliente (código do cliente
  PJ, sem nome nem telefone). Sem nome de vendedor (a carteira identifica) e sem texto de ligação.
  O arquivo é gravado com outro nome e renomeado no fim, para o OneDrive nunca sincronizar um arquivo pela metade.
  A cada execução, painel.html, app.js, vendor/ e "Abrir painel.bat" da pasta deste script são copiados para a pasta
  do painel se estiverem diferentes (é assim que uma versão nova do painel chega a todos).
  Se existir <pasta do painel>/logs/, os acessos registrados pelo "Abrir painel.bat" viram contagens no painel.

DEFINIÇÕES (as mesmas do memo da RMR; o painel mostra o dicionário completo na página "Qualidade do dado"):
  analisada = tem fonte_classificacao · conversa = analisada e p2_tipo diferente de sem_conteudo
  oportunidade de venda = analisada e p1_desfecho diferente de nao_era_venda · fechamento = p1_desfecho começa com "fechou"
  problema = tem_problema SIM · carga operacional (tempo) = problema + suporte, cobrança, pós-venda e dúvida de contrato,
  sobre o tempo das ligações classificadas pelo GPT com duração · horário de Brasília (UTC −3).
  Baseline = o período de CONFIG_PAINEL (setembro/2026), calculado dos próprios dados com os mesmos filtros da tela.
"""
import argparse
import json
import os
import re
import tempfile
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

VERSAO = "2.0"
FUSO_H = -3
OPERACIONAIS = ["suporte_operacional", "supporte_operacional", "cobranca", "pos_venda_manutencao", "pos_venda_sinistro",
                "duvida_contrato"]
NEGOCIACAO = ["nova_venda", "upsell", "renovacao", "retencao", "misto"]
RELACIONAMENTO = ["relacionamento_sem_demanda", "onboarding"]
SENTINELAS = {"sem dados necessários", "nenhum", "Sem Classificação", "nao_aplicavel", "NENHUM"}
CAMPOS_SENTINELA = ["volume_aluguel_concorrencia", "volume_frota_propria", "aluguel_concorrencia", "frota_propria",
                    "spin_implicacao", "data_sugerida_nova_visita", "motivo_nova_visita"]
CONFIG_PAINEL = {
    # baseline: calculado dos dados deste período (o painel compara qualquer filtro com o mesmo filtro neste período)
    "baseline_inicio": "2026-09-01", "baseline_fim": "2026-09-30", "baseline_rotulo": "setembro/2026",
    "meta_k1_pp": -5, "meta_k1_piloto_pp": -10,          # metas da carga operacional, em pontos percentuais do baseline
    "alerta_pp": 10, "limite_cobertura": 0.95, "dias_uteis_mes": 21,
    "min_ligacoes": 30,      # mínimo de conversas no período para uma carteira entrar em rankings e medianas
    "min_n_taxa": 30,        # abaixo disso a taxa aparece com aviso de amostra pequena
    "dias_recontato": 7,
}
CONFIG_EXTRA = Path(__file__).with_name("painel_config.json")   # opcional: sobrescreve chaves de CONFIG_PAINEL
OBRIGATORIAS = ["id_transcricao", "data_visita_ev", "status", "tipo_ligacao", "codigo_cliente", "DISTRITAL", "CARTEIRA",
                "CallDurationInSeconds", "fonte_classificacao", "p1_desfecho", "p2_tipo", "tem_problema",
                "p3_problema_principal", "p3_foi_resolvido_na_ligacao", "p5_teve_challenger", "segment_id"]
OPCIONAIS = ["resumo_analise", "categoria_principal", "falou_tomador_decisao", "falou_secretaria_eletronica",
             "necessidade_nova_visita_boleano", "urgencia_nova_visita", "data_sugerida_nova_visita", "nota_spin_situacao",
             "nota_spin_problema", "nota_spin_implicacao", "nota_spin_necessidade_solucao", "nota_final_spin",
             "p1_tentativa_comercial", "p3_problemas_identificados", "p5_qualidade", "p5_codigos_challenger",
             "p5_trouxe_dado", "p5_conectou_situacao", "p5_cliente_reagiu", "p5_challenger_sem_dado",
             "frota_propria_boleano", "aluguel_concorrencia_boleano", "venda"]
CONFIG_LOCAL = Path(__file__).with_name("atualizar_painel_config.json")
ARQUIVOS_PAINEL = ["painel.html", "app.js", "Abrir painel.bat", "vendor/echarts.min.js", "vendor/echarts-pt-br.js",
                   "vendor/LICENSE-echarts.txt"]
FAIXAS_DUR = [0, 120, 300, 480, 720, 1e9]
FAIXAS_HORA = [0, 10, 12, 14, 16, 24]
NOMES_FACETAS = ["Qualidade do Challenger", "Teve Challenger", "Trouxe dado", "Cliente reagiu", "SPIN Implicação",
                 "SPIN nota final", "Falou com o decisor", "Tipo de oportunidade", "Origem da ligação", "Duração da ligação",
                 "Teve problema na ligação", "Horário"]
NIVEIS_FACETAS = [["Sem Challenger", "Baixa", "Média", "Alta"], ["Não", "Sim"], ["Não", "Sim"], ["Não", "Sim"],
                  ["1", "2", "3", "4", "5"], ["1", "2", "3", "4", "5"], ["Não", "Sim"], None, ["Receptiva", "Ativa"],
                  ["< 2 min", "2–5 min", "5–8 min", "8–12 min", "> 12 min"], ["Não", "Sim"],
                  ["antes das 10h", "10h–12h", "12h–14h", "14h–16h", "16h ou mais"]]


# --------------------------------------------------------------------------------------------------------------------
# leitura
# --------------------------------------------------------------------------------------------------------------------
def ler_csv(caminho):
    for enc in ("utf-8-sig", "cp1252"):
        try:
            with open(caminho, encoding=enc) as f:
                cab = f.readline()
            sep = ";" if cab.count(";") >= cab.count(",") else ","
            return pd.read_csv(caminho, sep=sep, encoding=enc, dtype=str, keep_default_na=False, low_memory=False)
        except UnicodeDecodeError:
            continue
    raise SystemExit(f"Não consegui ler {caminho} (codificação desconhecida).")


def carregar(entrada):
    p = Path(entrada)
    arquivos = sorted(p.glob("*.csv"), key=lambda x: x.stat().st_mtime) if p.is_dir() else [p]
    if not arquivos:
        raise SystemExit(f"Nenhum CSV encontrado em {p}")
    partes = []
    for i, a in enumerate(arquivos):
        df = ler_csv(a)
        df["_ordem"] = i
        partes.append(df)
        print(f"  lido {a.name}: {len(df):,} linhas".replace(",", "."))
    df = pd.concat(partes, ignore_index=True)
    faltam = [c for c in OBRIGATORIAS if c not in df.columns]
    if faltam:
        raise SystemExit("O CSV não tem as colunas obrigatórias (é a exportação da consulta completa?).\n"
                         "Faltam: " + ", ".join(faltam))
    ausentes = [c for c in OPCIONAIS if c not in df.columns]
    if ausentes:
        print("  colunas opcionais ausentes (viram 'sem dado' no painel): " + ", ".join(ausentes))
    df = df.replace("", np.nan)
    antes = len(df)
    df = df.sort_values("_ordem").drop_duplicates("id_transcricao", keep="last").drop(columns="_ordem")
    if len(df) < antes:
        print(f"  {antes - len(df):,} linhas repetidas entre arquivos (ficou a versão mais recente)".replace(",", "."))
    return df


def numero(s):
    """Converte '46265,53716', '123', '12.5' em float (CSV pt-BR ou en-US)."""
    t = s.astype("string").str.strip()
    br = t.str.contains(",", regex=False, na=False)
    t = t.where(~br, t.str.replace(".", "", regex=False).str.replace(",", ".", regex=False))
    return pd.to_numeric(t, errors="coerce").astype(float)


def data_hora(s):
    """data_visita_ev vem como número de série do Excel (UTC) ou como texto de data; devolve horário de Brasília."""
    v = numero(s)
    serial = pd.to_datetime("1899-12-30") + pd.to_timedelta(v, unit="D")
    texto = pd.to_datetime(s.where(v.isna()), dayfirst=True, errors="coerce")
    return serial.fillna(texto) + pd.Timedelta(hours=FUSO_H)


def booleano(s):
    m = {"verdadeiro": True, "true": True, "1": True, "sim": True, "falso": False, "false": False, "0": False, "nao": False,
         "não": False}
    return s.astype("string").str.strip().str.lower().map(m)


def coluna(df, nome):
    return df[nome] if nome in df.columns else pd.Series(np.nan, index=df.index, dtype=object)


def sim(serie):
    return serie.astype("string").str.strip().str.upper().isin(["SIM", "TRUE", "VERDADEIRO", "1"]).fillna(False).astype(bool)


def preparar(df):
    s = pd.DataFrame(index=df.index)
    s["ts"] = data_hora(df["data_visita_ev"])
    s = s[s["ts"].notna()].copy()
    df = df.loc[s.index]
    c = lambda nome: coluna(df, nome)  # noqa: E731
    s["dt"] = s["ts"].dt.normalize()
    s["hora"] = s["ts"].dt.hour
    s["dur"] = numero(df["CallDurationInSeconds"])
    s["status"] = df["status"]
    s["comp"] = df["status"].eq("Completed")
    s["tipo"] = df["tipo_ligacao"]
    s["outb"] = s["tipo"].eq("Outbound")
    s["carteira"] = df["CARTEIRA"].fillna("(sem carteira)")
    s["distrital"] = df["DISTRITAL"].fillna("")
    s["fonte"] = df["fonte_classificacao"]
    s["an"] = s["fonte"].notna()
    s["gpt"] = s["fonte"].eq("gpt")
    s["p1"] = df["p1_desfecho"]
    s["p2"] = df["p2_tipo"]
    # definições do memo
    s["conv"] = s["an"] & s["p2"].notna() & s["p2"].ne("sem_conteudo")
    s["opp"] = s["an"] & s["p1"].notna() & s["p1"].ne("nao_era_venda")
    s["inter"] = s["p1"].eq("interessou_nao_fechou")
    s["fech"] = s["p1"].fillna("").str.startswith("fechou")
    s["prob"] = s["an"] & df["tem_problema"].eq("SIM")
    s["res"] = df["p3_foi_resolvido_na_ligacao"]
    s["cod_prob"] = df["p3_problema_principal"]
    s["pend"] = s["prob"] & s["res"].ne("SIM")
    # tempo (carga operacional): base = classificada pelo GPT com duração
    s["op"] = s["prob"] | s["p2"].isin(OPERACIONAIS)
    s["neg"] = s["p2"].isin(NEGOCIACAO) & ~s["op"]
    s["rel"] = s["p2"].isin(RELACIONAMENTO) & ~s["op"]
    s["sc"] = s["p2"].eq("sem_conteudo") & ~s["op"]
    s["base"] = s["gpt"] & s["dur"].notna()
    s["analise"] = c("resumo_analise").notna()
    s["gem"] = s["comp"] & s["dur"].notna() & s["analise"]
    s["suporte"] = c("categoria_principal").eq("Suporte")
    # Challenger (sobre as conversas)
    s["ch"] = s["conv"] & sim(df["p5_teve_challenger"])
    q = c("p5_qualidade").astype("string").str.strip().str.lower().fillna("")
    s["chq"] = q.map({"baixa": 1, "media": 2, "média": 2, "alta": 3}).fillna(0).astype(int).where(s["ch"], 0)
    s["ch_sd"] = s["conv"] & sim(c("p5_challenger_sem_dado"))
    for k, nome in (("dado", "p5_trouxe_dado"), ("con", "p5_conectou_situacao"), ("rea", "p5_cliente_reagiu")):
        s[k + "_s"] = s["conv"] & sim(c(nome))
        s[k + "_n"] = s["conv"] & c(nome).notna()
    s["ch_cod"] = c("p5_codigos_challenger").where(s["conv"])
    # SPIN e campos da análise Gemini
    for k, nome in (("ss", "nota_spin_situacao"), ("sp", "nota_spin_problema"), ("si", "nota_spin_implicacao"),
                    ("sn", "nota_spin_necessidade_solucao"), ("sf", "nota_final_spin")):
        v = numero(c(nome))
        s[k] = v.where(v.between(1, 5))
    for k, nome in (("dec", "falou_tomador_decisao"), ("sec", "falou_secretaria_eletronica"), ("fp", "frota_propria_boleano"),
                    ("ac", "aluguel_concorrencia_boleano")):
        b = booleano(c(nome))
        s[k + "_s"] = b.eq(True).fillna(False).astype(bool)
        s[k + "_n"] = b.notna()
    tc = c("p1_tentativa_comercial")
    s["tc_s"] = s["conv"] & sim(tc)
    s["tc_n"] = s["conv"] & tc.notna()
    s["pi_cod"] = c("p3_problemas_identificados").where(s["prob"])
    cod = df["codigo_cliente"].astype("string").str.strip().str.replace(r"\.0$", "", regex=True)
    s["cod"] = cod.where(cod.notna() & cod.ne("")).str.zfill(8)
    s["necess"] = booleano(c("necessidade_nova_visita_boleano")).eq(True).fillna(False).astype(bool)
    s["urg"] = numero(c("urgencia_nova_visita"))
    s["sug"] = pd.to_datetime(c("data_sugerida_nova_visita"), format="%d/%m/%Y", errors="coerce")
    s["id"] = df["id_transcricao"]
    s["segment_id"] = df["segment_id"]
    return s, df


# --------------------------------------------------------------------------------------------------------------------
# fatos agregados
# --------------------------------------------------------------------------------------------------------------------
def r6(x):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 6)


def num(v):
    v = float(v)
    return int(v) if v.is_integer() else round(v, 3)


def linhas(frame, chaves, valores):
    if frame.empty:
        return []
    g = frame.groupby(chaves, as_index=False)[valores].sum()
    return [[num(v) for v in row] for row in g[chaves + valores].to_numpy()]


def construir(s, df, pasta_saida, config):
    dias = sorted(s["dt"].dt.strftime("%Y-%m-%d").unique())
    di = {d: i for i, d in enumerate(dias)}
    cart = (s.groupby("carteira")["distrital"].agg(lambda x: x.mode().iat[0] if len(x.mode()) else "")).sort_index()
    ci = {c: i for i, c in enumerate(cart.index)}
    s["di"] = s["dt"].dt.strftime("%Y-%m-%d").map(di).astype(int)
    s["ci"] = s["carteira"].map(ci).astype(int)
    d0 = s["dur"].fillna(0)
    b = s["base"]
    um = pd.Series(1.0, index=s.index)

    def soma(cond, val=None):
        return (cond if val is None else val.where(cond, 0)).astype(float)

    colsA = {
        # volume e funil
        "tent": um, "atend": soma(s["comp"]), "sem_suc": soma(s["status"].eq("Sem Sucesso")), "open": soma(s["status"].eq("Open")),
        "outb": soma(s["outb"]), "outb_a": soma(s["outb"] & s["comp"]),
        "an": soma(s["an"]), "gpt": soma(s["gpt"]), "conv": soma(s["conv"]), "opp": soma(s["opp"]), "inter": soma(s["inter"]),
        "fech": soma(s["fech"]), "fech_novo": soma(s["p1"].eq("fechou_novo")), "fech_renov": soma(s["p1"].eq("fechou_renovacao")),
        "fech_upsell": soma(s["p1"].eq("fechou_upsell")), "tc_s": soma(s["tc_s"]), "tc_n": soma(s["tc_n"]),
        # problemas
        "prob": soma(s["prob"]), "pend": soma(s["pend"]), "res_sim": soma(s["prob"] & s["res"].eq("SIM")),
        "res_par": soma(s["prob"] & s["res"].eq("PARCIAL")), "res_nao": soma(s["prob"] & s["res"].eq("NAO")),
        # tempo
        "base_n": soma(b), "seg_base": soma(b, d0), "seg_op": soma(b & s["op"], d0), "seg_prob": soma(b & s["prob"], d0),
        "seg_neg": soma(b & s["neg"], d0), "seg_rel": soma(b & s["rel"], d0), "seg_sc": soma(b & s["sc"], d0),
        "n_prob_base": soma(b & s["prob"]), "n_ops": soma(b & s["op"] & ~s["prob"]), "n_neg": soma(b & s["neg"]),
        "n_rel": soma(b & s["rel"]), "n_sc": soma(b & s["sc"]),
        "seg_opp": soma(b & s["opp"], d0), "n_opp_base": soma(b & s["opp"]),
        "gem_seg": soma(s["gem"], d0), "gem_sup": soma(s["gem"] & s["suporte"], d0),
        # cobertura
        "comp_cls": soma(s["comp"] & s["an"]), "comp_dur": soma(s["comp"] & s["dur"].notna()), "comp_gem": soma(s["comp"] & s["analise"]),
        # Challenger
        "ch": soma(s["ch"]), "ch_alta": soma(s["chq"].eq(3)), "ch_media": soma(s["chq"].eq(2)), "ch_baixa": soma(s["chq"].eq(1)),
        "ch_sd": soma(s["ch_sd"]),
        "dado_s": soma(s["dado_s"]), "dado_n": soma(s["dado_n"]), "con_s": soma(s["con_s"]), "con_n": soma(s["con_n"]),
        "rea_s": soma(s["rea_s"]), "rea_n": soma(s["rea_n"]),
        # SPIN
        "ss_sum": s["ss"].fillna(0), "ss_n": soma(s["ss"].notna()), "sp_sum": s["sp"].fillna(0), "sp_n": soma(s["sp"].notna()),
        "si_sum": s["si"].fillna(0), "si_n": soma(s["si"].notna()),
        "sn_sum": s["sn"].fillna(0), "sn_n": soma(s["sn"].notna()), "sf_sum": s["sf"].fillna(0), "sf_n": soma(s["sf"].notna()),
        # análise Gemini
        "dec_s": soma(s["dec_s"]), "dec_n": soma(s["dec_n"]), "sec_s": soma(s["sec_s"]), "sec_n": soma(s["sec_n"]),
        "fp_s": soma(s["fp_s"]), "fp_n": soma(s["fp_n"]), "ac_s": soma(s["ac_s"]), "ac_n": soma(s["ac_n"]),
        "nec": soma(s["necess"] & s["analise"]),
    }
    for k in ("ss", "sp", "si", "sn", "sf"):       # distribuição das notas SPIN: ss1..ss5, sp1..sp5, ...
        for nota in range(1, 6):
            colsA[f"{k}{nota}"] = soma(s[k].eq(nota))
    A = pd.DataFrame(colsA)
    A["di"], A["ci"] = s["di"], s["ci"]
    A = A.groupby(["di", "ci"], as_index=False).sum()
    colA = list(colsA)

    # conversão por fator (sobre as oportunidades de venda)
    op = s[s["opp"]].copy()
    fac = []

    def faceta(i, nivel, filtro=None):
        x = op if filtro is None else op[filtro]
        nv = nivel if filtro is None else nivel[filtro]
        fac.append(pd.DataFrame({"di": x["di"], "ci": x["ci"], "f": i, "nv": nv.astype(int), "n": 1, "k": x["fech"].astype(int)}))

    tipos_opp = [t for t in NEGOCIACAO if (op["p2"] == t).any()] + ["outro"]
    faceta(0, op["chq"])
    faceta(1, op["ch"].astype(int))
    faceta(2, op["dado_s"].astype(int), op["dado_n"])
    faceta(3, op["rea_s"].astype(int), op["rea_n"])
    faceta(4, op["si"].fillna(0) - 1, op["si"].notna())
    faceta(5, op["sf"].fillna(0) - 1, op["sf"].notna())
    faceta(6, op["dec_s"].astype(int), op["dec_n"])
    faceta(7, op["p2"].map({t: i for i, t in enumerate(tipos_opp)}).fillna(len(tipos_opp) - 1))
    faceta(8, op["outb"].astype(int))
    faceta(9, pd.Series(pd.cut(op["dur"], FAIXAS_DUR, labels=False), index=op.index).fillna(0), op["dur"] > 0)
    faceta(10, op["prob"].astype(int))
    faceta(11, pd.Series(pd.cut(op["hora"], FAIXAS_HORA, right=False, labels=False), index=op.index).fillna(0))
    CV = linhas(pd.concat(fac), ["di", "ci", "f", "nv"], ["n", "k"]) if fac else []
    niveis = [lv if lv is not None else [t.replace("_", " ") for t in tipos_opp] for lv in NIVEIS_FACETAS]

    # códigos Challenger (uma ligação pode ter mais de um)
    chc = s["ch_cod"].dropna().astype(str).str.findall(r"CH\d+").explode().dropna()
    ch_codigos = sorted(chc.unique(), key=lambda x: int(x[2:]))
    CH = linhas(pd.DataFrame({"di": s.loc[chc.index, "di"], "ci": s.loc[chc.index, "ci"],
                              "k": chc.map({c: i for i, c in enumerate(ch_codigos)}), "n": 1}), ["di", "ci", "k"], ["n"])

    # problemas: código principal (com tempo, pendência e resolução) e todos os códigos identificados
    pg = s[s["prob"]].copy()
    pi = s["pi_cod"].dropna().astype(str).str.findall(r"P\d+").explode().dropna()
    codigos = sorted(set(pg["cod_prob"].fillna("nenhum")) | set(pi), key=lambda c: (c == "nenhum", len(c), c))
    cidx = {c: i for i, c in enumerate(codigos)}
    pg["cod_i"] = pg["cod_prob"].fillna("nenhum").map(cidx)
    pg = pg.assign(n=1, seg=pg["dur"].where(pg["base"], 0).fillna(0), nb=pg["base"].astype(int), pd_=pg["pend"].astype(int),
                   sim_=pg["res"].eq("SIM").astype(int), par=pg["res"].eq("PARCIAL").astype(int), nao=pg["res"].eq("NAO").astype(int))
    P = linhas(pg, ["di", "ci", "cod_i"], ["n", "seg", "nb", "pd_", "sim_", "par", "nao"])
    PI = linhas(pd.DataFrame({"di": s.loc[pi.index, "di"], "ci": s.loc[pi.index, "ci"], "k": pi.map(cidx), "n": 1}),
                ["di", "ci", "k"], ["n"])

    # tempo por tipo de ligação (p2_tipo) e por hora
    tp = s[s["an"] & s["p2"].notna()].copy()
    tipos = list(tp["p2"].value_counts().index)
    tp = tp.assign(t=tp["p2"].map({t: i for i, t in enumerate(tipos)}), n=1, nb=tp["base"].astype(int),
                   seg=tp["dur"].where(tp["base"], 0).fillna(0), pr=tp["prob"].astype(int))
    TP = linhas(tp, ["di", "ci", "t"], ["n", "nb", "seg", "pr"])
    H = linhas(s.assign(t=1, a=s["comp"].astype(int), seg=d0.where(b, 0), conv_=s["conv"].astype(int)),
               ["di", "ci", "hora"], ["t", "a", "seg", "conv_"])
    # faixas de duração das oportunidades de venda
    nz = s[s["opp"] & (s["dur"] > 0)].copy()
    nz["faixa"] = pd.cut(nz["dur"], FAIXAS_DUR, labels=False).astype(int)
    F = linhas(nz.assign(n=1, k=nz["fech"].astype(int), seg=nz["dur"]), ["di", "ci", "faixa"], ["n", "k", "seg"])
    # origem: conversas e problemas por receptiva/ativa
    O = linhas(s[s["conv"]].assign(tp=lambda x: x["outb"].astype(int), n=1, p=lambda x: x["prob"].astype(int)),
               ["di", "ci", "tp"], ["n", "p"])

    # clientes (código PJ); tempo = todas as ligações com duração, classificadas ou não
    clientes = sorted(s["cod"].dropna().unique())
    kidx = {c: i for i, c in enumerate(clientes)}
    s["k"] = s["cod"].map(kidx)
    sc_ = s[s["k"].notna()].copy()
    sc_["k"] = sc_["k"].astype(int)
    CL = linhas(sc_.assign(t=1, a=sc_["comp"].astype(int), cv=sc_["conv"].astype(int), seg=d0.loc[sc_.index],
                           p=sc_["prob"].astype(int), pd_=sc_["pend"].astype(int), o=sc_["opp"].astype(int),
                           f=sc_["fech"].astype(int)), ["di", "ci", "k"], ["t", "a", "cv", "seg", "p", "pd_", "o", "f"])

    # nº da tentativa (ligação ativa por cliente, em ordem de horário)
    o = s[s["outb"] & s["cod"].notna()].sort_values(["cod", "ts"]).copy()
    o["nt"] = (o.groupby("cod").cumcount() + 1).clip(upper=5)
    T = linhas(o.assign(t=1, a=o["comp"].astype(int)), ["di", "ci", "nt"], ["t", "a"])
    dados_ate = s["dt"].max()
    cl = o.groupby("cod").agg(tent=("comp", "size"), ok=("comp", "max"), ult=("ts", "max"))
    corte = dados_ate - pd.Timedelta(days=config["dias_recontato"])
    uma = cl[(cl["tent"] == 1) & (~cl["ok"]) & (cl["ult"] < corte)].index
    s2 = o[o["cod"].isin(uma)]
    S2 = [[int(a), int(c_), int(k)] for a, c_, k in s2[["di", "ci", "k"]].to_numpy()]

    # retornos pedidos pelo cliente com data sugerida já vencida
    ac = s[s["comp"] & s["analise"] & s["cod"].notna() & s["necess"] & s["sug"].notna()
           & (s["sug"] <= dados_ate) & (s["sug"] > s["dt"])].copy()
    todos = s[s["cod"].notna()][["cod", "ts", "dt"]]
    m = ac[["id", "cod", "ts", "sug"]].merge(todos, on="cod", suffixes=("", "_n"))
    m = m[m["ts_n"] > m["ts"]]
    noprazo = (m["dt"] <= m["sug"] + pd.Timedelta(days=2)).groupby(m["id"]).max()
    ac["np"] = ac["id"].map(noprazo).fillna(False).astype(bool).astype(int)
    ac["u"] = pd.cut(ac["urg"], [0, 3, 6, 10], labels=False).fillna(-1).astype(int)
    R = [[int(a), int(c_), int(k), int(u), int(n_)] for a, c_, k, u, n_ in ac[["di", "ci", "k", "u", "np"]].to_numpy()]

    # diagnóstico e sentinelas (arquivo inteiro)
    comp = s[s["comp"]]
    diag = {"linhas": int(len(s)), "dup": int(len(s) - s["id"].nunique()), "comp": int(len(comp)),
            "comp_sem_seg": int(comp["segment_id"].isna().sum()), "sem_gem": int((~comp["analise"]).sum()),
            "sem_cls": int((~comp["an"]).sum()), "sem_dur": int(comp["dur"].isna().sum()),
            "sem_cod": int(s["cod"].isna().sum()),
            "colunas_ausentes": [c for c in OPCIONAIS if c not in df.columns]}
    sent = []
    for c in CAMPOS_SENTINELA:
        if c in df.columns:
            x = df.loc[s.index, c].dropna()
            if len(x):
                sent.append({"campo": c, "pct": r6(x.isin(SENTINELAS).mean())})
    sent.sort(key=lambda r: -r["pct"])

    def ultimo(cond):
        x = s.loc[cond, "dt"]
        return x.max().strftime("%Y-%m-%d") if len(x) else None

    return {
        "meta": {"versao": VERSAO, "gerado_em": datetime.now().strftime("%Y-%m-%d %H:%M"), "linhas": int(len(s)),
                 "dados_ate": dados_ate.strftime("%Y-%m-%d"), "duracao_ate": ultimo(s["dur"].notna()),
                 "classif_ate": ultimo(s["an"]), "gpt_ate": ultimo(s["gpt"]), "gemini_ate": ultimo(s["analise"]),
                 "inicio": dias[0]},
        "config": config, "dias": dias,
        "carteiras": [{"c": c, "d": d} for c, d in cart.items()],
        "codigos": codigos, "ch_codigos": ch_codigos, "tipos": tipos, "colA": colA,
        "facetas": {"nomes": NOMES_FACETAS, "niveis": niveis},
        "A": [[int(r["di"]), int(r["ci"])] + [num(v) for v in r[colA]] for _, r in A.iterrows()],
        "CV": CV, "CH": CH, "P": P, "PI": PI, "TP": TP, "H": H, "F": F, "O": O,
        "clientes": clientes, "CL": CL, "T": T, "S2": S2, "R": R,
        "diag": diag, "sentinelas": sent, "colunas": {"usar": 46, "ressalva": 34, "nao_usar": 8},
        "uso": resumir_logs(Path(pasta_saida) / "logs"),
    }


def _data_log(linha):
    """%DATE% do Windows: dd/mm/aaaa em pt-BR (às vezes com o dia da semana antes); aceita também aaaa-mm-dd e mm/dd/aaaa."""
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", linha)
    if m:
        a, mes, d = m.groups()
    else:
        m = re.search(r"(\d{1,2})[/.-](\d{1,2})[/.-](\d{4})", linha)
        if not m:
            return None
        d, mes, a = m.groups()
        if int(mes) > 12 >= int(d):
            d, mes = mes, d
    try:
        return datetime(int(a), int(mes), int(d)).strftime("%Y-%m-%d")
    except ValueError:
        return None


def resumir_logs(pasta):
    """Lê logs/<usuario>.csv gravados pelo 'Abrir painel.bat' e devolve só contagens (sem nomes)."""
    if not pasta.is_dir():
        return None
    acessos = []
    for a in pasta.glob("*.csv"):
        try:
            with open(a, encoding="cp1252", errors="replace") as f:
                for linha in f:
                    dia = _data_log(linha)
                    if dia:
                        acessos.append((dia, a.stem.lower()))
        except OSError:
            continue
    if not acessos:
        return {"pessoas_total": 0, "acessos_total": 0, "por_dia": []}
    u = pd.DataFrame(acessos, columns=["dia", "pessoa"])
    por_dia = u.groupby("dia").agg(acessos=("pessoa", "size"), pessoas=("pessoa", "nunique")).reset_index().tail(30)
    ult7 = u[u["dia"] >= (pd.to_datetime(u["dia"]).max() - pd.Timedelta(days=6)).strftime("%Y-%m-%d")]
    return {"pessoas_total": int(u["pessoa"].nunique()), "acessos_total": int(len(u)),
            "pessoas_7d": int(ult7["pessoa"].nunique()), "acessos_7d": int(len(ult7)),
            "por_dia": por_dia.to_dict("records")}


def gravar(dados, pasta):
    pasta = Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)
    conteudo = "/* gerado por atualizar_painel.py — não editar à mão */\nwindow.PAINEL_DADOS = " + \
               json.dumps(dados, ensure_ascii=False, separators=(",", ":")) + ";\n"
    fd, tmp = tempfile.mkstemp(prefix=".dados_", suffix=".tmp", dir=pasta)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(conteudo)
    destino = pasta / "dados.js"
    os.replace(tmp, destino)
    try:
        os.chmod(destino, 0o644)
    except OSError:
        pass
    return destino, len(conteudo.encode("utf-8"))


def publicar_arquivos(pasta):
    """Copia os arquivos do painel (ARQUIVOS_PAINEL) da pasta do script para a pasta do painel quando estiverem diferentes.
    Assim, uma versão nova do painel chega a todos na próxima atualização diária."""
    copiados = []
    origem = Path(__file__).resolve().parent
    for nome in ARQUIVOS_PAINEL:
        a, b = origem / nome, Path(pasta) / nome
        if not a.is_file() or a.resolve() == b.resolve():
            continue
        novo = a.read_bytes()
        if b.is_file() and b.read_bytes() == novo:
            continue
        b.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(prefix=".copia_", suffix=".tmp", dir=b.parent)
        with os.fdopen(fd, "wb") as f:
            f.write(novo)
        os.replace(tmp, b)
        try:
            os.chmod(b, 0o644)
        except OSError:
            pass
        copiados.append(nome)
    return copiados


# --------------------------------------------------------------------------------------------------------------------
# interface
# --------------------------------------------------------------------------------------------------------------------
def escolher(cfg):
    import tkinter as tk
    from tkinter import filedialog, messagebox
    root = tk.Tk()
    root.withdraw()
    entrada = filedialog.askopenfilename(title="CSV exportado da consulta (Cancelar = escolher uma PASTA de CSVs)",
                                         initialdir=cfg.get("pasta_entrada") or str(Path.home()),
                                         filetypes=[("CSV", "*.csv"), ("Todos", "*.*")])
    if not entrada:
        entrada = filedialog.askdirectory(title="Pasta com os CSVs exportados", initialdir=cfg.get("pasta_entrada") or str(Path.home()))
    if not entrada:
        raise SystemExit("Nenhuma entrada escolhida.")
    saida = cfg.get("saida")
    if not saida or not Path(saida).is_dir() or not messagebox.askyesno("Painel", f"Gravar o painel em\n{saida}?"):
        saida = filedialog.askdirectory(title="Pasta do painel (onde estão painel.html e 'Abrir painel.bat')",
                                        initialdir=saida or str(Path.home()))
    if not saida:
        raise SystemExit("Nenhuma pasta de saída escolhida.")
    root.destroy()
    return entrada, saida


def main():
    ap = argparse.ArgumentParser(description="Atualiza o painel da venda interna (dados.js).")
    ap.add_argument("--entrada", help="CSV exportado da consulta, ou pasta com vários CSVs")
    ap.add_argument("--saida", help="pasta do painel (onde fica painel.html)")
    a = ap.parse_args()
    cfg = {}
    if CONFIG_LOCAL.exists():
        try:
            cfg = json.loads(CONFIG_LOCAL.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            cfg = {}
    config = dict(CONFIG_PAINEL)
    if CONFIG_EXTRA.exists():
        try:
            config.update(json.loads(CONFIG_EXTRA.read_text(encoding="utf-8")))
        except (OSError, ValueError) as e:
            print(f"  ATENÇÃO: {CONFIG_EXTRA.name} ignorado ({e})")
    entrada, saida = (a.entrada, a.saida) if a.entrada and a.saida else escolher(cfg)
    print(f"Lendo {entrada}")
    df = carregar(entrada)
    s, df = preparar(df)
    print(f"  {len(s):,} ligações de {s['dt'].min():%d/%m/%Y} a {s['dt'].max():%d/%m/%Y}".replace(",", "."))
    dados = construir(s, df, saida, config)
    destino, tam = gravar(dados, saida)
    copiados = publicar_arquivos(saida)
    me = dados["meta"]
    bl = s[(s["dt"] >= config["baseline_inicio"]) & (s["dt"] <= config["baseline_fim"])]
    comp = s[s["comp"] & (s["dt"] == s["dt"].max())]
    print(f"Gravado {destino} ({tam / 1024:,.0f} KB)".replace(",", "."))
    if copiados:
        print("  versão nova copiada para a pasta do painel: " + ", ".join(copiados))
    print(f"  dados até {me['dados_ate']} · duração até {me['duracao_ate']} · classificação até {me['classif_ate']}")
    if len(bl):
        br = lambda n: f"{int(n):,}".replace(",", ".")  # noqa: E731
        pct = lambda a, b_: f"{a / max(b_, 1) * 100:.1f}%".replace(".", ",")  # noqa: E731
        an, conv, opp, fe, pr = (bl[c].sum() for c in ("an", "conv", "opp", "fech", "prob"))
        res = (bl["prob"] & bl["res"].eq("SIM")).sum()
        print(f"  baseline ({config['baseline_rotulo']}): {br(an)} analisadas · {br(conv)} conversas · {br(opp)} oportunidades · "
              f"{br(fe)} fechamentos ({pct(fe, opp)}) · {br(pr)} com problema ({pct(pr, conv)}) · {br(res)} resolvidos ({pct(res, pr)})")
        print("  confira esses números com o memo da RMR antes de divulgar (devem ser iguais).")
    else:
        print(f"  ATENÇÃO: o arquivo não tem dados do período do baseline ({config['baseline_inicio']} a {config['baseline_fim']})")
    if len(comp):
        print(f"  último dia: {len(comp)} atendidas · classificadas {comp['fonte'].notna().mean():.0%} · com duração {comp['dur'].notna().mean():.0%}")
    avisos = []
    if me["duracao_ate"] and me["duracao_ate"] < me["dados_ate"]:
        avisos.append(f"duração das ligações só até {me['duracao_ate']}: indicadores de tempo param nessa data")
    if me["classif_ate"] and me["classif_ate"] < me["dados_ate"]:
        avisos.append(f"classificação só até {me['classif_ate']}: conversas, vendas e problemas param nessa data")
    for x in avisos:
        print("  ATENÇÃO: " + x)
    try:
        CONFIG_LOCAL.write_text(json.dumps({"pasta_entrada": str(Path(entrada).parent if Path(entrada).is_file() else entrada),
                                            "saida": str(saida)}, ensure_ascii=False, indent=1), encoding="utf-8")
    except OSError:
        pass


if __name__ == "__main__":
    main()
