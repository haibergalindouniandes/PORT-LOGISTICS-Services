# Importación de dependencias
from flask import Flask, jsonify
from flask_restful import Api
from flask_cors import CORS
from blueprints.resources import users_blueprint
from errors.errors import ApiError
from models.models import db
import os

# Constantes
CONNECTION_STRING = os.environ["CONNECTION_STRING"]

# Configuracion app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = CONNECTION_STRING
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.register_blueprint(users_blueprint)
app_context = app.app_context()
app_context.push()
cors = CORS(app)
db.init_app(app)
db.create_all()
api = Api(app)

# Manejador de errores
@app.errorhandler(ApiError)
def handle_exception(err):
    response = {
        "code": err.code,
        "description": err.description
    }
    return jsonify(response), err.code

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
