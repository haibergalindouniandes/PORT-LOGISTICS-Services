from flask import request, Blueprint
from flask.json import jsonify
from queries.get_by_id import GetNotificationById
from queries.get import GetNotifications
from commands.create import CreateNotification
from commands.update import UpdateNotification

# Creación de Blueprints para las diferentes versiones y APIs
healthcheck_blueprint = Blueprint('notifications', __name__)

@healthcheck_blueprint.route("/", methods=["GET"])
def healthcheck():
    """Expone el recurso para validar el estado de la aplicación.

    Args:
        N/A

    Returns:
        Objeto Json: 
            - status (String): Estado de la aplicación.

    """                
    return jsonify({'status': 'UP'})

api_v1 = Blueprint('api_v1', __name__)

@api_v1.route('/notifications', methods=['POST'], endpoint='create')
def create():
    """Expone el recurso para realizar la creación de una notificación.

    Args:
        headers (Objeto): Cabeceras.
        payload: 
            - data (Objeto Json): 
                - name (String): Titulo de la notificación.
                - rol (String): Rol del usuario.
                - type (String): Tipo de la notificación.
                - template (String): Plantilla con la estrucuta de la notificación.
                - description (String): Contenido de la notificación.
                - created_by (Integer): Usuario que creo la notificación.

    Returns:
        payload: 
            - description (String): Descripción en caso de presentarse un error.
            - data (Objeto Json): 
                - id (Integer): Identificación de la notificación.
                - name (String): Titulo de la notificación.
                - rol (String): Rol del usuario.
                - type (String): Tipo de la notificación.
                - template (String): Plantilla con la estrucuta de la notificación.
                - description (String): Contenido de la notificación.
                - status (String): Estado de la notificación.
                - created_by (Integer): Usuario que creo la notificación.
                - created_at (String): Fecha de creación de la notificación.
                - updated_at (String): Fecha de actualización de la notificación.

    """
    data = request.get_json()
    return jsonify(CreateNotification(data).execute()), 201

@api_v1.route("/notifications", methods=["GET"], endpoint='get_notifications')
def get_notifications():
    """Expone el recurso para consultar todas las notificaciones.

    Args:
        headers (Objeto): Cabeceras.
        payload: N/A

    Returns:
        payload: 
            - description (String): Descripción en caso de presentarse un error.
            - data (Array Objeto Json): 
                - id (Integer): Identificación de la notificación.
                - name (String): Titulo de la notificación.
                - rol (String): Rol del usuario.
                - type (String): Tipo de la notificación.
                - template (String): Plantilla con la estrucuta de la notificación.
                - description (String): Contenido de la notificación.
                - status (String): Estado de la notificación.
                - created_by (Integer): Usuario que creo la notificación.
                - created_at (String): Fecha de creación de la notificación.
                - updated_at (String): Fecha de actualización de la notificación.

    """                
    return jsonify(GetNotifications().query())

@api_v1.route("/notifications/<string:notificationId>", methods=["GET"], endpoint='get_notification_by_id')
def get_notification_by_id(notificationId):
    """Expone el recurso para consultar un notificacion con base al ID.

    Args:
        headers (Objeto): Cabeceras.
        payload: N/A
        path parameters:
            - notificationId: ID de la notificación a consultar.

    Returns:
        payload: 
            - description (String): Descripción en caso de presentarse un error.
            - data (Objeto Json): 
                - id (Integer): Identificación de la notificación.
                - name (String): Titulo de la notificación.
                - rol (String): Rol del usuario.
                - type (String): Tipo de la notificación.
                - template (String): Plantilla con la estrucuta de la notificación.
                - description (String): Contenido de la notificación.
                - status (String): Estado de la notificación.
                - created_by (Integer): Usuario que creo la notificación.
                - created_at (String): Fecha de creación de la notificación.
                - updated_at (String): Fecha de actualización de la notificación.
    """                
    return jsonify(GetNotificationById(notificationId).query())

@api_v1.route('/notifications/<string:notificationId>', methods=['PATCH'], endpoint='update')
def update(notificationId):
    """Expone el recurso para realizar la creación de una notificación.

    Args:
        headers (Objeto): Cabeceras.
        payload: 
            - data (Objeto Json): 
                - name (String): Titulo de la notificación.
                - rol (String): Rol del usuario.
                - type (String): Tipo de la notificación.
                - template (String): Plantilla con la estrucuta de la notificación.
                - description (String): Contenido de la notificación.
                - created_by (Integer): Usuario que creo la notificación.

    Returns:
        payload: 
            - description (String): Descripción en caso de presentarse un error.
            - data (Objeto Json): 
                - id (Integer): Identificación de la notificación.
                - name (String): Titulo de la notificación.
                - rol (String): Rol del usuario.
                - type (String): Tipo de la notificación.
                - template (String): Plantilla con la estrucuta de la notificación.
                - description (String): Contenido de la notificación.
                - status (String): Estado de la notificación.
                - created_by (Integer): Usuario que creo la notificación.
                - created_at (String): Fecha de creación de la notificación.
                - updated_at (String): Fecha de actualización de la notificación.
    """
    data = request.get_json()
    return UpdateNotification(notificationId, data).execute()