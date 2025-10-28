from sqlalchemy import Column, Integer, String, ForeignKey, Text, PrimaryKeyConstraint
from .bases import BaseProyectos

class Methodology(BaseProyectos):
    __tablename__ = 'methodology'
    idmethodology = Column(Integer, primary_key=True)
    name = Column(String)

class ProjectStatus(BaseProyectos):
    __tablename__ = 'projectstatus'
    idprojectstatus = Column(Integer, primary_key=True)
    name = Column(String)

class Project(BaseProyectos):
    __tablename__ = 'project'
    idproject = Column(Integer, primary_key=True)
    idprojectstatus = Column(Integer, ForeignKey('projectstatus.idprojectstatus'))
    idmethodology = Column(Integer, ForeignKey('methodology.idmethodology'))

class Phase(BaseProyectos):
    __tablename__ = 'phase'
    idphase = Column(Integer, primary_key=True)
    idproject = Column(Integer, ForeignKey('project.idproject'))

class TaskStatus(BaseProyectos):
    __tablename__ = 'taskstatus'
    idtaskstatus = Column(Integer, primary_key=True)
    name = Column(String)

class Task(BaseProyectos):
    __tablename__ = 'task'
    idtask = Column(Integer, primary_key=True)
    idphase = Column(Integer, ForeignKey('phase.idphase'))
    idtaskstatus = Column(Integer, ForeignKey('taskstatus.idtaskstatus'))

class RoleProyecto(BaseProyectos):
    __tablename__ = 'role'
    idrole = Column(Integer, primary_key=True)
    idmethodology = Column(Integer)
    name = Column(String)

class UserRoleProject(BaseProyectos):
    __tablename__ = 'userroleproject'
    iduser = Column(Integer, nullable=False)
    idrole = Column(Integer, nullable=False)
    idproject = Column(Integer, ForeignKey('project.idproject'))
    __table_args__ = (PrimaryKeyConstraint('iduser', 'idrole', name='userroleproject_pk'),)

class UserTask(BaseProyectos):
    __tablename__ = 'usertask'
    idusertask = Column(Integer, primary_key=True)
    iduser = Column(Integer)
    idtask = Column(Integer, ForeignKey('task.idtask'))

class PublicMessage(BaseProyectos):
    __tablename__ = 'publicmessage'
    idpublicmessage = Column(Integer, primary_key=True)
    idproject = Column(Integer, ForeignKey('project.idproject'))
