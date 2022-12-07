from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Tekton API"
    db_url: str = "sqlite:///./app.db"
    discount_api_url: str = "https://6386f4eed9b24b1be3e1e965.mockapi.io"


settings = Settings()
