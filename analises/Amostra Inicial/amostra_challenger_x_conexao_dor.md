# Amostra: Challenger (qualidade) × Conexão da solução à dor — só ligações que fecharam

Filtro aplicado no `resultados/consolidado/CONSOLIDADO_LIGACOES.csv` (6.623 ligações):
- **Fechou** = `p1_desfecho` em {fechou_novo, fechou_renovacao, fechou_upsell}
- **Qualidade do Challenger** = campo `p5_qualidade` (alta = "bom/eficiente", baixa = "ruim/ineficiente")
- **Conectou solução à dor** = campo `p1_B5` (SIM/NAO — comportamento "upsell conectado à dor" do Prompt 1)

| Caso | Critério | Candidatos na base |
|---|---|---|
| 1 | Challenger alta + B5=NAO | 117 |
| 2 | Challenger baixa + B5=NAO | 18 |
| 3 | Challenger alta + B5=SIM | 45 |
| 4 | Challenger baixa + B5=SIM | **1** |

Todos os IDs abaixo são `cliente_id` (código, sem nome — carteira/CNAE não usados aqui). Trechos reduzidos para os pontos relevantes; reticências indicam corte de trecho operacional (login, digitação de reserva etc.).

---

## Caso 1 — Challenger bom, mas NÃO conectou a solução a uma dor (fechou)

O vendedor usa uma técnica de Challenger sólida (CH1/CH5/CH6), mas a IA não identificou uma dor explícita do cliente sendo conectada ao produto — o gatilho é operacional/financeiro, não uma dor relatada.

### 1.1 — Cliente 01185565 (642s, fechou_novo, CH5, FC3)
> **Resumo da IA:** Explica as opções de cobertura (padrão e ampliada) para terceiros em caso de sinistros.

> A: "Aí ele vai liberar aqui para você agora, cobertura para terceiros."
> A: "Aí você vai selecionar padrão ou ampliada. A padrão não é cobrado nada, a ampliada é cobrado 178,50 e ela tem uma cobertura maior. Isso são em casos de sinistros a terceiros. Mas digo assim, uma batida, por exemplo, num carro terceiro, entendeu? Ou uma pessoa terceira."
> C: "Vou colocar ampliado, né?"
> A: "Essa pessoa que vai ficar com o carro, ela vai rodar muita estrada..."
> C: "Vai, vai. Vai, eu vou colocar (...) porque Deus me livre acontece alguma coisa... Então vamos lá, proteção a terceiro ampliada."

### 1.2 — Cliente 04198180 (641s, fechou_novo, CH1, FC1)
> **Resumo da IA:** O vendedor revela o custo oculto de alugar em cidades com tarifas mais altas, sugerindo alugar em BH para obter um preço mais baixo.

> A: "Dependendo da quantidade de meses, às vezes vale a pena vocês deslocarem para alguma cidade — por exemplo BH, que tem preços melhores, porque aí você abre o contrato com um preço mais interessante (...) Às vezes abriu em outra cidade, só porque abriu em outra cidade vocês já vão pagar todo mês o valor mais alto de bobeira."
> C: "Para a gente não tem problema nenhum não, porque na verdade a nossa sede era em Belo Horizonte."
> A: "Ouro Branco a gente tem essa modalidade também do mensal fixo, só que tem um preço mais alto (...) vale a pena pegar em BH."

### 1.3 — Cliente 06356330 (218s, fechou_upsell, CH5, FC1)
> **Resumo da IA:** Ampliar contrato diário para mensal evita custos mais altos.

> A: "Você fez uma reserva para a AD de 20 dias que era para ter devolvido no dia 30, certo? Não devolveu. Aí ela está ficando mais cara que o mensal. O que eu te sugiro? Você ampliar esse contrato para o mensal, para deixar ele ali nos 2.600, do que você pagar os 2.800 ou 3.100 se for ficar mais dias com o carro."
> C: "Boa ideia, como é que faz isso aí?"
> A: "Eu já faço aqui para você."

---

## Caso 2 — Challenger ruim (ou ausente) e NÃO conectou a solução a uma dor (fechou)

Nestes casos a IA não identificou nenhuma técnica de Challenger (`p5_codigos_challenger = nenhum`) — são ligações essencialmente operacionais (o vendedor guia o cliente na tela de reserva) que mesmo assim fecharam, porque o cliente já tinha decidido antes de ligar.

### 2.1 — Cliente 12600140 (388s, fechou_novo)
> C: "Vamos escolher o grupo 2 mil quilômetros também, só flexível. Continuar (...) deu o valor 3.259,47 na reserva."
> A: "É só clicar em continuar."

Ligação inteira é passo a passo de preenchimento de reserva — nenhum diagnóstico, nenhuma dor mencionada, nenhuma técnica de venda. Fecha porque o cliente já ligou decidido.

### 2.2 — Cliente 19302679 (99s, fechou_novo)
> C: "Eu estou precisando de limite aí para me alugar carro, cara."
> A: "Deixa eu ver se está comigo aqui (...) já pedi o crédito aqui, deve levar uns 20 a 30 minutos (...) já aprovou! Já consegue retirar."
> C: "Maravilha. Não, então fechou. Obrigada, viu?"

Fechamento imediato por liberação de crédito — não há qualquer elemento de venda consultiva.

### 2.3 — Cliente 09301010 (672s, fechou_novo)
Ligação de suporte de cadastro de usuário no portal (gestão de perfis, redefinição de senha, biometria). Termina com reserva concluída, mas o conteúdo inteiro é operacional/plataforma — reforça a H3 do projeto ("plataforma consome o tempo comercial").

