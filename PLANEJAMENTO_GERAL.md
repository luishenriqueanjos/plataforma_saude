# Planejamento Geral — Plataforma de Hábitos Saudáveis e Performance de Treinos

Este documento consolida o diagnóstico técnico do repositório `plataforma_saude`, o mapeamento do que já foi implementado até a **Review Parcial (Encontro 9)**, as entregas em revisão e o planejamento detalhado de todas as etapas restantes até a **Review Final (Encontro 16)**, respeitando estritamente o escopo acadêmico definido em `Descoberta.md`, `Requisitos.md`, `PROJETO.md`, `ARQUITETURA.md`, `PROCESSO.md` e `ITERACOES.md`.

---

## 1. Diagnóstico do Estado Atual do Repositório

### 1.1. Entregas Concluídas (Integradas na `main`)

| Artefato / Funcionalidade | Requisitos / Critérios | Evidência no Repositório | Status |
| :--- | :--- | :--- | :--- |
| Descoberta, Personas e Escopo do MVP | `N1`, `N2`, `N3`, `N4`, `R1`–`R3` | `Descoberta.md` (PRs `#8`, `#9`) | Concluído |
| Especificação de Requisitos e Casos de Uso | `HU-01` a `HU-04`, `UC-01`, `RNF-01`, `RN-01`, `RN-02` | `Requisitos.md` (PR `#10`) | Concluído |
| Modelagem de Domínio, Dados, Sequência e Estados | `D-01` a `D-05` | `PROJETO.md` e `diagrams/*.mmd` (PRs `#11`, `#12`) | Concluído |
| Arquitetura Monolítica Modular e Contrato Inicial | `A-01` a `A-04` | `ARQUITETURA.md`, `contrato/operacoes.md`, `contrato/exemplos/` (PR `#13`) | Concluído |
| Fluxo Principal de Registro de Treinos e Persistência SQLite | `HU-01` (`CA-01.1`, `CA-01.2`, `CA-01.3`) | `main.py` (`init_db`, `obter_treinos`, `salvar_novo_treino`, rotas `GET/POST /api/treinos`) e `prototipo/index.html` (PR `#13`) | Concluído |
| Cálculo Automático de Volume e Validação de Séries | `HU-02` (`CA-02.1`, `CA-02.2`, `CA-02.3`), `RN-01`, `RN-02` | `main.py` (`calcular_volume` e validação `HTTP 400`) e `prototipo/index.html` (PR `#13`) | Concluído |

### 1.2. Entregas em Revisão (Pull Requests Abertos)

