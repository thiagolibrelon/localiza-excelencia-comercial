/* =====================================================================================================================
   Painel DVINT v2 · venda interna. Lê window.PAINEL_DADOS (dados.js, gerado por atualizar_painel.py) e calcula tudo no
   navegador conforme os filtros. Gráficos: Apache ECharts (vendor/echarts.min.js, licença Apache 2.0), sem internet.
   Definições iguais às do memo da RMR (ver DICIONARIO no fim deste bloco e a página "Qualidade do dado").
   ===================================================================================================================== */
(function () {
"use strict";
const D = window.PAINEL_DADOS;
const app = document.getElementById('app');
function falha(titulo, corpo) { app.innerHTML = `<div class="erro"><h1>${titulo}</h1>${corpo}</div>`; }
const AJUDA_SYNC = `<ol><li>Abra a pasta do painel no Explorador de Arquivos.</li><li>Se os arquivos aparecerem com ícone de nuvem, clique com o botão direito na pasta → <b>Sempre manter neste dispositivo</b>.</li><li>Se o problema continuar, avise o responsável pela atualização diária.</li></ol>`;
if (!window.echarts) { falha('Não encontrei a biblioteca de gráficos', `<p>O arquivo <code>vendor/echarts.min.js</code> não está na pasta do painel ou ainda não sincronizou.</p>${AJUDA_SYNC}`); return; }
if (!D) { falha('Não encontrei os dados do painel', `<p>O arquivo <code>dados.js</code> não está na mesma pasta deste <code>painel.html</code>, ou ainda não terminou de sincronizar.</p>${AJUDA_SYNC}`); return; }
if (!D.CV || !D.CL) { falha('Os dados são de uma versão antiga do painel', `<p>O <code>dados.js</code> foi gerado pela versão ${D.meta && D.meta.versao || '1'} do script. Rode o <b>Atualizar painel.bat</b> com o <code>atualizar_painel.py</code> 2.0 ou mais novo.</p>`); return; }

/* ---------------- formatos ---------------- */
const nf = (x, d = 0) => x == null || !isFinite(x) ? '–' : Number(x).toLocaleString('pt-BR', { minimumFractionDigits: d, maximumFractionDigits: d });
const pc = (x, d = 1) => x == null || !isFinite(x) ? '–' : nf(x * 100, d) + '%';
const sinal = x => x > 0 ? '+' : x < 0 ? '−' : '';
const pp = (x, d = 1) => x == null || !isFinite(x) ? '–' : sinal(x) + nf(Math.abs(x), d) + ' p.p.';
const comp = x => x == null || !isFinite(x) ? '–' : Math.abs(x) >= 1e4 ? nf(x / 1000, Math.abs(x) >= 1e5 ? 0 : 1) + ' mil' : nf(x);
const hs = seg => seg == null || !isFinite(seg) ? '–' : nf(seg / 3600, seg / 3600 >= 100 ? 0 : 1) + ' h';
const mmss = s => s == null || !isFinite(s) ? '–' : Math.floor(s / 60) + ':' + String(Math.round(s % 60)).padStart(2, '0');
const dd = s => s ? s.slice(8, 10) + '/' + s.slice(5, 7) : '–';
const ddmmaa = s => s ? s.slice(8, 10) + '/' + s.slice(5, 7) + '/' + s.slice(0, 4) : '–';
const MESES = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez'];
const DSEM = ['dom', 'seg', 'ter', 'qua', 'qui', 'sex', 'sáb'];
const esc = s => String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const div = (a, b) => b > 0 ? a / b : null;
const soma = a => a.reduce((x, y) => x + y, 0);
const mediana = a => { const b = a.filter(v => v != null && isFinite(v)).sort((x, y) => x - y); if (!b.length) return null; const m = b.length >> 1; return b.length % 2 ? b[m] : (b[m - 1] + b[m]) / 2; };
function wilson(k, n, z = 1.96) { if (!(n > 0)) return [null, null]; const p = k / n, d = 1 + z * z / n, c = p + z * z / (2 * n), a = z * Math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)); return [Math.max(0, (c - a) / d), Math.min(1, (c + a) / d)]; }
function zprop(k1, n1, k2, n2) { if (!(n1 > 0 && n2 > 0)) return 0; const p = (k1 + k2) / (n1 + n2); const se = Math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2)); return se > 0 ? (k1 / n1 - k2 / n2) / se : 0; }
function dataMais(s, n) { const d = new Date(s + 'T12:00:00'); d.setDate(d.getDate() + n); return d.toISOString().slice(0, 10); }
function segunda(s) { const d = new Date(s + 'T12:00:00'); d.setDate(d.getDate() - (d.getDay() + 6) % 7); return d.toISOString().slice(0, 10); }
function diasEntre(a, b) { return Math.round((new Date(b + 'T12:00:00') - new Date(a + 'T12:00:00')) / 864e5); }

/* ---------------- cores (LDS, validadas para daltonismo) ---------------- */
const COR = { verde: '#018444', azul: '#3A7FC1', verm: '#D92020', vermClaro: '#EF8A8A', lima: '#5FAE1E', cinza: '#919191', cinzaClaro: '#D4D4D4',
  tinta: '#262626', tinta2: '#4A4A4A', mudo: '#6E6E6E', grade: '#EDEDED', eixo: '#BDBDBD', noite: '#003418' };
const ORD4 = ['#7CC79A', '#3FA66A', '#018444', '#00602F'];
const ORD5 = ['#7CC79A', '#4DAE76', '#1E9454', '#00753A', '#004F27'];
const SEQ = ['#F3FAF5', '#CDEBD7', '#8FD0A6', '#4DAE76', '#018444', '#004F27'];
const FONTE = getComputedStyle(document.body).fontFamily;

/* ---------------- dados ---------------- */
const DIAS = D.dias, ND = DIAS.length, CART = D.carteiras, COLA = D.colA;
/* configuração: a oficial vem do dados.js (painel_config.json do script); cada leitor pode ter ajustes pessoais (localStorage) */
const CFG_OFICIAL = Object.assign({}, D.config);
const CHAVE_CFG = 'painel_dvint_cfg', AJUSTAVEIS = ['baseline_inicio', 'baseline_fim', 'baseline_rotulo', 'min_ligacoes', 'min_n_taxa', 'limite_cobertura'];
let CFG_PESSOAL = {};
try { const g = JSON.parse(localStorage.getItem(CHAVE_CFG) || 'null'); if (g && typeof g === 'object') AJUSTAVEIS.forEach(k => { if (k in g) CFG_PESSOAL[k] = g[k]; }); } catch (e) { /* sem armazenamento */ }
const CFG = Object.assign({}, CFG_OFICIAL, CFG_PESSOAL);
function aplicaCfg(novo) {
  CFG_PESSOAL = novo; AJUSTAVEIS.forEach(k => { CFG[k] = k in novo ? novo[k] : CFG_OFICIAL[k]; });
  try { if (Object.keys(novo).length) localStorage.setItem(CHAVE_CFG, JSON.stringify(novo)); else localStorage.removeItem(CHAVE_CFG); } catch (e) { /* sem armazenamento */ }
}
const basePessoal = () => CFG.baseline_inicio !== CFG_OFICIAL.baseline_inicio || CFG.baseline_fim !== CFG_OFICIAL.baseline_fim;
const IA = {}; COLA.forEach((c, i) => IA[c] = i + 2);
const DIST = [...new Set(CART.map(c => c.d).filter(Boolean))].sort();
const DOWI = DIAS.map(d => new Date(d + 'T12:00:00').getDay());
const NOMES_P = { P1: 'Acesso/sistema', P2: 'Faturamento/cobrança', P3: 'Multa/infração', P4: 'Manutenção/substituto', P5: 'Condutor/cadastro', P6: 'Km excedente', P7: 'Disponibilidade', P8: 'Franquia/agência', P9: 'Sinistro', P10: 'Reserva/sistema', P11: 'Outro', P12: 'Manipulação de pesquisa/NPS', P13: 'Crédito/cadastro PJ', P14: 'Preço/competitividade', P15: 'Tag de pedágio', nenhum: 'Sem código' };
const NOMES_CH = { CH1: 'Custo oculto revelado', CH2: 'ROI calculado', CH3: 'Urgência por regra real', CH4: 'Concorrente superado com dado', CH5: 'Dor revelada → produto', CH6: 'Antecipação de problema', CH7: 'Necessidade não declarada' };
const NOMES_TIPO = { relacionamento_sem_demanda: 'Relacionamento sem demanda', sem_conteudo: 'Sem conteúdo', nova_venda: 'Nova venda', suporte_operacional: 'Suporte operacional', supporte_operacional: 'Suporte operacional', renovacao: 'Renovação', cobranca: 'Cobrança', misto: 'Misto', duvida_contrato: 'Dúvida de contrato', onboarding: 'Onboarding', upsell: 'Upsell', pos_venda_manutencao: 'Pós-venda manutenção', retencao: 'Retenção', pos_venda_sinistro: 'Pós-venda sinistro' };
const GRUPO_TIPO = t => ['suporte_operacional', 'supporte_operacional', 'cobranca', 'pos_venda_manutencao', 'pos_venda_sinistro', 'duvida_contrato'].includes(t) ? 'op' : ['nova_venda', 'upsell', 'renovacao', 'retencao', 'misto'].includes(t) ? 'neg' : ['relacionamento_sem_demanda', 'onboarding'].includes(t) ? 'rel' : 'sc';
const nomeCod = c => c === 'nenhum' ? 'Sem código' : `${c} · ${NOMES_P[c] || c}`;

/* ---------------- dicionário (definições exibidas no ⓘ e na página de qualidade) ---------------- */
const DIC = {
  tent: ['Ligações (tentativas)', 'Todas as tentativas registradas, atendidas ou não.', 'linhas do CSV'],
  atend: ['Taxa de atendimento', 'Tentativas com status Completed ÷ tentativas.', 'status'],
  an: ['Ligações analisadas', 'Ligações que o classificador analisou (têm fonte de classificação).', 'fonte_classificacao'],
  conv: ['Conversas', 'Ligações analisadas que tiveram conversa (tipo diferente de "sem conteúdo").', 'p2_tipo'],
  opp: ['Oportunidades de venda', 'Interações classificadas como venda: desfecho diferente de "não era venda".', 'p1_desfecho'],
  fech: ['Taxa de fechamento', 'Fechamentos (desfecho "fechou …") ÷ oportunidades de venda. É o fechamento identificado na conversa, não no CRM.', 'p1_desfecho'],
  inter: ['Interessou e não fechou', 'Oportunidades com desfecho "interessou, não fechou" ÷ oportunidades.', 'p1_desfecho'],
  tc: ['Tentativa comercial', 'Conversas em que o vendedor tentou vender ÷ conversas.', 'p1_tentativa_comercial'],
  prob: ['Conversas com problema', 'Conversas em que o cliente trouxe um problema ÷ conversas.', 'tem_problema'],
  res: ['Resolvidos na ligação', 'Problemas resolvidos totalmente na própria ligação ÷ problemas.', 'p3_foi_resolvido_na_ligacao'],
  pend: ['Pendências', 'Problemas não resolvidos totalmente na ligação (parcial ou não).', 'p3_foi_resolvido_na_ligacao'],
  k5: ['Reincidência', 'Problemas de clientes que trouxeram 2 ou mais problemas no período ÷ problemas.', 'codigo_cliente'],
  k1: ['Carga operacional (tempo)', 'Tempo em ligações com problema, suporte, cobrança, pós-venda ou dúvida de contrato ÷ tempo das ligações classificadas pelo GPT com duração.', 'CallDurationInSeconds, p2_tipo, tem_problema'],
  k1gem: ['Carga operacional · régua Gemini', 'Tempo das ligações com categoria Suporte ÷ tempo das atendidas com análise Gemini e duração.', 'categoria_principal'],
  horas: ['Horas de conversa', 'Soma da duração das ligações classificadas pelo GPT com duração.', 'CallDurationInSeconds'],
  tma: ['Tempo médio (TMA)', 'Duração média das ligações classificadas com duração.', 'CallDurationInSeconds'],
  k3: ['Horas excedentes', 'Ligações com problema × (TMA com problema − TMA sem problema).', 'CallDurationInSeconds'],
  ch: ['Teve Challenger', 'Conversas com abordagem Challenger ÷ conversas.', 'p5_teve_challenger'],
  chAlta: ['Challenger de alta qualidade', 'Conversas com Challenger de qualidade alta ÷ conversas.', 'p5_qualidade'],
  dado: ['Trouxe dado', 'Conversas em que o vendedor trouxe um dado ao cliente ÷ conversas avaliadas.', 'p5_trouxe_dado'],
  con: ['Conectou à situação', 'Conversas em que o dado foi conectado à situação do cliente ÷ conversas avaliadas.', 'p5_conectou_situacao'],
  rea: ['Cliente reagiu', 'Conversas em que o cliente reagiu ao dado ÷ conversas avaliadas.', 'p5_cliente_reagiu'],
  sf: ['SPIN · nota final', 'Média da nota final SPIN (1 a 5) das ligações com análise.', 'nota_final_spin'],
  si: ['SPIN · Implicação', 'Média da nota de Implicação (1 a 5).', 'nota_spin_implicacao'],
  si1: ['Implicação com nota 1', 'Análises com nota 1 em Implicação ÷ análises com nota.', 'nota_spin_implicacao'],
  dec: ['Falou com o decisor', 'Análises em que o vendedor falou com quem decide ÷ análises.', 'falou_tomador_decisao'],
  c1: ['Cobertura de classificação', 'Atendidas com classificação ÷ atendidas. Meta ≥ 95%.', 'fonte_classificacao'],
  c2: ['Cobertura de duração', 'Atendidas com duração ÷ atendidas. Meta ≥ 95%.', 'CallDurationInSeconds'],
  cli: ['Clientes contatados', 'Códigos de cliente distintos com ao menos uma tentativa no período.', 'codigo_cliente'],
  s2: ['Sem 2ª tentativa', `Clientes com uma única tentativa ativa, sem sucesso, e nenhuma outra há ${CFG.dias_recontato} dias ou mais.`, 'tipo_ligacao, status'],
  ret: ['Retornos no prazo', 'Retornos pedidos pelo cliente com data já vencida que tiveram nova ligação até 2 dias depois da data.', 'necessidade_nova_visita, data_sugerida_nova_visita'],
};
const info = k => DIC[k] ? `<button class="info" type="button" title="${esc(DIC[k][1])}" aria-label="${esc(DIC[k][0] + ': ' + DIC[k][1])}">i</button>` : '';

/* ---------------- estado ---------------- */
const CHAVE = 'painel_dvint_v2';
const PADRAO = { pag: 'geral', preset: 'mes', d0: 0, d1: ND - 1, comp: 'base', gran: 'dia', dist: '', cart: '', cod: '', faceta: 0,
  metrica: 'fech', pareto: 'n', filtroCli: 'todos', simCod: 'P1', simPct: 30, metCart: 'k1', metDist: 'fech' };
let S = Object.assign({}, PADRAO);
try { const g = JSON.parse(localStorage.getItem(CHAVE) || 'null'); if (g && typeof g === 'object') S = Object.assign(S, g); } catch (e) { /* sem armazenamento */ }
function salvar() { try { localStorage.setItem(CHAVE, JSON.stringify(S)); } catch (e) { /* sem armazenamento */ } }
const idxDe = s => { const i = DIAS.findIndex(d => d >= s); return i < 0 ? ND : i; };
const idxAte = s => { let i = ND - 1; while (i >= 0 && DIAS[i] > s) i--; return i; };
const presets = () => [['mes', 'Mês do último dado'], ['mesAnt', 'Mês anterior'], ['d7', 'Últimos 7 dias'], ['d30', 'Últimos 30 dias'], ['base', 'Baseline (' + CFG.baseline_rotulo + ')'], ['tudo', 'Tudo'], ['pers', 'Personalizado']];
function aplicaPreset(p) {
  const ult = DIAS[ND - 1];
  if (p === 'tudo') { S.d0 = 0; S.d1 = ND - 1; }
  else if (p === 'mes') { S.d0 = idxDe(ult.slice(0, 7) + '-01'); S.d1 = ND - 1; }
  else if (p === 'mesAnt') { const m = new Date(ult.slice(0, 7) + '-01T12:00:00'); m.setMonth(m.getMonth() - 1); const ini = m.toISOString().slice(0, 7) + '-01'; m.setMonth(m.getMonth() + 1); m.setDate(0); S.d0 = idxDe(ini); S.d1 = idxAte(m.toISOString().slice(0, 10)); }
  else if (p === 'd7' || p === 'd30') { S.d0 = idxDe(dataMais(ult, -(p === 'd7' ? 6 : 29))); S.d1 = ND - 1; }
  else if (p === 'base') { S.d0 = idxDe(CFG.baseline_inicio); S.d1 = idxAte(CFG.baseline_fim); }
  if (S.d0 > S.d1 || S.d0 >= ND) { S.d0 = 0; S.d1 = ND - 1; }
}
function normaliza() {
  if (S.preset !== 'pers') aplicaPreset(S.preset);
  S.d0 = Math.max(0, Math.min(ND - 1, S.d0 | 0)); S.d1 = Math.max(S.d0, Math.min(ND - 1, S.d1 | 0));
  if (S.cart && !CART.some(c => c.c === S.cart)) S.cart = '';
  if (S.dist && !DIST.includes(S.dist)) S.dist = '';
  if (S.cod && !D.codigos.includes(S.cod)) S.cod = '';
}
normaliza();

/* ---------------- seleção e somas (com memória por atualização) ---------------- */
let MEMO = new Map();
const okCart = (ci, semCart) => { const c = CART[ci]; return (!S.dist || c.d === S.dist) && (semCart || !S.cart || c.c === S.cart); };
function sel(bloco, r0 = S.d0, r1 = S.d1, semCart = false) {
  const k = bloco + '|' + r0 + '|' + r1 + '|' + semCart + '|' + S.dist + '|' + S.cart;
  if (MEMO.has(k)) return MEMO.get(k);
  const out = (D[bloco] || []).filter(r => r[0] >= r0 && r[0] <= r1 && okCart(r[1], semCart));
  MEMO.set(k, out); return out;
}
function somaA(rows) {
  const n = COLA.length, t = new Float64Array(n); const ds = new Set();
  for (const r of rows) { ds.add(r[0]); for (let i = 0; i < n; i++) t[i] += r[i + 2]; }
  const o = { _dias: ds.size }; COLA.forEach((c, i) => o[c] = t[i]); return o;
}
function agrupa(rows, f) { const m = new Map(); for (const r of rows) { const k = f(r); let a = m.get(k); if (!a) m.set(k, a = []); a.push(r); } return m; }

/* ---------------- métricas ---------------- */
const MET = {
  at: { nome: 'Taxa de atendimento', num: 'atend', den: 'tent', bom: 1, dic: 'atend' },
  opp: { nome: 'Oportunidades por conversa', num: 'opp', den: 'conv', bom: 1, dic: 'opp' },
  fech: { nome: 'Taxa de fechamento', num: 'fech', den: 'opp', bom: 1, dic: 'fech' },
  fechConv: { nome: 'Fechamentos por conversa', num: 'fech', den: 'conv', bom: 1, dic: 'fech' },
  inter: { nome: 'Interessou e não fechou', num: 'inter', den: 'opp', bom: 0, dic: 'inter' },
  tc: { nome: 'Tentativa comercial', num: 'tc_s', den: 'tc_n', bom: 1, dic: 'tc' },
  prob: { nome: 'Conversas com problema', num: 'prob', den: 'conv', bom: -1, dic: 'prob' },
  res: { nome: 'Resolvidos na ligação', num: 'res_sim', den: 'prob', bom: 1, dic: 'res' },
  k1: { nome: 'Carga operacional (tempo)', num: 'seg_op', den: 'seg_base', n: 'base_n', bom: -1, dic: 'k1' },
  k1gem: { nome: 'Carga operacional · Gemini', num: 'gem_sup', den: 'gem_seg', n: 'comp_gem', bom: -1, dic: 'k1gem' },
  k7: { nome: 'Tempo em negociação', num: 'seg_neg', den: 'seg_base', n: 'base_n', bom: 1, dic: 'k1' },
  ch: { nome: 'Teve Challenger', num: 'ch', den: 'conv', bom: 1, dic: 'ch' },
  chAlta: { nome: 'Challenger alta qualidade', num: 'ch_alta', den: 'conv', bom: 1, dic: 'chAlta' },
  dado: { nome: 'Trouxe dado', num: 'dado_s', den: 'dado_n', bom: 1, dic: 'dado' },
  con: { nome: 'Conectou à situação', num: 'con_s', den: 'con_n', bom: 1, dic: 'con' },
  rea: { nome: 'Cliente reagiu', num: 'rea_s', den: 'rea_n', bom: 1, dic: 'rea' },
  si1: { nome: 'Implicação com nota 1', num: 'si1', den: 'si_n', bom: -1, dic: 'si1' },
  dec: { nome: 'Falou com o decisor', num: 'dec_s', den: 'dec_n', bom: 1, dic: 'dec' },
  c1: { nome: 'Cobertura de classificação', num: 'comp_cls', den: 'atend', bom: 1, dic: 'c1' },
  c2: { nome: 'Cobertura de duração', num: 'comp_dur', den: 'atend', bom: 1, dic: 'c2' },
  outb: { nome: 'Ligações ativas', num: 'outb', den: 'tent', bom: 0 },
};
const MEDIAS = { sf: ['sf_sum', 'sf_n'], ss: ['ss_sum', 'ss_n'], sp: ['sp_sum', 'sp_n'], si: ['si_sum', 'si_n'], sn: ['sn_sum', 'sn_n'], tma: ['seg_base', 'base_n'] };
const tx = (t, k) => { const m = MET[k]; return div(t[m.num], t[m.den]); };
const media = (t, k) => div(t[MEDIAS[k][0]], t[MEDIAS[k][1]]);
const nEf = (t, k) => { const m = MET[k]; return m.n ? t[m.n] : t[m.den]; };
function k3(t) { const a = div(t.seg_prob, t.n_prob_base), b = div(t.seg_base - t.seg_prob, t.base_n - t.n_prob_base); return a != null && b != null ? t.n_prob_base * (a - b) / 3600 : null; }

