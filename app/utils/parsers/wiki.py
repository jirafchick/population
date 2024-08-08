import asyncio

from bs4.element import Tag

from app.utils.parsers.base import AbstractBaseParser


class WikiParser(AbstractBaseParser):
	"""Parser for Wikipedia tables."""

	async def parse(self) -> Tag:
		"""Asynchronously parse Wikipedia table content."""
		return await asyncio.to_thread(self._sync_parse)

	def _sync_parse(self) -> Tag:
		"""Synchronously extract table rows from Wikipedia HTML."""
		table = self.soup.find("table", {"class": "wikitable"})
		return table
