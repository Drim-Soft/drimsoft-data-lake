from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# URIs de Supabase (externos)
DB_URI_DRIMSOFT = "postgresql://postgres.zqbwjlrlnxjlrusmmciw:Drimsoft2025.@aws-1-us-east-2.pooler.supabase.com:6543/postgres?sslmode=require"
DB_URI_PLANIFIKA = "postgresql://postgres.znzlfnztvnnzfbbsdjsl:Planifika2025.@aws-1-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require"
DB_URI_PROYECTOS = "postgresql://postgres.rniqzbnygegbkecikbxj:Planifika2025.@aws-1-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require"
DB_URI_SUSCRIPCIONES = "postgresql://postgres.iwnxlkmjvxmcuscangyi:Drimsoft2025.@aws-1-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require"

# Engines
engine_drimsoft = create_engine(DB_URI_DRIMSOFT, pool_pre_ping=True, pool_recycle=3600, echo=False)
engine_planifika = create_engine(DB_URI_PLANIFIKA, pool_pre_ping=True, pool_recycle=3600, echo=False)
engine_proyectos = create_engine(DB_URI_PROYECTOS, pool_pre_ping=True, pool_recycle=3600, echo=False)
engine_suscripciones = create_engine(DB_URI_SUSCRIPCIONES, pool_pre_ping=True, pool_recycle=3600, echo=False)

# Sesiones
SessionDrimsoft = sessionmaker(bind=engine_drimsoft)
SessionPlanifika = sessionmaker(bind=engine_planifika)
SessionProyectos = sessionmaker(bind=engine_proyectos)
SessionSuscripciones = sessionmaker(bind=engine_suscripciones)