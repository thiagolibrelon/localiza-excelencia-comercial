# Lote 01 (novo lote, 5.348) — Exploração P4+P8+P11+P13+P14+P15

## Resumo
- Total de ligações no lote: 38 (2 caíram em secretária eletrônica/recado sem conversa: Cliente 08662157, Cliente 24117417; 1 morreu em espera de URA: Cliente 01056255)
- Vendedores identificados neste lote: Paulo (gerente conta PR), Fábio (2 ligações), Matheus (2), Francisco, Victor, Isadora Maciel, Carla Cunha, Carla, Fabrício, Rosane, Rosana, Pedro Fonseca, Vitor, Andresa (2), Rosiane/Rosilene, Bruna (2), Camila Andrade, Amanda Silva, Brenda, Ângela, Liliane, Aline, Lucas (2), Cristina, Ana, Tainara, Tamires Duarte, Thalita, Ramiro, Cristiane + 1 vendedor não nomeado ("meu jovem", Cliente 24762223)

## P4 — Health Score (por cliente, só os que têm sinal claro)
| Cliente | Volume | Adimplência | Fidelidade | Engajamento | Complex.Operacional | Potencial Upsell | Score Total (0-12) | Risco Churn |
|---|---|---|---|---|---|---|---|---|
| 05897867 | 2 (31 carros assinatura) | 1 | 2 | 1 | 1 (frota própria + provisórios) | 2 (RAC esporádico confirmado) | 9 | Baixo |
| 26382175 | 1 (múltiplos carros: Toro+Onix) | 0 (faturas vencidas, multas, prorrogações) | 2 | 2 | 0 | 2 (2ª empresa Inovare + assinatura) | 7 | Médio (crédito, não relacional) |
| 18561902 | 1 (equipe topografia, +1 carro em rua) | 1 | 2 | 2 | 0 (assalto, itens faltantes, cobrança vindo) | 1 | 7 | Baixo |
| 25203214 | 1 | 1 | 1 | 2 | 1 (erro grave de portal) | 1 | 7 | Baixo (confiança no portal abalada) |
| 07448263 | 1 (carro GF ativo) | 1 | 2 | 1 | 1 | 2 (filial Fortaleza, viagem mensal, alvo cashback) | 8 | Baixo |
| 27023339 | 1 | 1 | 2 | 2 | 1 | 2 (carro adicional p/ Minas) | 9 | Baixo |
| 05633986 | 1 | 1 | 1 | 2 (quer 2 carros esta semana) | 0 (login/biometria travando) | 2 | 7 | Médio (fricção de onboarding) |
| 25545847 | 0 | 1 | 0 | 1 | 1 | 1 | 4 | Alto (acha PJ mais caro que PF, abriu cadastro alternativo) |
| 24810537 | 0 (nunca locou) | 1 | 0 (locou na concorrente) | 1 | 1 | 0 | 3 | Alto |
| 24762223 | 0 | 1 | 0 (comprou carro próprio) | 0 | 1 | 1 | 3 | Alto |
| 26356711 / 27214586 / 23460552 | 0-1 | 1 | 1 | 1 | 1 | 1 | 5-6 | Médio (contas dormentes, contato de manutenção) |

## P8 — Objeções (tabela de frequência)
| Tipo | Ocorrências | Resposta mais usada | Eficácia predominante | Melhor exemplo observado |
|---|---|---|---|---|
| OB3 Demanda baixa | 7 (24810537, 24762223, 27214586, 26356711, 23460552, 10216722, 27337310) | R5 leve (aceita + deixa WhatsApp/cadastro ativo) | Baixa/média — quase nunca explora causa raiz | Bruna (24810537): única que investigou a causa antes de aceitar ("contrato fechado? frota própria?") |
| OB1 Preço/valor | 3 (25545847 PF vs PJ; 24762223 preço da diária; 27299074 proteção ampliada +R$60) | R6 (argumentou sem usar o dado do cliente) | Média | Camila (25545847) explicou pacote total avarias vs adicionais PF e converteu em cotação futura — desfecho adiado |
| OB2 Prazo/adiamento | 4 (27005116, 23460552, 06938442, 01671793) | R4 (agenda + WhatsApp) | Média | Amanda (27005116): agendou recontato via WhatsApp para o dia seguinte no horário do cliente |
| OB5 Problema não resolvido | 2 (22027180 multa fixo→flexível; 05633986 login que nunca funcionava) | R1 (validou + escalou) | Média | Lucas (22027180): não capitulou nem prometeu estorno — levou à diretoria com prazo ("amanhã cedinho te ligo") |
| OB6 Burocracia/aprovação | 2 (27334172 procuração/cadastro; 05633986 biometria repetida) | R1 | Média | Pedro Fonseca (27334172) destravou o fluxo procurador vs gestora de reservas passo a passo |

