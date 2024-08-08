from abc import ABC, abstractmethod

from bs4 import BeautifulSoup


class AbstractBaseParser(ABC):
	"""Abstract base class for HTML parsers."""

	def __init__(self, content: str):
		self.soup = BeautifulSoup(content, "html.parser")

	@abstractmethod
	def parse(self):
		"""Parse the HTML content. To be implemented by subclasses."""
		pass
