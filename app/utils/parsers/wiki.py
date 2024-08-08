import asyncio

from bs4 import ResultSet

from app.utils.parsers.base import AbstractBaseParser


class WikiParser(AbstractBaseParser):
	"""Parser for Wikipedia tables."""

	async def parse(self):
		"""Asynchronously parse Wikipedia table content."""
		return await asyncio.to_thread(self._sync_parse)

	def _sync_parse(self) -> str:
		"""Synchronously extract table rows from Wikipedia HTML."""
		table = self.soup.find("table", {"class": "wikitable"})
		rows: ResultSet = table.find_all("tr")
		return str(rows)
