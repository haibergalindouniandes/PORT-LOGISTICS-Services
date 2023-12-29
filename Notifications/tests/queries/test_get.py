from src.queries.get import GetNotifications
from src.commands.create import CreateNotification
from faker import Faker
import random
import time
import src.main

# Clase que contiene la logica de las pruebas del servicio
class TestGet():
    
    # Declaración constantes
    dataFactory = Faker()
    name = None
    rol = None
    type = None
    template = None
    description = None
    created_by = None
    data = {}
    created_notifications = []

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
            
    # Función realiza creación exitosa de una notificación
    def create_notification(self):
        # Creación de notificación
        self.set_up()
        notification = CreateNotification(self.data).execute()
        # assert notification != None
        self.created_notifications.append(notification)
        
    # Función que valida la respuesta cuando no hay notificaciones registradas
    def test_notifications_not_found(self):
        try:
            GetNotifications().query()
        except Exception as e:
            assert e.code == 409      

   # Función que valida la consulta exitosa de notificaciones
    def test_get_notifications(self):
        iterations = 10
        for i in range(iterations):
            self.create_notification()
        notifications = GetNotifications().query()
        assert notifications != None
        for created_notification in self.created_notifications:
            assert created_notification in notifications