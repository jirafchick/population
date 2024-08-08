from abc import ABC, abstractmethod

from prettytable import PrettyTable
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import text

from app.config import settings
from app.database import db
from app.models import Country
from app.schemas import CountryModel
from app.utils.extractors.base import AbstractBaseExtractor
from app.utils.fetchers import WebPageRetriever
from app.utils.parsers.base import AbstractBaseParser


class AbstractTableService(ABC):
	"""Abstract base class for services that fetch, parse, and save data."""

	def __init__(self):
		self.fetcher = WebPageRetriever(target_url=settings.PARSE_URL)

	@abstractmethod
	def get_parser(self) -> type[AbstractBaseParser]:
		"""Abstract method to get the parser class."""
		raise NotImplementedError

	@abstractmethod
	def get_extractor(self) -> type[AbstractBaseExtractor]:
		"""Abstract method to get the extractor class."""
		raise NotImplementedError

	async def __save_data(self, data):
		"""Saves the extracted data to the database."""
		await self.__save_table_to_db(data=data)

	async def get_data(self):
		"""Fetches, parses, and saves data."""
		table = await self.__parse_table()
		await self.__save_data(table)

	async def __parse_table(self):
		"""Parses the fetched content and extracts data."""
		parser = self.get_parser()(await self.fetcher.fetch_content())
		extractor = self.get_extractor()(await parser.parse())
		return await extractor.extract()

	@staticmethod
	async def __save_table_to_db(data: list[CountryModel]):
		"""Saves a list of country data to the database."""
		async with db.session_factory() as session:
			stmt = insert(Country).values(data).on_conflict_do_nothing(index_elements=["name"])
			await session.execute(stmt)
			await session.commit()

	async def print_data(self):
		async with db.session_factory() as session:
			result = await session.execute(self.query)
			print(self.print_table(result.fetchall()))

	@staticmethod
	def print_table(rows):
		"""Method returns table for pretty print."""
		table = PrettyTable(
			field_names=[
				"Region",
				"Population (total)",
				"Country (most populous)",
				"Population most populated country",
				"Country (least populated)",
				"Population least populated country",
			]
		)
		table.add_rows(rows)
		return table

	@property
	def query(self):
		"""Property with sql query."""
		query = text("""SELECT
						region,
						SUM(population) AS total_population,
						MAX(name) FILTER (WHERE population = (SELECT MAX(population) FROM countries c2 WHERE c2.region = c1.region)) AS largest_country,
						MAX(population) FILTER (WHERE population = (SELECT MAX(population) FROM countries c2 WHERE c2.region = c1.region)) AS largest_population,
						MAX(name) FILTER (WHERE population = (SELECT MIN(population) FROM countries c2 WHERE c2.region = c1.region)) AS smallest_country,
						MIN(population) FILTER (WHERE population = (SELECT MIN(population) FROM countries c2 WHERE c2.region = c1.region)) AS smallest_population
					FROM
						countries c1
					GROUP BY
						region;
		""")
		return query
