from flask import request, Blueprint
from flask.json import jsonify
from commands.create import CreateNotification

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

@api_v1.route('/notifications', methods=['POST'])
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
            - code (Integer): Código de respuesta.
            - description (String): Descripción de la respuesta.
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
    return CreateNotification(data).execute()