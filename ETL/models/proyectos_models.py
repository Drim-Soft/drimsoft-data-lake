from sqlalchemy import Column, Integer, String, ForeignKey
from . import Base

class Project(Base):
    __tablename__ = 'project'
    idproject = Column(Integer, primary_key=True)
    idprojectstatus = Column(Integer, ForeignKey('projectstatus.idprojectstatus'))
    idmethodology = Column(Integer)

class ProjectStatus(Base):
    __tablename__ = 'projectstatus'
    idprojectstatus = Column(Integer, primary_key=True)
    name = Column(String)
