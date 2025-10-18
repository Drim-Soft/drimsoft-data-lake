from sqlalchemy import Column, Integer, String, ForeignKey
from . import Base

class UserPlanifika(Base):
    __tablename__ = 'userplanifika'
    iduser = Column(Integer, primary_key=True)
    iduserstatus = Column(Integer, ForeignKey('userstatus.iduserstatus'))

class UserStatus(Base):
    __tablename__ = 'userstatus'
    iduserstatus = Column(Integer, primary_key=True)
    name = Column(String)
