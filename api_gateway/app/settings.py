from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    book_service_url: str
    user_service_url: str
    rental_service_url: str
    file_service_url: str
    db_host: str
    db_port: str
    db_name: str
    db_user: str
    db_pass: str

    @property
    def db_url(self):
        return f'postgresql+asyncpg://{self.db_user}:{self.db_pass}@{self.db_host}/{self.db_name}'

    class Config:
        env_file = ".env"


settings = Settings()
