from plantilla_base_etl import BaseETL

class UsuariosDrimsoftETL(BaseETL):
    def __init__(self):
        uri = "postgresql://usuario:contraseña@host:5432/usuarios_drimsoft"
        super().__init__(uri, "Usuarios Drimsoft")
