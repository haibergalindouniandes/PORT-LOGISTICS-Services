# Importación de dependencias
from flask import jsonify, request

# Clase que contiene los handlers del app
class Handlers:
    # Función que permite realizar la manipulación del request
    def before_request_handler(self):
        if request.method not in ['GET', 'DELETE']:
            if 'data' in request.json:
                original_json = request.json["data"]
                request.json.pop('data')
                for key, value in original_json.items():
                    request.json[key] = value
    
    # Función que permite realizar la manipulación del reponse
    def after_request_handler(self, response):
        if response.status_code in [200, 201]:
            json_response = response.get_json()
            response.set_data(jsonify({'data':json_response}).data)
        return response
    
    # Función que permite realizar la manipulación del response en caso de error
    def exception_handler(self, err):
        response = {
            "description": err.description
        }
        return jsonify(response), err.code