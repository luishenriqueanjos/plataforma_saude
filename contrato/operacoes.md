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
