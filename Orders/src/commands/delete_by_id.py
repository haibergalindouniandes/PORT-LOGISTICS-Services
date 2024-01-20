# Importación de dependencias

from commands.base_command import BaseCommannd
from errors.errors import ApiError, BadRequest, SuccessfulTransaction
from models.models import  Orders
from sqlalchemy.exc import SQLAlchemyError
from models.models import db
import traceback

# Clase que contiene la logica de consulta de ordenes
class DeleteOrderById(BaseCommannd):
    def __init__(self, orderId):
      self.orderId = orderId

    # Función que elimina una orden con base al ID
    def execute(self):
        try:
            order = Orders.query.filter(Orders.id == self.orderId).first()
            if order == None:
                raise BadRequest
            db.session.delete(order)
            db.session.commit()
            return {"description": SuccessfulTransaction.description}
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)
