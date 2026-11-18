# Relatório Técnico — Semana 02 (Arthur Sidarta)

- **Responsável pela trilha:** Arthur Sidarta Fernandes de Souza Lima (`@Sidrata`)
- **Tarefa do Quadro:** `T-ARTHUR-S02` — Testes Automatizados de Metas Diárias, Exemplos JSON de Contrato e Sincronização com a `main` (`HU-03`: `CA-03.1`, `CA-03.2`, `CA-03.3`)
- **Branch:** `feature/arthur-semana-02-testes-e-contrato-metas`
- **Pull Request:** *(será atualizado após abertura do PR)*
- **Declaração de uso de IA:** Este artefato e os testes/contratos associados foram desenvolvidos com assistência de agente autônomo de IA (Antigravity / Gemini), sob supervisão e revisão da trilha de Banco de Dados, Backend, API e Testes atribuída a Arthur Sidarta.

---

## 1. O que foi desenvolvido

1. **Exemplos JSON oficiais de contrato para Metas Diárias (`HU-03`):**
   - `contrato/exemplos/metas-criadas.json`: modelo exato de resposta `201 Created` para `POST /api/metas` (`agua_ml = 2000`, `sono_horas = 8`, progresso zerado e percentual `0`).
   - `contrato/exemplos/erro-meta-invalida.json`: modelo exato de resposta `400 Bad Request` para metas inválidas (`<= 0`).
   - Atualização de `contrato/operacoes.md` referenciando ambos os arquivos de exemplo e documentando explicitamente as respostas `400 Bad Request` e `404 Not Found` de `POST /api/metas/progresso`.
2. **Suíte de Testes Automatizados de Metas Diárias (`tests/test_backend_metas.py`):**
   - Implementação de 6 testes automatizados (`unittest`, compatíveis também com `pytest`) validando persistência SQLite na tabela `META`, regras de negócio (`CA-03.1`, `CA-03.2`, `CA-03.3`), teto visual de `100%` no percentual de progresso, recusa de entradas inválidas e fluxo HTTP completo via `HTTPServer` efêmero (`GET /api/metas`, `POST /api/metas`, `POST /api/metas/progresso`).
3. **Sincronização com o pipeline de CI da `main`:**
   - Integração limpa da `origin/main` (que trouxe a `HU-03` dos PRs `#14` e `#16`, `pytest` e `ruff` em `.github/workflows/verificacao.yml`) e ajuste de formatação em `tests/test_backend_treinos.py` com `ruff format` para manter a verificação automática 100% verde.

---

## 2. Qual problema foi resolvido

Após o merge da `HU-03` (`PR #14` e `PR #16`) na `main`, as rotas de metas diárias (`GET /api/metas`, `POST /api/metas` e `POST /api/metas/progresso`) possuíam testes unitários diretos em `tests/test_api_treinos.py`, mas ainda faltavam:
- Os arquivos de exemplo JSON em `contrato/exemplos/` vinculados ao `contrato/operacoes.md` (equivalentes aos já existentes para `/api/treinos`);
- Testes de integração HTTP reais exercitando serialização JSON, cabeçalhos, códigos de status (`200`, `201`, `400`, `404`) e persistência fim a fim nas rotas de metas;
- Verificação automatizada de casos de borda da `HU-03`, como atualização de metas existentes sem duplicar linhas na tabela `META`, preservação dos valores salvos após erro `400`, e teto de `100%` quando o consumo ultrapassa a meta diária.

---

## 3. Como o código funciona (Guia para apresentação)

O arquivo `tests/test_backend_metas.py` é composto por duas classes de teste seguindo o padrão `# Preparar`, `# Agir`, `# Conferir`:

1. **`TestMetasPersistenciaERegras`:**
   - Isola o banco SQLite em um diretório temporário (`tempfile.TemporaryDirectory`) redirecionando `main.DB_PATH` e executando `main.init_db(reset=True)` em `setUp()`.
   - Confirma que o seed inicial cria exatamente as metas padrão (`agua = 2000.0 ml`, `sono = 8.0 h`, `progresso_atual = 0.0`) sem duplicar registros quando `main.salvar_metas()` é chamado novamente.
   - Valida que entradas inválidas (`0`, negativos, string vazia, `None`, `"abc"`) retornam `400` com as mesmas chaves de `contrato/exemplos/erro-meta-invalida.json` e não alteram o banco.
   - Valida o acúmulo de progresso em `main.registrar_progresso_meta()`, o tratamento case-insensitive de `"SONO"`, o limite de `100%` no `percentual` e o retorno `404` quando a tabela `META` está vazia.
2. **`TestMetasIntegracaoHTTP`:**
   - Sobe uma instância real de `HTTPServer(("127.0.0.1", 0), main.PlataformaHandler)` em thread `daemon` com porta dinâmica alocada pelo sistema operacional.
   - Realiza requisições HTTP com `urllib.request` para `GET /api/metas`, `POST /api/metas` (`201` e `400`) e `POST /api/metas/progresso` (`200` e `400`), comparando os payloads JSON retornados com `contrato/exemplos/metas-criadas.json` e `contrato/exemplos/erro-meta-invalida.json`.

---

## 4. Quais arquivos foram criados/modificados

| Arquivo | Tipo de Alteração | Descrição |
| :--- | :--- | :--- |
| `contrato/exemplos/metas-criadas.json` | Novo arquivo | Exemplo JSON da resposta `201 Created` de `POST /api/metas`. |
| `contrato/exemplos/erro-meta-invalida.json` | Novo arquivo | Exemplo JSON da resposta `400 Bad Request` para meta inválida. |
| `contrato/operacoes.md` | Atualização | Referência aos exemplos JSON de metas e respostas `400`/`404` em `/api/metas/progresso`. |
| `tests/test_backend_metas.py` | Novo arquivo | 6 testes automatizados de regras, persistência SQLite e integração HTTP da `HU-03`. |
| `tests/test_backend_treinos.py` | Formatação (`ruff`) | Adequação à checagem `ruff format --check .` do workflow de CI. |
| `QUADRO.md` | Atualização | Atualização do status de `H-05` (`Concluído`) e `T-ARTHUR-S02` (`Em Revisão`). |
| `docs/relatorios/semana-02-arthur.md` | Novo arquivo | Relatório técnico detalhado da entrega da Semana 02. |

---

## 5. Conceitos técnicos utilizados

- **Testes Guiados por Contrato (*Contract Testing*):** Comparação direta entre os JSONs reais devolvidos pelas rotas HTTP e os exemplos documentados em `contrato/exemplos/`.
- **Isolamento de Banco SQLite em Testes:** Uso de `tempfile.TemporaryDirectory()` + substituição temporária de `main.DB_PATH` para evitar qualquer efeito colateral no `treinos.db` local.
- **Servidor HTTP Efêmero com Porta `0`:** Execução real do `BaseHTTPRequestHandler` em thread de teste com fechamento explícito de conexões e respostas `HTTPError`.

---

## 6. Testes executados e resultados obtidos

Todos os comandos abaixo foram executados na raiz do repositório após as alterações finais:

1. `python -m ruff format --check .` -> `5 files already formatted` (exit code `0`)
2. `python -m ruff check .` -> `All checks passed!` (exit code `0`)
3. `python -m unittest discover -s tests -v` -> `Ran 14 tests in 1.407s — OK`
4. `python -m pytest -v` -> `33 passed in 2.14s`
