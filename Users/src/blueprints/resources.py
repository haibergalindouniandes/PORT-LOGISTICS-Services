from flask import request, Blueprint
from flask.json import jsonify
from commands.create import CreateUser
from queries.detail import GetUserDetail
from utilities.utilities import formatDateTimeToUTC

users_blueprint = Blueprint('users', __name__)

@users_blueprint.route('/users/me', methods=['GET'])
def detail():
    """Expone el recurso para la actualización de información de un usuario.

    Args:
        headers (Objeto): Cabeceras.

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
    
    data = request.headers
    result = GetUserDetail(data).query()
    return jsonify({'id': result.id, 'username': result.username, 'email': result.email, 'full_name': result.full_name, 'dni': result.dni, 'phone_number': result.phone_number, 'status': result.status})

@users_blueprint.route('/users', methods=['POST'])
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