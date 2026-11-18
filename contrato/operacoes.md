# Contrato da API — Fluxo Principal (Treinos)

## 1. Registrar novo treino

- **Método e caminho:** `POST /api/treinos`
- **Critérios atendidos:** `CA-01.1`, `CA-01.2`, `CA-02.1`, `CA-02.2`
- **Corpo da requisição (JSON — formato único ou múltiplos exercícios):**

```json
{
  "data": "2026-10-15",
  "exercicios": [
    {
      "nome": "Supino reto",
      "series": [
        { "repeticoes": 10, "carga": 20 },
        { "repeticoes": 10, "carga": 20 }
      ]
    },
    {
      "nome": "Agachamento",
      "series": [
        { "repeticoes": 8, "carga": 60 }
      ]
    }
  ]
}
```

*(Também permanece compatível com o formato legado `{ "data", "exercicio", "series" }` para um único exercício.)*

- **Respostas previstas:**
  - `201 Created`: treino salvo no banco e volume total calculado (exemplo em `contrato/exemplos/treino-criado.json`).
  - `400 Bad Request`: dados obrigatórios ausentes ou valores de repetições/carga menores ou iguais a zero (exemplo em `contrato/exemplos/erro-validacao.json`).

---

## 2. Listar treinos registrados (Histórico)

- **Método e caminho:** `GET /api/treinos`
- **Critérios atendidos:** `CA-01.3`, `CA-02.3`
- **Resposta `200 OK`:** retorna a lista de treinos persistidos no banco, em ordem do mais recente para o mais antigo, com o respectivo volume total calculado.

---

## 3. Consultar metas diárias de hábitos (Água e Sono)

- **Método e caminho:** `GET /api/metas`
- **Critérios atendidos:** `CA-03.1`, `CA-03.2`
- **Resposta `200 OK`:** retorna as metas diárias cadastradas na tabela `META` (`agua` em ml e `sono` em horas), o progresso acumulado no dia e o percentual concluído.

---

## 4. Cadastrar ou atualizar metas diárias

- **Método e caminho:** `POST /api/metas`
- **Critérios atendidos:** `CA-03.1`, `CA-03.3`
- **Corpo da requisição (JSON):**

```json
{
  "agua_ml": 2000,
  "sono_horas": 8
}
```

- **Respostas previstas:**
  - `201 Created`: metas gravadas na tabela `META` e progresso reiniciado em zero (`CA-03.1`; exemplo em `contrato/exemplos/metas-criadas.json`).
  - `400 Bad Request`: valores vazios ou menores/iguais a zero (`CA-03.3`; exemplo em `contrato/exemplos/erro-meta-invalida.json`).

---

## 5. Registrar progresso diário da meta (água fracionada ou sono diário)

- **Método e caminho:** `POST /api/metas/progresso`
- **Critérios atendidos:** `CA-03.2`, `CA-03.3`
- **Corpo da requisição (JSON):**

```json
{
  "tipo": "agua",
  "quantidade": 250,
  "modo": "somar"
}
```

- **Modos aceitos:**
  - `"somar"` *(padrão)*: soma `quantidade` ao `progresso_atual` (ideal para água ao longo do dia).
  - `"definir"`: define diretamente `progresso_atual = quantidade` (ideal para registrar o total de horas dormidas no dia de uma só vez).
- **Respostas previstas:**
  - `200 OK`: atualiza a coluna `progresso_atual` na tabela `META` e retorna o novo percentual calculado (limitado a `100%` para exibição, mantendo o valor acumulado real).
  - `400 Bad Request`: `tipo` diferente de `"agua"`/`"sono"`, `modo` inválido ou `quantidade` vazia, não numérica ou menor/igual a zero (`CA-03.3`).
  - `404 Not Found`: meta diária correspondente ainda não cadastrada na tabela `META`.

---

## 6. Consultar histórico de metas de água e sono

- **Método e caminho:** `GET /api/metas/historico?tipo=agua` *(filtro `tipo` opcional: `agua` ou `sono`)*
- **Critérios atendidos:** `CA-03.1`, `CA-03.2`
- **Resposta `200 OK`:** retorna `resumo_diario` (totais por data, meta diária, percentual e flag `atingida`) e `registros` (histórico detalhado em ordem do mais recente para o mais antigo).

---

## 7. Consultar evolução de cargas por exercício

- **Método e caminho:** `GET /api/treinos/evolucao?exercicio=Supino%20reto`
- **Critérios atendidos:** `CA-04.1`, `CA-04.2`
- **Resposta `200 OK`:** retorna os exercícios disponíveis, a série cronológica por sessão (`carga_maxima`, `carga_media`, `volume_total`, `total_series`), resumo de variação e a flag `dados_suficientes` (`true` quando houver `>= 2` sessões; exemplo em `contrato/exemplos/evolucao-exercicio.json`).
