from flask import request, Blueprint
from flask.json import jsonify
from commands.create import CreateUser
from queries.detail import GetUserDetail
from utilities.utilities import formatDateTimeToUTC

# Creación de Blueprints para las diferentes versiones y APIs
users_blueprint = Blueprint('users', __name__)

@users_blueprint.route("/", methods=["GET"])
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

@api_v1.route('/users/<string:user_id>', methods=['GET'])
def detail(user_id):
    """Expone el recurso para la actualización de información de un usuario.

    Args:
        user_id (String): ID del usuario.

    Returns:
        Objeto Json: 
            - code (Integer): Código de respuesta.
            - description (String): Descripción de la respuesta.
            - data (Objeto): 
                - id (String): Identificación del usuario.
                - username (String): Nombre de usuario.
                - email (String): Email del usuario.
                - full_name (String): Nombre completo del usuario.
                - dni (String): Número de documento del usuario.
                - phone_number (String): Número de celular del usuario.
                - status (String): Estatus del usuario.

    """
    
    result = GetUserDetail(user_id).query()
    return jsonify({'id': result.id, 'username': result.username, 'email': result.email, 'full_name': result.full_name, 'dni': result.dni, 'phone_number': result.phone_number, 'status': result.status})

@api_v1.route('/users', methods=['POST'])
def create():
    """Expone el recurso para el registro de información de un usuario.

    Args:
        headers (Objeto): Cabeceras.
        Objeto Json: 
            - data (Objeto): 
                - id (String): Identificación del usuario.
                - username (String): Nombre de usuario.
                - email (String): Email del usuario.
                - full_name (String): Nombre completo del usuario.
                - dni (String): Número de documento del usuario.
                - phone_number (String): Número de celular del usuario.

    Returns:
        Objeto Json: 
            - code (Integer): Código de respuesta.
            - description (String): Descripción de la respuesta.
            - data (Objeto): 
                - id (String): Identificación del usuario.
                - created_at (String): Fecha y hora del registro del usuario.

    """
    data = request.get_json()
    result = CreateUser(data).execute()
    return jsonify({'id': result.id, 'created_at': formatDateTimeToUTC(str(result.created_at))}), 201



# Vesrion 2 de la aplicación
api_v2 = Blueprint('api_v2', __name__)

@api_v2.route("/users", methods=["GET"])
def example():
    """Expone el recurso para validar el estado de la aplicación.

    Args:
        N/A

    Returns:
        Objeto Json: 
            - status (String): Estado de la aplicación.

    """                
    return jsonify({'app_version': 'v2', 'status': 'UP'})