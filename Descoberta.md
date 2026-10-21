# Descoberta do problema

## Problema

Manter hábitos saudáveis e acompanhar a evolução dos treinos pode ser difícil quando as informações são registradas de forma desorganizada ou em diferentes ferramentas.

No acompanhamento de hábitos, o usuário pode ter dificuldade para manter metas e visualizar sua evolução ao longo do tempo. Da mesma forma, praticantes de atividades físicas costumam registrar exercícios, séries, repetições e cargas em anotações soltas ou planilhas genéricas, dificultando a análise da progressão e o cálculo do volume dos treinos.

Nosso projeto busca centralizar essas informações em um único sistema, permitindo o acompanhamento dos treinos, do volume de carga e das metas diárias de hábitos.

## Partes interessadas

| Parte                          | Categoria           | Interesse                                                                 | Poder | Contato                      |
| ------------------------------ | ------------------- | ------------------------------------------------------------------------- | ----- | ---------------------------- |
| Praticante de atividade física | Usa e é afetado     | Registrar treinos, acompanhar cargas, repetições e evolução do desempenho | Alto  | Colegas da turma praticantes |
| Academias                      | Oferece e utiliza   | Oferecer aos alunos uma ferramenta de acompanhamento de treinos           | Médio | Academias locais (Palmas)    |
| Personal trainers              | Usa e é afetado     | Auxiliar no acompanhamento da evolução dos alunos                         | Médio | Instrutores de academia      |

## Usuários e Personas

*Nota da equipe: Como o contato formal e documentado com usuários externos ainda estava em andamento no início do projeto, as personas abaixo foram construídas inicialmente como hipóteses derivadas do público-alvo e validadas com colegas praticantes de musculação.*

### Persona 1: Marcos, praticante de treinamento estruturado
- **Contexto:** Pratica musculação há dois anos, segue uma divisão de treinos na semana e busca acompanhar a progressão de cargas. [Fonte: D1 e conversa com colegas praticantes].
- **Objetivo:** Registrar diariamente seus exercícios, séries, repetições e cargas de forma rápida para visualizar a evolução do volume de treino ao longo do tempo. [Fonte: D1].
- **Dificuldade atual:** Atualmente usa o bloco de notas do celular ou planilhas genéricas, o que dificulta o cálculo automático de volume e o acompanhamento rápido da progressão. [Fonte: D1].
- **Condição de uso:** Acessa a plataforma pelo celular ou navegador logo após as séries de exercícios, precisando de um formulário direto e sem campos desnecessários. [Fonte: Suposição validada no protótipo V1].
- **O que ele não precisa:** Funcionalidades de rede social para compartilhar o treino com outros usuários ou dicas genéricas de exercícios básicos. [Fonte: Delimitação de escopo da equipe].

### Persona 2: Camila, iniciante na melhora de hábitos diários
- **Contexto:** Tem uma rotina de estudos e trabalho agitada e deseja começar a rastrear o consumo de água e horas de sono para melhorar a saúde geral. [Fonte: Hipótese derivada do público-alvo].
- **Objetivo:** Cadastrar metas diárias simples (como beber 2L de água e dormir 8 horas) e registrar seu cumprimento no dia a dia. [Fonte: Hipótese; a verificar].
- **Dificuldade atual:** Esquece de anotar os hábitos no meio do expediente por falta de organização e acaba abandonando o acompanhamento após poucos dias. [Fonte: Hipótese da declaração do problema].
- **Condição de uso:** Acessa a plataforma rapidamente durante pausas do dia, precisando de poucos cliques para registrar o progresso da meta. [Fonte: Suposição de usabilidade].
- **O que ela não precisa:** Planilhas avançadas de periodização esportiva para atletas competitivos. [Fonte: Hipótese para separar perfis de uso].

## Fontes consultadas

- **D1:** Proposta inicial do projeto (`README.md`) e exemplos de anotações de treino em bloco de notas de integrantes e colegas da turma (2026-08-27).
- **V1:** Sessão de validação do protótipo de baixa fidelidade com usuário do perfil Marcos (2026-09-03, 20 min).

