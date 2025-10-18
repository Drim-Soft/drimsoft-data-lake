# planifika_models.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserPlanifika(Base):
    __tablename__ = 'userplanifika'
    iduser = Column(Integer, primary_key=True)
    iduserstatus = Column(Integer, ForeignKey('userstatus.iduserstatus'))
    
class UserStatus(Base):
    __tablename__ = 'userstatus'
    iduserstatus = Column(Integer, primary_key=True)
    name = Column(String)
