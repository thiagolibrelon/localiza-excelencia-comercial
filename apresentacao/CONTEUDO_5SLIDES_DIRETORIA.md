# Aletheia RAC — Apresentação Diretoria (5 slides)

Base: RMR_Diretoria_v1.pptx (18 slides) + APRESENTACAO_EXECUTIVA.md (10 hipóteses) + analise_6_cross_selling.md + analise_recalculo_base_combinada_6623.md
Público: diretoria, primeira exposição ao Aletheia — sem jargão técnico (nada de H1/H2/H10, B5, FC1/FC3, CH1 no que aparece na tela)
Sem R$ agregado nesta rodada. Sem pedido formal de aprovação — foco em gerar confiança nos dados.

**Histórico:** substitui `CONTEUDO_4SLIDES_DIRETORIA.md` (mesmo conteúdo-base, reestruturado em 09/07/2026 de 4 pra 5 slides — cada hipótese ganhou seu próprio slide em vez de dividir colunas, e o slide de abertura virou gancho puro).

---

## Slide 1 — Gancho: a pergunta que abriu o projeto

**Título:** *"O que o vendedor faz para fechar um contrato?"*

- Pergunta feita pelo CEO/diretoria no início do projeto — é o fio condutor de tudo que vem a seguir
- **6.623 ligações** analisadas por IA · junho–julho de 2026 (1.275 da base piloto + 5.348 do lote seguinte)
- Não é amostra: 99,6% das ligações já têm desfecho e comportamento mapeados
- **3 hipóteses emergiram dos dados** (detalhe nos próximos slides):
  1. O mercado real é menor do que parece
  2. A plataforma consome tempo comercial que poderia ser venda
  3. Não é um comportamento isolado — os bons comportamentos se somam

*Nota de transição:* fechar este slide com "vamos ver cada uma" — é o único momento de overview, os próximos 3 slides são 1 hipótese cada.

---

## Slide 2 — Hipótese 1: o mercado real é menor do que parece

**Título:** Antes de julgar o time, é preciso medir o esforço certo

**Dados:**
- **57,4%** das ligações não era venda (suporte, senha, cadastro, biometria)
- 37,3% interessou mas não fechou
- **5,1%** fechou
- **Achado novo:** dentro do "não era venda", 26,5% (1.002 ligações — 15% de toda a base) eram tentativas de prospecção nova que não geraram nenhuma tração — 90% iniciadas pelo próprio vendedor. Não é só suporte consumindo tempo comercial.

**Exemplo real:**
> "Eu queria saber, não sei se era no WhatsApp ou no e-mail, para eu poder fazer a renovação, né?" (...) "Tá, eu vou mandar de novo, então, que é o link de prorrogação do contrato, né?"
— Cliente 25966050 · 170s · fechou renovação · **score comercial: 0**
Renovou por inércia — sem nenhum comportamento comercial. O contrato "fechou" sozinho; o risco é que migre pra concorrência do mesmo jeito, por inércia, quando alguém ligar primeiro com proposta ativa.

---

## Slide 3 — Hipótese 2: a plataforma consome tempo que poderia ser venda

**Título:** O vendedor virou suporte de sistema em boa parte do dia

**Dados:**
- **65,6%** dos problemas relatados se concentram em só 4 tipos — não são preço nem produto:
  Faturamento/cobrança **19,3%** · Acesso/sistema **18,2%** · Condutor/cadastro **16,1%** · Reserva/sistema **11,9%**
- **39,9%** de toda oportunidade perdida da base é ligação que encerra sem nenhuma pergunta comercial — o vendedor resolve o problema e desliga, sem sondar nada
- São 4 times diferentes (financeiro, TI, cadastro, reservas) que poderiam resolver isso sem depender do vendedor

**Exemplos reais:**
> "Estou tentando fazer uma reserva... a partir do momento que pede a nacionalidade ele para e trava!"
— Cliente 17015435 · bug confirmado no sistema, vendedor só pode prometer avisar quando voltar. Ligação inteira de suporte a um problema que não é do cliente nem do vendedor.

