# Estratégia e Casos de Teste (`TESTES.md`)

## 1. Estratégia de Teste por Nível (Cap. 11)

| Nível | O que se testa | Quem escreve | Quando |
| :--- | :--- | :--- | :--- |
| **Unidade** | Regra `calcular_volume` (`RN-01`) e validações de entradas (`RN-02`), sem servidor HTTP | Quem implementou a função (Arthur) | Junto com o código |
| **Integração** | Contrato das rotas `POST /api/treinos`, `GET /api/treinos` e `/api/metas` com banco SQLite de teste isolado | Dupla backend e qualidade (Arthur e Samuel) | Ao fechar o contrato da API |
| **Sistema** | Fluxo completo no navegador (`http://localhost:5000`), do formulário ao resumo ou tela de recusa, na build identificada | Quem não implementou a tela (Luis Henrique) | Antes de cada marco |
| **Aceitação** | Critérios de aceitação de `HU-01`, `HU-02` e `HU-03`, em conjunto com o usuário/professor | A equipe e o avaliador | Ao fim da iteração / Review |

### Ambiente, Identificação da Build e Critério de Saída
- **Ambiente de teste:** Python 3.12+, banco de dados SQLite isolado em arquivo temporário durante a execução do `pytest` (evitando poluir o `treinos.db` local) e navegador Chrome/Edge para os testes manuais de sistema.
- **Identificação da build testada:** `v0.2.0` (commit `a374913` — branch `feature/metas-agua-sono`).
- **Critério de saída:** Suíte automatizada (`pytest`) e verificador de estilo (`ruff`) verdes no GitHub Actions, casos de sistema executados na build identificada e nenhum defeito *major* aberto.

---

## 2. Omissões Deliberadas (Cap. 11)

| Fica de fora | Motivo | Risco aceito |
| :--- | :--- | :--- |
| Navegadores além das versões atuais do Chrome e Edge | Equipe e usuários dos testes utilizam apenas esses navegadores | Layout mobile simulado (`.app`) pode apresentar diferenças visuais em navegadores antigos |
| Testes de carga e concorrência simultânea no SQLite | Decisão arquitetural `A-02` adotou SQLite embarcado para escopo acadêmico local | Múltiplas gravações simultâneas em produção poderiam gerar bloqueio de arquivo (*database locked*) |
| Testes de penetração e resistência a ataques | Testes funcionais não demonstram segurança contra intrusão; autenticação fica para o Cap. 13 | Acesso local restrito a `127.0.0.1` e uso exclusivo de usuário de teste (`id = 1`) |

---

## 3. Partições de Equivalência e Valores Limite

Para os campos de **Repetições**, **Carga (kg)** (`RN-02`) e **Metas de Água/Sono** (`CA-03.3`):

- **Repetições (inteiro):**
  - Partição inválida (vazio/não numérico): `""`, `null`, `"abc"`
  - Partição inválida ($\le 0$): `..., -5, -1, 0`
  - Partição válida ($\ge 1$): `1, 10, 15, ...`
  - **Valores limite testados:** `0` (inválido — recusa `400`) e `1` (válido — aceita `201`).
- **Carga em kg (decimal):**
  - Partição inválida ($\le 0$): `-10.0`, `0.0`
  - Partição válida ($> 0$): `0.5`, `20.0`, `100.0`
  - **Valores limite testados:** `0.0` (inválido — recusa `400`) e `0.5` (válido — aceita `201`).
- **Meta de Água em ml e Sono em horas:**
  - Partição inválida ($\le 0$ ou ausente): `null`, `-250`, `0`
  - Partição válida ($> 0$): `1`, `2000` (água), `8` (sono)
  - **Valores limite testados:** `0` (inválido — recusa `400`) e `1` (válido — aceita `201`).

---

## 4. Casos de Teste Derivados dos Critérios (Cap. 11)

