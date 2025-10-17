from plantilla_base_etl import BaseETL

class SubcripcionesETL(BaseETL):
    def __init__(self):
        uri = "postgresql://usuario:contraseña@host:5432/subcripciones"
        super().__init__(uri, "Subcripciones")

