from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base  # ahora sí existe unificado 💪

# URIs
DB_URI_SUSCRIPCIONES = "postgresql://postgres:[YOUR-PASSWORD]@db.iwnxlkmjvxmcuscangyi.supabase.co:5432/postgres"
DB_URI_PLANIFIKA = "postgresql://postgres:[YOUR-PASSWORD]@db.znzlfnztvnnzfbbsdjsl.supabase.co:5432/postgres"
DB_URI_DRIMSOFT = "postgresql://postgres:[YOUR-PASSWORD]@db.zqbwjlrlnxjlrusmmciw.supabase.co:5432/postgres"
DB_URI_PROYECTOS = "postgresql://postgres:[YOUR-PASSWORD]@db.rniqzbnygegbkecikbxj.supabase.co:5432/postgres"

# Engines
engine_suscripciones = create_engine(DB_URI_SUSCRIPCIONES)
engine_planifika = create_engine(DB_URI_PLANIFIKA)
engine_drimsoft = create_engine(DB_URI_DRIMSOFT)
engine_proyectos = create_engine(DB_URI_PROYECTOS)

# Sesiones
SessionSuscripciones = sessionmaker(bind=engine_suscripciones)
SessionPlanifika = sessionmaker(bind=engine_planifika)
SessionDrimsoft = sessionmaker(bind=engine_drimsoft)
SessionProyectos = sessionmaker(bind=engine_proyectos)

# Crear todas las tablas (si no existen)
Base.metadata.create_all(bind=engine_suscripciones)
Base.metadata.create_all(bind=engine_planifika)
Base.metadata.create_all(bind=engine_drimsoft)
Base.metadata.create_all(bind=engine_proyectos)
