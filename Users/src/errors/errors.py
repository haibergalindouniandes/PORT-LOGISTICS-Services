# Clase que contiene la estructura de error por defecto
class ApiError(Exception):
    code = 500
    description = "Error interno, por favor revise el log"
    
# Clase que contiene la estructura de error cuando ya esta registrado el username
class UserNameExists(ApiError):
    code = 412
    description = "El username ya se encuentra registrado"

# Clase que contiene la estructura de error cuando ya esta registrado el email
class UserEmailExists(ApiError):
    code = 412
    description = "El email ya se encuentra registrado"

# Clase que contiene la estructura de error cuando no esta registra el username
class UserNameNotExists(ApiError):
    code = 404
    description = "El usuario no se encuentra registrado"
    
# Clase que contiene la estructura de error cuando no esta registra el password
class PasswordNotExists(ApiError):
    code = 404
    description = "El password es incorrecto"    
    
# Clase que contiene la estructura de error cuando el token no es valido o esta vencido
class InvalidToken(ApiError):
    code = 401
    description = "El token no es válido o está vencido" 
    
# Clase que contiene la estructura de error cuando no se envia el token
class MissingToken(ApiError):
    code = 403
    description = "El token no está en el encabezado de la solicitud"

# Clase que contiene la estructura de un error de tipo Bad Request
class BadRequest(ApiError):
    code = 400
    description = "Párametros de entrada invalidos"