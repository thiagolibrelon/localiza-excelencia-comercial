# Lote 03 (novo lote, 5.348) — Exploração P4+P8+P11+P13+P14+P15

## Resumo
- Total de ligações no lote: 38 (34 com conteúdo comercial; 4 sem conteúdo: URA/recado/correio de voz/número errado — Clientes 04927827, 21938846, 21764269, 24412774)
- Vendedores identificados neste lote: Juliana, Ana Paula (Oliva), Carlos, Fábio, Tatiana, Carla, Isadora, Andresa, Paulo, Flávia, Lucas, Flávio, Tatiane, Bruna, Ramiro, Fabrício, Stephanie, Ebert, Marisa, Thalita, Vitor, Cristina, Graziele, Paulo Faustino

## P4 — Health Score (por cliente, só os que têm sinal claro)
| Cliente | Volume | Adimplência | Fidelidade | Engajamento | Complex.Operacional | Potencial Upsell | Score Total (0-12) | Risco Churn |
|---|---|---|---|---|---|---|---|---|
| 15580210 | 2 | 2 | 2 | 2 | 1 | 2 | 11 | Baixo |
| 23765394 | 1 | 2 | 2 | 2 | 1 | 1 | 9 | Baixo |
| 27372575 | 1 | 1 | 1 | 2 | 1 | 2 | 8 | Baixo (novo, em teste) |
| 13404480 | 2 | 1 | 2 | 1 | 1 | 1 | 8 | Médio ("péssimo apoio da Localiza") |
| 19009834 | 1 | 2 | 1 | 2 | 1 | 0 | 7 | Médio ("tá ficando difícil pagar esse aluguel") |
| 20371206 | 1 | 1 | 2 | 2 | 1 | 0 | 7 | Médio (contestações de fatura recorrentes) |
| 27307774 | 1 | 1 | 0 | 2 | 1 | 2 | 7 | Baixo (novo; 11 utilitários próprios = upsell frota) |
| 23428588 | 1 | 1 | 1 | 2 | 1 | 0 | 6 | Alto (custo total 6,5 mil/mês, pediu redução e ouviu "não tem como") |
| 26670679 | 2 | 0 | 1 | 2 | 0 | 1 | 6 | Alto (CNPJ negativado no Serasa por boleto não entregue) |
| 08113560 | 1 | 1 | 0 | 1 | 1 | 1 | 5 | Médio (dual-sourcing declarado com Unidas) |

## P8 — Objeções (tabela de frequência)
| Tipo | Ocorrências | Resposta mais usada | Eficácia predominante | Melhor exemplo observado |
|---|---|---|---|---|
| OB3 Demanda baixa | 6 | R1 (validou, manteve cadastro/condição ativa e sondou frota própria) | Média (preserva relação, não converte) | Cliente 15574756 — vendedor validou a pausa, deixou tarifa especial cadastrada e sondou frota própria |
| OB1 Preço/valor | 5 | R2 (recalculou com dados do próprio cliente) | Mista: alta quando há margem/simulação; baixa quando "não tem exceção" | Cliente 19009834 — Ana Paula recalculou franquia e reajuste e recomendou NÃO migrar por estar "na vantagem" (aliado genuíno) |
| OB5 Problema não resolvido | 4 | R4 parcial + encaminhar canal (0800/e-mail de contestação) | Média-baixa (ônus fica com o cliente) | Cliente 20371206 — Bruna validou a contestação de KM, enviou fatura e pediu cópia no e-mail para acompanhar |
| OB2 Prazo/adiamento | 2 | R3 (urgência: "última unidade" / "margenzinha pra queimar" + follow-up agendado) | Média (ambas adiadas com callback marcado) | Cliente 27285931 — Vitor: "amanhã eu te ligo, você já recebeu as outras cotações e a gente negocia" |
| OB6 Burocracia/aprovação | 2 | R6 (explicou a política sem flexibilizar: só gestor cadastrado acessa boleto) | Baixa | Cliente 26670679 — gestor único embarcou para os EUA e ninguém mais consegue emitir boletos |

Desfechos gerais: nas OB1 o padrão foi "adiada" (cliente vai pensar/esperar reajuste); nenhuma objeção de preço foi claramente superada com fechamento, exceto a explicação PJ vs PF do Cliente 26306605 (reserva concluída na hora).

