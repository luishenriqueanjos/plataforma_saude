# Contrato da API — Fluxo Principal (Treinos)

## 1. Registrar novo treino

- **Método e caminho:** `POST /api/treinos`
- **Critérios atendidos:** `CA-01.1`, `CA-01.2`, `CA-02.1`, `CA-02.2`
- **Corpo da requisição (JSON):**

```json
{
  "data": "2026-10-15",
  "exercicio": "Supino reto",
  "series": [
    { "repeticoes": 10, "carga": 20 },
    { "repeticoes": 10, "carga": 20 },
    { "repeticoes": 10, "carga": 20 }
  ]
}
```

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
  - `201 Created`: metas gravadas na tabela `META` e progresso reiniciado em zero (`CA-03.1`).
  - `400 Bad Request`: valores vazios ou menores/iguais a zero (`CA-03.3`).

---

## 5. Registrar progresso diário da meta (copo de água ou horas de sono)

- **Método e caminho:** `POST /api/metas/progresso`
- **Critérios atendidos:** `CA-03.2`
- **Corpo da requisição (JSON):**

```json
{
  "tipo": "agua",
  "quantidade": 250
}
```

- **Resposta `200 OK`:** atualiza a coluna `progresso_atual` na tabela `META` e retorna o novo percentual calculado.
