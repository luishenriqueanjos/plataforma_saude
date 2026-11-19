# Quadro de Tarefas (Kanban)

> **Projeto:** Plataforma de Hábitos Saudáveis e Treinos  
> **Equipe:** Arthur Sidarta, Luis Henrique, Samuel Andrade  
> **Política de WIP (Work in Progress):** Máximo de 1 tarefa ativa em andamento/revisão por integrante.  
> **Fonte do diagrama:** [`diagrams/quadro-tarefas.mmd`](diagrams/quadro-tarefas.mmd)

```mermaid
kanban
  todo["A Fazer — Próxima Semana (Cap. 15 / Evolução)"]
    dt03["Treino multiexercício, autocomplete, sessão anterior e CRUD"]@{ ticket: "DT-03 (2 pts)", assigned: "Arthur Sidarta", priority: "High" }
    hu03_evol["Painel semanal de água e sono, sono decimal/cochilo e modal de metas"]@{ ticket: "HU-03+ (2 pts)", assigned: "Arthur Sidarta", priority: "High" }
    dt01["Extrair consultas SQLite do main.py para módulo próprio"]@{ ticket: "DT-01 (2 pts)", assigned: "Arthur Sidarta", priority: "Low" }
    cap16["Revisão final de documentação, conferência cruzada e roteiro final"]@{ ticket: "Cap. 16 (1 pt)", assigned: "Luis Henrique", priority: "High" }
  inProgress["Em Andamento (In Progress)"]
    hu04["Gráfico de evolução de cargas (Carga Máxima, 1RM e Volume) com filtros"]@{ ticket: "HU-04 (2 pts)", assigned: "Samuel Andrade", priority: "High" }
  inReview["Em Revisão (In Review)"]
    cap12_rev["Conferência cruzada final do Marco 3 e revisão dos PRs de testes"]@{ ticket: "Cap. 12 (1 pt)", assigned: "Luis Henrique", priority: "High" }
  done["Concluído (Done)"]
    hu01["Modelagem SQLite, rota POST /api/treinos e tela de recusa 400"]@{ ticket: "HU-01 (3 pts)", assigned: "Arthur Sidarta", priority: "Very High" }
    hu02["Cálculo automático de volume e histórico de treinos"]@{ ticket: "HU-02 (2 pts)", assigned: "Samuel Andrade", priority: "Very High" }
    arch["Definição da arquitetura, contrato da API e roteiro da Review Parcial"]@{ ticket: "ARCH (2 pts)", assigned: "Luis Henrique", priority: "High" }
    hu03["Cadastro e progresso de metas de água e sono na tabela META"]@{ ticket: "HU-03 (3 pts)", assigned: "Arthur Sidarta", priority: "High" }
    cap10_rev["Checklist de revisão de código, template de PR e métricas GQM"]@{ ticket: "Cap. 10 (1 pt)", assigned: "Luis Henrique", priority: "High" }
    cap10_dt["Mapeamento de dívida técnica com estimativa em pontos"]@{ ticket: "Cap. 10 (DT)", assigned: "Samuel Andrade", priority: "Low" }
    cap11["Inspeção de requisitos e casos de teste no TESTES.md"]@{ ticket: "Cap. 11 (2 pts)", assigned: "Samuel Andrade", priority: "High" }
    cap12_qa["Suíte pytest, verificador ruff, CI verde e testes de metas (CA-03.1–03.3)"]@{ ticket: "Cap. 12 (2 pts)", assigned: "Arthur e Luis", priority: "Very High" }
    kanban_bd["Quadro Kanban em Mermaid e Burndown Chart da Iteração 3"]@{ ticket: "Gestão (18/11)", assigned: "Arthur Sidarta", priority: "High" }
```

---

## Atualização Semanal (Apresentação 19/11 — Cap. 15 e 16)

### O que passou nesta semana (12/11 a 18/11)

- **Fechamento da Iteração 3 (Marco: Qualidade Verificada):**
  - Integração completa da `HU-03` (metas diárias de água e sono) e da suíte de testes automatizados (`pytest`) com verificador de estilo (`ruff`) e CI verde no GitHub Actions (`PR #14` e `PR #16` mesclados na `main`).
  - Expansão da suíte de testes de integração HTTP, contrato JSON de metas diárias (`CA-03.1` a `CA-03.3`) e planejamento semanal de entregas (`PR #15` e `PR #17` abertos para revisão).
  - Conversão do quadro de tarefas para o diagrama nativo `kanban` em Mermaid (`diagrams/quadro-tarefas.mmd`) e criação do **Burndown Chart** da Iteração 3 (`diagrams/burndown-iteracao3.mmd` e `ITERACOES.md`), restando `1 pt` em revisão final (`Cap. 12`).

### O que será feito na próxima semana (Iteração 4 — Evolução / Cap. 15 e 16)

- **`HU-04` (Gráficos de evolução de exercícios — Samuel Andrade):** evolução das sessões por exercício com seletor de métricas (**Carga Máxima**, **1RM Estimado** por Epley e **Volume Total**), filtros de período (`1M`, `3M`, `6M`, `Tudo`) e tooltips interativos.
- **`DT-03` (Treino completo e CRUD — Arthur Sidarta):** liberação de múltiplos exercícios por sessão, campo de busca com autocomplete, recuperação da última sessão do exercício e operações de editar/excluir treino.
- **`HU-03+` (Evolução de hábitos diários — Arthur Sidarta):** painel visual semanal de hidratação e sono (7 dias), registro decimal de sono com opção de cochilo, botão desfazer para hidratação e modal de configuração de metas.
- **`DT-01` (Dívida técnica — Arthur Sidarta):** extrair a camada de persistência SQLite do `main.py` para módulo próprio antes de iniciar o `Cap. 13`/etapas finais.
- **`Cap. 16` (Fechamento — Luis Henrique):** revisão final de documentação, conferência cruzada (`PROJETO.md`, `ARQUITETURA.md`, `ITERACOES.md`) e roteiro da apresentação final.

---

## Histórico de Atualização do Quadro

- **2026-09-17 (Iteração 1):** Criação do quadro com os itens de modelagem (`PROJETO.md`), diagramas e protótipo navegável.
- **2026-10-08 (Iteração 2):** Adoção do limite de WIP (1 tarefa por integrante) e acompanhamento da implementação de `HU-01` e `HU-02` para a Review Parcial.
- **2026-11-05 (Iteração 3):** Movimentação de `HU-01`/`HU-02` para Concluído, inclusão de `HU-03` e tarefas de qualidade e testes (Capítulos 10 a 12).
- **2026-11-18:** Conversão integral do quadro para Mermaid `kanban`, atualização semanal (o que passou e o que será feito na próxima semana — Cap. 15 e 16) e sincronização com a `main`.
