# Recomendação para o time de Produto — renovação de contrato não é automática

**Status:** achado qualitativo confirmado, volume não mensurável via ligações — pedido de dado ao time de Produto/Operações para dimensionar.

Levantado em 04/08/2026 durante auditoria de causa raiz dos códigos de problema (P1/P2/P10/P12) de julho/2026. Ver `apresentacao/arvore_decisao_problemas_produto_julho2026.html`.

---

## 1. O que descobrimos

Contratos de aluguel mensal no regime **"mensal flexível"** (30 dias, renovável) **não renovam automaticamente** no WebCorp. Se ninguém prorrogar manualmente, o contrato "vence" silenciosamente — o cliente continua com o carro, continua pagando em dia, mas passa a estar **sem a proteção total de avarias que contratou**, sem nenhum aviso proativo da Localiza.

**Origem do achado:** ligação de 35 minutos (cliente 10935579, gestor de frota administrando 5 veículos/contratos, 15/07/2026), na qual o cliente audita manualmente cada contrato e descobre o problema ao vivo com o atendente:

> **Cliente:** "Nossa, eu não sabia que esse processo era manual. Caramba! Ou seja, se eu não tivesse feito essa pergunta, a gente nem saberia se acontecesse algum perrengue, a gente estaria fora [da proteção]."

> **Cliente** (mais adiante, sobre outro contrato): "Eu tô fora das proteções... mesmo sem saber. Eu tô com o carro, tô pagando, mas tô fora das proteções."

> **Atendente**, confirmando que não é bug, é o processo mesmo: "O sistema não prorroga automático... Devia ter uma iniciativa da Localiza também para isso... é um processo que tem que ser automático."

O próprio atendente reconhece o problema e concorda que deveria ser automático — não é um erro pontual do sistema, é uma lacuna de produto/processo.

---

## 2. Por que não conseguimos dimensionar isso pelas ligações

Buscamos na base inteira de julho (10.240 ligações) por variações desse padrão — menção explícita a "prorrogação não é automática", proteção/cobertura vencida, cliente pego de surpresa. **Resultado: esse caso é o único que descreve a lacuna de forma explícita na base inteira.**

Isso não enfraquece o achado — o contrário. A natureza do problema é que **ele é invisível pro cliente**: só foi descoberto porque um gestor de frota incomumente meticuloso resolveu auditar contrato por contrato. A esmagadora maioria dos clientes não tem esse nível de atenção, então **não liga reclamando** — não porque o problema não existe, mas porque ninguém percebe que está exposto até um sinistro acontecer.

**Conclusão metodológica:** volume de ligação é a métrica errada para medir esse risco. Risco silencioso não gera chamada. Só dá pra dimensionar de verdade consultando a base de contratos diretamente.

**Proxy indireto que conseguimos extrair (não é o número final, é só um limite inferior de exposição):** 198 clientes distintos (de 8.132 na base de julho) mencionam estar em contrato "mensal flexível" — o tipo de contrato sujeito a essa lacuna — em algum momento do mês. Isso mede quem *tem esse tipo de contrato*, não quem *está com a proteção vencida agora*.

---

## 3. O que estamos pedindo ao time de Produto/Operações

Uma consulta direta na base de contratos (não nas ligações) respondendo:

1. **Quantos contratos ativos hoje estão no regime "mensal flexível"?** (universo total exposto à lacuna)
2. **Desses, quantos estão com a data de prorrogação vencida** (contrato "venceu" mas o veículo continua em uso e sendo faturado)?
3. **Desses, quantos tinham Proteção Total de Avarias contratada** originalmente — ou seja, quantos clientes estão hoje dirigindo *sem saber* que perderam a cobertura que pagavam?
4. Se possível, **distribuição de tempo vencido** (contratos vencidos há 1 semana vs. há meses) — indica há quanto tempo esse gap vem se acumulando sem correção.

---

## 4. Sugestão de correção (para avaliação do time de Produto)

Duas alternativas, em ordem de impacto:

1. **Renovação automática de fato** — o contrato mensal flexível prorroga sozinho enquanto o cliente estiver pagando em dia, sem exigir ação manual do vendedor. Elimina o risco na raiz.
2. **Se renovação automática não for viável a curto prazo**, ao menos um **alerta proativo ao cliente** (e-mail/WhatsApp, não só ao vendedor) quando o contrato estiver a N dias de vencer, deixando claro que a proteção contratada será perdida se não houver ação — hoje esse aviso, quando existe, vai só para o vendedor via e-mail interno (que também mencionou taxa alta de extravio em spam, o mesmo padrão já visto na auditoria de NPS).

---

## 5. Cuidados antes de levar adiante

- Este é um achado de **1 ligação extensa**, não uma amostra estatística — trate como hipótese forte a validar, não como fato quantificado, até a consulta da seção 3 voltar.
- Se a consulta confirmar volume relevante de contratos vencidos com proteção perdida, isso tem exposição financeira e de reputação (cliente sem cobertura em caso de sinistro) — vale tratar com a mesma urgência que o achado de P12 (NPS) já levado ao time de Produto.
