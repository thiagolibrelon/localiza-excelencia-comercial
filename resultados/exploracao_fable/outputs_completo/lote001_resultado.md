# Lote 001 — Exploração P3+P7

## Resumo do lote
- Total de ligações no lote: 38 — todas da BASE_ANTIGA_1275
- Clientes únicos: 33 (Cliente 00714731 com 2 ligações, Cliente 00844996 com 3, Cliente 01185565 com 3)
- Ligações "vazias" para classificação: 7 — Cliente 00307930 (contato ausente, retornará), Cliente 00409189 (3 contatos ausentes/de férias), Cliente 00639774 (só coletou WhatsApp do contato), Cliente 00714731 ×2 (cliente dirigindo/ocupada; segunda ligação foi rediscagem indevida do próprio sistema no mesmo dia), Cliente 01076493 (caiu em secretária eletrônica), Cliente 00844996 de 02/06-51s (recado com recepcionista)
- Base analisada: 31 ligações com conteúdo; 19 delas contêm pelo menos um problema classificável (25 ocorrências de problema no total)
- Perfil do lote: fortemente dominado por suporte de acesso/portal (WebCorp, senha, biometria, cadastros) e por manutenção proativa de carteira; poucas ligações de venda "pura"

## P3 — Problemas recorrentes

### Parte 1 — Por ligação (só as 19 com problema)
```
cliente_id,data,problemas_identificados,quem_relatou,foi_resolvido_na_ligacao,escalou_para,observacao
00033938,2026-06-03,P9,cliente,PARCIAL,0800,terceiro bateu na Montana parada; proteção básica = franquia 12k/18k; orientado BO + assinatura de sinistro na agência + 0800 para terceiro pagar; substituição do veículo orientada
00044031,2026-06-01,P1,cliente,SIM,nao_escalou,"senha inválida" porque cliente usava login antigo da empresa anterior (Vaini); reset + biometria conduzidos ao vivo
00104800,2026-06-01,P10,cliente,NAO,0800,tag inclusa no contrato saiu bloqueada da agência; diretor pagou pedágio do próprio bolso; reembolso só via ASCLI
00221703,2026-06-03,P1,cliente,PARCIAL,IT,faturamento eletrônico multi-CNPJ só exibe o código errado (Interange) e esconde as faturas da Leder; formalizado por e-mail ao time responsável com cliente em cópia
00310434,2026-06-03,P1+P5,cliente,PARCIAL,nao_escalou,cadastro WebCorp preso na ex-funcionária; CPF da nova gestora ainda vinculado a empresa anterior (FCC); desvinculação formalizada por e-mail com ok da cliente
00575098,2026-06-02,P10,cliente,SIM,nao_escalou,sistema de reserva não oferecia horário compatível com chegada do voo (11h55); vendedora ensinou a digitar 23h59 (agência 24h)
00584308,2026-06-02,P2,cliente,SIM,nao_escalou,renegociação de fatura concluída com sucesso pelo canal que o vendedor tinha indicado em contato anterior
00608392,2026-06-02,P11,vendedor_detectou,PARCIAL,IT,cadastro de CNPJ de filial devolvido pelo chamado interno pedindo nova validação + documentação; diretora (validadora) ausente até quinta
00839850,2026-06-01,P10,vendedor_detectou,SIM,nao_escalou,datas da reserva divergentes no sistema (28/05-12/06 vs 1 semana real); vendedor garantiu acerto na devolução
00844996,2026-06-01,P1+P5,vendedor_detectou,PARCIAL,nao_escalou,acessos WebCorp órfãos (gestora Eliana saiu); representante legal sem CPF cadastrado; sem acesso ninguém libera novos usuários
00844996,2026-06-02,P1+P5,cliente,PARCIAL,nao_escalou,follow-up: acesso segue travado (gestor sem tempo de aprovar); vendedora propõe cadastro direto por e-mail
00849954,2026-06-03,P1,cliente,SIM,nao_escalou,senha expirada + link expirado; reset com QR code e biometria conduzido ao vivo durante a reserva
00867099,2026-06-02,P1,cliente,SIM,nao_escalou,erro no fim do fluxo de troca de senha; resolvido com link via WhatsApp + biometria + login numérico correto
00913571,2026-06-03,P10+P11,cliente,PARCIAL,nao_escalou,desconto negociado ainda não refletia no sistema (esperar ~30min para reservar); aumento de limite de crédito de 15 mil pedido na ligação anterior segue pendente
00917456,2026-06-03,P1+P5,cliente,PARCIAL,nao_escalou,login master (Alexandre) não aprova os acessos solicitados e trava recebimento de faturas; vendedor assume inclusão manual por e-mail
00951813,2026-06-05,P1,cliente,SIM,nao_escalou,erro "não existe aprovador cadastrado na área solicitante" ao criar usuários; contornado ao vivo reordenando cadastro (aprovador antes de solicitante)
01010282,2026-06-01,P11,vendedor_detectou,PARCIAL,nao_escalou,cadastro de 2 CNPJs parado em análise de crédito: termo SCR digital para sócio + documentação financeira; redirecionado à Marília (financeiro do cliente)
01130882,2026-06-01,P11,cliente,SIM,nao_escalou,dúvida de renovação já resolvida pelo 0800 antes do retorno; vendedora cita instabilidade de internet/portais na matriz naquele dia
01155964,2026-06-02,P5+P2,vendedor_detectou,PARCIAL,nao_escalou,gestor que acompanhava faturas de multa/indenização saiu da empresa; faturas indo ao portal sem ninguém olhar — risco de protesto; obteve contato do financeiro (Soraya) e vai formalizar
01185565,2026-06-02,P11+P5,cliente,PARCIAL,nao_escalou,filial sem cadastro exige validação facial de sócio/procurador ("os diretores é complicado"); gestora antiga de locações saiu do quadro
```

