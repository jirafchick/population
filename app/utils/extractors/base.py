from abc import ABC, abstractmethod

import pandas as pd


class AbstractBaseExtractor(ABC):
	"""Abstract base class for data extractors."""

	def __init__(self, content):
		self._data_frame = pd.read_html(str(content))[0]

	@abstractmethod
	async def extract(self) -> dict:
		"""Extract data from the DataFrame. To be implemented by subclasses."""
		pass
