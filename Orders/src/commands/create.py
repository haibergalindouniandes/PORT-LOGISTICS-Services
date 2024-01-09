# Importación de dependencias
from validators.validators import validate_schema, validateDateString, create_order_schema
from commands.base_command import BaseCommannd
from errors.errors import ApiError, OrdenAlreadyExists
from models.models import db, Orders, OrderSchema
from sqlalchemy.exc import SQLAlchemyError
import traceback

# Creacion de esquemas
order_schema = OrderSchema()

# Clase que contiene la logica de creción de ordenes
class CreateOrder(BaseCommannd):
    def __init__(self, order_json_request):
        print(order_json_request)
        validate_schema(order_json_request, create_order_schema)
        self.data = order_json_request

    # Función que valida si ya se encuentra registrada una orden con el mismo numero
    def validate_order_repeated(self, order_number):
        order = Orders.query.filter(Orders.order_number == order_number).first()
        if order != None:
            raise OrdenAlreadyExists # pragma: no cover

    # Función que realiza creación de una orden
    def execute(self):
        try:
            # Validación del numero de orden
            self.validate_order_repeated(self.data['order_number'])
            # Validación de fechas
            if 'warehouse_dropoff_date' in self.data:
                warehouse_dropoff_date = validateDateString(self.data['warehouse_dropoff_date'])
            else:
                warehouse_dropoff_date = None    
            if 'documents_cut_off_date' in self.data:
                documents_cut_off_date = validateDateString(self.data['documents_cut_off_date'])
            else:
                documents_cut_off_date = None    
            if 'first_receiving_date' in self.data:
                first_receiving_date = validateDateString(self.data['first_receiving_date'])
            else:
                first_receiving_date = None    
            if 'cut_off_date' in self.data:
                cut_off_date = validateDateString(self.data['cut_off_date'])
            else:
                cut_off_date = None    
            # Creación de la orden
            new_order = Orders(shipping_company=self.data['shipping_company'],                               
                               order_number=self.data['order_number'],
                               booking_number=self.data['booking_number'], 
                               warehouse_dropoff_date=warehouse_dropoff_date,
                               documents_cut_off_date=documents_cut_off_date,
                               first_receiving_date=first_receiving_date,
                               cut_off_date=cut_off_date,
                               created_by=self.data['created_by'])
            db.session.add(new_order)
            db.session.commit()
            return order_schema.dump(new_order)
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)