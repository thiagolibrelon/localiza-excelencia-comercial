# Plano de oportunidades — Missão 4T26

> **Draft v0.1 — 01/10/2026.** Plano separado para as **89 oportunidades** de `AUDITORIA_DADOS_E_OPORTUNIDADES.md`. O plano da missão (`PLANO_MISSAO_4T26.md`) compromete a redução da carga operacional;
> este plano organiza **tudo o que a exploração dos dados pode gerar**: o que entregar, em que ordem, com que capacidade e com que critério para parar.
> Fontes de dado: o CSV de setembro e o código M. A única exceção é a legenda dos códigos P1–P15 e CH1–CH7, que vem do repositório.
> Os prazos dos dossiês coincidem com os da missão (D1 23/10 · D2 30/10 · D3 06/11 · D4 19/11 · D5 04/12). As estimativas de esforço são minhas e precisam de calibragem.

---

## 1. O que este plano é, e o que não é

- **É** o portfólio de exploração: 89 oportunidades agrupadas em **12 pacotes de entrega**, cada um com dono, data, esforço e critério de aceite.
- **Não é** compromisso de fazer tudo. Só entra no calendário o que passa por **três gates** (seção 3) e cabe na **capacidade** (seção 5).
- **Regras do jogo:**
  1. Há **um mês** de dados e nenhum resultado real depois da ligação: todo achado é **descritivo**. Recomendação de ação só sai de **experimento** com piloto e controle (seção 7).
  2. Toda entrega tem dono e data; toda lacuna vira pedido de dado (pacote PK12).
  3. Nada de ranking punitivo: carteira e vendedor são 1:1, então comparações usam a mediana e carteiras de perfil parecido.
  4. Texto livre e trechos têm dado pessoal: só circulam com perfil de acesso e máscara (PK02).

---

## 2. O portfólio em números

| Visão | Resultado |
|---|---|
| Oportunidades | **89**: 65 prontas, 16 parciais, 8 dependem de dado que não temos |
| Pacotes | **12**: 4 compartilhados com a missão (21 dias) e 8 só de oportunidades (34 dias) |
| Eixos | E1 16 · E2 10 · E3 11 · E4 14 · E5 7 · E6 7 · E7 16 · E8 8 |
| Por onda do catálogo | Onda 1: 50 · Onda 2: 29 · Onda 3: 10 |

**As ondas do catálogo dizem quando o dado permite; os pacotes dizem o que será entregue.** A seção 5 mostra quantos pacotes cabem em cada capacidade.

---

## 3. Como priorizamos

**Valor do pacote** = soma, sobre os itens, de *impacto* (alto 3, médio 2, baixo 1) × *prontidão* (pronto 1, parcial 0,5, lacuna 0).
**Valor por dia** = valor ÷ dias estimados. Pacotes **compartilhados com a missão** (PK01, PK02, PK03, PK11) não competem por capacidade: entram sempre. Pacotes **habilitadores** entram sempre e consomem capacidade: PK06 (as listas que alimentam o experimento EX4 da missão) e PK12 (pedidos de dado).

**Gates (um item só entra no calendário se passar nos três):**

| Gate | Pergunta | Se não passar |
|---|---|---|
| G1 · Dado | O dado existe no CSV hoje, ou o pedido de dado já tem dono e prazo? | Vai para PK12 (pedido) e fica na Onda 3 |
| G2 · Dono | Existe uma gerência que vai usar a entrega e decidir com ela? | Fica no catálogo, sem calendário |
| G3 · Esforço | Cabe na capacidade do trimestre (seção 5)? | Entra na lista "se sobrar capacidade" |

**Definição de pronto por tipo de entrega:**

| Tipo | Pronto quando |
|---|---|
| Correção de dado | A correção está no Power Query ou no pipeline e o BI mostra a cobertura |
| Dossiê | 2–4 páginas com número, intervalo, ressalva, recomendação e dono; revisado pela gerência usuária |
| Lista | Planilha ou página do BI com dono, data de tratamento e retorno do resultado |
| Experimento | Hipótese, métrica, piloto e controle, regra de decisão e leitura publicada |
| Produto de treinamento | Conteúdo curado, regra de pontuação, plano de medição e carteiras usando |
| Rotina e BI | Roda sem intervenção por 5 dias úteis, com ata ou alerta |

