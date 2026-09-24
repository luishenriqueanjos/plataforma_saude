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
Como praticante de atividades físicas, quero registrar informações como exercícios, séries, repetições e cargas utilizadas[cite: 1], para centralizar minhas informações e acompanhar minha evolução. 
[Origem: N1, confirmada em D1]

- **CA-01.1 Caminho principal:** Dado que o usuário está na tela de novo treino, quando ele adiciona um exercício, preenche 3 séries de 10 repetições com 20kg e clica em salvar, então o sistema registra o treino no banco de dados e exibe o resumo da sessão.
- **CA-01.2 Dado incompleto:** Dado que o usuário adicionou um exercício, quando ele tenta salvar o treino sem informar a carga de uma das séries, então o sistema impede o salvamento e destaca o campo obrigatório em vermelho.
- **CA-01.3 Efeito persistente:** Dado que o usuário salvou o treino com sucesso, quando ele acessa o histórico na semana seguinte, então os dados de exercícios, séries e cargas daquela sessão permanecem exatos e inalterados.

### HU-02 Calcular e exibir volume de treino
Como pessoa que realiza treinamento estruturado, quero que o sistema calcule automaticamente o volume do meu treino[cite: 1], para facilitar a análise de performance sem o uso de planilhas genéricas. 
[Origem: N2, confirmada em D1]

- **CA-02.1 Cálculo exato:** Dado que o usuário possui um treino registrado com 3 séries de 10 repetições e 20kg de carga, quando ele acessa a tela de detalhes do treino, então o sistema exibe o volume total calculado do exercício (ex: 600kg).

### HU-03 Cadastrar metas diárias de água e sono
Como iniciante na melhora de hábitos, quero cadastrar metas diárias de consumo de água e horas de sono[cite: 1], para criar uma rotina mais saudável e acompanhar meu progresso.
[Origem: N3, confirmada em D1]

- **CA-03.1 Cadastro de metas:** Dado que o usuário acessa a tela de hábitos diários, quando ele preenche a meta de 2 litros de água e 8 horas de sono e clica em salvar, então o sistema registra essas metas diárias e exibe o progresso inicialmente zerado.
- **CA-03.2 Atualização de progresso:** Dado que o usuário tem uma meta de água estabelecida, quando ele registra o consumo de um copo (ex: 250ml), então o sistema atualiza a barra de progresso visual em direção à meta total.

### HU-04 Visualizar gráficos de progressão de cargas
Como praticante de treinamento estruturado, quero visualizar gráficos com informações sobre a evolução das minhas cargas ao longo do tempo[cite: 1], para analisar de forma rápida se estou progredindo nos treinos.
[Origem: N1, confirmada em D1]

- **CA-04.1 Exibição de histórico visual:** Dado que o usuário possui o mesmo exercício registrado em múltiplos treinos com cargas variadas, quando ele acessa a tela de evolução, então o sistema apresenta um gráfico de linhas conectando as cargas levantadas nas respectivas datas.
- **CA-04.2 Ausência de dados suficientes:** Dado que o usuário acaba de realizar seu primeiro treino no aplicativo, quando ele acessa a tela de evolução, então o sistema oculta o gráfico vazio e exibe uma mensagem informando que as estatísticas visuais estarão disponíveis após mais registros.

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
### V1 — 2026-09-03, Validação com usuário (Perfil: Marcos, praticante de musculação)
*Nota: A sessão foi conduzida com base na persona representativa, validando um protótipo de baixa fidelidade (papel) no contexto de uso rápido pelo celular durante o treino na academia.*
| Achado | Efeito | Item alterado |
|---|---|---|
| O usuário avaliou o fluxo de registro de um treino e questionou se as séries iniciais de aquecimento entrariam no volume total, o que distorceria a métrica de esforço real. | Necessidade de separar o cálculo de volume do aquecimento das séries válidas. | Incluída anotação de exceção no UC-01 para planejamento de iterações futuras. |
| Durante o preenchimento rápido das informações no celular, o usuário esqueceu de preencher a carga da última série. | O cálculo de volume ficaria quebrado ou zerado se o campo fosse salvo vazio. | CA-01.2 criado na HU-01 para impedir o salvamento sem informar todas as cargas. |

## Histórico de revisão
- 2026-09-03: Atualização e validação com usuário (linha de base do marco 1).