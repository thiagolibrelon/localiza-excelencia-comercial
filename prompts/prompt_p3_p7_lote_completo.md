# Prompt combinado P3+P7 — colar no Fable junto com cada lote

Uso: para cada arquivo `resultados/exploracao_fable/inputs_completo/loteNNN.txt`,
colar este prompt + o conteúdo do lote numa única mensagem no Fable. Salvar a
resposta em `resultados/exploracao_fable/outputs_completo/loteNNN_resultado.md`.

Fonte: `prompts/prompts_analises_separados.md` (PROMPT 3 e PROMPT 7, formato lote —
não usar a versão "por ligação" de `prompts_nivel1_por_ligacao.md`, que é para 1
ligação isolada).

---

Você é um analista de Customer Success e de expansão de receita em contas B2B de locação de frotas corporativas (Localiza — locação mensal PJ). Vendedor = "A", Cliente = "C". STT fragmentado — junte turns do mesmo speaker. `<unk>` = inaudível, ignore.

Você vai receber um LOTE de ligações (dezenas de ligações, cada uma delimitada por `=== LIGACAO | Base:... | Cliente:... | Data:... | Dur:...s | Sent:... ===`). Analise TODAS as ligações do lote e produza as duas análises abaixo (P3 e P7).

## PARTE P3 — PROBLEMAS RECORRENTES
### Categorias de problema
| Código | Categoria | Exemplos |
|--------|-----------|---------|
| P1 | Acesso/sistema | Portal fora do ar, senha, biometria, dois portais distintos |
| P2 | Faturamento/cobrança | Boleto errado, fatura para terceiro, valor incorreto |
| P3 | Multa/infração | Multa no condutor errado, prazo de indicação, contestação |
| P4 | Manutenção/substituto | Carro em oficina, demora, sem substituto disponível |
| P5 | Condutor/cadastro | Troca de condutor, demitido com acesso, habilitação |
| P6 | Km excedente | Cobrança incorreta, plano errado, negociação de desconto |
| P7 | Disponibilidade | Carro reservado indisponível, categoria esgotada |
| P8 | Franquia/agência | Processo diferente em franqueada, fatura não baixada |
| P9 | Sinistro | Acidente, franquia de dano, mudança de oficina |
| P10 | Reserva/sistema | Reserva não aparece no sistema, status incorreto, erro ao criar/editar uma reserva, bug reproduzível do fluxo de reserva. **Não** marcar P10 quando for só dúvida de como navegar/usar o portal sem nenhum erro real (isso é "nenhum", não P10), nem quando o assunto real da ligação for outro (fatura, cadastro, troca de contato comercial) e "reserva" só aparecer de passagem. |
| P11 | Outro | Descrever |
| P12 | Manipulação de pesquisa/NPS | Vendedor pede/dita a nota da pesquisa de satisfação — problema de integridade do indicador, não do cliente. Marcar `quem_relatou=vendedor_detectou`, `foi_resolvido_na_ligacao=NAO` |

Identifique CADA problema mencionado ou vivenciado em cada ligação (um problema pode se repetir entre clientes). Só marque um código se o problema for tema central ou relevante da ligação — não marque por menção tangencial de 1 palavra-chave sem um problema real por trás dela.

**Saída — Parte 1 (por ligação):**
```
cliente_id,data,problemas_identificados,quem_relatou,foi_resolvido_na_ligacao,escalou_para,observacao
```
- `problemas_identificados`: códigos separados por `+` (ex: P1+P3)
- `quem_relatou`: cliente / vendedor_detectou
- `foi_resolvido_na_ligacao`: SIM / NAO / PARCIAL
- `escalou_para`: 0800 / supervisora / IT / nao_escalou

**Saída — Parte 2 (consolidado do lote):**
```
codigo,categoria,total_ocorrencias,clientes_afetados,resolvido_na_ligacao_%,escala_%
```

Depois, responda: (1) quais problemas são sistêmicos? (2) quais o vendedor resolve sem escalar, e como? (3) quais escala desnecessariamente? (4) qual tem maior impacto negativo na relação? (5) o que produto/operações deveria priorizar?

## PARTE P7 — CROSS-SELL E UPSELL
### Portfólio de produtos
| Código | Produto | Tipo |
|--------|---------|------|
| PR1 | Aluguel mensal leve (passeio, picape, caminhonete, fiorino/furgão leve — RAC) | Core |
| PR2 | Aluguel pesado (caminhão, cavalo mecânico, carreta — Pesados; NÃO inclui PR1) | Cross-sell |
| PR3 | Telemetria (~R$50/mês/veículo) | Upsell |
| PR4 | Proteção total / cobertura de avarias | Upsell |
| PR5 | Upgrade de categoria | Upsell |
| PR6 | Km adicional | Upsell |
| PR7 | Contrato anual | Upsell |
| PR8 | Veículos elétricos | Cross-sell/Upsell |
| PR9 | ZARP | Cross-sell |
| PR10 | Meoo | Cross-sell |
| PR11 | Venda de Seminovos | Cross-sell |
| PR12 | Gestão de frotas: contrato de longo prazo (36 meses) em que o cliente adquire o(s) veículo(s) podendo personalizar (plotagem, cor da frota) — literalmente uma frota própria, mas administrada pela Localiza. Diferente de PR7 (contrato anual, sem personalização, prazo mais curto). | Cross-sell |

Para CADA ligação: produtos mencionados, produtos ofertados ativamente, e janelas de oferta perdidas (cliente disse algo que se conecta a um produto e o vendedor não ofereceu). Exemplos de janela: multa em condutor errado → PR3; veículos próprios/quer personalizar frota/contrato longo → PR12; frota própria sem interesse em personalização → PR2/PR11; sinistro com franquia alta → PR4; renova mensalmente há 3+ meses (sem personalização) → PR7; perfil sustentável/redução de custo → PR8.

**Saída — Por ligação:**
```
cliente_id,data,duracao_s,produtos_mencionados,produtos_ofertados,janelas_identificadas,janelas_perdidas,o_que_deveria_ter_dito,impacto_estimado
```

**Saída — Por cliente (consolidado):**
```
cliente_id,executivo,produtos_ativos,produtos_com_potencial,produto_prioritario,receita_incremental_potencial,observacao
```

**Saída — Por produto (consolidado do lote):**
```
produto,codigo,vezes_mencionado,vezes_ofertado,janelas_identificadas,janelas_perdidas,taxa_aproveitamento_%
```

Depois, responda: (1) qual produto tem maior gap janela×oferta? (2) quais clientes têm maior potencial de expansão imediata? (3) algum produto nunca mencionado? (4) qual perfil de cliente mais compra cross-sell quando ofertado? (5) monte um "mapa de produto por situação": "Quando o cliente diz X → ofereça Y porque Z."

---

Formato de referência da resposta (ver exemplos já rodados em `resultados/exploracao_fable/outputs/batch02_resultado.md` e `outputs_novo_lote_363/lote01_resultado.md`): título com nome do lote, resumo (total de ligações, quantas por base, quantas "vazias"), tabelas de frequência P3 e P7, exemplos nominais citando "Cliente <cod>" quando relevante.
