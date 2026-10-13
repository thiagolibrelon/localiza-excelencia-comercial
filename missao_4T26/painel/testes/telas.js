// Teste do painel com Playwright. Uso: veja testes/LEIA-ME.md
const { chromium } = (() => { try { return require('playwright'); } catch (e) { return require('/opt/node22/lib/node_modules/playwright'); } })();
const abrir = () => chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const dir = process.argv[2], out = process.argv[3], w = +(process.argv[4] || 1440), h = +(process.argv[5] || 900);
const fs = require('fs'); fs.mkdirSync(out, { recursive: true });
(async () => {
  const b = await abrir();
  const p = await b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  const errs = []; p.on('console', m => { if (['error', 'warning'].includes(m.type())) errs.push(m.type() + ': ' + m.text()); }); p.on('pageerror', e => errs.push('pageerror: ' + e.message));
  await p.goto('file://' + dir + '/painel.html'); await p.waitForTimeout(600);
  const pags = await p.$$eval('[data-pag]', bs => bs.map(b => b.dataset.pag));
  for (const pg of pags) {
    await p.click(`[data-pag="${pg}"]`); await p.waitForTimeout(900);
    const r = await p.evaluate(() => {
      const bad = [];
      document.querySelectorAll('.card,.kpi').forEach(c => { if (c.scrollWidth > c.clientWidth + 2) bad.push('largura: ' + (c.querySelector('h2,.lab') || {}).textContent); });
      document.querySelectorAll('.kpi .lab span,.kpi .sub').forEach(e => { if (e.scrollWidth > e.clientWidth + 1 || e.scrollHeight > e.clientHeight + 2) bad.push('cortado: ' + e.textContent.slice(0, 70)); });
      const vazios = [...document.querySelectorAll('.vazio:not([hidden])')].map(v => v.textContent.slice(0, 60));
      const aviso = (document.getElementById('aviso') || {}).textContent;
      return { bad, vazios, aviso, altura: document.body.scrollHeight };
    });
    console.log(`[${pg}] altura ${r.altura}${r.bad.length ? ' | ' + r.bad.join(' ; ') : ''}${r.vazios.length ? ' | vazios: ' + r.vazios.join(' ; ') : ''}`);
    await p.screenshot({ path: `${out}/${pg}.png`, fullPage: true });
  }
  console.log(errs.length ? errs.join('\n') : 'sem erros de console');
  await b.close();
})();
