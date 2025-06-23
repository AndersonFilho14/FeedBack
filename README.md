# Sistema de Feedback

Este sistema busca resolver a **falta de acompanhamento visual e detalhado do desempenho dos alunos por sala de aula**. Atualmente, é desafiador identificar proativamente alunos com melhores e piores desempenhos, bem como realizar análises agregadas por turma e escola. Nosso objetivo é possibilitar a visualização das melhores turmas, associadas aos seus respectivos professores, e também comparar o desempenho entre as diferentes escolas.

---

## Estrutura do Banco de Dados

A criação e as interações com o banco de dados são gerenciadas em `.\FeedBack\src\infra\db\settings\connection.py` utilizando **SQLAlchemy ORM**.


---

## Política de Branches

**Somente tarefas concluídas devem ser mergeadas na branch `main`.**

---

## Como Rodar

Siga os passos abaixo para configurar e executar o projeto:

1.  **Instale o `uv`:**
    ```bash
    pip install uv
    ```

2.  **Clone o projeto:**
    ```bash
    git clone `https://github.com/AndersonFilho14/FeedBack.git`
    cd `FeedBack` # Navegue até o diretório do seu projeto
    ```

3.  **Sincronize as dependências:**
    Use o `uv` para instalar as dependências do projeto no seu ambiente virtual:
    ```bash
    uv sync
    ```

4.  **Navegue até a pasta `src`:**
    ```bash
    cd .\src\
    ```

5.  **Inicialize e popule o banco de dados:**
    Execute o script para alimentar o banco de dados com os dados iniciais:
    ```bash
    uv run .\alimentar_tabela.py
    ```
    Seu banco de dados agora está populado e pronto para requisições relacionadas a Professor, Escola e Município.

6.  **Inicie a aplicação:**
    ```bash
    uv run .\main.py
    ```

---

## Rotas

### Autenticação

**Endpoint:** `/acesso/<string:user_name>/<string:passworld>`

- Credenciais para Teste:
    * **Usuários aceitos:** `['prof_alfa', 'escola_alfa', 'municipio_alfa']`
    * **Senha aceita:** `senha123`

    **Respostas:**
    * **Sucesso:** Objeto JSON contendo `id_user`,`nome`, `cargo` e `token`.
    * **Falha (Usuário Não Encontrado):** "User não encontrado"
