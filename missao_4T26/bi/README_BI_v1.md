# BI v1 — Excelência Comercial · venda interna (DVINT)

> **Publicação alvo: quarta-feira, 07/10/2026.** Pacote de montagem: Power Query corrigido, medidas DAX, tema, mockups das 8 páginas, especificação dos visuais, valores esperados de setembro e roteiro de publicação.
> **Leia primeiro a seção 1 (o que isto é e o que não é).**

---

## 1. O que isto é e o que não é

**É** o pacote para montar o BI no Power BI Desktop em 4 dias úteis e publicar na quarta, com os números de setembro (31/08–30/09) já conferidos contra o CSV.

**Não foi executado.** O Power Query (M) e o DAX foram escritos aqui sem Power BI à mão. Verifiquei só o que dá para verificar fora dele: parênteses e colchetes balanceados, toda coluna citada existe no dicionário do CSV, toda medida citada existe, e os valores esperados (`reconciliacao.csv`) saem do CSV por um script independente. Pode haver erro de sintaxe que o Desktop aponta na primeira colagem; a reconciliação existe para pegar erro de lógica. **Ninguém deve publicar antes de a reconciliação fechar.**

**Não é diário na quarta.** A duração das ligações só existe até 22/09 e a classificação do GPT até 25/09 (28–30/09 sem nenhuma). Se nada mudar nos dados até lá, a v1 mostra setembro com o fluxo todo montado; ela passa a mostrar o dia anterior quando (a) a tabela de duração voltar a atualizar (pedido de dado nº 1 da auditoria) e (b) o classificador rodar todo dia (entrega E5, 16/10). A página 8 existe justamente para isso ficar visível.

**O baseline é provisório.** K1 = 43,2% (01–22/09, régua GPT) e as metas (−5 p.p. geral, −10 p.p. piloto) saem dele. O baseline congelado (setembro inteiro, uma versão do classificador) é a entrega E2 de 09/10. O BI mostra esse aviso em todas as páginas.

---

## 2. O que tem nesta pasta

| Caminho | O que é |
|---|---|
| `powerquery/00_parametros.m` | Parâmetros `pInclusaoDesde` (data de corte do SQL) e `pFusoHoras` (−3) |
| `powerquery/01_Ligacoes_Base.m` | Consulta de staging: o SQL original parametrizado + junções, sem filtro de linha (desabilitar carga) |
| `powerquery/Fato_Ligacoes.m` | Tabela fato: filtros, colunas derivadas (`EhOperacional`, `BaseKPI`, `GrupoTempo`…), classificação corrigida, sem texto livre |
| `powerquery/Dim_*.m`, `Dim_Feriados.m`, `Atualizacao.m` | Dimensões e carimbo de atualização |
| `powerquery/Diagnostico_Pipeline.m`, `Dicionario_Colunas.m` | Fonte da página 8 |
| `powerquery/Cliente_Contato.m`, `Tentativa_Seq.m`, `Retornos_Devidos.m` | v1.1 (recontato e retorno no prazo, página 6) |
| `powerquery/Textos_Restrito.m`, `Dim_Vendedor_Restrito.m`, `Dim_Acesso.m` | Só para modelo de gestão com RLS. **Não** entram no relatório da empresa toda |
| `powerquery/Dim_Cliente.m`, `Resumo_Time.m` | Só para a página 9, "Meu painel" (v1.2) |
| `dax/calendario_e_dimensoes.dax` | Tabelas calculadas (calendário, metas, parâmetros, habilidades) e a lista de relacionamentos |
| `dax/medidas.dax` | **166 medidas** (19 delas da página do vendedor), com pasta de exibição e formato em comentário |
| `dax/medidas_por_escopo.md` | Quais medidas criar primeiro: **88 do núcleo** (páginas 1–5 e 8), +14 de reconciliação, +34 das páginas 6–7 |
| `dax/rls.dax` | Funções de RLS (Gestão, Distrital, Carteira) e como testar |
| `tema/Excelencia_Comercial.json` | Tema do relatório (azul = negociação, laranja = carga operacional) |
| `mockups/png/` e `mockups/*.pdf` | Imagens das 9 páginas (8 do relatório de gestão + "Meu painel"), versão limpa e anotada (ID do visual + medidas) |
| `mockups/bi_mockups.html` | As mesmas imagens, navegáveis |
| `especificacao_visuais.md` | 61 visuais v1, 4 v1.1 e 9 v1.2 (página 9, do vendedor): tipo, campos, medidas, filtros, observações |
| `modelo.md` | Modelo estrela, relacionamentos, colunas a ocultar, atualização |
| `reconciliacao.csv` | **151 valores esperados** de setembro (12 deles da página do vendedor, com a carteira S1I05A de exemplo), com período, filtro e tolerância; colunas em branco para preencher |
| `post_lancamento.md` | Texto do comunicado, perguntas frequentes e o que não concluir dos números |
| `../../scripts/reconciliar_bi_v1.py` | Gera `reconciliacao.csv` a partir do CSV (independente do Power BI) |

