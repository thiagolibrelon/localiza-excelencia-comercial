# Personas — Programa Aletheia RAC

Mapa de papéis envolvidos no programa, pra orientar o nível de detalhe, linguagem e formato de qualquer entrega futura ("isso é para o Gerente de Vendas" muda o que se produz vs. "isso é para o CEO").

**Nota:** a numeração pedida saltou de 2 para 4 — não criei uma persona "3" para não inventar um papel que não foi especificado. Se houver uma peça faltando (ex: um Gerente de Cross-sell/Produtos dedicado), é só avisar.

---

## Organograma

```
CEO
 └── Diretor do RAC PJ
      ├── Gerente de Excelência Comercial
      │    └── Especialista de Excelência Comercial
      ├── Gerente de Vendas
      ├── Especialista de Treinamentos  (trabalha junto do Gerente de Vendas)
      └── Gerente de Produto
```

---

## 1. Especialista de Excelência Comercial

**Missão:** levantar e tratar os dados do Aletheia — é quem constrói e mantém a base consolidada, roda as explorações (Gemini + Fable), audita achados antes de subirem, e escreve os documentos técnicos de apoio.

**O que produz:** `resultados/consolidado/CONSOLIDADO_LIGACOES.csv`, os arquivos em `analises/`, as explorações em `resultados/exploracao_fable/`, os scripts em `scripts/`.

**O que NÃO faz:** não decide o que vai pra apresentação executiva, não decide política comercial, não treina o time de vendas diretamente.

**Reporta para:** Gerente de Excelência Comercial.

**Tom de comunicação esperado:** técnico, com número exato e ressalva de amostra/cobertura sempre explícita. É o papel que este projeto tem ocupado durante toda a sessão.

---

## 2. Gerente de Excelência Comercial

**Missão:** é o filtro entre o dado bruto e o resto da organização. Vê a exploração **antes de qualquer outra persona** — decide o que é sinal real vs. ruído de amostra pequena, o que sobe pra apresentação executiva, e o que fica só no radar técnico. Trabalha em conjunto direto com a frente de cross-sell (é quem eu chamaria primeiro se aparecer um padrão de produto/portfólio novo, como os achados de pesados/telemetria/elétrico do slide 4).

**O que consome:** tudo que o Especialista produz, antes de qualquer decisão de conteúdo.

**O que decide:** que hipóteses vão pras 3-4 do RMR, que achados exploratórios (P13 tipo "padrões emergentes") esperam mais dados antes de virar apresentação, que riscos (ex: desvio de crédito, manipulação de NPS) são escalados fora do fluxo de vendas.

**Reporta para:** Diretor do RAC PJ.

**Artefato-chave:** `apresentacao/CONTEUDO_4SLIDES_DIRETORIA.md` é essencialmente o produto de trabalho desta persona (com apoio do Especialista).

---

## 4. Gerente de Vendas

**Missão:** consome os dados pra gerir o time comercial no dia a dia — quem liga pra quem, meta de ligações, priorização de carteira.

**O que consome:** achados de comportamento (B1-B10), hipóteses confirmadas, e — com ressalva — o scoring automático (atualmente **não deve ser usado pra priorização**, está no radar por miscalibração: score médio de quem fecha é menor que de quem não fecha).

**Ponto de atenção direto:** a lógica de visitas mínimas/meta de ligações por dia é dessa persona — e é a explicação-raiz de por que 15% da base é prospecção fria de baixo retorno (o vendedor liga porque precisa bater a meta de contatos, não porque há sinal comercial). Qualquer recomendação de "pare de fazer cold call" precisa passar por aqui, porque tirar o vendedor da meta de ligações sem mudar a política tem custo.

**Reporta para:** Diretor do RAC PJ.

---

## 5. Especialista de Treinamentos

**Missão:** consome os achados de comportamento e gera material de treinamento — trabalha em conjunto com o Gerente de Vendas pra decidir o que entra em treinamento formal vs. coaching individual.

**O que consome:** achados de comportamento qualificado (não número agregado) — precisa do "como fazer certo", não só do "isso correlaciona com fechamento".

**Artefato-chave:** `treinamento/GUIA_CHALLENGER_BEM_FEITO.md` é o primeiro material desenhado especificamente pra essa persona. Deve ser o padrão pra qualquer treinamento futuro (ex: um guia equivalente pra B5/upsell conectado à dor, ou pra fechamento com data).

**Ponto de atenção:** não usar métrica de presença binária (ex: "teve Challenger SIM/NAO") como KPI de treinamento — os dados mostram que isso não discrimina e incentiva execução malfeita só pra bater a métrica.

**Reporta para:** não especificado explicitamente — colabora lateralmente com Gerente de Vendas, provável reporte ao Diretor do RAC PJ ou ao próprio Gerente de Vendas.

---

## 6. Gerente de Produto

**Missão:** atua nos problemas que o time de vendas tem enfrentado — é quem recebe a Hipótese 3 (plataforma consome tempo comercial) e as auditorias de fricção operacional.

**O que consome:** a quebra por categoria de problema (faturamento 19,3% · acesso/sistema 18,2% · cadastro 16,1% · reserva 11,9%), os casos concretos de vazamento de receita (PJ→PF por fricção de login, bug de reserva que gravou devolução em 2031).

**O que NÃO recebe:** os achados de comportamento comercial (isso é do Gerente de Vendas/Especialista de Treinamentos) — o recorte pra essa persona é estritamente "o que trava o cliente/vendedor por causa de sistema, não por causa de comportamento".

**Reporta para:** Diretor do RAC PJ.

---

## 7. Diretor do RAC PJ

**Missão:** comanda as 4 personas operacionais acima (Gerente de Excelência Comercial, Gerente de Vendas, Especialista de Treinamentos, Gerente de Produto). É quem decide prioridade entre as frentes quando competem por recurso (ex: "focar em treinar Challenger" vs. "focar em resolver o bug de biometria" — decisão de portfólio de iniciativas, não de dado).

**O que consome:** a apresentação executiva consolidada (RMR), não o dado bruto — espera síntese e recomendação, não tabela.

**Reporta para:** CEO.

**Contexto da apresentação atual:** é o público-alvo direto do `apresentacao/CONTEUDO_4SLIDES_DIRETORIA.md` — a "diretoria" mencionada em toda a preparação da RMR é este papel (e o CEO, se participar).

---

## 8. CEO

**Missão:** olha pra empresa inteira, não só pro RAC PJ. Reporta pra investidores.

**O que consome do Aletheia:** só o que tiver relevância de negócio em nível de empresa — R$ de oportunidade, risco de compliance real (ex: desvio de crédito, se confirmado em escala), ou métrica que vai pra board/investidor (ex: se NPS/CSAT for indicador externo, a descoberta de manipulação é relevante aqui).

**O que NÃO recebe:** comportamento B1-B10, códigos de Challenger, nada operacional do dia a dia comercial — isso para na mesa do Diretor do RAC PJ.

**Implicação prática:** os dois achados mais "picantes" desta auditoria (desvio de crédito e manipulação de NPS) são justamente os dois que têm potencial de subir até esse nível, se confirmados em escala — hoje ainda estão em `analises/AUDITORIA_desvio_credito.md` e `analises/AUDITORIA_manipulacao_nps.md`, no radar do Gerente de Excelência Comercial, não escalados ainda.
