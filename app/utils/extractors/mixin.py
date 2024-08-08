import pandas as pd


class ExtractorMixin:
	"""Mixin class providing utility methods for data extraction and conversion."""

	@staticmethod
	def to_int(value):
		"""Converts various input types to integer."""
		match value:
			case _ if pd.isna(value):
				return pd.NA
			case int() | float():
				return int(value)
			case str():
				return int(value.replace(",", ""))
			case _:
				return pd.NA