Desfechos: nenhuma objeção "perdida" em definitivo na ligação, mas OB3/OB1 quase sempre terminam "adiadas" — o padrão da carteira é semear contato, não fechar.

## P11 — Inteligência competitiva (tabela de frequência)
| Tipo | Ocorrências | Concorrentes citados | Vendedor explorou (SIM/NAO — contagem) |
|---|---|---|---|
| IC1 Menção direta a concorrente | 1 (24810537) | Movida ("Movisa" no STT) | SIM (1) — perguntou formato do contrato e se foi pontual |
| IC4 Frota própria / carro comprado revelado | 2 (24762223 comprou carro; 05897867 frota própria p/ blindados) | — | NAO (24762223: só deu preço e encerrou); SIM (05897867: posicionou provisórios) |
| IC5 Comparação implícita de preço | 1 (25545847) | Locação PF da própria Localiza + "Local Max" | PARCIAL — argumentou pacote, não pediu a simulação do cliente |
| IC6 Vendedor sondou concorrência | 2 (24810537 Bruna; 24810537 idem frota própria) | — | SIM (2) |
| IC7 Risco competitivo detectado | 3 (24810537 Movida atendeu bem; 25545847 percepção PJ caro; 24762223 compra resolve a demanda) | Movida | Explorado em 1 de 3 |
| Canal alternativo (não categorizado) | 1 (11046953) | Agência de viagem "multicidade" intermedia as locações | NAO explorado nesta ligação |

## P13 — Padrões emergentes (o que NENHUM prompt captura)
1. **S3 | Fricção de plataforma/acesso como assunto dominante** — 8 de 38 ligações (~21%) giram em torno de falha técnica: prorrogação que virou contrato até 2031 (Cliente 25203214), tag de pagamento não liberada na retirada digital (17136083), login multi-CNPJ errado (27100891), senha/biometria que nunca ativa (05633986), conta bloqueada 30 min (27054532), WebCorp travada no CPF (22131549), itens extras cobrados sem querer na reserva (27299074), portal de fatura bloqueado por extensão do Chrome (25148800). Frequência: alta. Impacto: **alto** — consome horas dos executivos e mina confiança ("agora eu não confio mais no portal", Cliente 25203214).
2. **S4 | Turnover de gestor/contato no cliente** — 5 ocorrências: contato saiu da empresa (10689718), sócio que geria a conta saiu (25321109), gestora fora do país com substituto (01056255), gestor real é outro (26356711), operadora nova no cargo errando modalidade de contrato (22027180). Frequência: média-alta. Impacto: **alto** — cadastros desatualizados = relacionamento e receita órfãos.
3. **S1 | Executivos viram "concierge manual" do self-service** — dão WhatsApp pessoal e assumem operações que o portal deveria fazer: prorrogação manual (Paulo, 25203214), alterar proteção "por dentro" (Vitor, 27299074), refazer reserva junto (Isadora, 27100891). Frequência: alta. Impacto: **médio** — retém cliente no curto prazo, mas cria dependência e não escala.
4. **S1 | Pedido explícito de nota na pesquisa pós-ligação** — pelo menos 6 vendedores (Fábio, Rosana, Camila, Thalita, Lucas/26356711, Fabrício) encerram pedindo para o cliente aguardar/responder a avaliação. Frequência: alta. Impacto: **médio** — NPS/CSAT provavelmente inflado por survey-begging.
5. **S4 | Campanha cashback R$1.000 GF→RAC mal dominada** — Aline (07448263) oferece cashback maior que o valor do aluguel e não sabe responder se é recorrente; cliente reage com ceticismo ("você está me dando desconto maior do que o que eu pago?"). Frequência: 1 no lote, mas é campanha vigente. Impacto: **alto** — risco de promessa mal calibrada e custo de incentivo mal explicado.
6. **S2 | Cliente PJ pequeno percebe CNPJ sem vantagem de preço** — Cliente 25545847 simulou PF mais barato que PJ e migrou o comportamento. Frequência: 1 explícita, provável cauda. Impacto: **médio** — ataca a proposta de valor central do canal Empresas.

