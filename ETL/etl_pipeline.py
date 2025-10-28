from prefect import flow, task
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os, sys
import pandas as pd

# Agregar el path del proyecto y el de la carpeta models
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "models")))

# Importaciones de los modelos
# ==== IMPORTAR BASES SEPARADAS ====
from models import (
    BaseDrimsoft,
    BasePlanifika,
    BaseProyectos,
    BaseSuscripciones
)

# ==== IMPORTAR MODELOS ====
# --- SUSCRIPCIONES ---
from models.suscripciones_models import (
    Invoice,
    Subscription,
    SubscriptionStatus,
    PaymentMethod,
    Currency
)

# --- PROYECTOS ---
from models.proyectos_models import (
    Project,
    ProjectStatus,
    Task,
    TaskStatus,
    Phase,
    UserRoleProject,
    RoleProyecto,
    Methodology
)

# --- PLANIFIKA ---
from models.planifika_models import (
    UserPlanifika,
    UserStatusPlanifika,
    Organization,
    UserType
)

# --- DRIMSOFT ---
from models.drimsoft_models import (
    UserDrimsoft,
    TicketSupport,
    TicketStatus,
    RoleDrimsoft,
    UserStatusDrimsoft
)

# ==== IMPORTAR ENGINES ====
from main import (
    engine_suscripciones,
    engine_proyectos,
    engine_planifika,
    engine_drimsoft
)


# Conexión al warehouse
WAREHOUSE_URI = "postgresql+psycopg2://warehouse:warehouse123@localhost:5433/warehouse"
engine_warehouse = create_engine(WAREHOUSE_URI)
SessionWarehouse = sessionmaker(bind=engine_warehouse)

# ====================== EXTRACT ======================

# --- SUSCRIPCIONES ---
@task(name="Extract Invoices")
def extract_invoices():
    print("📥 Extrayendo invoices...")
    Session = sessionmaker(bind=engine_suscripciones)
    with Session() as session:
        data = session.query(Invoice).all()
    print(f"   ✅ {len(data)} invoices extraídos")
    return [row.__dict__ for row in data]

@task(name="Extract Subscriptions")
def extract_subscriptions():
    print("📥 Extrayendo subscriptions...")
    Session = sessionmaker(bind=engine_suscripciones)
    with Session() as session:
        data = session.query(Subscription).all()
    print(f"   ✅ {len(data)} subscriptions extraídas")
    return [row.__dict__ for row in data]

@task(name="Extract Payment Methods")
def extract_payment_methods():
    print("📥 Extrayendo payment methods...")
    Session = sessionmaker(bind=engine_suscripciones)
    with Session() as session:
        data = session.query(PaymentMethod).all()
    print(f"   ✅ {len(data)} payment methods extraídos")
    return [row.__dict__ for row in data]

# --- PROYECTOS ---
@task(name="Extract Projects")
def extract_projects():
    print("📥 Extrayendo projects...")
    Session = sessionmaker(bind=engine_proyectos)
    with Session() as session:
        data = session.query(Project).all()
    print(f"   ✅ {len(data)} projects extraídos")
    return [row.__dict__ for row in data]

@task(name="Extract Tasks")
def extract_tasks():
    print("📥 Extrayendo tasks...")
    Session = sessionmaker(bind=engine_proyectos)
    with Session() as session:
        data = session.query(Task).all()
    print(f"   ✅ {len(data)} tasks extraídas")
    return [row.__dict__ for row in data]

@task(name="Extract Phases")
def extract_phases():
    print("📥 Extrayendo phases...")
    Session = sessionmaker(bind=engine_proyectos)
    with Session() as session:
        data = session.query(Phase).all()
    print(f"   ✅ {len(data)} phases extraídas")
    return [row.__dict__ for row in data]

@task(name="Extract User Role Projects")
def extract_user_role_projects():
    print("📥 Extrayendo user role projects...")
    Session = sessionmaker(bind=engine_proyectos)
    with Session() as session:
        data = session.query(UserRoleProject).all()
    print(f"   ✅ {len(data)} user role projects extraídos")
    return [row.__dict__ for row in data]

