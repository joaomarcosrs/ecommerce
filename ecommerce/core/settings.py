from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = 'sqlite:///database.db'
    JWT_SECRET_KEY: str = 'change-me-in-env'
    JWT_ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = {
        'env_file': '.env',
        'env_file_encoding': 'utf-8',
    }


settings = Settings()
