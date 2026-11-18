# Guia de Contribuição

Para manter o projeto organizado e com qualidade verificada, siga as regras abaixo:

## 1. Ramificação (Branches)
- Crie uma branch própria a partir da `main` para cada tarefa:
  `feature/nome-da-funcionalidade` ou `fix/nome-da-correcao`

## 2. Commits
- Escreva mensagens de commit claras no tempo presente, citando o item ou história relacionada (ex: `feat: implementa cadastro de metas de agua e sono (HU-03)`).

## 3. Pull Requests (PR) e Verificação Automática
- Nenhum código entra direto na `main`.
- Abra um Pull Request utilizando o modelo em `.github/pull_request_template.md` e vincule ao item do backlog (`Closes #...`).
- **Aprovação obrigatória:** Todo PR deve ser revisado e aprovado por pelo menos 1 integrante da equipe que não seja o autor antes do merge.
- **Verificação Contínua (Cap. 12):** A integração ao `main` exige que o workflow `.github/workflows/verificacao.yml` (`ruff format --check .`, `ruff check .` e `pytest`) esteja **verde**.

## 4. Lista de Verificação de Revisão de Código (Cap. 10)

Durante a revisão, o revisor avalia o código pelas lentes abaixo e classifica seus comentários em **`[Bloqueia]`**, **`[Sugere]`**, **`[Pergunta]`** ou **`[Elogia]`**:

| Lente | Pergunta de verificação | Origem da regra |
| :--- | :--- | :--- |
| **Item** | O pull request cumpre os critérios de aceitação do item, e só eles? | Capítulo 5 |
| **Tamanho** | É apenas um item de backlog por pull request? | Capítulo 2 |
| **Projeto** | A regra de negócio (`RN-01`, `RN-02`) fica no backend e respeita as camadas? | Capítulos 6 e 7 |
| **Contrato** | A mudança respeita `contrato/operacoes.md`, ou atualizou o contrato no mesmo PR? | Capítulo 7 |
| **Legibilidade** | Os nomes usam o glossário do `Requisitos.md` e cada função se entende na primeira leitura? | Capítulo 6 |
| **Multiplicidade** | O código trata zero, uma e várias séries/metas sem quebrar o cálculo ou lançar erro de divisão por zero? *(Pergunta adicionada a partir do risco `R1`)* | Capítulo 6 e 10 |
| **Testes** | Existe teste automatizado (`pytest`) com `# Preparar`, `# Agir` e `# Conferir` tirado do critério de aceitação? | Capítulo 12 |
| **Segurança e dados** | Nenhum segredo no repositório e nenhum dado pessoal civil/clínico real em registro ou exemplo? | Capítulos 2 e 13 |
