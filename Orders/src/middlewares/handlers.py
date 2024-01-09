# Importación de dependencias
from flask import jsonify, request
from errors.errors import HealthCheckUp, SuccessfulTransaction

# Clase que contiene los handlers del app
class Handlers:
    # Función que permite realizar la manipulación del request
    def before_request_handler(self):
        if request.method not in ['GET', 'DELETE']:
            if 'data' in request.json:
                request.json.update(request.json.pop('data'))
    
    # Función que permite realizar la manipulación del reponse
    def after_request_handler(self, response):
        if response.status_code in [200, 201]:
            json_response = response.get_json()
            print(type(json_response))
            if isinstance(json_response, dict):
                if 'description' in json_response:
                    if json_response['description'] not in [SuccessfulTransaction.description, HealthCheckUp.description]:
                        response.data = jsonify({'data': json_response}).data
            else:
                response.data = jsonify({'data': json_response}).data
            
        return response
    
    # Función que permite realizar la manipulación del response en caso de error
    def exception_handler(self, err):
        response = {
            "description": err.description
        }
        return jsonify(response), err.code