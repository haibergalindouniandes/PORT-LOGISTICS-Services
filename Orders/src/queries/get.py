# Importación de dependencias
from queries.base_query import BaseQuery
from errors.errors import ApiError, BadRequest
from models.models import  Orders, OrderSchema
from sqlalchemy.exc import SQLAlchemyError
import traceback

# Creacion de esquemas
orders_schema = OrderSchema(many=True)

# Clase que contiene la logica de consulta de ordenes
class GetOrders(BaseQuery):

    # Función que retorna todas las ordenes
    def query(self):
        try:
            orders = Orders.query.all()
            if len(orders) == 0:
                raise BadRequest
            return orders_schema.dump(orders)
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)
