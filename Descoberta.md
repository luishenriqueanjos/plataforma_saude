# Descoberta do problema

## Problema

Manter hábitos saudáveis e acompanhar a evolução dos treinos pode ser difícil quando as informações são registradas de forma desorganizada ou em diferentes ferramentas.

No acompanhamento de hábitos, o usuário pode ter dificuldade para manter metas e visualizar sua evolução ao longo do tempo. Da mesma forma, praticantes de atividades físicas podem registrar exercícios, séries, repetições e cargas em anotações ou planilhas, dificultando a análise da progressão e do volume dos treinos.

Nosso projeto busca centralizar essas informações em um único sistema, permitindo o acompanhamento dos hábitos, das metas e da evolução dos treinos.

## Partes interessadas

| Parte                          | Categoria           | Interesse                                                                        | Poder |
| ------------------------------ | ------------------- | -------------------------------------------------------------------------------- | ----- |
| Praticante de atividade física | Usa e é afetado     | Registrar treinos, acompanhar cargas, repetições e evolução do desempenho        | Alto  |
| Academias                      | Oferece e utiliza   | Oferecer aos alunos uma ferramenta de acompanhamento de treinos e evolução       | Médio |
| Personal trainers              | Usa e é afetado     | Auxiliar no acompanhamento da evolução dos alunos                                | Médio |

## Usuários e Personas

*Nota da equipe: Como o contato formal e documentado com os usuários reais ainda não ocorreu até o presente marco, as personas abaixo foram construídas como hipóteses derivadas da definição de público-alvo. Cada traço precisará ser validado em entrevistas na próxima iteração.*

### Persona 1: Marcos, praticante de treinamento estruturado
- **Contexto:** Pratica musculação há dois anos, segue uma periodização de treinos em blocos e busca acompanhar a progressão de cargas[cite: 1]. [Fonte: Hipótese derivada do público-alvo; a verificar em entrevista].
- **Objetivo:** Registrar diariamente seus exercícios, séries, repetições e cargas de forma rápida para visualizar a evolução do volume de treino e performance ao longo do tempo[cite: 1]. [Fonte: Hipótese; a verificar em entrevista].
- **Dificuldade atual:** Atualmente usa o bloco de notas do celular ou planilhas genéricas, o que dificulta o cálculo automático de volume e o acompanhamento rápido da progressão[cite: 1]. [Fonte: Hipótese baseada na declaração de problema do sistema; a verificar com usuário].
- **Condição de uso:** Acessa a plataforma pelo celular de dentro da academia, muitas vezes entre as séries de exercícios, digitando com uma mão só e com suor. [Fonte: Suposição da equipe sobre o contexto físico de uso; a verificar].
- **O que ele não precisa:** Funcionalidades de rede social para compartilhar o treino com outros usuários ou dicas genéricas de exercícios básicos. [Fonte: Suposição da equipe para delimitar o escopo].

### Persona 2: Camila, iniciante na melhora de hábitos diários
- **Contexto:** Tem uma rotina de trabalho agitada e deseja começar a rastrear o consumo de água, a qualidade do sono e a alimentação básica para melhorar a saúde geral[cite: 1, 2]. [Fonte: Hipótese derivada do público-alvo; a verificar em entrevista].
- **Objetivo:** Cadastrar metas diárias simples (como beber 2L de água e dormir 8 horas) e receber lembretes consistentes para registrar seu cumprimento[cite: 1]. [Fonte: Hipótese; a verificar].
- **Dificuldade atual:** Esquece de anotar os hábitos no meio do expediente por falta de organização e acaba abandonando o acompanhamento após poucos dias[cite: 1]. [Fonte: Hipótese da declaração do problema; a verificar].
- **Condição de uso:** Acessa a plataforma rapidamente várias vezes ao dia (geralmente em pausas do trabalho), precisando de uma interface que exija no máximo dois cliques para confirmar um hábito. [Fonte: Suposição de usabilidade; a verificar em observação].
- **O que ela não precisa:** Cálculos complexos de estatística de progressão de cargas, planilhas de periodização esportiva ou gráficos de volume de treino[cite: 1]. [Fonte: Hipótese para separar perfis de uso].

### O que precisa ser verificado (Próximos Passos)
1. Conduzir entrevistas com pelo menos 2 praticantes de musculação para confirmar se a maior dificuldade atual é realmente a falta de cálculo de volume[cite: 1].
2. Observar uma pessoa tentando registrar o consumo de água durante o dia útil para validar a "Condição de uso" da Camila.
3. Confirmar se a preocupação com a privacidade dos dados de peso e sono realmente afeta a disposição do usuário em usar a plataforma (conforme risco mapeado no PROCESSO.md)[cite: 2].

## Necessidades levantadas

| Id | Necessidade                                    | Parte                         | Situação    |
| -- | ---------------------------------------------- | ----------------------------- | ----------- |
| N1 | Registrar hábitos saudáveis                    | Praticante de atividade física| Confirmada  |
| N2 | Definir e acompanhar metas                     | Praticante de atividade física| Confirmada  |
| N3 | Consultar histórico de hábitos                 | Praticante de atividade física| Confirmada  |
| N4 | Registrar treinos, séries, repetições e cargas | Praticante de atividade física| Confirmada  |
| N5 | Acompanhar a evolução do desempenho            | Praticante de atividade física| Confirmada  |
| N6 | Ter uma ferramenta para acompanhar os alunos   | Academia                      | A considerar|
| N7 | Acompanhar o progresso dos alunos              | Personal Trainer              | A considerar|

## Escopo

### Entra nesta versão

* Cadastro e acompanhamento de hábitos;
* Definição de metas diárias;
* Registro do cumprimento dos hábitos;
* Histórico dos hábitos;
* Cadastro de treinos e exercícios;
* Registro de séries, repetições e cargas;
* Cálculo do volume de treino;
* Visualização da evolução dos exercícios.

### Fora de escopo nesta versão

* Prescrição automática de treinos, pois exigiria regras específicas para diferentes perfis de usuários;
* Diagnóstico ou acompanhamento médico, pois a plataforma não tem como objetivo substituir profissionais de saúde;
* Integração com relógios ou outros dispositivos, pois aumentaria a complexidade da implementação;
* Planos alimentares personalizados, pois estão fora do objetivo principal da plataforma;
* Integração com academias ou outros serviços externos, pois não é necessária para o funcionamento da versão inicial.

## Produto mínimo viável

O MVP será definido como uma fatia vertical do sistema, contemplando o fluxo completo de acompanhamento de hábitos saudáveis:

1. Usuário cadastra um hábito;
2. Define uma meta para o hábito;
3. Registra a realização do hábito;
4. Consulta seu histórico e progresso.

Essa fatia permite validar o funcionamento básico do sistema desde o cadastro até o acompanhamento da evolução do usuário.

## Histórico de revisão

* 2026-09-02: versão inicial
