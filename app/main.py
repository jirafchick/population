import argparse
import asyncio

from app.database import db


def get_parse_args() -> argparse.ArgumentParser:
	"""Parses command line arguments for the population data management application."""
	parser = argparse.ArgumentParser(description="Population data management")
	subparsers = parser.add_subparsers(dest="command", help="Available commands", required=True)
	subparsers.add_parser("get_data", help="Fetch and store population data")
	subparsers.add_parser("print_data", help="Print aggregated population data")
	return parser


async def main():
	"""Handles the main entry point for the population data management application."""
	parser = get_parse_args()
	args = parser.parse_args()

	if args.command == "get_data":
		pass
	elif args.command == "print_data":
		pass
	parser.print_help()


if __name__ == "__main__":
	asyncio.set_event_loop(asyncio.new_event_loop())
	loop = asyncio.get_event_loop()
	loop.run_until_complete(db.init_db())
	loop.run_until_complete(main())
