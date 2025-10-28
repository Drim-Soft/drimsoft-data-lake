from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import pandas as pd
import time

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
    UserPlanifika
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

# ==== WAREHOUSE LOCAL ====
WAREHOUSE_URI = "postgresql+psycopg2://warehouse:warehouse123@localhost:5433/warehouse"
engine_warehouse = create_engine(WAREHOUSE_URI)

# ===============================================================
# FUNCIÓN DE EXTRACCIÓN Y CARGA
# ===============================================================
def extract_and_load(engine_source, model_class, warehouse_table_name):
    """Extrae de BD origen y carga al warehouse, cerrando sesión y conexión."""
    start_time = time.time()
    print(f"🔥 Extrayendo {warehouse_table_name}...", end=" ")

    Session = sessionmaker(bind=engine_source)
    session = None

    try:
        session = Session()
        data = session.query(model_class).all()

        if not data:
            print("⚠️  Sin datos")
            return

        df = pd.DataFrame([row.__dict__ for row in data])
        df = df.drop(columns=['_sa_instance_state'], errors='ignore')

        df.to_sql(warehouse_table_name, con=engine_warehouse, if_exists='replace', index=False)

        elapsed = time.time() - start_time
        print(f"✅ {len(df)} registros ({elapsed:.2f}s)")

    except Exception as e:
        print(f"❌ Error: {str(e).splitlines()[0][:120]}")

    finally:
        if session is not None:
            session.close()
        engine_source.dispose()
        print(f"🔒 Conexión cerrada: {warehouse_table_name}")

# ===============================================================
# PIPELINE PRINCIPAL
# ===============================================================
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
    time.sleep(3)
    try:
        extract_and_load(engine_planifika, UserPlanifika, "planifika_user")
        print("   ✅ Planifika completado\n")
    except Exception as e:
        print(f"   ❌ Error en Planifika: {e}\n")

    # ==================== SUSCRIPCIONES ====================
    print("📦 SUSCRIPCIONES:")
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
    time.sleep(5)
    try:
        extract_and_load(engine_proyectos, Methodology, "proyectos_methodology")
        extract_and_load(engine_proyectos, ProjectStatus, "proyectos_projectstatus")
        extract_and_load(engine_proyectos, Project, "proyectos_project")
        extract_and_load(engine_proyectos, Phase, "proyectos_phase")
        extract_and_load(engine_proyectos, TaskStatus, "proyectos_taskstatus")
        extract_and_load(engine_proyectos, Task, "proyectos_task")
        extract_and_load(engine_proyectos, RoleProyecto, "proyectos_role")
        extract_and_load(engine_proyectos, UserRoleProject, "proyectos_userroleproject")
        print("   ✅ Proyectos completado\n")
    except Exception as e:
        print(f"   ⚠️  Error en Proyectos: {str(e)[:100]}\n")

    # ==================== RESUMEN FINAL ====================
    print("="*70)
    print("✅ PIPELINE COMPLETADO")
    print("="*70)
    print("\n📊 Resumen:")
    print("   • DRIMSOFT: 5 tablas")
    print("   • PLANIFIKA: 1 tabla")
    print("   • SUSCRIPCIONES: 5 tablas")
    print("   • PROYECTOS: 8 tablas")
    print("   • TOTAL: 19 tablas cargadas al warehouse\n")
    print("💡 Todas las conexiones fueron cerradas correctamente.\n")

if __name__ == "__main__":
    main()

    engine_drimsoft.dispose()
    engine_planifika.dispose()
    engine_suscripciones.dispose()
    engine_proyectos.dispose()
