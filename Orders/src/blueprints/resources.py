from flask import request, Blueprint
from flask.json import jsonify
from errors.errors import HealthCheckUp
from commands.delete_by_id import DeleteOrderById
from queries.get_by_id import GetOrderById
from queries.get import GetOrders
from commands.create import CreateOrder
from commands.update import UpdateOrder

# Creación de Blueprints para las diferentes versiones y APIs
healthcheck_blueprint = Blueprint('orders', __name__)

@healthcheck_blueprint.route("/", methods=["GET"])
def healthcheck():
    """Expone el recurso para validar el estado de la aplicación.

    Args:
        N/A

    Returns:
        Objeto Json: 
            - status (String): Estado de la aplicación.

    """                
    response = jsonify({'description': HealthCheckUp.description})
    return response

api_v1 = Blueprint('api_v1', __name__)

@api_v1.route('/orders', methods=['POST'], endpoint='create')
def create():
    """Expone el recurso para realizar la creación de una orden.

    Args:
        headers (Objeto): Cabeceras.
        payload: 
            - data (Objeto Json): 
                - shipping_company (Integer): Naviera que transporta contenedores.
                - order_number (String): Numero de la orden.
                - booking_number (String): Numero del booking de la orden.
                - warehouse_dropoff_date (Datetime): Fecha para entregar contenedor en bodega.
                - documents_cut_off_date (Datetime): Fecha para entrega de la documentacion de la orden.
                - first_receiving_date (Datetime): Fecha inicial para entregar contenedor en el puerto.
                - cut_off_date (Datetime): Fecha final para entregar contenedor en el puerto.
                - created_by (Integer): Usuario que creo la orden.

    Returns:
        payload: 
            - description (String): Descripción en caso de presentarse un error.
            - data (Objeto Json): 
                - id (Integer): Identificación de la orden.
                - shipping_company (Integer): Naviera que transporta contenedores.
                - order_number (String): Numero de la orden.
                - booking_number (String): Numero del booking de la orden.
                - warehouse_dropoff_date (Datetime): Fecha para entregar contenedor en bodega.
                - documents_cut_off_date (Datetime): Fecha para entrega de la documentacion de la orden.
                - first_receiving_date (Datetime): Fecha inicial para entregar contenedor en el puerto.
                - cut_off_date (Datetime): Fecha final para entregar contenedor en el puerto.
                - status (String): Estado de la orden.
                - created_by (Integer): Usuario que creo la orden.
                - created_at (String): Fecha de creación de la orden.
                - updated_by (Integer): NULL (Usuario que actualizo la orden)
                - updated_at (String): NULL (Fecha de actualización de la orden)

    """
    data = request.get_json()
    return jsonify(CreateOrder(data).execute()), 201

@api_v1.route("/orders", methods=["GET"], endpoint='get_orders')
def get_orders():
    """Expone el recurso para consultar todas las ordenes.

    Args:
        headers (Objeto): Cabeceras.
        payload: N/A

    Returns:
        payload: 
            - description (String): Descripción en caso de presentarse un error.
            - data (Array Objeto Json): 
                - id (Integer): Identificación de la orden.
                - shipping_company (Integer): Naviera que transporta contenedores.
                - order_number (String): Numero de la orden.
                - booking_number (String): Numero del booking de la orden.
                - warehouse_dropoff_date (Datetime): Fecha para entregar contenedor en bodega.
                - documents_cut_off_date (Datetime): Fecha para entrega de la documentacion de la orden.
                - first_receiving_date (Datetime): Fecha inicial para entregar contenedor en el puerto.
                - cut_off_date (Datetime): Fecha final para entregar contenedor en el puerto.
                - status (String): Estado de la orden.
                - created_by (Integer): Usuario que creo la orden.
                - created_at (String): Fecha de creación de la orden.
                - updated_by (Integer): Usuario que actualizo la orden.
                - updated_at (String): Fecha de actualización de la orden.

    """                
    return jsonify(GetOrders().query())

