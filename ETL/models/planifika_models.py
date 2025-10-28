from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from .bases import BasePlanifika

class UserPlanifika(BasePlanifika):
    __tablename__ = 'userplanifika'
    iduser = Column(Integer, primary_key=True)
    name = Column(String)
    photourl = Column(String)
    iduserstatus = Column(Integer)
    idusertype = Column(Integer)
    idorganization = Column(Integer)
    supabaseuserid = Column(UUID(as_uuid=True))

class Organization(BasePlanifika):
    __tablename__ = 'organization'
    idorganization = Column(Integer, primary_key=True)
    name = Column(String)

class UserType(BasePlanifika):
    __tablename__ = 'usertype'
    idusertype = Column(Integer, primary_key=True)
    name = Column(String)

class UserStatusPlanifika(BasePlanifika):
    __tablename__ = 'userstatus'
    iduserstatus = Column(Integer, primary_key=True)
    name = Column(String)