### Parte 2 — Consolidado do lote
```
codigo,categoria,total_ocorrencias,clientes_afetados,resolvido_na_ligacao_%,escala_%
P1,Acesso/sistema,9,8,44% SIM / 56% PARCIAL,11% (1 IT)
P2,Faturamento/cobranca,2,2,50% SIM / 50% PARCIAL,0%
P5,Condutor/cadastro,6,5,0% SIM / 100% PARCIAL,0%
P9,Sinistro,1,1,0% SIM / 100% PARCIAL,100% (0800)
P10,Reserva/sistema,4,4,50% SIM / 25% PARCIAL / 25% NAO,25% (0800)
P11,Outro (cadastro de CNPJ/credito/burocracia),5,5,20% SIM / 80% PARCIAL,20% (chamado interno)
P12,Manipulacao de pesquisa/NPS,0,0,-,-
```
Leitura direcional: P1 + P5 + P10 (acesso, cadastro órfão e falhas de portal/reserva) somam 19 das 25 ocorrências — três em cada quatro problemas do lote nascem da plataforma ou da gestão de acessos, não da operação de locação em si. O subtipo mais repetido dentro de P1/P5 é "gestor que saiu da empresa deixou o acesso preso" (Clientes 00310434, 00844996, 00917456*, 01155964, 01185565 — *trava de aprovação interna). Nenhum P12 estrito, mas duas vendedoras (Clientes 00310434 e 00951813) pedem explicitamente que a cliente fique na linha para responder a pesquisa de atendimento — survey-begging leve, sem ditar nota.

