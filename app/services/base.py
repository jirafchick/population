from abc import ABC, abstractmethod

from app.config import Settings
from app.database import db
from app.models import Country
from app.schemas import CountryModel
from app.utils.extractors.base import AbstractBaseExtractor
from app.utils.fetchers import WebPageRetriever
from app.utils.parsers.base import AbstractBaseParser


class AbstractService(ABC):
	"""Abstract base class for services that fetch, parse, and save data."""

	def __init__(self):
		self.fetcher = WebPageRetriever(target_url=Settings().PARSE_URL)

	@abstractmethod
	def get_parser(self) -> type[AbstractBaseParser]:
		"""Abstract method to get the parser class."""
		raise NotImplementedError

	@abstractmethod
	def get_extractor(self) -> type[AbstractBaseExtractor]:
		"""Abstract method to get the extractor class."""
		raise NotImplementedError

	async def save_data(self, data):
		"""Saves the extracted data to the database."""
		await self.save_table_to_db(data=data)

	async def get_data(self):
		"""Fetches, parses, and saves data."""
		table = await self.parse_table()
		await self.save_data(table)

	async def parse_table(self):
		"""Parses the fetched content and extracts data."""
		parser = self.get_parser()(await self.fetcher.fetch_content())
		extractor = self.get_extractor()(await parser.parse())
		return await extractor.extract()

	@staticmethod
	async def save_table_to_db(data: list[CountryModel]):
		"""Saves a list of country data to the database."""
		async with db.session_factory() as session:
			await session.execute(Country.__table__.insert().values(data))
			await session.commit()