| ID | Critério | Preparo (*Dado*) | Passos (*Quando*) | Resultado esperado (*Então*) | Status na Build `v0.2.0` |
| :--- | :--- | :--- | :--- | :--- | :---: |
| `TC-01.1` | `CA-01.1`, `CA-02.1` | Banco inicializado e usuário na tela/rota de novo treino | Enviar treino `"Supino reto"` em `"2026-10-15"` com 3 séries de `10` repetições e `20` kg | Retorna `201 Created`, grava no banco e apresenta `volume_total = 600.0` e `total_series = 3` | **Aprovado** |
| `TC-01.2` | `CA-01.2` | Usuário preenchendo treino com 3 séries | Tentar salvar deixando a carga da 3ª série vazia (`""` ou `null`) | Retorna `400 Bad Request` com erro `"Dados incompletos."` e não grava no banco | **Aprovado** |
| `TC-01.3` | `CA-01.3`, `CA-02.3` | Treino de `"Supino reto"` (`600 kg`) previamente salvo no banco | Consultar `GET /api/treinos` ou recarregar a tela inicial | Lista contém o treino com data `"2026-10-15"`, `"Supino reto"` e `volume_total = 600.0` | **Aprovado** |
| `TC-02.1` | `CA-02.2` | Valor limite inválido na série (`repeticoes = 0` ou `carga = 0`) | Enviar `POST /api/treinos` com `carga = 0` ou `-5` | Retorna `400 Bad Request` com erro `"Dados inválidos."` | **Aprovado** |
| `TC-02.2` | `CA-02.1` | Valor limite mínimo válido (`1` repetição com `0.5` kg) | Calcular volume e enviar `POST /api/treinos` | Retorna `201 Created` com `volume_total = 0.5` | **Aprovado** |
| `TC-02.4` | `HU-01` | Exercício de peso corporal (ex: barra fixa sem peso adicional, `carga = 0`) | Tentar registrar série com `carga = 0` | **Bloqueado** pela pergunta em aberto n.º 4 da Inspeção no `Requisitos.md` | **Bloqueado** |
| `TC-03.1` | `CA-03.1` | Usuário configurando metas diárias | Enviar `POST /api/metas` com `agua_ml = 2000` e `sono_horas = 8` | Retorna `201 Created` com metas salvas e `progresso_atual = 0.0` (`percentual = 0`) | **Aprovado** |
| `TC-03.2` | `CA-03.2` | Meta de água de `2000 ml` cadastrada com progresso `0` | Enviar `POST /api/metas/progresso` com `tipo = "agua"` e `quantidade = 250` | Retorna `200 OK`, atualiza `progresso_atual` para `250.0` e `percentual` para `12` / `13%` | **Aprovado** |
| `TC-03.3` | `CA-03.3` | Valor limite inválido na meta (`agua_ml = 0` ou `-100`) | Enviar `POST /api/metas` com valor $\le 0$ | Retorna `400 Bad Request` com erro `"Meta inválida."` | **Aprovado** |

---

## 5. Automação e Integração Contínua (Cap. 12)

### Execução
- **Suíte automatizada:** `pytest` (na raiz do repositório).
- **Verificador de estilo e formatação:** `ruff format --check .` e `ruff check .`.
- **Cobertura:** `pytest --cov=main --cov-report=term-missing`.
- **Integração contínua:** `.github/workflows/verificacao.yml`, executando a cada Pull Request e a cada push na `main`.

### Casos e onde são verificados

| ID | Critério | Verificado por |
| :--- | :--- | :--- |
| `TC-01.1` | `CA-01.1`, `CA-02.1` | **Unidade:** `tests/test_unidade.py::test_calcula_volume_tres_series_iguais`<br>**Integração:** `tests/test_api_treinos.py::test_salvar_novo_treino_valido_respeita_contrato_201`<br>**Sistema (manual):** Passo 2 do roteiro na build `v0.2.0` |
| `TC-01.2` | `CA-01.2` | **Integração:** `tests/test_api_treinos.py::test_recusa_treino_com_carga_ausente_retorna_400_contrato`<br>**Sistema (manual):** Tela de alerta "Dados incompletos" |
| `TC-01.3` | `CA-01.3`, `CA-02.3` | **Integração:** `tests/test_api_treinos.py::test_persistencia_treino_listado_no_historico` |
| `TC-02.1` | `CA-02.2` | **Integração (Valores Limite):** `tests/test_api_treinos.py::test_recusa_valores_limite_zero_ou_negativo` |
| `TC-02.2` | `CA-02.1` | **Unidade (Valor Limite):** `tests/test_unidade.py::test_calcula_volume_valor_limite_minimo` |
| `TC-03.1` | `CA-03.1` | **Integração:** `tests/test_api_treinos.py::test_cadastrar_metas_diarias_agua_e_sono_inicia_zerado` |
| `TC-03.2` | `CA-03.2` | **Integração:** `tests/test_api_treinos.py::test_atualizar_progresso_meta_agua_calcula_percentual` |
| `TC-03.3` | `CA-03.3` | **Integração:** `tests/test_api_treinos.py::test_recusa_meta_invalida_zero_ou_negativa` |

### Fora da automação
- **RNF-01 (Privacidade):** Inspeção manual do esquema `diagrams/dados.mmd` e das tabelas no `main.py` garantindo ausência de CPF/dados civis.
- **Teste de utilidade (`V2`):** Observação manual presencial do uso da interface em `prototipo/index.html`.
- **Renderização visual das barras de progresso CSS:** Verificada manualmente no navegador.

### Leitura do Relatório de Cobertura
- As funções de regra de negócio e persistência (`init_db`, `calcular_volume`, `obter_treinos`, `salvar_novo_treino`, `obter_metas`, `salvar_metas`, `registrar_progresso_meta`) são integralmente exercitadas pelos testes automatizados.
- As linhas listadas na coluna `Missing` do `main.py` referem-se apenas ao bloco `if __name__ == "__main__":` e ao loop de socket do `HTTPServer`, que sobem o servidor interativo de linha de comando e são verificados no teste de sistema manual.
