import os
from dotenv import load_dotenv

# Cargar variables del .env
load_dotenv()

DB_URI_SUSCRIPCIONES = f"postgresql://{os.getenv('CUBSCRIPTIONS_DB_USER')}:{os.getenv('CUBSCRIPTIONS_DB_PASSWORD')}@aws-1-us-east-1.pooler.supabase.com:6543/postgres"
DB_URI_PLANIFIKA = f"postgresql://{os.getenv('PLANIFIKA_DB_USER')}:{os.getenv('PLANIFIKA_DB_PASSWORD')}@aws-1-us-east-1.pooler.supabase.com:6543/postgres"
DB_URI_DRIMSOFT = f"postgresql://{os.getenv('DRIMSOFT_DB_USER')}:{os.getenv('DRIMSOFT_DB_PASSWORD')}@aws-1-us-east-2.pooler.supabase.com:6543/postgres"
DB_URI_PROYECTOS = f"postgresql://{os.getenv('PROJECTS_DB_USER')}:{os.getenv('PROJECTS_DB_PASSWORD')}@aws-1-us-east-1.pooler.supabase.com:6543/postgres"
