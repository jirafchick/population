import argparse
import asyncio
from urllib.parse import urlparse

from app.database import db, settings
from app.services import parse_table_factory


def extract_domain(parse_url: str) -> str:
	"""Extracts the domain from the given URL."""
	parsed_url = urlparse(parse_url)
	domain = parsed_url.netloc
	return domain


def get_parse_args() -> argparse.ArgumentParser:
	"""Parses command line arguments for the population data management application."""
	parser = argparse.ArgumentParser(description="Population data management")
	subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)
	subparsers.add_parser("get_data", help="Fetch and store population data")
	subparsers.add_parser("print_data", help="Print aggregated population data")
	return parser


async def main():
	"""Handles the main entry point for the population data management application."""
	await db.init_db()
	parser = get_parse_args()
	args = parser.parse_args()

	domain = extract_domain(settings.PARSE_URL)

	parse_service = parse_table_factory(domain)

	if args.command == "get_data":
		await parse_service().get_data()
	elif args.command == "print_data":
		await parse_service().print_data()
	else:
		parser.print_help()


if __name__ == "__main__":
	asyncio.run(main())