### P3 — Exemplos
- **Cliente 00033938** (P9): terceiro bateu na Montana parada em posto. A vendedora Flávia fez o playbook completo ao vivo: BO → condutor assina sinistro na agência em 24h → e-mail à assistência ao cliente → 0800 para direcionar cobrança ao terceiro culpado; explicou franquia da proteção básica (12 mil parcial / 18 mil total) e ensinou a pedir substituição sem encerrar o contrato mensal ("eu não quero devolver, quero substituir"). Auditou a proteção dos 7 carros da frota, um por um.
- **Cliente 00104800** (P10): tag de pedágio inclusa no contrato saiu bloqueada da agência e o diretor pagou pedágio do bolso. A vendedora diagnosticou a causa provável (balcão não ativou a tag) mas não conseguiu tratar o reembolso: "precisa ver com eles mesmo... eu não tenho acesso a essa informação" — cliente sai com duas tarefas (ligar no 0800 e brigar pelo recibo).
- **Cliente 01155964** (P5+P2): o gestor que acompanhava multas saiu e ninguém assumiu — "a RDR fica lá devendo, devendo a Localiza, vai protestar vocês". A vendedora Andresa explicou a mecânica (locação fatura na agência de viagem, multa/indenização cai no portal órfão) para um funcionário de suprimentos até conseguir o contato do financeiro. Melhor prevenção de inadimplência do lote.
- **Cliente 00951813** (P1): durante onboarding de fluxo de aprovação, o WebCorp rejeitou o cadastro ("não existe aprovador cadastrado na área solicitante"). A vendedora Rosana depurou o erro ao vivo por tentativa e erro — inverteu a ordem (cadastrar aprovador antes do solicitante) e concluiu — mas a UX exigiu 30 minutos de ligação para algo que deveria ser autoexplicativo.
- **Cliente 00844996** (P1+P5): empresa cliente de frota ficou sem nenhum acesso válido ao WebCorp porque a única gestora cadastrada saiu; o representante legal nem CPF cadastrado tinha. A vendedora Keila alertou o padrão: "tem empresa que às vezes só o dono tem acesso... precisa outra pessoa ter acesso".

### P3 — Respostas
1. **Quais problemas são sistêmicos?** (a) Gestão de acessos atrelada a pessoa física: quando o gestor cadastrado sai da empresa, o acesso da conta inteira morre e o CPF fica vinculado ao CNPJ antigo (00310434, 00844996, 01155964, 01185565) — é o problema mais repetido do lote; (b) fricção de senha/biometria do WebCorp: 5 resets conduzidos por telefone em uma semana (00044031, 00849954, 00867099, mais os fluxos de 00951813 e 00221703); (c) visão multi-CNPJ quebrada no faturamento eletrônico (00221703); (d) tag de pedágio que sai bloqueada da agência mesmo inclusa em contrato (00104800); (e) burocracia de cadastro de CNPJ/filial com validação facial de sócio, que trava expansão de contas que querem comprar mais (00608392, 01010282, 01185565).
2. **Quais o vendedor resolve sem escalar, e como?** Todo o bloco de senha/acesso: reset guiado passo a passo com link por WhatsApp, biometria e login numérico correto (00044031, 00849954, 00867099, 00951813 — 4 SIM). Também resolvem contornos de sistema por conhecimento tácito: digitar 23h59 para agência 24h (00575098), garantir acerto de cobrança na devolução (00839850) e assumir inclusões manuais de cadastro por e-mail (00917456, 00310434). O padrão é o executivo operar como suporte N1 do portal.
3. **Quais escala desnecessariamente?** Quase nada — a taxa de escala do lote é baixa (4 de 25). O caso discutível é o inverso: 00104800 (tag/reembolso) foi mandado para o 0800 quando o executivo poderia ao menos abrir o chamado de reembolso em nome do cliente; o cliente lesado ficou com o ônus do processo.
4. **Qual tem maior impacto negativo na relação?** O acesso órfão pós-turnover (P5): ele bloqueia reserva, fatura e multa ao mesmo tempo, gera risco financeiro real (protesto no caso 01155964) e faz o cliente "sumir" do portal sem que ninguém perceba. Em segundo lugar, a tag bloqueada (00104800): dinheiro do bolso do diretor do cliente + processo de reembolso incerto é o tipo de atrito que vira história ruim internamente.
5. **O que produto/operações deveria priorizar?** (1) Fluxo self-service de transferência de gestor/desvinculação de CPF entre CNPJs — hoje exige e-mail formal do executivo e ok manual; (2) alerta automático de "conta sem gestor ativo" para o executivo quando o único login para de ser usado; (3) revisão do fluxo senha/biometria do WebCorp (link que expira, erro genérico "senha inválida" quando o problema é o login); (4) verificação de ativação da tag no checkout da agência; (5) mensagens de erro acionáveis no cadastro de perfis (caso 00951813).

