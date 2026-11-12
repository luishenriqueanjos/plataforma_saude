# Quadro de Tarefas e Acompanhamento Semanal

Este quadro registra o status de todas as entregas do projeto **Plataforma de Hábitos Saudáveis e Performance de Treinos**, incluindo o histórico concluído até a Review Parcial, as entregas em revisão e o cronograma semanal até a Review Final.

---

## 1. Histórico Consolidado (Iterações 1 e 2 — Até a Review Parcial)

| ID | Tarefa / Entrega | Responsável | Critérios de Aceitação / Artefatos | Status | Prazo | Link da Entrega |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `H-01` | Descoberta do problema, personas e escopo | Luis Henrique / Ayrton | `Descoberta.md` (`N1`–`N6`, `R1`–`R3`) | Concluído | 2026-09-02 | [PR #8](https://github.com/luishenriqueanjos/plataforma_saude/pull/8), [PR #9](https://github.com/luishenriqueanjos/plataforma_saude/pull/9) |
| `H-02` | Especificação de requisitos, histórias e casos de uso | Luis Henrique | `Requisitos.md` (`HU-01` a `HU-04`, `UC-01`, `RNF-01`, `RN-01`, `RN-02`) | Concluído | 2026-09-17 | [PR #10](https://github.com/luishenriqueanjos/plataforma_saude/pull/10) |
| `H-03` | Modelagem de domínio, dados, sequência, estados e protótipo | Ayrton / Equipe | `PROJETO.md`, `diagrams/*.mmd`, `prototipo/index.html` | Concluído | 2026-10-08 | [PR #11](https://github.com/luishenriqueanjos/plataforma_saude/pull/11), [PR #12](https://github.com/luishenriqueanjos/plataforma_saude/pull/12) |
| `H-04` | Fluxo principal (`HU-01` e `HU-02`), banco SQLite, API e arquitetura | Arthur / Samuel / Ayrton / Luis | `CA-01.1`, `CA-01.2`, `CA-01.3`, `CA-02.1`, `CA-02.2`, `CA-02.3`, `main.py`, `ARQUITETURA.md`, `ITERACOES.md` | Concluído | 2026-10-21 | [PR #13](https://github.com/luishenriqueanjos/plataforma_saude/pull/13) |
| `H-05` | Implementação de metas diárias de água e sono na tabela `META` (`HU-03`) | Arthur Sidarta | `CA-03.1`, `CA-03.2`, `CA-03.3`, rotas `GET/POST /api/metas` e `POST /api/metas/progresso` | Em Revisão | 2026-11-05 | [PR #14](https://github.com/luishenriqueanjos/plataforma_saude/pull/14) |

---

## 2. Quadro de Execução Semanal (Iterações 3 a 5 — Semanas 01 a 06)

### Semana 01 (Iteração 3 — Parte 1)

| ID | Tarefa | Responsável | Critérios de Aceitação | Status | Prazo | Link da Entrega |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `T-ARTHUR-S01` | Planejamento completo (`PLANEJAMENTO_GERAL.md`, `QUADRO.md`), suíte de testes automatizados do fluxo principal (`tests/test_backend_treinos.py`) e relatório da Semana 01 | Arthur Sidarta | 1. `PLANEJAMENTO_GERAL.md` e `QUADRO.md` criados na raiz.<br>2. Testes automatizados (`unittest`) validando `CA-01.1`, `CA-01.2`, `CA-01.3`, `CA-02.1`, `CA-02.2`, `CA-02.3`, `RN-01`, `RN-02` e `RNF-01` com 100% de aprovação.<br>3. Relatório `docs/relatorios/semana-01-arthur.md` publicado. | Em Revisão (PR Aberto) | Semana 01 (2026-11-11) | [PR #15](https://github.com/luishenriqueanjos/plataforma_saude/pull/15) |
| `T-LUIS-S01` | Revisão do PR `#14` (`HU-03`) e do PR da Semana 01 | Luis Henrique | Revisão de código, verificação de critérios `CA-03.1`–`CA-03.3` e merge para `main`. | Pendente | Semana 01 | — |
| `T-SAMUEL-S01` | Definição das métricas estatísticas de progressão de carga (`HU-04`) | Samuel Andrade | Especificação de cálculo de carga máxima, carga média, variação entre sessões e regra de dados mínimos (`CA-04.1`, `CA-04.2`). | Pendente | Semana 01 | — |

### Semana 02 (Iteração 3 — Parte 2)

| ID | Tarefa | Responsável | Critérios de Aceitação | Status | Prazo | Link da Entrega |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `T-ARTHUR-S02` | Testes automatizados da API de metas diárias (`tests/test_backend_metas.py`) e exemplos JSON de contrato (`HU-03`) | Arthur Sidarta | 1. Testes cobrindo `CA-03.1`, `CA-03.2` e `CA-03.3` (`GET /api/metas`, `POST /api/metas`, `POST /api/metas/progresso`).<br>2. Exemplos JSON em `contrato/exemplos/`.<br>3. Relatório `docs/relatorios/semana-02-arthur.md`. | Pendente | Semana 02 (2026-11-16) | — |
| `T-SAMUEL-S02` | Implementação dos algoritmos estatísticos de progressão de cargas (`HU-04`) | Samuel Andrade | Funções de cálculo de série temporal de cargas, variação percentual e validação de suficiência (`>= 2` sessões para `CA-04.2`). | Pendente | Semana 02 (2026-11-16) | — |
| `T-LUIS-S02` | Registro e retrospectiva da Iteração 3 em `ITERACOES.md` | Luis Henrique | Atualização de `ITERACOES.md` com pontos entregues e retrospectiva da equipe. | Pendente | Semana 02 (2026-11-16) | — |

### Semana 03 (Iteração 4 — Parte 1)

| ID | Tarefa | Responsável | Critérios de Aceitação | Status | Prazo | Link da Entrega |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `T-ARTHUR-S03` | Persistência, consulta SQLite e endpoint `GET /api/treinos/evolucao` para histórico de cargas por exercício (`HU-04`) | Arthur Sidarta | 1. Rota `GET /api/treinos/evolucao` retornando histórico cronológico por exercício e flag de suficiência (`CA-04.1`, `CA-04.2`).<br>2. Contrato atualizado em `contrato/operacoes.md` e exemplo em `contrato/exemplos/evolucao-exercicio.json`.<br>3. Testes em `tests/test_backend_evolucao.py` e relatório `docs/relatorios/semana-03-arthur.md`. | Pendente | Semana 03 (2026-11-23) | — |
| `T-SAMUEL-S03` | Validação estatística das séries históricas por exercício | Samuel Andrade | Conferência dos cálculos de progressão com múltiplos exercícios e cargas variadas. | Pendente | Semana 03 (2026-11-23) | — |
| `T-LUIS-S03` | Revisão arquitetural e de contrato da `HU-04` | Luis Henrique | Revisão de Pull Requests e atualização de `ARQUITETURA.md` se necessário. | Pendente | Semana 03 (2026-11-23) | — |

### Semana 04 (Iteração 4 — Parte 2)

| ID | Tarefa | Responsável | Critérios de Aceitação | Status | Prazo | Link da Entrega |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `T-ARTHUR-S04` | Endpoint de exclusão de treino (`DELETE /api/treinos/<id>`) e integridade referencial no SQLite (`PROJETO.md`) | Arthur Sidarta | 1. Exclusão física em cascata de `SERIE`, `EXERCICIO` e `TREINO` por `id` (`200 OK` ou `404 Not Found`).<br>2. Documentação em `contrato/operacoes.md` e testes em `tests/test_backend_exclusao.py`.<br>3. Relatório `docs/relatorios/semana-04-arthur.md`. | Pendente | Semana 04 (2026-11-30) | — |
| `T-FRONTEND-S04` | Tela de evolução e gráfico de linhas no protótipo (`HU-04`) | Ayrton Miranda | Exibição de gráfico de evolução (`CA-04.1`) e mensagem de dados insuficientes (`CA-04.2`). | Pendente | Semana 04 (2026-11-30) | — |
| `T-LUIS-S04` | Registro e retrospectiva da Iteração 4 em `ITERACOES.md` | Luis Henrique | Atualização de `ITERACOES.md` e revisão dos PRs da Iteração 4. | Pendente | Semana 04 (2026-11-30) | — |

### Semana 05 (Iteração 5 — Parte 1)

| ID | Tarefa | Responsável | Critérios de Aceitação | Status | Prazo | Link da Entrega |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `T-ARTHUR-S05` | Integração da API de evolução e exclusão com o frontend (`prototipo/index.html`) e testes ponta a ponta | Arthur Sidarta | 1. Integração `fetch('/api/treinos/evolucao')` no frontend mantendo fallback offline.<br>2. Testes de integração ponta a ponta.<br>3. Relatório `docs/relatorios/semana-05-arthur.md`. | Pendente | Semana 05 (2026-12-07) | — |
| `T-SAMUEL-S05` | Validação final dos indicadores de progressão exibidos | Samuel Andrade | Revisão dos cálculos apresentados ao usuário na tela de evolução. | Pendente | Semana 05 (2026-12-07) | — |
| `T-LUIS-S05` | Conferência cruzada preliminar para a Review Final | Luis Henrique | Atualização da tabela de conferência cruzada em `PROJETO.md`. | Pendente | Semana 05 (2026-12-07) | — |

### Semana 06 (Iteração 5 — Parte 2 — Review Final)

| ID | Tarefa | Responsável | Critérios de Aceitação | Status | Prazo | Link da Entrega |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `T-ARTHUR-S06` | Preparação de operação (`PORT`, `PLATAFORMA_DB_PATH`, `GET /api/health`), revisão de privacidade (`RNF-01`) e bateria final de testes | Arthur Sidarta | 1. Suporte a variáveis de ambiente e rota `/api/health`.<br>2. Todos os testes automatizados (`unittest`) passando.<br>3. Relatório `docs/relatorios/semana-06-arthur.md`. | Pendente | Semana 06 (2026-12-14) | — |
| `T-LUIS-S06` | Fechamento de `ITERACOES.md`, `ARQUITETURA.md` e roteiro da Review Final (Encontro 16) | Luis Henrique | Documentação final consolidada e roteiro de demonstração completo. | Pendente | Semana 06 (2026-12-14) | — |
