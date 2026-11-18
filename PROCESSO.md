# Processo de desenvolvimento

## Escolha e justificativa
Iterativo e incremental, com iterações de 2 semanas.
Avaliação dos cinco fatores (Boehm e Turner):
- Tamanho: 3 pessoas — ágil
- Criticidade: média, envolve dados pessoais de saúde do usuário (peso, sono, hábitos) — plano-dirigido
- Dinamismo: alto, funcionalidades de acompanhamento e metas ainda em validação com usuários — ágil
- Pessoal: primeira experiência em equipe — plano-dirigido
- Cultura: ajuste tolerado, desde que registrado — ágil

Compensação para o fator "criticidade": checklist de privacidade e segurança de dados de saúde revisado a cada marco, com anonimização/consentimento explícito documentado antes de qualquer coleta de novo dado sensível.

Compensação para o fator "pessoal": artefatos escritos a cada marco e revisão obrigatória de toda contribuição.

## Iteração
- Duração: 2 semanas, iniciando na segunda-feira (1 iteração até o Marco 1 no Encontro 5; mais 2 iterações até a Review Parcial no Encontro 9; até o Encontro 12 para o Marco de Qualidade Verificada; e até a Review Final no Encontro 16)
- Planejamento: 30 min, na segunda-feira
- Acompanhamento: mensagem escrita diária no canal da equipe e quadro de tarefas (`QUADRO_TAREFAS.md`)
- Demonstração: sexta-feira da segunda semana, com o usuário quando possível
- Retrospectiva: 15 min, após a demonstração

## Papéis
- Prioriza o backlog: Luis Henrique Anjos de Oliveira
- Conduz a demonstração: Arthur Sidarta Fernandes de Souza Lima
- Revisa privacidade e dados de saúde: Samuel Silva Andrade
- Demais decisões técnicas: quem estiver na tarefa, conforme `CONTRIBUTING.md`

## Definição de pronto
- Critério de aceitação atendido
- Revisado por outra pessoa com a lista do `CONTRIBUTING.md` e integrado ao `main`
- Verificação automática (`ruff` e `pytest`) verde no GitHub Actions
- Item de backlog fechado e vinculado ao pull request
- Quando aplicável, checklist de privacidade/dados de saúde preenchido

## Qualidade do Processo e Medição da Revisão (Cap. 10)

### Aderência e Eficácia da Revisão
| Pergunta | O que ela examina | Evidência no repositório | No projeto |
| :--- | :--- | :--- | :--- |
| **Aderência** | Todo pull request foi revisado por outra pessoa antes do merge? | Histórico de merges e PRs no GitHub | Sim, PRs revisados entre os membros |
| **Eficácia** | A revisão evita que defeitos de validação/multiplicidade cheguem à demonstração? | Defeitos registrados após integração | Parcial na Iteração 1; corrigido com a inclusão da pergunta de multiplicidade e validação de séries no `CONTRIBUTING.md` |

### Método Objetivo-Pergunta-Métrica (GQM)
| Objetivo | Pergunta | Métrica | Como obter |
| :--- | :--- | :--- | :--- |
| Garantir revisões ágeis que barrem defeitos de regra de negócio antes do `main` | Quanto tempo o pull request espera até a integração? | Tempo entre abertura e merge do PR | Histórico dos Pull Requests no GitHub |
| Garantir revisões ágeis que barrem defeitos de regra de negócio antes do `main` | A revisão está encontrando desvios reais? | Número de comentários classificados como `[Bloqueia]` por PR | Contagem nos comentários do PR |
| Garantir revisões ágeis que barrem defeitos de regra de negócio antes do `main` | O que escapa da revisão? | Defeitos encontrados em testes/demonstração após o merge | Issues de defeito vinculadas ao PR de origem |

## Histórico de revisão do processo
- 2026-08-24: versão adaptada para o app de Hábitos Saudáveis e Treinos
- 2026-10-08: adoção de integração frequente em ramos curtos e padronização da conferência cruzada antes da demonstração
- 2026-11-05: inclusão da lista de verificação de revisão, métricas GQM (Cap. 10) e exigência da suíte automatizada na Definição de Pronto (Cap. 12)