## P11 — Inteligência competitiva (tabela de frequência)
| Tipo | Ocorrências | Concorrentes citados | Vendedor explorou (SIM/NAO — contagem) |
|---|---|---|---|
| IC4 Frota própria revelada | 7 | — | SIM 6 / NAO 1 (Clientes 27307774, 05628910, 15580210, 19279800, 01303217, 07155344, 15574756) |
| IC6 Vendedor sondou concorrência/frota | 7 | — | SIM (pergunta de script: "vocês têm frota própria?" em quase toda prospecção) |
| IC5 Comparação implícita de preço | 3 | Unidas, "outras cotações" não nomeadas | SIM 1 / NAO 2 (Cliente 27285931: Vitor reagiu com follow-up; Clientes 08113560 e 27308105: não aprofundaram) |
| IC1 Menção direta a concorrente | 3 | Unidas (08113560), "a concorrência de vocês" (27308105), Hertz (27372575 — do próprio grupo) | NAO 2 / n.a. 1 — nenhum vendedor perguntou preço/condição do concorrente |
| IC7 Risco competitivo detectado | 2 | Unidas; cotações paralelas de assinatura | SIM 1 / NAO 1 |

Achado central: Cliente 08113560 declarou textualmente "a gente trabalha com a Localiza e com a Unidas, fecha onde está com o melhor valor" — a vendedora corrigiu a confusão de plataformas mas não fez nenhuma pergunta sobre a Unidas.

## P13 — Padrões emergentes (o que NENHUM prompt captura)
1. **S1 | Coaching de nota na pesquisa de satisfação** — Fabrício ligou exclusivamente para pedir que a cliente respondesse a pesquisa: "o gol é sempre dá 10 em tudo, já dando 9 já ajuda, porque esse mês eu vou te contar". Frequência: 1 explícita (+ pedidos de avaliação ao fim de ~10 ligações). Impacto: **alto** — NPS/CSAT da operação está contaminado. Evidência: Cliente 16824498.
2. **S3 | Boleto não chega ao cliente** — a Localiza não envia boleto por e-mail (política de segurança) e o cliente só descobre com atraso, juros ou Serasa. Frequência: 4/38 (Clientes 26670679, 26716683, 20371206, 10891848). Impacto: **alto** — gera inadimplência artificial, negativação e desgaste; é o assunto mais recorrente de atrito do lote.
3. **S3 | Login/biometria/e-mail desatualizado como gargalo de receita** — sessões inteiras de suporte para criar senha e reserva por telefone; um cliente ficou ~5 anos sem conseguir usar o cadastro por e-mail desatualizado. Frequência: 5/38 (Clientes 26306605, 11615931, 25977335, 25545687, 27372575). Impacto: **alto** (custo de atendimento + demanda represada).
4. **S4 | Reajuste tarifário recente como gatilho de dor transversal** — o reajuste de tabela aparece como causa de objeção em 4 ligações; vendedores relatam internamente "não está tendo exceção, nem com volume de 8 carros deram desconto". Frequência: 4/38 (Clientes 19009834, 23428588, 13404480, 26306605). Impacto: **alto** — pressão de churn na base mensal PME.
5. **S3 | Fricção agência × executivo × 0800** — agência não acessa contrato ativo, executivo não tem autonomia sobre boleto/tarifa/troca de carro; cliente é rebatido entre canais. Frequência: 4/38 (Clientes 10891848, 23765394, 23428588, 26670679). Impacto: **médio-alto**.
6. **S2 | PJ pequena se comporta como PF** — dono/cônjuge é o gestor, compara tarifa PJ×PF, histórico de locação como pessoa física antecede o CNPJ. Frequência: 3-4/38 (Clientes 25545687, 26306605, 27372575). Impacto: **médio** — argumento "PJ é sempre mais barato" converte bem nesse perfil.

