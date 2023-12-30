# Importación de dependencias

from commands.base_command import BaseCommannd
from errors.errors import ApiError, NotFound, SuccessDelete
from models.models import  Notification
from sqlalchemy.exc import SQLAlchemyError
from models.models import db
import traceback

# Clase que contiene la logica de consulta de notificaciones
class DeleteNotificationById(BaseCommannd):
    def __init__(self, notificationId):
      self.notificationId = notificationId

    # Función que elimina una notificación con base al ID
    def execute(self):
        try:
            notification = Notification.query.filter(Notification.id == self.notificationId).first()
            if notification == None:
                raise NotFound
            db.session.delete(notification)
            db.session.commit()
            return {"description": SuccessDelete.description}
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)