Em outro caso, o cliente relatou que **deixou de alugar** por não conseguir acessar login/senha: *"precisei alugar um carro, tive que passar no cartão... era tão fácil pela plataforma."* — Cliente 20148743. Receita perdida silenciosamente, não por preço ou produto.

---

## Slide 4 — Hipótese 3: os bons comportamentos se somam

**Título:** Duas coisas separam quem fecha: conectar o produto certo à dor do cliente, e mostrar por que a Localiza é melhor que a concorrência — com dado real, não papo genérico

**Os 2 comportamentos-chave (nomear os dois explicitamente na tela, não deixar implícito):**
1. **Upsell conectado à dor** — o vendedor liga o produto a algo específico que o cliente acabou de dizer, não a um catálogo genérico
2. **Boa comparação com o concorrente** — usa um dado real e verificável pra mostrar a vantagem da Localiza, não uma afirmação vaga de "vale a pena"

**A conta, passo a passo (como chegamos no 6,25x):**

| Combinação | N | Taxa de fechamento |
|---|---|---|
| Nenhum dos dois (padrão do time hoje) | 4.885 | 3,2% |
| Upsell na dor, sozinho | 68 | 13,2% |
| Boa comparação com concorrente, sozinha | 1.228 | 9,1% |
| **Os dois juntos** | **225** | **20,0%** |

**3,2% → 20,0% = 6,25x mais fechamento.** Não é mágica de combinação — cada comportamento sozinho já ajuda por conta própria (13,2% e 9,1%, ambos acima do 3,2% base), e juntos o efeito soma.

**O detalhe que mais importa:** "tentar" uma boa comparação não é suficiente — quando é malfeita (dado genérico, sem conexão com o que o cliente disse), o resultado fica **abaixo da média geral da base**. Só quando é bem executada (dado real, específico, que o cliente reage) é que o efeito aparece.

**Exemplo real:**
> Cliente: "Eu posso fazer o pagamento pelo cartão da empresa? [...] eu precisaria que ele retirasse se eu fizesse o pagamento por aqui ou faturado."
> Vendedora: "O bom de ser faturado pra empresa é que o seu condutor vai retirar sem nenhuma burocracia. Ele não tem que apresentar nenhum cartão nominal, nenhum pagamento de caução — igual lá na pessoa física, que geralmente é duas vezes o valor da caução."
— Cliente 14683216 · 1.180s · **fechou novo contrato**
Conectou a dúvida específica do cliente a uma vantagem concreta e verificável — não uma afirmação genérica de que "vale a pena".

**Fecha o slide:** por isso já existe um guia de treinamento pronto especificamente sobre como executar bem esse tipo de argumentação (critério objetivo de 3 pontos, com exemplos reais bons e ruins da própria base) — a análise já virou ação.

---

## Slide 5 — Não é só "pesados": o portfólio inteiro está batendo na porta

**Título:** O cliente já fala do que quer comprar — só falta alguém perguntar

**A escala real (contagem de menções, busca na base inteira de 6.623 ligações):**

| Produto | Base piloto (1.275) | Novo lote (5.348) |
|---|---|---|
| Frota pesada / caminhão / picape | 175 | 537 |
| Elétrico / HB20 / TAO | 119 | 383 |
| Telemetria | 79 | 341 |
| Gestão de frota | 80 | 288 |
| Seminovos | 16 | 45 |
| ZARP | 1 | 4 |
| Meoo | 0 | 0 |

**Leitura:** frota pesada, elétrico, telemetria e gestão de frota aparecem **centenas de vezes** na base inteira — isso não é um produto de nicho, é conversa recorrente que o time já está tendo. ZARP é genuinamente raro (não é viés de amostra). Meoo tem **zero menções em 6.623 ligações** — ou o produto não é chamado assim nessas conversas, ou realmente não está sendo oferecido a ninguém.

