# CLAUDE.md — Guia de interpretação da base de diárias

## Objetivo do repositório

Este repositório armazena uma base versionada de **diárias mensais por código (`Cod`)**, usada para consulta por agentes de IA.

A principal tarefa da IA neste repositório é responder perguntas sobre:

- diárias do tipo **AM**;
- diárias do tipo **AD**;
- histórico mensal por `Cod`;
- carteira associada ao `Cod`;
- CNAE associado ao `Cod`;
- somatórios, comparações e tendências simples ao longo dos meses.

Não invente dados. Se um `Cod`, mês, carteira ou CNAE não for encontrado, responda explicitamente que não há registro na base.

---

## Arquivos principais da base

A base principal fica dividida em **4 arquivos JSON compactados**, para facilitar manutenção no GitHub:

```text
./diarias_00_24.json
./diarias_25_49.json
./diarias_50_74.json
./diarias_75_99.json
```

Cada arquivo contém uma parte dos códigos, definida pelos **2 últimos dígitos do `Cod`**.

### Regra para escolher o arquivo correto

1. Trate `Cod` sempre como **string**.
2. Preserve zeros à esquerda.
3. Se necessário, complete com zeros à esquerda até 8 caracteres.
4. Pegue os **2 últimos dígitos**.
5. Use a faixa abaixo:

| Final do `Cod` | Arquivo |
|---:|---|
| `00` a `24` | `diarias_00_24.json` |
| `25` a `49` | `diarias_25_49.json` |
| `50` a `74` | `diarias_50_74.json` |
| `75` a `99` | `diarias_75_99.json` |

### Exemplos

| Cod informado | Cod normalizado | Final | Arquivo correto |
|---|---:|---:|---|
| `01053727` | `01053727` | `27` | `diarias_25_49.json` |
| `43` | `00000043` | `43` | `diarias_25_49.json` |
| `00192222` | `00192222` | `22` | `diarias_00_24.json` |
| `00337054` | `00337054` | `54` | `diarias_50_74.json` |
| `00082794` | `00082794` | `94` | `diarias_75_99.json` |

---

## Estrutura dos JSONs compactados

Cada arquivo tem esta estrutura geral:

```json
{
  "_meta": {
    "versao": "2.0",
    "gerado_em": "YYYY-MM-DD",
    "parte": "25_49",
    "regra": "Cod com dois últimos dígitos entre 25 e 49",
    "campos": {
      "c": "CNAE",
      "k": "Carteira",
      "h": "Histórico no formato YYYY-MM: [AM, AD]"
    },
    "total_codigos": 9999
  },
  "d": {
    "01053727": {
      "c": "SERVIÇOS DE ARQUITETURA E ENGENHARIA",
      "k": "RJI04A",
      "h": {
        "2026-03": [93, 0],
        "2026-04": [90, 0]
      }
    }
  }
}
```

### Campos

| Campo | Significado |
|---|---|
| `_meta` | Metadados do arquivo. Não contém dados de diárias. |
| `d` | Dicionário principal da base. As chaves são `Cod`. |
| `c` | CNAE do código. |
| `k` | Carteira do código. |
| `h` | Histórico mensal. |
| `YYYY-MM` | Competência no formato ano-mês. |
| `[AM, AD]` | Lista compacta com duas posições: primeira é `AM`, segunda é `AD`. |

### Interpretação obrigatória de `[AM, AD]`

Sempre interprete o array do histórico assim:

```text
[0] = AM
[1] = AD
```

Exemplo:

```json
"2026-03": [93, 4]
```

Significa:

```text
AM = 93
AD = 4
Total do mês = 97
```

---

## Regras de consulta

### Consulta por `Cod`

Quando a pergunta trouxer um `Cod` específico:

1. Normalize o `Cod` como string de 8 dígitos.
2. Escolha apenas o arquivo correspondente pela regra dos 2 últimos dígitos.
3. Procure o `Cod` dentro de `d`.
4. Se o `Cod` não existir em `d`, responda que não há registro para esse código.
5. Se existir, use `c`, `k` e `h` para responder.

