from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres@localhost/projectbot')
Base = declarative_base()

class Author(Base):
        __tablename__   = 'author' 
        id              = Column(Integer, primary_key=True)
        name            = Column(String, unique=True)
        projects        = relationship('Projects', secondary='assignement')

class Projects(Base):
        __tablename__   = 'projects'
        id              = Column(Integer, primary_key=True)
        name            = Column(String, unique=True)
        description     = Column(String)
        authors         = relationship('Author', secondary='assignement')

class Assignement(Base):
        __tablename__   = 'assignement'
        id              = Column(Integer,primary_key=True)
        author_id       = Column(Integer,ForeignKey('author.id', ondelete='CASCADE'))
        projects_id     = Column(Integer,ForeignKey('projects.id', ondelete='CASCADE'))
        
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()

def db_get_author(name):
    aTry = session.query(Author).filter(Author.name==name).first()
    if aTry:
        return (True, aTry)
    return (False,None)

def db_get_project(name):
    aTry = session.query(Projects).filter(Projects.name==name).first()
    if aTry:
        return (True, aTry)
    return (False,None)

def db_list_author():
    aTry  = session.query(Author)
    return aTry

def db_list_project():
    aTry  = session.query(Projects)
    return aTry

def db_list_unassigned():
    aTry = session.query(Projects).filter(Projects.authors == None)
    if aTry:
        return (True,aTry)
    return (False,None)

def db_list_assigned():
    aTry = session.query(Projects).filter(Projects.authors != None)
    if aTry:
        return (True,aTry)
    return (False,None)
