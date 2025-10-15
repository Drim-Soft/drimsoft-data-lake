"""
ETL Pipeline: Genera datos de ventas y los carga en PostgreSQL
Ejecutar: python etl_ventas.py
"""

from prefect import flow, task
import psycopg2
from datetime import datetime, timedelta
import random

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'port': 5433,
    'database': 'warehouse',
    'user': 'warehouse',
    'password': 'warehouse123'
}

@task(name="Crear tabla en warehouse")
def crear_tabla():
    """Crea la tabla de ventas si no existe"""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ventas (
            id SERIAL PRIMARY KEY,
            fecha DATE NOT NULL,
            producto VARCHAR(100) NOT NULL,
            categoria VARCHAR(50) NOT NULL,
            cantidad INTEGER NOT NULL,
            precio_unitario DECIMAL(10,2) NOT NULL,
            total DECIMAL(10,2) NOT NULL,
            ciudad VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Tabla 'ventas' creada exitosamente")

@task(name="Generar datos de ventas")
def generar_datos(num_registros=100):
    """Genera datos de ventas aleatorios"""
    
    productos = {
        'Laptop': ('Electrónica', 800, 1500),
        'Mouse': ('Electrónica', 10, 50),
        'Teclado': ('Electrónica', 20, 100),
        'Monitor': ('Electrónica', 150, 400),
        'Silla Gamer': ('Muebles', 100, 300),
        'Escritorio': ('Muebles', 150, 500),
        'Audífonos': ('Electrónica', 30, 150),
        'Webcam': ('Electrónica', 40, 120),
        'Lámpara LED': ('Iluminación', 15, 60),
        'Mousepad': ('Accesorios', 5, 25)
    }
    
    ciudades = ['Bogotá', 'Medellín', 'Cali', 'Barranquilla', 'Cartagena']
    
    ventas = []
    fecha_inicio = datetime.now() - timedelta(days=90)  # Últimos 90 días
    
    for _ in range(num_registros):
        producto = random.choice(list(productos.keys()))
        categoria, precio_min, precio_max = productos[producto]
        
        cantidad = random.randint(1, 10)
        precio_unitario = round(random.uniform(precio_min, precio_max), 2)
        total = round(cantidad * precio_unitario, 2)
        
        fecha = fecha_inicio + timedelta(days=random.randint(0, 90))
        ciudad = random.choice(ciudades)
        
        ventas.append({
            'fecha': fecha.date(),
            'producto': producto,
            'categoria': categoria,
            'cantidad': cantidad,
            'precio_unitario': precio_unitario,
            'total': total,
            'ciudad': ciudad
        })
    
    print(f"✅ Generados {len(ventas)} registros de ventas")
    return ventas

@task(name="Cargar datos a PostgreSQL")
def cargar_datos(ventas):
    """Inserta los datos en la base de datos"""
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    
    # Limpiar datos antiguos (opcional)
    cur.execute("TRUNCATE TABLE ventas RESTART IDENTITY")
    
    # Insertar nuevos datos
    insert_query = """
        INSERT INTO ventas (fecha, producto, categoria, cantidad, precio_unitario, total, ciudad)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    for venta in ventas:
        cur.execute(insert_query, (
            venta['fecha'],
            venta['producto'],
            venta['categoria'],
            venta['cantidad'],
            venta['precio_unitario'],
            venta['total'],
            venta['ciudad']
        ))
    
    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ {len(ventas)} registros insertados en PostgreSQL")

@flow(name="ETL Ventas Pipeline")
def etl_ventas_pipeline(num_registros=200):
    """Pipeline completo de ETL"""
    print("🚀 Iniciando pipeline de ETL...")
    
    # 1. Crear tabla
    crear_tabla()
    
    # 2. Generar datos
    ventas = generar_datos(num_registros)
    
    # 3. Cargar a la base de datos
    cargar_datos(ventas)
    
    print("🎉 Pipeline completado exitosamente!")

if __name__ == "__main__":
    # Instalar dependencias primero:
    # pip install prefect psycopg2-binary
    
    etl_ventas_pipeline(num_registros=200)