# --- PLANIFIKA ---
@task(name="Extract Users Planifika")
def extract_users_planifika():
    print("📥 Extrayendo users planifika...")
    Session = sessionmaker(bind=engine_planifika)
    with Session() as session:
        data = session.query(UserPlanifika).all()
    print(f"   ✅ {len(data)} users extraídos")
    return [row.__dict__ for row in data]

# --- DRIMSOFT ---
@task(name="Extract Users Drimsoft")
def extract_users_drimsoft():
    print("📥 Extrayendo users drimsoft...")
    Session = sessionmaker(bind=engine_drimsoft)
    with Session() as session:
        data = session.query(UserDrimsoft).all()
    print(f"   ✅ {len(data)} users drimsoft extraídos")
    return [row.__dict__ for row in data]

@task(name="Extract Tickets Support")
def extract_tickets_support():
    print("📥 Extrayendo tickets support...")
    Session = sessionmaker(bind=engine_drimsoft)
    with Session() as session:
        data = session.query(TicketSupport).all()
    print(f"   ✅ {len(data)} tickets extraídos")
    return [row.__dict__ for row in data]

# ====================== LOAD ======================

@task(name="Load to Warehouse")
def load_to_warehouse(table_name: str, data: list):
    if not data:
        print(f"⚠️  No hay datos para cargar en {table_name}")
        return
    
    print(f"📤 Cargando datos en {table_name}...")
    df = pd.DataFrame(data)
    
    # Limpiar columnas de SQLAlchemy
    df = df.drop(columns=['_sa_instance_state'], errors='ignore')
    
    # Cargar en el warehouse
    df.to_sql(
        table_name, 
        con=engine_warehouse, 
        if_exists='replace',  # Cambia a 'append' si quieres acumular datos
        index=False
    )
    
    print(f"   ✅ {len(df)} registros cargados en {table_name}")

# ====================== FLOW PRINCIPAL ======================

@flow(name="ETL Pipeline Completo - Drimsoft Data Lake")
def etl_pipeline_completo():
    """
    Pipeline ETL que extrae datos de 4 bases de datos Supabase
    y los consolida en un Data Warehouse PostgreSQL local
    """
    
    print("\n" + "="*60)
    print("🚀 INICIANDO ETL PIPELINE COMPLETO")
    print("="*60 + "\n")
    
    # ========== EXTRACT ==========
    print("📦 FASE 1: EXTRACCIÓN DE DATOS")
    print("-" * 60)
    
    # Suscripciones
    invoices = extract_invoices()
    subscriptions = extract_subscriptions()
    payment_methods = extract_payment_methods()
    
    # Proyectos
    projects = extract_projects()
    tasks = extract_tasks()
    phases = extract_phases()
    user_role_projects = extract_user_role_projects()
    
    # Planifika
    users_planifika = extract_users_planifika()
    
    # Drimsoft
    users_drimsoft = extract_users_drimsoft()
    tickets_support = extract_tickets_support()
    
    # ========== LOAD ==========
    print("\n📦 FASE 2: CARGA AL DATA WAREHOUSE")
    print("-" * 60)
    
    # Cargar Suscripciones
    load_to_warehouse("invoice", invoices)
    load_to_warehouse("subscription", subscriptions)
    load_to_warehouse("paymentmethod", payment_methods)
    
    # Cargar Proyectos
    load_to_warehouse("project", projects)
    load_to_warehouse("task", tasks)
    load_to_warehouse("phase", phases)
    load_to_warehouse("userroleproject", user_role_projects)
    
    # Cargar Planifika
    load_to_warehouse("userplanifika", users_planifika)
    
    # Cargar Drimsoft
    load_to_warehouse("userdrimsoft", users_drimsoft)
    load_to_warehouse("ticketsupport", tickets_support)
    
    print("\n" + "="*60)
    print("✅ ETL PIPELINE COMPLETADO EXITOSAMENTE")
    print("="*60 + "\n")

# ====================== EJECUCIÓN ======================

if __name__ == "__main__":
    etl_pipeline_completo()