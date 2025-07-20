from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    SECRET_KEY: str
    API_KEY: str

    class Config:
        env_file = "/home/chanwoo/PycharmProjects/parking-map/.env"
        env_file_encoding = "utf-8"

settings = Settings()