---

## Caso 3 — Challenger eficiente COM conexão da solução à dor (fechou)

Aqui a IA identificou tanto a técnica de Challenger quanto uma dor explícita do cliente sendo resolvida pelo produto — o padrão que a hipótese H10 aponta como o de maior conversão.

⚠️ Nota: o cliente 14683216 (usado antes no slide de diretoria) **foi excluído** desta amostra — já identificado como falso positivo de B5 (não é upsell real, é esclarecimento de forma de pagamento).

### 3.1 — Cliente 11251620 (88s, fechou_upsell, CH1, FC1)
> **Resumo da IA:** O vendedor identificou que o cliente estava pagando mais caro na diária do que pagaria no mensal e ofereceu a migração, o que o cliente aceitou imediatamente.

> C: "Vamos lá, Vitor. Você vai reduzir minha taxa, a tarifa do carro que eu tô ficando, tem um mês com ele já."
> A: "Eu vou te falar exatamente isso (...) eu vi que estava ficando mais ou menos o preço do mensal. Eu falei assim, vou ligar para ele, para falar que compensa mais ele ficar com esse carro mensal do que com..."
> C: "Pode virar, Vitor, fazendo favor" → aceite imediato.

### 3.2 — Cliente 13190047 (920s, fechou_novo, CH1, FC3)
> **Resumo da IA:** A vendedora revela um custo oculto ao explicar que o contrato mensal fixo tem multa de 10% sobre o valor remanescente em caso de devolução antecipada, o que não ocorre no mensal flexível.

> A: "O mensal fixo você não pode devolver antes do prazo se não tem um pagamento de 10% em relação ao prazo remanescente..."
> C: "Eu não posso usar meu dinheiro público para pagar multa. Então eu estou fora. Então tem que ser no mensal flexível, é isso?"
> A: "Se você for ficar com ele seis meses mesmo, ótimo (...) mas se você devolve antes, tem uma multa."
> C: "Vou ficar na mensal flexível, combinado?"

Aqui a dor é explícita (restrição de uso de dinheiro público / risco de multa) e o vendedor ajusta a oferta em tempo real para resolver exatamente isso.

### 3.3 — Cliente 13518725 (594s, fechou_renovacao, CH7, FC1)
> **Resumo da IA:** A vendedora descobriu que o cliente terceirizava caminhões e não sabia que a Localiza oferecia esse serviço, apresentando a solução.

> A: "Você sabe dizer quantos carros você tem de cada... E você tem demanda para caminhão?"
> C: "Temos sim (...) isso aí é 100% terceirizado (...) às vezes eu tenho algumas cargas aqui mais curtas, com o que eu preciso de caminhões menores e acabo pagando um caminhão enorme por nada."
> A: "Devandro, eu não sei se você tem essa informação, mas a Localiza também tem solução para caminhões (...) já te encaminhei o nosso portfólio."
> C: "Ah, que massa!"

Melhor exemplo de CH7 (necessidade não declarada) + dor concreta (pagar caminhão grande por carga pequena) conectada a um produto real (Localiza Pesados).

---

## Caso 4 — Challenger ineficiente/ruim, mas COM conexão à dor (fechou)

**Este caso praticamente não existe na base como padrão real.** Relaxando o filtro (`baixa` + `média`), só há **2 candidatos em 6.623 ligações**, e os dois têm o mesmo problema: `p5_codigos_challenger = nenhum` e `p5_teve_challenger = NAO` — ou seja, a própria IA não identificou nenhuma técnica de Challenger, apesar de `p5_qualidade` ter sido marcado como baixa/média. Isso bate com o bug de divergência entre `p5_teve_challenger` e `p5_qualidade` já registrado na auditoria do H10 (diverge em ~19,6% das linhas).

O único candidato dentro do filtro estrito (baixa + B5=SIM) foi lido na íntegra: é uma ligação **de reserva operacional** (preenchimento de formulário de aluguel) em que o vendedor sugere a "proteção total de avarias" — provavelmente isso disparou o B5=SIM automaticamente (produto ligado a um risco), mas não há nenhum diagnóstico, nenhuma dor relatada pelo cliente, nenhuma técnica Challenger de fato.

### 4.1 — Cliente 07789595 (691s, fechou_novo, B5=SIM, qualidade=baixa, mas CH=nenhum)
> A: "Aí embaixo tem a proteção total de avarias. Eu te aconselho a colocar a proteção total de avarias. É a que eu colocaria para mim."
> C: "Perfeito."
> A: "Mas aí fica o critério, tá?"

Não há dor mencionada pelo cliente em nenhum momento — é uma sugestão de produto padrão, sem diagnóstico. **Recomendo tratar este caso como "não observado na base"** em vez de usar como exemplo real de Challenger ineficiente-mas-conectado — o rótulo B5=SIM aqui é provavelmente ruído de classificação, não um padrão de venda real.

---

## Conclusão prática

- Casos 1, 2 e 3 têm exemplos genuínos e ilustrativos (3 cada).
- Caso 4 é **um vazio estatístico real**: em 6.623 ligações fechadas, não existe um exemplo limpo de "Challenger ruim que ainda assim conectou a dor". Isso é coerente com a lógica do H10 — conectar a dor bem normalmente *é* o que torna o Challenger bom; a combinação inversa (ruim + conectado) é rara/inexistente porque um Challenger que conecta a dor tende a ser automaticamente classificado como de qualidade alta ou média pela IA.