---

## 4. Os 12 pacotes

| Pacote | Entrega | Tipo | Cliente interno | Datas | Dias | Itens | Prontos / parciais / lacunas |
|---|---|---|---|---|---:|---|---|
| **PK01** | Fundação de dados e código M *(compartilhado)* | Correção de dado | Dados/TI + Excelência Comercial | 09/10 (baseline) · 13/10 (código M) | 8 | 15 (O-16, O-58, O-66, O-68–75, O-77–78, O-80–81) | 15 / 0 / 0 |
| **PK02** | Governança e LGPD *(compartilhado)* | Correção de dado | Dados/TI + Jurídico/Privacidade | 16/10 | 3 | 2 (O-67, O-76) | 1 / 0 / 1 |
| **PK03** | Dossiê: carga operacional e capacidade (D1) *(compartilhado)* | Dossiê | Gerência Operacional | 23/10 | 5 | 13 (O-01–05, O-07–09, O-11, O-14–15, O-31, O-85) | 11 / 2 / 0 |
| **PK04** | Dossiê: tempo e ritmo da ligação (D1) | Dossiê + experimento | Gerência Comercial | 23/10 | 4 | 9 (O-17–25) | 7 / 2 / 0 |
| **PK05** | Dossiê: contato, cadência e retorno no prazo (D2) | Dossiê + lista | Gerência Comercial | 30/10 | 5 | 14 (O-27–30, O-32–36, O-53–57) | 14 / 0 / 0 |
| **PK06** | Listas ativas para a Operação | Lista | Gerência Operacional | 30/10 | 2 | 2 (O-06, O-10) | 2 / 0 / 0 |
| **PK07** | Dossiê: Challenger e SPIN (D3) | Dossiê | Treinamento + Gerência Comercial | 06/11 | 4 | 8 (O-38–41, O-43–46) | 7 / 1 / 0 |
| **PK08** | Trilha de conhecimento do vendedor (MVP) | Produto de treinamento | Treinamento | 13/11 (gate) · 27/11 (conteúdo) · 07/12 (MVP) | 10 | 6 (O-42, O-47–51) | 2 / 3 / 1 |
| **PK09** | Dossiê: melhores práticas e carteiras desviantes (D5) | Dossiê | Gerência Comercial | 04/12 | 3 | 2 (O-52, O-84) | 0 / 2 / 0 |
| **PK10** | Dossiê: mercado, concorrência e Produto (D4) | Dossiê + lista | Gerência Comercial + Produto | 19/11 | 3 | 6 (O-59–64) | 3 / 3 / 0 |
| **PK11** | Gestão e BI: rituais, piloto e alertas *(compartilhado)* | Rotina e BI | Gerência Operacional + Excelência Comercial | 26/10 (ritual) · 16/11 (piloto) | 5 | 6 (O-82–83, O-86–89) | 3 / 2 / 1 |
| **PK12** | Pedidos de dado e lacunas | Coordenação | Excelência Comercial | 09/10 (pedidos) · quinzenal (cobrança) | 3 | 6 (O-12–13, O-26, O-37, O-65, O-79) | 0 / 1 / 5 |

**Critério de aceite de cada pacote:**

