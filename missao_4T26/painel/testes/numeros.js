// Teste do painel com Playwright. Uso: veja testes/LEIA-ME.md
const { chromium } = (() => { try { return require('playwright'); } catch (e) { return require('/opt/node22/lib/node_modules/playwright'); } })();
const abrir = () => chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const esp = JSON.parse(require('fs').readFileSync(process.argv[3], 'utf8'));
(async () => {
  const b = await abrir(); const p = await b.newPage();
  await p.goto('file://' + process.argv[2] + '/painel.html'); await p.waitForTimeout(500);
  const casos = { set: ['2026-09-01', '2026-09-30', '', ''], S1I05A_0122: ['2026-09-01', '2026-09-22', '', 'S1I05A'], DTIN4_set: ['2026-09-01', '2026-09-30', 'DTIN4', ''] };
  let ok = 0, ruim = 0;
  for (const [nome, [a, z, dist, cart]] of Object.entries(casos)) {
    const v = await p.evaluate(([a, z, dist, cart]) => { const P = window.__painel, D = P.D; Object.assign(P.S, { preset: 'pers', d0: D.dias.indexOf(a) < 0 ? D.dias.findIndex(d => d >= a) : D.dias.indexOf(a), d1: (() => { let i = D.dias.length - 1; while (D.dias[i] > z) i--; return i; })(), dist, cart });
      const C = P.contexto(); const t = C.t; const cl = new Map(); P.sel('CL').forEach(r => { if (r[7] > 0) cl.set(r[2], (cl.get(r[2]) || 0) + r[7]); }); let tot = 0, re = 0; cl.forEach(n => { tot += n; if (n >= 2) re += n; });
      return { tent: t.tent, atend: t.atend, an: t.an, conv: t.conv, opp: t.opp, fech: t.fech, txFech: P.tx(t, 'fech'), prob: t.prob, txProb: P.tx(t, 'prob'), res: P.tx(t, 'res'), pend: t.pend, k1: P.tx(t, 'k1'), horas: t.seg_base / 3600,
        ch: P.tx(t, 'ch'), chAlta: P.tx(t, 'chAlta'), dado: P.tx(t, 'dado'), rea: P.tx(t, 'rea'), sf: P.media(t, 'sf'), si1: P.tx(t, 'si1'), dec: P.tx(t, 'dec'), tc: P.tx(t, 'tc'), clientes: new Set(P.sel('CL').map(r => r[2])).size, k5: tot ? re / tot : null };
    }, [a, z, dist, cart]);
    for (const [k, e] of Object.entries(esp[nome])) { const x = v[k]; const bate = e == null ? x == null : Math.abs(x - e) <= Math.max(1e-6, Math.abs(e) * 1e-9) + 1e-9; if (bate) ok++; else { ruim++; console.log(`DIFERENTE ${nome}.${k}: painel ${x} · pandas ${e}`); } }
  }
  console.log(`conferidos ${ok + ruim}: ${ok} iguais, ${ruim} diferentes`); await b.close();
})();