---

## 3. Escopo de 07/10

| Entra na v1 (07/10) | Fica para a v1.1 (até 20/10) |
|---|---|
| **Núcleo:** páginas 1 Dia · 2 Semana · 3 Mês · 4 Problemas · 5 Carteiras · 8 Qualidade do dado | Cartões de recontato e retorno no prazo (página 6) |
| **Se der tempo:** páginas 6 Tempo e ritmo e 7 Competências (todos os visuais que saem só da `Fato_Ligacoes`) | Trecho para coaching com acesso restrito (página 7) |
| Segmentações Período, Distrital e Carteira sincronizadas | Alerta de mudança de régua e de pico de P1 (precisa de coluna de versão do classificador) |
| Aviso de baseline provisório e de "duração até 22/09" | Ficha da carteira (drill-through) · RLS por distrital e carteira abertos aos vendedores |

**Ordem de corte se faltar tempo** (do que cortar primeiro): simulador de P1 (3.9, 3.10) → 2.8 → 5.3 → páginas 6 e 7 → 4.7. **Não cortar:** página 8, 1.6–1.9, 3.1–3.8, 4.6, 5.1 e o aviso de baseline provisório.

---

## 4. Cronograma (quinta 01/10 a quarta 07/10)

| Dia | Entrega do dia | Critério de saída |
|---|---|---|
| **Qui 01/10** (hoje) | Decidir audiência e RLS (seção 6). Confirmar acesso: Power BI Desktop, workspace com licença Pro, gateway com o DSN `lclz-dados` para atualização agendada. Criar os parâmetros, colar `01_Ligacoes_Base`, `Fato_Ligacoes`, dimensões, `Diagnostico_Pipeline`; primeiro refresh | Fato com **19.078 linhas** e sem erro de coluna. Linhas M01–M11 do `reconciliacao.csv` conferidas. Histograma de ligações por hora com vale em 12–13h (valida o fuso) |
| **Sex 02/10** | Tabelas calculadas e relacionamentos; medidas do núcleo e de reconciliação (102); tema | Linhas K, P, C, S, Q, W e D do `reconciliacao.csv` dentro da tolerância |
| **Seg 05/10** | Construir páginas 1–5 seguindo `especificacao_visuais.md` e `mockups/png/*_anotado.png`; segmentações sincronizadas | Páginas 1–5 abrem sem erro, filtro por distrital e carteira funciona |
| **Ter 06/10** | Página 8 (e 6 e 7 se der); RLS e teste "Exibir como"; publicar em workspace de teste; revisão com a Gerência Operacional; **E1** (dicionário de KPIs validado pelo chefe) | Reconciliação 100% preenchida; nenhuma linha fora da tolerância sem explicação escrita |
| **Qua 07/10** | Publicar o app; enviar o comunicado (`post_lancamento.md`); acompanhar a atualização das 07h do dia seguinte | Relatório aberto pelo chefe e pela Gerência Operacional; lista de ajustes da v1.1 |

**Plano B de atualização.** Se o gateway/DSN não estiver pronto até terça, publicar o `.pbix` com atualização manual (abrir no Desktop, atualizar, republicar) e dizer isso no comunicado. A data de publicação não depende do agendamento.

---

## 5. Montagem, passo a passo

