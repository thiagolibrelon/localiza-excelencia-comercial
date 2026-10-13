"""Atualiza o painel de carga operacional (MVP em HTML): lê o CSV exportado da consulta e grava dados.js na pasta do painel.

COMO USAR (no seu computador, com Python 3 + pandas):
  python atualizar_painel.py
      sem argumentos: abre uma janela para escolher o CSV (ou a pasta com os CSVs) e outra para a pasta do painel
      (a pasta sincronizada do SharePoint, onde ficam painel.html e "Abrir painel.bat"). Lembra as escolhas para a próxima vez.
  python atualizar_painel.py --entrada "C:\\...\\Consulta Power Bi.csv" --saida "C:\\...\\Painel Carga Operacional\\Gestao"

ENTRADA: o CSV da consulta do Power BI/Excel, no MESMO formato do arquivo de setembro (88 colunas, separador ";").
  Pode ser um arquivo só (acumulado desde o início) ou uma pasta com vários CSVs: as linhas são juntadas e uma ligação
  (id_transcricao) que aparece em mais de um arquivo fica com a versão do arquivo mais recente.

SAÍDA: <pasta do painel>/dados.js — só números agregados por dia e carteira. Sem nome de vendedor, sem texto de ligação;
  o código de cliente vira um número sequencial que muda a cada atualização (serve só para contar reincidência e concentração).
  O arquivo é gravado primeiro com outro nome e renomeado no fim, para o OneDrive nunca sincronizar um arquivo pela metade.
  Se existir <pasta do painel>/logs/, os acessos registrados pelo "Abrir painel.bat" são resumidos (só contagens) no painel.

Regras de negócio: as mesmas do plano da missão e de missao_4T26/bi/ (carga operacional completa, base = classificada pelo GPT
com duração, fuso -3 h). Os números de setembro conferem com missao_4T26/bi/reconciliacao.csv.
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

VERSAO = "1.0"
FUSO_H = -3
OPERACIONAIS = ["suporte_operacional", "supporte_operacional", "cobranca", "pos_venda_manutencao", "pos_venda_sinistro",
                "duvida_contrato"]
NEGOCIACAO = ["nova_venda", "upsell", "renovacao", "retencao", "misto"]
RELACIONAMENTO = ["relacionamento_sem_demanda", "onboarding"]
SENTINELAS = {"sem dados necessários", "nenhum", "Sem Classificação", "nao_aplicavel", "NENHUM"}
CAMPOS_SENTINELA = ["volume_aluguel_concorrencia", "volume_frota_propria", "aluguel_concorrencia", "frota_propria",
                    "spin_implicacao", "data_sugerida_nova_visita", "motivo_nova_visita"]
CONFIG_PAINEL = {  # metas e limites; o baseline é PROVISÓRIO (setembro 01–22/09, régua GPT)
    "k1_baseline": 0.432, "k1_meta": 0.382, "k1_meta_piloto": 0.332, "k7_baseline": 0.351,
    "alerta_k1_pp": 10, "limite_cobertura": 0.95, "dias_uteis_mes": 21, "min_ligacoes": 40, "dias_recontato": 7,
    "baseline_texto": "Baseline provisório · setembro 01–22/09 (régua GPT)",
}
OBRIGATORIAS = ["id_transcricao", "data_visita_ev", "status", "tipo_ligacao", "codigo_cliente", "DISTRITAL", "CARTEIRA",
                "CallDurationInSeconds", "resumo_analise", "falou_tomador_decisao", "venda", "necessidade_nova_visita_boleano",
                "urgencia_nova_visita", "data_sugerida_nova_visita", "nota_spin_situacao", "nota_spin_problema",
                "nota_spin_implicacao", "nota_spin_necessidade_solucao", "categoria_principal", "fonte_classificacao",
                "p1_desfecho", "p2_tipo", "tem_problema", "p3_problema_principal", "p3_foi_resolvido_na_ligacao",
                "p5_teve_challenger", "p5_trouxe_dado", "p5_conectou_situacao", "p5_cliente_reagiu", "segment_id"]
CONFIG_LOCAL = Path(__file__).with_name("atualizar_painel_config.json")


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
        raise SystemExit("O CSV não tem as colunas esperadas (é a exportação da consulta completa, com 88 colunas?).\n"
                         "Faltam: " + ", ".join(faltam))
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


def preparar(df):
    s = pd.DataFrame(index=df.index)
    s["ts"] = data_hora(df["data_visita_ev"])
    s = s[s["ts"].notna()].copy()
    df = df.loc[s.index]
    s["dt"] = s["ts"].dt.normalize()
    s["hora"] = s["ts"].dt.hour
    s["dur"] = numero(df["CallDurationInSeconds"])
    s["comp"] = df["status"].eq("Completed")
    s["status"] = df["status"]
    s["tipo"] = df["tipo_ligacao"]
    s["carteira"] = df["CARTEIRA"].fillna("(sem carteira)")
    s["distrital"] = df["DISTRITAL"].fillna("")
    s["fonte"] = df["fonte_classificacao"]
    s["gpt"] = df["fonte_classificacao"].eq("gpt")
    s["prob"] = df["tem_problema"].eq("SIM")
    s["p2"] = df["p2_tipo"]
    s["op"] = s["prob"] | s["p2"].isin(OPERACIONAIS)
    s["tneg"] = s["p2"].isin(NEGOCIACAO)
    s["neg"] = s["tneg"] & ~s["op"]
    s["rel"] = s["p2"].isin(RELACIONAMENTO) & ~s["op"]
    s["sc"] = s["p2"].eq("sem_conteudo") & ~s["op"]
    s["base"] = s["gpt"] & s["dur"].notna()
    s["analise"] = df["resumo_analise"].notna()
    s["gem"] = s["comp"] & s["dur"].notna() & s["analise"]
    s["suporte"] = df["categoria_principal"].eq("Suporte")
    s["res"] = df["p3_foi_resolvido_na_ligacao"]
    s["cod_prob"] = df["p3_problema_principal"]
    s["pend"] = s["gpt"] & s["prob"] & s["res"].ne("SIM")
    s["fech"] = df["p1_desfecho"].fillna("").str.startswith("fechou") | booleano(df["venda"]).eq(True).fillna(False).astype(bool)
    s["ch"] = df["p5_teve_challenger"].eq("SIM")
    for k, c in (("dado", "p5_trouxe_dado"), ("con", "p5_conectou_situacao"), ("rea", "p5_cliente_reagiu")):
        s[k + "_s"] = s["gpt"] & df[c].eq("SIM")
        s[k + "_n"] = s["gpt"] & df[c].notna()
    for k, c in (("ss", "nota_spin_situacao"), ("sp", "nota_spin_problema"), ("si", "nota_spin_implicacao"),
                 ("sn", "nota_spin_necessidade_solucao")):
        s[k] = numero(df[c])
    dec = booleano(df["falou_tomador_decisao"])
    s["dec_s"] = dec.eq(True).fillna(False).astype(bool)
    s["dec_n"] = dec.notna()
    cod = df["codigo_cliente"].astype("string").str.strip()
    s["cod"] = cod.where(cod.notna() & cod.ne(""), None).str.zfill(8)
    s["necess"] = booleano(df["necessidade_nova_visita_boleano"]).eq(True).fillna(False).astype(bool)
    s["urg"] = numero(df["urgencia_nova_visita"])
    s["sug"] = pd.to_datetime(df["data_sugerida_nova_visita"], format="%d/%m/%Y", errors="coerce")
    s["id"] = df["id_transcricao"]
    s["segment_id"] = df["segment_id"]
    return s, df


# --------------------------------------------------------------------------------------------------------------------
# fatos agregados
# --------------------------------------------------------------------------------------------------------------------
def r6(x):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), 6)


def construir(s, df, pasta_saida):
    dias = sorted(s["dt"].dt.strftime("%Y-%m-%d").unique())
    di = {d: i for i, d in enumerate(dias)}
    cart = (s.groupby("carteira")["distrital"].agg(lambda x: x.mode().iat[0] if len(x.mode()) else "")).sort_index()
    ci = {c: i for i, c in enumerate(cart.index)}
    s["di"] = s["dt"].dt.strftime("%Y-%m-%d").map(di).astype(int)
    s["ci"] = s["carteira"].map(ci).astype(int)
    d0 = s["dur"].fillna(0)
    b = s["base"]

    def soma(cond, val=None):
        return (cond if val is None else val.where(cond, 0)).astype(float)

    colsA = {
        "tent": soma(pd.Series(True, index=s.index)), "atend": soma(s["comp"]), "sem_suc": soma(s["status"].eq("Sem Sucesso")),
        "open": soma(s["status"].eq("Open")), "gpt": soma(s["gpt"]),
        "base_n": soma(b), "seg_base": soma(b, d0), "seg_op": soma(b & s["op"], d0), "seg_prob": soma(b & s["prob"], d0),
        "seg_neg": soma(b & s["neg"], d0), "seg_rel": soma(b & s["rel"], d0), "seg_sc": soma(b & s["sc"], d0),
        "n_prob_base": soma(b & s["prob"]), "n_ops": soma(b & s["op"] & ~s["prob"]), "n_neg": soma(b & s["neg"]),
        "n_rel": soma(b & s["rel"]), "n_sc": soma(b & s["sc"]),
        "gem_seg": soma(s["gem"], d0), "gem_sup": soma(s["gem"] & s["suporte"], d0),
        "prob_gpt": soma(s["gpt"] & s["prob"]), "pend": soma(s["pend"]), "res_sim": soma(s["gpt"] & s["prob"] & s["res"].eq("SIM")),
        "comp_cls": soma(s["comp"] & s["fonte"].notna()), "comp_dur": soma(s["comp"] & s["dur"].notna()),
        "comp_gem": soma(s["comp"] & s["analise"]),
        "ch": soma(s["gpt"] & s["ch"]), "dado_s": soma(s["dado_s"]), "dado_n": soma(s["dado_n"]), "con_s": soma(s["con_s"]),
        "con_n": soma(s["con_n"]), "rea_s": soma(s["rea_s"]), "rea_n": soma(s["rea_n"]),
        "ss_sum": s["ss"].fillna(0), "ss_n": soma(s["ss"].notna()), "sp_sum": s["sp"].fillna(0), "sp_n": soma(s["sp"].notna()),
        "si_sum": s["si"].fillna(0), "si_n": soma(s["si"].notna()), "si_1": soma(s["si"].eq(1)),
        "sn_sum": s["sn"].fillna(0), "sn_n": soma(s["sn"].notna()), "dec_s": soma(s["dec_s"]), "dec_n": soma(s["dec_n"]),
    }
    A = pd.DataFrame(colsA)
    A["di"], A["ci"] = s["di"], s["ci"]
    A = A.groupby(["di", "ci"], as_index=False).sum()
    colA = [c for c in colsA]

    def linhas(frame, chaves, valores):
        g = frame.groupby(chaves, as_index=False)[valores].sum()
        return [[int(v) if float(v).is_integer() else round(float(v), 3) for v in row] for row in g[chaves + valores].to_numpy()]

    # faixas de duração (ligações de negociação com duração > 0)
    nz = s[s["gpt"] & s["tneg"] & (s["dur"] > 0)].copy()
    nz["faixa"] = pd.cut(nz["dur"], [0, 120, 300, 480, 720, 1e9], labels=False).astype(int)
    nz["k"] = nz["fech"].astype(int)
    nz["n"] = 1
    F = linhas(nz.assign(seg=nz["dur"]), ["di", "ci", "faixa"], ["n", "k", "seg"])

    # problemas por código
    pg = s[s["gpt"] & s["prob"]].copy()
    codigos = sorted(pg["cod_prob"].fillna("nenhum").unique(), key=lambda c: (len(c), c))
    pg["cod_i"] = pg["cod_prob"].fillna("nenhum").map({c: i for i, c in enumerate(codigos)})
    pg = pg.assign(n=1, seg=pg["dur"].where(pg["base"], 0).fillna(0), pd_=pg["pend"].astype(int),
                   sim=pg["res"].eq("SIM").astype(int), par=pg["res"].eq("PARCIAL").astype(int), nao=pg["res"].eq("NAO").astype(int))
    P = linhas(pg, ["di", "ci", "cod_i"], ["n", "seg", "pd_", "sim", "par", "nao"])

    # atendimento por hora
    H = linhas(s.assign(t=1, a=s["comp"].astype(int)), ["di", "ci", "hora"], ["t", "a"])
    # origem (base com duração)
    bb = s[b]
    O = linhas(bb.assign(tp=bb["tipo"].eq("Outbound").astype(int), n=1, p=bb["prob"].astype(int)), ["di", "ci", "tp"], ["n", "p"])

    # nº da tentativa (ligação ativa por cliente, em ordem de horário)
    o = s[s["tipo"].eq("Outbound") & s["cod"].notna()].sort_values(["cod", "ts"]).copy()
    o["nt"] = (o.groupby("cod").cumcount() + 1).clip(upper=5)
    T = linhas(o.assign(t=1, a=o["comp"].astype(int)), ["di", "ci", "nt"], ["t", "a"])
    dados_ate = s["dt"].max()
    cl = o.groupby("cod").agg(tent=("comp", "size"), ok=("comp", "max"), ult=("ts", "max"))
    corte = dados_ate - pd.Timedelta(days=CONFIG_PAINEL["dias_recontato"])
    uma = cl[(cl["tent"] == 1) & (~cl["ok"]) & (cl["ult"] < corte)].index
    S2 = linhas(o[o["cod"].isin(uma)].assign(n=1), ["di", "ci"], ["n"])

    # retornos pedidos pelo cliente com data sugerida já vencida
    ac = s[s["comp"] & s["analise"] & s["cod"].notna() & s["necess"] & s["sug"].notna()
           & (s["sug"] <= dados_ate) & (s["sug"] > s["dt"])].copy()
    todos = s[s["cod"].notna()][["cod", "ts", "dt"]]
    m = ac[["id", "cod", "ts", "sug"]].merge(todos, on="cod", suffixes=("", "_n"))
    m = m[m["ts_n"] > m["ts"]]
    noprazo = (m["dt"] <= m["sug"] + pd.Timedelta(days=2)).groupby(m["id"]).max()
    ac["np"] = ac["id"].map(noprazo).fillna(False).astype(bool).astype(int)
    ac["u"] = pd.cut(ac["urg"], [0, 3, 6, 10], labels=False).fillna(-1).astype(int)
    R = linhas(ac.assign(n=1), ["di", "ci", "u"], ["n", "np"])

    # clientes: código vira número sequencial (aleatório a cada atualização)
    cods = s["cod"].dropna().unique()
    rng = np.random.default_rng()
    perm = rng.permutation(len(cods))
    cli_i = dict(zip(cods, perm.tolist()))
    sc_ = s[s["cod"].notna()].assign(k=lambda x: x["cod"].map(cli_i), seg=d0)
    CC = linhas(sc_, ["di", "ci", "k"], ["seg"])
    cp = s[s["gpt"] & s["prob"] & s["cod"].notna()].assign(k=lambda x: x["cod"].map(cli_i), n=1)
    CP = linhas(cp, ["di", "ci", "k"], ["n"])

    # diagnóstico e sentinelas (arquivo inteiro)
    comp = s[s["comp"]]
    diag = {"linhas": int(len(s)), "dup": int(len(s) - s["id"].nunique()), "comp": int(len(comp)),
            "comp_sem_seg": int(comp["segment_id"].isna().sum()), "sem_gem": int((~comp["analise"]).sum()),
            "sem_gpt": int(comp["fonte"].isna().sum()), "sem_dur": int(comp["dur"].isna().sum()),
            "sem_cod": int(s["cod"].isna().sum()), "sem_data": 0}
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
                 "gpt_ate": ultimo(s["gpt"]), "gemini_ate": ultimo(s["analise"]), "inicio": dias[0]},
        "config": CONFIG_PAINEL, "dias": dias,
        "carteiras": [{"c": c, "d": d} for c, d in cart.items()],
        "codigos": codigos, "colA": colA,
        "A": [[int(r["di"]), int(r["ci"])] + [int(v) if float(v).is_integer() else round(float(v), 3) for v in r[colA]]
              for _, r in A.iterrows()],
        "F": F, "P": P, "H": H, "O": O, "T": T, "S2": S2, "R": R, "CC": CC, "CP": CP,
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
    """Copia painel.html e 'Abrir painel.bat' da pasta do script para a pasta do painel quando estiverem diferentes.
    Assim, uma versão nova do painel chega a todos na próxima atualização diária."""
    copiados = []
    origem = Path(__file__).resolve().parent
    for nome in ("painel.html", "Abrir painel.bat"):
        a, b = origem / nome, Path(pasta) / nome
        if not a.is_file() or a.resolve() == b.resolve():
            continue
        novo = a.read_bytes()
        if b.is_file() and b.read_bytes() == novo:
            continue
        fd, tmp = tempfile.mkstemp(prefix=".copia_", suffix=".tmp", dir=pasta)
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
    ap = argparse.ArgumentParser(description="Atualiza o painel de carga operacional (dados.js).")
    ap.add_argument("--entrada", help="CSV exportado da consulta, ou pasta com vários CSVs")
    ap.add_argument("--saida", help="pasta do painel (onde fica painel.html)")
    a = ap.parse_args()
    cfg = {}
    if CONFIG_LOCAL.exists():
        try:
            cfg = json.loads(CONFIG_LOCAL.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            cfg = {}
    entrada, saida = (a.entrada, a.saida) if a.entrada and a.saida else escolher(cfg)
    print(f"Lendo {entrada}")
    df = carregar(entrada)
    s, df = preparar(df)
    print(f"  {len(s):,} ligações de {s['dt'].min():%d/%m/%Y} a {s['dt'].max():%d/%m/%Y}".replace(",", "."))
    dados = construir(s, df, saida)
    destino, tam = gravar(dados, saida)
    copiados = publicar_arquivos(saida)
    me = dados["meta"]
    b = s[s["base"]]
    k1 = b.loc[b["op"], "dur"].sum() / b["dur"].sum() if len(b) else float("nan")
    comp = s[s["comp"] & (s["dt"] == s["dt"].max())]
    print(f"Gravado {destino} ({tam / 1024:,.0f} KB)".replace(",", "."))
    if copiados:
        print("  versão nova copiada para a pasta do painel: " + ", ".join(copiados))
    print(f"  dados até {me['dados_ate']} · duração até {me['duracao_ate']} · classificação GPT até {me['gpt_ate']}")
    print(f"  K1 (carga operacional) no arquivo inteiro: {k1:.1%}".replace(".", ","))
    if len(comp):
        print(f"  último dia: {len(comp)} atendidas · classificadas {comp['fonte'].notna().mean():.0%} · com duração {comp['dur'].notna().mean():.0%}")
    avisos = []
    if me["duracao_ate"] and me["duracao_ate"] < me["dados_ate"]:
        avisos.append(f"duração das ligações só até {me['duracao_ate']}: K1, K7 e horas não existem depois disso")
    if me["gpt_ate"] and me["gpt_ate"] < me["dados_ate"]:
        avisos.append(f"classificação GPT só até {me['gpt_ate']}")
    for x in avisos:
        print("  ATENÇÃO: " + x)
    try:
        CONFIG_LOCAL.write_text(json.dumps({"pasta_entrada": str(Path(entrada).parent if Path(entrada).is_file() else entrada),
                                            "saida": str(saida)}, ensure_ascii=False, indent=1), encoding="utf-8")
    except OSError:
        pass


if __name__ == "__main__":
    main()
