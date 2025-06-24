from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    firecrawl_api_key: str = Field(..., alias="FIRECRAWL_API_KEY")
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")