@api_v1.route("/orders/<string:orderId>", methods=["GET"], endpoint='get_order_by_id')
def get_order_by_id(orderId):
    """Expone el recurso para consultar una orden con base al ID.

    Args:
        headers (Objeto): Cabeceras.
        payload: N/A
        path parameters:
            - ordenId: ID de la orden a consultar.

    Returns:
        payload: 
            - description (String): Descripción en caso de presentarse un error.
            - data (Objeto Json): 
                - id (Integer): Identificación de la orden.
                - shipping_company (Integer): Naviera que transporta contenedores.
                - order_number (String): Numero de la orden.
                - booking_number (String): Numero del booking de la orden.
                - warehouse_dropoff_date (Datetime): Fecha para entregar contenedor en bodega.
                - documents_cut_off_date (Datetime): Fecha para entrega de la documentacion de la orden.
                - first_receiving_date (Datetime): Fecha inicial para entregar contenedor en el puerto.
                - cut_off_date (Datetime): Fecha final para entregar contenedor en el puerto.
                - status (String): Estado de la orden.
                - created_by (Integer): Usuario que creo la orden.
                - created_at (String): Fecha de creación de la orden.
                - updated_by (Integer): Usuario que actualizo la orden.
                - updated_at (String): Fecha de actualización de la orden.
    """                
    return jsonify(GetOrderById(orderId).query())

@api_v1.route('/orders/<string:orderId>', methods=['PATCH'], endpoint='update')
def update(orderId):
    """Expone el recurso para realizar la actualizacion de una orden.

    Args:
        headers (Objeto): Cabeceras.
        payload: 
            - data (Objeto Json): 
                - shipping_company (Integer): Naviera que transporta contenedores.
                - order_number (String): Numero de la orden.
                - booking_number (String): Numero del booking de la orden.
                - warehouse_dropoff_date (Datetime): Fecha para entregar contenedor en bodega.
                - documents_cut_off_date (Datetime): Fecha para entrega de la documentacion de la orden.
                - first_receiving_date (Datetime): Fecha inicial para entregar contenedor en el puerto.
                - cut_off_date (Datetime): Fecha final para entregar contenedor en el puerto.
                - status (String): Estado de la orden.
                - updated_by (Integer): Usuario que actualizo la orden.                
        path parameters:
            - ordenId: ID de la orden a actualizar.                

    Returns:
        payload: 
            - description (String): Descripción en caso de presentarse un error.
            - data (Objeto Json): 
                - id (Integer): Identificación de la orden.
                - shipping_company (Integer): Naviera que transporta contenedores.
                - order_number (String): Numero de la orden.
                - booking_number (String): Numero del booking de la orden.
                - warehouse_dropoff_date (Datetime): Fecha para entregar contenedor en bodega.
                - documents_cut_off_date (Datetime): Fecha para entrega de la documentacion de la orden.
                - first_receiving_date (Datetime): Fecha inicial para entregar contenedor en el puerto.
                - cut_off_date (Datetime): Fecha final para entregar contenedor en el puerto.
                - status (String): Estado de la orden.
                - created_by (Integer): Usuario que creo la orden.
                - created_at (String): Fecha de creación de la orden.
                - updated_by (Integer): Usuario que actualizo la orden.
                - updated_at (String): Fecha de actualización de la orden.
    """
    data = request.get_json()
    return UpdateOrder(orderId, data).execute()

@api_v1.route("/orders/<string:orderId>", methods=["DELETE"], endpoint='delete_order_by_id')
def delete_order_by_id(orderId):
    """Expone el recurso para eliminar una orden con base al ID.

    Args:
        headers (Objeto): Cabeceras.
        payload: N/A
        path parameters:
            - ordenId: ID de la orden a eliminar.

    Returns:
        payload: 
            - description (String): Descripción de la transaccion.
    """                
    return jsonify(DeleteOrderById(orderId).execute())