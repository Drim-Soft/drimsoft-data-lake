from sqlalchemy import create_engine, text

# Cambia tu contraseña aquí
engine = create_engine("postgresql+psycopg2://warehouse:warehouse123@localhost:5433/warehouse")

with engine.connect() as conn:
    result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public';"))
    print("\n📊 Tablas en el esquema 'public':\n")
    for row in result:
        print(" -", row[0])
