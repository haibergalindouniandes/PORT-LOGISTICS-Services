# Función que retorna la respuesta exitosa para la creación de una notificación
def success_create_response(data):
    return {"data" : data}, 201

# Función que retorna la respuesta exitosa para la consulta de notificaciones
def success_query_response(data):
    return {"data" : data}