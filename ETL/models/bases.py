# ETL/models/bases.py
from sqlalchemy.orm import declarative_base

# ✅ Un Base independiente por base de datos
BaseDrimsoft = declarative_base()
BasePlanifika = declarative_base()
BaseProyectos = declarative_base()
BaseSuscripciones = declarative_base()
