# Comunicado de lançamento — BI v1 (rascunho)

> Texto para enviar na quarta, 07/10, depois que a reconciliação fechar. Ajustar nomes, link e audiência. O tom é deliberado: dizer o que o painel mostra **e o que ainda não mostra**.

---

**Assunto:** Painel de carga operacional da venda interna — versão 1 (setembro)

Olá, pessoal,

A partir de hoje está no ar o **painel de carga operacional da venda interna (DVINT)**: [link].

**Para que serve.** Mostrar onde o tempo de ligação do time vai: quanto é negociação e quanto é carga operacional (problema, suporte, cobrança, pós-venda e dúvida de contrato). A meta da nossa missão do trimestre é **reduzir a carga operacional sobre a força de vendas** e devolver horas para vender.

**O que tem.** 8 páginas: dia, semana, mês, problemas, carteiras, tempo e ritmo, competências e qualidade do dado. Os números vêm das análises do Aletheia, organizadas por carteira.

**O que olhar primeiro.** Em setembro (01–22/09), **43,2% do tempo de ligação foi carga operacional** e 35,1% foi negociação. As ligações com problema duram quase o dobro das demais (7:12 contra 3:52) e três códigos — acesso/sistema, faturamento/cobrança e crédito/cadastro PJ — concentram dois terços desse tempo.

**O que ainda não é.**
- **É um retrato de setembro.** A duração das ligações só existe até 22/09 e a classificação até 25/09; o painel ainda não é diário. Ele passa a ser diário quando esses dados voltarem a chegar todo dia (previsto até 16/10).
- **O baseline é provisório.** Congelamos o baseline de setembro em 09/10; até lá, os números são ordem de grandeza.
- **A classificação por IA mudou de nível no meio de setembro** (a taxa de problema dobra em 15/09). Por isso mostramos duas réguas lado a lado e **não** devemos concluir "piorou" ou "melhorou" só pela linha do tempo de setembro.

**Como ler os números por carteira.** O painel mostra a carteira (código), não o nome do vendedor. Ele serve para achar onde há obstáculo para remover, não para comparar pessoas. Carteiras com poucas ligações no período não entram em ranking.

**Dúvidas, erros e pedidos.** Fale com [nome] (Excelência Comercial). Se um número não fizer sentido, **avise**: a página "Qualidade do dado" mostra o que sabemos que está errado ou incompleto.

Obrigado,
[nome]

---

## Perguntas frequentes

| Pergunta | Resposta curta |
|---|---|
| Por que o painel não mostra ontem? | A duração das ligações parou de chegar em 22/09 e a classificação em 25/09. Estamos pedindo a normalização; a página 8 mostra isso dia a dia |
| 43,2% é muito? | É o ponto de partida provisório. A meta é −5 p.p. no geral (38,2%) e −10 p.p. nas carteiras do piloto contra as de controle |
| Por que a taxa de problema dobrou em 15/09? | Muito provavelmente por mudança de versão do classificador, não do comportamento do time. Estamos reprocessando setembro com uma única versão (09/10) |
| O que é "carga operacional"? | Tempo em ligações com problema, suporte, cobrança, pós-venda e dúvida de contrato, dividido pelo tempo de todas as ligações classificadas |
| Suporte, cobrança e pós-venda não são papel do vendedor? | São. O painel não diz que são "ruins": mede quanto do tempo eles ocupam, para decidir o que automatizar, resolver na origem ou redistribuir |
| Posso usar o painel para avaliar um vendedor? | Não. É para remover obstáculo. Uma carteira pode ter carga alta por perfil de cliente, não por desempenho |
| Qual duração de ligação é a melhor? | Não há duração única. A taxa de fechamento sobe com a duração, mas a ligação longa também é a de negócio maior. A página 6 mostra o intervalo de confiança |

## O que não concluir dos números de setembro

1. **"A carga subiu na segunda quinzena."** A régua do GPT mudou em 15/09; o Gemini mostra queda no mesmo período.
2. **"A carteira X é pior."** Poucas ligações por carteira geram oscilação grande; use o período inteiro e a mediana.
3. **"A trilha de treinamento vai reduzir a carga."** Competências e carga operacional são metas diferentes; a ligação entre elas é hipótese a testar.
4. **"Fechamos X%."** Fechamento é inferido da conversa (dois classificadores concordam só em parte); não é resultado de reserva ou contrato.
