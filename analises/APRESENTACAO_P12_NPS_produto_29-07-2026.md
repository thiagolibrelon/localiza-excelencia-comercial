# Apresentação — P12 (Manipulação de NPS) para times de Produto e NPS

**Status:** PRELIMINAR — base de julho com 86% de cobertura em P3/P7 (5.334 de 6.641 ligações) em 29/07/2026.
**TODO antes da reunião:** rodar de novo depois que P3/P7 fechar 100% (execução agendada amanhã, 30/07, 4:30 BRT — cota reseta e deve zerar os ~13 batches restantes). Comando de recontagem no fim deste arquivo.

Rascunhado em 29/07/2026 a pedido do usuário, que vai puxar agenda com o time de Produto e o time de NPS (mesma pessoa/área, dois analistas diferentes) pra discutir o achado.

---

## 1. Contexto — por que isso virou pauta

Em 09/07/2026, uma auditoria de compliance encontrou 2 casos pontuais de coaching explícito de nota de pesquisa de satisfação (vendedor dita a nota que o cliente deve dar). Isso gerou a categoria **P12 (Manipulação de pesquisa/NPS)** no Prompt 3 (Problemas Recorrentes), que desde então roda sistematicamente em toda ligação analisada — não é mais amostra pontual, é classificação de 100% da base.

Ver histórico completo em `analises/AUDITORIA_manipulacao_nps.md`.

## 2. Escala (dado quantitativo, base julho 2026)

- **141 ligações com P12** de 5.334 analisadas (86% da base) = **6,2% de todos os problemas detectados no mês**, **2,6% de todas as ligações**.
- **90% desses casos (127/141) nunca foram escalados** (`escalou_para=nao_escalou`) — hoje não existe nenhum mecanismo que capture isso.
- 127/141 detectados pelo padrão do próprio vendedor (`vendedor_detectou`); 13 vieram de comentário espontâneo do cliente.
- Contexto adicional (problemas em geral, não só P12): taxa de resolução na própria ligação = 54,7% (932 SIM vs 773 NÃO); escalonamento geral quando ocorre: 0800 (129), supervisora (68), IT (34), assistência clientes (8).

## 3. Evidência — 4 exemplos com transcrição real

| Data | Cliente / Vendedor | Frase |
|---|---|---|
| 17/06/2026 | Cliente 02536234 / Luma | "tem que ser até o final, senão não contabiliza... as notas boas é 9 e 10" |
| 22/06/2026 | Cliente 16824498 / Fabrício | "o gol é sempre dá 10 em tudo, já dando 9 já ajuda" |
| **08/07/2026** | **Cliente 12660415** | **"não precisa me dar 10 em tudo não, mas me dando 9 já me ajuda, viu?"** |
| **17/07/2026** | **Cliente 06495149** | **"8 não é nota boa, puxa meu resultado pra baixo... não precisa ceder, mas pelo menos o 9 vai me ajudar muito"** |

**Ponto forte pra reunião:** a frase "me dando 9 já ajuda" se repete quase palavra por palavra em 2 vendedores diferentes, em 2 meses diferentes (junho e julho). Sugere prática compartilhada informalmente no time, não invenção isolada de 1 pessoa.

Transcrições completas dos 2 casos de junho: `analises/AUDITORIA_manipulacao_nps.md`.
Origem dos 2 casos de julho: `JULHO/dados_convertidos/julho_completo.json`, clientes 12660415 (08/07) e 06495149 (17/07) — trechos extraídos e conferidos em 29/07/2026.

## 4. Estrutura sugerida (4 blocos)

1. **O que é / por que virou pauta** — nasceu de 2 casos pontuais em auditoria de compliance, virou classificação sistemática.
2. **Escala** — os números da seção 2. Deixar claro que é 86% da base (antecipa objeção "isso pode cair quando fechar").
3. **Evidência** — tabela da seção 3, com destaque pra repetição de frase entre vendedores/meses.
4. **Por que importa pros dois times (separar os asks):**
   - **Time de NPS:** se a nota alimenta indicador de qualidade/comp de vendedor, está inflada por construção. Ask: cruzar notas reais desses ~141 clientes com a média geral pra estimar o viés.
   - **Time de Produto:** processo de coleta (timing, forma de pedir) cria oportunidade de manipulação. Ask: avaliar pesquisa assíncrona/pós-ligação automatizada, sem o vendedor saber o momento exato do envio.

## 5. Cuidados antes de levar

1. **Preliminar** — 86% da base. Recontar antes de usar os números como definitivos (comando abaixo).
2. **Nomes de vendedor/cliente** — a auditoria original usa nome de vendedor (Luma, Fabrício) e cliente. Decidir se anonimiza para "Vendedor A/B" na versão de apresentação, ou se mantém (usuário ainda não decidiu — perguntar antes de montar o deck final).

## 6. Comando para recontar com a base completa

```bash
cd "C:\Users\quase\Documents\Ligaçoes"
python -c "
import csv
from collections import Counter

c = Counter()
resolvido = Counter()
com_problema = 0
total = 0
p12_resolvido = Counter()
p12_escalou = Counter()
p12_quem = Counter()

with open('JULHO/consolidado/P3.csv', encoding='utf-8') as f:
    r = csv.DictReader(f)
    for row in r:
        total += 1
        probs = row['problemas_identificados']
        if probs and probs != 'nenhum':
            com_problema += 1
            codes = [p.strip() for p in probs.split('+') if p.strip()]
            for p in codes:
                c[p] += 1
            if 'P12' in codes:
                p12_resolvido[row['foi_resolvido_na_ligacao']] += 1
                p12_escalou[row['escalou_para']] += 1
                p12_quem[row['quem_relatou']] += 1

print('Total P3:', total, '| com problema:', com_problema)
print('P12 total:', c['P12'], f\"({c['P12']/com_problema*100:.1f}% dos problemas, {c['P12']/total*100:.1f}% de todas ligacoes)\")
print('P12 quem_relatou:', dict(p12_quem))
print('P12 escalou:', dict(p12_escalou))
"
```

## Próximo passo

Depois de recontar com 100%: montar o deck de fato (referência: `scripts/gerar_rmr_5slides.py`). Perguntar ao usuário se quer anonimizar nomes antes de gerar a versão final.
