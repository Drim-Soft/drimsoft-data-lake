

# Dashboard Drimsoft - Data Lake

## Descripción

Este proyecto implementa un **Data Lake** con PostgreSQL y un dashboard interactivo usando **Apache Superset**. Además, se cuenta con flujos de ETL automatizados mediante **Prefect** para generar y cargar datos de ventas en PostgreSQL.

Se utiliza **pgAdmin** para administrar las bases de datos y verificar que los datos estén correctamente cargados.

---

## Contenedores y servicios

| Servicio     | Imagen                   | Puerto    | Usuario/Contraseña                                   |
| ------------ | ------------------------ | --------- | ---------------------------------------------------- |
| Warehouse DB | postgres:15              | 5433:5432 | warehouse / warehouse123                             |
| Superset DB  | postgres:15              | 5432/tcp  | superset / superset                                  |
| Superset     | apache/superset:3.1.1    | 8088:8088 | admin / admin123                                     |
| Prefect      | prefecthq/prefect:2.19.4 | 4200:4200 | —                                                    |
| Redis        | redis:7                  | 6379/tcp  | —                                                    |
| pgAdmin      | dpage/pgadmin4:latest    | 5050:80   | [admin@admin.com](mailto:admin@admin.com) / admin123 |

Red de Docker: `drimsoft-data-lake_datalake` con subnet `172.19.0.0/16`.

---

## Problemas y errores encontrados

1. **Tabla `ventas` no existía en la base de datos**

   * Error: `relation "ventas" does not exist`.
   * Solución: ejecutar `etl_simple.py` para crear la tabla y cargar datos de prueba en la base de datos `warehouse`.

2. **Conexión a PostgreSQL desde Superset**

   * Error: no aparecían datos al hacer query.
   * Solución: revisar `host`, `port`, `database`, `user` y `password`. En Docker, para el contenedor `warehouse` se debe usar `localhost` con el puerto mapeado `5433`, o el nombre del contenedor si se hace desde otro contenedor (`warehouse:5432`).

3. **pgAdmin no mostraba la tabla `ventas`**

   * Error: conectábamos a otra base por defecto.
   * Solución: asegurarse de seleccionar la base de datos correcta (`warehouse`) al registrar la conexión.

4. **Problemas con Display Name en Superset**

   * Error: la conexión se veía como `Backend AQE DML CSV upload Expose in SQL Lab`.
   * Solución: el `Display Name` es solo descriptivo y **no afecta la conexión real**.

5. **ETL y Prefect**

   * Error: sin instalar `psycopg2-binary` o `prefect` daba fallos al correr el flujo.
   * Solución: instalar dependencias correctas:

     ```bash
     pip install psycopg2-binary prefect pandas SQLAlchemy
     ```

6. **Problemas con el puerto de PostgreSQL**

   * Si ejecutabas scripts de Python, asegurarte de que usan el puerto correcto (`5433` para `warehouse`, `5432` para `superset-db`).

---

## Flujo de trabajo

1. Levantar todos los contenedores:

```bash
docker compose up -d --build
```

2. Crear la tabla y cargar datos de prueba:

```bash
python etl_simple.py
```

3. Verificar los datos en **pgAdmin**:

* URL: `http://localhost:5050`
* Conectar a la base `warehouse`.
* Comprobar la tabla `ventas`.

4. Crear dashboards en **Superset**:

* URL: `http://localhost:8088`
* Usuario: `admin`, Contraseña: `admin123`.
* Registrar conexión a `warehouse`.
* Crear gráficos (bar, pie, line) usando columnas como `producto`, `categoria`, `total`, `ciudad`.

---

## Dependencias (requirements.txt)

```txt
psycopg2-binary==2.9.11
prefect==3.4.23
pandas==2.1.1
SQLAlchemy==2.0.44
```

---

## Aprendizajes clave

* Siempre verificar **host y puerto** cuando los servicios están en Docker.
* La base de datos por defecto puede variar; siempre especificar `database` en scripts de Python y Superset.
* `Display Name` en Superset es solo visual, no afecta la conexión.
* Prefect y scripts ETL requieren instalar dependencias correctas (`psycopg2-binary`, `pandas`, `SQLAlchemy`).
* Antes de crear dashboards, asegurarse que las tablas existan y tengan datos.

