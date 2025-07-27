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

## **Rotas da API**

A API oferece os seguintes endpoints para interação com o sistema:

### **1. Autenticação de Usuário (Login)**

* **Endpoint:** `/acesso/<string:user_name>/<string:passworld>`
* **Método:** `GET`
* **Descrição:** Realiza o login do usuário (professor, escola ou município) e retorna suas informações e um token de acesso.

    * **Credenciais de Teste:**
        * **Usuários Aceitos:** `['prof_alfa', 'escola_alfa', 'municipio_alfa']`
        * **Senha Aceita:** `senha123`

    * **Exemplo de Requisição (com `curl`):**
        ```bash
        curl [http://127.0.0.1:5000/acesso/prof_alfa/senha123](http://127.0.0.1:5000/acesso/prof_alfa/senha123)
        ```

    * **Respostas:**
        * **Sucesso (JSON):** Retorna um objeto JSON contendo `id_user`, `nome`, `cargo` e `token`.
            ```json
            {
              "cargo": "Professor",
              "id_user": 1,
              "nome": "Professor Alfa",
              "token": "your_auth_token_here"
            }
            ```
        * **Falha (Texto Simples):** "User não encontrado"

### **2. Visualizar Alunos Vinculados ao Professor**

* **Endpoint:** `/professor/visualizar_alunos/<string:id_professor>`
* **Método:** `GET`
* **Descrição:** Retorna uma lista de todos os alunos associados a um determinado professor.

    * **Exemplo de Requisição (com `curl`):**
        ```bash
        curl [http://127.0.0.1:5000/professor/visualizar_alunos/ID_DO_PROFESSOR](http://127.0.0.1:5000/professor/visualizar_alunos/ID_DO_PROFESSOR)
        ```
        (Substitua `ID_DO_PROFESSOR` pelo ID obtido no login).

### **3. Atualizar Quantidade de Faltas de um Aluno**

* **Endpoint:** `/professor/atualizar_quantidade_de_faltas_para_aluno/<string:id_professor>/<string:id_aluno>/<string:faltas>`
* **Método:** `GET` (Atualizar para ser um `POST` ou `PUT`)
* **Descrição:** Atualiza o número de faltas para um aluno específico, associado a um professor.

    * **Exemplo de Requisição (com `curl`):**
        ```bash
        curl [http://127.0.0.1:5000/professor/atualizar_quantidade_de_faltas_para_aluno/1/1/1
        ```
        (Substitua os placeholders pelos valores corretos).


### **4. Consultar Disciplinas e Matérias do Professor**

* **Endpoint:** `/materia_e_disciplina_que_o_professor_ensina/<int:id_professor>`
* **Método:** `GET`
* **Descrição:** Retorna uma estrutura aninhada com todas as disciplinas e matérias que um professor específico leciona.

* **Exemplo de Requisição (com `curl`):**
    ```bash
    curl [http://127.0.0.1:5000/materia_e_disciplina_que_o_professor_ensina/1](http://127.0.0.1:5000/materia_e_disciplina_que_o_professor_ensina/1)
    ```

* **Respostas:**
    * **Sucesso (JSON):** Retorna um objeto onde as chaves são os nomes das disciplinas.
        ```json
        {
            "Português": {
                "id_disciplina": 1,
                "materias": [
                    {
                        "id_materia": 1,
                        "nome_materia": "Gramática"
                    }
                ]
            },
            "Matemática": {
                "id_disciplina": 2,
                "materias": [
                    {
                        "id_materia": 3,
                        "nome_materia": "Álgebra"
                    }
                ]
            }
        }
        ```
    * **Falha:** Retorna um objeto JSON vazio `{}` se o professor não for encontrado.

### **5. Adicionar Nota de Avaliação a um Aluno**

* **Endpoint:** `/professor/adicionar_nota`
* **Método:** `POST`
* **Descrição:** Permite que um professor adicione uma nova nota de avaliação para um aluno. Os dados devem ser enviados no corpo (body) da requisição em formato JSON.

* **Corpo da Requisição (JSON):**
    ```json
    {
        "id_professor": 1,
        "id_aluno": 101,
        "id_materia": 3,
        "id_disciplina": 2,
        "tipo_avaliacao": "Prova Bimestral",
        "nota": 8.5
    }
    ```

* **Exemplo de Requisição (com `curl`):**
    ```bash
    curl -X POST -H "Content-Type: application/json" \
    -d '{ "id_professor": 1, "id_aluno": 101, "id_materia": 3, "id_disciplina": 2, "tipo_avaliacao": "Prova Bimestral", "nota": 8.5 }' \
    [http://127.0.0.1:5000/professor/adicionar_nota](http://127.0.0.1:5000/professor/adicionar_nota)
    ```

* **Respostas:**
    * **Sucesso (201 Created):** Retorna um JSON confirmando que a nota foi adicionada.
        ```json
        {
          "sucesso": "Nota para o aluno 101 inserida com sucesso."
        }
        ```
    * **Falha (400 Bad Request):** Retorna um JSON com uma mensagem de erro se houver campos faltando ou se os valores forem inválidos.
        ```json
        {
          "erro": "Payload inválido. Verifique as chaves obrigatórias."
        }
        ```
