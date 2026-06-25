# Dicionário Técnico — Framework de Análise de Ligações B2B
## Localiza Frota PJ | Junho 2026

> Este documento é o mapa de tradução entre os códigos usados internamente no framework
> e a linguagem usada nas apresentações e nos arquivos de resultado.
> Serve como referência para quem precisar interpretar os arquivos CSV de saída do sistema.

---

## 1. OS 15 PROMPTS (PERGUNTAS DE ANÁLISE)

| Código | Nome | O que analisa |
|--------|------|---------------|
| P1 | Desfecho e Comportamentos Comerciais | Resultado da ligação + 10 comportamentos do vendedor (B1–B10) |
| P2 | Tipo de Ligação | Natureza da chamada: nova venda, renovação, suporte, retenção... |
| P3 | Problemas Recorrentes | Problemas relatados pelo cliente e se foram resolvidos |
| P4 | Health Score do Cliente | Pontuação de valor e risco da conta em 6 dimensões |
| P5 | Comportamentos Challenger | Técnicas de venda consultiva (CH1–CH7) |
| P6 | Oportunidades Perdidas | Janelas comerciais que existiam e não foram aproveitadas |
| P7 | Cross-sell e Upsell | Produtos mencionados vs. ofertados; receita potencial por ligação |
| P8 | Objeções | Tipo de objeção do cliente e qualidade da resposta do vendedor |
| P9 | Abertura e Fechamento | Como o vendedor abriu e fechou a ligação (AB1–AB4, FC1–FC5) |
| P10 | Promessas | Compromissos assumidos pelo vendedor com prazo e risco |
| P11 | Inteligência Competitiva | Menções a concorrentes e como o vendedor reagiu (IC1–IC7) |
| P12 | Talk Ratio | Proporção de fala: vendedor vs. cliente |
| P13 | Padrões Emergentes | Comportamentos novos, temas recorrentes não mapeados (S1–S4) |
| P14 | Diferenças entre Vendedores | Comparação de 5 dimensões de performance entre vendedores |
| P15 | Eventos Raros de Alto Impacto | Sinais de baixa frequência + alto impacto (R1–R4) |

---

## 2. COMPORTAMENTOS DO VENDEDOR (B1–B10)
*Avaliados no Prompt P1. Cada comportamento detectado contribui com pontos para o score_comercial (0–18).*

| Código | Nome | O que significa | Peso |
|--------|------|-----------------|------|
| B1 | Diagnóstico | Vendedor fez perguntas sobre a situação do cliente antes de oferecer o produto | 2 |
| B2 | Storytelling | Vendedor usou caso de outro cliente como exemplo | 1 |
| B3 | Proposta de valor | Vendedor conectou o produto a uma necessidade explícita do cliente | 1 |
| B4 | Escuta ativa | Vendedor parafraseou ou confirmou o que o cliente disse | 1 |
| B5 | Upsell | Vendedor tentou expandir o contrato ou ofertou produto adicional | 2 |
| B6 | Urgência | Vendedor criou pressão de tempo com fato real (prazo, preço, disponibilidade) | 2 |
| B7 | Objeção tratada | Vendedor respondeu uma objeção do cliente com argumento estruturado | 1 |
| B8 | Pergunta aberta | Vendedor usou perguntas abertas para aprofundar a conversa | 1 |
| B9 | Confirmação de alinhamento | Vendedor checou ao final se o cliente entendeu e concordou | 1 |
| B10 | Sondagem de concorrência | Vendedor perguntou sobre outros fornecedores ou frota própria do cliente | **3** |

**Score_comercial máximo:** 15 pontos (soma dos pesos de B1–B10).

---

## 3. COMPORTAMENTOS CHALLENGER (CH1–CH7)
*Avaliados no Prompt P5. Cada comportamento recebe avaliação de qualidade (baixa/média/alta) e resultado imediato (cliente_aceitou / cliente_refletiu / sem_reacao_visivel).*

| Código | Nome | O que significa |
|--------|------|-----------------|
| CH1 | Custo oculto revelado | Vendedor mostrou um custo que o cliente não havia calculado (ex: diária × dias > mensal) |
| CH2 | ROI demonstrado | Vendedor calculou retorno financeiro do produto para aquele cliente específico |
| CH3 | Urgência com fato | Vendedor criou pressão com dado real: prazo que expira, preço que sobe, disponibilidade limitada |
| CH4 | Dado do concorrente | Vendedor usou dado comparativo para se diferenciar da concorrência |
| CH5 | Dor conectada ao produto | Vendedor ligou uma dor declarada pelo cliente diretamente a uma funcionalidade do produto |
| CH6 | Antecipação de problema | Vendedor alertou sobre um problema futuro que o cliente ainda não havia percebido |
| CH7 | Necessidade não declarada | Vendedor descobriu uma necessidade que o cliente não sabia que tinha (e que o produto resolve) |

---

## 4. TIPOS DE FECHAMENTO (FC1–FC5)
*Avaliados no Prompt P9. FC1 é o fechamento mais forte; FC5 é ausência de fechamento.*

| Código | Nome | O que significa | Efetividade |
|--------|------|-----------------|-------------|
| FC1 | Compromisso duplo com prazo | Vendedor propõe data e o cliente confirma: "te ligo terça às 10 — você confirma?" | Alta |
| FC2 | Próximo passo só do vendedor | Vendedor assume uma ação ("vou te mandar a proposta"), mas sem compromisso do cliente | Média |
| FC3 | Convite genérico | "Qualquer coisa me chama" / "fico à disposição" — sem data, sem próximo passo | Baixa |
| FC4 | Fechamento em aberto | A ligação termina sem qualquer definição de continuidade | Muito baixa |
| FC5 | Inaplicável | Ligação de suporte puro onde não havia contexto para fechamento comercial | — |

