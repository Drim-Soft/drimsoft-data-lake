from sqlalchemy.ext.declarative import declarative_base

# Base global compartida por todos los modelos
Base = declarative_base()

# Importar todos los modelos aquí 👇
from .suscripciones_models import *
from .proyectos_models import *
from .planifika_models import *
# from .drimsoft_models import *  # si luego creas uno
