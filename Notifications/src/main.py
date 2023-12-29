# Importación de dependencias
from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from middlewares.handlers import Handlers
from blueprints.resources import healthcheck_blueprint, api_v1 
from errors.errors import ApiError
from models.models import db
import os

# Constantes
CONNECTION_STRING = os.environ.get('CONNECTION_STRING')

# Configuracion app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = CONNECTION_STRING
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
# Registro de Blueprints en la aplicación
app.register_blueprint(healthcheck_blueprint)
app.register_blueprint(api_v1, url_prefix='/api/v1')
# Asignación de contexto
app_context = app.app_context()
app_context.push()
cors = CORS(app)
# Asignación de handlers
handlers = Handlers()
app.before_request(handlers.before_request_handler)
app.after_request(handlers.after_request_handler)
app.errorhandler(ApiError)(handlers.exception_handler)
# Creación de la estructura de BD
db.init_app(app)
db.create_all()
api = Api(app)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
