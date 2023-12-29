# Importación de dependencias
from validators.validators import validate_schema, update_notification_schema
from commands.base_command import BaseCommannd
from errors.errors import ApiError, NotFound
from models.models import db, Notification, NotificationSchema
from sqlalchemy.exc import SQLAlchemyError
import traceback

# Creacion de esquemas
notification_schema = NotificationSchema()

# Clase que contiene la logica de creción de notificaciones
class UpdateNotification(BaseCommannd):
    def __init__(self, notificationId, notification):
        validate_schema(notification, update_notification_schema)
        self.notificationId = notificationId
        self.data = notification

    # Función que valida la existencia de una notifiacación con base al ID
    def get_notification_by_id(self, notificationId):
        notification = Notification.query.filter(Notification.id == notificationId).first()
        if notification == None:
            raise NotFound# pragma: no cover
        return notification

    # Función asigna los valores que se van a actualizar
    def assign_update_values(self, notification_to_update):
        if "name" in self.data:
            notification_to_update.name = self.data["name"]
        if "rol" in self.data:
            notification_to_update.rol = self.data["rol"]
        if "type" in self.data:
            notification_to_update.type = self.data["type"]
        if "template" in self.data:
            notification_to_update.template = self.data["template"]
        if "description" in self.data:
            notification_to_update.description = self.data["description"]
        if "created_by" in self.data:
            notification_to_update.created_by = self.data["created_by"]
        if "status" in self.data:
            notification_to_update.status = self.data["status"]
        return notification_to_update

    # Función que realiza creación de la notificación
    def execute(self):
        try:
            # Validación del nombre de la notificación
            notification_to_update = self.get_notification_by_id(self.notificationId)
            # Actualización de la notificación
            db.session.add(self.assign_update_values(notification_to_update))
            db.session.commit()            
            return notification_schema.dump(notification_to_update)
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)