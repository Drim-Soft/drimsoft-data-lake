from sqlalchemy import create_engine, text
import pandas as pd

WAREHOUSE_URI = "postgresql+psycopg2://warehouse:warehouse123@localhost:5433/warehouse"
engine = create_engine(WAREHOUSE_URI)

print("\n🔍 VERIFICANDO DATOS EN EL WAREHOUSE")
print("="*60)

with engine.connect() as conn:
    # Listar todas las tablas
    result = conn.execute(text("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name
    """))
    
    tables = [row[0] for row in result.fetchall()]
    
    print(f"\n📊 Tablas en el warehouse ({len(tables)}):\n")
    
    for table in tables:
        # Contar registros en cada tabla
        count_result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
        count = count_result.scalar()
        print(f"   • {table:30} → {count:6} registros")

print("\n" + "="*60 + "\n")