from src.commands.create import CreateOrder
from faker import Faker
from datetime import datetime, timedelta
import random
import time
import src.main

# Clase que contiene la logica de las pruebas del servicio
class TestCreate():
    
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
                        "shipping_company": self.shipping_company,
                        "order_number": f"{self.order_number}",
                        "booking_number": f"{self.booking_number}",
                        "warehouse_dropoff_date": self.warehouse_dropoff_date,
                        "first_receiving_date": self.first_receiving_date,
                        "cut_off_date": self.cut_off_date,
                        "documents_cut_off_date": self.documents_cut_off_date,
                        "created_by": self.created_by
                    }
            
    # Función que valida la creación exitosa de una orden
    def test_create_order(self):
        # Creación de orden
        self.set_up()
        assert CreateOrder(self.data).execute() != None
    
    # Función que valida la creación de una orden ya registrada
    def test_create_existing_order(self):
        try:
            # Creación orden
            self.set_up()
            assert CreateOrder(self.data).execute() != None
            # Creación orden existente
            CreateOrder(self.data).execute()
        except Exception as e:
            assert e.code == 409
   
    # Función que valida la creación de una orden cuando se envia un request invalido
    def test_create_order_bad_request(self):
        try:
            # Creación orden
            self.set_up()
            data = {
                        "order_number": f"{self.order_number}",
                        "cut_off_date": f"{self.cut_off_date}",
                        "created_by": f"{self.created_by}"
                    }
            # Creación orden con data incompleta
            CreateOrder(data).execute()
        except Exception as e:
            assert e.code == 400