## P7 — Cross-sell e Upsell

### Por ligação (só as 14 com sinal comercial relevante)
```
cliente_id,data,duracao_s,produtos_mencionados,produtos_ofertados,janelas_identificadas,janelas_perdidas,o_que_deveria_ter_dito,impacto_estimado
00033938,2026-06-03,546,PR1+PR4,PR4,sinistro com franquia alta em frota de 7 mensais,-,"(bem executado) 'da próxima, contrate a total de avarias' + auditou carro a carro",alto — upsell PR4 em ate 2 carros da frota
00041270,2026-06-02,124,PR1,-,cliente declara operar 100% com frota própria (máquinas/implementos),PR12+PR11+PR2,"como vocês gerenciam custo e revenda dessa frota própria? posso simular terceirização (GF) e temos seminovos/pesados",médio — conta hoje inativa
00128792,2026-06-01,141,PR1,PR1(mensal),loca 12 diárias via agência de viagem,-,(sondagem de mensal feita; cliente já usa) —,baixo
00256658,2026-06-05,111,PR1,PR1,demanda esporádica; feriados no mês,-,(orientou reserva antecipada em feriado) —,baixo
00584308,2026-06-02,100,PR1+PR2?,PR1,planejamento do 2º semestre sai mês que vem; devolveu 1 de 3 carros,PR7(futura),"quando fechar o planejamento, te apresento tarifa de contrato anual para a frota recorrente",médio — followup agendado
00839850,2026-06-01,109,PR1,PR1(conversão p/ mensal),contrato de 15 dias custava o mesmo que 1 mês,-,(ofereceu conversão diária→mensal por iniciativa própria) —,médio
00844996,2026-06-01/02,1524,PR1+PR4+PR6+PR7+PR12,PR1+PR4+PR7,cotação 6 meses Cuiabá; km livre desejado; FlyTour intermedia,-,"(cotou fixo vs flexível, 6 vs 12 meses, com e sem total avarias) —",alto — contrato de 6 meses em fechamento
00849954,2026-06-03,743,PR1+PR4+PR6+PR12,PR1(flexível)+PR4,provisório de 90 dias antes de pedido definitivo na frota GF,-,"(guiou mensal flexível + total avarias inclusa + tag + acordo diário atualizado) —",alto — ponte RAC→GF exemplar
00862150,2026-06-03,218,PR1+PR12,PR1(campanha GF),cliente GF com demanda esporádica RAC; ação cashback ate R$1000 na fatura GF,-,(ofereceu campanha e encaminhou à decisora Sandra) —,médio
00913571,2026-06-03,180,PR1+PR4,PR1,projeto usando mais carros; pediu aumento de limite p/ 15 mil+,PR7,"esse projeto tem prazo? com volume crescente consigo tarifa de contrato anual e limite maior",médio-alto — expansão orgânica em curso
00951813,2026-06-05,1791,PR1+PR4,PR4(padronização),onboarding de fluxo de aprovação; interesse em governança; 'neutraliza' explicado,PR8(leve)+PR3(leve),"para governança de frota em uso intenso, telemetria dá visibilidade de condutor; e temos elétricos p/ agenda ESG",médio
01070937,2026-06-05,102,PR1+PR12,PR1(campanha GF),cliente GF sem demanda RAC declarada,-,(ofereceu campanha GF↔RAC mesmo com recusa) —,baixo
01155964,2026-06-02,336,PR1+PR3(implícito),-,multas/indenizações sem gestão após saída do gestor,PR3+PR12,"além de regularizar o contato, nossa telemetria/gestão de frotas centraliza infrações e evita esse tipo de buraco",médio
01185565,2026-06-02/05,1026,PR1+PR4+PR6,PR1+PR4(ampliada),3 veículos novos + filial nova sendo cadastrada; reajuste de preço iminente,-,"(reserva assistida; cliente aceitou cobertura ampliada a terceiros +R$178,50/mês) —",alto — conta em expansão ativa
```

