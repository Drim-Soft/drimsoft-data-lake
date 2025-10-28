from sqlalchemy import create_engine, text, inspect
import pandas as pd

from main import engine_suscripciones, engine_drimsoft

def inspect_table_structure(engine, table_name, db_name):
    """Muestra la estructura real de una tabla"""
    print(f"\n{'='*70}")
    print(f"📋 Estructura de: {db_name}.{table_name}")
    print('='*70)
    
    try:
        # Obtener columnas
        query = f"""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = '{table_name}'
        ORDER BY ordinal_position;
        """
        df = pd.read_sql(query, engine)
        
        if df.empty:
            print(f"❌ Tabla '{table_name}' no existe")
            return
        
        print(f"\nColumnas encontradas:")
        for _, row in df.iterrows():
            nullable = "NULL" if row['is_nullable'] == 'YES' else "NOT NULL"
            print(f"  • {row['column_name']:30} {row['data_type']:15} {nullable}")
        
        # Mostrar 2 filas de ejemplo
        sample_query = f"SELECT * FROM {table_name} LIMIT 2"
        sample_df = pd.read_sql(sample_query, engine)
        
        if not sample_df.empty:
            print(f"\n📊 Datos de ejemplo ({len(sample_df)} filas):")
            print(sample_df.to_string(index=False))
        else:
            print("\n⚠️  Tabla vacía (sin datos)")
            
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("\n" + "="*70)
    print("🔍 INSPECCIÓN DE TABLAS EN SUPABASE")
    print("="*70)
    
    # DRIMSOFT
    print("\n📦 BASE DE DATOS: DRIMSOFT")
    inspect_table_structure(engine_drimsoft, "userdrimsoft", "drimsoft")
    inspect_table_structure(engine_drimsoft, "ticketsupport", "drimsoft")
    inspect_table_structure(engine_drimsoft, "role", "drimsoft")
    inspect_table_structure(engine_drimsoft, "userstatus", "drimsoft")
    inspect_table_structure(engine_drimsoft, "ticketstatus", "drimsoft")
    
    # SUSCRIPCIONES
    print("\n\n📦 BASE DE DATOS: SUSCRIPCIONES")
    inspect_table_structure(engine_suscripciones, "invoice", "suscripciones")
    inspect_table_structure(engine_suscripciones, "subscription", "suscripciones")
    inspect_table_structure(engine_suscripciones, "paymentmethod", "suscripciones")
    inspect_table_structure(engine_suscripciones, "subscriptionstatus", "suscripciones")
    inspect_table_structure(engine_suscripciones, "currency", "suscripciones")
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()