/* ---------------- comparação (baseline ou período anterior) ---------------- */
function janelaComp() {
  if (S.comp === 'base') { const a = idxDe(CFG.baseline_inicio), b = idxAte(CFG.baseline_fim); return a <= b && a < ND ? { r0: a, r1: b, rot: 'baseline (' + CFG.baseline_rotulo + (basePessoal() ? ', pessoal' : '') + ')', curto: 'baseline' } : null; }
  if (S.comp === 'ant') { const n = diasEntre(DIAS[S.d0], DIAS[S.d1]) + 1; const fim = dataMais(DIAS[S.d0], -1), ini = dataMais(fim, -(n - 1)); const a = idxDe(ini), b = idxAte(fim); return a <= b && a < ND && b >= 0 ? { r0: a, r1: b, rot: 'período anterior (' + dd(DIAS[a]) + '–' + dd(DIAS[b]) + ')', curto: 'anterior' } : null; }
  return null;
}
/* delta de uma taxa: p.p., significância (z de duas proporções) e se é bom ou ruim */
function deltaTaxa(k, t, tc) {
  if (!tc) return null; const m = MET[k]; const a = tx(t, k), b = tx(tc, k); if (a == null || b == null) return null;
  const n1 = nEf(t, k), n2 = nEf(tc, k); const z = m.n ? zprop(a * n1, n1, b * n2, n2) : zprop(t[m.num], t[m.den], tc[m.num], tc[m.den]);
  const sig = Math.abs(z) >= 1.96; const d = (a - b) * 100;
  return { d, txt: pp(d), sig, classe: !sig || !m.bom ? 'neutro' : (d * m.bom > 0 ? 'bom' : 'ruim'), base: b };
}
function deltaVolume(v, vc, dias, diasC, bom = 1) {
  if (vc == null || !(diasC > 0) || !(dias > 0)) return null; const a = v / dias, b = vc / diasC; if (!(b > 0)) return null;
  const r = a / b - 1; const sig = Math.abs(r) >= 0.1;
  return { d: r, txt: sinal(r) + nf(Math.abs(r) * 100, 0) + '% /dia', sig, classe: !sig || !bom ? 'neutro' : (r * bom > 0 ? 'bom' : 'ruim') };
}
function deltaMedia(a, b, bom, casas = 2, lim = 0.1) {
  if (a == null || b == null) return null; const d = a - b; const sig = Math.abs(d) >= lim;
  return { d, txt: sinal(d) + nf(Math.abs(d), casas), sig, classe: !sig || !bom ? 'neutro' : (d * bom > 0 ? 'bom' : 'ruim') };
}
const seta = d => d.classe === 'neutro' ? '≈' : d.d > 0 ? '▲' : '▼';
function chipDelta(d, rot) {
  if (!d) return ''; const titulo = d.sig ? `diferença contra ${rot}` : `diferença contra ${rot} dentro da margem de erro`;
  return `<span class="delta ${d.classe}" title="${esc(titulo)}">${seta(d)} ${d.txt}</span>`;
}

/* ---------------- tempo agrupado (dia, semana ou mês) ---------------- */
const chaveBalde = i => S.gran === 'dia' ? DIAS[i] : S.gran === 'semana' ? segunda(DIAS[i]) : DIAS[i].slice(0, 7);
function rotBalde(k) {
  if (S.gran === 'mes') return MESES[+k.slice(5, 7) - 1] + '/' + k.slice(2, 4);
  if (S.gran === 'semana') return 'sem ' + dd(k);
  return dd(k);
}
function porBalde(rows) { const m = agrupa(rows, r => chaveBalde(r[0])); return [...m.keys()].sort().map(k => ({ k, rot: rotBalde(k), rows: m.get(k) })); }

