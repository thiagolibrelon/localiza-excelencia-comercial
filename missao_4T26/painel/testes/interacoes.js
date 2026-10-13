// Teste do painel com Playwright. Uso: veja testes/LEIA-ME.md
const { chromium } = (() => { try { return require('playwright'); } catch (e) { return require('/opt/node22/lib/node_modules/playwright'); } })();
const abrir = () => chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
const dir = process.argv[2], out = process.argv[3];
(async () => {
  const b = await abrir();
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, acceptDownloads: true }); const p = await ctx.newPage();
  const errs = []; p.on('pageerror', e => errs.push(e.message)); p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await p.goto('file://' + dir + '/painel.html'); await p.waitForTimeout(700);
  const chips = async () => (await p.locator('#chips').innerText()).replace(/\s+/g, ' ');
  // 1 clique na barra do distrital (ECharts: clicar no canvas na posição da barra)
  await p.locator('#g-dist').scrollIntoViewIfNeeded(); await p.waitForTimeout(200);
  const pos = await p.evaluate(() => { const c = echarts.getInstanceByDom(document.getElementById('g-dist')); const px = c.convertToPixel({ seriesIndex: 0 }, [1, 0.05]); const r = document.getElementById('g-dist').getBoundingClientRect(); return { x: r.left + px[0], y: r.top + px[1] }; });
  await p.mouse.click(pos.x, pos.y); await p.waitForTimeout(400); console.log('1 clique no distrital →', await chips());
  await p.click('[data-tira="dist"]'); await p.waitForTimeout(300); console.log('  tirar chip →', await chips());
  // 2 KPI leva à página
  await p.click('#k-prob'); await p.waitForTimeout(500); console.log('2 cartão "problemas" → página', await p.locator('.menu .on').innerText());
  // 3 clique no código P14 no Pareto → detalhe
  await p.locator('#g-pareto').scrollIntoViewIfNeeded(); await p.waitForTimeout(200);
  const pos2 = await p.evaluate(() => { const c = echarts.getInstanceByDom(document.getElementById('g-pareto')); const op = c.getOption(); const cats = op.xAxis[0].data; const i = cats.indexOf('P14'); const v = op.series[0].data[i].value; const px = c.convertToPixel({ seriesIndex: 0 }, [i, v / 2]); const r = document.getElementById('g-pareto').getBoundingClientRect(); return { x: r.left + px[0], y: r.top + px[1] }; });
  await p.mouse.click(pos2.x, pos2.y); await p.waitForTimeout(500);
  console.log('3 P14 →', (await p.locator('#h-detcod').innerText()).replace(/\s+/g, ' ').slice(0, 160));
  await p.screenshot({ path: out + '/int_problemas_p14.png', fullPage: true });
  // 4 granularidade semana e comparação período anterior
  await p.click('[data-gran="semana"]'); await p.waitForTimeout(400);
  console.log('4 semana: eixo da evolução =', await p.evaluate(() => echarts.getInstanceByDom(document.getElementById('g-evolp')).getOption().xAxis[0].data.join(', ')));
  // 5 período 15–30/09 contra anterior → o que mudou
  await p.click('[data-pag="geral"]'); await p.waitForTimeout(300);
  await p.fill('#fD0', '2026-09-15'); await p.dispatchEvent('#fD0', 'change'); await p.waitForTimeout(200);
  await p.click('[data-comp="ant"]'); await p.waitForTimeout(600);
  console.log('5 chips:', await chips());
  console.log('  o que mudou:', (await p.locator('#h-mudou').innerText()).replace(/\n+/g, ' | ').slice(0, 400));
  console.log('  delta fechamento:', await p.locator('#kd-fech').innerText(), '| delta problemas:', await p.locator('#kd-prob').innerText());
  await p.screenshot({ path: out + '/int_geral_anterior.png', fullPage: true });
  // 6 vendas: fator SPIN Implicação
  await p.click('[data-pag="vendas"]'); await p.waitForTimeout(400); await p.click('[data-pil="faceta"][data-v="4"]'); await p.waitForTimeout(500);
  console.log('6 fator SPIN: categorias =', await p.evaluate(() => echarts.getInstanceByDom(document.getElementById('g-fator')).getOption().xAxis[0].data.join(', ')));
  // 7 tabela do gráfico e CSV
  await p.click('[data-acao="tabela"][data-id="fator"]'); await p.waitForTimeout(200); console.log('7 tabela do gráfico:', (await p.locator('#t-fator').innerText()).split('\n').slice(0, 3).join(' / '));
  const [dl] = await Promise.all([p.waitForEvent('download'), p.click('[data-acao="csv"][data-id="fator"]')]); console.log('  CSV:', dl.suggestedFilename());
  const [dl2] = await Promise.all([p.waitForEvent('download'), p.click('[data-acao="png"][data-id="funilv"]')]); console.log('  PNG:', dl2.suggestedFilename());
  // 8 clientes: filtro, busca, ordenação, mais
  await p.click('[data-pag="clientes"]'); await p.waitForTimeout(500);
  await p.click('[data-pil="filtroCli"][data-v="s2"]'); await p.waitForTimeout(300); console.log('8 sem 2ª tentativa:', await p.locator('#h-tabcli .cont').innerText());
  await p.click('[data-pil="filtroCli"][data-v="todos"]'); await p.waitForTimeout(300);
  await p.fill('#h-tabcli [data-tab-busca]', 'RJI05A'); await p.waitForTimeout(300); console.log('  busca RJI05A:', await p.locator('#h-tabcli .cont').innerText());
  await p.click('#h-tabcli th[data-tab-ord="h"]'); await p.waitForTimeout(200); console.log('  ordenar horas: 1ª linha', (await p.locator('#h-tabcli tbody tr').first().innerText()).replace(/\s+/g, ' '));
  await p.fill('#h-tabcli [data-tab-busca]', ''); await p.waitForTimeout(300); await p.click('#h-tabcli [data-tab-mais]'); await p.waitForTimeout(300); console.log('  mostrar mais:', await p.locator('#h-tabcli .cont').innerText());
  // 9 carteiras: clique na tabela abre ficha
  await p.click('[data-pag="carteiras"]'); await p.waitForTimeout(500); await p.click('#h-tabcart tr[data-tab-linha="S1I05A"]'); await p.waitForTimeout(500);
  console.log('9 ficha:', (await p.locator('#ficha h2').innerText()), '| chips:', await chips());
  await p.screenshot({ path: out + '/int_ficha.png', fullPage: true });
  // 10 tempo com carteira: simulador
  await p.click('[data-pag="tempo"]'); await p.waitForTimeout(400); await p.locator('[data-sim="pct"]').fill('50'); await p.waitForTimeout(300); console.log('10 simulador 50%:', (await p.locator('#simOut').innerText()).replace(/\s+/g, ' ').slice(0, 90));
  // 11 persistência
  await p.reload(); await p.waitForTimeout(700); console.log('11 após recarregar:', await p.locator('.menu .on').innerText(), '|', await chips());
  await p.click('#fLimpar'); await p.waitForTimeout(300); console.log('   limpar:', await chips());
  console.log(errs.length ? 'ERROS: ' + errs.join(' | ') : 'sem erros');
  await b.close();
})();
