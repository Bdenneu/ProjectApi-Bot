from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres@localhost/projectbot')
Base = declarative_base()

class Author(Base):
	__tablename__ = 'author' 
	id = Column(Integer, primary_key=True)
	name = Column(String)

class Projects(Base):
	__tablename__ = 'projects'
	id = Column(Integer, primary_key=True)
	name = Column(String)
	description = Column(String)

Base.metadata.create_all(engine)
