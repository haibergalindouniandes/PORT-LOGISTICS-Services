# Importación de dependencias
from queries.base_query import BaseQuery
from errors.errors import ApiError, NotFound
from models.models import  Notification, NotificationSchema
from sqlalchemy.exc import SQLAlchemyError
import traceback

# Creacion de esquemas
notifications_schema = NotificationSchema(many=True)

# Clase que contiene la logica de consulta de notificaciones
class GetNotifications(BaseQuery):

    # Función que retorna todas las notificaciones
    def query(self):
        try:
            notifications = Notification.query.all()
            if len(notifications) == 0:
                raise NotFound
            return notifications_schema.dump(notifications)
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)