## P14 — Diferenças entre vendedores
- **Ana Paula (Oliva)**: a mais consultiva do lote — faz o cálculo de franquia na frente do cliente e recomenda NÃO mudar o contrato quando o cliente está "na vantagem", mesmo perdendo a migração; avisa proativamente do reajuste de 3,7% (Cliente 19009834).
- **Fábio**: gestão de expectativa exemplar — explica que não garante modelo específico, admite os limites da própria autonomia e ainda instrui o cliente a "jogar a responsabilidade para cima de mim" na agência (Cliente 23765394). Constrói relacionamento sem prometer o que não controla.
- **Stephanie**: honesta, mas repete "não tem como" ~10 vezes sem oferecer nenhuma alternativa intermediária (downgrade de categoria, revisão futura, escalação formal) a um cliente que pediu explicitamente ajuda para reduzir custo (Cliente 23428588) — objeção de preço morre sem plano B.
- **Isadora**: hand-holding operacional extremo — cria senha, navega o WebCorp junto e conclui a reserva dentro da própria ligação (Cliente 26306605); resolve cobrança confusa enviando demonstrativo na hora (Cliente 10891848). Converte suporte em fechamento.
- **Bruna**: ágil no WhatsApp (fatura, multa, link de senha na mesma chamada — Clientes 26716683, 25599928), mas na contestação de KM transfere 100% do ônus ao cliente ("eu preciso que você mesmo faça") em vez de abrir o chamado (Cliente 20371206).
- **Fabrício**: informal e persistente em conseguir contatos alternativos (Cliente 08320022), porém usa o relacionamento para inflar a pesquisa de satisfação (Cliente 16824498) — risco de integridade.
- **Cristina**: a mais completa em cross-sell — na mesma ligação simula plano 12 meses no WebCorp, aciona cotação do Localiza Meu (zero km) e resolve troca de condutor com carta de autorização (Cliente 15580210, 1.115s).
- **Paulo Faustino**: melhor onboarding do lote — melhora a tarifa proativamente antes do primeiro acesso, envia vídeo passo a passo e explica a lógica 30/31 dias do mensal (Cliente 27372575).
- **Carlos/Carla (prospecção fria)**: script idêntico e disciplinado — apresentação + "condições especiais" + sondagem de frota própria + WhatsApp (Clientes 15574756, 15600678); eficiente, mas raso quando o cliente diz que não tem demanda.

## P15 — Eventos raros de alto impacto
| Cliente | Categoria | Evento | Impacto potencial | Ação recomendada |
|---|---|---|---|---|
| 25599928 | R4 Influência | Cliente indicou espontaneamente empresa de amigos para cadastro e passou o contato do decisor | Alto (lead quente por indicação) | Contato em 24h + reconhecer a indicação ao cliente indicador |
| 26670679 | R2 Churn | CNPJ (escritório de advocacia, 4 carros assinatura + rack) negativado no Serasa por boletos nunca entregues; "nosso CNPJ não pode estar no Serasa de maneira alguma" | Alto | Task-force: baixar Serasa, estornar ~R$900 de juros, cadastrar 2º gestor imediatamente |
| 23428588 | R2 Churn | Cliente paga ~R$6,5 mil/mês (aluguel + parcelas de avaria), pediu redução formal e encerrou com "vou pensar" após ouvir que não há exceção | Alto | Oferta de retenção estruturada antes da devolução do carro |
| 08113560 | R3 Intel. competitiva | Associação confirma operar simultaneamente com Unidas, decidindo por preço a cada locação | Médio-alto | Proposta de tarifa acordo/volume para recapturar share |
| 27372575 | R1 Expansão | Novo CNPJ em "teste" com 1 HB20 mensal: "se funcionar bem, a gente avança um pouco mais"; decisor aluga constantemente Hertz nos EUA | Médio-alto | Acompanhamento próximo dos primeiros 60 dias do piloto |
| 05628910 | R1 Expansão | Indústria metal-mecânica com caminhões pesados aceitou receber executivo de Pesados da Localiza | Médio | Garantir handoff efetivo ao time de pesados |
| 16807108 | R5 Mudança estrutural | Troca de responsável no cliente (funcionária nova na 1ª semana substituindo a gestora) + executiva da conta saindo de férias no mesmo dia | Médio | Recadastrar gestores e formalizar transição antes das férias |

## Observações livres
O lote é dominado por atendimento reativo/onboarding e não por venda: a maior alavanca de receita visível não é objeção mal tratada, e sim fricção operacional (boleto invisível, login travado, gestor único) que consome as ligações longas e gera os dois maiores riscos de churn. O pedido de avaliação ao final da chamada é quase universal, o que — combinado ao caso explícito de coaching de nota do Fabrício — sugere que a métrica de satisfação dessa operação deve ser lida com desconto.
