# DIO Bank API - Guia de Implementação com FastAPI

Este repositório contém o guia passo a passo e o código-fonte para a construção de uma **API Bancária Assíncrona** moderna e eficiente utilizando o framework **FastAPI** em Python. O projeto foi desenvolvido como parte do desafio da trilha de Python da Digital Innovation One (DIO).

## 🚀 Funcionalidades Implementadas

*   **Autenticação JWT:** Login e proteção de rotas com JSON Web Tokens.
*   **Gestão de Contas:** Criação de novas contas (`/accounts/`).
*   **Transações Assíncronas:** Depósitos (`/transactions/deposit`) e Saques (`/transactions/withdraw`).
*   **Extrato:** Visualização do saldo e histórico de transações (`/transactions/statement`).
*   **Validação de Negócio:** Verificação de saldo e valores positivos para transações.
*   **Persistência de Dados:** Uso do SQLAlchemy 2.0+ e `databases` para operações assíncronas com banco de dados.
*   **Migrações:** Configuração do Alembic para gerenciamento de esquema de banco de dados.

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Descrição |
| :--- | :--- |
| **Python** | Linguagem de programação principal (v3.12+) |
| **FastAPI** | Framework web de alta performance para APIs |
| **Pydantic** | Validação de dados e serialização |
| **SQLAlchemy** | ORM (Object-Relational Mapper) para interação com o banco de dados |
| **Alembic** | Ferramenta de migração de banco de dados |
| **`databases`** | Biblioteca para operações assíncronas com banco de dados |
| **`passlib`** | Hashing de senhas (bcrypt) |
| **`python-jose`** | Implementação de JWT (JSON Web Tokens) |

## ⚙️ Configuração do Ambiente

### 1. Clonar o Repositório e Criar o Ambiente Virtual

\`\`\`bash
git clone https://github.com/seu-usuario/dio-bank-api.git
cd dio-bank-api
python -m venv venv
source venv/bin/activate # Linux/macOS
# venv\\Scripts\\activate # Windows
\`\`\`

### 2. Instalar Dependências

O projeto utiliza o **Poetry** para gerenciamento de dependências.

\`\`\`bash
# Instale o Poetry se ainda não o tiver
pip install poetry

# Instale as dependências do projeto
poetry install
\`\`\`

### 3. Configurar Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto, copiando o conteúdo de `.env.example`:

**`.env.example`**
\`\`\`
ENVIRONMENT="local"
DATABASE_URL="sqlite:///./bank.db"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
\`\`\`

### 4. Inicializar e Aplicar Migrações do Banco de Dados

Use o Alembic para criar o esquema do banco de dados.

\`\`\`bash
# Inicializa o Alembic (apenas na primeira vez)
# alembic init migrations

# Gera a primeira migração (após a criação dos modelos)
# alembic revision --autogenerate -m "create initial tables"

# Aplica as migrações
alembic upgrade head
\`\`\`

## ▶️ Executando a API

Inicie o servidor Uvicorn:

\`\`\`bash
uvicorn src.main:app --reload
\`\`\`

A API estará disponível em `http://127.0.0.1:8000`.

## 📄 Documentação Interativa

A documentação interativa (Swagger UI) está disponível em:

*   **Swagger UI:** `http://127.0.0.1:8000/docs`
*   **Redoc:** `http://127.0.0.1:8000/redoc`

Use a documentação para testar os endpoints:

1.  **Criar Conta:** POST `/accounts/`
2.  **Obter Token:** POST `/auth/token` (Use o e-mail e senha da conta criada)
3.  **Acessar Rotas Protegidas:** Use o token JWT obtido no cabeçalho `Authorization: Bearer <token>` para testar:
    *   GET `/accounts/me`
    *   POST `/transactions/deposit`
    *   POST `/transactions/withdraw`
    *   GET `/transactions/statement`

## 💡 Guia de Desenvolvimento Passo a Passo

O guia completo de desenvolvimento, detalhando cada arquivo e conceito, está disponível no arquivo `GUIDE.md` (a ser criado).
