from sqlalchemy import create_engine, text
from sqlalchemy.pool import NullPool
import time

# URIs de Connection Pooling para todas las bases de datos
CONNECTIONS = {
    "DRIMSOFT": {
        "uri": "postgresql://postgres.zqbwjlrlnxjlrusmmciw:Drimsoft2025.@aws-1-us-east-2.pooler.supabase.com:6543/postgres?sslmode=require",
        "region": "us-east-2"
    },
    "PLANIFIKA": {
        "uri": "postgresql://postgres.znzlfnztvnnzfbbsdjsl:Planifika2025.@aws-1-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require",
        "region": "us-east-1"
    },
    "PROYECTOS": {
        "uri": "postgresql://postgres.rniqzbnygegbkecikbxj:Planifika2025.@aws-1-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require",
        "region": "us-east-1"
    },
    "SUSCRIPCIONES": {
        "uri": "postgresql://postgres.iwnxlkmjvxmcuscangyi:Drimsoft2025.@aws-1-us-east-1.pooler.supabase.com:6543/postgres?sslmode=require",
        "region": "us-east-1"
    }
}

def test_connection(db_name, db_info):
    """Prueba la conexión a una base de datos específica"""
    print(f"\n{'='*60}")
    print(f"🔌 Probando conexión a: {db_name} ({db_info['region']})")
    print(f"{'='*60}")
    
    engine = None
    
    try:
        engine = create_engine(
            db_info['uri'], 
            poolclass=NullPool,
            pool_pre_ping=True
        )
        
        with engine.connect() as conn:
            # Test 1: Verificar versión de PostgreSQL
            result = conn.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ Conexión exitosa!")
            print(f"   PostgreSQL: {version.split(',')[0]}")
            
            # Test 2: Contar tablas en el esquema public
            result = conn.execute(text("""
                SELECT COUNT(*) 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
            """))
            table_count = result.fetchone()[0]
            print(f"   Total de tablas: {table_count}")
            
            # Test 3: Listar todas las tablas
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public'
                ORDER BY table_name
            """))
            tables = result.fetchall()
            
            if tables:
                print(f"\n   📊 Tablas encontradas:")
                for i, table in enumerate(tables, 1):
                    print(f"      {i}. {table[0]}")
            else:
                print(f"   ⚠️  No se encontraron tablas en el esquema 'public'")
            
            # Test 4: Verificar que podemos hacer queries
            result = conn.execute(text("SELECT 1 as test;"))
            test_result = result.fetchone()[0]
            if test_result == 1:
                print(f"\n   ✅ Query test exitoso")
            
            print(f"   🔒 Cerrando conexión a {db_name}...")
            
        return True
            
    except Exception as e:
        print(f"\n   ❌ Error de conexión:")
        print(f"      {str(e)[:200]}")
        if "Max client connections reached" in str(e):
            print(f"\n   💡 Sugerencia: Espera 30 segundos y reintenta")
        elif "password authentication failed" in str(e):
            print(f"\n   💡 Sugerencia: Verifica la contraseña")
        elif "could not translate host name" in str(e):
            print(f"\n   💡 Sugerencia: Verifica la región y el host")
        return False
        
    finally:
        # CRÍTICO: Asegurar que el engine se cierre SIEMPRE
        if engine is not None:
            engine.dispose()
            print(f"   ✅ Engine de {db_name} cerrado correctamente")

def main():
    print("\n" + "="*60)
    print("🚀 PRUEBA DE CONEXIONES A SUPABASE")
    print("="*60)
    
    results = {}
    
    # Probar cada conexión
    for db_name, db_info in CONNECTIONS.items():
        success = test_connection(db_name, db_info)
        results[db_name] = success
        
        # Pequeña pausa entre conexiones para evitar límites
        time.sleep(1)
    
    # Resumen final
    print("\n" + "="*60)
    print("📊 RESUMEN DE RESULTADOS")
    print("="*60)
    
    successful = sum(results.values())
    total = len(results)
    
    for db_name, success in results.items():
        status = "✅ EXITOSA" if success else "❌ FALLIDA"
        print(f"{db_name:20} → {status}")
    
    print(f"\n{'='*60}")
    print(f"Total: {successful}/{total} conexiones exitosas")
    
    if successful == total:
        print("🎉 ¡Todas las conexiones funcionan correctamente!")
        print("🔒 Todas las conexiones han sido cerradas correctamente")
    elif successful > 0:
        print("⚠️  Algunas conexiones fallaron. Revisa los errores arriba.")
    else:
        print("❌ Todas las conexiones fallaron. Verifica las credenciales.")
    
    
    print("="*60 + "\n")
    
    return successful == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)