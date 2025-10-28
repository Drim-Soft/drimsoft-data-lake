from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pandas as pd
import time

from models.suscripciones_models import Invoice, Subscription, PaymentMethod, SubscriptionStatus, Currency
from models.proyectos_models import Project, Task, Phase, UserRoleProject, Methodology, ProjectStatus, TaskStatus, RoleProyecto
from models.planifika_models import UserPlanifika
from models.drimsoft_models import UserDrimsoft, TicketSupport, TicketStatus, RoleDrimsoft, UserStatusDrimsoft

from main import engine_suscripciones, engine_proyectos, engine_planifika, engine_drimsoft

# Warehouse
WAREHOUSE_URI = "postgresql+psycopg2://warehouse:warehouse123@localhost:5433/warehouse"
engine_warehouse = create_engine(WAREHOUSE_URI)

def extract_and_load(engine_source, model_class, warehouse_table_name):
    """Extrae de BD origen y carga al warehouse"""
    print(f"🔥 {warehouse_table_name}...", end=" ")
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
        df.to_sql(warehouse_table_name, con=engine_warehouse, if_exists='replace', index=False)
        print(f"✅ {len(df)} registros")
        
    except Exception as e:
        error_msg = str(e).split('\n')[0][:100]
        print(f"❌ {error_msg}")

def main():
    print("\n" + "="*70)
    print("🚀 ETL PIPELINE COMPLETO - DRIMSOFT DATA LAKE")
    print("="*70 + "\n")
    
    # ==================== DRIMSOFT ====================
    print("📦 DRIMSOFT:")
    try:
        extract_and_load(engine_drimsoft, UserDrimsoft, "drimsoft_user")
        extract_and_load(engine_drimsoft, TicketSupport, "drimsoft_ticket")
        extract_and_load(engine_drimsoft, TicketStatus, "drimsoft_ticketstatus")
        extract_and_load(engine_drimsoft, RoleDrimsoft, "drimsoft_role")
        extract_and_load(engine_drimsoft, UserStatusDrimsoft, "drimsoft_userstatus")
        print("   ✅ Drimsoft completado\n")
    except Exception as e:
        print(f"   ❌ Error en Drimsoft: {e}\n")
    
    # ==================== PLANIFIKA ====================
    print("📦 PLANIFIKA:")
    print("⏳ Esperando 3 segundos...")
    time.sleep(3)
    
    try:
        extract_and_load(engine_planifika, UserPlanifika, "planifika_user")
        print("   ✅ Planifika completado\n")
    except Exception as e:
        print(f"   ❌ Error en Planifika: {e}\n")
    
    # ==================== SUSCRIPCIONES ====================
    print("📦 SUSCRIPCIONES:")
    print("⏳ Esperando 3 segundos...")
    time.sleep(3)
    
    try:
        extract_and_load(engine_suscripciones, Invoice, "suscripciones_invoice")
        extract_and_load(engine_suscripciones, Subscription, "suscripciones_subscription")
        extract_and_load(engine_suscripciones, PaymentMethod, "suscripciones_paymentmethod")
        extract_and_load(engine_suscripciones, SubscriptionStatus, "suscripciones_subscriptionstatus")
        extract_and_load(engine_suscripciones, Currency, "suscripciones_currency")
        print("   ✅ Suscripciones completado\n")
    except Exception as e:
        print(f"   ❌ Error en Suscripciones: {e}\n")
    
    # ==================== PROYECTOS ====================
    print("📦 PROYECTOS:")
    print("⏳ Esperando 5 segundos...")
    time.sleep(5)
    
    try:
        extract_and_load(engine_proyectos, Methodology, "proyectos_methodology")
        extract_and_load(engine_proyectos, ProjectStatus, "proyectos_projectstatus")
        extract_and_load(engine_proyectos, Project, "proyectos_project")
        extract_and_load(engine_proyectos, Phase, "proyectos_phase")
        extract_and_load(engine_proyectos, TaskStatus, "proyectos_taskstatus")
        extract_and_load(engine_proyectos, Task, "proyectos_task")
        extract_and_load(engine_proyectos, RoleProyecto, "proyectos_role")  # ← Nombre único
        extract_and_load(engine_proyectos, UserRoleProject, "proyectos_userroleproject")
        print("   ✅ Proyectos completado\n")
    except Exception as e:
        print(f"   ⚠️  Proyectos error: {str(e)[:100]}\n")
    
    print("="*70)
    print("✅ PIPELINE COMPLETADO")
    print("="*70)
    print("\n📊 Resumen:")
    print("   • DRIMSOFT: 5 tablas (user, ticket, ticketstatus, role, userstatus)")
    print("   • PLANIFIKA: 1 tabla (user)")
    print("   • SUSCRIPCIONES: 5 tablas (invoice, subscription, paymentmethod, subscriptionstatus, currency)")
    print("   • PROYECTOS: 8 tablas (methodology, projectstatus, project, phase, taskstatus, task, role, userroleproject)")
    print("   • TOTAL: 19 tablas en el warehouse\n")
    print("💡 Nota: Las tablas tienen prefijos únicos (drimsoft_, planifika_, etc.)")
    print("   para evitar conflictos de nombres\n")

if __name__ == "__main__":
    main()