## Necessidades levantadas

| Id | Necessidade                                    | Parte                          | Fonte   | Situação     |
| -- | ---------------------------------------------- | ------------------------------ | ------- | ------------ |
| N1 | Registrar treinos, séries, repetições e cargas | Praticante de atividade física | D1, V1  | Confirmada   |
| N2 | Calcular o volume de treino automaticamente    | Praticante de atividade física | D1, V1  | Confirmada   |
| N3 | Definir e acompanhar metas de água e sono      | Praticante de atividade física | D1      | Confirmada   |
| N4 | Consultar histórico e evolução de cargas       | Praticante de atividade física | D1      | Confirmada   |
| N5 | Ter uma ferramenta para acompanhar os alunos   | Academia                       | Equipe  | A considerar |
| N6 | Acompanhar o progresso dos alunos              | Personal Trainer               | Equipe  | A considerar |

## Cenário atual e cenário pretendido

- **Cenário atual:** O praticante abre o bloco de notas do celular durante o treino, digita o nome do exercício, as séries e os pesos em texto livre, e precisa multiplicar e somar manualmente caso queira saber o volume total levantado na sessão.
- **Cenário pretendido:** O praticante abre a aplicação, seleciona o exercício, informa as repetições e cargas de cada série e salva o treino; o sistema valida se nenhuma carga ficou em branco, grava a sessão no banco de dados e exibe imediatamente o volume total calculado.

## Escopo

### Entra nesta versão

* Cadastro de treinos e exercícios;
* Registro de séries, repetições e cargas;
* Cálculo automático do volume de treino;
* Consulta ao histórico de treinos registrados;
* Cadastro e acompanhamento de metas diárias de hábitos (água e sono);
* Visualização da evolução dos exercícios.

### Fora de escopo nesta versão

* Prescrição automática de treinos, pois exigiria regras específicas de educação física para diferentes perfis;
* Diagnóstico ou acompanhamento médico, pois a plataforma não substitui profissionais de saúde;
* Integração com relógios inteligentes (smartwatches), pois aumentaria a complexidade técnica;
* Planos alimentares personalizados, pois fogem do objetivo central do projeto;
* Painel multiusuário para academias e personal trainers (N5 e N6 ficam fora desta versão para focar na experiência do praticante).

## Produto mínimo viável

O MVP foi definido como uma fatia vertical completa focada no fluxo principal de registro e cálculo de treino (`HU-01` e `HU-02`):

1. Usuário inicia um novo treino informando a data e o exercício;
2. Registra as séries com suas repetições e cargas (com validação de dados obrigatórios);
3. O sistema salva o treino no banco de dados e calcula automaticamente o volume total ($\text{repetições} \times \text{carga}$);
4. Usuário visualiza o resumo e o histórico de treinos salvos.

Essa fatia atravessa interface, regra de negócio no servidor e persistência no banco, cabendo em **2 iterações de duas semanas** até a Review Parcial (Encontro 9).

## Riscos iniciais

| Id | Risco                                                                 | Prob. | Impacto | Resposta | Ação e responsável                                                       |
| -- | --------------------------------------------------------------------- | ----- | ------- | -------- | ------------------------------------------------------------------------ |
| R1 | Usuário esquecer de preencher carga em uma série e distorcer o volume | Alta  | Alto    | Mitigar  | Validar todas as séries no backend antes de salvar (Arthur / Samuel)     |
| R2 | Escopo grande (hábitos + treinos + gráficos) atrasar a entrega        | Média | Alto    | Mitigar  | Priorizar o fluxo de treino e volume no MVP até o encontro 9 (Luis)      |
| R3 | Coleta de dados pessoais de saúde sem controle de privacidade         | Baixa | Médio   | Mitigar  | Revisar checklist de dados e usar usuário de teste na review (Ayrton)    |

## Histórico de revisão

* 2026-09-02: versão inicial.
* 2026-09-17: alinhamento do MVP com o fluxo principal de treinos e inclusão da tabela de riscos.