---

## 5. TIPOS DE ABERTURA (AB1–AB4)
*Avaliados no Prompt P9.*

| Código | Nome | O que significa |
|--------|------|-----------------|
| AB1 | Contextualizada | Vendedor abre com referência ao histórico do cliente ou motivo claro da ligação |
| AB2 | Relacional | Vendedor abre com interesse genuíno na pessoa antes de falar de negócio |
| AB3 | Genérica | Abertura padrão sem personalização ("Bom dia, tudo bem?") |
| AB4 | Reativa | Vendedor responde a uma ligação recebida — cliente tomou a iniciativa |

---

## 6. TIPOS DE PROBLEMAS DO CLIENTE (P1–P11)
*Avaliados no Prompt P3. Atenção: a letra "P" aqui não é prompt — é o código do tipo de problema.*

| Código | Tipo de Problema |
|--------|-----------------|
| P1 | Acesso à plataforma (login, senha, biometria) |
| P2 | Faturamento com erro ou dúvida |
| P3 | Multa contestada |
| P4 | Manutenção do veículo |
| P5 | Sinistro / acidente |
| P6 | Atraso na entrega do veículo |
| P7 | Problema no sistema WebCorp / plataforma de gestão |
| P8 | Problema com condutor (cadastro, habilitação) |
| P9 | Problema com TAG / pedágio |
| P10 | Solicitação de reserva ou substituição |
| P11 | Problema de comunicação ou contato com a equipe |

---

## 7. SINAIS DE INTELIGÊNCIA COMPETITIVA (IC1–IC7)
*Avaliados no Prompt P11.*

| Código | Sinal |
|--------|-------|
| IC1 | Cliente menciona que usa (ou considera) outro fornecedor de locação |
| IC2 | Cliente menciona que é exclusivo da Localiza |
| IC3 | Cliente migrou de outro fornecedor para a Localiza |
| IC4 | Cliente tem ou considera ter frota própria |
| IC5 | Cliente compara preço da Localiza com concorrente |
| IC6 | Vendedor explorou o sinal competitivo ativamente |
| IC7 | Vendedor não explorou o sinal competitivo (perdeu a janela) |

---

## 8. STATUS COMPETITIVO (campo nos resultados de P11)

| Valor | Significado |
|-------|-------------|
| exclusivo_localiza | Cliente usa apenas a Localiza |
| divide_com_concorrente | Cliente distribui a frota entre Localiza e outro fornecedor |
| tem_frota_propria | Cliente tem veículos próprios (além de ou no lugar de locação) |
| indefinido | Não foi possível determinar a situação competitiva na ligação |

---

## 9. PADRÕES EMERGENTES (S1–S4)
*Avaliados no Prompt P13.*

| Código | Tipo de Padrão |
|--------|----------------|
| S1 | Comportamento novo do vendedor — não mapeado no framework original |
| S2 | Comportamento recorrente do cliente — problema ou sinal que aparece em múltiplas ligações |
| S3 | Sinal operacional — problema sistêmico que afeta múltiplos clientes |
| S4 | Sinal fraco de mudança — tendência incipiente que pode se tornar relevante |

---

## 10. EVENTOS RAROS (R1–R4)
*Avaliados no Prompt P15.*

| Código | Evento |
|--------|--------|
| R1 | Cliente anuncia expansão significativa de frota (oportunidade imediata) |
| R2 | Cliente anuncia risco de cancelamento ou exclusão da Localiza |
| R3 | Inteligência competitiva crítica (mudança de fornecedor, novo concorrente, preço agressivo) |
| R4 | Mudança estrutural no negócio do cliente (fusão, venda da empresa, mudança de política de frota) |

---

## 11. PORTFÓLIO DE PRODUTOS (PR1–PR12)
*Referenciados nos Prompts P7 e P15.*

| Código | Produto |
|--------|---------|
| PR1 | Locação mensal de veículos leves (produto principal) |
| PR2 | Localiza Pesados — locação de caminhões e utilitários pesados |
| PR3 | TAG / gestão de pedágio |
| PR4 | Seguro e proteção de frota |
| PR5 | Gestão de frota (telemetria, relatórios) |
| PR6 | Locação diária / avulsa |
| PR7 | Outros produtos não mapeados individualmente |

*Nota: PR8–PR12 existem no portfólio completo mas não foram identificados nos dados do período analisado.*

---

## 12. DESFECHOS (campo desfecho no Prompt P1)

| Valor | Significado |
|-------|-------------|
| fechou | A venda foi concluída ou o contrato foi assinado/ampliado na ligação |
| interessou_nao_fechou | Cliente demonstrou interesse mas não houve decisão — ficou em aberto |
| nao_era_venda | A ligação era de suporte, operacional ou administrativa — sem contexto de venda |
| sem_conteudo | Ligação muito curta, interrompida ou sem conversa identificável |

---

## 13. CLASSIFICAÇÕES DE POTENCIAL (scoring automático Python)

| Faixa | Classificação | Pontuação |
|-------|--------------|-----------|
| 20–30 | ALTO | Alto potencial comercial — prioridade máxima |
| 13–19 | MÉDIO | Potencial real — requer follow-up estruturado |
| 7–12 | BAIXO | Potencial limitado — monitorar |
| 0–6 | SEM POTENCIAL | Suporte puro ou sem oportunidade identificada |

---

*Documento de referência interna — Projeto de Inteligência Comercial | Localiza Frota PJ | Junho 2026*
