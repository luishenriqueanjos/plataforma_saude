# Requisitos

## Glossário do domínio
| Termo | Definição | Fonte |
|---|---|---|
| Volume de treino | Soma da multiplicação entre repetições e carga ($\text{repetições} \times \text{carga}$) de todas as séries registradas em um exercício ou sessão. | D1 (README) |
| Série | Conjunto contínuo de repetições de um exercício realizado com determinada carga em kg. | D1 (README) |
| Periodização | Organização de treinos em diferentes períodos e blocos estruturados ao longo do tempo. | D1 (README) |
| Carga | Peso (em quilogramas) utilizado pelo usuário na execução de uma série de um exercício. | D1 (README) |

## Backlog ordenado
| Ordem | Item | Origem | MoSCoW | Risco | Depende de |
|---:|---|---|---|---|---|
| 1 | HU-01 Registrar treino diário (exercícios, séries e cargas) | N1 | Obrigatório | Alto (Banco de Dados) | — |
| 2 | HU-02 Calcular e exibir volume de treino | N2 | Obrigatório | Alto (Lógica Estatística) | HU-01 |
| 3 | HU-03 Cadastrar metas diárias de água e sono | N3 | Importante | Baixo | — |
| 4 | HU-04 Visualizar gráficos de progressão de cargas | N4 | Desejável | Médio (Integração visual) | HU-02 |

## Histórias de usuário e critérios de aceitação

### HU-01 Registrar treino diário
Como praticante de atividades físicas, quero registrar informações como exercícios, séries, repetições e cargas utilizadas, para centralizar minhas informações e acompanhar minha evolução. 
[Origem: N1, confirmada em D1 e V1]

- **CA-01.1 Caminho principal:** Dado que o usuário está na tela de novo treino, quando ele adiciona um exercício, preenche 3 séries de 10 repetições com 20kg e clica em salvar, então o sistema registra o treino no banco de dados e exibe o resumo da sessão.
- **CA-01.2 Dado incompleto (recusa):** Dado que o usuário adicionou um exercício, quando ele tenta salvar o treino sem informar a carga ou as repetições de uma das séries, então o sistema impede o salvamento e exibe a mensagem de alerta de dados incompletos.
- **CA-01.3 Efeito persistente:** Dado que o usuário salvou o treino com sucesso, quando ele recarrega a aplicação ou consulta a lista de treinos registrados, então os dados de data, exercício, séries e cargas daquela sessão permanecem salvos e disponíveis.

### HU-02 Calcular e exibir volume de treino
Como pessoa que realiza treinamento estruturado, quero que o sistema calcule automaticamente o volume do meu treino, para facilitar a análise de performance sem o uso de planilhas genéricas. 
[Origem: N2, confirmada em D1 e V1]

- **CA-02.1 Cálculo exato (caminho principal):** Dado que o usuário possui um treino registrado com 3 séries de 10 repetições e 20kg de carga, quando o treino é salvo ou consultado no resumo, então o sistema calcula e exibe o volume total de 600kg.
- **CA-02.2 Recusa de valores inválidos:** Dado que o usuário está preenchendo as séries de um exercício, quando ele informa carga ou repetições menores ou iguais a zero, então o sistema recusa o cálculo e solicita valores positivos válidos.
- **CA-02.3 Efeito persistente do volume:** Dado que um treino teve seu volume calculado e salvo, quando o usuário visualiza o histórico de treinos na tela inicial, então o volume total correspondente continua exibido junto ao registro do treino.

### HU-03 Cadastrar metas diárias de água e sono
Como iniciante na melhora de hábitos, quero cadastrar metas diárias de consumo de água e horas de sono, para criar uma rotina mais saudável e acompanhar meu progresso.
[Origem: N3, confirmada em D1]

- **CA-03.1 Cadastro de metas (caminho principal):** Dado que o usuário acessa a tela de hábitos diários, quando ele preenche a meta de 2 litros de água e 8 horas de sono e clica em salvar, então o sistema registra essas metas diárias e exibe o progresso inicialmente zerado.
- **CA-03.2 Atualização de progresso:** Dado que o usuário tem uma meta de água estabelecida, quando ele registra o consumo de um copo (ex: 250ml), então o sistema atualiza o progresso em direção à meta total.
- **CA-03.3 Recusa de meta inválida:** Dado que o usuário está cadastrando uma meta diária, quando ele informa um valor vazio ou negativo, então o sistema impede o cadastro e informa que a meta deve ser maior que zero.