| Pacote | Aceite |
|---|---|
| **PK01** | Baseline congelado com versão por linha; M-01, M-02, M-05, M-06 corrigidos; IDs com 8 dígitos; valores-sentinela como nulo; duas réguas lado a lado; 'venda confirmada' e 'provável' definidas |
| **PK02** | Perfis de acesso e máscara aplicados a resumos, SPIN e trechos; auditoria de 100 ligações com ≥ 90% de concordância em `tem_problema` (C4) |
| **PK03** | 2–3 páginas: mapa de alocação, Pareto de problemas, pendências, origem inbound × outbound, simulador de horas e 3 hipóteses de ação com horas estimadas |
| **PK04** | Faixas de duração × resultado com intervalos de confiança; duração por tipo; protocolo de aprofundamento desenhado para o piloto; ressalva explícita de que é descritivo |
| **PK05** | Lista de recontato (≈ 2.985 clientes) e de retornos vencidos (1.634 devidos; 27,1% no prazo); cadência por tentativa; horário; capacidade por dia da semana; proposta de agenda de retorno |
| **PK06** | Lista de clientes reincidentes (18,8% das ligações com problema) e de contas de alto consumo (≈ 120 clientes = 20,1% do tempo), com dono e data de tratamento |
| **PK07** | Escada do Challenger e elo fraco do SPIN por carteira; Challenger × resultado com duração controlada; escala de qualidade recalibrada pelas sub-flags |
| **PK08** | Especificação aprovada em 13/11; biblioteca curada em 27/11; 2 trilhas e 10 lições no ar em 07/12; plano de medição ativo |
| **PK09** | Carteiras desviantes validadas contra ruído e perfil; metas por perfil de carteira; roteiro de 3 entrevistas para documentar a prática |
| **PK10** | Listas de frota própria (≈ 700 ligações) e de aluguel com concorrente (376); mapa de menções; dossiê ao Produto com P1, P2 e P13 e trechos |
| **PK11** | Leitura semanal rodando com ata; piloto pareado no ar; painel de coaching com trechos; alertas com limites por desvio |
| **PK12** | 9 pedidos com dono e prazo; amostra de diário de tempo (8–10 vendedores, 1 semana) agendada; resposta da base de resultado e de treinamento |

---

## 5. Ranking e corte por capacidade

**Capacidade assumida (a confirmar):** 25 dias-pessoa para oportunidades até 18/12, cerca de 46% dos 54 dias úteis restantes; o resto vai para a missão. Se a capacidade real for outra, o corte muda.

| Ordem | Pacote | Valor | Dias | Valor por dia | Dias acumulados | Papel |
|---:|---|---:|---:|---:|---:|---|
| 1 | **PK06** Listas ativas para a Operação | 6.0 | 2 | 3.0 | 2 | Habilitador da missão: listas da Operação (sempre entra) |
| 2 | **PK12** Pedidos de dado e lacunas | 1.0 | 3 | 0.3 | 5 | Habilitador: pedidos de dado (sempre entra) |
| 3 | **PK05** Dossiê: contato, cadência e retorno no prazo (D2) | 29.0 | 5 | 5.8 | 10 | Por valor por dia |
| 4 | **PK07** Dossiê: Challenger e SPIN (D3) | 19.5 | 4 | 4.9 | 14 | Por valor por dia |
| 5 | **PK04** Dossiê: tempo e ritmo da ligação (D1) | 16.5 | 4 | 4.1 | 18 | Por valor por dia |
| 6 | **PK10** Dossiê: mercado, concorrência e Produto (D4) | 10.0 | 3 | 3.3 | 21 | Por valor por dia |
| 7 | **PK09** Dossiê: melhores práticas e carteiras desviantes (D5) | 3.0 | 3 | 1.0 | 24 | Por valor por dia |
| 8 | **PK08** Trilha de conhecimento do vendedor (MVP) | 9.5 | 10 | 0.9 | 34 | Gate: depende de base de treinamento |

**O que cabe em cada capacidade** (pacotes compartilhados com a missão não entram na conta):

| Capacidade | Pacotes que cabem | Dias usados | O que fica de fora |
|---|---|---:|---|
| **15 dias** | PK06, PK12, PK05, PK07 | 14 | PK04, PK10, PK09, PK08 |
| **25 dias** | PK06, PK12, PK05, PK07, PK04, PK10, PK09 | 24 | PK08 |
| **35 dias** | PK06, PK12, PK05, PK07, PK04, PK10, PK09, PK08 | 34 | nada |

**Consequência para o plano da missão:** a entrega (5) do canvas ("MVP da trilha de conhecimento") só cabe com **35 dias**. Com 25 dias, a trilha vira **especificação + protótipo** (o protótipo navegável `prototipos/trilha_prototipo.html` já adianta parte) e o MVP passa para o 1º trimestre de 2027.
Decisão a tomar até 09/10.

---

## 6. Calendário (05/10 → 18/12)

