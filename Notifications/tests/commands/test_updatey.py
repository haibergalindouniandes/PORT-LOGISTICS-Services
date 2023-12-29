from src.commands.update import UpdateNotification
from src.commands.create import CreateNotification
from faker import Faker
import random
import time
import src.main

# Clase que contiene la logica de las pruebas del servicio
class TestUpdate():
    
    # Declaración constantes
    dataFactory = Faker()
    name = None
    rol = None
    type = None
    template = None
    description = None
    created_by = None
    data = {}
    created_notification = None

    # Función que genera data de la notificación
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
                        "name": f"{self.name}",
                        "rol": f"{self.rol}",
                        "type": f"{self.type}",
                        "template": f"{self.template}",
                        "description": f"{self.description}",
                        "created_by": self.created_by
                    }
            
    # Función que valida la creación exitosa de una notificación
    def create_notification(self):
        # Creación de notificación
        self.set_up()
        notification = CreateNotification(self.data).execute()
        self.created_notification = notification
    
    # Función que valida la actualización exitosa de una notificación
    def test_update_notification(self):
        # Creación de notificación
        self.create_notification()
        # Actualización notificación
        self.set_up()
        data_to_update = self.data
        data_to_update["status"] = "Inactivo"
        updated_notification = UpdateNotification(self.created_notification["id"], data_to_update).execute()
        assert updated_notification != None
        assert self.created_notification["id"] == updated_notification["id"]
        assert data_to_update["name"] == updated_notification["name"]
        assert data_to_update["rol"] == updated_notification["rol"]
        assert data_to_update["type"] == updated_notification["type"]
        assert data_to_update["template"] == updated_notification["template"]
        assert data_to_update["description"] == updated_notification["description"]
        assert data_to_update["status"] == updated_notification["status"]
        assert data_to_update["created_by"] == updated_notification["created_by"]
    
    # Función que valida la actualización de una notificación no se encuentra registrada
    def test_update_not_existing_notification(self):
        try:
            # Actualización notificación
            self.set_up()
            UpdateNotification(10000000000, self.data).execute()
        except Exception as e:
            assert e.code == 404
   
  # Función que valida la respuesta de error cuando se envia un request invalido
    def test_update_notification_bad_request(self):
        try:
            # Creación de notificación
            self.create_notification()
            # Actualización notificación
            self.set_up()
            data_to_update = {}
            UpdateNotification(self.created_notification["id"], data_to_update).execute()
        except Exception as e:
            assert e.code == 400