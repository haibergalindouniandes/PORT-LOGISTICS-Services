# Importación de dependencias
from errors.errors import BadRequest
from jsonschema import validate
from dateutil.parser import parse, ParserError
from datetime import datetime
import traceback
import jsonschema

# Esquemas
# Esquema para la creación de ordenes
create_order_schema = {
	"type": "object",
	"properties": {				
		"shipping_company": {"type": "integer"},
		"order_number": {"type": "string", "minimum": 4, "maximum": 64},
		"booking_number": {"type": "string", "minimum": 4, "maximum": 64},
		"warehouse_dropoff_date": {"type": ["string", "null"]},		
        "documents_cut_off_date": {"type": ["string", "null"]},
        "first_receiving_date": {"type": ["string", "null"]},
        "cut_off_date": {"type": ["string", "null"]},
		"created_by": {"type": "integer"},
	},
	"required": ["shipping_company", "order_number", "booking_number", "created_by"]
}

# Esquema para la actualización de ordenes
update_order_schema = {
	"type": "object",
	"properties": {
		"shipping_company": {"type": "integer"},
		"order_number": {"type": "string", "minimum": 4, "maximum": 64},
		"booking_number": {"type": "string", "minimum": 4, "maximum": 64},
		"warehouse_dropoff_date": {"type": ["string", "null"]},		
        "documents_cut_off_date": {"type": ["string", "null"]},
        "first_receiving_date": {"type": ["string", "null"]},
        "cut_off_date": {"type": ["string", "null"]},
		"status": {"type": "string", "minimum": 4, "maximum": 16},
		"updated_by": {"type": "integer"},
	},
    "required": "updated_by",
	"minProperties": 2,
	"additionalProperties": False
}

# Función que valida el request para la creación de ordenes
def validate_schema(json_data, schema):
    try:
        validate(instance=json_data, schema=schema)
    except jsonschema.exceptions.ValidationError as err:
        traceback.print_exc()
        raise BadRequest

# Funcion que valida si un string es un tipo de dato fecha y no es una fecha expirada  
def validateDateString(dateStr):
    try:        
        dateValue = parse(dateStr)
        if dateValue <= datetime.now():
            raise BadRequest
        return dateValue
    except ParserError:
        traceback.print_exc()
        raise BadRequest