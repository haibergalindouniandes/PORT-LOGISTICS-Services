# Importación de dependencias
from errors.errors import BadRequest
from jsonschema import validate
import traceback
import jsonschema

# Esquemas
# Esquema para la creación de usuarios
create_user_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string", "minimum": 4, "maximum": 64},
        "email": {"type": "string", "minimum": 6, "maximum": 64, "format": "email"},
        "phone_number": {"type": "string", "minimum": 7, "maximum": 12, "pattern": "^ *\d[\d ]*$"},
        "dni":  {"type": "string", "minimum": 3, "maximum": 20, "pattern": "^ *\d[\d ]*$"},
        "full_name": {"type": "string", "minimum": 3, "maximum": 100},
        "password": {"type": "string", "minimum": 4, "maximum": 64},
        "status": {"type": "string", "enum": ["POR_VERIFICAR", "NO_VERIFICADO", "VERIFICADO"]},
    },
    "required": ["username", "email", "password"]
}

# Esquema para la generación del token
generate_token_schema = {
    "type": "object",
    "properties": {
        "username": {"type": "string", "minimum": 4, "maximum": 64},
        "password": {"type": "string", "minimum": 4, "maximum": 64},
    },
    "required": ["username", "password"]
}

# Esquema para la actualización de usuarios
update_user_schema = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "enum": ["POR_VERIFICAR", "NO_VERIFICADO", "VERIFICADO"]},
        "phone_number": {"type": "string", "minimum": 7, "maximum": 12, "pattern": "^ *\d[\d ]*$"},
        "dni":  {"type": "string", "minimum": 3, "maximum": 20, "pattern": "^ *\d[\d ]*$"},
        "full_name": {"type": "string", "minimum": 3, "maximum": 100},
    }
}

# Función que valida el request para la creación de usuarios
def validateSchema(json_data, schema):
    try:
        validate(instance=json_data, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        traceback.print_exc()
        raise BadRequest