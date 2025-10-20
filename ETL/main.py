import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from config import DB_URI_SUSCRIPCIONES, DB_URI_PLANIFIKA, DB_URI_DRIMSOFT, DB_URI_PROYECTOS


# =============================
# Cargar variables de entorno
# =============================
load_dotenv()

def build_db_uri(prefix: str) -> str:
    """Construye la URI de conexión a partir de las variables .env."""
    jdbc_url = os.getenv(f"{prefix}_DB_URL")
    user = os.getenv(f"{prefix}_DB_USER")
    password = os.getenv(f"{prefix}_DB_PASSWORD")

    if not jdbc_url or not user or not password:
        raise ValueError(f"Faltan variables para {prefix}")

    # Limpiar el formato jdbc y quitar parámetros extra
    clean_url = jdbc_url.replace("jdbc:", "").split("?")[0]
    return f"{clean_url.replace('postgresql://', f'postgresql://{user}:{password}@')}"

# =============================
# Construir URIs de cada base
# =============================
DB_URI_DRIMSOFT = build_db_uri("DRIMSOFT")
DB_URI_PLANIFIKA = build_db_uri("PLANIFIKA")
DB_URI_PROJECTS = build_db_uri("PROJECTS")
DB_URI_SUBSCRIPTIONS = build_db_uri("CUBSCRIPTIONS")  

# =============================
# Crear engines y sesiones
# =============================
engine_drimsoft = create_engine(DB_URI_DRIMSOFT)
engine_planifika = create_engine(DB_URI_PLANIFIKA)
engine_projects = create_engine(DB_URI_PROJECTS)
engine_subscriptions = create_engine(DB_URI_SUBSCRIPTIONS)

SessionDrimsoft = sessionmaker(bind=engine_drimsoft)
SessionPlanifika = sessionmaker(bind=engine_planifika)
SessionProjects = sessionmaker(bind=engine_projects)
SessionSubscriptions = sessionmaker(bind=engine_subscriptions)


for engine in [
    engine_drimsoft,
    engine_planifika,
    engine_projects,
    engine_subscriptions,
]:
    Base.metadata.create_all(bind=engine)

print("✅ Conexión y creación de tablas completada con éxito.")