/* ---------------- gráficos ---------------- */
const ro = new ResizeObserver(es => { for (const e of es) { const g = echarts.getInstanceByDom(e.target); if (g) g.resize(); } });
function g(id) {
  const el = document.getElementById('g-' + id); if (!el) return null;
  let c = echarts.getInstanceByDom(el);
  if (!c) { c = echarts.init(el, null, { locale: 'PT-br' }); ro.observe(el); }
  return c;
}
function descartar(container) { container.querySelectorAll('.grafico,.spark').forEach(el => { const c = echarts.getInstanceByDom(el); if (c) { ro.unobserve(el); c.dispose(); } }); }
const TT = { backgroundColor: '#fff', borderColor: '#E6E6E6', borderWidth: 1, padding: [8, 11], textStyle: { color: COR.tinta, fontSize: 12.5, fontFamily: FONTE }, extraCssText: 'box-shadow:0 6px 18px rgba(0,0,0,.12);border-radius:8px;', confine: true };
function base(extra) {
  return Object.assign({
    textStyle: { fontFamily: FONTE, color: COR.tinta2 }, animationDuration: 500, animationDurationUpdate: 450, animationEasingUpdate: 'cubicOut',
    aria: { enabled: true }, grid: { left: 6, right: 18, top: 30, bottom: 6, containLabel: true },
  }, extra);
}
const eixoCat = (data, extra = {}) => Object.assign({ type: 'category', data, axisLine: { lineStyle: { color: COR.eixo } }, axisTick: { show: false }, axisLabel: { color: COR.mudo, fontSize: 11.5, hideOverlap: true } }, extra);
const eixoVal = (fmt, extra = {}) => Object.assign({ type: 'value', splitLine: { lineStyle: { color: COR.grade } }, axisLabel: { color: COR.mudo, fontSize: 11.5, formatter: fmt } }, extra);
const fmtPc0 = v => nf(v * 100, 0) + '%';
/* tooltip: valor em destaque, rótulo depois; chave em forma de traço */
function ttLinha(cor, rot, val, extra) { return `<div style="display:flex;gap:8px;align-items:center;margin-top:3px"><span style="width:12px;height:3px;border-radius:2px;background:${cor};display:inline-block"></span><b style="font-weight:650">${val}</b><span style="color:${COR.mudo}">${esc(rot)}${extra ? ' · ' + extra : ''}</span></div>`; }
const ttTitulo = t => `<div style="font-weight:600;margin-bottom:2px">${esc(t)}</div>`;
function linhaRef(valor, rot, cor = COR.cinza) { return { silent: true, symbol: 'none', lineStyle: { color: cor, type: [5, 4], width: 1.4 }, label: { formatter: rot, color: COR.tinta2, fontSize: 11, position: 'insideStartTop', textBorderColor: '#fff', textBorderWidth: 3 }, data: [{ yAxis: valor }] }; }
const barra = (extra = {}) => Object.assign({ type: 'bar', barMaxWidth: 24, itemStyle: { borderRadius: [4, 4, 0, 0] }, emphasis: { focus: 'none', itemStyle: { opacity: .85 } } }, extra);
const linha = (extra = {}) => Object.assign({ type: 'line', symbol: 'circle', symbolSize: 7, showSymbol: false, lineStyle: { width: 2 }, emphasis: { scale: 1.4 } }, extra);
/* tabela de dados equivalente a cada gráfico (botão "Tabela" e "CSV") */
const TABDADOS = {};
function registra(id, colunas, linhas) { TABDADOS[id] = { colunas, linhas }; const t = document.getElementById('t-' + id); if (t && !t.hidden) desenhaTabDados(id); }
function desenhaTabDados(id) {
  const t = document.getElementById('t-' + id), d = TABDADOS[id]; if (!t || !d) return;
  t.innerHTML = `<div class="tab-wrap" style="max-height:${Math.max(220, (document.getElementById('g-' + id) || {}).offsetHeight || 280)}px"><table class="tb"><thead><tr>${d.colunas.map((c, i) => `<th class="${i ? '' : 'txt'}">${esc(c)}</th>`).join('')}</tr></thead><tbody>${d.linhas.map(l => `<tr>${l.map((v, i) => `<td class="${i ? '' : 'txt'}">${esc(v)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>`;
}
function baixarCSV(nome, colunas, linhas) {
  const q = v => { const s = String(v == null ? '' : v); return /[;"\n]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s; };
  const txt = '﻿' + [colunas, ...linhas].map(l => l.map(q).join(';')).join('\r\n');
  const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([txt], { type: 'text/csv;charset=utf-8' })); a.download = nome + '.csv'; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500);
}
function baixarPNG(id, nome) { const c = g(id); if (!c) return; const a = document.createElement('a'); a.href = c.getDataURL({ pixelRatio: 2, backgroundColor: '#fff' }); a.download = nome + '.png'; document.body.appendChild(a); a.click(); a.remove(); }

/* ---------------- componentes HTML ---------------- */
function card(id, cls, titulo, sub, altura, extra = '') {
  return `<section class="card ${cls}" id="card-${id}"><div class="card-cab"><div><h2>${titulo}</h2>${sub ? `<p id="s-${id}">${sub}</p>` : ''}</div><div class="acoes"><button type="button" data-acao="tabela" data-id="${id}" aria-pressed="false">Tabela</button><button type="button" data-acao="png" data-id="${id}">PNG</button><button type="button" data-acao="csv" data-id="${id}">CSV</button></div></div>${extra}<div class="grafico" id="g-${id}" style="height:${altura}px" role="img" aria-label="${esc(titulo)}"></div><div class="vazio" id="v-${id}" hidden></div><div id="t-${id}" hidden></div><div class="nota" id="n-${id}"></div></section>`;
}
function cardHtml(id, cls, titulo, sub, extra = '') {
  return `<section class="card ${cls}" id="card-${id}"><div class="card-cab"><div><h2>${titulo}</h2>${sub ? `<p id="s-${id}">${sub}</p>` : ''}</div></div>${extra}<div id="h-${id}"></div><div class="nota" id="n-${id}"></div></section>`;
}
const html = (id, v) => { const el = document.getElementById(id); if (el) el.innerHTML = v; };
const texto = (id, v) => { const el = document.getElementById(id); if (el) el.textContent = v; };
/* cartão de indicador com minigráfico */
function kpis(lista) { const n = lista.length, c = n <= 6 ? n : Math.ceil(n / 2); return `<div class="kpis" style="--c:${c}">${lista.map(k => `<div class="kpi${k.ir ? ' link' : ''}" id="k-${k.id}" ${k.ir ? `data-ir="${k.ir}" tabindex="0" role="link"` : ''}><div class="lab"><span>${k.nome}</span>${info(k.dic || k.id)}</div><div class="val" id="kv-${k.id}">–</div><div class="linha"><span id="kd-${k.id}"></span></div><div class="sub" id="ks-${k.id}"></div><div class="spark" id="kp-${k.id}"></div></div>`).join('')}</div>`; }
function kpi(id, valor, delta, sub, serie, cor = COR.verde, fmt = v => v) {
  texto('kv-' + id, valor); html('kd-' + id, delta || ''); html('ks-' + id, sub || '');
  const el = document.getElementById('kp-' + id); if (!el) return;
  if (!serie || serie.length < 2) { const c0 = echarts.getInstanceByDom(el); if (c0) c0.clear(); return; }
  let c = echarts.getInstanceByDom(el); if (!c) { c = echarts.init(el, null, { locale: 'PT-br' }); ro.observe(el); }
  c.setOption({ animationDurationUpdate: 400, grid: { left: 4, right: 4, top: 4, bottom: 2 }, xAxis: { type: 'category', show: false, data: serie.map(s => s.rot) }, yAxis: { type: 'value', show: false, scale: true },
    tooltip: Object.assign({}, TT, { trigger: 'axis', padding: [4, 8], formatter: p => `${esc(p[0].name)}: <b>${p[0].value == null ? '–' : fmt(p[0].value)}</b>`, axisPointer: { type: 'line', lineStyle: { color: COR.eixo } } }),
    series: [{ type: 'line', data: serie.map(s => s.v), symbol: 'none', smooth: false, connectNulls: false, lineStyle: { width: 1.6, color: cor }, areaStyle: { color: cor, opacity: .08 } }] }, true);
}
/* tabela ordenável com busca, exportação e paginação */
const TAB = {};
function tabela(el, o) {
  if (!el) return; const st = TAB[o.id] || (TAB[o.id] = { ord: o.ord || null, asc: !!o.asc, busca: '', lim: o.limite || 100 });
  el.__o = o;
  let linhas = o.linhas;
  if (st.busca) { const b = st.busca.toLowerCase(); linhas = linhas.filter(l => o.colunas.some(c => c.busca && String(l[c.k] == null ? '' : l[c.k]).toLowerCase().includes(b))); }
  if (st.ord) { const c = o.colunas.find(x => x.k === st.ord); if (c) linhas = [...linhas].sort((a, b) => { const x = a[st.ord], y = b[st.ord]; const nx = x == null || (typeof x === 'number' && !isFinite(x)), ny = y == null || (typeof y === 'number' && !isFinite(y)); if (nx || ny) return nx - ny; const r = typeof x === 'string' ? String(x).localeCompare(String(y)) : (x - y); return st.asc ? r : -r; }); }
  const vis = linhas.slice(0, st.lim);
  const fmt = (c, l) => { const v = l[c.k]; const t = c.f ? c.f(v, l) : esc(v == null ? '–' : v); if (c.barra && v != null && isFinite(v)) { const mx = c.barra === true ? Math.max(1e-9, ...linhas.map(x => x[c.k] || 0)) : c.barra; return `<span class="barra-cel"><span>${t}</span><i style="width:${Math.max(2, Math.min(60, v / mx * 60))}px;background:${c.cor || COR.verde}"></i></span>`; } return t; };
  el.innerHTML = `<div class="tab-barra">${o.busca !== false ? `<input type="search" placeholder="${esc(o.placeholder || 'Buscar')}" value="${esc(st.busca)}" data-tab-busca aria-label="Buscar na tabela">` : ''}${o.botoes || ''}<span class="cont">${nf(linhas.length)} ${o.unidade || 'linhas'}${linhas.length > vis.length ? ` · mostrando ${nf(vis.length)}` : ''}</span><button type="button" class="pilula" data-tab-csv>Baixar CSV</button></div>
  <div class="tab-wrap" style="max-height:${o.altura || 520}px"><table class="tb"><thead><tr>${o.colunas.map(c => `<th class="${c.txt ? 'txt' : ''}" data-tab-ord="${c.k}" title="${esc(c.dica || 'Ordenar')}">${esc(c.t)}${st.ord === c.k ? `<span class="seta">${st.asc ? '▲' : '▼'}</span>` : ''}</th>`).join('')}</tr></thead>
  <tbody>${vis.map(l => `<tr class="${o.clique ? 'clic' : ''} ${o.sel && o.sel(l) ? 'sel' : ''} ${o.fraco && o.fraco(l) ? 'fraco' : ''}" ${o.clique ? `data-tab-linha="${esc(l[o.chave])}" tabindex="0"` : ''}>${o.colunas.map(c => `<td class="${c.txt ? 'txt' : ''}"${c.quebra ? ' style="white-space:normal;min-width:150px"' : ''}>${fmt(c, l)}</td>`).join('')}</tr>`).join('')}</tbody></table></div>
  ${linhas.length > vis.length ? `<button type="button" class="mais" data-tab-mais>Mostrar mais ${nf(Math.min(100, linhas.length - vis.length))}</button>` : ''}`;
  el.__linhas = linhas;
  if (!el.__ligado) {
    el.__ligado = true;
    el.addEventListener('click', ev => {
      const o2 = el.__o, st2 = TAB[o2.id];
      const th = ev.target.closest('[data-tab-ord]'); if (th) { const k = th.dataset.tabOrd; if (st2.ord === k) st2.asc = !st2.asc; else { st2.ord = k; st2.asc = !!(o2.colunas.find(c => c.k === k) || {}).txt; } tabela(el, o2); return; }
      if (ev.target.closest('[data-tab-mais]')) { st2.lim += 100; tabela(el, o2); return; }
      if (ev.target.closest('[data-tab-csv]')) { baixarCSV(o2.id, o2.colunas.map(c => c.t), el.__linhas.map(l => o2.colunas.map(c => c.csv ? c.csv(l[c.k], l) : l[c.k]))); return; }
      const tr = ev.target.closest('[data-tab-linha]'); if (tr && o2.clique) o2.clique(tr.dataset.tabLinha);
    });
    el.addEventListener('keydown', ev => { const tr = ev.target.closest('[data-tab-linha]'); if (tr && (ev.key === 'Enter' || ev.key === ' ') && el.__o.clique) { ev.preventDefault(); el.__o.clique(tr.dataset.tabLinha); } });
    el.addEventListener('input', ev => { if (ev.target.matches('[data-tab-busca]')) { const st2 = TAB[el.__o.id]; st2.busca = ev.target.value; st2.lim = el.__o.limite || 100; const pos = ev.target.selectionStart; tabela(el, el.__o); const i = el.querySelector('[data-tab-busca]'); if (i) { i.focus(); i.setSelectionRange(pos, pos); } } });
  }
}

/* =====================================================================================================================
   PÁGINAS
   ===================================================================================================================== */
function pinta(id, opt) { cheio(id); const c = g(id); if (c) c.setOption(opt, { replaceMerge: ['series', 'xAxis', 'yAxis', 'visualMap', 'grid', 'legend'] }); return c; }
function vazioGrafico(id, msg) {
  const el = document.getElementById('g-' + id); if (el) { const c = echarts.getInstanceByDom(el); if (c) c.clear(); el.style.display = 'none'; }
  const n = document.getElementById('v-' + id); if (n) { n.hidden = false; n.textContent = msg; }
  TABDADOS[id] = { colunas: ['—'], linhas: [] };
}
function cheio(id) {
  const n = document.getElementById('v-' + id); if (n) n.hidden = true;
  const el = document.getElementById('g-' + id); const t = document.getElementById('t-' + id);
  if (el && el.style.display === 'none' && !(t && !t.hidden)) { el.style.display = ''; const c = echarts.getInstanceByDom(el); if (c) c.resize(); }
}
function errorBar(params, api) {
  const x = api.value(0), lo = api.coord([x, api.value(1)]), hi = api.coord([x, api.value(2)]), w = 5, st = { stroke: COR.tinta, lineWidth: 1.2 };
  return { type: 'group', children: [{ type: 'line', shape: { x1: lo[0], y1: lo[1], x2: hi[0], y2: hi[1] }, style: st }, { type: 'line', shape: { x1: lo[0] - w, y1: lo[1], x2: lo[0] + w, y2: lo[1] }, style: st }, { type: 'line', shape: { x1: hi[0] - w, y1: hi[1], x2: hi[0] + w, y2: hi[1] }, style: st }] };
}
const nomeMet = k => (MET[k] && MET[k].nome) || (DIC[k] && DIC[k][0]) || k;
function pilulas(grupo, opcoes, atual) { return `<div class="controles" role="group">${opcoes.map(([v, t]) => `<button type="button" class="pilula${String(v) === String(atual) ? ' on' : ''}" data-pil="${grupo}" data-v="${esc(v)}" aria-pressed="${String(v) === String(atual)}">${esc(t)}</button>`).join('')}</div>`; }
function marcaPilulas(grupo, atual) { document.querySelectorAll(`[data-pil="${grupo}"]`).forEach(b => { const on = b.dataset.v === String(atual); b.classList.toggle('on', on); b.setAttribute('aria-pressed', on); }); }
const minConv = () => CFG.min_ligacoes;

/* contexto comum de uma atualização */
let C = null;
function contexto() {
  MEMO = new Map();
  const rows = sel('A'), t = somaA(rows), jc = janelaComp(), tc = jc ? somaA(sel('A', jc.r0, jc.r1)) : null;
  const baldes = porBalde(rows).map(b => Object.assign(b, { t: somaA(b.rows) }));
  return { rows, t, jc, tc, baldes, rot: jc ? jc.rot : '' };
}
function kpiTaxa(id, k, sub, cor) { const v = tx(C.t, k); kpi(id, pc(v), chipDelta(deltaTaxa(k, C.t, C.tc), C.rot), sub, C.baldes.map(b => ({ rot: b.rot, v: tx(b.t, k) })), cor, x => pc(x)); }
function kpiVol(id, campo, sub, bom = 1, fmtv = comp) { const v = C.t[campo]; const d = C.tc ? deltaVolume(v, C.tc[campo], C.t._dias, C.tc._dias, bom) : null; kpi(id, fmtv(v), chipDelta(d, C.rot), sub, C.baldes.map(b => ({ rot: b.rot, v: b.t[campo] })), COR.verde, x => nf(x)); }
function evolucao(id, k, cor = COR.verde) {
  const media_ = !!MEDIAS[k] && !MET[k];
  const val = t => media_ ? media(t, k) : tx(t, k), nn = t => media_ ? t[MEDIAS[k][1]] : nEf(t, k);
  const pts = C.baldes.map(b => ({ rot: b.rot, v: val(b.t), n: nn(b.t) }));
  const ref = C.tc ? val(C.tc) : null; const fmt = media_ ? (v => nf(v, 2)) : (v => pc(v));
  if (!pts.some(p => p.v != null)) return vazioGrafico(id, 'Sem dados para este indicador no período escolhido.');
  pinta(id, base({ grid: { left: 6, right: 56, top: 30, bottom: 6, containLabel: true },
    tooltip: Object.assign({}, TT, { trigger: 'axis', formatter: ps => { const p = pts[ps[0].dataIndex]; return ttTitulo(p.rot) + ttLinha(cor, nomeMet(k), fmt(p.v), 'n = ' + nf(p.n)) + (ref != null ? ttLinha(COR.cinza, C.jc.curto, fmt(ref)) : '') + (p.n < CFG.min_n_taxa && !media_ ? `<div style="color:${COR.mudo};margin-top:3px">amostra pequena</div>` : ''); } }),
    xAxis: eixoCat(pts.map(p => p.rot), { boundaryGap: false }), yAxis: eixoVal(media_ ? (v => nf(v, 1)) : fmtPc0, { scale: true }),
    series: [linha({ id: 'serie', name: nomeMet(k), data: pts.map(p => p.v), lineStyle: { width: 2, color: cor }, itemStyle: { color: cor }, showSymbol: pts.length <= 31, connectNulls: false,
      endLabel: { show: true, formatter: p => fmt(p.value), color: COR.tinta, fontWeight: 600, fontSize: 12 },
      markLine: ref != null ? linhaRef(ref, C.jc.curto + ' ' + fmt(ref)) : { data: [] } })] }));
  registra(id, ['Período', nomeMet(k), 'n'], pts.map(p => [p.rot, fmt(p.v), p.n]));
}
function fator(id, f) {
  const niv = D.facetas.niveis[f]; const acc = niv.map(() => [0, 0]);
  sel('CV').forEach(r => { if (r[2] === f && acc[r[3]]) { acc[r[3]][0] += r[4]; acc[r[3]][1] += r[5]; } });
  const tot = acc.reduce((s, a) => [s[0] + a[0], s[1] + a[1]], [0, 0]); const geral = div(tot[1], tot[0]);
  const itens = niv.map((nome, i) => { const [n, k] = acc[i]; const [lo, hi] = wilson(k, n); return { nome, n, k, p: div(k, n), lo, hi }; }).filter(x => x.n > 0);
  if (!itens.length) return vazioGrafico(id, 'Sem oportunidades de venda com esse dado no período.');
  const pequeno = x => x.n < CFG.min_n_taxa;
  pinta(id, base({ grid: { left: 6, right: 18, top: 30, bottom: 6, containLabel: true },
    tooltip: Object.assign({}, TT, { trigger: 'item', formatter: p => { const x = itens[p.dataIndex]; if (!x) return ''; return ttTitulo(x.nome) + ttLinha(pequeno(x) ? COR.cinza : COR.verde, 'taxa de fechamento', pc(x.p)) + `<div style="color:${COR.mudo};margin-top:4px">${nf(x.k)} fechamentos em ${nf(x.n)} oportunidades<br>intervalo de 95%: ${pc(x.lo)} a ${pc(x.hi)}${pequeno(x) ? '<br><b style="color:#720D0D">amostra pequena: não conclua</b>' : ''}</div>`; } }),
    xAxis: eixoCat(itens.map(x => x.nome), { axisLabel: { color: COR.mudo, fontSize: 11.5, interval: 0, width: 90, overflow: 'break' } }),
    yAxis: eixoVal(fmtPc0, { max: v => Math.min(1, Math.max(v.max, ...itens.map(x => x.hi || 0)) * 1.08) }),
    series: [barra({ id: 'taxa', name: 'Taxa de fechamento', data: itens.map(x => ({ value: x.p, itemStyle: { color: pequeno(x) ? COR.cinzaClaro : COR.verde } })),
      markLine: linhaRef(geral, 'média ' + pc(geral), COR.tinta2) }),
    { id: 'ic', type: 'custom', name: 'Intervalo de 95%', renderItem: errorBar, data: itens.map((x, i) => [i, x.lo, x.hi]), z: 5, silent: true, tooltip: { show: false } }] }));
  registra(id, ['Nível', 'Oportunidades', 'Fechamentos', 'Taxa', 'IC 95% inferior', 'IC 95% superior'], itens.map(x => [x.nome, x.n, x.k, pc(x.p), pc(x.lo), pc(x.hi)]));
  return { itens, geral };
}
function barrasH(id, itens, o = {}) {
  /* itens: [{nome, v, cor?, tip?}] em ordem de exibição (de cima para baixo) */
  if (!itens.length) return vazioGrafico(id, o.vazio || 'Sem dados no período.');
  const fmt = o.fmt || (v => pc(v)); const its = [...itens].reverse();
  pinta(id, base({ grid: { left: 14, right: 54, top: 8, bottom: 4, containLabel: true },
    tooltip: Object.assign({}, TT, { trigger: 'item', formatter: p => { const x = its[p.dataIndex]; return ttTitulo(x.nome) + ttLinha(x.cor || o.cor || COR.verde, o.rot || '', fmt(x.v)) + (x.tip ? `<div style="color:${COR.mudo};margin-top:4px">${x.tip}</div>` : ''); } }),
    xAxis: eixoVal(o.fmtEixo || fmtPc0, { max: o.max, axisLabel: { show: false } }), yAxis: eixoCat(its.map(x => x.nome), { axisLabel: { color: COR.tinta2, fontSize: 12, width: o.larg || 170, overflow: 'truncate' } }),
    series: [barra({ id: 'b', data: its.map(x => ({ value: x.v, itemStyle: { color: x.cor || o.cor || COR.verde, opacity: x.fraco ? .35 : 1 } })), itemStyle: { borderRadius: [0, 4, 4, 0] }, barMaxWidth: 18,
      label: { show: true, position: 'right', formatter: p => fmt(p.value), color: COR.tinta2, fontSize: 11.5 } })] }));
  const c = g(id); c.off('click'); if (o.clique) c.on('click', p => o.clique(its[p.dataIndex]));
  registra(id, [o.colNome || 'Item', o.colVal || 'Valor'], itens.map(x => [x.nome, fmt(x.v)]));
}
function faixaAviso() {
  const avisos = []; const fim = DIAS[S.d1];
  if (D.meta.duracao_ate && D.meta.duracao_ate < fim) avisos.push(`a duração das ligações vai até ${dd(D.meta.duracao_ate)} (indicadores de tempo param aí)`);
  if (D.meta.classif_ate && D.meta.classif_ate < fim) avisos.push(`a classificação vai até ${dd(D.meta.classif_ate)} (conversas, vendas, problemas e Challenger param aí)`);
  return avisos.length ? `<div class="faixa-info" role="note">ⓘ No período escolhido, ${avisos.join(' e ')}.</div>` : '';
}

const PAG = {};

/* ---------------- 1 · Visão geral ---------------- */
const METS_GERAL = [['fech', 'Fechamento'], ['prob', 'Problemas'], ['res', 'Resolução'], ['k1', 'Carga operacional'], ['chAlta', 'Challenger alta'], ['ch', 'Challenger'], ['at', 'Atendimento'], ['opp', 'Oportunidades']];
PAG.geral = {
  esqueleto: () => kpis([{ id: 'tent', nome: 'Ligações', ir: 'contato' }, { id: 'conv', nome: 'Conversas', ir: 'vendas' }, { id: 'opp', nome: 'Oportunidades de venda', ir: 'vendas' },
    { id: 'fech', nome: 'Taxa de fechamento', ir: 'vendas' }, { id: 'prob', nome: 'Conversas com problema', ir: 'problemas' }, { id: 'res', nome: 'Resolvidos na ligação', ir: 'problemas' },
    { id: 'k1', nome: 'Carga operacional (tempo)', ir: 'tempo' }, { id: 'chAlta', nome: 'Challenger alta qualidade', ir: 'competencias' }]) +
    `<div class="grade">${card('evol', 'c8', 'Evolução', 'Escolha o indicador · a linha tracejada é a comparação', 300, pilulas('metrica', METS_GERAL, S.metrica))}
    ${cardHtml('mudou', 'c4', 'O que mudou', 'Só o que passou da margem de erro')}
    ${card('funil', 'c6', 'Do contato ao fechamento', 'Volumes do período · passe o mouse para ver a conversão de cada etapa', 290)}
    ${card('dist', 'c6', 'Por distrital', 'Mesmo indicador da evolução · clique para filtrar', 290)}</div>`,
  atualizar() {
    const t = C.t;
    kpiVol('tent', 'tent', `${pc(div(t.atend, t.tent))} atendidas`);
    kpiVol('conv', 'conv', `de ${comp(t.an)} analisadas`);
    kpiVol('opp', 'opp', `${pc(div(t.opp, t.conv))} das conversas`);
    kpiTaxa('fech', 'fech', `${nf(t.fech)} fechamentos`);
    kpiTaxa('prob', 'prob', `${nf(t.prob)} problemas`, COR.verm);
    kpiTaxa('res', 'res', `${nf(t.pend)} pendências`);
    kpiTaxa('k1', 'k1', `${hs(t.seg_op)} de ${hs(t.seg_base)}`, COR.verm);
    kpiTaxa('chAlta', 'chAlta', `teve Challenger ${pc(div(t.ch, t.conv))}`);
    const k = S.metrica; evolucao('evol', k, MET[k].bom < 0 ? COR.verm : COR.verde);
    texto('s-evol', `${nomeMet(k)} por ${S.gran === 'dia' ? 'dia' : S.gran === 'semana' ? 'semana' : 'mês'}${C.jc ? ' · tracejada: ' + C.jc.rot : ''}`);
    /* funil */
    const et = [['Ligações', t.tent], ['Atendidas', t.atend], ['Analisadas', t.an], ['Conversas', t.conv], ['Oportunidades de venda', t.opp], ['Fechamentos', t.fech]];
    pinta('funil', base({ grid: { left: 14, right: 70, top: 8, bottom: 4, containLabel: true },
      tooltip: Object.assign({}, TT, { trigger: 'item', formatter: p => { const i = p.dataIndex, e = et[et.length - 1 - i], j = et.length - 1 - i; return ttTitulo(e[0]) + ttLinha(COR.verde, '', nf(e[1])) + (j > 0 ? `<div style="color:${COR.mudo};margin-top:3px">${pc(div(e[1], et[j - 1][1]))} da etapa anterior · ${pc(div(e[1], et[0][1]), 2)} das ligações</div>` : ''); } }),
      xAxis: eixoVal(v => comp(v)), yAxis: eixoCat([...et].reverse().map(e => e[0]), { axisLabel: { color: COR.tinta2, fontSize: 12 } }),
      series: [barra({ id: 'f', data: [...et].reverse().map(e => e[1]), itemStyle: { color: COR.verde, borderRadius: [0, 4, 4, 0] }, barMaxWidth: 22, label: { show: true, position: 'right', formatter: p => nf(p.value), color: COR.tinta2 } })] }));
    registra('funil', ['Etapa', 'Volume', '% da etapa anterior'], et.map((e, i) => [e[0], e[1], i ? pc(div(e[1], et[i - 1][1])) : '']));
    /* distritais */
    const todosD = agrupa(D.A.filter(r => r[0] >= S.d0 && r[0] <= S.d1), r => CART[r[1]].d);
    const its = DIST.map(d => { const tt = somaA(todosD.get(d) || []); return { nome: d, v: tx(tt, k), n: nEf(tt, k) }; }).filter(x => x.v != null);
    if (!its.length) vazioGrafico('dist', 'Sem dados.');
    else {
      pinta('dist', base({ tooltip: Object.assign({}, TT, { trigger: 'item', formatter: p => { const x = its[p.dataIndex]; return ttTitulo(x.nome) + ttLinha(COR.verde, nomeMet(k), pc(x.v), 'n = ' + nf(x.n)); } }),
        xAxis: eixoCat(its.map(x => x.nome)), yAxis: eixoVal(fmtPc0),
        series: [barra({ id: 'd', data: its.map(x => ({ value: x.v, itemStyle: { color: !S.dist || S.dist === x.nome ? (MET[k].bom < 0 ? COR.verm : COR.verde) : COR.cinzaClaro } })), label: { show: true, position: 'top', formatter: p => pc(p.value), color: COR.tinta2, fontSize: 11.5 } })] }));
      const c = g('dist'); c.off('click'); c.on('click', p => setFiltro({ dist: S.dist === its[p.dataIndex].nome ? '' : its[p.dataIndex].nome, cart: '' }));
      registra('dist', ['Distrital', nomeMet(k), 'n'], its.map(x => [x.nome, pc(x.v), x.n]));
    }
    /* o que mudou */
    if (!C.jc) { html('h-mudou', `<div class="vazio">Escolha uma comparação no topo (baseline ou período anterior).</div>`); return; }
    const itens = [];
    ['fech', 'prob', 'res', 'k1', 'chAlta', 'ch', 'at', 'opp', 'tc', 'dec', 'dado', 'rea', 'si1'].forEach(m => { const d = deltaTaxa(m, t, C.tc); if (d && d.sig) itens.push({ ic: d.classe, t: `${nomeMet(m)}: ${pc(tx(t, m))}`, s: `${d.txt} contra ${pc(d.base)} (${C.jc.curto})`, z: Math.abs(d.d), ir: { pag: { fech: 'vendas', prob: 'problemas', res: 'problemas', k1: 'tempo', at: 'contato' }[m] || 'competencias' } }); });
    /* carteiras que mais mudaram */
    const agora = agrupa(sel('A', S.d0, S.d1, true), r => r[1]), antes = agrupa(sel('A', C.jc.r0, C.jc.r1, true), r => r[1]);
    const cartMud = [];
    agora.forEach((rs, ci) => { const a = somaA(rs), b = somaA(antes.get(ci) || []); if (a.conv < minConv()) return; ['fech', 'prob', 'k1'].forEach(m => { const d = deltaTaxa(m, a, b); if (d && d.sig && d.classe !== 'neutro') cartMud.push({ ic: d.classe, t: `${CART[ci].c} · ${nomeMet(m)} ${pc(tx(a, m))}`, s: `${d.txt} contra ${pc(d.base)}`, z: Math.abs(d.d), cart: CART[ci].c }); }); });
    cartMud.sort((x, y) => y.z - x.z);
    itens.sort((x, y) => y.z - x.z);
    const lista = itens.slice(0, 6).concat(cartMud.filter(x => x.ic === 'ruim').slice(0, 3));
    html('h-mudou', lista.length ? `<div class="lista">${lista.map((x, i) => `<div class="item clic" data-mudou="${i}" tabindex="0"><span class="ic ${x.ic}">${x.ic === 'bom' ? '▲' : x.ic === 'ruim' ? '!' : 'i'}</span><div><b>${esc(x.t)}</b><span>${esc(x.s)}</span></div></div>`).join('')}</div>` : `<div class="vazio">Nada mudou além da margem de erro contra ${esc(C.jc.rot)}.</div>`);
    if (lista.length >= 4) html('n-mudou', 'Muitos indicadores mudando juntos pode ser troca de versão do classificador, não mudança no time: confira a página Qualidade do dado.'); else html('n-mudou', '');
    const h = document.getElementById('h-mudou'); h.__lista = lista;
    if (!h.__ligado) { h.__ligado = true; const ir = ev => { const it = ev.target.closest('[data-mudou]'); if (!it) return; const x = h.__lista[+it.dataset.mudou]; if (x.cart) setFiltro({ cart: x.cart }); else if (x.ir) irPara(x.ir.pag); }; h.addEventListener('click', ir); h.addEventListener('keydown', ev => { if (ev.key === 'Enter') ir(ev); }); }
  },
};

/* ---------------- 2 · Tempo ---------------- */
const GRUPOS_TEMPO = [['Negociação', 'seg_neg', 'n_neg', COR.verde], ['Relacionamento', 'seg_rel', 'n_rel', COR.azul], ['Operacional sem problema', null, 'n_ops', COR.vermClaro], ['Operacional com problema', 'seg_prob', 'n_prob_base', COR.verm], ['Sem conteúdo', 'seg_sc', 'n_sc', COR.cinza]];
const segGrupo = (t, i) => i === 2 ? t.seg_op - t.seg_prob : t[GRUPOS_TEMPO[i][1]];
PAG.tempo = {
  esqueleto: () => kpis([{ id: 'horas', nome: 'Horas de conversa', dic: 'horas' }, { id: 'k1', nome: 'Carga operacional (GPT)' }, { id: 'k1gem', nome: 'Carga operacional (Gemini)' },
    { id: 'k7', nome: 'Tempo em negociação', dic: 'k1' }, { id: 'tma', nome: 'Tempo médio por ligação' }, { id: 'k3', nome: 'Horas excedentes' }]) +
    `<div class="grade">${card('comp', 'c8', 'Para onde vai o tempo', 'Composição do tempo de ligação classificada', 300)}
    ${card('tipos', 'c4', 'Tempo por tipo de ligação', 'Horas · cor = grupo da composição', 300)}
    ${card('codt', 'c6', 'Tempo em problema, por código', 'Horas · clique para abrir o código na página de problemas', 300)}
    ${card('mapa', 'c6', 'Quando o tempo acontece', 'Horas de conversa por dia da semana e hora (Brasília)', 300)}
    ${card('faixa', 'c6', 'Duração da ligação × fechamento', 'Oportunidades de venda · barra preta = intervalo de 95%', 280)}
    ${card('fph', 'c3', 'Fechamentos por hora de conversa', 'Por faixa de duração', 280)}
    ${cardHtml('sim', 'c3', 'Simulador', 'Quanto vale reduzir um código de problema?')}</div>`,
  atualizar() {
    const t = C.t;
    kpiVol('horas', 'seg_base', `${nf(t.base_n)} ligações com duração`, 0, v => hs(v));
    kpiTaxa('k1', 'k1', `${hs(t.seg_op)} operacionais`, COR.verm);
    kpiTaxa('k1gem', 'k1gem', 'régua Aletheia (Suporte)', COR.tinta2);
    kpiTaxa('k7', 'k7', 'negociação sem problema', COR.verde);
    const tm = media(t, 'tma'), tmC = C.tc ? media(C.tc, 'tma') : null;
    kpi('tma', mmss(tm), chipDelta(deltaMedia(tm, tmC, 0, 0, 15), C.rot), `com problema ${mmss(div(t.seg_prob, t.n_prob_base))} · sem ${mmss(div(t.seg_base - t.seg_prob, t.base_n - t.n_prob_base))}`, C.baldes.map(b => ({ rot: b.rot, v: media(b.t, 'tma') })), COR.tinta2, mmss);
    const x3 = k3(t); kpi('k3', x3 == null ? '–' : nf(x3, 1) + ' h', '', 'a mais nas ligações com problema', C.baldes.map(b => ({ rot: b.rot, v: k3(b.t) })), COR.verm, v => nf(v, 1) + ' h');
    /* composição */
    const bs = C.baldes.filter(b => b.t.seg_base > 0);
    if (!bs.length) vazioGrafico('comp', 'Sem ligações com duração no período.');
    else {
      pinta('comp', base({ grid: { left: 6, right: 16, top: 36, bottom: 6, containLabel: true }, legend: { top: 0, left: 0, itemWidth: 10, itemHeight: 10, textStyle: { fontSize: 12, color: COR.tinta2 } },
        tooltip: Object.assign({}, TT, { trigger: 'axis', formatter: ps => { const b = bs[ps[0].dataIndex]; return ttTitulo(b.rot) + GRUPOS_TEMPO.map((gr, i) => ttLinha(gr[3], gr[0], pc(div(segGrupo(b.t, i), b.t.seg_base)), hs(segGrupo(b.t, i)))).reverse().join('') + `<div style="color:${COR.mudo};margin-top:3px">${hs(b.t.seg_base)} classificadas</div>`; } }),
        xAxis: eixoCat(bs.map(b => b.rot)), yAxis: eixoVal(fmtPc0, { max: 1 }),
        series: GRUPOS_TEMPO.map((gr, i) => barra({ id: 'g' + i, name: gr[0], stack: 'tempo', data: bs.map(b => div(segGrupo(b.t, i), b.t.seg_base)), itemStyle: { color: gr[3], borderRadius: 0, borderColor: '#fff', borderWidth: 1 }, barMaxWidth: 34 })) }));
      registra('comp', ['Período', ...GRUPOS_TEMPO.map(x => x[0])], bs.map(b => [b.rot, ...GRUPOS_TEMPO.map((gr, i) => pc(div(segGrupo(b.t, i), b.t.seg_base)))]));
    }
    /* por tipo */
    const tp = new Map(); sel('TP').forEach(r => { const a = tp.get(r[2]) || [0, 0, 0, 0]; for (let i = 0; i < 4; i++) a[i] += r[3 + i]; tp.set(r[2], a); });
    const corG = { op: COR.vermClaro, neg: COR.verde, rel: COR.azul, sc: COR.cinza };
    const tpn = new Map(); tp.forEach((a, i) => { const nome = NOMES_TIPO[D.tipos[i]] || D.tipos[i]; const x = tpn.get(nome) || { nome, a: [0, 0, 0, 0], g: GRUPO_TIPO(D.tipos[i]) }; a.forEach((v, j) => x.a[j] += v); tpn.set(nome, x); });
    const tipos = [...tpn.values()].map(({ nome, a, g: gr }) => ({ nome, v: a[2], cor: corG[gr], tip: `${nf(a[0])} ligações · TMA ${mmss(div(a[2], a[1]))} · ${pc(div(a[3], a[0]), 0)} com problema` })).filter(x => x.v > 0).sort((a, b) => b.v - a.v);
    barrasH('tipos', tipos, { fmt: v => hs(v), fmtEixo: v => nf(v / 3600, 0) + ' h', larg: 150, colNome: 'Tipo', colVal: 'Horas', vazio: 'Sem ligações com duração no período.' });
    /* por código */
    const pc_ = new Map(); sel('P').forEach(r => { const a = pc_.get(r[2]) || [0, 0, 0, 0]; a[0] += r[3]; a[1] += r[4]; a[2] += r[5]; a[3] += r[6]; pc_.set(r[2], a); });
    const cods = [...pc_.entries()].map(([i, a]) => ({ cod: D.codigos[i], nome: nomeCod(D.codigos[i]), v: a[1], cor: COR.verm, fraco: S.cod && S.cod !== D.codigos[i], tip: `${nf(a[0])} ligações com problema · TMA ${mmss(div(a[1], a[2]))} · ${pc(div(a[3], a[0]), 0)} pendentes` })).filter(x => x.v > 0).sort((a, b) => b.v - a.v);
    barrasH('codt', cods, { fmt: v => hs(v), fmtEixo: v => nf(v / 3600, 0) + ' h', larg: 170, colNome: 'Código', colVal: 'Horas', vazio: 'Sem ligações com problema e duração no período.', clique: x => { S.cod = x.cod; irPara('problemas'); } });
    /* mapa de calor dia × hora */
    const dias = [1, 2, 3, 4, 5]; const m = new Map(), hset = new Set(); sel('H').forEach(r => { const k = DOWI[r[0]] + '|' + r[2]; m.set(k, (m.get(k) || 0) + r[5]); if (r[5] > 0) hset.add(r[2]); });
    const horasH = []; if (hset.size) for (let h = Math.min(...hset); h <= Math.max(...hset); h++) horasH.push(h);
    const dados = []; let mx = 0; dias.forEach((d, yi) => horasH.forEach((h, xi) => { const v = (m.get(d + '|' + h) || 0) / 3600; mx = Math.max(mx, v); dados.push([xi, yi, +v.toFixed(2)]); }));
    if (!(mx > 0)) vazioGrafico('mapa', 'Sem ligações com duração no período.');
    else {
      pinta('mapa', base({ grid: { left: 6, right: 12, top: 8, bottom: 44, containLabel: true },
        tooltip: Object.assign({}, TT, { trigger: 'item', formatter: p => ttTitulo(`${DSEM[dias[p.value[1]]]} · ${horasH[p.value[0]]}h`) + ttLinha(COR.verde, 'de conversa', nf(p.value[2], 1) + ' h') }),
        xAxis: eixoCat(horasH.map(h => h + 'h'), { splitArea: { show: false } }), yAxis: eixoCat(dias.map(d => DSEM[d]), { inverse: true }),
        visualMap: { min: 0, max: mx, orient: 'horizontal', left: 'center', bottom: 0, itemWidth: 12, itemHeight: 140, calculable: false, inRange: { color: SEQ }, text: ['mais horas', 'menos'], textStyle: { color: COR.mudo, fontSize: 11 } },
        series: [{ id: 'h', type: 'heatmap', data: dados, itemStyle: { borderColor: '#fff', borderWidth: 2, borderRadius: 3 }, emphasis: { itemStyle: { borderColor: COR.tinta, borderWidth: 1 } } }] }));
      registra('mapa', ['Dia', ...horasH.map(h => h + 'h')], dias.map((d, yi) => [DSEM[d], ...horasH.map((h, xi) => nf(dados[yi * horasH.length + xi][2], 1))]));
    }
    /* faixa de duração */
    const NF = ['< 2 min', '2–5 min', '5–8 min', '8–12 min', '> 12 min']; const fa = NF.map(() => [0, 0, 0]);
    sel('F').forEach(r => { fa[r[2]][0] += r[3]; fa[r[2]][1] += r[4]; fa[r[2]][2] += r[5]; });
    const its = NF.map((nome, i) => { const [n, k, s] = fa[i]; const [lo, hi] = wilson(k, n); return { nome, n, k, s, p: div(k, n), lo, hi, fph: s > 0 ? k / (s / 3600) : null }; });
    if (!its.some(x => x.n > 0)) { vazioGrafico('faixa', 'Sem oportunidades com duração no período.'); vazioGrafico('fph', 'Sem dados.'); }
    else {
      pinta('faixa', base({ tooltip: Object.assign({}, TT, { trigger: 'item', formatter: p => { const x = its[p.dataIndex]; return ttTitulo(x.nome) + ttLinha(COR.verde, 'taxa de fechamento', pc(x.p)) + `<div style="color:${COR.mudo};margin-top:3px">${nf(x.k)} de ${nf(x.n)} · intervalo ${pc(x.lo)} a ${pc(x.hi)}</div>`; } }),
        xAxis: eixoCat(NF), yAxis: eixoVal(fmtPc0, { max: v => Math.min(1, Math.max(v.max, ...its.map(x => x.hi || 0)) * 1.1) }),
        series: [barra({ id: 'f', data: its.map(x => ({ value: x.p, itemStyle: { color: x.n < CFG.min_n_taxa ? COR.cinzaClaro : COR.verde } })) }), { id: 'ic', type: 'custom', renderItem: errorBar, data: its.map((x, i) => [i, x.lo, x.hi]), z: 5, silent: true, tooltip: { show: false } }] }));
      registra('faixa', ['Faixa', 'Oportunidades', 'Fechamentos', 'Taxa', 'IC inferior', 'IC superior'], its.map(x => [x.nome, x.n, x.k, pc(x.p), pc(x.lo), pc(x.hi)]));
      pinta('fph', base({ tooltip: Object.assign({}, TT, { trigger: 'item', formatter: p => { const x = its[p.dataIndex]; return ttTitulo(x.nome) + ttLinha(COR.azul, 'fechamentos por hora', nf(x.fph, 2)) + `<div style="color:${COR.mudo};margin-top:3px">${nf(x.k)} fechamentos em ${hs(x.s)}</div>`; } }),
        xAxis: eixoCat(NF.map(x => x.replace(' min', '')), { axisLabel: { color: COR.mudo, fontSize: 11, interval: 0 } }), yAxis: eixoVal(v => nf(v, 1)),
        series: [barra({ id: 'p', data: its.map(x => x.fph), itemStyle: { color: COR.azul } })] }));
      registra('fph', ['Faixa', 'Fechamentos por hora'], its.map(x => [x.nome, nf(x.fph, 2)]));
    }
    const fNota = its.slice(2).reduce((a, x) => a + x.s, 0), fTot = its.reduce((a, x) => a + x.s, 0), kT = its.reduce((a, x) => a + x.k, 0);
    html('n-faixa', fTot > 0 && kT > 0 ? `Ligações de 5 min ou mais: <b>${pc(fNota / fTot, 0)}</b> do tempo das oportunidades e <b>${pc(its.slice(2).reduce((a, x) => a + x.k, 0) / kT, 0)}</b> dos fechamentos. Associação: ligação longa também pode ser consequência da venda.` : '');
    /* simulador */
    const codsSim = cods.map(x => x.cod); if (!codsSim.includes(S.simCod) && codsSim.length) S.simCod = codsSim[0];
    const alvo = cods.find(x => x.cod === S.simCod); const segC = alvo ? alvo.v : 0; const diasB = new Set(C.rows.filter(r => r[IA.base_n] > 0).map(r => r[0])).size;
    const hMes = diasB ? segC / 3600 / diasB * CFG.dias_uteis_mes : 0; const red = S.simPct / 100; const efeito = t.seg_base > 0 ? segC * red / t.seg_base : null;
    const hsim = document.getElementById('h-sim'); const chaveSim = codsSim.join(',');
    if (hsim.dataset.cods !== chaveSim) { hsim.dataset.cods = chaveSim; hsim.innerHTML = `<div class="controles"><select data-sim="cod" aria-label="Código de problema">${codsSim.map(c => `<option value="${esc(c)}">${esc(nomeCod(c))}</option>`).join('')}</select></div>
      <div class="slider"><input type="range" min="0" max="80" step="5" data-sim="pct" aria-label="Redução das ligações do código"><b id="simPct"></b></div><div id="simOut"></div>`; }
    const sSel = hsim.querySelector('[data-sim="cod"]'), sRng = hsim.querySelector('[data-sim="pct"]'); if (sSel) sSel.value = S.simCod; if (sRng && document.activeElement !== sRng) sRng.value = S.simPct; texto('simPct', '−' + S.simPct + '%');
    html('simOut', `<div class="numeros"><div><b>${nf(hMes * red, 1)} h</b><span>devolvidas por mês</span></div><div><b>${efeito == null ? '–' : pp(-efeito * 100)}</b><span>na carga operacional</span></div></div>
      <div class="nota">${esc(S.simCod)} no período: ${hs(segC)} em ${diasB} dias com duração ≈ ${nf(hMes, 1)} h por mês. Conta aritmética, não previsão.</div>`);
  },
};

/* ---------------- 3 · Vendas ---------------- */
const FAC_OPC = D.facetas.nomes.map((n, i) => [i, n]);
PAG.vendas = {
  esqueleto: () => kpis([{ id: 'opp', nome: 'Oportunidades de venda' }, { id: 'fechn', nome: 'Fechamentos', dic: 'fech' }, { id: 'fech', nome: 'Taxa de fechamento' },
    { id: 'fechConv', nome: 'Fechamentos por 100 conversas', dic: 'fech' }, { id: 'tc', nome: 'Tentativa comercial' }, { id: 'dec', nome: 'Falou com o decisor' }]) +
    `<div class="grade">${card('funilv', 'c5', 'Funil comercial', 'Das conversas aos fechamentos', 280)}
    ${card('evolv', 'c7', 'Taxa de fechamento no tempo', '', 280)}
    ${card('fator', 'c12', 'O que acompanha o fechamento', 'Taxa de fechamento por fator · barra cinza = amostra pequena · associação, não causa', 300, pilulas('faceta', FAC_OPC, S.faceta))}
    ${card('tiposv', 'c5', 'Fechamentos por tipo', 'Novo, renovação e upsell', 280)}
    ${card('cartv', 'c7', 'Carteiras: oportunidades × taxa de fechamento', 'Horizontal = oportunidades · vertical = taxa · tamanho = fechamentos · clique para filtrar', 280)}</div>`,
  atualizar() {
    const t = C.t;
    kpiVol('opp', 'opp', `${pc(div(t.opp, t.conv))} das conversas`);
    kpiVol('fechn', 'fech', `novo ${nf(t.fech_novo)} · renovação ${nf(t.fech_renov)} · upsell ${nf(t.fech_upsell)}`);
    kpiTaxa('fech', 'fech', 'fechamentos ÷ oportunidades');
    kpi('fechConv', nf(div(t.fech, t.conv) * 100, 1), chipDelta(deltaTaxa('fechConv', t, C.tc), C.rot), `${nf(t.inter)} oportunidades ficaram em aberto`, C.baldes.map(b => ({ rot: b.rot, v: div(b.t.fech, b.t.conv) * 100 })), COR.verde, v => nf(v, 1));
    kpiTaxa('tc', 'tc', 'conversas com tentativa de venda');
    kpiTaxa('dec', 'dec', 'análises com o decisor');
    const et = [['Conversas', t.conv], ['Com tentativa comercial', t.tc_s], ['Oportunidades de venda', t.opp], ['Fechamentos', t.fech]];
    pinta('funilv', base({ grid: { left: 14, right: 70, top: 8, bottom: 4, containLabel: true },
      tooltip: Object.assign({}, TT, { trigger: 'item', formatter: p => { const j = et.length - 1 - p.dataIndex, e = et[j]; return ttTitulo(e[0]) + ttLinha(COR.verde, '', nf(e[1])) + (j > 0 ? `<div style="color:${COR.mudo};margin-top:3px">${pc(div(e[1], et[0][1]))} das conversas</div>` : ''); } }),
      xAxis: eixoVal(v => comp(v)), yAxis: eixoCat([...et].reverse().map(e => e[0]), { axisLabel: { color: COR.tinta2, fontSize: 12 } }),
      series: [barra({ id: 'f', data: [...et].reverse().map(e => e[1]), itemStyle: { color: COR.verde, borderRadius: [0, 4, 4, 0] }, barMaxWidth: 22, label: { show: true, position: 'right', formatter: p => nf(p.value), color: COR.tinta2 } })] }));
    registra('funilv', ['Etapa', 'Volume'], et);
    evolucao('evolv', 'fech'); texto('s-evolv', `Por ${S.gran === 'dia' ? 'dia' : S.gran === 'semana' ? 'semana' : 'mês'}${C.jc ? ' · tracejada: ' + C.jc.rot : ''}`);
    const r = fator('fator', +S.faceta);
    html('n-fator', r ? `Média do período: <b>${pc(r.geral)}</b>. Diferença só conta quando as barras pretas (intervalos de 95%) não se sobrepõem. O fator pode estar ligado a outra coisa (ex.: ligações mais longas), por isso use como hipótese para o piloto.` : '');
    /* por tipo */
    const bs = C.baldes; const tiposF = [['Novo', 'fech_novo', COR.verde], ['Renovação', 'fech_renov', COR.azul], ['Upsell', 'fech_upsell', COR.lima]];
    if (!bs.some(b => b.t.fech > 0)) vazioGrafico('tiposv', 'Sem fechamentos no período.');
    else {
      pinta('tiposv', base({ grid: { left: 6, right: 16, top: 34, bottom: 6, containLabel: true }, legend: { top: 0, left: 0, itemWidth: 10, itemHeight: 10, textStyle: { fontSize: 12, color: COR.tinta2 } },
        tooltip: Object.assign({}, TT, { trigger: 'axis', formatter: ps => { const b = bs[ps[0].dataIndex]; return ttTitulo(b.rot) + tiposF.map(x => ttLinha(x[2], x[0], nf(b.t[x[1]]))).reverse().join(''); } }),
        xAxis: eixoCat(bs.map(b => b.rot)), yAxis: eixoVal(v => nf(v)),
        series: tiposF.map((x, i) => barra({ id: 't' + i, name: x[0], stack: 'f', data: bs.map(b => b.t[x[1]]), itemStyle: { color: x[2], borderRadius: 0, borderColor: '#fff', borderWidth: 1 }, barMaxWidth: 30 })) }));
      registra('tiposv', ['Período', ...tiposF.map(x => x[0])], bs.map(b => [b.rot, ...tiposF.map(x => b.t[x[1]])]));
    }
    /* dispersão de carteiras */
    const porC = agrupa(sel('A', S.d0, S.d1, true), r_ => r_[1]); const pts = [];
    porC.forEach((rs, ci) => { const a = somaA(rs); if (a.opp >= 10) pts.push({ c: CART[ci].c, d: CART[ci].d, x: a.opp, y: div(a.fech, a.opp), f: a.fech, conv: a.conv }); });
    if (!pts.length) vazioGrafico('cartv', 'Nenhuma carteira com 10 ou mais oportunidades no período.');
    else {
      const med = mediana(pts.map(p => p.y)), mxF = Math.max(1, ...pts.map(p => p.f));
      pinta('cartv', base({ grid: { left: 6, right: 24, top: 24, bottom: 24, containLabel: true },
        tooltip: Object.assign({}, TT, { trigger: 'item', formatter: p => { const x = pts[p.dataIndex]; return ttTitulo(`${x.c} · ${x.d}`) + ttLinha(COR.verde, 'taxa de fechamento', pc(x.y)) + `<div style="color:${COR.mudo};margin-top:3px">${nf(x.f)} fechamentos em ${nf(x.x)} oportunidades</div>`; } }),
        xAxis: eixoVal(v => nf(v)), yAxis: eixoVal(fmtPc0),
        series: [{ id: 's', type: 'scatter', data: pts.map(p => [p.x, p.y]), symbolSize: (v, p) => 8 + 22 * Math.sqrt(pts[p.dataIndex].f / mxF),
          itemStyle: { color: p => pts[p.dataIndex].c === S.cart ? COR.noite : COR.verde, opacity: .8, borderColor: '#fff', borderWidth: 2 },
          markLine: linhaRef(med, 'mediana ' + pc(med)) }] }));
      const c = g('cartv'); c.off('click'); c.on('click', p => setFiltro({ cart: S.cart === pts[p.dataIndex].c ? '' : pts[p.dataIndex].c }));
      registra('cartv', ['Carteira', 'Distrital', 'Oportunidades', 'Fechamentos', 'Taxa'], pts.sort((a, b) => b.y - a.y).map(p => [p.c, p.d, p.x, p.f, pc(p.y)]));
    }
  },
};

/* ---------------- 4 · Problemas ---------------- */
PAG.problemas = {
  esqueleto: () => kpis([{ id: 'prob', nome: 'Conversas com problema' }, { id: 'probn', nome: 'Problemas', dic: 'prob' }, { id: 'res', nome: 'Resolvidos na ligação' },
    { id: 'par', nome: 'Resolvidos em parte', dic: 'res' }, { id: 'pend', nome: 'Pendências' }, { id: 'k5', nome: 'Reincidência' }]) +
    `<div id="faixaCod"></div><div class="grade">${card('pareto', 'c7', 'Problemas por código', 'Clique num código para ver o detalhe e filtrar a página', 320, pilulas('pareto', [['n', 'Ligações'], ['h', 'Horas'], ['todos', 'Todos os códigos citados']], S.pareto))}
    ${card('resol', 'c5', 'Resolução na ligação, por código', 'Todos os códigos, do mais frequente para o menos', 352)}
    ${card('evolp', 'c6', 'Conversas com problema no tempo', '', 260)}
    ${card('cartp', 'c6', 'Problemas por 100 conversas, por carteira', 'Clique para filtrar', 260)}
    ${cardHtml('origem', 'c4', 'Origem', 'Ligação receptiva × ativa')}
    ${cardHtml('detcod', 'c8', 'Detalhe do código', 'Clique num código no gráfico de cima')}</div>`,
  atualizar() {
    const t = C.t;
    kpiTaxa('prob', 'prob', 'problemas ÷ conversas', COR.verm);
    kpiVol('probn', 'prob', `em ${comp(t.conv)} conversas`, -1);
    kpiTaxa('res', 'res', `${nf(t.res_sim)} resolvidos`);
    kpi('par', pc(div(t.res_par, t.prob)), '', `não resolvidos ${pc(div(t.res_nao, t.prob))}`, C.baldes.map(b => ({ rot: b.rot, v: div(b.t.res_par, b.t.prob) })), COR.azul, x => pc(x));
    kpiVol('pend', 'pend', 'parcial ou não resolvido', -1);
    const cl = new Map(); sel('CL').forEach(r => { if (r[7] > 0) cl.set(r[2], (cl.get(r[2]) || 0) + r[7]); }); let tot = 0, re = 0, cre = 0; cl.forEach(n => { tot += n; if (n >= 2) { re += n; cre++; } });
    kpi('k5', pc(div(re, tot)), '', `${nf(cre)} clientes com 2+ problemas`, null);
    /* códigos */
    const P = sel('P'), porCod = new Map(); P.forEach(r => { const a = porCod.get(r[2]) || [0, 0, 0, 0, 0, 0, 0]; for (let i = 0; i < 7; i++) a[i] += r[3 + i]; porCod.set(r[2], a); });
    let itens;
    if (S.pareto === 'todos') { const pi = new Map(); sel('PI').forEach(r => pi.set(r[2], (pi.get(r[2]) || 0) + r[3])); itens = [...pi.entries()].map(([i, n]) => ({ cod: D.codigos[i], v: n })); }
    else itens = [...porCod.entries()].map(([i, a]) => ({ cod: D.codigos[i], v: S.pareto === 'h' ? a[1] / 3600 : a[0], a }));
    itens = itens.filter(x => x.v > 0 && x.cod !== 'nenhum').sort((a, b) => b.v - a.v);
    const totV = soma(itens.map(x => x.v)); let acum = 0; itens.forEach(x => { acum += x.v; x.cum = acum / totV; });
    if (!itens.length) vazioGrafico('pareto', 'Sem problemas no período.');
    else {
      const fmtV = v => S.pareto === 'h' ? nf(v, 1) + ' h' : nf(v);
      pinta('pareto', base({ tooltip: Object.assign({}, TT, { trigger: 'item', formatter: p => { const x = itens[p.dataIndex]; return ttTitulo(nomeCod(x.cod)) + ttLinha(COR.verm, S.pareto === 'h' ? 'horas' : S.pareto === 'todos' ? 'ligações em que foi citado' : 'ligações (código principal)', fmtV(x.v)) + `<div style="color:${COR.mudo};margin-top:3px">${pc(x.v / totV)} do total · acumulado ${pc(x.cum)}</div>`; } }),
        xAxis: eixoCat(itens.map(x => x.cod), { axisLabel: { color: COR.tinta2, fontSize: 11.5, interval: 0 } }), yAxis: eixoVal(v => S.pareto === 'h' ? nf(v, 0) + ' h' : nf(v)),
        series: [barra({ id: 'p', data: itens.map(x => ({ value: +x.v.toFixed(2), itemStyle: { color: COR.verm, opacity: S.cod && S.cod !== x.cod ? .3 : 1 } })), label: { show: true, position: 'top', formatter: p => p.dataIndex < 5 ? pc(itens[p.dataIndex].v / totV, 0) : '', color: COR.tinta2, fontSize: 11 } })] }));
      const c = g('pareto'); c.off('click'); c.on('click', p => { S.cod = S.cod === itens[p.dataIndex].cod ? '' : itens[p.dataIndex].cod; atualizar(); });
      registra('pareto', ['Código', 'Nome', 'Valor', '% do total', '% acumulado'], itens.map(x => [x.cod, NOMES_P[x.cod] || '', fmtV(x.v), pc(x.v / totV), pc(x.cum)]));
      html('n-pareto', `Os 3 primeiros somam <b>${pc(itens[Math.min(2, itens.length - 1)].cum)}</b>${S.pareto === 'todos' ? ' das citações (uma ligação pode citar mais de um código)' : ' dos problemas'}.`);
    }
    /* resolução por código */
    const rs = [...porCod.entries()].map(([i, a]) => ({ cod: D.codigos[i], n: a[0], s: a[4], p: a[5], nao: a[6] })).filter(x => x.n > 0 && x.cod !== 'nenhum').sort((a, b) => a.n - b.n);
    if (!rs.length) vazioGrafico('resol', 'Sem problemas no período.');
    else {
      const sr = [['Resolvido', 's', COR.verde], ['Parcial', 'p', COR.azul], ['Não resolvido', 'nao', COR.verm]];
      pinta('resol', base({ grid: { left: 6, right: 16, top: 32, bottom: 4, containLabel: true }, legend: { top: 0, left: 0, itemWidth: 10, itemHeight: 10, textStyle: { fontSize: 12, color: COR.tinta2 } },
        tooltip: Object.assign({}, TT, { trigger: 'axis', axisPointer: { type: 'shadow' }, formatter: ps => { const x = rs[ps[0].dataIndex]; return ttTitulo(nomeCod(x.cod)) + sr.map(s => ttLinha(s[2], s[0], pc(div(x[s[1]], x.n), 0), nf(x[s[1]]))).join('') + `<div style="color:${COR.mudo};margin-top:3px">${nf(x.n)} ligações</div>`; } }),
        xAxis: eixoVal(fmtPc0, { max: 1 }), yAxis: eixoCat(rs.map(x => x.cod), { axisLabel: { color: COR.tinta2, fontSize: 11.5 } }),
        series: sr.map((s, j) => barra({ id: 'r' + j, name: s[0], stack: 'r', data: rs.map(x => ({ value: div(x[s[1]], x.n), itemStyle: { opacity: S.cod && S.cod !== x.cod ? .3 : 1 } })), itemStyle: { color: s[2], borderRadius: 0, borderColor: '#fff', borderWidth: 1 }, barMaxWidth: 16 })) }));
      const c = g('resol'); c.off('click'); c.on('click', p => { const x = rs[p.dataIndex]; S.cod = S.cod === x.cod ? '' : x.cod; atualizar(); });
      registra('resol', ['Código', 'Ligações', 'Resolvido', 'Parcial', 'Não resolvido'], [...rs].reverse().map(x => [x.cod, x.n, pc(div(x.s, x.n)), pc(div(x.p, x.n)), pc(div(x.nao, x.n))]));
    }
    evolucao('evolp', 'prob', COR.verm); texto('s-evolp', `Por ${S.gran === 'dia' ? 'dia' : S.gran === 'semana' ? 'semana' : 'mês'}${C.jc ? ' · tracejada: ' + C.jc.rot : ''}`);
    /* por carteira */
    const conv = new Map(); sel('A', S.d0, S.d1, true).forEach(r => conv.set(r[1], (conv.get(r[1]) || 0) + r[IA.conv]));
    const probC = new Map(); sel('P', S.d0, S.d1, true).forEach(r => { if (!S.cod || D.codigos[r[2]] === S.cod) probC.set(r[1], (probC.get(r[1]) || 0) + r[3]); });
    const cs = [...conv.entries()].filter(([, n]) => n >= minConv()).map(([ci, n]) => ({ nome: CART[ci].c, v: (probC.get(ci) || 0) / n * 100, n, p: probC.get(ci) || 0, cor: CART[ci].c === S.cart ? COR.noite : COR.verm })).sort((a, b) => b.v - a.v);
    if (!cs.length) vazioGrafico('cartp', `Nenhuma carteira com ${minConv()} ou mais conversas no período.`);
    else {
      const med = mediana(cs.map(x => x.v)); const top = cs.slice(0, 20);
      pinta('cartp', base({ tooltip: Object.assign({}, TT, { trigger: 'item', formatter: p => { const x = top[p.dataIndex]; return ttTitulo(x.nome) + ttLinha(COR.verm, 'problemas por 100 conversas', nf(x.v, 1)) + `<div style="color:${COR.mudo};margin-top:3px">${nf(x.p)} problemas em ${nf(x.n)} conversas</div>`; } }),
        xAxis: eixoCat(top.map(x => x.nome), { axisLabel: { color: COR.mudo, fontSize: 10.5, interval: 0, rotate: 45 } }), yAxis: eixoVal(v => nf(v)),
        series: [barra({ id: 'c', data: top.map(x => ({ value: +x.v.toFixed(1), itemStyle: { color: x.cor } })), markLine: linhaRef(med, 'mediana ' + nf(med, 1)) })] }));
      const c = g('cartp'); c.off('click'); c.on('click', p => setFiltro({ cart: S.cart === top[p.dataIndex].nome ? '' : top[p.dataIndex].nome }));
      registra('cartp', ['Carteira', 'Problemas por 100 conversas', 'Problemas', 'Conversas'], cs.map(x => [x.nome, nf(x.v, 1), x.p, x.n]));
      texto('s-cartp', `${S.cod ? nomeCod(S.cod) + ' · ' : ''}20 carteiras com mais problemas (mínimo de ${minConv()} conversas) · clique para filtrar`);
    }
    /* origem */
    const og = [0, 0, 0, 0]; sel('O').forEach(r => { og[r[2] * 2] += r[3]; og[r[2] * 2 + 1] += r[4]; });
    html('h-origem', og[0] + og[2] > 0 ? `<div class="numeros"><div><b>${pc(div(og[1], og[0]))}</b><span>das receptivas têm problema<br>(${nf(og[1])} de ${nf(og[0])})</span></div><div><b>${pc(div(og[3], og[2]))}</b><span>das ativas têm problema<br>(${nf(og[3])} de ${nf(og[2])})</span></div></div><div class="nota"><b>${pc(div(og[3], og[1] + og[3]), 0)}</b> dos problemas aparecem em ligações ativas: o cliente aproveita a ligação do vendedor para resolver pendências.</div>` : '<div class="vazio">Sem conversas no período.</div>');
    /* detalhe do código */
    html('faixaCod', S.cod ? `<div class="faixa-info">Código em destaque: <b>${esc(nomeCod(S.cod))}</b><button type="button" data-tira-cod>tirar destaque</button></div>` : '');
    if (!S.cod) { html('h-detcod', '<div class="vazio">Clique num código no gráfico "Problemas por código" para ver volume, tempo, resolução e as carteiras com mais ocorrências.</div>'); texto('n-detcod', ''); return; }
    const ic = D.codigos.indexOf(S.cod), a = porCod.get(ic) || [0, 0, 0, 0, 0, 0, 0];
    const porCart = new Map(); P.forEach(r => { if (r[2] === ic) porCart.set(r[1], (porCart.get(r[1]) || 0) + r[3]); });
    const topC = [...porCart.entries()].sort((x, y) => y[1] - x[1]).slice(0, 6);
    html('h-detcod', `<div class="numeros"><div><b>${nf(a[0])}</b><span>ligações (${pc(div(a[0], t.prob), 1)} dos problemas)</span></div><div><b>${hs(a[1])}</b><span>de conversa · TMA ${mmss(div(a[1], a[2]))}</span></div><div><b>${pc(div(a[4], a[0]), 0)}</b><span>resolvidos na ligação</span></div><div><b>${nf(a[3])}</b><span>pendências</span></div></div>
      <div class="nota" style="margin-top:8px"><b>Carteiras com mais ocorrências:</b> ${topC.map(([ci, n]) => `<a href="#" data-cart-link="${esc(CART[ci].c)}">${esc(CART[ci].c)}</a> (${n})`).join(' · ') || '–'}</div>`);
    texto('s-detcod', nomeCod(S.cod));
  },
};

/* ---------------- 5 · Challenger e SPIN ---------------- */
const SPIN_DIMS = [['Situação', 'ss'], ['Problema', 'sp'], ['Implicação', 'si'], ['Necessidade', 'sn'], ['Nota final', 'sf']];
PAG.competencias = {
  esqueleto: () => kpis([{ id: 'ch', nome: 'Teve Challenger' }, { id: 'chAlta', nome: 'Challenger alta qualidade' }, { id: 'dado', nome: 'Trouxe dado' }, { id: 'rea', nome: 'Cliente reagiu' },
    { id: 'sf', nome: 'SPIN · nota final' }, { id: 'si1', nome: 'Implicação com nota 1' }]) +
    `<div class="grade">${card('escada', 'c5', 'Como a conversa é conduzida', '% das conversas (análise da ligação)', 300)}
    ${card('qual', 'c7', 'Qualidade do Challenger no tempo', '% das conversas com Challenger de qualidade alta, média ou baixa', 300)}
    ${card('codch', 'c5', 'Tipos de Challenger', 'Códigos CH1–CH7 · uma conversa pode ter mais de um', 300)}
    ${card('spin', 'c7', 'Notas SPIN', 'Distribuição das notas de 1 a 5 por etapa', 300)}
    ${card('chconv', 'c6', 'Challenger e fechamento', 'Taxa de fechamento por qualidade do Challenger · associação, não causa', 260)}
    ${card('spinconv', 'c6', 'SPIN Implicação e fechamento', 'Taxa de fechamento por nota de Implicação', 260)}
    ${card('mapac', 'c12', 'Competências por carteira', 'Cor = posição da carteira na coluna (mais escuro = melhor) · clique na linha para filtrar', 420)}</div>`,
  atualizar() {
    const t = C.t;
    kpiTaxa('ch', 'ch', `${nf(t.ch)} conversas`);
    kpiTaxa('chAlta', 'chAlta', `${pc(div(t.ch_alta, t.ch), 0)} dos Challengers`);
    kpiTaxa('dado', 'dado', `${nf(t.dado_s)} conversas`);
    kpiTaxa('rea', 'rea', `${nf(t.rea_s)} conversas`);
    const sf = media(t, 'sf'), sfC = C.tc ? media(C.tc, 'sf') : null;
    kpi('sf', nf(sf, 2), chipDelta(deltaMedia(sf, sfC, 1, 2, .1), C.rot), `${nf(t.sf_n)} análises`, C.baldes.map(b => ({ rot: b.rot, v: media(b.t, 'sf') })), COR.verde, v => nf(v, 2));
    kpiTaxa('si1', 'si1', `implicação média ${nf(media(t, 'si'), 2)}`, COR.verm);
    const esc_ = [['Tentativa comercial', 'tc'], ['Trouxe dado', 'dado'], ['Conectou à situação', 'con'], ['Cliente reagiu', 'rea'], ['Teve Challenger', 'ch'], ['Challenger alta qualidade', 'chAlta'], ['Falou com o decisor', 'dec']];
    barrasH('escada', esc_.map(([n, k]) => ({ nome: n, v: tx(t, k), tip: `n = ${nf(nEf(t, k))}` + (C.tc ? ` · ${C.jc.curto} ${pc(tx(C.tc, k))}` : '') })).filter(x => x.v != null), { larg: 160, max: v => Math.min(1, v.max * 1.15), colNome: 'Indicador', colVal: '% das conversas' });
    const bs = C.baldes.filter(b => b.t.conv > 0); const niv = [['Alta', 'ch_alta', ORD4[3]], ['Média', 'ch_media', ORD4[2]], ['Baixa', 'ch_baixa', ORD4[1]]];
    if (!bs.length) vazioGrafico('qual', 'Sem conversas no período.');
    else {
      pinta('qual', base({ grid: { left: 6, right: 16, top: 34, bottom: 6, containLabel: true }, legend: { top: 0, left: 0, itemWidth: 10, itemHeight: 10, textStyle: { fontSize: 12, color: COR.tinta2 } },
        tooltip: Object.assign({}, TT, { trigger: 'axis', formatter: ps => { const b = bs[ps[0].dataIndex]; return ttTitulo(b.rot) + niv.map(x => ttLinha(x[2], x[0], pc(div(b.t[x[1]], b.t.conv)), nf(b.t[x[1]]))).join('') + `<div style="color:${COR.mudo};margin-top:3px">${nf(b.t.conv)} conversas</div>`; } }),
        xAxis: eixoCat(bs.map(b => b.rot)), yAxis: eixoVal(fmtPc0),
        series: [...niv].reverse().map((x, i) => barra({ id: 'q' + i, name: x[0], stack: 'q', data: bs.map(b => div(b.t[x[1]], b.t.conv)), itemStyle: { color: x[2], borderRadius: 0, borderColor: '#fff', borderWidth: 1 }, barMaxWidth: 30 })) }));
      registra('qual', ['Período', 'Alta', 'Média', 'Baixa', 'Conversas'], bs.map(b => [b.rot, pc(div(b.t.ch_alta, b.t.conv)), pc(div(b.t.ch_media, b.t.conv)), pc(div(b.t.ch_baixa, b.t.conv)), b.t.conv]));
    }
    const chc = new Map(); sel('CH').forEach(r => chc.set(r[2], (chc.get(r[2]) || 0) + r[3]));
    barrasH('codch', [...chc.entries()].map(([i, n]) => { const c = D.ch_codigos[i]; return { nome: `${c} · ${NOMES_CH[c] || ''}`, v: n, cor: COR.azul, tip: `${pc(div(n, t.ch), 0)} das conversas com Challenger` }; }).sort((a, b) => b.v - a.v),
      { fmt: v => nf(v), fmtEixo: v => nf(v), larg: 200, colNome: 'Código', colVal: 'Conversas', vazio: 'Sem códigos Challenger no período.' });
    /* notas SPIN */
    const dims = SPIN_DIMS.filter(([, k]) => t[k + '_n'] > 0);
    if (!dims.length) vazioGrafico('spin', 'Sem notas SPIN no período.');
    else {
      const ys = [...dims].reverse();
      pinta('spin', base({ grid: { left: 6, right: 16, top: 34, bottom: 4, containLabel: true }, legend: { top: 0, left: 0, itemWidth: 10, itemHeight: 10, textStyle: { fontSize: 12, color: COR.tinta2 } },
        tooltip: Object.assign({}, TT, { trigger: 'axis', axisPointer: { type: 'shadow' }, formatter: ps => { const [n, k] = ys[ps[0].dataIndex]; return ttTitulo(`${n} · média ${nf(media(t, k), 2)}`) + [5, 4, 3, 2, 1].map(v => ttLinha(ORD5[v - 1], 'nota ' + v, pc(div(t[k + v], t[k + '_n']), 0), nf(t[k + v]))).join(''); } }),
        xAxis: eixoVal(fmtPc0, { max: 1 }), yAxis: eixoCat(ys.map(([n]) => n), { axisLabel: { color: COR.tinta2, fontSize: 12 } }),
        series: [1, 2, 3, 4, 5].map(v => barra({ id: 'n' + v, name: 'nota ' + v, stack: 's', data: ys.map(([, k]) => div(t[k + v], t[k + '_n'])), itemStyle: { color: ORD5[v - 1], borderRadius: 0, borderColor: '#fff', borderWidth: 1 }, barMaxWidth: 22 })) }));
      registra('spin', ['Etapa', 'Média', 'Nota 1', 'Nota 2', 'Nota 3', 'Nota 4', 'Nota 5'], dims.map(([n, k]) => [n, nf(media(t, k), 2), ...[1, 2, 3, 4, 5].map(v => pc(div(t[k + v], t[k + '_n']), 0))]));
    }
    fator('chconv', 0); fator('spinconv', 4);
    /* mapa por carteira */
    const cols = [['Challenger', 'ch'], ['Alta qualidade', 'chAlta'], ['Trouxe dado', 'dado'], ['Reagiu', 'rea'], ['Decisor', 'dec'], ['Tentativa comercial', 'tc'], ['Fechamento', 'fech'], ['SPIN Situação', 'ss'], ['SPIN Problema', 'sp'], ['SPIN Implicação', 'si'], ['SPIN Necessidade', 'sn']];
    const porC = agrupa(sel('A', S.d0, S.d1, true), r => r[1]); const lin = [];
    porC.forEach((rs, ci) => { const a = somaA(rs); if (a.conv >= minConv()) lin.push({ c: CART[ci].c, vals: cols.map(([, k]) => MET[k] ? tx(a, k) : media(a, k)), conv: a.conv }); });
    if (!lin.length) { vazioGrafico('mapac', `Nenhuma carteira com ${minConv()} ou mais conversas no período.`); return; }
    lin.sort((a, b) => (b.vals[6] || 0) - (a.vals[6] || 0));
    const rank = cols.map((_, j) => { const vs = lin.map(l => l.vals[j]).filter(v => v != null).sort((a, b) => a - b); return v => v == null || vs.length < 2 ? null : vs.indexOf(v) / (vs.length - 1); });
    const dados = []; lin.forEach((l, yi) => l.vals.forEach((v, xi) => dados.push([xi, yi, rank[xi](v), v])));
    const el = document.getElementById('g-mapac'); el.style.height = Math.max(240, lin.length * 22 + 80) + 'px';
    pinta('mapac', base({ grid: { left: 6, right: 10, top: 34, bottom: 8, containLabel: true },
      tooltip: Object.assign({}, TT, { trigger: 'item', formatter: p => { const [xi, yi, , v] = p.data; const k = cols[xi][1]; return ttTitulo(`${lin[yi].c} · ${cols[xi][0]}`) + ttLinha(COR.verde, MET[k] ? 'da carteira' : 'nota média', MET[k] ? pc(v) : nf(v, 2)) + `<div style="color:${COR.mudo};margin-top:3px">mediana das carteiras: ${MET[k] ? pc(mediana(lin.map(l => l.vals[xi]))) : nf(mediana(lin.map(l => l.vals[xi])), 2)}</div>`; } }),
      xAxis: eixoCat(cols.map(c => c[0]), { position: 'top', axisLabel: { color: COR.tinta2, fontSize: 11, interval: 0 } }), yAxis: eixoCat(lin.map(l => l.c), { inverse: true, axisLabel: { color: COR.tinta2, fontSize: 11.5 } }),
      visualMap: { show: false, min: 0, max: 1, dimension: 2, inRange: { color: SEQ } },
      series: [{ id: 'm', type: 'heatmap', data: dados.map(d => ({ value: d, itemStyle: d[2] == null ? { color: '#F2F2F2' } : undefined, label: { color: d[2] != null && d[2] > .62 ? '#fff' : COR.tinta } })), label: { show: true, fontSize: 10.5, formatter: p => { const v = p.data.value[3], k = cols[p.data.value[0]][1]; return v == null ? '–' : MET[k] ? nf(v * 100, 0) : nf(v, 1); } },
        itemStyle: { borderColor: '#fff', borderWidth: 2, borderRadius: 3 }, emphasis: { itemStyle: { borderColor: COR.tinta, borderWidth: 1 } } }] }));
    g('mapac').resize();
    const c = g('mapac'); c.off('click'); c.on('click', p => { const l = lin[p.data.value[1]]; setFiltro({ cart: S.cart === l.c ? '' : l.c }); });
    registra('mapac', ['Carteira', 'Conversas', ...cols.map(c_ => c_[0])], lin.map(l => [l.c, l.conv, ...l.vals.map((v, j) => MET[cols[j][1]] ? pc(v) : nf(v, 2))]));
    html('n-mapac', `Taxas em % (rótulo sem o símbolo) e notas SPIN de 1 a 5. Ordenado pela taxa de fechamento. Carteiras com ao menos ${minConv()} conversas no período.`);
  },
};

/* ---------------- 6 · Clientes ---------------- */
const FILTROS_CLI = [['todos', 'Todos'], ['pend', 'Com pendência'], ['reinc', '2+ problemas'], ['s2', 'Sem 2ª tentativa'], ['ret', 'Retorno vencido'], ['fech', 'Fecharam']];
PAG.clientes = {
  esqueleto: () => kpis([{ id: 'cli', nome: 'Clientes contatados' }, { id: 'clia', nome: 'Clientes atendidos', dic: 'cli' }, { id: 'clip', nome: 'Clientes com problema', dic: 'prob' },
    { id: 'clir', nome: 'Com 2+ problemas', dic: 'k5' }, { id: 's2', nome: 'Sem 2ª tentativa' }, { id: 'ret', nome: 'Retornos no prazo' }]) +
    `<div class="grade">${card('conc', 'c4', 'Concentração do tempo', 'Horizontal = % dos clientes (dos que mais tomam tempo) · vertical = % do tempo', 260)}
    ${card('freq', 'c4', 'Tentativas por cliente', 'Quantos clientes receberam 1, 2, 3… tentativas', 260)}
    ${card('sinais', 'c4', 'Sinais nas conversas', '% das ligações analisadas (campos da análise)', 260)}
    ${cardHtml('tabcli', 'c12', 'Clientes', 'Código do cliente PJ · clique no cabeçalho para ordenar', pilulas('filtroCli', FILTROS_CLI, S.filtroCli))}</div>`,
  atualizar() {
    const CL = sel('CL'); const m = new Map();
    CL.forEach(r => { let x = m.get(r[2]); if (!x) m.set(r[2], x = { k: r[2], cod: D.clientes[r[2]], carts: new Map(), t: 0, a: 0, cv: 0, seg: 0, p: 0, pd: 0, o: 0, f: 0, ult: -1 }); x.carts.set(r[1], (x.carts.get(r[1]) || 0) + r[3]); x.t += r[3]; x.a += r[4]; x.cv += r[5]; x.seg += r[6]; x.p += r[7]; x.pd += r[8]; x.o += r[9]; x.f += r[10]; if (r[0] > x.ult) x.ult = r[0]; });
    const s2 = new Set(sel('S2').map(r => r[2])); const rv = new Map(); sel('R').forEach(r => { const a = rv.get(r[2]) || [0, 0]; a[0]++; a[1] += r[4]; rv.set(r[2], a); });
    const cl = [...m.values()]; cl.forEach(x => { x.cart = CART[[...x.carts.entries()].sort((a, b) => b[1] - a[1])[0][0]].c; x.s2 = s2.has(x.k); const r = rv.get(x.k); x.ret = r ? r[0] - r[1] : 0; x.h = x.seg / 3600; x.ultD = DIAS[x.ult]; });
    const nA = cl.filter(x => x.a > 0).length, nP = cl.filter(x => x.p > 0).length, nR = cl.filter(x => x.p >= 2).length;
    kpi('cli', comp(cl.length), '', `${nf(soma(cl.map(x => x.t)) / Math.max(1, cl.length), 1)} tentativas por cliente`, null);
    kpi('clia', comp(nA), '', `${pc(div(nA, cl.length))} dos contatados`, null);
    kpi('clip', comp(nP), '', `${pc(div(nP, nA))} dos atendidos`, null);
    kpi('clir', nf(nR), '', `${pc(div(soma(cl.filter(x => x.p >= 2).map(x => x.p)), soma(cl.map(x => x.p))))} dos problemas`, null);
    kpi('s2', nf(s2.size), '', 'uma tentativa sem sucesso, nenhuma outra', null);
    let dev = 0, np = 0; rv.forEach(a => { dev += a[0]; np += a[1]; });
    kpi('ret', pc(div(np, dev)), '', `${nf(dev)} retornos vencidos`, null);
    /* concentração */
    const segs = cl.map(x => x.seg).filter(v => v > 0).sort((a, b) => b - a); const tt = soma(segs);
    if (!(tt > 0)) vazioGrafico('conc', 'Sem tempo de conversa no período.');
    else {
      const pts = []; let ac = 0; const passo = Math.max(1, Math.floor(segs.length / 200)); pts.push([0, 0]);
      segs.forEach((v, i) => { ac += v; if (i % passo === 0 || i === segs.length - 1) pts.push([(i + 1) / segs.length, ac / tt]); });
      const em = q => { const k = Math.max(1, Math.floor(segs.length * q)); return soma(segs.slice(0, k)) / tt; };
      pinta('conc', base({ grid: { left: 6, right: 18, top: 16, bottom: 6, containLabel: true },
        tooltip: Object.assign({}, TT, { trigger: 'axis', formatter: ps => { const p = ps[0].data; return ttLinha(COR.verde, `do tempo está em ${pc(p[0], 0)} dos clientes`, pc(p[1], 0)); } }),
        xAxis: eixoVal(fmtPc0, { max: 1 }), yAxis: eixoVal(fmtPc0, { max: 1 }),
        series: [linha({ id: 'l', data: pts, showSymbol: false, lineStyle: { color: COR.verde, width: 2 }, areaStyle: { color: COR.verde, opacity: .08 } }), linha({ id: 'd', data: [[0, 0], [1, 1]], lineStyle: { color: COR.eixo, width: 1, type: [4, 4] }, silent: true, tooltip: { show: false } })] }));
      registra('conc', ['Top % dos clientes', '% do tempo'], [1, 5, 10, 20, 50].map(q => [q + '%', pc(em(q / 100))]));
      html('n-conc', `<b>${pc(em(.01), 0)}</b> do tempo está em 1% dos clientes; <b>${pc(em(.1), 0)}</b> em 10%.`);
    }
    /* frequência */
    const fq = [0, 0, 0, 0, 0]; cl.forEach(x => fq[Math.min(5, x.t) - 1]++);
    pinta('freq', base({ tooltip: Object.assign({}, TT, { trigger: 'item', formatter: p => ttTitulo(['1 tentativa', '2 tentativas', '3 tentativas', '4 tentativas', '5 ou mais'][p.dataIndex]) + ttLinha(COR.verde, 'clientes', nf(p.value)) }),
      xAxis: eixoCat(['1', '2', '3', '4', '5+']), yAxis: eixoVal(v => comp(v)), series: [barra({ id: 'f', data: fq, itemStyle: { color: COR.verde }, label: { show: true, position: 'top', formatter: p => comp(p.value), color: COR.tinta2, fontSize: 11 } })] }));
    registra('freq', ['Tentativas', 'Clientes'], fq.map((v, i) => [i < 4 ? String(i + 1) : '5+', v]));
    const t = C.t;
    barrasH('sinais', [['Tem frota própria', 'fp'], ['Aluga com concorrente', 'ac'], ['Falou com o decisor', 'dec'], ['Caiu na secretária eletrônica', 'sec']].map(([n, k]) => ({ nome: n, v: div(t[k + '_s'], t[k + '_n']), cor: COR.azul, tip: `${nf(t[k + '_s'])} de ${nf(t[k + '_n'])} análises` })).filter(x => x.v != null),
      { larg: 175, max: v => Math.min(1, v.max * 1.2), colNome: 'Sinal', colVal: '% das análises', vazio: 'Sem análises no período.' });
    html('n-sinais', 'Frota própria e concorrente vêm da análise da conversa e muitas vezes ficam sem informação: use como sinal, não como cadastro.');
    /* tabela */
    const f = S.filtroCli; const filtrado = cl.filter(x => f === 'todos' || (f === 'pend' && x.pd > 0) || (f === 'reinc' && x.p >= 2) || (f === 's2' && x.s2) || (f === 'ret' && x.ret > 0) || (f === 'fech' && x.f > 0));
    tabela(document.getElementById('h-tabcli'), { id: 'clientes', linhas: filtrado, chave: 'cod', unidade: 'clientes', placeholder: 'Buscar código ou carteira', ord: 'p', asc: false,
      colunas: [{ k: 'cod', t: 'Cliente', txt: true, busca: true }, { k: 'cart', t: 'Carteira', txt: true, busca: true }, { k: 't', t: 'Tentativas' }, { k: 'a', t: 'Atendidas' }, { k: 'cv', t: 'Conversas' },
        { k: 'h', t: 'Horas', f: v => nf(v, 1), csv: v => nf(v, 2) }, { k: 'p', t: 'Problemas', barra: true, cor: COR.verm }, { k: 'pd', t: 'Pendências' }, { k: 'o', t: 'Oportunidades' }, { k: 'f', t: 'Fechou' },
        { k: 'ultD', t: 'Último contato', f: v => dd(v), csv: v => ddmmaa(v) }, { k: 's2', t: 'Sinais', txt: true, f: (v, l) => (l.s2 ? '<span class="tag a">sem 2ª tentativa</span>' : '') + (l.ret ? '<span class="tag r">retorno vencido</span>' : '') + (l.p >= 2 ? '<span class="tag r">2+ problemas</span>' : '') + (l.f ? '<span class="tag v">fechou</span>' : ''), csv: (v, l) => [l.s2 ? 'sem 2ª tentativa' : '', l.ret ? 'retorno vencido' : '', l.p >= 2 ? '2+ problemas' : '', l.f ? 'fechou' : ''].filter(Boolean).join(' | ') }] });
    html('n-tabcli', `Código do cliente PJ (sem nome nem telefone). "Sem 2ª tentativa": uma tentativa ativa sem sucesso e nenhuma outra há ${CFG.dias_recontato}+ dias. "Retorno vencido": o cliente pediu retorno e a data passou sem nova ligação em até 2 dias.`);
  },
};

/* ---------------- 7 · Contato e cadência ---------------- */
PAG.contato = {
  esqueleto: () => kpis([{ id: 'tent', nome: 'Tentativas' }, { id: 'at', nome: 'Taxa de atendimento', dic: 'atend' }, { id: 'vd', nome: 'Tentativas por vendedor-dia', dic: 'tent' },
    { id: 'outb', nome: 'Ligações ativas', dic: 'tent' }, { id: 's2', nome: 'Clientes sem 2ª tentativa' }, { id: 'ret', nome: 'Retornos no prazo' }]) +
    `<div class="grade">${card('calor', 'c7', 'Quando o cliente atende', 'Taxa de atendimento por dia da semana e hora (Brasília)', 300)}
    ${card('hora', 'c5', 'Volume por hora', 'Tentativas atendidas e não atendidas', 300)}
    ${card('nt', 'c4', 'Atendimento por nº da tentativa', 'Ligações ativas ao mesmo cliente', 260)}
    ${card('status', 'c4', 'Status das tentativas', '', 260)}
    ${card('vdia', 'c4', 'Tentativas por vendedor-dia', 'Média por dia da semana', 260)}
    ${cardHtml('s2c', 'c6', 'Clientes sem 2ª tentativa', 'Uma tentativa ativa, sem sucesso, e nenhuma outra')}
    ${cardHtml('retc', 'c6', 'Retornos pedidos pelo cliente', 'Data sugerida já vencida')}</div>`,
  atualizar() {
    const t = C.t;
    kpiVol('tent', 'tent', `${nf(t.atend)} atendidas`);
    kpiTaxa('at', 'at', `${nf(t.sem_suc)} sem sucesso`);
    const vdias = C.rows.filter(r => r[IA.tent] > 0).length;
    kpi('vd', nf(div(t.tent, vdias), 1), '', `${nf(div(t.atend, vdias), 1)} atendidas por vendedor-dia`, C.baldes.map(b => ({ rot: b.rot, v: div(b.t.tent, b.rows.filter(r => r[IA.tent] > 0).length) })), COR.verde, v => nf(v, 1));
    kpiTaxa('outb', 'outb', `atendimento nas ativas ${pc(div(t.outb_a, t.outb))}`, COR.azul);
    const s2 = sel('S2').length; const T = new Map(); sel('T').forEach(r => { const a = T.get(r[2]) || [0, 0]; a[0] += r[3]; a[1] += r[4]; T.set(r[2], a); });
    const t2 = T.get(2) ? div(T.get(2)[1], T.get(2)[0]) : null;
    kpi('s2', nf(s2), '', t2 != null ? `≈ ${nf(s2 * t2)} conversas se ligar de novo` : '', null);
    let dev = 0, np = 0; const pu = [[0, 0], [0, 0], [0, 0], [0, 0]]; sel('R').forEach(r => { dev++; np += r[4]; const u = r[3] < 0 ? 3 : r[3]; pu[u][0]++; pu[u][1] += r[4]; });
    kpi('ret', pc(div(np, dev)), '', `${nf(dev)} retornos vencidos`, null);
    /* calor */
    const H = new Map(); sel('H').forEach(r => { const k = DOWI[r[0]] + '|' + r[2]; const a = H.get(k) || [0, 0]; a[0] += r[3]; a[1] += r[4]; H.set(k, a); });
    const tH = new Map(); H.forEach((a, k) => { const h = +k.split('|')[1]; tH.set(h, (tH.get(h) || 0) + a[0]); }); const hOk = [...tH.entries()].filter(([, n]) => n >= 50).map(([h]) => h);
    const horas = []; if (hOk.length) for (let h = Math.min(...hOk); h <= Math.max(...hOk); h++) horas.push(h); const dias = [1, 2, 3, 4, 5]; const dados = [];
    dias.forEach((d, yi) => horas.forEach((h, xi) => { const a = H.get(d + '|' + h) || [0, 0]; dados.push([xi, yi, a[0] >= 20 ? +(a[1] / a[0]).toFixed(4) : null, a[0], a[1]]); }));
    if (!dados.some(d => d[2] != null)) vazioGrafico('calor', 'Poucas tentativas no período para o mapa.');
    else {
      const vs = dados.filter(d => d[2] != null).map(d => d[2]);
      pinta('calor', base({ grid: { left: 6, right: 12, top: 8, bottom: 44, containLabel: true },
        tooltip: Object.assign({}, TT, { trigger: 'item', formatter: p => { const d = p.data.value || p.data; return ttTitulo(`${DSEM[dias[d[1]]]} · ${horas[d[0]]}h`) + ttLinha(COR.verde, 'atendidas', d[2] == null ? 'amostra pequena' : pc(d[2])) + `<div style="color:${COR.mudo};margin-top:3px">${nf(d[4])} de ${nf(d[3])} tentativas</div>`; } }),
        xAxis: eixoCat(horas.map(h => h + 'h')), yAxis: eixoCat(dias.map(d => DSEM[d]), { inverse: true }),
        visualMap: { min: Math.min(...vs), max: Math.max(...vs), dimension: 2, orient: 'horizontal', left: 'center', bottom: 0, itemWidth: 12, itemHeight: 140, inRange: { color: SEQ }, text: [pc(Math.max(...vs), 0), pc(Math.min(...vs), 0)], textStyle: { color: COR.mudo, fontSize: 11 } },
        series: [{ id: 'c', type: 'heatmap', data: dados.map(d => d[2] == null ? { value: d, itemStyle: { color: '#F2F2F2' } } : { value: d, label: { color: (d[2] - Math.min(...vs)) / Math.max(1e-9, Math.max(...vs) - Math.min(...vs)) > .62 ? '#fff' : COR.tinta } }), label: { show: true, fontSize: 10, formatter: p => { const d = p.data.value || p.data; return d[2] == null ? '' : nf(d[2] * 100, 0); } },
          itemStyle: { borderColor: '#fff', borderWidth: 2, borderRadius: 3 }, emphasis: { itemStyle: { borderColor: COR.tinta, borderWidth: 1 } } }] }));
      registra('calor', ['Dia', ...horas.map(h => h + 'h')], dias.map((d, yi) => [DSEM[d], ...horas.map((h, xi) => { const v = dados[yi * horas.length + xi]; return v[2] == null ? '' : pc(v[2], 0); })]));
      html('n-calor', 'Células com menos de 20 tentativas ficam em branco. Rótulo = % atendidas.');
    }
    /* volume por hora */
    const hh = new Map(); sel('H').forEach(r => { const a = hh.get(r[2]) || [0, 0]; a[0] += r[3]; a[1] += r[4]; hh.set(r[2], a); });
    const hs_ = [...hh.keys()].filter(h => hh.get(h)[0] >= 20).sort((a, b) => a - b); const hv = hs_.map(h => hh.get(h));
    pinta('hora', base({ grid: { left: 6, right: 16, top: 34, bottom: 6, containLabel: true }, legend: { top: 0, left: 0, itemWidth: 10, itemHeight: 10, textStyle: { fontSize: 12, color: COR.tinta2 } },
      tooltip: Object.assign({}, TT, { trigger: 'axis', formatter: ps => { const a = hv[ps[0].dataIndex]; return ttTitulo(hs_[ps[0].dataIndex] + 'h') + ttLinha(COR.verde, 'atendidas', nf(a[1]), pc(div(a[1], a[0]), 0)) + ttLinha(COR.cinza, 'não atendidas', nf(a[0] - a[1])); } }),
      xAxis: eixoCat(hs_.map(h => h + 'h')), yAxis: eixoVal(v => comp(v)),
      series: [barra({ id: 'a', name: 'Atendidas', stack: 'h', data: hv.map(a => a[1]), itemStyle: { color: COR.verde, borderRadius: 0 } }), barra({ id: 'n', name: 'Não atendidas', stack: 'h', data: hv.map(a => a[0] - a[1]), itemStyle: { color: COR.cinzaClaro } })] }));
    registra('hora', ['Hora', 'Tentativas', 'Atendidas', '% atendidas'], hs_.map((h, i) => [h + 'h', hv[i][0], hv[i][1], pc(div(hv[i][1], hv[i][0]))]));
    /* nº da tentativa */
    const nts = [1, 2, 3, 4, 5].filter(n => T.has(n)).map(n => ({ n, t: T.get(n)[0], a: T.get(n)[1] }));
    if (!nts.length) vazioGrafico('nt', 'Sem ligações ativas com código de cliente.');
    else {
      pinta('nt', base({ tooltip: Object.assign({}, TT, { trigger: 'item', formatter: p => { const x = nts[p.dataIndex]; return ttTitulo(x.n < 5 ? x.n + 'ª tentativa' : '5ª ou mais') + ttLinha(COR.verde, 'atendidas', pc(div(x.a, x.t))) + `<div style="color:${COR.mudo};margin-top:3px">${nf(x.a)} de ${nf(x.t)}</div>`; } }),
        xAxis: eixoCat(nts.map(x => x.n < 5 ? x.n + 'ª' : '5ª+')), yAxis: eixoVal(fmtPc0),
        series: [barra({ id: 'nt', data: nts.map(x => div(x.a, x.t)), itemStyle: { color: COR.verde }, label: { show: true, position: 'top', formatter: p => pc(p.value), color: COR.tinta2, fontSize: 11 } })] }));
      registra('nt', ['Tentativa', 'Ligações', 'Atendidas', '%'], nts.map(x => [x.n < 5 ? x.n + 'ª' : '5ª+', x.t, x.a, pc(div(x.a, x.t))]));
    }
    /* status */
    const bs = C.baldes; const st = [['Atendida', 'atend', COR.verde], ['Sem sucesso', 'sem_suc', COR.cinza], ['Em aberto', 'open', COR.cinzaClaro]];
    pinta('status', base({ grid: { left: 6, right: 16, top: 34, bottom: 6, containLabel: true }, legend: { top: 0, left: 0, itemWidth: 10, itemHeight: 10, textStyle: { fontSize: 12, color: COR.tinta2 } },
      tooltip: Object.assign({}, TT, { trigger: 'axis', formatter: ps => { const b = bs[ps[0].dataIndex]; return ttTitulo(b.rot) + st.map(x => ttLinha(x[2], x[0], pc(div(b.t[x[1]], b.t.tent)), nf(b.t[x[1]]))).join(''); } }),
      xAxis: eixoCat(bs.map(b => b.rot)), yAxis: eixoVal(fmtPc0, { max: 1 }),
      series: st.map((x, i) => barra({ id: 's' + i, name: x[0], stack: 's', data: bs.map(b => div(b.t[x[1]], b.t.tent)), itemStyle: { color: x[2], borderRadius: 0, borderColor: '#fff', borderWidth: 1 }, barMaxWidth: 30 })) }));
    texto('s-status', `% das tentativas por ${S.gran === 'dia' ? 'dia' : S.gran === 'semana' ? 'semana' : 'mês'}`);
    registra('status', ['Período', ...st.map(x => x[0])], bs.map(b => [b.rot, ...st.map(x => pc(div(b.t[x[1]], b.t.tent)))]));
    /* vendedor-dia */
    const vd = new Map(); C.rows.forEach(r => { if (r[IA.tent] <= 0) return; const d = DOWI[r[0]]; const a = vd.get(d) || [0, 0, 0]; a[0] += r[IA.tent]; a[1] += r[IA.atend]; a[2]++; vd.set(d, a); });
    const ds = [1, 2, 3, 4, 5].filter(d => vd.has(d));
    pinta('vdia', base({ grid: { left: 6, right: 16, top: 34, bottom: 6, containLabel: true }, legend: { top: 0, left: 0, itemWidth: 10, itemHeight: 10, textStyle: { fontSize: 12, color: COR.tinta2 } },
      tooltip: Object.assign({}, TT, { trigger: 'axis', formatter: ps => { const a = vd.get(ds[ps[0].dataIndex]); return ttTitulo(DSEM[ds[ps[0].dataIndex]]) + ttLinha(COR.azul, 'tentativas', nf(a[0] / a[2], 1)) + ttLinha(COR.verde, 'atendidas', nf(a[1] / a[2], 1)) + `<div style="color:${COR.mudo};margin-top:3px">${nf(a[2])} vendedor-dias</div>`; } }),
      xAxis: eixoCat(ds.map(d => DSEM[d])), yAxis: eixoVal(v => nf(v)),
      series: [barra({ id: 't', name: 'Tentativas', data: ds.map(d => +(vd.get(d)[0] / vd.get(d)[2]).toFixed(1)), itemStyle: { color: COR.azul } }), barra({ id: 'a', name: 'Atendidas', data: ds.map(d => +(vd.get(d)[1] / vd.get(d)[2]).toFixed(1)), itemStyle: { color: COR.verde } })] }));
    registra('vdia', ['Dia', 'Tentativas por vendedor-dia', 'Atendidas por vendedor-dia'], ds.map(d => [DSEM[d], nf(vd.get(d)[0] / vd.get(d)[2], 1), nf(vd.get(d)[1] / vd.get(d)[2], 1)]));
    html('h-s2c', `<div class="numeros"><div><b>${nf(s2)}</b><span>clientes</span></div><div><b>${t2 == null ? '–' : '≈ ' + nf(s2 * t2)}</b><span>conversas se a 2ª tentativa for feita<br>(${pc(t2)} atendem na 2ª)</span></div></div><div class="nota"><a href="#" data-ir-cli="s2">Ver a lista na página de clientes →</a></div>`);
    html('h-retc', `<div class="numeros"><div><b>${nf(dev)}</b><span>retornos vencidos</span></div><div><b>${pc(div(np, dev))}</b><span>feitos no prazo (+2 dias)</span></div></div><div class="nota">Por urgência 1–3 / 4–6 / 7–10: <b>${pu.slice(0, 3).map(a => pc(div(a[1], a[0]), 0)).join(' / ')}</b>. <a href="#" data-ir-cli="ret">Ver clientes com retorno vencido →</a></div>`);
  },
};

/* ---------------- 8 · Carteiras ---------------- */
const METS_CART = [['k1', 'Carga operacional'], ['fech', 'Fechamento'], ['prob', 'Problemas'], ['res', 'Resolução'], ['chAlta', 'Challenger alta'], ['at', 'Atendimento']];
PAG.carteiras = {
  esqueleto: () => `<div id="ficha"></div><div class="grade">${card('disp', 'c8', 'Volume × indicador', 'Horizontal = conversas · vertical = indicador · tamanho = horas · clique para abrir a ficha', 320, pilulas('metCart', METS_CART, S.metCart))}
    ${card('distr', 'c4', 'Distritais', 'Mesmo indicador · clique para filtrar', 352)}
    ${cardHtml('tabcart', 'c12', 'Todas as carteiras', 'Clique numa linha para abrir a ficha da carteira · cinza = menos de ' + minConv() + ' conversas')}</div>`,
  atualizar() {
    const k = S.metCart; const porC = agrupa(sel('A', S.d0, S.d1, true), r => r[1]); const antes = C.jc ? agrupa(sel('A', C.jc.r0, C.jc.r1, true), r => r[1]) : new Map();
    const lin = []; porC.forEach((rs, ci) => { const a = somaA(rs), b = antes.has(ci) ? somaA(antes.get(ci)) : null;
      const dK1 = b ? deltaTaxa('k1', a, b) : null, dF = b ? deltaTaxa('fech', a, b) : null;
      lin.push({ c: CART[ci].c, d: CART[ci].d, conv: a.conv, h: a.seg_base / 3600, k1: tx(a, 'k1'), dk1: dK1 ? dK1.d : null, dk1s: dK1, fech: tx(a, 'fech'), dfech: dF ? dF.d : null, dfechs: dF, prob: tx(a, 'prob'), res: tx(a, 'res'), chAlta: tx(a, 'chAlta'), sf: media(a, 'sf'), at: tx(a, 'at'), t: a }); });
    const ok = lin.filter(l => l.conv >= minConv());
    /* dispersão */
    const pts = ok.filter(l => l[k] != null);
    if (!pts.length) vazioGrafico('disp', `Nenhuma carteira com ${minConv()} ou mais conversas no período.`);
    else {
      const med = mediana(pts.map(p => p[k])), mx = Math.max(1, ...pts.map(p => p.h)); const ruim = MET[k].bom < 0;
      const ord_ = [...pts].sort((a, b) => a[k] - b[k]); const extremos = new Set([...ord_.slice(0, 3), ...ord_.slice(-3)].map(p => p.c));
      pinta('disp', base({ grid: { left: 6, right: 30, top: 24, bottom: 24, containLabel: true },
        tooltip: Object.assign({}, TT, { trigger: 'item', formatter: p => { const x = pts[p.dataIndex]; return ttTitulo(`${x.c} · ${x.d}`) + ttLinha(ruim ? COR.verm : COR.verde, nomeMet(k), pc(x[k])) + `<div style="color:${COR.mudo};margin-top:3px">${nf(x.conv)} conversas · ${nf(x.h, 1)} h</div>`; } }),
        xAxis: eixoVal(v => nf(v)), yAxis: eixoVal(fmtPc0, { scale: true }),
        series: [{ id: 's', type: 'scatter', data: pts.map(p => [p.conv, p[k]]), symbolSize: (v, p) => 9 + 20 * Math.sqrt(pts[p.dataIndex].h / mx),
          itemStyle: { color: p => { const x = pts[p.dataIndex]; if (x.c === S.cart) return COR.noite; const acima = x[k] - med; return Math.abs(acima) < .03 ? COR.cinza : ((acima > 0) === ruim ? COR.verm : COR.verde); }, opacity: .82, borderColor: '#fff', borderWidth: 2 },
          label: { show: true, position: 'right', fontSize: 10.5, color: COR.tinta2, formatter: p => { const x = pts[p.dataIndex]; return extremos.has(x.c) || x.c === S.cart ? x.c : ''; } },
          markLine: linhaRef(med, 'mediana ' + pc(med)) }] }));
      const c = g('disp'); c.off('click'); c.on('click', p => setFiltro({ cart: S.cart === pts[p.dataIndex].c ? '' : pts[p.dataIndex].c }));
      registra('disp', ['Carteira', 'Distrital', 'Conversas', nomeMet(k)], pts.map(p => [p.c, p.d, p.conv, pc(p[k])]));
      html('n-disp', `Verde = melhor que a mediana; vermelho = pior; cinza = a até 3 p.p. da mediana.`);
    }
    /* distritais */
    const todosD = agrupa(D.A.filter(r => r[0] >= S.d0 && r[0] <= S.d1), r => CART[r[1]].d);
    barrasH('distr', DIST.map(d => { const a = somaA(todosD.get(d) || []); return { nome: d, v: tx(a, k), cor: S.dist && S.dist !== d ? COR.cinzaClaro : (MET[k].bom < 0 ? COR.verm : COR.verde), tip: `n = ${nf(nEf(a, k))}` }; }).filter(x => x.v != null),
      { larg: 60, colNome: 'Distrital', colVal: nomeMet(k), clique: x => setFiltro({ dist: S.dist === x.nome ? '' : x.nome, cart: '' }) });
    /* tabela */
    const dfmt = (d) => d ? `<span class="delta ${d.classe}" style="font-size:11px">${seta(d)} ${pp(d.d, 1)}</span>` : '';
    tabela(document.getElementById('h-tabcart'), { id: 'carteiras', linhas: lin, chave: 'c', unidade: 'carteiras', placeholder: 'Buscar carteira', ord: 'k1', asc: false, limite: 200, altura: 600,
      sel: l => l.c === S.cart, fraco: l => l.conv < minConv(), clique: c => setFiltro({ cart: S.cart === c ? '' : c }),
      colunas: [{ k: 'c', t: 'Carteira', txt: true, busca: true }, { k: 'd', t: 'Distrital', txt: true, busca: true }, { k: 'conv', t: 'Conversas', barra: true }, { k: 'h', t: 'Horas', f: v => nf(v, 1), csv: v => nf(v, 2) },
        { k: 'k1', t: 'Carga op.', f: v => pc(v), csv: v => pc(v) }, { k: 'dk1', t: 'Δ carga', f: (v, l) => dfmt(l.dk1s), csv: v => pp(v), dica: 'Variação contra a comparação escolhida no topo' },
        { k: 'fech', t: 'Fechamento', f: v => pc(v), csv: v => pc(v) }, { k: 'dfech', t: 'Δ fech.', f: (v, l) => dfmt(l.dfechs), csv: v => pp(v) },
        { k: 'prob', t: '% problema', f: v => pc(v), csv: v => pc(v) }, { k: 'res', t: 'Resolvidos', f: v => pc(v), csv: v => pc(v) }, { k: 'chAlta', t: 'Challenger alta', f: v => pc(v), csv: v => pc(v) },
        { k: 'sf', t: 'SPIN final', f: v => nf(v, 2), csv: v => nf(v, 2) }, { k: 'at', t: 'Atendimento', f: v => pc(v), csv: v => pc(v) }] });
    /* ficha */
    if (!S.cart) { html('ficha', `<div class="faixa-info">Clique numa carteira (no gráfico ou na tabela) para abrir a ficha dela comparada à mediana das carteiras.</div>`); return; }
    const me = lin.find(l => l.c === S.cart); if (!me) { html('ficha', ''); return; }
    const medDe = key => mediana(ok.map(l => l[key]));
    const itens = [['Conversas', nf(me.conv), `mediana ${nf(medDe('conv'))}`], ['Carga operacional', pc(me.k1), `mediana ${pc(medDe('k1'))}`, me.dk1s], ['Taxa de fechamento', pc(me.fech), `mediana ${pc(medDe('fech'))}`, me.dfechs],
      ['Conversas com problema', pc(me.prob), `mediana ${pc(medDe('prob'))}`], ['Resolvidos na ligação', pc(me.res), `mediana ${pc(medDe('res'))}`], ['Challenger alta', pc(me.chAlta), `mediana ${pc(medDe('chAlta'))}`],
      ['SPIN nota final', nf(me.sf, 2), `mediana ${nf(medDe('sf'), 2)}`], ['Atendimento', pc(me.at), `mediana ${pc(medDe('at'))}`]];
    html('ficha', `<div class="card" style="margin-bottom:14px"><div class="card-cab"><div><h2>Ficha da carteira ${esc(me.c)} · ${esc(me.d)}</h2><p>Período escolhido · comparação com a mediana das carteiras com ${minConv()}+ conversas${C.jc ? ' e com ' + esc(C.jc.rot) : ''}</p></div><div class="acoes"><button type="button" data-tira-cart>Fechar ficha</button></div></div>
      <div class="kpis" style="margin:0">${itens.map(x => `<div class="kpi"><div class="lab"><span>${x[0]}</span></div><div class="val">${x[1]}</div><div class="linha">${x[3] ? chipDelta(x[3], C.rot) : ''}<span class="sub">${x[2]}</span></div></div>`).join('')}</div>
      <div class="nota">Todas as outras páginas também estão filtradas por esta carteira enquanto a ficha estiver aberta.</div></div>`);
  },
};

/* ---------------- 9 · Qualidade do dado ---------------- */
PAG.qualidade = {
  esqueleto: () => kpis([{ id: 'c1', nome: 'Cobertura de classificação' }, { id: 'c2', nome: 'Cobertura de duração' }, { id: 'gem', nome: 'Atendidas sem análise Gemini', dic: 'c1' },
    { id: 'atual', nome: 'Atualização do painel', dic: 'c1' }, { id: 'uso', nome: 'Uso do painel (7 dias)', dic: 'c1' }]) +
    `<div class="grade">${card('cob', 'c8', 'Cobertura por dia', 'Atendidas com classificação, com duração e com análise Gemini', 280)}
    ${card('uso', 'c4', 'Acessos ao painel', 'Registrados pelo "Abrir painel.bat" (só contagens)', 280)}
    ${cardHtml('diag', 'c6', 'Verificações da carga', 'Arquivo inteiro, refeito a cada atualização')}
    ${card('sent', 'c6', 'Campos com valor-sentinela', '% das linhas com "sem dados necessários" ou equivalente', 280)}
    ${cardHtml('dic', 'c12', 'Dicionário dos indicadores', 'As mesmas definições do memo da RMR')}</div>`,
  atualizar() {
    const t = C.t; const lim = CFG.limite_cobertura;
    kpiTaxa('c1', 'c1', `meta ≥ ${pc(lim, 0)} · ${nf(t.atend - t.comp_cls)} sem classificação`);
    kpiTaxa('c2', 'c2', `${nf(t.atend - t.comp_dur)} sem duração`);
    kpi('gem', nf(t.atend - t.comp_gem), '', `${pc(div(t.atend - t.comp_gem, t.atend))} das atendidas`, null);
    kpi('atual', D.meta.gerado_em.slice(8, 10) + '/' + D.meta.gerado_em.slice(5, 7) + ' ' + D.meta.gerado_em.slice(11), '', `dados até ${ddmmaa(D.meta.dados_ate)}`, null);
    const u = D.uso; kpi('uso', u && u.acessos_total ? nf(u.pessoas_7d) + ' pessoas' : '–', '', u && u.acessos_total ? `${nf(u.acessos_7d)} acessos · ${nf(u.pessoas_total)} pessoas desde o início` : 'nenhum acesso registrado ainda', null);
    const pd = agrupa(C.rows, r => r[0]); const ds = [...pd.keys()].sort((a, b) => a - b).map(i => ({ d: DIAS[i], t: somaA(pd.get(i)) }));
    const sr = [['Classificação', 'comp_cls', COR.noite], ['Duração', 'comp_dur', COR.lima], ['Análise Gemini', 'comp_gem', COR.azul]];
    pinta('cob', base({ grid: { left: 6, right: 16, top: 34, bottom: 6, containLabel: true }, legend: { top: 0, left: 0, itemWidth: 14, itemHeight: 3, textStyle: { fontSize: 12, color: COR.tinta2 } },
      tooltip: Object.assign({}, TT, { trigger: 'axis', formatter: ps => { const x = ds[ps[0].dataIndex]; return ttTitulo(dd(x.d)) + sr.map(s => ttLinha(s[2], s[0], pc(div(x.t[s[1]], x.t.atend)))).join('') + `<div style="color:${COR.mudo};margin-top:3px">${nf(x.t.atend)} atendidas</div>`; } }),
      xAxis: eixoCat(ds.map(x => dd(x.d)), { boundaryGap: false }), yAxis: eixoVal(fmtPc0, { max: 1 }),
      series: sr.map((s, i) => linha({ id: 'c' + i, name: s[0], data: ds.map(x => div(x.t[s[1]], x.t.atend)), lineStyle: { width: 2, color: s[2] }, itemStyle: { color: s[2] }, markLine: i === 0 ? linhaRef(lim, 'meta ' + pc(lim, 0)) : undefined })) }));
    registra('cob', ['Dia', ...sr.map(s => s[0]), 'Atendidas'], ds.map(x => [dd(x.d), ...sr.map(s => pc(div(x.t[s[1]], x.t.atend))), x.t.atend]));
    const pdia = (u && u.por_dia) || [];
    if (!pdia.length) vazioGrafico('uso', 'Nenhum acesso registrado ainda. Os acessos aparecem depois que alguém abrir pelo "Abrir painel.bat" e a atualização seguinte rodar.');
    else {
      pinta('uso', base({ tooltip: Object.assign({}, TT, { trigger: 'axis', formatter: ps => { const x = pdia[ps[0].dataIndex]; return ttTitulo(dd(x.dia)) + ttLinha(COR.verde, 'acessos', nf(x.acessos)) + ttLinha(COR.azul, 'pessoas', nf(x.pessoas)); } }),
        xAxis: eixoCat(pdia.map(x => dd(x.dia))), yAxis: eixoVal(v => nf(v)), series: [barra({ id: 'u', name: 'Acessos', data: pdia.map(x => x.acessos), itemStyle: { color: COR.verde } })] }));
      registra('uso', ['Dia', 'Acessos', 'Pessoas'], pdia.map(x => [dd(x.dia), x.acessos, x.pessoas]));
    }
    const dg = D.diag; const pill = s => s === 'ok' ? '<span class="tag v">OK</span>' : s === 'at' ? '<span class="tag a">ATENÇÃO</span>' : s === 'cr' ? '<span class="tag r">CRÍTICO</span>' : '';
    const lin = [['Linhas lidas do arquivo', dg.linhas, dg.linhas, '', null], ['id_transcricao duplicado', dg.dup, dg.linhas, dg.dup > 0 ? 'cr' : 'ok', 0], ['Atendidas sem segment_id', dg.comp_sem_seg, dg.comp, dg.comp_sem_seg / dg.comp > .02 ? 'cr' : 'ok', .02],
      ['Atendidas sem análise Gemini', dg.sem_gem, dg.comp, dg.sem_gem / dg.comp > .1 ? 'at' : 'ok', .1], ['Atendidas sem classificação', dg.sem_cls, dg.comp, dg.sem_cls / dg.comp > .05 ? 'cr' : 'ok', .05],
      ['Atendidas sem duração', dg.sem_dur, dg.comp, dg.sem_dur / dg.comp > .05 ? 'cr' : 'ok', .05], ['Linhas sem código de cliente', dg.sem_cod, dg.linhas, dg.sem_cod / dg.linhas > .1 ? 'at' : 'ok', .1]];
    html('h-diag', `<div class="tab-wrap" style="max-height:none"><table class="tb"><thead><tr><th>Verificação</th><th>Falhas</th><th>Base</th><th>%</th><th>Limite</th><th>Status</th></tr></thead><tbody>${lin.map(l => `<tr><td>${l[0]}</td><td>${nf(l[1])}</td><td>${nf(l[2])}</td><td>${pc(div(l[1], l[2]))}</td><td>${l[4] == null ? '' : pc(l[4], 0)}</td><td>${pill(l[3])}</td></tr>`).join('')}</tbody></table></div>`);
    html('n-diag', `Arquivo de ${ddmmaa(D.meta.inicio)} a ${ddmmaa(D.meta.dados_ate)} · duração até ${ddmmaa(D.meta.duracao_ate)} · classificação até ${ddmmaa(D.meta.classif_ate)} · análise Gemini até ${ddmmaa(D.meta.gemini_ate)}.${dg.colunas_ausentes && dg.colunas_ausentes.length ? ' Colunas ausentes no CSV: ' + esc(dg.colunas_ausentes.join(', ')) + '.' : ''}`);
    barrasH('sent', (D.sentinelas || []).map(s => ({ nome: s.campo, v: s.pct, cor: s.pct > .8 ? COR.verm : COR.vermClaro })), { larg: 190, max: 1, colNome: 'Campo', colVal: '% sentinela' });
    html('n-sent', 'Campos que parecem preenchidos mas não informam nada: não usar em decisão.');
    html('h-dic', `<div class="tab-wrap" style="max-height:none"><table class="tb"><thead><tr><th class="txt">Indicador</th><th class="txt">Definição</th><th class="txt">Colunas do CSV</th></tr></thead><tbody>${Object.values(DIC).map(d => `<tr><td class="txt"><b>${esc(d[0])}</b></td><td class="txt" style="white-space:normal">${esc(d[1])}</td><td class="txt" style="white-space:normal;color:${COR.mudo}">${esc(d[2])}</td></tr>`).join('')}</tbody></table></div>`);
  },
};

/* ---------------- 10 · Configurações ---------------- */
const NOMES_MES = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'];
const rotMes = m => NOMES_MES[+m.slice(5, 7) - 1] + '/' + m.slice(0, 4);
const fimMes = m => { const d = new Date(m + '-01T12:00:00'); d.setMonth(d.getMonth() + 1); d.setDate(0); return d.toISOString().slice(0, 10); };
const diasUteis = (a, b) => { let n = 0; for (let s = a; s <= b; s = dataMais(s, 1)) { const w = new Date(s + 'T12:00:00').getDay(); if (w && w < 6) n++; } return n; };
let RASC = null; /* rascunho da baseline em edição */
const rotJanela = c => { const datas = `${ddmmaa(c.baseline_inicio)} a ${ddmmaa(c.baseline_fim)}`; return c.baseline_rotulo === datas ? datas : `${c.baseline_rotulo} (${datas})`; };
function resumoJanela(ini, fim) {
  const r0 = idxDe(ini), r1 = idxAte(fim);
  const rows = r0 <= r1 && r0 < ND ? D.A.filter(r => r[0] >= r0 && r[0] <= r1) : [];
  const t = somaA(rows);
  const avisos = [];
  if (!rows.length) avisos.push('sem dados nesse período');
  else {
    const uteis = diasUteis(ini < DIAS[0] ? DIAS[0] : ini, fim > DIAS[ND - 1] ? DIAS[ND - 1] : fim);
    if (ini < DIAS[0] || fim > DIAS[ND - 1]) avisos.push('parte do período está fora dos dados');
    if (t._dias < Math.max(5, uteis * .8)) avisos.push(`só ${t._dias} dias com dado`);
    if (tx(t, 'c1') != null && tx(t, 'c1') < CFG.limite_cobertura) avisos.push(`classificação cobre ${pc(tx(t, 'c1'), 0)} das atendidas`);
    if (tx(t, 'c2') != null && tx(t, 'c2') < CFG.limite_cobertura) avisos.push(`duração cobre ${pc(tx(t, 'c2'), 0)} das atendidas`);
  }
  return { t, avisos, dias: t._dias };
}
PAG.config = {
  esqueleto: () => `<div class="grade">${cardHtml('cfgbase', 'c7', 'Baseline', 'O período que serve de referência nas comparações')}
    ${cardHtml('cfgpar', 'c5', 'Parâmetros de análise', 'Valem para rankings, medianas e avisos de amostra')}
    ${cardHtml('cfgmeses', 'c12', 'Meses disponíveis nos dados', 'Para escolher a baseline: prefira um mês completo, com cobertura alta e volume normal · clique numa linha para usar o mês')}
    ${cardHtml('cfgofic', 'c12', 'Tornar oficial para todos', 'A baseline oficial é a mesma para todos os leitores e vem do arquivo painel_config.json')}</div>`,
  atualizar() {
    if (!RASC) RASC = { inicio: CFG.baseline_inicio, fim: CFG.baseline_fim, rotulo: CFG.baseline_rotulo, rotManual: false };
    const pessoal = basePessoal();
    const meses = [...new Set(DIAS.map(d => d.slice(0, 7)))].sort().reverse();
    const r = resumoJanela(RASC.inicio, RASC.fim);
    const mesSel = meses.find(m => RASC.inicio === m + '-01' && RASC.fim === fimMes(m)) || '';
    const igualAtual = RASC.inicio === CFG.baseline_inicio && RASC.fim === CFG.baseline_fim && RASC.rotulo === CFG.baseline_rotulo;
    html('h-cfgbase', `<div class="faixa-info texto" style="margin-bottom:10px">${pessoal
      ? `Você está usando uma <b>baseline pessoal</b>: ${esc(rotJanela(CFG))}. A oficial é ${esc(rotJanela(CFG_OFICIAL))}. Só você vê esta escolha. <button type="button" data-cfg-acao="oficial">voltar à oficial</button>`
      : `Em uso: <b>baseline oficial ${esc(rotJanela(CFG))}</b>, a mesma para todos os leitores.`}</div>
      <div class="form-cfg">
        <label>Mês<select data-cfg="mes"><option value="">Período personalizado</option>${meses.map(m => `<option value="${m}"${m === mesSel ? ' selected' : ''}>${esc(rotMes(m))}</option>`).join('')}</select></label>
        <label>De<input type="date" data-cfg="inicio" value="${RASC.inicio}"></label>
        <label>Até<input type="date" data-cfg="fim" value="${RASC.fim}"></label>
        <label class="largo">Nome que aparece no painel<input type="text" data-cfg="rotulo" value="${esc(RASC.rotulo)}" maxlength="40"></label>
      </div>
      <div class="nota" style="margin:8px 0">${r.dias ? `No período escolhido: <b>${nf(r.dias)}</b> dias com dado · ${nf(r.t.an)} ligações analisadas · ${nf(r.t.conv)} conversas · fechamento ${pc(tx(r.t, 'fech'))} · problema ${pc(tx(r.t, 'prob'))} · carga operacional ${pc(tx(r.t, 'k1'))}.` : ''}
        ${r.avisos.length ? `<br><span class="tag r">atenção</span> ${esc(r.avisos.join(' · '))}.` : r.dias ? ' <span class="tag v">período bom para baseline</span>' : ''}</div>
      <div class="controles"><button type="button" class="pilula on" data-cfg-acao="aplicar"${igualAtual || !r.dias ? ' disabled' : ''}>Usar esta baseline (só para mim)</button>${pessoal ? '<button type="button" class="pilula" data-cfg-acao="oficial">Voltar à baseline oficial</button>' : ''}</div>`);
    html('n-cfgbase', 'A baseline entra nos cartões ("Comparar com: Baseline"), nas linhas tracejadas e no período "Baseline" do topo. Cada carteira e distrital é comparada com o próprio desempenho nesse período.');
    /* parâmetros */
    html('h-cfgpar', `<div class="form-cfg">
        <label>Mínimo de conversas por carteira<input type="number" min="5" max="500" step="5" data-cfg="min_ligacoes" value="${CFG.min_ligacoes}"></label>
        <label>Amostra mínima de uma taxa<input type="number" min="5" max="500" step="5" data-cfg="min_n_taxa" value="${CFG.min_n_taxa}"></label>
        <label>Meta de cobertura (%)<input type="number" min="50" max="100" step="1" data-cfg="limite_cobertura" value="${Math.round(CFG.limite_cobertura * 100)}"></label>
      </div>
      <div class="nota">Oficial: ${CFG_OFICIAL.min_ligacoes} conversas · amostra ${CFG_OFICIAL.min_n_taxa} · cobertura ${pc(CFG_OFICIAL.limite_cobertura, 0)}. Mudanças aqui valem só para você e na hora.${['min_ligacoes', 'min_n_taxa', 'limite_cobertura'].some(k => k in CFG_PESSOAL) ? ' <button type="button" class="link" data-cfg-acao="paroficial">Voltar aos parâmetros oficiais</button>' : ''}</div>`);
    /* meses */
    const porMes = agrupa(D.A, r_ => DIAS[r_[0]].slice(0, 7));
    const linhas = meses.map(m => { const t = somaA(porMes.get(m) || []); const fim = fimMes(m); const uteis = diasUteis(m + '-01', fim);
      const inc = fim > DIAS[ND - 1] || (m + '-01') < DIAS[0] || t._dias < uteis * .8;
      const c1 = tx(t, 'c1'), c2 = tx(t, 'c2');
      return { m, nome: rotMes(m), dias: t._dias, tent: t.tent, an: t.an, conv: t.conv, fech: tx(t, 'fech'), prob: tx(t, 'prob'), res: tx(t, 'res'), k1: tx(t, 'k1'), c1, c2,
        inc, baixa: (c1 != null && c1 < CFG.limite_cobertura) || (c2 != null && c2 < CFG.limite_cobertura),
        atual: CFG.baseline_inicio === m + '-01' && CFG.baseline_fim === fim, oficial: CFG_OFICIAL.baseline_inicio === m + '-01' && CFG_OFICIAL.baseline_fim === fim };
    });
    tabela(document.getElementById('h-cfgmeses'), { id: 'meses', linhas, chave: 'm', unidade: 'meses', busca: false, ord: 'm', asc: false, altura: 420,
      sel: l => l.m === mesSel, clique: m => { RASC = { inicio: m + '-01', fim: fimMes(m), rotulo: rotMes(m), rotManual: false }; atualizar(); window.scrollTo({ top: 0, behavior: 'smooth' }); },
      colunas: [{ k: 'm', t: 'Mês', txt: true, f: (v, l) => esc(l.nome), csv: (v, l) => l.nome }, { k: 'dias', t: 'Dias com dado' }, { k: 'tent', t: 'Ligações', f: v => nf(v) }, { k: 'an', t: 'Analisadas', f: v => nf(v) }, { k: 'conv', t: 'Conversas', f: v => nf(v) },
        { k: 'fech', t: 'Fechamento', f: v => pc(v), csv: v => pc(v) }, { k: 'prob', t: '% problema', f: v => pc(v), csv: v => pc(v) }, { k: 'res', t: 'Resolvidos', f: v => pc(v), csv: v => pc(v) },
        { k: 'k1', t: 'Carga op.', f: v => pc(v), csv: v => pc(v) }, { k: 'c1', t: 'Cob. classificação', f: v => pc(v, 0), csv: v => pc(v) }, { k: 'c2', t: 'Cob. duração', f: v => pc(v, 0), csv: v => pc(v) },
        { k: 'sit', t: 'Situação', txt: true, quebra: true, f: (v, l) => (l.oficial ? '<span class="tag v">oficial</span>' : '') + (l.atual && !l.oficial ? '<span class="tag a">em uso (pessoal)</span>' : '') + (l.inc ? '<span class="tag a">mês incompleto</span>' : '') + (l.baixa ? '<span class="tag r">cobertura baixa</span>' : ''),
          csv: (v, l) => [l.oficial ? 'oficial' : '', l.inc ? 'mês incompleto' : '', l.baixa ? 'cobertura baixa' : ''].filter(Boolean).join(' | ') }] });
    html('n-cfgmeses', `Indicadores do mês inteiro, todas as carteiras. "Mês incompleto" = menos de 80% dos dias úteis com dado. "Cobertura baixa" = classificação ou duração abaixo de ${pc(CFG.limite_cobertura, 0)} das atendidas. O painel só compara com meses que estão no dados.js: não apague da pasta de CSVs os arquivos do mês da baseline.`);
    /* oficial */
    const json = JSON.stringify({ baseline_inicio: CFG.baseline_inicio, baseline_fim: CFG.baseline_fim, baseline_rotulo: CFG.baseline_rotulo, min_ligacoes: CFG.min_ligacoes, min_n_taxa: CFG.min_n_taxa, limite_cobertura: CFG.limite_cobertura }, null, 1);
    html('h-cfgofic', `<div class="duas-col"><div><ol class="passos">
        <li>Escolha a baseline e os parâmetros acima e confira os números no painel.</li>
        <li>Clique em <b>Baixar painel_config.json</b>.</li>
        <li>Salve o arquivo <b>na sua pasta local</b>, ao lado do <code>atualizar_painel.py</code> (não na pasta compartilhada). Se já existir, substitua.</li>
        <li>Rode o <b>Atualizar painel.bat</b>. Ele mostra os números da nova baseline para você conferir, e todos os leitores passam a ver a nova baseline oficial.</li></ol>
        <div class="controles"><button type="button" class="pilula on" data-cfg-acao="baixar">Baixar painel_config.json</button></div></div>
      <div><div class="nota" style="margin-top:0">Conteúdo do arquivo (escolhas em uso agora):</div><pre class="json">${esc(json)}</pre></div></div>`);
    html('n-cfgofic', 'Só quem roda a atualização muda a baseline oficial. Quem escolher uma baseline pessoal continua vendo a pessoal até clicar em "voltar à oficial".');
  },
};
function acaoConfig(acao) {
  if (acao === 'aplicar') { aplicaCfg(Object.assign({}, CFG_PESSOAL, { baseline_inicio: RASC.inicio, baseline_fim: RASC.fim, baseline_rotulo: RASC.rotulo.trim() || rotMes(RASC.inicio.slice(0, 7)) })); }
  else if (acao === 'oficial') { const n = Object.assign({}, CFG_PESSOAL); delete n.baseline_inicio; delete n.baseline_fim; delete n.baseline_rotulo; aplicaCfg(n); RASC = null; }
  else if (acao === 'paroficial') { const n = Object.assign({}, CFG_PESSOAL); ['min_ligacoes', 'min_n_taxa', 'limite_cobertura'].forEach(k => delete n[k]); aplicaCfg(n); }
  else if (acao === 'baixar') {
    const json = JSON.stringify({ baseline_inicio: CFG.baseline_inicio, baseline_fim: CFG.baseline_fim, baseline_rotulo: CFG.baseline_rotulo, min_ligacoes: CFG.min_ligacoes, min_n_taxa: CFG.min_n_taxa, limite_cobertura: CFG.limite_cobertura }, null, 1);
    const a = document.createElement('a'); a.href = URL.createObjectURL(new Blob([json + '\n'], { type: 'application/json' })); a.download = 'painel_config.json'; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 500); return;
  }
  if (S.preset === 'base') aplicaPreset('base');
  atualizar();
}
function mudaConfig(campo, valor) {
  if (!RASC) RASC = { inicio: CFG.baseline_inicio, fim: CFG.baseline_fim, rotulo: CFG.baseline_rotulo, rotManual: false };
  if (campo === 'mes') { if (valor) RASC = { inicio: valor + '-01', fim: fimMes(valor), rotulo: rotMes(valor), rotManual: false }; }
  else if (campo === 'inicio' || campo === 'fim') { if (!/^\d{4}-\d\d-\d\d$/.test(valor)) return; RASC[campo] = valor; if (RASC.inicio > RASC.fim) [RASC.inicio, RASC.fim] = [RASC.fim, RASC.inicio]; if (!RASC.rotManual) RASC.rotulo = RASC.inicio.slice(0, 7) === RASC.fim.slice(0, 7) && RASC.inicio.endsWith('-01') && RASC.fim === fimMes(RASC.inicio.slice(0, 7)) ? rotMes(RASC.inicio.slice(0, 7)) : `${ddmmaa(RASC.inicio)} a ${ddmmaa(RASC.fim)}`; }
  else if (campo === 'rotulo') { RASC.rotulo = valor.slice(0, 40); RASC.rotManual = true; }
  else if (['min_ligacoes', 'min_n_taxa', 'limite_cobertura'].includes(campo)) {
    let v = Number(valor); if (!isFinite(v)) return;
    if (campo === 'limite_cobertura') v = Math.max(.5, Math.min(1, v / 100)); else v = Math.max(5, Math.min(500, Math.round(v)));
    const n = Object.assign({}, CFG_PESSOAL, { [campo]: v }); if (v === CFG_OFICIAL[campo]) delete n[campo]; aplicaCfg(n);
  }
  atualizar();
}

/* =====================================================================================================================
   MOLDURA: menu, filtros, chips, navegação
   ===================================================================================================================== */
const IC = {
  geral: '<path d="M3 13h4v7H3zM10 8h4v12h-4zM17 4h4v16h-4z"/>',
  tempo: '<circle cx="12" cy="12" r="8.5"/><path d="M12 7v5l3.5 2"/>',
  vendas: '<path d="M4 17l5-5 4 4 7-8"/><path d="M15 8h5v5"/>',
  problemas: '<path d="M12 3l9.5 17h-19z"/><path d="M12 10v4M12 17.2v.1"/>',
  competencias: '<path d="M4 6h16v10H8l-4 4z"/><path d="M8 10h8M8 13h5"/>',
  clientes: '<circle cx="9" cy="8.5" r="3.5"/><path d="M2.5 20c.8-3.6 3.4-5.5 6.5-5.5s5.7 1.9 6.5 5.5"/><path d="M16 5.5a3.2 3.2 0 0 1 0 6.2M18.5 14.8c1.6.8 2.6 2.6 3 5.2"/>',
  contato: '<path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/>',
  carteiras: '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M9 9v11"/>',
  qualidade: '<path d="M12 3l7 3v6c0 4.5-3 7.8-7 9-4-1.2-7-4.5-7-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
  config: '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.8l.1.1a2 2 0 1 1-2.8 2.8l-.1-.1a1.7 1.7 0 0 0-1.8-.3 1.7 1.7 0 0 0-1 1.5V21a2 2 0 1 1-4 0v-.1a1.7 1.7 0 0 0-1.1-1.5 1.7 1.7 0 0 0-1.8.3l-.1.1a2 2 0 1 1-2.8-2.8l.1-.1a1.7 1.7 0 0 0 .3-1.8 1.7 1.7 0 0 0-1.5-1H3a2 2 0 1 1 0-4h.1a1.7 1.7 0 0 0 1.5-1.1 1.7 1.7 0 0 0-.3-1.8l-.1-.1a2 2 0 1 1 2.8-2.8l.1.1a1.7 1.7 0 0 0 1.8.3H9a1.7 1.7 0 0 0 1-1.5V3a2 2 0 1 1 4 0v.1a1.7 1.7 0 0 0 1 1.5 1.7 1.7 0 0 0 1.8-.3l.1-.1a2 2 0 1 1 2.8 2.8l-.1.1a1.7 1.7 0 0 0-.3 1.8V9a1.7 1.7 0 0 0 1.5 1H21a2 2 0 1 1 0 4h-.1a1.7 1.7 0 0 0-1.5 1z"/>',
};
const PAGINAS = [['geral', 'Visão geral', 'Como o time trabalhou no período?'], ['tempo', 'Tempo', 'Para onde vai o tempo do time?'], ['vendas', 'Vendas', 'Quanto convertemos e o que acompanha o fechamento?'],
  ['problemas', 'Problemas', 'Onde estão as fricções e o que fica pendente?'], ['competencias', 'Challenger e SPIN', 'Como o time conduz a conversa?'], ['clientes', 'Clientes', 'Quem são os clientes que demandam o time?'],
  ['contato', 'Contato e cadência', 'Quando e como o time consegue falar com o cliente?'], ['carteiras', 'Carteiras', 'Como cada carteira está?'], ['qualidade', 'Qualidade do dado', 'Posso confiar nos números de hoje?'], ['config', 'Configurações', 'Qual período é a baseline e quais parâmetros usar?']];
const AJUDAS = {
  geral: 'Os cartões mostram o período escolhido no topo e a variação contra a comparação escolhida (baseline ou período anterior). Verde = melhorou, vermelho = piorou, cinza com "≈" = diferença dentro da margem de erro. Clique num cartão para ir à página do tema.',
  tempo: 'A carga operacional é a parte do tempo de ligação gasta com problema, suporte, cobrança, pós-venda e dúvida de contrato. Só entram ligações classificadas pelo GPT e com duração.',
  vendas: 'Oportunidade de venda é toda conversa em que o classificador viu interesse comercial (desfecho diferente de "não era venda"). O fechamento é o identificado na conversa. O gráfico de fatores mostra associação: use para formular hipóteses e testar no piloto.',
  problemas: 'Clique num código para destacá-lo: a página mostra o detalhe e o ranking de carteiras passa a contar só aquele código.',
  competencias: 'Challenger e notas SPIN vêm da análise de cada ligação. O mapa por carteira compara as carteiras entre si: mais escuro = melhor posição naquela coluna.',
  clientes: 'A tabela lista os clientes (código PJ) do período. Use os botões para achar quem tem pendência, quem trouxe 2+ problemas, quem ficou sem 2ª tentativa ou com retorno vencido. Baixe o CSV para distribuir às carteiras.',
  contato: 'Taxa de atendimento = tentativas atendidas ÷ tentativas. O mapa mostra os melhores horários para ligar; a cadência mostra o ganho de insistir.',
  carteiras: 'Cada carteira corresponde a um vendedor. Compare sempre com a mediana e olhe o volume: carteira com poucas conversas oscila muito.',
  config: 'A baseline oficial é a mesma para todos e vem do painel_config.json que o responsável salva ao lado do script. Aqui você pode testar outra baseline só para você (por exemplo, janeiro/2026) e, se for o caso, baixar o arquivo para torná-la oficial.',
  qualidade: 'Se a cobertura cair abaixo de 95%, os indicadores do dia podem estar incompletos. As definições estão no dicionário no fim da página.',
};
const menu = document.getElementById('menu');
menu.innerHTML = PAGINAS.map(([id, nome]) => `<button type="button" data-pag="${id}"><svg viewBox="0 0 24 24" aria-hidden="true">${IC[id]}</svg>${nome}</button>`).join('') +
  `<div class="rodape">Painel v${esc(D.meta.versao)} · números agregados do CSV da consulta · carteira = código, sem nome de vendedor<br>Gráficos: Apache ECharts</div>`;

/* ---------------- filtros do topo ---------------- */
const $ = id => document.getElementById(id);
$('fComp').innerHTML = [['base', 'Baseline'], ['ant', 'Anterior'], ['nada', 'Nada']].map(([v, t]) => `<button type="button" data-comp="${v}">${t}</button>`).join('');
$('fGran').innerHTML = [['dia', 'Dia'], ['semana', 'Semana'], ['mes', 'Mês']].map(([v, t]) => `<button type="button" data-gran="${v}">${t}</button>`).join('');
$('fD0').min = $('fD1').min = DIAS[0]; $('fD0').max = $('fD1').max = DIAS[ND - 1];
function sincronizaControles() {
  $('fPreset').innerHTML = presets().map(([v, t]) => `<option value="${v}">${esc(t)}</option>`).join(''); $('fPreset').value = S.preset; $('fD0').value = DIAS[S.d0]; $('fD1').value = DIAS[S.d1];
  document.querySelectorAll('[data-comp]').forEach(b => { b.classList.toggle('on', b.dataset.comp === S.comp); b.setAttribute('aria-pressed', b.dataset.comp === S.comp); });
  document.querySelectorAll('[data-gran]').forEach(b => { b.classList.toggle('on', b.dataset.gran === S.gran); b.setAttribute('aria-pressed', b.dataset.gran === S.gran); });
  $('fDist').innerHTML = `<option value="">Todas</option>` + DIST.map(d => `<option${d === S.dist ? ' selected' : ''}>${esc(d)}</option>`).join('');
  $('listaCart').innerHTML = CART.filter(c => !S.dist || c.d === S.dist).map(c => `<option value="${esc(c.c)}">${esc(c.d)}</option>`).join('');
  if (document.activeElement !== $('fCart')) $('fCart').value = S.cart;
  menu.querySelectorAll('[data-pag]').forEach(b => { b.classList.toggle('on', b.dataset.pag === S.pag); if (b.dataset.pag === S.pag) b.setAttribute('aria-current', 'page'); else b.removeAttribute('aria-current'); });
}
function chips() {
  const c = []; const per = `${ddmmaa(DIAS[S.d0])} – ${ddmmaa(DIAS[S.d1])}`;
  c.push(`<span class="chip neutro">${esc(per)}</span>`);
  if (S.dist) c.push(`<span class="chip">Distrital ${esc(S.dist)}<button type="button" data-tira="dist" aria-label="Tirar filtro de distrital">×</button></span>`);
  if (S.cart) c.push(`<span class="chip">Carteira ${esc(S.cart)}<button type="button" data-tira="cart" aria-label="Tirar filtro de carteira">×</button></span>`);
  if (S.cod && S.pag === 'problemas') c.push(`<span class="chip">Código ${esc(S.cod)}<button type="button" data-tira="cod" aria-label="Tirar destaque do código">×</button></span>`);
  const jc = janelaComp(); const pes = S.comp === 'base' && basePessoal();
  c.push(`<button type="button" class="chip neutro bot${pes ? ' pessoal' : ''}" data-ir-config title="Escolher a baseline">${jc ? 'comparando com ' + esc(jc.rot) : S.comp === 'base' ? 'baseline fora dos dados' : 'sem comparação'} ⚙</button>`);
  const atraso = []; if (D.meta.duracao_ate && D.meta.duracao_ate < D.meta.dados_ate) atraso.push('duração até ' + dd(D.meta.duracao_ate)); if (D.meta.classif_ate && D.meta.classif_ate < D.meta.dados_ate) atraso.push('classificação até ' + dd(D.meta.classif_ate));
  c.push(`<span class="status-dados">${atraso.length ? `<span class="alerta">${esc(atraso.join(' · '))}</span>` : ''}<span>Dados até ${dd(D.meta.dados_ate)} · atualizado em ${dd(D.meta.gerado_em.slice(0, 10))} ${esc(D.meta.gerado_em.slice(11))}</span></span>`);
  $('chips').innerHTML = c.join('');
}
function setFiltro(o) { Object.assign(S, o); if (o.cart && S.dist) { const k = CART.find(x => x.c === o.cart); if (k && k.d !== S.dist) S.dist = ''; } atualizar(); }

/* ---------------- montagem e atualização ---------------- */
const raiz = $('conteudo');
function montarPagina() {
  descartar(raiz); Object.keys(TABDADOS).forEach(k => delete TABDADOS[k]);
  const p = PAGINAS.find(x => x[0] === S.pag) || PAGINAS[0]; S.pag = p[0];
  raiz.innerHTML = `<div class="cab"><div><h1>${p[1]}</h1><p>${p[2]} <button type="button" class="info" data-ajuda aria-expanded="false" title="Como ler esta página">?</button></p></div><div class="escopo" id="escopo"></div></div>
    <div class="ajuda" id="ajuda" hidden>${esc(AJUDAS[p[0]] || '')}</div><div id="aviso"></div>${PAG[p[0]].esqueleto()}`;
  atualizar(true);
}
function atualizar(novaPagina) {
  normaliza(); C = contexto(); sincronizaControles(); chips();
  const escopo = S.cart ? 'Carteira ' + S.cart : S.dist ? 'Distrital ' + S.dist : 'Todas as carteiras';
  html('escopo', `${esc(escopo)}<br>${ddmmaa(DIAS[S.d0])} a ${ddmmaa(DIAS[S.d1])} · ${nf(C.t._dias)} dias com dado`);
  html('aviso', S.pag === 'config' ? '' : faixaAviso());
  try { PAG[S.pag].atualizar(); }
  catch (e) { console.error(e); html('aviso', `<div class="faixa-info">Não foi possível calcular parte desta página com os filtros atuais (${esc(e.message)}). Tente "Limpar filtros".</div>`); }
  salvar();
  if (novaPagina !== true) { /* filtros mudaram: gráficos já animaram a transição */ }
}
function irPara(pag) { S.pag = pag; montarPagina(); chips(); window.scrollTo({ top: 0 }); raiz.focus({ preventScroll: true }); }

/* ---------------- eventos ---------------- */
menu.addEventListener('click', ev => { const b = ev.target.closest('[data-pag]'); if (b) irPara(b.dataset.pag); });
$('fPreset').addEventListener('change', ev => { S.preset = ev.target.value; if (S.preset !== 'pers') aplicaPreset(S.preset); atualizar(); });
function mudaData() { const a = $('fD0').value, b = $('fD1').value; if (!a || !b) return; let i0 = idxDe(a < b ? a : b), i1 = idxAte(a < b ? b : a); if (i0 > i1 || i0 >= ND) return; S.d0 = i0; S.d1 = i1; S.preset = 'pers'; atualizar(); }
$('fD0').addEventListener('change', mudaData); $('fD1').addEventListener('change', mudaData);
$('fComp').addEventListener('click', ev => { const b = ev.target.closest('[data-comp]'); if (b) { S.comp = b.dataset.comp; atualizar(); } });
$('fGran').addEventListener('click', ev => { const b = ev.target.closest('[data-gran]'); if (b) { S.gran = b.dataset.gran; atualizar(); } });
$('fDist').addEventListener('change', ev => { S.dist = ev.target.value; if (S.cart && S.dist && (CART.find(x => x.c === S.cart) || {}).d !== S.dist) S.cart = ''; atualizar(); });
$('fCart').addEventListener('change', ev => { const v = ev.target.value.trim().toUpperCase(); if (!v) { S.cart = ''; atualizar(); return; } const k = CART.find(x => x.c.toUpperCase() === v); if (k) setFiltro({ cart: k.c }); else ev.target.value = S.cart; });
$('fLimpar').addEventListener('click', () => { Object.assign(S, { preset: 'mes', dist: '', cart: '', cod: '', comp: 'base' }); aplicaPreset('mes'); atualizar(); });
$('chips').addEventListener('click', ev => { const b = ev.target.closest('[data-tira]'); if (b) { S[b.dataset.tira] = ''; atualizar(); return; } if (ev.target.closest('[data-ir-config]')) irPara('config'); });
raiz.addEventListener('click', ev => {
  const pil = ev.target.closest('[data-pil]');
  if (pil) { const grupo = pil.dataset.pil; S[grupo] = isNaN(+pil.dataset.v) || grupo === 'metrica' || grupo === 'pareto' || grupo === 'filtroCli' || grupo === 'metCart' ? pil.dataset.v : +pil.dataset.v; marcaPilulas(grupo, S[grupo]); if (grupo === 'filtroCli' && TAB.clientes) TAB.clientes.lim = 100; atualizar(); return; }
  const ac = ev.target.closest('[data-acao]');
  if (ac) {
    const id = ac.dataset.id, nome = (document.querySelector('#card-' + id + ' h2') || {}).textContent || id;
    if (ac.dataset.acao === 'png') baixarPNG(id, nome);
    else if (ac.dataset.acao === 'csv') { const d = TABDADOS[id]; if (d) baixarCSV(nome, d.colunas, d.linhas); }
    else { const t = $('t-' + id), gr = $('g-' + id); const on = t.hidden; t.hidden = !on; ac.classList.toggle('on', on); ac.setAttribute('aria-pressed', on); if (on) { desenhaTabDados(id); gr.style.display = 'none'; } else { if (!gr.dataset.vazio) gr.style.display = ''; const c = echarts.getInstanceByDom(gr); if (c) c.resize(); } }
    return;
  }
  const kp = ev.target.closest('[data-ir]'); if (kp && !ev.target.closest('.info')) { irPara(kp.dataset.ir); return; }
  if (ev.target.closest('[data-ajuda]')) { const a = $('ajuda'); a.hidden = !a.hidden; ev.target.closest('[data-ajuda]').setAttribute('aria-expanded', !a.hidden); return; }
  if (ev.target.closest('[data-tira-cod]')) { S.cod = ''; atualizar(); return; }
  if (ev.target.closest('[data-tira-cart]')) { S.cart = ''; atualizar(); return; }
  const cl = ev.target.closest('[data-cart-link]'); if (cl) { ev.preventDefault(); setFiltro({ cart: cl.dataset.cartLink }); return; }
  const ca = ev.target.closest('[data-cfg-acao]'); if (ca) { if (!ca.disabled) acaoConfig(ca.dataset.cfgAcao); return; }
  const ic = ev.target.closest('[data-ir-cli]'); if (ic) { ev.preventDefault(); S.filtroCli = ic.dataset.irCli; irPara('clientes'); return; }
});
raiz.addEventListener('change', ev => {
  const s = ev.target.closest('[data-sim]'); if (s) { if (s.dataset.sim === 'cod') S.simCod = s.value; atualizar(); return; }
  const cf = ev.target.closest('[data-cfg]'); if (cf) mudaConfig(cf.dataset.cfg, cf.value);
});
raiz.addEventListener('input', ev => { const s = ev.target.closest('[data-sim="pct"]'); if (s) { S.simPct = +s.value; atualizar(); } });
raiz.addEventListener('keydown', ev => { const kp = ev.target.closest('[data-ir]'); if (kp && (ev.key === 'Enter' || ev.key === ' ')) { ev.preventDefault(); irPara(kp.dataset.ir); } });
document.addEventListener('keydown', ev => { if (/INPUT|SELECT|TEXTAREA/.test(ev.target.tagName) || ev.ctrlKey || ev.metaKey || ev.altKey) return; const n = parseInt(ev.key, 10); if (n >= 1 && n <= 9) irPara(PAGINAS[n - 1][0]); else if (n === 0) irPara('config'); });
const ajustaTopo = () => document.documentElement.style.setProperty('--topo-h', $('topo').offsetHeight + 'px');
new ResizeObserver(ajustaTopo).observe($('topo')); ajustaTopo();

/* para conferência automatizada (testes) */
window.__painel = { S, D, somaA, sel, tx, media, MET, contexto, atualizar, irPara, setFiltro, janelaComp, deltaTaxa, k3 };
montarPagina();
})();