Legenda: ■ em execução · ▲ entrega. **O calendário mostra o cenário de 35 dias**; no corte de 25 dias o PK08 vira só especificação (gate de 13/11), e no de 15 dias saem também PK04, PK10 e PK09.

| Pacote | 05/10 | 12/10 | 19/10 | 26/10 | 02/11 | 09/11 | 16/11 | 23/11 | 30/11 | 07/12 | 14/12 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| PK01 Fundação de dados e código M | ■ ▲ baseline | ▲ código M | | | | | | | | | |
| PK02 Governança e LGPD | | ■ ▲ | | | | | | | | | |
| PK12 Pedidos de dado | ▲ pedidos | | ■ | | ■ | | ■ | | ■ | | |
| PK03 + PK04 Dossiê D1 | | ■ | ■ ▲ D1 | | | | | | | | |
| PK05 + PK06 Dossiê D2 e listas | | | ■ | ▲ D2 | | | | | | | |
| PK11 Rituais, piloto e alertas | | | | ▲ ritual | ■ | ■ | ▲ piloto | ■ | ■ | ■ | |
| PK07 Dossiê D3 (Challenger e SPIN) | | | | ■ | ▲ D3 | | | | | | |
| PK10 Dossiê D4 (mercado e Produto) | | | | | | ■ | ▲ D4 | | | | |
| PK08 Trilha | | | | | ■ | ▲ gate | ■ | ▲ conteúdo | ■ | ▲ MVP | |
| PK09 Dossiê D5 (melhores práticas) | | | | | | | | ■ | ▲ D5 | | |
| Experimentos EX1–EX5 | | | | | | | ▲ início | ■ | ■ | ▲ leitura | |

---

## 7. Experimentos

Os experimentos usam os **6 pares de carteiras** do plano da missão (piloto e controle sorteados com carga operacional parecida). Eles são a única forma de transformar um achado descritivo em recomendação.

| # | Experimento | Tipo | Hipótese | Métrica | Linha de base | Amostra | Regra de decisão | Pacote |
|---|---|---|---|---|---|---|---|---|
| EX1 | **Agenda de retorno** | Produtividade | Mostrar ao vendedor, todo dia, os retornos devidos aumenta o retorno no prazo. | % de retornos com nova tentativa até o prazo + 2 dias | 27,1% (1.634 devidos até 30/09) | ≈ 160 retornos/mês nas 6 carteiras-piloto | Sucesso se piloto ≥ 40% e controle estável; poder suficiente em 4 semanas | PK05 |
| EX2 | **Segunda tentativa de recontato** | Produtividade | Uma 2ª tentativa em 1–3 dias úteis converte clientes que ficaram com uma única tentativa falha. | Conversas adicionais (Completed) por 100 clientes recontatados | 2ª tentativa atende 30,5%; 2.985 clientes com 1 tentativa falha | ≈ 270 clientes/mês nas 6 carteiras-piloto | Sucesso se atendimento da 2ª tentativa ≥ 30% sem queda do atendimento geral | PK05 |
| EX3 | **Protocolo de aprofundamento** | Produtividade | Conduzir até 8–12 min quando há decisor e dor identificada em 3 min melhora o avanço comercial. | POSITIVA, objetivo atingido e nota de demanda ≥ 8 (proxies); fechamentos por hora como leitura secundária | Fechamentos: 138 eventos/mês na base inteira | ≈ 15–20 fechamentos por grupo em 4 semanas: **sem poder estatístico para fechamentos**; decidir pelos proxies e por leitura qualitativa | Recomendar só se os proxies melhorarem no piloto e não no controle | PK04 |
| EX4 | **Triagem antes do outbound** | Missão (carga) | Checar pendências conhecidas do cliente (reincidentes) antes de ligar reduz ligações com problema no outbound. | K6 (taxa de problema) e K1 no outbound do piloto | Outbound com problema: 16,8%; 80% das ligações com problema nascem de ligação ativa | ≈ 600 ligações classificadas por 15 dias úteis nas 6 carteiras-piloto | Sucesso se K1 do piloto cair ≥ 5 p.p. a mais que o controle | PK06 |
| EX5 | **Trilha 'Resolver rápido' (T5) e 'Dado concreto' (T2)** | Missão (carga) + competência | Lições curtas sobre P1, P2, P13 reduzem o tempo de ligação com problema e aumentam o dado concreto. | TMA das ligações com problema; taxa de `p5_trouxe_dado` | TMA com problema 432 s; trouxe dado 14,0% | ≈ 160 ligações com problema por 15 dias úteis nas 6 carteiras-piloto | Sucesso se TMA cair ≥ 10% e dado concreto subir ≥ 3 p.p. contra o controle | PK08 |

