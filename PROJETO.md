# Projeto

## Modelo de domínio

Diagrama em `diagrams/dominio.mmd`.

| Classe    | Origem no REQUISITOS.md | Observação                                                                       |
| --------- | ----------------------- | -------------------------------------------------------------------------------- |
| Usuário   | HU-01, HU-03, HU-04     | Representa a pessoa que utiliza o sistema para registrar e acompanhar seus dados |
| Treino    | HU-01, HU-02, HU-04     | Representa uma sessão de treinamento realizada pelo usuário                      |
| Exercício | HU-01, HU-02            | Representa um exercício realizado durante um treino                              |
| Série     | HU-01, HU-02            | Armazena as repetições e a carga utilizadas em uma série                         |
| Meta      | HU-03                   | Representa uma meta diária relacionada à água ou ao sono                         |

### Associações e multiplicidades

* Um **Usuário** pode possuir vários **Treinos**; cada Treino pertence a um único Usuário. `Usuário 1:N Treino`
* Um **Treino** possui um ou vários **Exercícios**; cada Exercício registrado pertence a um único Treino. `Treino 1:N Exercício`
* Um **Exercício** possui uma ou várias **Séries**; cada Série pertence a um único Exercício. `Exercício 1:N Série`
* Um **Usuário** pode possuir várias **Metas**; cada Meta pertence a um único Usuário. `Usuário 1:N Meta`

## Modelo de dados

Diagrama em `diagrams/dados.mmd`.

O modelo de dados é derivado do modelo de domínio apresentado anteriormente.

### Identidade

Cada entidade possui uma chave artificial `id` para identificação única dos registros.

### Apagamento

Os registros poderão ser excluídos conforme as regras definidas na implementação. Nesta versão, não há necessidade de exclusão lógica prevista nos requisitos.

### Representação de tempo

As datas dos treinos serão armazenadas como informação de data, permitindo identificar quando cada sessão foi realizada e consultar o histórico.

### Armazenamento de arquivos

Não há armazenamento de arquivos previsto nesta versão do sistema.

## Comportamento

O fluxo principal considerado é o registro de um treino e o cálculo do seu volume.

Sequência do fluxo principal em `diagrams/sequencia-treino.mmd`.

1. O usuário inicia um novo treino.
2. O sistema apresenta o formulário de registro.
3. O usuário adiciona um ou mais exercícios.
4. O usuário informa as séries, repetições e cargas.
5. O usuário confirma o salvamento.
6. O sistema valida os dados informados.
7. O sistema registra o treino.
8. O sistema calcula o volume das séries registradas.
9. O sistema apresenta o resumo do treino.

### Diagrama de estados

Diagrama de estados em `diagrams/estados-treino.mmd`.

O objeto central considerado é o **Treino**.

Estados principais:

* **Em preenchimento:** o usuário iniciou o cadastro e ainda está adicionando informações.
* **Finalizado:** o treino foi salvo com sucesso e seus dados podem ser consultados.
* **Cancelado:** o usuário interrompeu o cadastro antes de finalizar.

Fluxo:

`Em preenchimento → Finalizado`

`Em preenchimento → Cancelado`

A modelagem dos estados reforça a necessidade de diferenciar um treino em preenchimento de um treino já registrado.

## Distribuição de responsabilidades

| Parte     | Sabe                            | Faz                                                                         |
| --------- | ------------------------------- | --------------------------------------------------------------------------- |
| Usuário   | Seus treinos, metas e registros | Cadastra treinos, informa séries, repetições e cargas e consulta seus dados |
| Treino    | Data, exercícios e volume       | Organiza os dados de uma sessão de treinamento                              |
| Exercício | Nome e séries realizadas        | Representa um exercício pertencente ao treino                               |
| Série     | Repetições e carga              | Armazena os dados utilizados para o cálculo do volume                       |
| Meta      | Tipo e objetivo diário          | Representa as metas de água e sono                                          |

## Decisões de projeto

| Id   | Decisão                                           | Motivo                                                                     | Consequência aceita                                       |
| ---- | ------------------------------------------------- | -------------------------------------------------------------------------- | --------------------------------------------------------- |
| D-01 | Separar Treino e Exercício                        | Um treino pode conter vários exercícios                                    | Maior quantidade de entidades no modelo                   |
| D-02 | Separar Exercício e Série                         | Um exercício pode possuir várias séries com diferentes repetições e cargas | Maior complexidade no modelo de dados                     |
| D-03 | Calcular o volume a partir das séries registradas | Permitir que o sistema faça o cálculo automaticamente                      | O sistema precisa aplicar uma regra de cálculo            |
| D-04 | Persistir os dados dos treinos                    | Permitir consulta posterior e acompanhamento da evolução                   | Necessidade de armazenamento dos registros                |
| D-05 | Não armazenar arquivos nesta versão               | Nenhum requisito atual exige imagens ou outros arquivos                    | O sistema não terá armazenamento de arquivos nesta versão |

## Protótipo

Protótipo navegável do fluxo principal em `prototipo/`.

O fluxo principal contempla o cadastro de um treino, a inclusão de exercícios, o registro de séries, repetições e cargas, o salvamento do treino e a visualização do volume calculado.

As telas de recusa devem contemplar situações em que o sistema não permite o avanço do fluxo, como a tentativa de salvar um treino sem informar dados obrigatórios.

## Conferência cruzada

A conferência cruzada deve verificar a correspondência entre o `REQUISITOS.md`, o modelo de domínio, o modelo de dados e os diagramas de comportamento.

Registro da conferência:

* Data: a preencher.
* Responsável pela conferência: a preencher.
* Correções realizadas: a preencher.

## Histórico de revisão

* 2026-09-17: primeira versão do `PROJETO.md`.
