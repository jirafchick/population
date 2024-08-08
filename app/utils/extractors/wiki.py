import asyncio

from pandas import DataFrame

from app.utils.extractors.base import AbstractBaseExtractor
from app.utils.extractors.mixin import ExtractorMixin


class WikiTableExtractor(AbstractBaseExtractor, ExtractorMixin):
	"""Extracts and processes data from Wikipedia tables."""

	__columns = ["country", "population_2022", "population_2023", "growth_rate", "continent", "region"]

	async def extract(self) -> DataFrame:
		"""Asynchronously extracts data from the Wikipedia table."""
		return await asyncio.to_thread(self._sync_extract)

	def _sync_extract(self) -> DataFrame:
		"""Synchronously extracts and processes data from the Wikipedia table."""
		self._set_columns()
		self._population_to_int()
		self._drop_na()
		return self._data_frame

	def _set_columns(self):
		"""Sets predefined column names for the DataFrame."""
		self._data_frame.columns = self.__columns

	def _population_to_int(self):
		"""Converts population columns to int."""
		self._data_frame["population_2022"] = self._data_frame["population_2022"].apply(self.to_int)
		self._data_frame["population_2023"] = self._data_frame["population_2023"].apply(self.to_int)

	def _drop_na(self):
		"""Removes rows with missing values from the DataFrame."""
		self._data_frame.dropna(inplace=True)
