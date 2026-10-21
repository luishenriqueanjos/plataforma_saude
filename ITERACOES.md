# Iterações

## Iteração 2 (Encontros 8 a 9 — Preparação da Review Parcial)

- **Meta:** Entregar o fluxo principal (`HU-01` e `HU-02`) funcionando de ponta a ponta (interface, servidor Python e banco SQLite), com cálculo real de volume e recusa de dados incompletos.
- **Capacidade:** 4 integrantes (aprox. 8 pontos na iteração).

| Item | Pontos | Responsável principal | Necessário para a demonstração |
| --- | ---: | --- | --- |
| `HU-01` Registrar treino diário (banco SQLite e rota `POST /api/treinos`) | 3 | Arthur Sidarta | Sim |
| `HU-02` Calcular e exibir volume de treino ($\sum \text{rep} \times \text{carga}$) | 2 | Samuel Andrade | Sim |
| Integração da tela (`prototipo/index.html`) com a API e tela de recusa | 2 | Ayrton Miranda | Sim |
| Conferência cruzada (`PROJETO.md`, `ARQUITETURA.md`) e roteiro da Review | 1 | Luis Henrique | Sim |

---

## Iteração 1 (Encontros 6 a 8)

- **Meta:** Definir o modelo de domínio, banco de dados, protótipo navegável e estrutura da arquitetura web.
- **Planejado:** 6 pontos. **Concluído:** 6 pontos (`PROJETO.md`, diagramas Mermaid e protótipo do fluxo principal).

### Retrospectiva da Iteração 1

- **Evidências:** Pull requests `#8`, `#9`, `#10`, `#11` e `#12` integrados ao `main` com `Descoberta.md`, `Requisitos.md`, `PROJETO.md`, diagramas e protótipo HTML.
- **Leitura:** A divisão entre documentação de requisitos, diagramas e protótipo funcionou bem, mas alguns ajustes pequenos foram feitos diretamente no `main` no final da semana por falta de sincronia de horários.
- **Decisões de melhoria:**

| Mudança | Dono | Como conferir | Quando conferir |
| --- | --- | --- | --- |
| Conferência cruzada antes da entrega do marco | Luis Henrique | Tabela de conferência preenchida no `PROJETO.md` | Antes da Review Parcial (Encontro 9) |
| Limitar trabalho em andamento a 1 tarefa por pessoa | Arthur Sidarta | Quadro de tarefas sem acúmulo na coluna "Em revisão" | Retrospectiva da Iteração 2 |

- **Riscos revisados:**
  - `R1` (série salva sem carga distorcendo volume): mitigado com validação no frontend e retorno `400` no backend (`main.py`).
  - `R2` (escopo grande): `HU-03` (metas de água/sono) e `HU-04` (gráficos de evolução) mantidos para a próxima iteração pós-review.

---

## Review parcial (Encontro 9)

- **Ambiente:** Execução local (`python main.py` em `http://localhost:5000`) com banco SQLite (`treinos.db`).
- **Limites e elementos simulados declarados:**
  - **Usuário:** Usuário de teste fixo (`id = 1`, perfil Marcos), pois autenticação não faz parte do escopo atual.
  - **Ambiente:** Servidor local, visto que a implantação externa será tratada no Capítulo 14.
  - **Itens fora desta demonstração (no backlog para as próximas iterações):** `HU-03` (metas de água e sono) e `HU-04` (gráficos de linha de evolução).

### Roteiro da demonstração

| Passo | Ação | O que o público vê | Critério comprovado |
| ---: | --- | --- | --- |
| 1 | Abrir a tela inicial da aplicação (`http://localhost:5000`) | Tela inicial com botão "Iniciar novo treino" e o histórico do último treino salvo no banco | `CA-01.3` |
| 2 | Clicar em "Iniciar novo treino", escolher "Supino reto", informar 3 séries (10 reps × 20 kg) e clicar em "Salvar treino" | O backend grava no SQLite, calcula o volume e exibe a tela "Treino salvo" com `600 kg` | `CA-01.1`, `CA-02.1` |
| 3 | Iniciar novo treino, apagar a carga de uma das séries (deixar vazio ou `0`) e tentar salvar | O sistema recusa o salvamento (`HTTP 400`) e exibe a tela de alerta "Dados incompletos" | `CA-01.2`, `CA-02.2` |
| 4 | Voltar para a tela inicial e atualizar a página (`F5`) | O treino recém-cadastrado permanece listado no histórico com data, exercício e volume total | `CA-01.3`, `CA-02.3` |

### Autoavaliação na data da Review Parcial

| Critério ou requisito | Status | Evidência |
| --- | --- | --- |
| `CA-01.1` Registrar treino (caminho principal) | Atendido | Rota `POST /api/treinos` em `main.py` e passo 2 do roteiro |
| `CA-01.2` Impedir salvamento com carga ausente (recusa) | Atendido | Validação no backend (`400`) e tela de erro no passo 3 do roteiro |
| `CA-01.3` Persistência dos treinos no histórico | Atendido | Tabelas SQLite em `treinos.db` e passo 4 do roteiro |
| `CA-02.1` Cálculo automático exato do volume | Atendido | Regra `RN-01` em `main.py` e exibição no resumo (passo 2) |
| `HU-03` Cadastrar metas diárias de água e sono | Não iniciado | Declarado nos limites: planejado para a Iteração 3 |
| `HU-04` Visualizar gráficos de progressão de cargas | Não iniciado | Declarado nos limites: planejado para a Iteração 3 |
| `RNF-01` Privacidade (uso de usuário de teste sem dados civis) | Atendido | Esquema `USUARIO` em `diagrams/dados.mmd` e `main.py` |
