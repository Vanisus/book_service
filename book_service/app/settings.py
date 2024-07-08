from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_host: str
    db_port: str
    db_name: str
    db_user: str
    db_pass: str
    file_service_url: str
    @property
    def db_url(self):
        return f'postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}/{self.db_name}'

    class Config:
        env_file = ".env"


settings = Settings()
