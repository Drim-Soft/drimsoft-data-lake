FROM apache/superset:latest

# Instalar dependencias adicionales necesarias
RUN pip install --no-cache-dir psycopg2-binary redis sqlalchemy