### Consolidado por produto
```
produto,codigo,vezes_mencionado,vezes_ofertado,janelas_identificadas,janelas_perdidas,taxa_aproveitamento_%
Aluguel mensal leve (core),PR1,~28,9,9,0,100%
Aluguel pesado,PR2,0,0,1,1,0%
Telemetria,PR3,0,0,2,2,0%
Proteção total/ampliada,PR4,7,5,5,0,100%
Upgrade de categoria,PR5,0,0,0,0,-
Km adicional/franquia flexível,PR6,4,2,2,0,100%
Contrato anual,PR7,2,1,3,2,33%
Veículos elétricos,PR8,0,0,1,1,0%
ZARP,PR9,0,0,0,0,-
Meoo,PR10,0,0,0,0,-
Venda de Seminovos,PR11,0,0,1,1,0%
Gestão de frotas,PR12,6,1,3,2,33%
```

### P7 — Exemplos
- **Oferta ativa bem feita — Cliente 00849954 (Geraldo)**: cliente GF precisava de provisório de 90 dias para engenheiro em experiência antes de pedir carro definitivo na frota. Geraldo resolveu a senha expirada, recomendou o mensal flexível pelo motivo certo ("devolve quando precisar, altera a franquia de km"), manteve a total de avarias inclusa ("só alugo com ela"), liberou a tag de pedágio e ainda atualizou o acordo para diárias futuras. Reserva concluída e validada dentro da ligação.
- **Oferta ativa consultiva — Cliente 00844996 (Keila)**: cotação de 6 meses em Cuiabá conduzida como consultoria: fixo vs flexível, 5.000 km, com/sem total de avarias, comparação com contrato de 12 meses (PR7) e até a diferença regional de tarifa. Também citou GF, descartado corretamente (necessidade de só 6 meses). Único senão: a promoção "só até hoje" criou pressa sem fechar.
- **Upsell aceito — Cliente 01185565 (Bruna)**: na reserva assistida da Toro, Bruna apresentou a cobertura a terceiros ampliada com preço e racional ("cobertura maior em sinistros a terceiros, +R$178,50"); a cliente ponderou e aceitou ("Deus me livre acontece alguma coisa"). Upsell de proteção no fluxo natural, sem empurrar.
- **Janela perdida — Cliente 00041270 (Tatiana)**: cliente de máquinas e implementos confirmou pela segunda vez seguida que opera 100% com frota própria e nem acessa a plataforma. A ligação encerrou com "vez em quando eu vou dando uma ligadinha" — nenhuma pergunta sobre custo/renovação da frota própria, nenhuma menção a GF (PR12), seminovos (PR11) ou pesados (PR2).
- **Janela perdida — Cliente 01155964 (Andresa)**: a dor relatada (multas e indenizações sem dono após turnover) é exatamente o problema que telemetria/gestão de frotas resolve; a ligação tratou só o sintoma (achar novo contato) e não conectou o produto (PR3/PR12).

