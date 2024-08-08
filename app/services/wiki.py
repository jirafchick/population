from app.services.base import AbstractService
from app.utils.extractors import WikiTableExtractor
from app.utils.parsers import WikiTabelParser


class WikiService(AbstractService):
	"""Service class for handling data fetching, parsing, and saving from Wikipedia"""

	def get_parser(self):
		return WikiTabelParser

	def get_extractor(self):
		return WikiTableExtractor
