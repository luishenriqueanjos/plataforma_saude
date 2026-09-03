# Requisitos

## Glossário do domínio
| Termo | Definição | Fonte |
|---|---|---|
| Volume de treino | Métrica calculada a partir dos registros de séries, repetições e cargas utilizadas em uma sessão de exercícios[cite: 1]. | D1 (README) |
| Periodização | Organização de treinos em diferentes períodos e blocos estruturados[cite: 1]. | D1 (README) |
| Carga | Peso utilizado pelo usuário na execução de um exercício específico[cite: 1]. | D1 (README) |

## Backlog ordenado
| Ordem | Item | Origem | MoSCoW | Risco | Depende de |
|---:|---|---|---|---|---|
| 1 | HU-01 Registrar treino diário (exercícios, séries e cargas) | N1 | Obrigatório | Alto (Banco de Dados) | — |
| 2 | HU-02 Calcular e exibir volume de treino | N2 | Obrigatório | Alto (Lógica Estatística) | HU-01 |
| 3 | HU-03 Cadastrar metas diárias de água e sono | N3 | Importante | Baixo | — |
| 4 | HU-04 Visualizar gráficos de progressão de cargas | N1 | Desejável | Médio (Integração visual) | HU-02 |

## Histórias de usuário e critérios de aceitação
### HU-01 Registrar treino diário
Como praticante de atividades físicas, quero registrar informações como exercícios, séries, repetições e cargas utilizadas[cite: 1], para centralizar minhas informações e acompanhar minha evolução[cite: 1].
[Origem: N1, confirmada em D1]

- **CA-01.1 Caminho principal:** Dado que o usuário está na tela de novo treino, quando ele adiciona um exercício, preenche 3 séries de 10 repetições com 20kg e clica em salvar, então o sistema registra o treino no banco de dados e exibe o resumo da sessão.
- **CA-01.2 Dado incompleto:** Dado que o usuário adicionou um exercício, quando ele tenta salvar o treino sem informar a carga de uma das séries, então o sistema impede o salvamento e destaca o campo obrigatório em vermelho.
- **CA-01.3 Efeito persistente:** Dado que o usuário salvou o treino com sucesso, quando ele acessa o histórico na semana seguinte, então os dados de exercícios, séries e cargas daquela sessão permanecem exatos e inalterados.

### HU-02 Calcular e exibir volume de treino
Como pessoa que realiza treinamento estruturado, quero que o sistema calcule automaticamente o volume do meu treino[cite: 1], para facilitar a análise de performance sem o uso de planilhas genéricas[cite: 1].
[Origem: N2, confirmada em D1]

- **CA-02.1 Cálculo exato:** Dado que o usuário possui um treino registrado com 3 séries de 10 repetições e 20kg de carga, quando ele acessa a tela de detalhes do treino, então o sistema exibe o volume total calculado do exercício (ex: 600kg).

## Casos de uso
### UC-01 Cadastrar novo treino
**Ator principal:** Praticante de atividades físicas.
**Pré-condição:** O usuário está com a aplicação aberta na aba de treinos.
**Garantia de sucesso:** O treino é salvo com a estrutura completa de séries, repetições e cargas[cite: 1].

**Fluxo principal:**
1. O usuário seleciona a opção de iniciar um novo treino.
2. O sistema apresenta um formulário em branco.
3. O usuário seleciona o nome do exercício e preenche quantidade de séries, repetições e carga[cite: 1].
4. O usuário finaliza o treino e confirma o salvamento.
5. O sistema registra os dados e exibe a tela de histórico contendo o volume total calculado[cite: 1].

**Fluxos alternativos:**
- *4a. Conexão perdida durante o salvamento:* O sistema armazena os dados localmente no dispositivo e tenta sincronizar automaticamente quando a conexão voltar, sem perda das informações preenchidas.

## Requisitos não funcionais
- **RNF-01 Privacidade de dados sensíveis:** 
  - **Grandeza:** Nível de acesso aos dados de sono, hábitos alimentares e peso do usuário[cite: 1, 2].
  - **Condição:** Durante o registro no banco de dados.
  - **Aceitável:** Dados anonimizados ou restritos estritamente ao acesso do próprio usuário criador[cite: 2].
  - **Como verificar:** Revisão do checklist de privacidade e segurança a cada marco por parte do responsável (Ayrton)[cite: 2].

## Restrições e regras de negócio
- **RE-01 Consentimento de saúde:** Nenhuma coleta de novo dado sensível (como peso ou sono) pode ocorrer sem o consentimento explícito e anonimização documentada no checklist da iteração[cite: 2].
- **RE-02 Regra de integração de código:** Nenhuma alteração entra direto na branch `main`; todo item exige um Pull Request vinculado ao backlog e aprovação de ao menos 1 integrante da equipe antes do merge[cite: 3].

## Validações realizadas
### V1 — 2026-09-03, Ensaio interno com usuário simulado (Perfil Marcos)
*Nota: Devido ao agendamento pendente, realizamos um ensaio com protótipo de papel simulando o cenário da academia.*
| Achado | Efeito | Item alterado |
|---|---|---|
| Usuário questionou se precisava registrar séries de aquecimento. | Necessidade de separar o cálculo de volume do aquecimento. | Incluída anotação técnica no UC-01 para iterações futuras. |
| Esqueceu de registrar a carga por falha na visualização. | O cálculo de volume ficaria zerado se o campo ficasse vazio. | CA-01.2 criado para impedir salvamento sem informar todas as cargas. |

## Histórico de revisão
- 2026-09-03: linha de base do marco 1.