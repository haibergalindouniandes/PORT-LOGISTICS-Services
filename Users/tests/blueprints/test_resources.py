import uuid
from src.main import app
from faker import Faker
import json

# Clase que contiene la logica del test
class TestResources():

    # Declaración constantes
    dataFactory = Faker()
    userId = None
    username = None
    password = None
    email = None
    dni = None
    full_name = None
    phone_number = None
    token = None
    response_create_user = {}
    response_detail_user = {}
    data = {}  

    # Función que genera data del usuario
    def set_up(self):
        self.username = self.dataFactory.first_name() + str(self.dataFactory.random_int(1, 1000000))
        self.password = self.dataFactory.password(
            length=10, special_chars=False, upper_case=True, lower_case=True, digits=True)
        self.email = self.dataFactory.email()
        self.dni = str(self.dataFactory.random_int(1000, 100000000))
        self.full_name = self.dataFactory.name()
        self.phone_number = str(self.dataFactory.random_int(1000000, 100000000000))
        self.data = {
            "username": f"{self.username}",
            "password": f"{self.password}",
            "email": f"{self.email}",
            "dni": f"{self.dni}",
            "full_name": f"{self.full_name}",
            "phone_number": f"{self.phone_number}"
        }

    # Función que crea un usuario
    def execute_create_user(self, data):
        with app.test_client() as test_client:
            self.response_create_user = test_client.post(
                '/users', json=data
            )

    # Función que consulta el detalle de un usuario
    def execute_detail_user(self, headers):
        with app.test_client() as test_client:
            self.response_detail_user = test_client.get(
                '/users/me', headers=headers
            )

    # Función que valida la creación exitosa de un usuario
    def validate_success_create_user(self): 
        response_json = json.loads(self.response_create_user.data)   
        assert self.response_create_user.status_code == 201
        assert 'id' in response_json
        assert 'created_at' in response_json 

    # Función que crea un usuario exitosamente
    def create_user_success(self):
        # Creación nuevo usuario
        self.set_up()
        self.execute_create_user(self.data)
        self.validate_success_create_user()
        response_json = json.loads(self.response_create_user.data)
        self.userId = response_json['id']

    # Función que valida la consulta exitosa de un usuario
    def validate_success_detail_user(self):
        response_json = json.loads(self.response_detail_user.data)
        assert self.response_detail_user.status_code == 200
        assert response_json["id"] == self.userId
        assert response_json["username"] == self.username
        assert response_json["email"] == self.email
        assert response_json["full_name"] == self.full_name
        assert response_json["dni"] == self.dni
        assert response_json["phone_number"] == self.phone_number
        assert response_json["status"] == "NO_VERIFICADO"        
        
       # Función que valida el estado del servidor
    def test_health_check(self):
        # Reset tabla usuarios
        with app.test_client() as test_client:
            response = test_client.get(
                '/'
            )
            data = str(response.data)
        assert response.status_code == 200
        assert 'status' in data
   
    # Función que valida la creación exitosa de un usuario
    def test_create_new_user(self):
        # Creación nuevo usuario
        self.create_user_success()
        
    # Función que consulta exitosamente el detalle del usuario
    def test_detail_user(self):
        # Creación usuario y generación token
        self.create_user_success()
        # Consulta de usuario
        headers = {}
        headers["Authorization"] = f"Bearer {self.token}"
        self.execute_detail_user(headers)
        self.validate_success_detail_user()    