**Cuidado de leitura:** com 138 fechamentos no mês na base inteira, o experimento EX3 não tem poder para detectar mudança em fechamentos; ele decide por proxies (POSITIVA, objetivo atingido, nota de demanda) e por leitura qualitativa.
Os experimentos da missão (EX4 e EX5) são os candidatos às "2 alavancas" do piloto de 16/11; EX1 e EX2 podem rodar nas mesmas carteiras sem interferir, porque medem outra coisa.

---

## 8. Dependências

| Depende de | Quem espera | Por quê |
|---|---|---|
| PK01 (baseline e código M) | Todos | Sem régua congelada e regra corrigida, nenhum número é comparável |
| PK02 (LGPD) | PK07, PK08, PK10, PK11 | Texto e trechos só circulam com perfil de acesso e máscara |
| PK12 (pedidos de dado) | PK08 (base de treinamento), PK03 (diário de tempo), PK05 (log de telefonia) | Cada lacuna é um pedido com dono |
| PK07 (escala do Challenger) | PK08 | A trilha precisa de uma escala que distinga níveis |
| PK03 e PK04 | Experimentos | Linha de base e hipótese saem dos dossiês D1 |
| Piloto (PK11) | EX1–EX5 | Piloto e controle são definidos uma vez e reaproveitados |

---

## 9. Riscos específicos do portfólio

| Risco | Prob. | Impacto | Mitigação |
|---|---|---|---|
| Tratar achado descritivo como causa | Alta | Alto | Toda recomendação passa por experimento; cada dossiê traz a seção "o que não sustentam" |
| Escopo crescer além da capacidade | Alta | Alto | Gates G1–G3; corte por capacidade na seção 5; nada novo entra sem tirar algo |
| Dossiês sem dono viram arquivo | Média | Alto | Cliente interno definido por pacote; revisão com a gerência antes da data de entrega |
| Fechamentos poucos demais para medir efeito | Alta | Médio | Proxies e leitura qualitativa; pedir a base de resultado real (PK12) |
| Comparação entre carteiras vira ranking | Média | Alto | Mediana e perfil; sem ranking nominal em ata |
| Texto com nomes circular sem máscara | Média | Alto | PK02 antes de PK07, PK08, PK10 e PK11 |

---

## 10. Decisões em aberto (até 09/10)

1. **Capacidade real para oportunidades** (15, 25 ou 35 dias até 18/12). Define se a trilha é MVP ou só especificação.
2. **Dono de cada pacote** na gerência usuária (Operacional, Comercial, Treinamento, Produto).
3. **Quais 2 experimentos** são as alavancas do piloto de 16/11.
4. **Quem fornece a base de treinamento** (gate de 13/11).

---

## 11. Protótipos já prontos

| Protótipo | Arquivo | O que cobre |
|---|---|---|
| Wireframe do BI | `prototipos/bi_wireframe.html` | As 8 páginas do BI com dados reais agregados; mostra as medidas dos pacotes PK03, PK04, PK05, PK06, PK07 e PK11 |
| Trilha do vendedor | `prototipos/trilha_prototipo.html` | Diagnóstico por carteira e 12 lições (T1 SPIN, T2 Challenger e T5 Resolver rápido) feitas de trechos reais do CSV, com nomes mascarados; adianta a especificação do PK08 |

As lições são **rascunho para curadoria do Treinamento**: os trechos e os códigos vêm do CSV, e as perguntas, opções e explicações foram escritas para o protótipo. `scripts/gerar_dados_prototipos.py` recalcula os agregados.

---

## 12. Itens por pacote

Lista completa em `anexos/catalogo_oportunidades.csv` (coluna `pacote`).


**PK01 · Fundação de dados e código M** (15 itens)

