from src.main import app
from faker import Faker
from faker import Faker
import random
import time
import json

# Clase que contiene la logica de las pruebas del servicio
class TestResources():
    
    # Declaración constantes
    dataFactory = Faker()
    name = None
    rol = None
    type = None
    template = None
    description = None
    created_by = None
    data = {}
    create_notification_rs = {}
    get_notifications_rs = {}
    get_notification_by_id_rs = {}

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
                        "data": {
                            "name": f"{self.name}",
                            "rol": f"{self.rol}",
                            "type": f"{self.type}",
                            "template": f"{self.template}",
                            "description": f"{self.description}",
                            "created_by": self.created_by
                        }
                    }
            
    # Función que consume el api para la creación de una notificación
    def execute_create_notification(self, data):
        with app.test_client() as test_client:
            self.create_notification_rs = test_client.post(
                '/api/v1/notifications', json=data
            )

    # Función que valida la creación exitosa de una notificación
    def validate_create_success_notification(self): 
        assert self.create_notification_rs.status_code == 201
        response_json = json.loads(self.create_notification_rs.data)["data"]
        assert 'id' in response_json
        assert 'created_at' in response_json
        assert 'updated_at' in response_json
        assert 'status' in response_json
        assert response_json['name'] == self.name
        assert response_json['rol'] == self.rol
        assert response_json['type'] == self.type
        assert response_json['template'] == self.template
        assert response_json['description'] == self.description
        assert response_json['created_by'] == self.created_by

 # Función que consume el api para la consulta de notificaciones
    def execute_get_notifications(self):
        with app.test_client() as test_client:
            self.get_notifications_rs = test_client.get(
                '/api/v1/notifications'
            )

 # Función que consume el api para la consulta de notificaciones
    def execute_get_notification_by_id(self, notificationId):
        with app.test_client() as test_client:
            self.get_notification_by_id_rs = test_client.get(
                f"/api/v1/notifications/{notificationId}"
            )
       
    # Función que valida la creación exitosa de una notificación
    def test_create_success_notification(self):
        # Generación data aleatoria 
        self.set_up()
        # Creación nuevo notificación
        self.execute_create_notification(self.data)        
        # Validación creación exitosa
        self.validate_create_success_notification()        

    # Función que valida la consulta exitosa de notificaciones
    def test_get_notifications(self):
        iterations = 10
        for i in range(iterations):
            # Generación data aleatoria 
            self.set_up()
            # Creación nueva notificación
            self.execute_create_notification(self.data)  

        self.execute_get_notifications()
        assert self.get_notifications_rs.status_code == 200
        response_json = json.loads(self.get_notifications_rs.data)["data"]
        assert len(response_json) >= iterations
        assert json.loads(self.create_notification_rs.data)["data"] in response_json
        
    # Función que valida la consulta exitosa de notificaciones
    def test_get_notification_by_id(self):
        # Generación data aleatoria 
        self.set_up()
        # Creación nueva notificación
        self.execute_create_notification(self.data)
        notification_created = json.loads(self.create_notification_rs.data)["data"] 
        # Consulta de notificación 
        self.execute_get_notification_by_id(notification_created["id"])
        assert self.get_notification_by_id_rs.status_code == 200
        response_json = json.loads(self.get_notification_by_id_rs.data)["data"]
        assert notification_created["id"] == response_json["id"]
        assert notification_created["name"] == response_json["name"]
        assert notification_created["rol"] == response_json["rol"]
        assert notification_created["type"] == response_json["type"]
        assert notification_created["template"] == response_json["template"]
        assert notification_created["description"] == response_json["description"]
        assert notification_created["status"] == response_json["status"]
        assert notification_created["status"] == response_json["status"]
        assert notification_created["created_by"] == response_json["created_by"]
        assert notification_created["updated_at"] == response_json["updated_at"]    