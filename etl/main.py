from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Cargar variables del archivo .env
load_dotenv()

# Leer las variables
DB_URI_DRIMSOFT = os.getenv("DB_URI_DRIMSOFT")
DB_URI_PLANIFIKA = os.getenv("DB_URI_PLANIFIKA")
DB_URI_PROYECTOS = os.getenv("DB_URI_PROYECTOS")
DB_URI_SUSCRIPCIONES = os.getenv("DB_URI_SUSCRIPCIONES")

# Crear engines
engine_drimsoft = create_engine(DB_URI_DRIMSOFT, pool_pre_ping=True, pool_recycle=3600, echo=False)
engine_planifika = create_engine(DB_URI_PLANIFIKA, pool_pre_ping=True, pool_recycle=3600, echo=False)
engine_proyectos = create_engine(DB_URI_PROYECTOS, pool_pre_ping=True, pool_recycle=3600, echo=False)
engine_suscripciones = create_engine(DB_URI_SUSCRIPCIONES, pool_pre_ping=True, pool_recycle=3600, echo=False)

# Sesiones
SessionDrimsoft = sessionmaker(bind=engine_drimsoft)
SessionPlanifika = sessionmaker(bind=engine_planifika)
SessionProyectos = sessionmaker(bind=engine_proyectos)
SessionSuscripciones = sessionmaker(bind=engine_suscripciones)
