# Clase que contiene la estructura de error por defecto
class ApiError(Exception):
    code = 500
    description = "Error interno, por favor revise el log"

# Clase que contiene la estructura de un error cuando se trata de crear una notificación con el mismo titulo
class NotificactionAlreadyExists(ApiError):
    code = 409
    description = "La notificación ya se encutra registrada"

# Clase que contiene la estructura de un error cuando se encuentra información
class NotFound(ApiError):
    code = 404
    description = "No se encontró información"

# Clase que contiene la estructura de error cuando no se envia el token
class MissingToken(ApiError):
    code = 403
    description = "El token no está en el encabezado de la solicitud"

# Clase que contiene la estructura de error cuando el token no es valido o esta vencido
class InvalidToken(ApiError):
    code = 401
    description = "El token no es válido o está vencido" 

# Clase que contiene la estructura de un error de tipo Bad Request
class BadRequest(ApiError):
    code = 400
    description = "Error en la estructura, formato y/o tipos de datos de la peticion"
