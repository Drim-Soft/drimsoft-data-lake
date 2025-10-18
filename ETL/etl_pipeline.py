from prefect import flow, task
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os, sys

# Agregar el path del proyecto y el de la carpeta models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "models")))

# Importaciones de los modelos ahora correctas 
from models.suscripciones_models import Invoice
from models.proyectos_models import Project
from models.planifika_models import UserPlanifika
from models import Base
from main import engine_suscripciones, engine_proyectos, engine_planifika, engine_drimsoft

#  Conexión al warehouse

WAREHOUSE_URI = "postgresql+psycopg2://warehouse:warehouse123@warehouse:5432/warehouse"
engine_warehouse = create_engine(WAREHOUSE_URI)
SessionWarehouse = sessionmaker(bind=engine_warehouse)

# ---------------------- EXTRACT ----------------------

@task
def extract_invoices():
    Session = sessionmaker(bind=engine_suscripciones)
    with Session() as session:
        data = session.query(Invoice).all()
    return [row.__dict__ for row in data]

@task
def extract_projects():
    Session = sessionmaker(bind=engine_proyectos)
    with Session() as session:
        data = session.query(Project).all()
    return [row.__dict__ for row in data]

@task
def extract_users():
    Session = sessionmaker(bind=engine_planifika)
    with Session() as session:
        data = session.query(UserPlanifika).all()
    return [row.__dict__ for row in data]

# ---------------------- LOAD ----------------------

@task
def load_to_warehouse(table_name: str, data: list):
    if not data:
        print(f"No hay datos para cargar en {table_name}")
        return
    import pandas as pd
    df = pd.DataFrame(data)
    df = df.drop(columns=['_sa_instance_state'], errors='ignore')
    df.to_sql(table_name, con=engine_warehouse, if_exists='replace', index=False)
    print(f"✅ {len(df)} registros cargados en la tabla {table_name} del warehouse")

# ---------------------- FLOW ----------------------

@flow(name="ETL Pipeline Base")
def etl_pipeline():
    invoices = extract_invoices()
    projects = extract_projects()
    users = extract_users()

    load_to_warehouse("invoice", invoices)
    load_to_warehouse("project", projects)
    load_to_warehouse("userplanifika", users)

if __name__ == "__main__":
    etl_pipeline()
