# Importación de dependencias
from validators.validators import validate_schema, validateDateString, update_order_schema
from commands.base_command import BaseCommannd
from errors.errors import ApiError, BadRequest
from models.models import db, Orders, OrderSchema
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import traceback

# Creacion de esquemas
order_schema = OrderSchema()

# Clase que contiene la logica de creción de ordenes
class UpdateOrder(BaseCommannd):
    def __init__(self, orderId, order_json_request):
        validate_schema(order_json_request, update_order_schema)
        self.orderId = orderId
        self.data = order_json_request

    # Función que valida la existencia de una orden con base al ID
    def get_order_by_id(self, orderId):
        orden = Orders.query.filter(Orders.id == orderId).first()
        if orden == None:
            raise BadRequest# pragma: no cover
        return orden

    # Función asigna los valores que se van a actualizar
    def assign_update_values(self, order_to_update):
        if "shipping_company" in self.data:
            order_to_update.shipping_company = self.data["shipping_company"]
        if "order_number" in self.data:
            order_to_update.order_number = self.data["order_number"]
        if "booking_number" in self.data:
            order_to_update.booking_number = self.data["booking_number"]
        if "warehouse_dropoff_date" in self.data:
            warehouse_dropoff_date = validateDateString(self.data['warehouse_dropoff_date'])
            order_to_update.warehouse_dropoff_date = warehouse_dropoff_date
        if "documents_cut_off_date" in self.data:
            documents_cut_off_date = validateDateString(self.data['documents_cut_off_date'])
            order_to_update.documents_cut_off_date = documents_cut_off_date
        if "first_receiving_date" in self.data:
            first_receiving_date = validateDateString(self.data['first_receiving_date'])
            order_to_update.first_receiving_date = first_receiving_date
        if "cut_off_date" in self.data:
            cut_off_date = validateDateString(self.data['cut_off_date'])
            order_to_update.cut_off_date = cut_off_date
        if "status" in self.data:
            order_to_update.status = self.data["status"]
        if "updated_by" in self.data:        
            order_to_update.updated_by = self.data["updated_by"]
        order_to_update.updated_at = datetime.utcnow()
        return order_to_update

    # Función que realiza creación de la orden
    def execute(self):
        try:
            # Validación del nombre de la orden
            order_to_update = self.get_order_by_id(self.orderId)
            # Actualización de la orden
            db.session.add(self.assign_update_values(order_to_update))
            db.session.commit()            
            return order_schema.dump(order_to_update)
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)