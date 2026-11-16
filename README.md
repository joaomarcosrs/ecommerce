# Ecommerce API

---

## 🇧🇷 Português (PT-BR)

API de e-commerce construída com FastAPI, SQLAlchemy, Alembic e autenticação JWT.

### Requisitos

- [uv](https://docs.astral.sh/uv/) — gerencia o Python e as dependências do projeto

> O Python não é mais gerenciado pelo pyenv/Poetry. A versão está fixada em
> `.python-version` (3.12) e o uv baixa um interpretador gerenciado no primeiro
> `uv sync` — nada de depender de um Python instalado globalmente.

### Instalação

```bash
uv sync
```

Isso cria o `.venv`, baixa o Python 3.12 (se necessário) e instala as
dependências de produção e de desenvolvimento (`dev`).

### Ambiente

Não há ativação automática. `uv run` usa o `.venv` do projeto e o sincroniza
antes de executar, então não é preciso ativar nada para rodar comandos:

```bash
uv run pytest
```

Para um shell ativado (comandos sem o prefixo `uv run`), rode `uv sync` uma vez
e ative:

```bash
uv sync
source .venv/bin/activate
```

### Configuração de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=sqlite:///database.db
JWT_SECRET_KEY=troque-para-um-segredo-forte
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Banco de dados (SQLite)

```bash
uv run alembic upgrade head
```

### Rodando a API

```bash
uv run task run
```

Equivalente a `uv run fastapi dev ecommerce/app.py`.

Servidor: `http://127.0.0.1:8000`

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### Qualidade e testes

```bash
uv run task lint
uv run pytest -q
uv run task test   # lint + pytest com cobertura + relatório HTML
```

### Gerenciando dependências

```bash
uv add <pacote>              # dependência de produção
uv add --group dev <pacote>  # dependência de desenvolvimento
uv remove <pacote>
uv lock                      # atualiza o uv.lock
uv sync                      # aplica o lock no .venv
```

`uv.lock` e `.python-version` devem ser commitados para reproduzir o ambiente.

### Rotas atuais

#### Auth

- `POST /auth/register/` — cadastrar usuário
- `POST /auth/token/` — login e obter token JWT

#### Products

- `POST /products/` — criar produto
- `GET /products/?q=<termo>` — listar/buscar produtos
- `GET /products/{product_id}/` — consultar produto
- `PUT /products/{product_id}/` — atualizar produto
- `DELETE /products/{product_id}/` — remover produto

#### Users (Bearer Token obrigatório)

- `GET /users/me/{user_id}/` — consultar perfil
- `PUT /users/me/{user_id}/` — atualizar perfil
- `DELETE /users/me/{user_id}/` — remover usuário

### Exemplo com curl

#### 1) Registrar usuário

```bash
curl -X POST http://127.0.0.1:8000/auth/register/ \
    -H "Content-Type: application/json" \
    -d '{
        "name": "John Doe",
        "email": "john@example.com",
        "password": "secret",
        "phone_number": "11999999999"
    }'
```

#### 2) Login

```bash
curl -X POST http://127.0.0.1:8000/auth/token/ \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=john@example.com&password=secret"
```

#### 3) Chamar rota protegida

```bash
curl -X GET http://127.0.0.1:8000/users/me/{PUBLIC_ID}/ \
    -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

#### 4) Criar produto

```bash
curl -X POST http://127.0.0.1:8000/products/ \
    -H "Content-Type: application/json" \
    -d '{
        "name": "Camiseta",
        "description": "Camiseta de algodão",
        "price": "59.90",
        "sku": "CAM-001"
    }'
```

### Arquitetura

- `ecommerce/api`: camada HTTP
- `ecommerce/auth`: domínio de autenticação
- `ecommerce/products`: domínio de produtos
- `ecommerce/users`: domínio de usuários
- `ecommerce/core`: infraestrutura compartilhada

### Troubleshooting (PT-BR)

- **`Library not loaded: .../libpython3.12.dylib`**
    - O `.venv` era do Poetry e apontava para um Python do pyenv que foi removido.
    - O projeto agora usa uv: apague o venv quebrado e ressincronize.
      ```bash
      rm -rf .venv
      uv sync
      ```

- **`uv: command not found`**
    - Instale o uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`.

- **`uv sync --frozen` reclama que o lock está desatualizado**
    - Rode `uv lock` e commite o `uv.lock`.

- **Erro de token (`Could not validate credentials`)**
    - Verifique se o header está como `Authorization: Bearer <token>`.
    - Gere um novo token via `POST /auth/token/`.
    - Confirme se `JWT_SECRET_KEY` no `.env` é o mesmo usado para emitir o token.

- **`Not authenticated` nas rotas `/users/me/...`**
    - Essas rotas exigem autenticação com Bearer Token.

