# Importación de dependencias
from validators.validators import validate_schema, create_notification_schema
from commands.base_command import BaseCommannd
from errors.errors import ApiError, NotificactionAlreadyExists
from models.models import db, Notification, NotificationSchema
from sqlalchemy.exc import SQLAlchemyError
import traceback

# Creacion de esquemas
notification_schema = NotificationSchema()

# Clase que contiene la logica de creción de notificaciones
class CreateNotification(BaseCommannd):
    def __init__(self, notification):
        print(notification)
        validate_schema(notification, create_notification_schema)
        self.data = notification

    # Función que valida si ya se encuentra registrada una notificación con el mismo nombre
    def validate_notification_name(self, name):
        notification = Notification.query.filter(Notification.name == name).first()
        if notification != None:
            raise NotificactionAlreadyExists# pragma: no cover

    # Función que realiza creación de la notificación
    def execute(self):
        try:
            # Validación del nombre de la notificación
            self.validate_notification_name(self.data['name'])
            # Creación de la notificación
            new_notification = Notification(name=self.data['name'], rol=self.data['rol'], 
                                            type=self.data['type'], template=self.data['template'], 
                                            description=self.data['description'], 
                                            created_by=self.data['created_by'])
            db.session.add(new_notification)
            db.session.commit()            
            return notification_schema.dump(new_notification)
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)