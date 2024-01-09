from src.main import app
from faker import Faker
from faker import Faker
from datetime import datetime, timedelta
import random
import time
import json

# Clase que contiene la logica de las pruebas del servicio
class TestResources():
    
    # Declaración constantes
    dataFactory = Faker()
    shipping_company = None
    order_number = None
    booking_number = None
    warehouse_dropoff_date = None
    first_receiving_date = None
    cut_off_date = None
    documents_cut_off_date = None
    created_by = None
    data = {}
    health_check_rs = {}
    create_order_rs = {}
    get_order_rs = {}
    get_order_by_id_rs = {}

    # Función que genera data de la orden
    def set_up(self):        
        self.shipping_company = self.dataFactory.random_int(100, 1000)
        self.order_number = self.dataFactory.random_int(min=100000, max=999999)
        self.booking_number = self.dataFactory.random_int(min=100000, max=999999)
        self.warehouse_dropoff_date = (datetime.now() + timedelta(days=self.dataFactory.random_int(min=5, max=10))).replace(microsecond=0).isoformat()
        self.first_receiving_date = (datetime.now() + timedelta(days=self.dataFactory.random_int(min=15, max=20))).replace(microsecond=0).isoformat()
        self.cut_off_date = (datetime.now() + timedelta(days=self.dataFactory.random_int(min=25, max=30))).replace(microsecond=0).isoformat()
        self.documents_cut_off_date = (datetime.now() + timedelta(days=self.dataFactory.random_int(min=25, max=30))).replace(microsecond=0).isoformat()
        self.created_by = self.dataFactory.random_int(100, 1000)
        self.data = {
                        "data": {
                            "shipping_company": self.shipping_company,
                            "order_number": f"{self.order_number}",
                            "booking_number": f"{self.booking_number}",
                            "warehouse_dropoff_date": self.warehouse_dropoff_date,
                            "first_receiving_date": self.first_receiving_date,
                            "cut_off_date": self.cut_off_date,
                            "documents_cut_off_date": self.documents_cut_off_date,
                            "created_by": self.created_by
                        }
                    }

    # Función que consume el api health check
    def execute_health_check(self):
        with app.test_client() as test_client:
            self.health_check_rs = test_client.get('/')
            
    # Función que consume el api para la creación de una orden
    def execute_create_order(self, data):
        with app.test_client() as test_client:
            self.create_order_rs = test_client.post('/api/v1/orders', json=data)

    # Función que valida la creación exitosa de una orden
    def validate_create_successful_order(self): 
        assert self.create_order_rs.status_code == 201
        response_json = json.loads(self.create_order_rs.data)["data"]
        assert 'id' in response_json
        assert 'created_at' in response_json        
        assert 'status' in response_json
        assert response_json['shipping_company'] == self.shipping_company
        assert response_json['order_number'] == self.order_number
        assert response_json['booking_number'] == self.booking_number
        assert response_json['warehouse_dropoff_date'] == self.warehouse_dropoff_date
        assert response_json['first_receiving_date'] == self.first_receiving_date
        assert response_json['cut_off_date'] == self.cut_off_date
        assert response_json['documents_cut_off_date'] == self.documents_cut_off_date
        assert response_json['created_by'] == self.created_by

    # Función que consume el api para la consulta de ordenes
    def execute_get_orders(self):
        with app.test_client() as test_client:
            self.get_order_rs = test_client.get('/api/v1/orders')

    # Función que consume el api para la consulta de ordenes
    def execute_get_order_by_id(self, orderId):
        with app.test_client() as test_client:
            self.get_order_by_id_rs = test_client.get(f"/api/v1/orders/{orderId}")

    # Función que valida el health check
    def test_health_check(self):
        self.execute_health_check()
        assert self.health_check_rs.status_code == 200
       
    # Función que valida la creación exitosa de una orden
    def test_create_successful_order(self):
        # Generación data aleatoria 
        self.set_up()
        # Creación nueva orden
        self.execute_create_order(self.data)        
        # Validación creación exitosa
        self.validate_create_successful_order()        

    # Función que valida la consulta exitosa de ordenes
    def test_get_orders(self):
        iterations = 10
        for i in range(iterations):
            # Generación data aleatoria 
            self.set_up()
            # Creación nueva orden
            self.execute_create_order(self.data)

        self.execute_get_orders()
        assert self.get_order_rs.status_code == 200
        response_json = json.loads(self.get_order_rs.data)["data"]
        assert len(response_json) >= iterations
        assert json.loads(self.create_order_rs.data)["data"] in response_json
        
    # Función que valida la consulta exitosa de ordenes
    def test_get_order_by_id(self):
        # Generación data aleatoria 
        self.set_up()
        # Creación nueva orden
        self.execute_create_order(self.data)
        order_created = json.loads(self.create_order_rs.data)["data"] 
        # Consulta de orden 
        self.execute_get_order_by_id(order_created["id"])
        assert self.get_order_by_id_rs.status_code == 200
        response_json = json.loads(self.get_order_by_id_rs.data)["data"]
        assert order_created["id"] == response_json["id"]
        assert order_created["shipping_company"] == response_json["shipping_company"]
        assert order_created["order_number"] == response_json["order_number"]
        assert order_created["booking_number"] == response_json["booking_number"]
        assert order_created["warehouse_dropoff_date"] == response_json["warehouse_dropoff_date"]
        assert order_created["first_receiving_date"] == response_json["first_receiving_date"]
        assert order_created["cut_off_date"] == response_json["cut_off_date"]
        assert order_created["documents_cut_off_date"] == response_json["documents_cut_off_date"]
        assert order_created["status"] == response_json["status"]
        assert order_created["created_by"] == response_json["created_by"]
        assert order_created["created_at"] == response_json["created_at"]    