# Plano de processamento — JULHO (01 a 21/07/2026)

## O que chegou

4 arquivos brutos (exportação em `;`, encoding **cp1252**, mesmo schema de sempre — 37 colunas, `transcricao_limpa` + `CLIENTE`):

| Arquivo | Período coberto | Linhas |
|---|---|---:|
| `arq1 - correto (1).txt` | 01/07 a 06/07 | 1.999 |
| `arq1 (1).2` | 06/07 a 10/07 | 1.999 |
| `arq2 (1).txt` | 10/07 a 14/07 | 1.999 |
| `arq2 (1).2` | 14/07 a 21/07 | 3.387 |
| **Total** | **01 a 21/07** | **9.384** |

Sem sobreposição entre os 4 (0 `cd_segmento` duplicado) — juntos cobrem o mês inteiro até 21/07, sem fim de semana (só dias úteis têm ligação).

**Achado crítico:** `cd_contato_master` veio corrompido pelo Excel (virou notação científica `7,11E+11`, colapsando milhares de IDs). Usamos `cd_segmento` (uuid, intacto) como ID único e `CLIENTE` como identificador do cliente.

## Conversão feita

`scripts/converter_julho.py` — lê os 4 brutos (cp1252), descarta linhas sem transcrição bem-sucedida, converte `AGENTE:/CLIENTE:` em `[A/C, texto]`, agrupa por cliente. Idempotente (reprocessa tudo do zero sempre que rodar de novo).

**Regra de exclusão de cliente (decidida em 22/07/2026, após checar o conteúdo das transcrições):**
- `CLIENTE="0"` (334 linhas): **excluído por completo**, com ou sem transcrição válida — checando o conteúdo, é majoritariamente correio de voz/ligação não atendida, sem valor de análise por cliente.
- `CLIENTE="Sem Informação"` (615 linhas, campo vem corrompido na fonte): quando a transcrição é válida (480 linhas) — conversa real de venda/suporte, só sem o vínculo de ID — **mantida**, mas com uma chave sintética própria por ligação (`SEMINFO_<segment_id>`) em vez de agrupar todas sob o mesmo "cliente" (isso criava um cliente fantasma de 480 ligações que quebrava o batching). Sem transcrição válida (135 linhas): excluída.

**Resultado (rodado em 22/07/2026, versão final):**
- 9.384 linhas lidas → 2.571 sem transcrição válida → 172 excluídas por `CLIENTE=0` (as com transcrição; as outras 162 já caem no filtro de transcrição) → **6.641 ligações usáveis**
- **5.450 "clientes"** (4.970 reais + 480 entradas sintéticas de 1 ligação cada, das "Sem Informação")
- Saída: `JULHO/dados_convertidos/julho_completo.json`

## Processamento Gemini

`scripts/analisar_gemini_julho.py` (cópia de `analisar_gemini_novo_lote.py`, mesma lógica e prompts — P1_P2, P5_P6, P9_P10 — só muda `FILE_PATH`/`OUTPUT_DIR`). Saída em `JULHO/resultados_gemini/`.

**Cota:** 20 chamadas/dia, compartilhada com `analisar_gemini_novo_lote.py` (mesma API key). Em 22/07 o novo_lote estava 100% completo (0 chamadas usadas hoje) — cota inteira liberada pro backlog de julho.

### Estimativa do backlog (6.641 ligações × 3 fases)

- `BATCH_SIZE=60` clientes/lote → 5.450 clientes ÷ 60 ≈ **91 batches**
- `MAX_LIG_PER_CALL=100` → batches grandes são divididos dinamicamente por contagem de ligações (fix aplicado em 22/07 — a divisão original só quebrava em 2, e um lote de 744 ligações estourava mesmo assim)
- 3 fases × ~91-100 chamadas efetivas ≈ **~270-300 chamadas totais**
- A 20 chamadas/dia (menos retentativas de truncagem) → **~15-16 dias corridos** pra zerar o backlog de 01-21/07, rodando 7 dias/semana (ver nota de fim de semana abaixo)

### Status (atualizado a cada execução — rodar `python scripts/gerar_status_prompts.py` pra conferir)

- 22/07/2026 18:05: primeira execução disparada. Achado durante o teste: `CLIENTE="0"` e `"Sem Informação"` precisavam de tratamento diferente (ver regra de exclusão acima) — os batches gerados antes da correção (batch01-17) foram **descartados** (grouping ficou obsoleto assim que os dados de entrada mudaram).
- 22/07/2026 18:45: horário da tarefa agendada alterado de 04:35 para **19:00**. Execução de hoje relançada do zero com os dados corrigidos — cota diária real já estava quase toda consumida pelos batches descartados (18/20 chamadas no servidor).
- 22/07/2026 18:46: confirmado — cota do servidor esgotada, 0 batches novos processados na tentativa manual.
- 22/07/2026 19:00: a tarefa agendada (ainda configurada pra 19:00 nesse momento) disparou sozinha e conseguiu rodar de verdade — **batch01, 02 e 03/91 [P1_P2] concluídos com sucesso** (finish=STOP, sem truncagem) antes de esgotar a cota de novo no batch04.
- 22/07/2026 19:07: horário revertido para **04:30** (pedido do usuário) — já é tarde demais pro disparo de hoje (19:00 já disparou), então a próxima execução automática é amanhã (23/07) às 04:30, retomando do batch04/91 em diante.

## Rotina diária daqui pra frente

1. **Usuário deposita os 4 tipos de arquivo do dia anterior em `JULHO/`** (mesmo nome de padrão: `arqN...`), OU um único export do dia — o conversor lê qualquer arquivo que bater com os nomes esperados em `ARQUIVOS` (ajustar a lista em `scripts/converter_julho.py` se o nome mudar).
2. `python scripts/converter_julho.py` — reconverte tudo (idempotente, sempre a partir do zero).
3. `python scripts/analisar_gemini_julho.py` — roda até 20 chamadas, resume de onde parou (idempotente via `ja_existe`).
4. Repetir os passos 2-3 todo dia — automatizar via Task Scheduler (ver abaixo) do mesmo jeito que `Localiza_GeminiNovoLote_Diario` já faz para o lote anterior.

**Por que sáb/dom não travam o fluxo:** não chega ligação nova no fim de semana, mas o script pode (e deve) rodar mesmo assim — usa a cota do dia pra reduzir o que sobrou da semana. Capacidade semanal (7×20 chamadas) folga confortavelmente acima do volume observado (pico de 3.537 ligações/semana ≈ 76% da capacidade) — mas só funciona se a tarefa agendada rodar TODO dia, sem falha.

## Saída

Todo resultado (batches Gemini + qualquer consolidação futura) fica dentro de `JULHO/` — não mistura com `resultados/gemini_novo_lote/` nem com o CSV consolidado antigo. Se/quando decidirem fundir julho ao consolidado principal, isso é um passo explícito e separado (ainda não feito).
