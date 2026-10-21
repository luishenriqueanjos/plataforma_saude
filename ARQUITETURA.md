# Arquitetura

## Visão geral

Diagrama em `diagrams/arquitetura.mmd`.

O sistema adota uma arquitetura web cliente-servidor organizada como um **monólito modular** em Python (`main.py` com servidor HTTP e API JSON), com interface web no navegador (HTML/CSS/JS) e persistência relacional em banco de dados SQLite (`treinos.db`).

## Responsabilidades

| Parte    | Sabe                                      | Faz                                                                                     |
| -------- | ----------------------------------------- | --------------------------------------------------------------------------------------- |
| Frontend | Telas, estado do formulário em tela       | Apresenta os formulários, faz verificação rápida de apoio e consome a API via JSON      |
| Backend  | Regras de negócio (`RN-01`, `RN-02`)      | Valida os dados recebidos, calcula o volume do treino e coordena a gravação no banco    |
| Banco    | Esquema relacional e integridade dos dados| Guarda e recupera os registros de usuários, treinos, exercícios, séries e metas         |

## Onde cada parte roda

Diagrama em `diagrams/implantacao.mmd`.

Nesta fase do projeto (até a Review Parcial), o servidor Python e o banco SQLite executam no ambiente local da equipe (`localhost:5000`), sendo acessados pelo navegador.

## Contrato da API

Operações documentadas em `contrato/operacoes.md`, com exemplos de respostas JSON em `contrato/exemplos/`.

## Verificações

| Verificação                                      | Frontend                                      | Backend                                                  |
| ------------------------------------------------ | --------------------------------------------- | -------------------------------------------------------- |
| Data e nome do exercício informados              | Campo obrigatório no formulário               | Valida presença; se ausente, recusa com status `400`     |
| Todas as séries com repetições e carga $> 0$     | Alerta visual imediato na tela de erro        | Valida cada série; se incompleta, recusa com status `400`|
| Cálculo do volume total ($\sum \text{rep} \times \text{carga}$) | Exibe o valor retornado pela API | Calcula a regra `RN-01` antes de responder `201`         |

## Qualidades e custos

| Qualidade    | Requisito | Decisão                                                       | Custo aceito                                                  |
| ------------ | --------- | ------------------------------------------------------------- | ------------------------------------------------------------- |
| Privacidade  | `RNF-01`  | Operar apenas com usuário de teste fixo sem coletar dados civis | Sem login individual real nesta versão                        |
| Simplicidade | `CA-01.3` | Banco relacional embarcado (SQLite) em arquivo único          | Não suporta alta concorrência de múltiplos servidores         |

## Decisões

| Id   | Decisão                                                | Alternativa descartada           | Motivo                                                                                     | Consequência aceita                                              | Situação |
| ---- | ------------------------------------------------------ | -------------------------------- | ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------- | -------- |
| A-01 | Monólito modular em Python (`main.py`)                 | Microsserviços separados         | Equipe de 4 pessoas e escopo enxuto; o salvamento de treino e séries ocorre na mesma transação | Todo o sistema é iniciado e implantado em um único processo      | Aceita   |
| A-02 | Banco de dados SQLite (`treinos.db`)                   | PostgreSQL externo em nuvem      | Dispensa configuração de servidor externo e funciona direto após `git clone`               | O arquivo do banco é local em cada máquina de execução           | Aceita   |
| A-03 | Regra de cálculo de volume e validação no Backend      | Calcular apenas no JavaScript    | Garantir que nenhum treino inválido entre no banco mesmo se a requisição vier fora da tela | Toda confirmação de treino exige uma requisição HTTP ao servidor | Aceita   |
| A-04 | Comunicação por API REST JSON (`/api/treinos`)         | Renderizar toda página recarregando HTML | Permite manter o protótipo navegável fluido consumindo dados reais do servidor     | Necessidade de manter o contrato JSON sincronizado               | Aceita   |

## Pontos em aberto

- Autenticação e separação de contas de usuários reais: previsto para o Capítulo 13 (Segurança e Privacidade).
- Implantação em servidor de nuvem acessível externamente: previsto para o Capítulo 14 (Implantação e Operação).

## Histórico de revisão

- 2026-09-24: primeira versão do `ARQUITETURA.md` (Encontro 7).