### Consulta por mês

Quando a pergunta trouxer uma competência específica, use o formato `YYYY-MM`.

Exemplos válidos:

```text
2025-07
2026-01
2026-06
```

Se o mês não existir em `h`, isso significa que **não há registro para aquele `Cod` naquela competência**. Não trate mês ausente como zero, a menos que o usuário peça explicitamente para preencher ausência com zero.

### Valores zero

Valor zero é diferente de ausência.

Exemplo:

```json
"2026-03": [0, 4]
```

Significa:

```text
AM registrado = 0
AD registrado = 4
```

Mas se `2026-03` não existir no histórico, significa:

```text
Não há registro para 2026-03.
```

---

## Fórmulas e cálculos

### Total mensal

```text
Total = AM + AD
```

### Total de AM em um período

Somar a posição `[0]` de cada mês do período.

### Total de AD em um período

Somar a posição `[1]` de cada mês do período.

### Total geral em um período

```text
Total geral = soma(AM) + soma(AD)
```

### Variação entre meses

Para comparar meses, use:

```text
Variação absoluta = valor_mes_final - valor_mes_inicial
Variação percentual = (valor_mes_final - valor_mes_inicial) / valor_mes_inicial
```

Se o valor inicial for zero, não calcule percentual. Informe que a variação percentual não é aplicável por base inicial igual a zero.

---

## Exemplo de consulta manual

Pergunta:

```text
Qual o AM e AD do código 01053727 em 2026-03?
```

Processo:

```text
Cod = 01053727
Final = 27
Arquivo = diarias_25_49.json
Buscar em d["01053727"]
Buscar h["2026-03"]
```

Se o registro for:

```json
"01053727": {
  "c": "SERVIÇOS DE ARQUITETURA E ENGENHARIA",
  "k": "RJI04A",
  "h": {
    "2026-03": [93, 0]
  }
}
```

Resposta correta:

```text
Para o código 01053727, em 2026-03, foram registradas 93 diárias AM e 0 diárias AD. O total do mês foi 93. CNAE: SERVIÇOS DE ARQUITETURA E ENGENHARIA. Carteira: RJI04A.
```

---

## Função de apoio em Python

Use este padrão quando precisar consultar os arquivos via script:

```python
import json
from pathlib import Path


def normalizar_cod(cod):
    return str(cod).strip().zfill(8)


def arquivo_por_cod(cod, base_dir="."):
    cod = normalizar_cod(cod)
    final = int(cod[-2:])

    if 0 <= final <= 24:
        nome = "diarias_00_24.json"
    elif 25 <= final <= 49:
        nome = "diarias_25_49.json"
    elif 50 <= final <= 74:
        nome = "diarias_50_74.json"
    else:
        nome = "diarias_75_99.json"

    return Path(base_dir) / nome


def buscar_cod(cod, base_dir="."):
    cod = normalizar_cod(cod)
    caminho = arquivo_por_cod(cod, base_dir)

    with open(caminho, "r", encoding="utf-8") as f:
        payload = json.load(f)

    return payload.get("d", {}).get(cod)


def buscar_mes(cod, ano_mes, base_dir="."):
    registro = buscar_cod(cod, base_dir)

    if registro is None:
        return None

    valores = registro.get("h", {}).get(ano_mes)

    if valores is None:
        return {
            "cod": normalizar_cod(cod),
            "encontrado": True,
            "mes_encontrado": False,
            "cnae": registro.get("c"),
            "carteira": registro.get("k"),
            "am": None,
            "ad": None,
            "total": None,
        }

    am, ad = valores

    return {
        "cod": normalizar_cod(cod),
        "encontrado": True,
        "mes_encontrado": True,
        "cnae": registro.get("c"),
        "carteira": registro.get("k"),
        "am": am,
        "ad": ad,
        "total": am + ad,
    }
```

