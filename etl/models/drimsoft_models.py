from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from . import BaseDrimsoft

class RoleDrimsoft(BaseDrimsoft):
    __tablename__ = 'role'
    idrole = Column(Integer, primary_key=True)
    name = Column(String)

class UserStatusDrimsoft(BaseDrimsoft):
    __tablename__ = 'userstatus'
    iduserstatus = Column(Integer, primary_key=True)
    name = Column(String)

class UserDrimsoft(BaseDrimsoft):
    __tablename__ = 'userdrimsoft'
    iduser = Column(Integer, primary_key=True)
    supabaseuserid = Column(UUID)
    iduserstatus = Column(Integer)
    idrole = Column(Integer)
    name = Column(String)

class TicketStatus(BaseDrimsoft):
    __tablename__ = 'ticketstatus'
    idticketstatus = Column(Integer, primary_key=True)
    name = Column(String)

class TicketSupport(BaseDrimsoft):
    __tablename__ = 'ticketsupport'
    idtickets = Column(Integer, primary_key=True)
    idplanifikauser = Column(Integer)
    idticketstatus = Column(Integer)
    title = Column(String)
    description = Column(Text)
    answer = Column(Text)
    iddrimsoftuser = Column(Integer)