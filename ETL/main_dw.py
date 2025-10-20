
from sqlalchemy import create_engine
from models import Base  # Importa la Base y todos los modelos

# ✅ URI de conexión a tu Data Warehouse (modifica con tus datos reales)
DB_URI_DW = "postgresql+psycopg2://warehouse:warehouse123@localhost:5433/warehouse"

def create_warehouse_tables():
    """
    Crea todas las tablas definidas en los modelos dentro de la base de datos
    del Data Warehouse.
    """
    try:
        # Crear motor de conexión
        engine = create_engine(DB_URI_DW)

        # Crear todas las tablas si no existen
        Base.metadata.create_all(engine)

        print("✅ Todas las tablas fueron creadas exitosamente en el Data Warehouse.")

    except Exception as e:
        print("❌ Error al crear las tablas en el Data Warehouse:", e)

if __name__ == "__main__":
    create_warehouse_tables()
