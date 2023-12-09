from src.commands.create import CreateUser
from faker import Faker

# Clase que contiene la logica de las pruebas del servicio
class TestCreate():
    
    # Declaración constantes
    dataFactory = Faker()
    username = None
    password = None
    email = None
    dni = None
    full_name = None
    phone_number = None
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
            
    # Función que valida la creación exitosa de un usuario
    def test_create_new_user(self):
        # Creación usuario
        self.set_up()
        result = CreateUser(self.data).execute()
        assert result != None
    
    # Función que valida la creación de un usuario ya registrado    
    def test_existing_user_creation(self):
        try:
            # Creación usuario
            self.set_up()
            result = CreateUser(self.data).execute()
            assert result != None
            # Creación usuario existente
            result = CreateUser(self.data).execute()
        except Exception as e:
            assert e.code == 412
   
    # Función que valida la creación de un usuario cuando se envia un request invalido
    def test_create_user_bad_request(self):
        try:
            # Creación usuario
            self.set_up()
            data = {
                "full_name": f"{self.full_name}"
            }
            # Creación usuario con data incompleta
            result = CreateUser(data).execute()
        except Exception as e:
            assert e.code == 400        