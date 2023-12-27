from src.queries.get_by_id import GetNotificationById
from src.commands.create import CreateNotification
from faker import Faker
import random
import time
import src.main

# Clase que contiene la logica de las pruebas del servicio
class TestGetById():
    
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
            
    # Función realiza creación exitosa de una notificación
    def create_notification(self):
        # Creación de notificación
        self.set_up()
        notification = CreateNotification(self.data).execute()
        assert notification != None
        self.created_notification = notification
        
    # Función que valida la respuesta cuando no hay notificaciones registradas
    def test_notification_not_found(self):
        try:
            GetNotificationById(1000000).query()
        except Exception as e:
            assert e.code == 404      

   # Función que valida la consulta exitosa de notificaciones
    def test_get_notification(self):
        iterations = 10
        for i in range(iterations):
            self.create_notification()
        notification = GetNotificationById(self.created_notification["id"]).query()
        assert notification != None
        assert self.created_notification["id"] == notification["id"]
        assert self.created_notification["name"] == notification["name"]
        assert self.created_notification["rol"] == notification["rol"]
        assert self.created_notification["type"] == notification["type"]
        assert self.created_notification["template"] == notification["template"]
        assert self.created_notification["description"] == notification["description"]
        assert self.created_notification["status"] == notification["status"]
        assert self.created_notification["status"] == notification["status"]
        assert self.created_notification["created_by"] == notification["created_by"]
        assert self.created_notification["updated_at"] == notification["updated_at"]