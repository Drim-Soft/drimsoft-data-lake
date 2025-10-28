from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, inspect
import pandas as pd

from models.suscripciones_models import Invoice, Subscription, PaymentMethod
from models.proyectos_models import Project, Task, Phase, UserRoleProject
from models.planifika_models import UserPlanifika
from models.drimsoft_models import UserDrimsoft, TicketSupport

from main import engine_suscripciones, engine_proyectos, engine_planifika, engine_drimsoft

# Warehouse
WAREHOUSE_URI = "postgresql+psycopg2://warehouse:warehouse123@localhost:5433/warehouse"
engine_warehouse = create_engine(WAREHOUSE_URI)

def extract_and_load(engine_source, model_class):
    """Extrae de BD origen y carga al warehouse usando el __tablename__ del modelo"""
    table_name = model_class.__tablename__
    print(f"📥 {table_name}...", end=" ")
    Session = sessionmaker(bind=engine_source)
    
    try:
        with Session() as session:
            data = session.query(model_class).all()
            
        if not data:
            print(f"⚠️  Sin datos")
            return
        
        # Convertir a DataFrame
        df = pd.DataFrame([row.__dict__ for row in data])
        df = df.drop(columns=['_sa_instance_state'], errors='ignore')
        
        # Cargar al warehouse
        df.to_sql(table_name, con=engine_warehouse, if_exists='replace', index=False)
        print(f"✅ {len(df)} registros")
        
    except Exception as e:
        print(f"❌ {str(e)[:80]}")

def main():
    print("\n" + "="*60)
    print("🚀 ETL PIPELINE - DRIMSOFT DATA LAKE")
    print("="*60 + "\n")
    
    print("📦 SUSCRIPCIONES:")
    extract_and_load(engine_suscripciones, Invoice)
    extract_and_load(engine_suscripciones, Subscription)
    extract_and_load(engine_suscripciones, PaymentMethod)
    
    print("\n📦 PROYECTOS:")
    extract_and_load(engine_proyectos, Project)
    extract_and_load(engine_proyectos, Task)
    extract_and_load(engine_proyectos, Phase)
    extract_and_load(engine_proyectos, UserRoleProject)
    
    print("\n📦 PLANIFIKA:")
    extract_and_load(engine_planifika, UserPlanifika)
    
    print("\n📦 DRIMSOFT:")
    extract_and_load(engine_drimsoft, UserDrimsoft)
    extract_and_load(engine_drimsoft, TicketSupport)
    
    print("\n" + "="*60)
    print("✅ PIPELINE COMPLETADO")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()