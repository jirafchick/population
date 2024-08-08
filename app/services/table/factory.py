from app.services.table.base import AbstractTableService

from .wiki import WikiTableService


def parse_table_factory(url_domain: str) -> type[AbstractTableService]:
	choices = {
		"en.wikipedia.org": WikiTableService,
	}
	try:
		return choices[url_domain]
	except KeyError:
		raise ValueError(f"Unrecognized URL wit domain: {url_domain}")
