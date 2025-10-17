from plantilla_base_etl import BaseETL

class ProyectosETL(BaseETL):
    def __init__(self):
        uri = "postgresql://usuario:contraseña@host:5432/proyectos"
        super().__init__(uri, "Proyectos")

    # Aquí puedes poner métodos personalizados si esta base requiere lógica extra
    # def transformar_proyectos(self, df):
    #     ...
