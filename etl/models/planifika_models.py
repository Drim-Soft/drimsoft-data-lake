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