from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool

DB_URI_DRIMSOFT = "postgresql://postgres.zqbwjlrlnxjlrusmmciw:Drimsoft2025.@aws-1-us-east-2.pooler.supabase.com:6543/postgres?sslmode=require"

def test_connection():
    print("🔌 Intentando conectar a Drimsoft (us-east-2)...")
    
    # Usar NullPool para no mantener conexiones abiertas
    engine = create_engine(
        DB_URI_DRIMSOFT, 
        poolclass=NullPool,
        pool_pre_ping=True
    )
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            print("\n✅ ¡Conexión exitosa a Drimsoft!")
            print(f"PostgreSQL version: {result.fetchone()[0]}")
            
            # Ver qué tablas hay
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            tables = result.fetchall()
            print(f"\n📊 Tablas encontradas ({len(tables)}):")
            for table in tables:
                print(f"  - {table[0]}")
                
    except Exception as e:
        print(f"\n❌ Error de conexión: {e}")
        print("\n💡 Sugerencia: Espera 30 segundos y vuelve a intentar")
        print("   Las conexiones de Supabase free tier son limitadas")
    finally:
        # Asegurar que el engine se cierre
        engine.dispose()
        print("\n🔒 Conexión cerrada correctamente")

if __name__ == "__main__":
    test_connection()