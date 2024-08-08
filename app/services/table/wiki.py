from app.services.table.base import AbstractTableService
from app.utils.extractors import WikiTableExtractor
from app.utils.parsers import WikiTabelParser


class WikiTableService(AbstractTableService):
	"""Service class for handling data fetching, parsing, and saving from Wikipedia"""

	def get_parser(self):
		return WikiTabelParser

	def get_extractor(self):
		return WikiTableExtractor