**O exemplo que ilustra o padrão:**
> **Vendedor:** "A gente também aluga pesado, cê sabia? Caminhão, picape. Olha, se você soubesse antes talvez tivesse locado em vez de comprar o pequeno."
> **Cliente:** "Me passa isso! Me passa a cotação disso aí."
— Cliente 22153452 · cliente tem 7-8 carros leves + 2 caminhões próprios (fora da Localiza) · descoberto por acidente, follow-up nunca confirmado

**Por que isso é ouro:**
- O cliente já confia na Localiza pra frota leve — cross-sell pra quem já é cliente é sempre mais barato que prospecção nova
- Foi descoberto por acidente, numa pergunta de curiosidade genuína — não por script
- Uma exploração em amostra de 456 ligações confirmou o mesmo padrão de janela perdida (cliente sinaliza, vendedor não persegue) em **11 dos 12 lotes analisados** — não é 1 história isolada, é sistemático

**A pergunta que abre tudo isso não é feita:**
> *"Além dos carros que vocês têm com a gente, como é o resto da operação de frota de vocês?"*
Não apareceu em nenhuma das 87 ligações da primeira auditoria de cross-sell — e o volume de menções na tabela acima sugere que a mesma pergunta abriria janela em telemetria, elétrico e gestão de frota, não só em pesados.

**Fecha a apresentação:** ainda não é a base inteira analisada com essa profundidade, mas a consistência entre amostras independentes (contagem de menções + exploração de comportamento) é o tipo de sinal que já justifica testar um script de sondagem — sem esperar terminar a análise completa.

---

## Notas de produção

- Não usar nome de cliente em nenhum exemplo — só `Cliente <Cod>`. Nome de vendedor pode ficar em exemplos positivos (reconhecimento), como antes.
- Removido: menção a R$ agregado ou pontual (decisão desta rodada).
- Termos técnicos (H1/H3/H5/H10, FC1/FC3, B5, CH1) ficam de fora do que a diretoria vê — usar apenas nesta nota de produção / documento técnico de apoio. No slide 4, falar em "boa argumentação com dado real" ou "comparação bem feita", nunca "Challenger".
- H2 (fechar sem data) não tem slide dedicado — evidência só na base piloto (P9/P10 em 33,8%). Boa resposta se a diretoria perguntar "mais alguma coisa?", junto com: diária vs. mensal converte mais, referral nunca é pedido, WhatsApp virou pseudo-fechamento sem prazo.
- Não trazer a comparação "7,0%→5,1%" como tópico de discussão — a diretoria nunca viu o número antigo, então "5,1%" é simplesmente o número atual, sem precisar justificar queda nenhuma. Causa da diferença entre as duas bases ainda em investigação interna, fora do escopo desta RMR.
- Todo exemplo de ligação deste documento foi conferido contra `resultados/consolidado/CONSOLIDADO_LIGACOES.csv` antes de entrar (segment_id, desfecho e comportamentos reais) — não reutilizar exemplos de versões antigas do material sem essa checagem, dado o erro encontrado no Cliente 13382750 (versão anterior do slide de combinação).
- Slide 4 referencia `treinamento/GUIA_CHALLENGER_BEM_FEITO.md` como o material já pronto — não citar o nome do arquivo na tela, só mencionar verbalmente que já existe.
- **Nota interna (09/07/2026, não mostrar pra diretoria):** "Frota pesada / caminhão / picape" (slide 5) mistura picape (frota utilitária, negócio RAC) com caminhão (negócio Pesados) — separação correta fica pra quando a análise sair da fase exploratória. Metodologia de contagem do 175/537 também não está documentada/reproduzível no repo (script original não encontrado); checagem estrita por keyword (só caminhão/caminhões/caminhonete, sem picape) deu bem menos — 60 piloto / 238 novo lote.
