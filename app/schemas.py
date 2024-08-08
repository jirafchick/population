from pydantic import BaseModel


class CountryModel(BaseModel):
	name: str
	population: int
	region: str

	class Config:
		extra = "forbid"