1. **Parâmetros.** Gerenciar Parâmetros: criar `pInclusaoDesde` (data, 01/09/2026) e `pFusoHoras` (−3), conforme `00_parametros.m`.
2. **Manter as consultas existentes** `F_Carteiras_Equipe`, `Tempo_de_ligação` e `Ligações Classificadas` como estão: as novas dependem delas.
3. **Criar `Ligacoes_Base`** com `01_Ligacoes_Base.m`. Desmarcar *Habilitar carga*. O SQL é o original; só o filtro de data virou parâmetro.
4. **Criar as demais consultas**, na ordem: `Fato_Ligacoes`, `Dim_Carteira`, `Dim_Problema`, `Dim_TipoDemanda`, `Dim_FaixaDuracao`, `Dim_Challenger`, `Dim_Feriados`, `Atualizacao`, `Diagnostico_Pipeline`, `Dicionario_Colunas` (ajustar o caminho do CSV). Deixar as de v1.1 e as restritas para depois.
5. **Fechar e Aplicar.** Primeiro refresh (pode levar alguns minutos; o `CommandTimeout` do SQL é de 30 min).
6. **Tabelas calculadas** de `dax/calendario_e_dimensoes.dax`, na ordem indicada no cabeçalho.
7. **Relacionamentos** conforme a lista no fim do mesmo arquivo; colunas de chave ocultas (`modelo.md`).
8. **Medidas** de `dax/medidas.dax` na tabela `_Medidas`, na ordem do arquivo; começar pelo núcleo (`dax/medidas_por_escopo.md`).
9. **Reconciliar** (seção 7) antes de desenhar página.
10. **Tema** (`tema/Excelencia_Comercial.json`), páginas e visuais conforme `especificacao_visuais.md`.
11. **RLS**, teste, publicação.

**Se a classificação não bater com a consulta antiga:** a coluna `Classe_Legada` da Fato reproduz a regra antiga. A matriz `Classe_Legada` × `ClasseLigacao` deve mostrar: POSITIVA 2.015 = 2.015, INFORMATIVA 1.652 = 1.652, DETRATORA antiga (2.511) = 1.854 DETRATORA + 657 SEM ANALISE, IGNORAR antiga (12.900) = 12.582 IGNORAR + 318 SECRETARIA. Qualquer outra diferença é bug da montagem.

---

## 6. Antes de publicar: audiência, LGPD e RLS

Decisões que o BI não toma por você e que precisam estar fechadas **na quinta**:

| Decisão | Recomendação desta v1 | Por quê |
|---|---|---|
| Quem vê | Publicar para **gestão** (Excelência Comercial, Gerência Operacional e Comercial, distritais). Abrir aos vendedores depois, com a função `Carteira`, após conversa com a Gerência e o jurídico/RH | O BI é por carteira e carteira é 1:1 com vendedor; "carteira" não anonimiza |
| Nome do vendedor | **Fora** do modelo publicado (`Dim_Vendedor_Restrito` só no modelo de gestão) | A missão mostra por carteira; o nome é só atributo restrito |
| Texto livre das ligações | **Fora** (`Textos_Restrito` só no modelo de gestão, v1.1) | Resumos e trechos citam nome de vendedor (46% dos resumos) e podem trazer nome e telefone do contato do cliente |
| Código do cliente | Coluna oculta, usada só em K5 e concentração | Não aparece em nenhum visual |
| Linguagem | "Carga operacional", "ligações com problema". Nunca "vendedor com problema" | O BI remove obstáculos; não pune |
| Aviso | Baseline provisório e "duração até 22/09" visíveis em todas as páginas | Evita que o número seja lido como definitivo |

---

## 7. Reconciliação: como usar `reconciliacao.csv`

1. Abrir o relatório com o período de cada linha (coluna `periodo`) e o filtro adicional.
2. Preencher `valor_no_bi` e `confere` (S/N). Cada linha traz a tolerância absoluta; inteiros devem ser iguais.
3. Onde não bater, diagnosticar por camada, de baixo para cima: **(1)** número de linhas da Fato (M01) → **(2)** colunas derivadas (`BaseKPI`: 3.546 linhas em 01–22/09) → **(3)** medida base (`Seg Base KPI` = 957.210 s = 265,9 h) → **(4)** medida do KPI → **(5)** visual (filtro de visual esquecido).
4. O que não pode ser conferido antes da primeira atualização real: M05 (Data igual à data UTC antiga — comparar com a coluna `Data` da consulta antiga), e as linhas 2–3 do `Diagnostico_Pipeline` (o CSV já vem filtrado).

Valores de referência (01–22/09, janela do baseline): K1 **43,2%** · K1a 30,0% · K1b 13,1% · K7 35,1% · K1 Gemini 47,6% · 3.546 ligações · 265,9 h · K2 698 · K4 10,3% · K5 18,8% · K6 19,1% · TMA 432 s vs 232 s · K3 36,9 h.

---

## 8. Limites conhecidos (para dizer em voz alta)

