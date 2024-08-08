from sqlalchemy import Column, Integer, String

from app.database import Base


class Country(Base):
	__tablename__ = "countries"

	id = Column(Integer, primary_key=True, index=True)
	name = Column(String, nullable=False, unique=True)
	population = Column(Integer, nullable=False)
	region = Column(String, nullable=False)
