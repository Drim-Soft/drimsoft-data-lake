# proyectos_models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Project(Base):
    __tablename__ = 'project'
    idproject = Column(Integer, primary_key=True)
    idprojectstatus = Column(Integer, ForeignKey('projectstatus.idprojectstatus'))
    idmethodology = Column(Integer)
    

class ProjectStatus(Base):
    __tablename__ = 'projectstatus'
    idprojectstatus = Column(Integer, primary_key=True)
    name = Column(String)



