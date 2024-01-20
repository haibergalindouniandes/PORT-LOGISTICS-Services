from src.commands.update import UpdateOrder
from src.commands.create import CreateOrder
from faker import Faker
from datetime import datetime, timedelta
import random
import time
import src.main

# Clase que contiene la logica de las pruebas del servicio
class TestUpdate():
    
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
    def create_order(self):
        # Creación de orden
        self.set_up()
        order = CreateOrder(self.data).execute()
        self.created_order = order
    
    # Función que valida la actualización exitosa de una orden
    def test_update_order(self):
        # Creación de orden
        self.create_order()
        # Actualización orden
        data_to_update = self.data
        data_to_update["updated_by"] = self.dataFactory.random_int(100, 1000)
        data_to_update["status"] = 'completado'
        updated_order = UpdateOrder(self.created_order["id"], data_to_update).execute()
        assert updated_order != None
        assert self.created_order["id"] == updated_order["id"]
        assert data_to_update["shipping_company"] == updated_order["shipping_company"]
        assert data_to_update["order_number"] == f'{updated_order["order_number"]}'
        assert data_to_update["booking_number"] == f'{updated_order["booking_number"]}'
        assert data_to_update["warehouse_dropoff_date"] == updated_order["warehouse_dropoff_date"]
        assert data_to_update["first_receiving_date"] == updated_order["first_receiving_date"]
        assert data_to_update["cut_off_date"] == updated_order["cut_off_date"]
        assert data_to_update["documents_cut_off_date"] == updated_order["documents_cut_off_date"]
        assert data_to_update["status"] == updated_order["status"]
        assert data_to_update["created_by"] == updated_order["created_by"]
        assert data_to_update["updated_by"] == updated_order["updated_by"]
    
    # Función que valida la actualización de una orden no se encuentra registrada
    def test_update_not_existing_order(self):
        try:
            # Actualización orden
            self.set_up()
            UpdateOrder(10000000, self.data).execute()
        except Exception as e:
            assert e.code == 400
   
  # Función que valida la respuesta de error cuando se envia un request invalido
    def test_update_order_bad_request(self):
        try:
            # Creación de orden
            self.create_order()
            # Actualización orden            
            data_to_update = {}
            UpdateOrder(self.created_order["id"], data_to_update).execute()
        except Exception as e:
            assert e.code == 400