from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
from functools import lru_cache


class Settings(BaseSettings):
    # MongoDB Configuration
    mongodb_uri: str = Field(..., alias="MONGODB_URL")
    mongodb_database: str = Field(..., alias="MONGODB_DATABASE")

    # Google Gemini Configuration
    GOOGLE_API_KEY: str = Field(..., alias="GOOGLE_API_KEY")
    MODEL_NAME: str = Field(..., alias="MODEL_NAME")

    # API Configuration
    api_host: str = Field("0.0.0.0", alias="API_HOST")
    api_port: int = Field(8000, alias="API_PORT")
    debug: bool = Field(True, alias="DEBUG")

    # CORS Configuration
    ALLOWED_ORIGINS: List[str] = Field(
        default=["http://localhost:3000"],
        alias="ALLOWED_ORIGINS"
    )

    AGENT_MAX_ITERATIONS: int = 10
    AGENT_VERBOSE: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
