# RMR — Inteligência Comercial Localiza Frota PJ
## Roteiro de apresentação — 30 minutos — Time (pares) — 13/07/2026

> **Nota de bastidor (não vai pra tela):**
> - Troquei H1 por H2 na espinha da história. H1 ("conta da diária vs. mensal") está com status `Em validação` no documento completo — ainda sem amostra controlada. H2 ("fechar sem data é não fechar") está `Confirmada` e já cobre o bloco de "tipo de fechamento" que você ia mostrar de qualquer forma — economiza uma seção inteira.
> - Os trechos abaixo têm nome de vendedor como aparecem na transcrição original. Oculte antes de subir pro slide, principalmente nos exemplos negativos (FC3) — nos positivos (CH1, B1) o nome pode ficar, é reconhecimento, não constrangimento.
> - Todos os números vêm da base auditada de 1.275 ligações (`apresentacao/APRESENTACAO_EXECUTIVA.md`). Não usei `evidencias_ligacoes.md` como fonte de números — esse arquivo tem estatísticas descartadas (amostra de 14 fechamentos, sinal invertido em B10/B1). Os trechos de conversa de lá foram conferidos e são válidos como ilustração, só as porcentagens ao redor deles é que estavam erradas.

---

## 1. Gancho (2 min)

Não abrir com metodologia. Abrir com o número que ninguém espera:

> "Das 1.275 ligações que a gente analisou em junho, só 7% terminaram em contrato fechado. E antes de vocês acharem que é o time — mais da metade nem era pra fechar."

---

## 2. Contexto rápido (3 min)

Uma frase de escala, sem entrar no framework de 15 perguntas:

- 1.275 ligações gravadas, 1.109 clientes, junho de 2026.
- Método: análise com IA (Gemini) + scoring automático em Python, cruzados.
- Pergunta central do projeto: **"o que o vendedor faz para fechar um contrato?"**
- Um novo lote de 5.348 ligações já chegou (01/07) e está sendo processado — vai dobrar a amostra e validar (ou não) o que vamos ver hoje em escala maior.

---

## 3. H5 — O mercado real é menor do que parece (8 min)

**Número:**
```
56,7% das ligações → não era venda (suporte, senha, biometria, onboarding)
35,8% → interessou mas não fechou
 7,0% → fechou (novo + renovação + upsell)
```

**Gancho de conversa — responsável não encontrado (nome oculto):**

16+ clientes num único bloco ligaram e não conseguiram falar com o responsável pelo contrato:

> "[Vendedor] não trabalha mais aqui", "Fátima está em almoço", "Alexandre em reunião"...

Essas ligações aparecem no sistema como "chamada realizada". Nenhuma teve conversa comercial.

**Comportamento negativo real — suporte que engole a ligação inteira (nome oculto):**
*Cliente 25966050 | 170s | Resultado: fechou renovação | Score comercial: 0*

> **[Vendedor]:** Oi, Eldis, boa tarde. Tudo bem?
> **Cliente:** Alô? Tudo bem?
> **[Vendedor]:** Graças a Deus, tudo jóia e você? Como vai?
> **Cliente:** É tudo quase. [Vendedor], eu queria me mandar, não sei se você era no WhatsApp ou se era no e-mail, para eu poder fazer a renovação, né?
> **[Vendedor]:** Ah, sim. Não recebeu? Eu te mandei no e-mail. Não chegou aí não, Eldis?
> **Cliente:** Não.
> **[Vendedor]:** Tá, eu vou mandar de novo, então, que é o link de prorrogação do contrato, né?

> **O que isso revela:** esse contrato renovou sem nenhum comportamento comercial. O cliente ligou pedindo o link, a vendedora enviou. Renovação por inércia — e migra por inércia quando o concorrente ligar primeiro com proposta ativa.

**Por que importa:** não é "o time é ruim", é "estamos medindo esforço errado". Desarma defensividade antes de entrar em comportamento.

---

## 4. H2 — Fechar sem data é não fechar (10 min)

**Número:**
```
FC3 ("qualquer coisa me chama")     → 44,8% das ligações
FC1 (compromisso duplo, o mais forte) → 31,9%
Prazo definido dos dois lados        → apenas 9%
```

**Gancho de conversa forte — FC3 real (nome oculto):**
*Cliente 26468784 | 66s | Cadastro ativo, sem negócio*

> **[Vendedor]:** Boa tarde! Na verdade, um contato bem rápido. A gente tem um cadastro aqui da sua empresa que foi atualizado este ano em janeiro, mas nós não tivemos ainda o prazer de recebê-los aqui na Localiza nos últimos meses...
> **Cliente:** É, tem assim.
> **[Vendedor]:** E a gente pode manter esse cadastro ativo? Vocês costumam alocar veículos?
> **Cliente:** Não há logo muito não, mas pode deixar ativo.
> **[Vendedor]:** né? Eu vou te mandar um e-mail então, com o telefone da minha mesa aqui, o contato direto. Qualquer situação futura, Diego, pode nos procurar que a gente deixa aqui o cadastro ativo, tá ok?
> **Cliente:** Tá bom.
> **[Vendedor]:** Beleza, muito obrigado! Bom trabalho!