| ID | Oportunidade | Prontidão | Impacto |
|---|---|---|---|
| O-16 | Conversas reais fora de Completed | Pronto | Médio |
| O-58 | Duas fontes de 'venda' | Pronto | Alto |
| O-66 | Congelar versão e baseline | Pronto | Alto |
| O-68 | Reconciliar Gemini × GPT | Pronto | Alto |
| O-69 | Normalizar IDs de cliente | Pronto | Médio |
| O-70 | Campos saturados, constantes e redundantes | Pronto | Médio |
| O-71 | Valores-sentinela | Pronto | Médio |
| O-72 | Regra POSITIVA/INFORMATIVA/DETRATORA | Pronto | Alto |
| O-73 | Chave carteira + mês | Pronto | Médio |
| O-74 | Corte de data fixo | Pronto | Médio |
| O-75 | Timestamp e calendário | Pronto | Baixo |
| O-77 | Duração ausente de 23/09 em diante | Pronto | Alto |
| O-78 | Cobertura de classificação | Pronto | Alto |
| O-80 | Rótulos e formatos | Pronto | Baixo |
| O-81 | Legenda oficial dos códigos no dicionário do BI | Pronto | Médio |

**PK02 · Governança e LGPD** (2 itens)

| ID | Oportunidade | Prontidão | Impacto |
|---|---|---|---|
| O-67 | Auditoria amostral humana | Lacuna | Alto |
| O-76 | LGPD e perfis de acesso | Pronto | Alto |

**PK03 · Dossiê: carga operacional e capacidade (D1)** (13 itens)

| ID | Oportunidade | Prontidão | Impacto |
|---|---|---|---|
| O-01 | Carga operacional completa | Pronto | Alto |
| O-02 | Mapa de alocação do tempo | Pronto | Alto |
| O-03 | Pareto do tempo por problema | Pronto | Alto |
| O-04 | Horas excedentes por problema | Pronto | Médio |
| O-05 | Pendências geradas | Pronto | Alto |
| O-07 | Origem do problema (inbound x outbound) | Pronto | Médio |
| O-08 | Suporte dura tanto quanto venda | Pronto | Médio |
| O-09 | Composição do atendimento sem problema | Pronto | Médio |
| O-11 | Candidatos a autoatendimento ou automação | Parcial | Alto |
| O-14 | Quando o suporte chega | Pronto | Médio |
| O-15 | Alerta de incidente sistêmico | Parcial | Médio |
| O-31 | Inbound como porta do suporte | Pronto | Médio |
| O-85 | Simulador de capacidade | Pronto | Médio |

**PK04 · Dossiê: tempo e ritmo da ligação (D1)** (9 itens)

| ID | Oportunidade | Prontidão | Impacto |
|---|---|---|---|
| O-17 | O fechamento exige tempo | Pronto | Alto |
| O-18 | Zona de baixa eficiência de 2 a 5 minutos | Parcial | Médio |
| O-19 | Avanço comercial satura em 5–8 minutos | Pronto | Médio |
| O-20 | Duração das ligações fechadas por tipo | Pronto | Médio |
| O-21 | TMA alvo por tipo | Pronto | Médio |
| O-22 | Ligações muito curtas e secretária eletrônica | Pronto | Baixo |
| O-23 | Habilidade exige tempo | Pronto | Alto |
| O-24 | Benchmark de TMA por carteira | Pronto | Médio |
| O-25 | Fechamentos de menos de 2 minutos | Parcial | Baixo |

**PK05 · Dossiê: contato, cadência e retorno no prazo (D2)** (14 itens)

| ID | Oportunidade | Prontidão | Impacto |
|---|---|---|---|
| O-27 | Funil de contato | Pronto | Alto |
| O-28 | Recontato de clientes não atendidos | Pronto | Alto |
| O-29 | Melhor horário de ligação | Pronto | Baixo |
| O-30 | Dia da semana | Pronto | Baixo |
| O-32 | Esforço de discagem | Pronto | Alto |
| O-33 | Atendimento por carteira | Pronto | Médio |
| O-34 | Cadência ideal de tentativas | Pronto | Médio |
| O-35 | Capacidade por dia da semana | Pronto | Médio |
| O-36 | Clientes com muitas tentativas e nenhuma conversa | Pronto | Baixo |
| O-53 | Acesso ao decisor | Pronto | Alto |
| O-54 | Contato desatualizado | Pronto | Médio |
| O-55 | Retorno no prazo | Pronto | Alto |
| O-56 | Urgência não muda o comportamento | Pronto | Médio |
| O-57 | Prazo sugerido de retorno | Pronto | Baixo |

