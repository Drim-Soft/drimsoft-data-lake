from prefect import flow, task
import psycopg2
import pandas as pd
from sqlalchemy import create_engine

# 🗄️ Conexiones externas
DB1_URI = "postgresql://user1:password1@host1:5432/db1"
DB2_URI = "postgresql://user2:password2@host2:5432/db2"

# 🏪 Data Warehouse
DWH_URI = "postgresql://warehouse:warehouse123@warehouse:5432/warehouse"

@task
def extraer_db(uri, query):
    engine = create_engine(uri)
    df = pd.read_sql(query, engine)
    engine.dispose()
    return df

@task
def transformar(df1, df2):
    # Ejemplo simple: concatenar datos
    df = pd.concat([df1, df2], ignore_index=True)
    return df

@task
def cargar(df, tabla):
    engine = create_engine(DWH_URI)
    df.to_sql(tabla, engine, if_exists='replace', index=False)
    engine.dispose()

@flow(name="ETL desde dos bases a Data Warehouse")
def etl_principal():
    q = "SELECT * FROM tu_tabla"
    df1 = extraer_db(DB1_URI, q)
    df2 = extraer_db(DB2_URI, q)
    df_final = transformar(df1, df2)
    cargar(df_final, "tabla_unificada")

if __name__ == "__main__":
    etl_principal()
