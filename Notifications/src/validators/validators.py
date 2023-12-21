# Importación de dependencias
from errors.errors import BadRequest
from jsonschema import validate
import traceback
import jsonschema

# Esquemas
# Esquema para la creación de notificationes
create_notification_schema = {
	"type": "object",
	"properties": {
		"data": {
			"type": "object",
			"properties": {				
				"name": {"type": "string", "minimum": 4, "maximum": 64},
				"rol": {"type": "string", "minimum": 4, "maximum": 64},
				"type": {"type": "string", "minimum": 4, "maximum": 64},
				"template": {"type": "string", "minimum": 4, "maximum": 4000},
				"description": {"type": "string", "minimum": 4, "maximum": 300},
                "created_by": {"type": "integer"},
			},
			"required": ["name", "rol", "type", "template", "description", "created_by"]
		}
	},
	"required": ["data"]
}

# Función que valida el request para la creación de usuarios
def validate_schema(json_data, schema):
    try:
        validate(instance=json_data, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        traceback.print_exc()
        raise BadRequest