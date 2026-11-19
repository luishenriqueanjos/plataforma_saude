# Relatório Técnico — Semana 01 (Arthur Sidarta)

- **Responsável pela trilha:** Arthur Sidarta Fernandes de Souza Lima (`@Sidrata`)
- **Tarefa do Quadro:** `T-ARTHUR-S01` — Planejamento Geral, Quadro de Acompanhamento e Suíte de Testes Automatizados do Fluxo Principal (`HU-01`, `HU-02`, `RNF-01`)
- **Branch:** `feature/arthur-semana-01-planejamento-e-testes-base`
- **Pull Request:** [PR #15](https://github.com/luishenriqueanjos/plataforma_saude/pull/15)
- **Declaração de uso de IA:** Este artefato e o código-fonte associado foram desenvolvidos com assistência de agente autônomo de IA (Antigravity / Gemini), sob supervisão e revisão da trilha de Banco de Dados, Backend, API e Testes atribuída a Arthur Sidarta.

---

## 1. O que foi desenvolvido

1. **Planejamento Completo do Projeto (`PLANEJAMENTO_GERAL.md`):**
   - Diagnóstico completo do repositório após a Review Parcial (Encontro 9), mapeando o que já foi integrado na `main` (PRs `#8` a `#13`), o que está em revisão para `HU-03` (PR `#14`) e todas as etapas restantes até a Review Final (Encontro 16), divididas em 6 semanas e respeitando as responsabilidades de Arthur, Samuel, Luis e Ayrton.
2. **Quadro Semanal de Tarefas (`QUADRO.md`):**
   - Rastreamento estruturado por semana com ID da tarefa, responsável, critérios de aceitação verificáveis, status, prazos e links para os Pull Requests.
3. **Suíte de Testes Automatizados de Banco de Dados e API (`tests/test_backend_treinos.py`):**
   - Implementação de 8 testes automatizados (unidade e integração HTTP) utilizando exclusivamente a biblioteca padrão do Python (`unittest`, `tempfile`, `sqlite3`, `http.server` e `urllib.request`), em conformidade com o `requirements.txt` do projeto.

---

## 2. Qual problema foi resolvido

Até a Review Parcial (`PR #13`), a validação do fluxo principal (`HU-01` e `HU-02`) dependia exclusivamente de testes manuais via navegador seguindo o roteiro do `ITERACOES.md`. Qualquer alteração futura no esquema SQLite ou nas rotas de `main.py` corria o risco de introduzir regressões silenciosas no cálculo de volume (`RN-01`), na recusa de dados incompletos (`RN-02`, `CA-01.2`, `CA-02.2`) ou na restrição de privacidade (`RNF-01`).

Além disso, faltava um artefato centralizado que conectasse o backlog restante (`HU-03` e `HU-04`) às entregas semanais de cada integrante até a Review Final.

---

## 3. Como o código funciona (Guia para apresentação ao professor)

O arquivo `tests/test_backend_treinos.py` está dividido em duas classes de teste baseadas em `unittest.TestCase`:

1. **`TestBancoDadosETreinos` (Testes de Persistência e Regras de Negócio):**
   - No método `setUp()`, cria-se um diretório temporário isolado (`tempfile.TemporaryDirectory()`) e redireciona-se a variável global `main.DB_PATH` para um arquivo SQLite temporário (`test_treinos.db`). Assim, os testes nunca alteram nem apagam o banco real `treinos.db` da aplicação.
   - Em seguida, chama-se `main.init_db(reset=True)`, que executa o `CREATE TABLE IF NOT EXISTS` para `USUARIO`, `TREINO`, `EXERCICIO`, `SERIE` e `META`, e insere o usuário de teste (`id = 1`) e o treino inicial (`Supino reto`, 3 séries de 10 × 20 kg = 600 kg).
   - Os métodos de teste inspecionam os metadados do SQLite via `sqlite_master` e `PRAGMA table_info(USUARIO)` (comprovando o `RNF-01`, isto é, que nenhuma coluna sensível como CPF, nome ou e-mail existe na tabela `USUARIO`), testam `main.calcular_volume()`, `main.salvar_novo_treino()` e `main.obter_treinos()`.
2. **`TestIntegracaoAPIHTTP` (Testes de Integração da API REST):**
   - No `setUp()`, instancia um servidor `HTTPServer(("127.0.0.1", 0), main.PlataformaHandler)` passando a porta `0`, o que faz o sistema operacional alocar automaticamente uma porta livre efêmera, rodando o servidor em uma `threading.Thread` em segundo plano (`daemon=True`).
   - Os testes fazem requisições HTTP reais com `urllib.request.urlopen` para `GET /`, `GET /api/treinos` e `POST /api/treinos`, verificando tanto o status `201 Created` (com retorno JSON do volume calculado) quanto o erro `400 Bad Request` quando uma série é enviada sem carga.
   - No `tearDown()`, o servidor é encerrado (`server.shutdown()` e `server.server_close()`) e o diretório temporário é removido.

---

## 4. Quais arquivos foram criados/modificados

| Arquivo | Tipo de Alteração | Descrição |
| :--- | :--- | :--- |
| `PLANEJAMENTO_GERAL.md` | Novo arquivo | Diagnóstico do repositório, matriz de dependências e cronograma das Semanas 01 a 06. |
| `QUADRO.md` | Novo arquivo | Quadro semanal de tarefas, critérios de aceitação, status e links de entregas. |
| `tests/test_backend_treinos.py` | Novo arquivo | Suíte de testes automatizados de banco de dados SQLite, regras de negócio e rotas HTTP. |
| `docs/relatorios/semana-01-arthur.md` | Novo arquivo | Relatório técnico detalhado da entrega da Semana 01. |

*(Nenhum arquivo modificado pelo PR `#14` em aberto foi alterado nesta branch, evitando conflitos de merge).*

---

## 5. Conceitos técnicos utilizados

- **Isolamento de Testes com Banco Efêmero (`tempfile` + Monkey Patching de configuração):** Redirecionamento de `main.DB_PATH` durante o ciclo de vida `setUp`/`tearDown` para garantir testes determinísticos e idempotentes.
- **Introspecção de Esquema SQLite (`sqlite_master` e `PRAGMA table_info`):** Consulta direta ao catálogo interno do SQLite para verificar automaticamente o requisito não funcional de privacidade (`RNF-01`).
- **Servidor Efêmero em Thread (`HTTPServer` na porta `0`):** Alocação dinâmica de porta TCP pelo sistema operacional para testar o protocolo HTTP e a serialização JSON de ponta a ponta sem conflitar com a porta `5000`.

---

## 6. Testes executados e resultados obtidos

Comando executado na raiz do projeto:

```bash
python -m unittest discover -s tests -v
```

Resultado obtido:

```text
test_calculo_volume_rn01_ca02_1 (test_backend_treinos.TestBancoDadosETreinos.test_calculo_volume_rn01_ca02_1)
Valida a regra RN-01: soma do produto (repeticoes * carga) de todas as series. ... ok
test_esquema_banco_e_privacidade_rnf01 (test_backend_treinos.TestBancoDadosETreinos.test_esquema_banco_e_privacidade_rnf01)
Verifica criacao das tabelas do modelo de dados e conformidade com RNF-01 (sem dados civis sensiveis). ... ok
test_recusa_dados_incompletos_ca01_2 (test_backend_treinos.TestBancoDadosETreinos.test_recusa_dados_incompletos_ca01_2)
Valida recusa (HTTP 400) quando data, exercicio ou carga estao ausentes. ... ok
test_recusa_valores_menores_ou_iguais_a_zero_ca02_2_rn02 (test_backend_treinos.TestBancoDadosETreinos.test_recusa_valores_menores_ou_iguais_a_zero_ca02_2_rn02)
Valida recusa (HTTP 400) quando repeticoes ou carga sao menores ou iguais a zero. ... ok
test_salvar_novo_treino_caminho_principal_ca01_1_ca01_3 (test_backend_treinos.TestBancoDadosETreinos.test_salvar_novo_treino_caminho_principal_ca01_1_ca01_3)
Valida o salvamento de um novo treino valido e sua persistencia na listagem. ... ok
test_seed_inicial_e_listagem_ca01_3_ca02_3 (test_backend_treinos.TestBancoDadosETreinos.test_seed_inicial_e_listagem_ca01_3_ca02_3)
Verifica se o treino inicial de demonstracao e persistido e retornado com volume de 600 kg. ... ok
test_get_e_post_api_treinos (test_backend_treinos.TestIntegracaoAPIHTTP.test_get_e_post_api_treinos) ... ok
test_get_pagina_inicial_html (test_backend_treinos.TestIntegracaoAPIHTTP.test_get_pagina_inicial_html) ... ok

----------------------------------------------------------------------
Ran 8 tests in 0.222s

OK
```
