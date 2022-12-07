from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Tekton API"
    db_url: str = "sqlite:///./app.db"


settings = Settings()
