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
            

    # Función que consume el api para la creación de una notificación
    def execute_create_notification(self, data):
        with app.test_client() as test_client:
            self.create_notification_rs = test_client.post(
                '/api/v1/notifications', json=data
            )

    # Función que valida la creación exitosa de una notificación
    def validate_create_success_notification(self): 
        response_json = json.loads(self.create_notification_rs.data)["data"]
        assert self.create_notification_rs.status_code == 201
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
        
    # Función que valida la creación exitosa de una notificación
    def test_create_success_notification(self):
        # Generación data aleatoria 
        self.set_up()
        # Creación nuevo usuario
        self.execute_create_notification(self.data)        
        # Validación creación exitosa
        self.validate_create_success_notification()        