> **O problema:** sem data, sem compromisso do cliente, sem razão pra ele ligar de volta. O cadastro fica "ativo" indefinidamente.

**Caso de negócio real (sem trecho, só o fato):** cliente com proposta do concorrente Carro Zero (assinatura, 12 meses). Vendedor enviou contraproposta por WhatsApp e fechou a ligação com "qualquer coisa me chama". Potencial de R$24.000 em jogo, decisão ficou 100% com o cliente, sem follow-up estruturado.

**Comportamento positivo (B5 — upsell conectado à dor):**
```
21,3% nas ligações que fecharam
13,9% nas que só interessaram
+7,4pp — maior diferencial isolado da base
```
Padrão nas falas de quem converte: "A diária está mais cara que o mensal. Se ampliar para mensal, você economiza." / "Quanto tempo você vai precisar? X dias × R$ diária = R$Y. O mensal custa R$Z." — não é persuasão, é conta que o cliente não tinha feito.

**Challenger (CH1 — custo oculto revelado) — nome pode ficar, é exemplo positivo:**
*Cliente 13382750 | 342s | Contexto: cliente comparando com concorrente mais barato*

> **[Vendedor]:** Agora, Bruno, eu vou te falar o seguinte. O preço deles realmente está no menor preço. Agora, a Localiza teve um ajuste de valor mesmo... Só que o que eu quero é que você fique tranquilo: eles não têm cobertura total. Aí eles cobram tudo de você na indenização. Isso é muito importante.
> ...
> **[Vendedor]:** A taxa de operação nossa é 12% e a deles é 20%.
> **Cliente:** *(confirma depois)* Com vocês eu nem fiz cotação, eu fui direto e já fechei.

> **O que o vendedor fez:** em vez de só dizer "a Localiza é melhor", revelou dado concreto (taxa de operação 12% vs 20%, cobertura inferior do concorrente). Use essa fala como fechamento da seção — é a linha que mais gruda na plateia.

---

## 5. Próximos 30 dias (5 min)

Já está pronto na seção 7 de `APRESENTACAO_EXECUTIVA.md` — puxar direto de lá:

| Ação | Prazo | Impacto |
|---|---|---|
| Ligar pros 5 clientes críticos (08208057, 10845574, 06821416, 27247224, 10508823) | Hoje | Retenção/expansão imediata |
| Escalar biometria pra produto/operações | Esta semana | Libera ~10% da capacidade comercial |
| Treinar CH1 — revelar custo oculto | 2 semanas | +2,5pp em urgência com evidência |
| Treinar B5 — upsell conectado à dor | 2 semanas | +7,4pp, maior diferencial identificado |
| Trocar "qualquer coisa me chama" por prazo com data | 2 semanas | FC3 de 44,8% pra meta abaixo de 20% |

Termina em ação, não em dado.

---

## 6. Visão de escala — de análise pontual pra feedback quase diário (3 min, fecha a apresentação)

O ponto que mais importa pra diretoria não é só o achado — é que isso pode virar operação contínua, sem infra nova:

- O lote de 5.348 ligações representa ~1 mês (julho). Isso dá **~178 ligações/dia**.
- Nesse volume, os 3 grupos de prompt completos (desfecho+comportamento, Challenger+oportunidades, abertura+fechamento) cabem em **~6 chamadas de API por dia** — bem dentro da cota gratuita de 20/dia.
- **Ou seja:** o gargalo que existe agora é só do backlog histórico (5.348 ligações acumuladas de uma vez). Em regime **D-1** — alimentando todo dia só as ligações de ontem — a análise roda folgada, de graça, sem precisar de mais infraestrutura.

**Linha do tempo honesta:**
- **Até 13/07 (hoje):** ainda há gargalo — processando o backlog do lote novo, IA não terminou os 3 grupos.
- **Entre 13/07 e ~20/07:** backlog é zerado, pipeline migra pra D-1, feedback passa a ser quase diário.
- **~20/07 em diante:** time e diretoria têm visibilidade quase em tempo real do que acontece nas ligações, não só um retrato de um mês atrás.

*Frase de fechamento sugerida:* "O que vocês viram hoje é uma foto de junho. Depois de validado, isso vira um filme — atualizado todo dia, sem custo adicional."

---

## 7. Buffer / perguntas (2 min)

---

## Dúvidas prováveis

- **"Isso é IA alucinando ou dado real?"** → "Todo número que mostrei veio da base completa e auditada de 1.275, não de amostra pequena."
- **"E o novo lote de 5.348, muda alguma coisa?"** → "Scoring automático já validou a mesma distribuição na base nova — direção se mantém, IA ainda processando, devo ter os números exatos até a RMR de diretoria."
- **"Por que só 2 hipóteses, o projeto não tem mais coisa?"** → "Tem mais 8 (H1, H3, H4, H6-H10) no documento completo — essa é a versão gancho pra alinhar o time; a versão completa sobe pra diretoria."
- **"Isso vira meta pro time?"** → não responder ao vivo se não combinado antes com o gestor — devolver pra "esse é o próximo passo depois de validar com vocês".
- **"Quando isso vira rotina de verdade?"** → "Até uns 20/07, se a gente validar hoje o caminho. O backlog de julho ainda está sendo processado; depois disso é só manter o dia a dia alimentado."