### P7 — Respostas
1. **Qual produto tem maior gap janela×oferta?** PR12 Gestão de frotas e PR3 Telemetria: 5 clientes do lote já são GF ou têm frota própria e mais 2 têm dores típicas de gestão (multas órfãs, governança de aprovação), mas houve só 1 menção ofertiva de GF (e nenhuma de telemetria) — os executivos RAC tratam GF como "outra empresa", não como portfólio. PR7 contrato anual vem em seguida: 3 sinais de recorrência longa, 1 oferta.
2. **Quais clientes têm maior potencial de expansão imediata?** Cliente 01185565 (3 ligações na semana, 3+ veículos novos, filial em cadastro — destravar o P11 do cadastro é destravar receita); Cliente 00844996 (contrato de 6 meses em fechamento, decisor engajado, falta só o acesso); Cliente 00913571 (projeto crescendo, pediu aumento de limite — candidato natural a contrato anual); Cliente 00849954 (ponte provisório→frota definitiva já em andamento).
3. **Algum produto nunca mencionado?** PR2 (pesados), PR3 (telemetria), PR5 (upgrade), PR8 (elétricos), PR9 (ZARP), PR10 (Meoo) e PR11 (seminovos) — 7 dos 12 produtos não aparecem nem na boca do cliente nem na do vendedor. A única ponta de sustentabilidade do lote (o adicional "neutraliza" explicado no Cliente 00951813) não virou conversa de elétricos.
4. **Qual perfil de cliente mais compra cross-sell/upsell quando ofertado?** O cliente em fluxo assistido de reserva/cotação com decisor na linha: as 3 aceitações de proteção (00033938 pós-sinistro, 00849954, 01185565) e a conversão diária→mensal (00839850) aconteceram quando o vendedor estava dentro da transação explicando trade-off de risco/custo com número na mesa. Sondagens frias de carteira ("tem demanda?") não converteram nada no lote.
5. **Mapa de produto por situação:**
   - Quando o cliente diz "batemos o carro / veio cobrança de franquia" → ofereça **PR4 proteção total** na renovação e audite a frota inteira, porque a dor da franquia (12-18 mil) acabou de ficar concreta (funcionou no 00033938).
   - Quando o cliente diz "temos frota própria" → sonde custo total e ofereça **PR12 GF / PR11 seminovos** (e **PR2** se o setor for industrial/agro), porque frota própria declarada é a única razão de inatividade da conta (perdido no 00041270).
   - Quando o cliente diz "as multas estão indo para ninguém / quem cuidava saiu" → ofereça **PR3 telemetria + PR12**, porque gestão de infração é produto, não favor (perdido no 01155964).
   - Quando o cliente diz "o projeto cresceu / preciso de mais limite" → ofereça **PR7 contrato anual** com tarifa menor em troca de compromisso, porque o volume já provou recorrência (perdido no 00913571).
   - Quando o cliente diz "vou ficar só 15-20 dias" mas a tarifa mensal empata → ofereça **conversão para mensal (PR1)** proativamente (funcionou no 00839850).
   - Quando o cliente monta reserva com você na linha → sempre apresente **PR4/cobertura ampliada com preço e cenário** ("se bater num terceiro, cobre até X por +R$Y") — taxa de aceite do lote foi alta nesse formato.

## Observações livres
O lote confirma o padrão de "executivo-concierge": a maior parte do tempo produtivo foi gasta operando o portal no lugar do cliente (5 resets de senha, 2 reservas montadas a quatro mãos, 3 destravamentos de cadastro), o que retém no curto prazo mas não escala e mascara a fricção real da WebCorp. O turnover de gestor no cliente é o fio condutor silencioso do lote — aparece em 5 contas e sempre gera o mesmo trio: acesso morto, fatura órfã e cadastro desatualizado. Houve uma falha operacional interna visível ao cliente: a rediscagem no mesmo dia à Cliente 00714731, que havia pedido retorno na semana seguinte ("acho que foi você mesma!") — sugestão de revisar a fila do discador. A campanha GF↔RAC (desconto de até R$1.000 na fatura GF com 5+ diárias) foi ofertada 2 vezes (00862150, 01070937) com script consistente, ao contrário do observado em lotes anteriores. Duas vendedoras pedem ao cliente que permaneça na linha para a pesquisa de atendimento — sem ditar nota, mas o hábito reforça o alerta de survey-begging já registrado no radar do programa. Nenhuma menção a concorrente em todo o lote.
