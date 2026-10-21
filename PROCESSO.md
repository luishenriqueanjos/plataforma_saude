# Processo de desenvolvimento

## Escolha e justificativa
Iterativo e incremental, com iterações de 2 semanas.
Avaliação dos cinco fatores (Boehm e Turner):
- Tamanho: 4 pessoas — ágil
- Criticidade: média, envolve dados pessoais de saúde do usuário (peso, sono, hábitos) — plano-dirigido
- Dinamismo: alto, funcionalidades de gamificação e lembretes ainda em validação com usuários — ágil
- Pessoal: primeira experiência em equipe — plano-dirigido
- Cultura: ajuste tolerado, desde que registrado — ágil

Compensação para o fator "criticidade": checklist de privacidade e segurança de dados de saúde revisado a cada marco, com anonimização/consentimento explícito documentado antes de qualquer coleta de novo dado sensível.

Compensação para o fator "pessoal": artefatos escritos a cada marco e revisão obrigatória de toda contribuição.

## Iteração
- Duração: 2 semanas, iniciando na segunda-feira (1 iteração até o Marco 1 no Encontro 5; mais 2 iterações até a Review Parcial no Encontro 9; e 3 iterações até a Review Final no Encontro 16)
- Planejamento: 30 min, na segunda-feira
- Acompanhamento: mensagem escrita diária no canal da equipe
- Demonstração: sexta-feira da segunda semana, com o usuário quando possível
- Retrospectiva: 15 min, após a demonstração

## Papéis
- Prioriza o backlog: Luis Henrique Anjos de Oliveira
- Conduz a demonstração: Arthur Sidarta Fernandes de Souza Lima
- Revisa privacidade e dados de saúde: Ayrton Miranda Pimenta da Silva
- Demais decisões técnicas: quem estiver na tarefa, conforme CONTRIBUTING.md

## Definição de pronto
- Critério de aceitação atendido
- Revisado por outra pessoa e integrado ao `main`
- Item de backlog fechado e vinculado ao pull request
- Quando aplicável, checklist de privacidade/dados de saúde preenchido

## Histórico de revisão do processo
- 2026-08-24: versão adaptada para o app de Hábitos Saudáveis e Treinos
- 2026-10-08: adoção de integração frequente em ramos curtos e padronização da conferência cruzada antes da demonstração