**PK06 · Listas ativas para a Operação** (2 itens)

| ID | Oportunidade | Prontidão | Impacto |
|---|---|---|---|
| O-06 | Reincidência de problema | Pronto | Alto |
| O-10 | Concentração do tempo em poucos clientes | Pronto | Alto |

**PK07 · Dossiê: Challenger e SPIN (D3)** (8 itens)

| ID | Oportunidade | Prontidão | Impacto |
|---|---|---|---|
| O-38 | Mapa de competências por carteira | Pronto | Alto |
| O-39 | Escada do Challenger | Pronto | Alto |
| O-40 | SPIN: elo fraco | Pronto | Alto |
| O-41 | SPIN × desfecho | Pronto | Médio |
| O-43 | Contraexemplos | Pronto | Médio |
| O-44 | Qualidade do Challenger sem variância | Parcial | Alto |
| O-45 | Uso dos 7 códigos Challenger | Pronto | Médio |
| O-46 | Efeito do Challenger no resultado | Pronto | Alto |

**PK08 · Trilha de conhecimento do vendedor (MVP)** (6 itens)

| ID | Oportunidade | Prontidão | Impacto |
|---|---|---|---|
| O-42 | Banco de conteúdo real | Pronto | Alto |
| O-47 | Curva de aprendizado | Parcial | Alto |
| O-48 | Dados de treinamento | Lacuna | Alto |
| O-49 | Gamificação sem gaming | Pronto | Médio |
| O-50 | Micro-lições por problema | Parcial | Alto |
| O-51 | Trilha de conhecimento do vendedor (MVP) | Parcial | Alto |

**PK09 · Dossiê: melhores práticas e carteiras desviantes (D5)** (2 itens)

| ID | Oportunidade | Prontidão | Impacto |
|---|---|---|---|
| O-52 | Desviantes positivos por carteira | Parcial | Alto |
| O-84 | Metas por perfil de carteira | Parcial | Alto |

**PK10 · Dossiê: mercado, concorrência e Produto (D4)** (6 itens)

| ID | Oportunidade | Prontidão | Impacto |
|---|---|---|---|
| O-59 | Lista de oportunidades: frota própria | Parcial | Alto |
| O-60 | Lista de reconquista: aluguel com concorrente | Parcial | Alto |
| O-61 | Concorrência na voz do cliente | Pronto | Médio |
| O-62 | Problemas sistêmicos para o Produto | Pronto | Alto |
| O-63 | Motivos de nova visita e objetivos | Parcial | Médio |
| O-64 | Ligações sem código de cliente | Pronto | Baixo |

**PK11 · Gestão e BI: rituais, piloto e alertas** (6 itens)

| ID | Oportunidade | Prontidão | Impacto |
|---|---|---|---|
| O-82 | Alertas diários | Parcial | Médio |
| O-83 | Ritual semanal | Pronto | Alto |
| O-86 | Painel de coaching por carteira | Pronto | Alto |
| O-87 | Pilotos pareados por carteira | Pronto | Alto |
| O-88 | Fila de ligações prioritárias | Parcial | Alto |
| O-89 | Previsão de carga | Lacuna | Médio |

**PK12 · Pedidos de dado e lacunas** (6 itens)

| ID | Oportunidade | Prontidão | Impacto |
|---|---|---|---|
| O-12 | Carga fora da ligação | Lacuna | Alto |
| O-13 | Horas devolvidas em R$ | Lacuna | Alto |
| O-26 | Talk ratio, silêncio e interrupções | Lacuna | Médio |
| O-37 | Motivo da falha de contato | Lacuna | Médio |
| O-65 | Resultado real depois da ligação | Lacuna | Alto |
| O-79 | Status Open | Parcial | Médio |
