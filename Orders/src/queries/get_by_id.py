# Importación de dependencias
from queries.base_query import BaseQuery
from errors.errors import ApiError, BadRequest
from models.models import  Orders, OrderSchema
from sqlalchemy.exc import SQLAlchemyError
import traceback

# Creacion de esquemas
order_schema = OrderSchema()

# Clase que contiene la logica de consulta de ordenes
class GetOrderById(BaseQuery):
    def __init__(self, orderId):
      self.orderId = orderId

    # Función que retorna una orden con base al ID
    def query(self):
        try:
            order = Orders.query.filter(Orders.id == self.orderId).first()
            if order == None:
                raise BadRequest
            return order_schema.dump(order)
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)
