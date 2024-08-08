from pydantic_settings import BaseSettings


class PostgresSettings(BaseSettings):
	DB_HOST: str = "localhost"
	DB_PORT: int = 5432
	DB_USER: str = "postgres"
	DB_PASSWORD: str = "postgres"
	DB_NAME: str = "postgres"

	@property
	def database_url(self) -> str:
		return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class Settings(BaseSettings):
	PARSE_URL: str
	db: PostgresSettings = PostgresSettings()

	class Config:
		env_file = ".env"


settings = Settings()

__all__ = ("settings", "PostgresSettings")
