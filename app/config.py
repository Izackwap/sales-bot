from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    adcombo_api_key: str
    database_url: str
    per_page: int = 25

    class Config:
        env_file = ".env"


settings = Settings()
