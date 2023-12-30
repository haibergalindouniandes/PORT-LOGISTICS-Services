from src.errors.errors import SuccessDelete
from src.commands.delete_by_id import DeleteNotificationById
from src.commands.create import CreateNotification
from faker import Faker
import random
import time
import src.main

# Clase que contiene la logica de las pruebas del servicio
class TestDeleteById():
    
    # Declaración constantes
    dataFactory = Faker()
    name = None
    rol = None
    type = None
    template = None
    description = None
    created_by = None
    data = {}

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
    def test_delete_notification(self):
        # Creación de notificación
        self.create_notification()
        deleted_notification = DeleteNotificationById(self.created_notification["id"]).execute()
        assert deleted_notification != None
        assert deleted_notification["description"] == SuccessDelete.description
    
    # Función que valida la actualización de una notificación no se encuentra registrada
    def test_delete_not_existing_notification(self):
        try:
            # Actualización notificación
            self.set_up()
            DeleteNotificationById(10000000).execute()
        except Exception as e:
            assert e.code == 404