# Modelo de dados do BI v1

Modelo em estrela: uma fato (uma linha por tentativa de ligação) e dimensões pequenas. As regras de negócio (carga operacional, base do KPI, grupos de tempo) vivem em **colunas da fato** (Power Query), não dentro das medidas: assim a medida só soma e conta, e qualquer pessoa confere a regra olhando uma coluna.

```
                      Dim_Calendario ─┐
                      Dim_Carteira ───┤
                      Dim_Problema ───┤
                      Dim_TipoDemanda ┼──►  Fato_Ligacoes  ◄── (v1.1) Cliente_Contato · Tentativa_Seq (1:1) · Retornos_Devidos*
                      Dim_FaixaDuracao┘            ▲
                                                   └─ (sem relacionamento) Diagnostico_Pipeline · Atualizacao · Dicionario_Colunas
                                                      Dim_Challenger · Dim_Habilidade · Param_* · _Medidas
        * Retornos_Devidos liga-se a Dim_Calendario e Dim_Carteira pelas próprias colunas Data e CARTEIRA
```

## Tabelas

| Tabela | Origem | Linhas hoje | Papel |
|---|---|---|---|
| `Fato_Ligacoes` | `Fato_Ligacoes.m` (de `Ligacoes_Base`) | 19.078 | Uma tentativa de ligação. Sem texto livre, sem nome de vendedor |
| `Dim_Calendario` | DAX (`calendario_e_dimensoes.dax`) | 123 (31/08–31/12) | Dia, semana (seg–sex), mês, dia útil, sequência de dias úteis |
| `Dim_Carteira` | `F_Carteiras_Equipe` (DVINT) | ≈ 67 (as 67 que ligaram em setembro; a tabela de equipe pode ter mais) | Carteira → distrital → divisional |
| `Dim_Problema` | M (legenda P1–P15) | 16 | Código de problema com rótulo |
| `Dim_TipoDemanda` | M | 14 | `p2_tipo` → grupo (negociação, operacional, relacionamento, sem conteúdo) |
| `Dim_FaixaDuracao` | M | 5 | Faixas < 2, 2–5, 5–8, 8–12, > 12 min |
| `Dim_Habilidade` | DAX | 9 | Eixo da página 7 (Challenger e SPIN) |
| `Dim_Challenger` | M | 7 | Legenda CH1–CH7 (rótulo apenas na v1) |
| `Dim_Feriados` | M | 5 | Feriados que tiram o dia útil |
| `Diagnostico_Pipeline` | M (de `Ligacoes_Base`) | 10 | Verificações de cobertura da carga |
| `Dicionario_Colunas` | CSV do dicionário | 88 | Perfil das colunas (página 8) |
| `Atualizacao` | M | 1 | Carimbo da última atualização |
| `Param_Meta` | DAX | 10 | Baseline, metas, limites de alerta |
| `Param_MinLigacoes`, `Param_ReducaoP1`, `Param_TopPct` | DAX | — | Parâmetros de segmentação |
| `_Medidas` | DAX | 1 | Só hospeda as medidas |

## Relacionamentos

| De (1) | Para (*) | Direção do filtro |
|---|---|---|
| `Dim_Calendario[Data]` | `Fato_Ligacoes[Data]` | Única |
| `Dim_Carteira[CARTEIRA]` | `Fato_Ligacoes[CARTEIRA]` | Única |
| `Dim_Problema[Codigo]` | `Fato_Ligacoes[p3_problema_principal]` | Única |
| `Dim_TipoDemanda[p2_tipo]` | `Fato_Ligacoes[p2_tipo]` | Única |
| `Dim_FaixaDuracao[Faixa]` | `Fato_Ligacoes[FaixaDuracao]` | Única |
| v1.1: `Cliente_Contato[CodigoCliente8]` | `Fato_Ligacoes[CodigoCliente8]` | Única |
| v1.1: `Tentativa_Seq[id_transcricao]` | `Fato_Ligacoes[id_transcricao]` | 1:1 |
| v1.1: `Dim_Calendario[Data]`, `Dim_Carteira[CARTEIRA]` | `Retornos_Devidos[Data]`, `[CARTEIRA]` | Única |

Marcar `Dim_Calendario` como tabela de datas. Ordenar `MesAbrev` por `AnoMes`, `SemanaRotulo` por `SemanaInicio`, `DiaSemanaNome` por `DiaSemanaNum`, `Dim_Problema[Rotulo]` por `Ordem`, `Dim_FaixaDuracao[Faixa]` por `Ordem`.

## Colunas da fato que as medidas usam

| Coluna | Regra | Quem usa |
|---|---|---|
| `EhGPT` | `fonte_classificacao = "gpt"` | K2, K4, K5, K6, Challenger |
| `BaseKPI` | `EhGPT` e `DuracaoSeg` informada | K1, K7, TMA, horas, faixas |
| `TemProblema` | `tem_problema = "SIM"` | K1a, K2–K6 |
| `EhOperacional` | `TemProblema` ou `p2_tipo` em suporte, cobrança, pós-venda (manutenção e sinistro), dúvida de contrato | **K1** |
| `EhTipoNegociacao` / `EhNegociacao` | `p2_tipo` em nova venda, upsell, renovação, retenção, misto / e sem problema | faixas de duração / **K7** |
| `GrupoTempo` | Operacional com problema · sem problema · Negociação · Relacionamento · Sem conteúdo · Não classificado | página 3 |
| `Pendencia` | `TemProblema` e resolução diferente de SIM | K2 |
| `FechouOuVenda` | GPT `fechou_*` ou Gemini `venda` | taxa de fechamento |
| `BaseGemini` | Completed, com duração e análise Gemini | K1 Gemini |
| `ClasseLigacao` | POSITIVA, INFORMATIVA, DETRATORA, SEM ANALISE, SECRETARIA, IGNORAR | reconciliação (M-01, M-09) |
| `Classe_Legada` | Regra antiga | reconciliação |

## Colunas a ocultar na visão de relatório

`id_transcricao`, `segment_id`, `Chave`, `ChaveAnoMes`, `CodigoCliente8`, `Classe_Legada`, todas as colunas booleanas de apoio (`Eh*`, `Tem*`, `Base*`, `Pendencia`, `Fechou*`), `DataHora`, `DuracaoSeg`. As medidas as usam; ninguém precisa arrastá-las para um visual.

## Atualização

- **Diária, antes das 08h** (meta C3). Com gateway: agendar 06h e 07h; sem gateway: atualização manual até o gateway sair (README, seção 4).
- O SQL lê só linhas com `DATA_INCLUSAO_REGISTRO >= pInclusaoDesde`. Com ~19 mil linhas por mês, o modelo fica leve até dezembro (~100 mil linhas). Se a atualização passar de 10 minutos, ativar atualização incremental por `Data`.
- `Atualizacao[Quando]` guarda o horário (Brasília) da última carga; o cabeçalho de cada página o exibe.

## Princípios que não mudam

1. Medida só soma e conta; regra de negócio é coluna.
2. Todo número de KPI tem uma linha em `reconciliacao.csv`.
3. Todo texto livre fica fora do modelo da empresa toda.
4. Todo limite de alerta, meta e baseline está em `Param_Meta`, não dentro de medida.