| Limite | Efeito no BI | O que resolve |
|---|---|---|
| Duração parou em 22/09 (C2 = 0% depois) | K1, K7, horas e faixas não existem para 23–30/09; páginas 3, 5 e 6 usam 01–22/09 | Pedido de dado nº 1 |
| Classificação GPT: 0 em 28–30/09, parcial em 24/09 | K2, K4, K5, K6 e Challenger deixam de existir nesses dias; C1 cai | Pipeline D-1 (E5, 16/10) |
| Régua do GPT mudou em 15/09 (taxa de problema 13,6% → 27,4%) | K6 e K2 sobem sem piora real comprovada; Gemini cai enquanto o GPT sobe | Baseline E2 (09/10) e coluna de versão (pedido novo N1) |
| K1 diário de carteira com poucas ligações oscila 20–50 p.p. | Alerta por carteira só com 8+ ligações; ranking só com 40+ | Ler a página 5 no período inteiro |
| Medianas de carteira dentro de RLS | Quem vê só uma carteira terá a própria como "mediana" | Tabela `Resumo_Time` fora do RLS (v1.1) |
| Fechamento = GPT "fechou" ou Gemini `venda` (kappa 0,46) | Taxa de fechamento é indício, não verdade | Resultado real depois da ligação (pedido nº 2) |
| 07/09 é feriado | 15 dias úteis em 01–22/09; K2/dia usa dias com classificação | `Dim_Feriados` (conferir feriados municipais) |

**Pedidos novos** (somam-se aos 9 da auditoria): **N1** coluna `versao_classificador` por linha (M-08; E2 exige "versão gravada por linha") · **N2** máscara de nome e telefone nos textos livres, na origem · **N3** classificação do GPT rodando todos os dias úteis (E5).

---

## 9. Página do vendedor ("Meu painel", v1.2)

**Faz sentido**, com três ajustes de desenho. Mockup em `mockups/png/p9_meu_painel*.png` (exemplo com a carteira S1I05A, números reais de setembro); especificação nos visuais 9.1–9.9.

1. **Relatório separado, mesmo modelo.** O vendedor não deve ver as páginas de gestão. Publicar "Meu painel" como relatório próprio sobre o mesmo conjunto de dados, em um app com público-alvo "vendedores", RLS `Carteira` (`dax/rls.dax`) e **permissão só de visualização** (sem Compilar). Atenção: `Dim_Cliente` não passa pelo RLS; quem puder compilar sobre o conjunto de dados poderia listar códigos de cliente de outras carteiras.
2. **"Clientes detratores" vira "conversas sem objetivo atingido" e "clientes para retomar".** No dado, *detratora* é a classe de uma **conversa** (objetivo não atingido), não um cliente. Chamar cliente de detrator seria impreciso (não é NPS) e pesaria contra o vendedor. O que ajuda o vendedor a agir é a lista de clientes para retomar, por três motivos que existem no dado: problema sem resolução na ligação, retorno pedido pelo cliente já vencido e uma única tentativa sem sucesso há 7+ dias. Em setembro, a carteira de exemplo tem 24, 32 e 49 clientes nessas três listas.
3. **Comparação com o time sem expor colegas.** O time vem de `Resumo_Time` (agregado do time inteiro, fora do RLS); não há ranking nem carteira de outros. O texto é neutro ("+3,6 p.p. em relação ao time"), nunca "pior".

**Quando.** Tecnicamente cabe na v1.1 (20/10). **Para o vendedor, só depois** de a Gerência Operacional e o RH/jurídico concordarem e de o RLS ser testado com 2 ou 3 vendedores. A sugestão é abrir junto com o piloto (16/11), quando as carteiras-piloto passam a ter um motivo claro para olhar o próprio tempo.

**Limites desta página.** "Sem resolução" é na ligação: a medida não enxerga se outra ligação resolveu depois. O comparativo com o time só existe com duração (01–22/09). O código completo do cliente aparece para o dono da carteira.

---

## 10. Mudanças no plano da missão

`PLANO_MISSAO_4T26.md` (v0.3.2): marco **07/10 BI v1 provisório** (E6a); **E6** (20/10) vira BI v1.1; **E7** (30/10) vira BI v2 em produção com baseline congelado e pipeline D-1; K6 passa a ser medido sobre todas as classificadas (19,1% em 01–22/09; os 18,8% anteriores eram só com duração). O gate de 16/10 passa a valer para o BI **oficial**; a v1 de 07/10 é rotulada como provisória.
