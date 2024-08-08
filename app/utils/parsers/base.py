from abc import ABC, abstractmethod


class AbstractBaseParser(ABC):
	@abstractmethod
	def parse(self):
		pass