## P14 — Diferenças entre vendedores
- **Paulo** (Cliente 25203214): diagnóstico forense ao vivo ("espelho da reserva é a caixa preta"), assume responsabilidade pessoal ("estou te dando minha palavra") e oferece operar prorrogações manualmente. Melhor gestão de crise do lote; risco de criar dependência.
- **Fábio** (Clientes 25148800, 18561902): o mais didático (explica ciclo de faturamento diário vs mensal para o cliente nunca mais depender de e-mail) e o de maior rapport — 24 min de conversa pessoal com a Cliente 18561902, incluindo compartilhar a própria quimioterapia. D3 extremo; ligações muito longas.
- **Matheus** (Clientes 17136083, 27337310): resolutivo com prazo curto e explícito ("2-3 minutinhos e te retorno"); no onboarding educa regras práticas (reservar com 4 dias de antecedência, mensal mais barato que diária). Bom equilíbrio D1/D4.
- **Bruna** (Clientes 24810537, 26108270): curta e objetiva; única que sondou concorrência de forma estruturada (formato de contrato, frota própria) e fecha pós-venda com pergunta de satisfação. Referência em D4/IC6.
- **Isadora** (Cliente 27100891): conduz o cliente passo a passo por fluxo burocrático multi-CNPJ (termo web, encaminhamento de e-mail) sem perder o cliente; ainda achou economia para ele (encerrar mensal no CNPJ errado sem multa). D1 forte.
- **Lucas** (Clientes 22027180, 26356711): em objeção de estorno não capitula nem promete — valida, cita cláusula e escala à diretoria com prazo. D5 correto.
- **Aline** (Cliente 07448263): oferta de campanha sem dominar as regras (recorrência do cashback), gerando ceticismo; compensa com follow-up prometido. D5 frágil.
- **Camila Andrade** (Cliente 25545847): diante de objeção de preço com dado concreto do cliente (simulação PF mais barata), respondeu com argumento genérico de pacote em vez de pedir a simulação — R6. D5 a desenvolver.
- **Vendedor não nomeado** (Cliente 24762223): tom informal ("meu jovem"), cliente revelou compra de carro próprio e ele apenas cotou preço e encerrou — zero exploração do evento competitivo. Pior D5 do lote.
- **Cristina** (Cliente 22131549): proatividade rara — ligou de volta ao detectar que a instabilidade da WebCorp afetava mais clientes e transferiu com contexto para a central. D1/D3 bons.

## P15 — Eventos raros de alto impacto
| Cliente | Categoria | Evento | Impacto potencial | Ação recomendada |
|---|---|---|---|---|
| 24810537 | R2/R3 | Cadastrou na Localiza mas fez a locação (pontual) com a Movida e "já deu certo" | Alto | Recontato com oferta agressiva na próxima demanda pontual; entender o que a Movida ofereceu (preço? agilidade?) |
| 24762223 | R3 | Cliente comprou carro próprio e encerrou a demanda de locação | Médio | Nutrir com TCO carro próprio vs mensal/assinatura; timing: revisão em 6-12 meses |
| 26382175 | R1 + risco crédito | Vai cadastrar 2ª empresa (Inovare) e contratar carro por assinatura — porém com faturas vencidas e multas na conta atual | Alto | Acelerar cadastro da nova empresa condicionado à regularização; acompanhar de perto o limite de crédito |
| 25321109 | R5 | Mudança societária: sócio que geria a conta (Wesley) saiu; sócia assumindo os acessos | Médio | Concluir troca de gestor e revalidar demanda — janela de re-engajamento |
| 18561902 | Risco de insatisfação | Veículo alugado assaltado (step, macaco e equipamentos levados); cobrança dos itens será faturada e proteção não cobre furto de itens | Alto | Avisar valor antes da fatura; orientar reposição com itens originais (vendedor já alertou risco de multa por item obrigatório) |
| 07448263 | R3 (inteligência interna) | Campanha cashback R$1.000 + upgrade Platinum para ativar clientes GF no RAC — regras de recorrência desconhecidas pelo próprio time | Médio | Briefing formal da campanha para o time comercial antes que promessas divirjam |
| 26382175 | R5 (interno) | Executiva Rosane transferida de Porto Alegre para Florianópolis — carteira RS trocará de atendente | Médio | Transição assistida (ela mesma propôs treinar a substituta) para não perder o vínculo com clientes de alto toque |
| 05897867 | R1 (conta-chave) | 31 carros por assinatura + demanda recorrente de provisórios (frota blindada própria) | Médio | Formalizar fluxo de provisórios/pane (bateria via 0800) como argumento de retenção da conta |

## Observações livres
O lote é dominado por ligações de manutenção/suporte (não de venda): o tempo dos executivos vai majoritariamente para consertar fricções de portal/login e atualizar contatos desatualizados — o que sugere que ganhos de UX na WebCorp liberariam capacidade comercial real. STT muito fragmentado em 4-5 ligações (eco do próprio vendedor transcrito como cliente), mas sem comprometer a leitura das demais; nenhuma ligação com sentimento negativo explícito no lote, embora 3 contas mostrem churn já consumado ou iminente (24810537, 24762223, 25545847).