- **`Not enough permissions`**
    - O `user_id` da URL precisa ser o `public_id` do usuário dono do token.

- **Falha ao iniciar com erro de banco**
    - Confirme `DATABASE_URL` no `.env`.
    - Rode `uv run alembic upgrade head` antes de subir a API.

- **Tabela não existe / migration pendente**
    - Rode: `uv run alembic upgrade head`.

---

## 🇺🇸 English (EN)

E-commerce API built with FastAPI, SQLAlchemy, Alembic, and JWT authentication.

### Requirements

- [uv](https://docs.astral.sh/uv/) — manages the project's Python and dependencies

> Python is no longer managed by pyenv/Poetry. The version is pinned in
> `.python-version` (3.12) and uv downloads a managed interpreter on the first
> `uv sync` — no reliance on a globally installed Python.

### Installation

```bash
uv sync
```

This creates `.venv`, downloads Python 3.12 if needed, and installs production
and development (`dev`) dependencies.

### Environment

There is no automatic activation. `uv run` uses the project's `.venv` and syncs
it before executing, so no activation is needed to run commands:

```bash
uv run pytest
```

For an activated shell (commands without the `uv run` prefix), run `uv sync`
once and activate:

```bash
uv sync
source .venv/bin/activate
```

### Environment configuration

Create a `.env` file at the project root:

```env
DATABASE_URL=sqlite:///database.db
JWT_SECRET_KEY=change-this-to-a-strong-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Database (SQLite)

```bash
uv run alembic upgrade head
```

### Running the API

```bash
uv run task run
```

Equivalent to `uv run fastapi dev ecommerce/app.py`.

Server: `http://127.0.0.1:8000`

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### Quality and tests

```bash
uv run task lint
uv run pytest -q
uv run task test   # lint + pytest with coverage + HTML report
```

### Managing dependencies

```bash
uv add <package>              # production dependency
uv add --group dev <package>  # development dependency
uv remove <package>
uv lock                       # update uv.lock
uv sync                       # apply the lock to .venv
```

Commit `uv.lock` and `.python-version` so the environment is reproducible.

### Current routes

#### Auth

- `POST /auth/register/` — sign up
- `POST /auth/token/` — login and get JWT token

#### Products

- `POST /products/` — create product
- `GET /products/?q=<term>` — list/search products
- `GET /products/{product_id}/` — read product
- `PUT /products/{product_id}/` — update product
- `DELETE /products/{product_id}/` — delete product

#### Users (Bearer Token required)

- `GET /users/me/{user_id}/` — read profile
- `PUT /users/me/{user_id}/` — update profile
- `DELETE /users/me/{user_id}/` — delete user

### curl examples

#### 1) Register user

```bash
curl -X POST http://127.0.0.1:8000/auth/register/ \
    -H "Content-Type: application/json" \
    -d '{
        "name": "John Doe",
        "email": "john@example.com",
        "password": "secret",
        "phone_number": "11999999999"
    }'
```

#### 2) Login

```bash
curl -X POST http://127.0.0.1:8000/auth/token/ \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=john@example.com&password=secret"
```

#### 3) Call protected route

```bash
curl -X GET http://127.0.0.1:8000/users/me/{PUBLIC_ID}/ \
    -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

#### 4) Create product

```bash
curl -X POST http://127.0.0.1:8000/products/ \
    -H "Content-Type: application/json" \
    -d '{
        "name": "T-Shirt",
        "description": "Cotton t-shirt",
        "price": "59.90",
        "sku": "TSH-001"
    }'
```

### Architecture

- `ecommerce/api`: HTTP layer
- `ecommerce/auth`: authentication domain
- `ecommerce/products`: products domain
- `ecommerce/users`: users domain
- `ecommerce/core`: shared infrastructure

### Troubleshooting (EN)

- **`Library not loaded: .../libpython3.12.dylib`**
    - The old `.venv` belonged to Poetry and pointed at a pyenv Python that was removed.
    - The project now uses uv: delete the broken venv and resync.
      ```bash
      rm -rf .venv
      uv sync
      ```

- **`uv: command not found`**
    - Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`.

- **`uv sync --frozen` complains the lock is out of date**
    - Run `uv lock` and commit `uv.lock`.

- **Token error (`Could not validate credentials`)**
    - Ensure the header is `Authorization: Bearer <token>`.
    - Generate a fresh token from `POST /auth/token/`.
    - Check `JWT_SECRET_KEY` in `.env` matches the key used to issue the token.

- **`Not authenticated` on `/users/me/...` routes**
    - Those routes require Bearer authentication.

- **`Not enough permissions`**
    - The URL `user_id` must match the token owner `public_id`.

- **Database startup errors**
    - Verify `DATABASE_URL` in `.env`.
    - Run `uv run alembic upgrade head` before starting the API.

- **Table not found / pending migrations**
    - Run: `uv run alembic upgrade head`.