---

## Formato legado

Pode existir um arquivo antigo chamado:

```text
diarias_por_cod.json
```

Esse arquivo usa formato expandido:

```json
{
  "versao": "1.0",
  "gerado_em": "YYYY-MM-DD",
  "total_codigos": 37347,
  "dados": {
    "00000043": {
      "cnae": "SERVIÇOS ESPECIALIZADOS PARA CONSTRUÇÃO",
      "carteira": "S2I05A",
      "historico": {
        "2025-07": {
          "am": 210,
          "ad": 7
        }
      }
    }
  }
}
```

Use o formato legado somente se os 4 arquivos compactados não existirem. Se os arquivos `diarias_00_24.json`, `diarias_25_49.json`, `diarias_50_74.json` e `diarias_75_99.json` existirem, eles são a fonte principal.

---

## Regras para respostas da IA

Ao responder perguntas de negócio:

1. Sempre preserve o `Cod` com zeros à esquerda.
2. Informe a carteira quando ela existir.
3. Informe o CNAE quando ele existir e não for vazio/nulo.
4. Para perguntas de um mês específico, informe AM, AD e total.
5. Para perguntas de período, informe soma de AM, soma de AD e total geral.
6. Para dados ausentes, diga claramente que não há registro.
7. Não deduza valores para meses ausentes.
8. Não altere os JSONs manualmente, salvo se a tarefa for explicitamente atualizar ou corrigir a base.
9. Para alterações estruturais na base, explique o impacto antes de editar arquivos.
10. Evite carregar todos os 4 arquivos se a pergunta puder ser respondida por apenas 1 arquivo.

---

## Regras para manutenção da base

A base deve ser atualizada preferencialmente por script, nunca por edição manual linha a linha.

Fluxo recomendado:

```text
1. Receber/exportar novo CSV.
2. Rodar o script Python de geração/atualização.
3. Validar se os 4 JSONs foram gerados.
4. Conferir total de códigos por arquivo.
5. Fazer commit no Git.
```

O CSV de entrada normalmente tem estas colunas:

```text
Data;Cod;Diarias;tipo;Carteira;CNAE
```

Regras de agregação ao gerar os JSONs:

- Agrupar por `Cod` e `Data`.
- Somar `Diarias` separadamente para `tipo = AM` e `tipo = AD`.
- Guardar CNAE em `c`.
- Guardar carteira em `k`.
- Guardar histórico em `h` no formato `"YYYY-MM": [AM, AD]`.
- Dividir os códigos em 4 arquivos conforme os 2 últimos dígitos do `Cod`.

---

## Padrão de resposta recomendado

Para consulta simples:

```text
Cod: 01053727
Carteira: RJI04A
CNAE: SERVIÇOS DE ARQUITETURA E ENGENHARIA
Competência: 2026-03
AM: 93
AD: 0
Total: 93
```

Para mês ausente:

```text
Não encontrei registro para o código 01053727 na competência 2026-07. O código existe na base, mas esse mês não está presente no histórico disponível.
```

Para código inexistente:

```text
Não encontrei o código 01053727 na parte correspondente da base. Confirme se o Cod está correto e se a base está atualizada.
```

---

## Cuidados importantes

- `Cod` não é número para fins de consulta. É identificador textual com zeros à esquerda.
- Não converter `Cod` para inteiro em respostas ou chaves de busca.
- CNAE pode aparecer como string vazia, `nan` ou ausente em registros antigos. Se isso ocorrer, informe que o CNAE não está disponível.
- Carteira pode eventualmente mudar em atualizações futuras. Se houver múltiplas carteiras em alguma evolução da estrutura, não escolha uma arbitrariamente; informe a ambiguidade.
- Os arquivos JSON podem estar minificados ou com uma linha por código. Isso é esperado.
- A estrutura compacta foi escolhida para reduzir tamanho e facilitar cópia/colagem no GitHub.
