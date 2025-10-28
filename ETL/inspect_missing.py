from sqlalchemy import text
import pandas as pd

from main import engine_suscripciones, engine_proyectos, engine_planifika

def inspect_table(engine, table_name, db_name):
    print(f"\n{'='*70}")
    print(f"📋 {db_name}.{table_name}")
    print('='*70)
    
    try:
        query = f"""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = '{table_name}'
        ORDER BY ordinal_position;
        """
        df = pd.read_sql(query, engine)
        
        if df.empty:
            print(f"❌ Tabla no existe")
            return
        
        print("Columnas:")
        for _, row in df.iterrows():
            print(f"  • {row['column_name']:30} {row['data_type']}")
        
        # Muestra de datos
        sample = pd.read_sql(f"SELECT * FROM {table_name} LIMIT 2", engine)
        if not sample.empty:
            print(f"\n📊 Ejemplo ({len(sample)} filas):")
            print(sample.to_string(index=False))
        else:
            print("\n⚠️  Sin datos")
            
    except Exception as e:
        print(f"❌ Error: {e}")

# SUSCRIPCIONES
print("\n📦 SUSCRIPCIONES")
inspect_table(engine_suscripciones, "subscription", "suscripciones")

# PROYECTOS
print("\n\n📦 PROYECTOS")
inspect_table(engine_proyectos, "userroleproject", "proyectos")
inspect_table(engine_proyectos, "role", "proyectos")

# PLANIFIKA (si conecta)
print("\n\n📦 PLANIFIKA")
try:
    inspect_table(engine_planifika, "userplanifika", "planifika")
    inspect_table(engine_planifika, "userstatus", "planifika")
except Exception as e:
    print(f"⚠️  No se pudo conectar: {str(e)[:80]}")