from src.commands.create import CreateNotification
from faker import Faker
import random
import time
import src.main

# Clase que contiene la logica de las pruebas del servicio
class TestCreate():
    
    # Declaración constantes
    dataFactory = Faker()
    name = None
    rol = None
    type = None
    template = None
    description = None
    created_by = None
    data = {}

    # Función que genera data del usuario
    def set_up(self):
        list_roles = ["Administrador", "Auxilar administrativo", "Conductor"]
        list_not_type = ["Cambio de fechas en el Booking", "Cargue exitoso", "La bodega ya puede recibir el contenedor", "Orden cerrada"]
        self.name = f"Notificación {int(time.time() * 1000)}"
        self.rol = random.choice(list_roles)
        self.type = f"Notificación - {random.choice(list_not_type)}"
        self.template = self.dataFactory.sentence(nb_words=10)
        self.description = self.dataFactory.sentence(nb_words=5)
        self.created_by = self.dataFactory.random_int(100, 1000)
        self.data = {
                        "data": {
                            "name": f"{self.name}",
                            "rol": f"{self.rol}",
                            "type": f"{self.type}",
                            "template": f"{self.template}",
                            "description": f"{self.description}",
                            "created_by": self.created_by
                        }
                    }
            
    # Función que valida la creación exitosa de una notificación
    def test_create_notification(self):
        # Creación de notificación
        self.set_up()
        assert CreateNotification(self.data).execute() != None
    
    # Función que valida la creación de una notificación ya registrada
    def test_create_existing_notification(self):
        try:
            # Creación notificación
            self.set_up()
            assert CreateNotification(self.data).execute() != None
            # Creación notificación existente
            CreateNotification(self.data).execute()
        except Exception as e:
            assert e.code == 409
   
    # Función que valida la creación de una notificaión cuando se envia un request invalido
    def test_create_notification_bad_request(self):
        try:
            # Creación notificación
            self.set_up()
            data = {
                        "data": {
                            "name": f"{self.name}",
                            "rol": f"{self.rol}",
                            "type": f"{self.type}"
                        }
                    }
            # Creación usuario con data incompleta
            CreateNotification(data).execute()
        except Exception as e:
            assert e.code == 400        