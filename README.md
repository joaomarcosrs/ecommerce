# Ecommerce API

---

## 🇧🇷 Português (PT-BR)

API de e-commerce construída com FastAPI, SQLAlchemy, Alembic e autenticação JWT.

### Requisitos

- Python 3.12+
- Poetry

### Instalação (Poetry)

```bash
poetry install
poetry shell
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
alembic upgrade head
```

### Rodando a API

```bash
poetry run task run
```

Servidor: `http://127.0.0.1:8000`

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### Qualidade e testes

```bash
poetry run task lint
poetry run pytest -q
```

### Rotas atuais

#### Auth

- `POST /auth/register/` — cadastrar usuário
- `POST /auth/token/` — login e obter token JWT

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

### Arquitetura

- `ecommerce/api`: camada HTTP
- `ecommerce/auth`: domínio de autenticação
- `ecommerce/users`: domínio de usuários
- `ecommerce/core`: infraestrutura compartilhada

### Troubleshooting (PT-BR)

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
    - Rode `alembic upgrade head` antes de subir a API.

- **Tabela não existe / migration pendente**
    - Rode: `alembic upgrade head`.

- **Poetry/env não reconhecido**
    - Reinstale dependências com `poetry install`.
    - Ative com `poetry shell` ou use `poetry run <comando>`.

---

## 🇺🇸 English (EN)

E-commerce API built with FastAPI, SQLAlchemy, Alembic, and JWT authentication.

### Requirements

- Python 3.12+
- Poetry

### Installation (Poetry)

```bash
poetry install
poetry shell
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
alembic upgrade head
```

### Running the API

```bash
poetry run task run
```

Server: `http://127.0.0.1:8000`

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### Quality and tests

```bash
poetry run task lint
poetry run pytest -q
```

### Current routes

#### Auth

- `POST /auth/register/` — sign up
- `POST /auth/token/` — login and get JWT token

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

### Architecture

- `ecommerce/api`: HTTP layer
- `ecommerce/auth`: authentication domain
- `ecommerce/users`: users domain
- `ecommerce/core`: shared infrastructure

### Troubleshooting (EN)

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
    - Run `alembic upgrade head` before starting the API.

- **Table not found / pending migrations**
    - Run: `alembic upgrade head`.

- **Poetry/environment issues**
    - Reinstall dependencies with `poetry install`.
    - Activate with `poetry shell` or use `poetry run <command>`.