| Pull Request | Branch | Responsável | Escopo | Status |
| :--- | :--- | :--- | :--- | :--- |
| [PR #14](https://github.com/luishenriqueanjos/plataforma_saude/pull/14) | `feature/metas-agua-sono` | Arthur (`Sidrata`) | Implementação de metas diárias de água e sono na tabela `META` (`HU-03`: `CA-03.1`, `CA-03.2`, `CA-03.3`), rotas `GET /api/metas`, `POST /api/metas` e `POST /api/metas/progresso`, atualização de `contrato/operacoes.md` e `prototipo/index.html`. | Em revisão (aguardando aprovação e merge) |

*(Observação: existe também a branch remota experimental `origin/feature/meta-sono` criada por Luis Henrique sem PR aberto, cujo escopo de `GET/POST /api/metas` já está contemplado de forma completa com controle de progresso no PR `#14`).*

### 1.3. O Que Está Pendente até a Conclusão do Projeto

1. **Testes Automatizados da Base Existente (`HU-01`, `HU-02`, `RNF-01`):**
   - O repositório não possuía suíte de testes automatizados (`unittest`) para validar persistência SQLite, regras de recusa (`CA-01.2`, `CA-02.2`), cálculo de volume (`CA-02.1`), contrato JSON das rotas `/api/treinos` e conformidade de privacidade (`RNF-01`).
2. **Testes Automatizados e Exemplos de Contrato para Metas Diárias (`HU-03`):**
   - Após/junto à integração do PR `#14`, adicionar exemplos JSON em `contrato/exemplos/` para metas diárias e suíte de testes automatizados cobrindo `CA-03.1`, `CA-03.2` e `CA-03.3`.
3. **Backend, Persistência e Contrato da Evolução/Progressão de Cargas (`HU-04`):**
   - Rota de API `GET /api/treinos/evolucao` (com filtro opcional por exercício) consultando o banco SQLite em ordem cronológica (`YYYY-MM-DD`) e expondo o histórico de séries/cargas por sessão para alimentar os gráficos de linha (`CA-04.1`) e a verificação de suficiência mínima de registros (`CA-04.2`).
4. **Lógica Estatística de Progressão e Métricas de Desempenho (`HU-04` / `HU-02`):**
   - Cálculos estatísticos de evolução por exercício (carga máxima da sessão, carga média, volume por sessão, variação absoluta/percentual entre treinos e indicador de dados suficientes para `CA-04.2`), sob responsabilidade de **Samuel**.
5. **Integração Visual dos Gráficos de Progressão (`HU-04`):**
   - Tela/seção de evolução em `prototipo/index.html` renderizando o gráfico de linhas (`CA-04.1`) e o estado vazio informativo quando houver menos de 2 registros do exercício (`CA-04.2`), sob responsabilidade de frontend (**Ayrton**) e integração com a API (**Arthur**).
6. **Gerenciamento/Exclusão de Registros e Histórico (`PROJETO.md` — Seção Apagamento):**
   - Suporte à exclusão de treino registrado (`DELETE /api/treinos/<id>`) conforme previsto na seção *Modelo de dados > Apagamento* de `PROJETO.md`, mantendo a integridade referencial entre `TREINO`, `EXERCICIO` e `SERIE`.
7. **Verificação de Privacidade (`RNF-01`), Configuração de Implantação e Documentação Final (`ARQUITETURA.md`):**
   - Suporte a configuração de porta/banco via variáveis de ambiente (`PORT`, `DB_PATH`), rota de verificação de saúde (`GET /api/health`), atualização final de `ITERACOES.md`, `PROJETO.md` (conferência cruzada final) e `ARQUITETURA.md`.

---

## 2. Equipe e Divisão de Responsabilidades

| Integrante | Papel no Projeto | Escopo de Atuação |
| :--- | :--- | :--- |
| **Arthur Sidarta** (`Sidrata`) | Desenvolvimento — Banco de Dados, Backend, API e Testes | Esquema e consultas SQLite (`treinos.db`), rotas HTTP/JSON em `main.py`, persistência, integrações de backend, contratos da API (`contrato/`), testes automatizados (`tests/`) e relatórios técnicos semanais (`docs/relatorios/`). |
| **Samuel Andrade** (`samuelsilvaandrade262-rgb`) | Desenvolvimento Estatístico | Lógica estatística de progressão de cargas, métricas de desempenho (carga máxima/média, evolução percentual, série histórica por exercício) e regras de suficiência de dados para `HU-04`. |
| **Luis Henrique** (`luishenriqueanjos`) | Coordenação e Arquitetura | Priorização do backlog, arquitetura do sistema (`ARQUITETURA.md`), organização da documentação (`PROJETO.md`, `ITERACOES.md`), acompanhamento das entregas e revisão/merge de Pull Requests. |
| **Ayrton Miranda** (`Ampds`) | Frontend e Privacidade (`PROCESSO.md` / `README.md`) | Interface web (`prototipo/index.html`), visualização de gráficos (`HU-04`) e revisão do checklist de privacidade (`RNF-01`). |

---

## 3. Matriz de Prioridades e Dependências

| ID da Etapa | Funcionalidade / Entrega | Requisito Relacionado | Prioridade (MoSCoW) | Responsável Principal | Dependências |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **ET-01** | Planejamento Geral, Quadro de Acompanhamento e Suíte de Testes Base (`HU-01` e `HU-02`) | `HU-01`, `HU-02`, `RNF-01`, `RN-01`, `RN-02` | Obrigatório (Must) | Arthur | `main` (PR `#13` já integrado) |
| **ET-02** | Revisão/Integração da `HU-03` (PR `#14`), Testes Automatizados de Metas e Exemplos de Contrato | `HU-03` (`CA-03.1`, `CA-03.2`, `CA-03.3`) | Importante (Should) | Luis (revisão PR `#14`) / Arthur (testes e contrato) | PR `#14` aberto |
| **ET-03** | Lógica Estatística de Progressão de Cargas e Critério de Suficiência (`HU-04`) | `HU-04` (`CA-04.1`, `CA-04.2`) | Desejável (Could) | Samuel | `HU-01`, `HU-02` |
| **ET-04** | Persistência e Endpoint de Histórico/Evolução de Cargas por Exercício (`GET /api/treinos/evolucao`) | `HU-04` (`CA-04.1`, `CA-04.2`) | Desejável (Could) | Arthur | `HU-01`, `HU-02` (integra com **ET-03** quando disponível) |
| **ET-05** | Operação de Exclusão de Treinos (`DELETE /api/treinos/<id>`) e Integridade Referencial no SQLite | `PROJETO.md` (Apagamento), `HU-01` | Importante (Should) | Arthur | `HU-01` |
| **ET-06** | Integração da API de Evolução com o Frontend (`prototipo/index.html`) e Gráficos de Linha | `HU-04` (`CA-04.1`, `CA-04.2`) | Desejável (Could) | Ayrton (UI) / Arthur (integração backend) | **ET-04** |
| **ET-07** | Preparação de Operação/Implantação (`ENV`, `/api/health`), Testes de Regressão e Documentação Final | `RNF-01`, `ARQUITETURA.md`, `ITERACOES.md` | Obrigatório (Must) | Arthur (backend/testes) / Luis (arquitetura e review final) | **ET-01** a **ET-06** |

---

## 4. Distribuição Semanal até a Conclusão (Iterações 3 a 5 — Semanas 01 a 06)

Seguindo o `PROCESSO.md` (3 iterações de 2 semanas entre a Review Parcial no Encontro 9 e a Review Final no Encontro 16), o cronograma semanal de entregas é estruturado abaixo:

### Semana 01 (Iteração 3 — Parte 1)
- **Arthur (`T-ARTHUR-S01`):**
  - Elaborar `PLANEJAMENTO_GERAL.md` e `QUADRO.md` na raiz do repositório.
  - Implementar a suíte de testes automatizados (`tests/test_backend_treinos.py`) validando banco de dados SQLite, regras de negócio (`RN-01`, `RN-02`), critérios `CA-01.1`, `CA-01.2`, `CA-01.3`, `CA-02.1`, `CA-02.2`, `CA-02.3`, privacidade (`RNF-01`) e rotas HTTP (`GET /api/treinos`, `POST /api/treinos`).
  - Documentar relatório técnico em `docs/relatorios/semana-01-arthur.md`.
- **Luis (`T-LUIS-S01`):**
  - Revisar o PR `#14` (`feature/metas-agua-sono` — `HU-03`) e o PR da Semana 01.
- **Samuel (`T-SAMUEL-S01`):**
  - Especificar as fórmulas e estrutura de retorno das métricas de progressão de cargas por exercício (`HU-04`).

### Semana 02 (Iteração 3 — Parte 2)
- **Arthur (`T-ARTHUR-S02`):**
  - Criar a suíte de testes automatizados de metas diárias (`tests/test_backend_metas.py`) cobrindo `CA-03.1`, `CA-03.2` e `CA-03.3` e adicionar exemplos JSON de contrato (`contrato/exemplos/metas-criadas.json`, `contrato/exemplos/erro-meta-invalida.json`).
  - Documentar relatório técnico em `docs/relatorios/semana-02-arthur.md`.
- **Samuel (`T-SAMUEL-S02`):**
  - Implementar funções de cálculo estatístico de evolução de cargas e verificação de suficiência de registros (`CA-04.1`, `CA-04.2`).
- **Luis (`T-LUIS-S02`):**
  - Atualizar `ITERACOES.md` com o registro e retrospectiva da Iteração 3.

### Semana 03 (Iteração 4 — Parte 1)
- **Arthur (`T-ARTHUR-S03`):**
  - Implementar no backend e SQLite a consulta parametrizada e rota `GET /api/treinos/evolucao` (listagem cronológica de cargas e volume por exercício, suportando filtro `?exercicio=...` e indicador de registros suficientes para `CA-04.1` e `CA-04.2`).
  - Integrar com o módulo estatístico de Samuel (caso já mesclado na `main`) ou expor a interface de dados compatível sem substituir o trabalho estatístico de Samuel.
  - Atualizar `contrato/operacoes.md`, criar `contrato/exemplos/evolucao-exercicio.json` e testes em `tests/test_backend_evolucao.py`.
  - Documentar relatório técnico em `docs/relatorios/semana-03-arthur.md`.
- **Samuel (`T-SAMUEL-S03`):**
  - Validar métricas de progressão com séries históricas de múltiplos treinos.
- **Luis (`T-LUIS-S03`):**
  - Revisar atualização de contrato da API e alinhamento arquitetural da `HU-04`.

### Semana 04 (Iteração 4 — Parte 2)
- **Arthur (`T-ARTHUR-S04`):**
  - Implementar a operação de exclusão de treinos (`DELETE /api/treinos/<id>`) prevista em `PROJETO.md` (seção *Apagamento*), garantindo remoção consistente das séries e exercícios vinculados no SQLite, atualização de `contrato/operacoes.md` e testes automatizados (`tests/test_backend_exclusao.py`).
  - Documentar relatório técnico em `docs/relatorios/semana-04-arthur.md`.
- **Ayrton / Equipe (`T-FRONTEND-S04`):**
  - Construir a visualização gráfica de evolução (`CA-04.1` e `CA-04.2`) em `prototipo/index.html`.
- **Luis (`T-LUIS-S04`):**
  - Atualizar `ITERACOES.md` com a retrospectiva da Iteração 4.

### Semana 05 (Iteração 5 — Parte 1)
- **Arthur (`T-ARTHUR-S05`):**
  - Realizar a integração de backend para suportar a tela de evolução e gerenciamento no frontend (`prototipo/index.html` consumindo `GET /api/treinos/evolucao` e `DELETE /api/treinos/<id>`), preservando o funcionamento offline/online e validando todos os fluxos ponta a ponta com testes de integração.
  - Documentar relatório técnico em `docs/relatorios/semana-05-arthur.md`.
- **Samuel (`T-SAMUEL-S05`):**
  - Conferir precisão dos indicadores exibidos no resumo de evolução.
- **Luis (`T-LUIS-S05`):**
  - Conduzir conferência cruzada preliminar para a Review Final.

### Semana 06 (Iteração 5 — Parte 2 — Preparação da Review Final)
- **Arthur (`T-ARTHUR-S06`):**
  - Implementar melhorias de operação e configuração previstas em `ARQUITETURA.md` (variáveis de ambiente `PORT` e `PLATAFORMA_DB_PATH`, endpoint `GET /api/health`, seed de demonstração completo no `--reset`), executar bateria completa de testes de regressão e atualizar a documentação técnica de backend/banco.
  - Documentar relatório técnico final em `docs/relatorios/semana-06-arthur.md`.
- **Luis / Equipe (`T-LUIS-S06`):**
  - Finalizar `ITERACOES.md` e `PROJETO.md` para apresentação da Review Final (Encontro 16).
