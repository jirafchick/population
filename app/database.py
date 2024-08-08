from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import PostgresSettings, Settings

Base = declarative_base()


class Database:
	"""Manages the database connection and provides session management."""

	_instance = None

	def __new__(cls, *args, **kwargs):
		if not isinstance(cls._instance, cls):
			cls._instance = super().__new__(cls)
		return cls._instance

	def __init__(self, db_conf: PostgresSettings):
		self._engine = create_async_engine(db_conf.database_url, echo=False, poolclass=NullPool)
		self.session_factory = sessionmaker(self._engine, expire_on_commit=False, class_=AsyncSession)

	async def init_db(self):
		"""Initializes the database by creating tables if they don't exist."""
		async with self._engine.begin() as conn:
			await conn.run_sync(Base.metadata.create_all)


settings = Settings()
db = Database(settings.db)

__all__ = ("db", "Base")
