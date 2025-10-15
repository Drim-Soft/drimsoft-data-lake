FROM apache/superset:latest

RUN pip install --no-cache-dir psycopg2-binary redis sqlalchemy
