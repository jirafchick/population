import asyncio

from pydantic import TypeAdapter

from app.schemas import CountryModel
from app.utils.extractors.base import AbstractBaseExtractor
from app.utils.extractors.mixin import ExtractorMixin


class WikiTableExtractor(AbstractBaseExtractor, ExtractorMixin):
	"""Extracts and processes data from Wikipedia tables."""

	__column_sequence = ["name", "population_2022", "population", "growth_rate", "region", "subregion"]

	async def extract(self) -> list[CountryModel]:
		"""Asynchronously extracts data from the Wikipedia table."""
		return await asyncio.to_thread(self._sync_extract)

	def _sync_extract(self) -> list[CountryModel]:
		"""Synchronously extracts and processes data from the Wikipedia table."""
		self._set_column_sequence()
		self._drop_unused_columns()
		self._population_to_int()
		self._drop_na()
		self.validate_dict()
		return self._data_frame.to_dict("records")

	def _set_column_sequence(self):
		"""Sets predefined column names for the DataFrame."""
		self._data_frame.columns = self.__column_sequence

	def _population_to_int(self):
		"""Converts population columns to int."""
		self._data_frame["population"] = self._data_frame["population"].apply(self.to_int)

	def _drop_na(self):
		"""Removes rows with missing values from the DataFrame."""
		self._data_frame.dropna(inplace=True)

	def _drop_unused_columns(self):
		"""Drops the unused columns from the DataFrame, keeping only the "name", "population", and "region" columns."""
		self._data_frame = self._data_frame[["name", "population", "region"]]

	def validate_dict(self):
		"""Validates the dictionary representation of the DataFrame with the CountryModel schema."""
		countries_data = self._data_frame.to_dict(orient="records")
		adapter = TypeAdapter(list[CountryModel])
		adapter.validate_python(countries_data)
