# Importación de dependencias
from queries.base_query import BaseQuery
from errors.errors import ApiError, NotFound
from models.models import  Notification, NotificationSchema
from sqlalchemy.exc import SQLAlchemyError
import traceback

# Creacion de esquemas
notification_schema = NotificationSchema()

# Clase que contiene la logica de consulta de notificaciones
class GetNotificationById(BaseQuery):
    def __init__(self, notificationId):
      self.notificationId = notificationId

    # Función que retorna todas las notificaciones
    def query(self):
        try:
            notification = Notification.query.filter(Notification.id == self.notificationId).first()
            if notification == None:
                raise NotFound
            return notification_schema.dump(notification)
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)