### HU-04 Visualizar gráficos de progressão de cargas
Como praticante de treinamento estruturado, quero visualizar gráficos com informações sobre a evolução das minhas cargas ao longo do tempo, para analisar de forma rápida se estou progredindo nos treinos.
[Origem: N4, confirmada em D1]

- **CA-04.1 Exibição de histórico visual:** Dado que o usuário possui o mesmo exercício registrado em múltiplos treinos com cargas variadas, quando ele acessa a tela de evolução, então o sistema apresenta um gráfico de linhas conectando as cargas levantadas nas respectivas datas.
- **CA-04.2 Ausência de dados suficientes:** Dado que o usuário acaba de realizar seu primeiro treino no aplicativo, quando ele acessa a tela de evolução, então o sistema oculta o gráfico vazio e exibe uma mensagem informando que as estatísticas visuais estarão disponíveis após mais registros.

## Casos de uso

### UC-01 Cadastrar novo treino
**Ator principal:** Praticante de atividades físicas.
**Pré-condição:** O usuário está com a aplicação aberta na tela inicial de treinos.
**Garantia de sucesso:** O treino é salvo no banco de dados com a estrutura completa de séries, repetições, cargas e volume total calculado.

**Fluxo principal:**
1. O usuário seleciona a opção de iniciar um novo treino.
2. O sistema apresenta o formulário de registro com data, seleção de exercício e campos de séries.
3. O usuário seleciona o nome do exercício e preenche as repetições e a carga de cada série.
4. O usuário confirma o salvamento do treino.
5. O sistema valida os dados, registra o treino no banco de dados, calcula o volume total e exibe a tela de resumo da sessão.

**Fluxos alternativos:**
- *4a. Dados incompletos ou inválidos:* Caso alguma série esteja sem carga/repetições ou com valor menor ou igual a zero, o sistema impede a gravação e exibe a tela de recusa informando o campo pendente (`CA-01.2`).
- *4b. Usuário cancela o cadastro:* O usuário aciona a opção de voltar/cancelar antes de salvar; o sistema descarta os dados em preenchimento e retorna à tela inicial sem gravar nada no banco.

## Requisitos não funcionais
- **RNF-01 Privacidade de dados sensíveis:** 
  - **Grandeza:** Nível de exposição de dados pessoais de saúde do usuário.
  - **Condição:** Durante o registro e listagem no banco de dados.
  - **Aceitável:** Sem coleta de CPF/dados clínicos sensíveis e uso exclusivo de usuário de teste local até a implementação de autenticação.
  - **Como verificar:** Inspeção do esquema do banco de dados (`diagrams/dados.mmd`) e revisão do checklist de privacidade pelo responsável (Ayrton).

## Restrições e regras de negócio
- **RN-01 Cálculo do volume do exercício:** O volume total de um exercício é obtido pela soma do produto `repetições × carga` de todas as suas séries válidas ($\text{Volume} = \sum_{i=1}^{n} \text{repetições}_i \times \text{carga}_i$). [Origem: D1]
- **RN-02 Obrigatoriedade de carga e repetição:** Nenhuma série pode ser registrada com repetições ou carga vazias ou menores/iguais a zero. [Origem: V1]
- **RE-01 Consentimento de saúde:** Nenhuma coleta de novo dado pessoal sensível pode ocorrer sem revisão prévia no checklist da iteração. [Origem: PROCESSO.md]
- **RE-02 Regra de integração de código:** Toda contribuição deve seguir o fluxo de revisão definido no `CONTRIBUTING.md`. [Origem: CONTRIBUTING.md]

## Validações realizadas
### V1 — 2026-09-03, Validação com usuário (Perfil: Marcos, praticante de musculação)
*Nota: A sessão foi conduzida com base na persona representativa, validando o protótipo no contexto de uso rápido durante o treino na academia.*
| Achado | Efeito | Item alterado |
|---|---|---|
| O usuário avaliou o fluxo de registro de um treino e questionou se as séries iniciais de aquecimento entrariam no volume total, o que distorceria a métrica de esforço real. | Necessidade de considerar futuramente a separação entre série de aquecimento e série válida. | Registrado como observação para evolução futura do backlog. |
| Durante o preenchimento rápido das informações no celular, o usuário esqueceu de preencher a carga da última série. | O cálculo de volume ficaria quebrado ou zerado se o campo fosse salvo vazio. | `CA-01.2` criado na `HU-01` e `RN-02` adicionada para impedir o salvamento sem informar todas as cargas. |

## Histórico de revisão
- 2026-09-03: Atualização e validação com usuário (linha de base do marco 1).
- 2026-09-17: Ajuste de rastreabilidade e inclusão do fluxo de cancelamento no UC-01 após modelagem de estados.
