# Importación de dependencias
from queries.base_query import BaseQuery
from errors.errors import ApiError, InvalidToken, MissingToken, UserNameNotExists
from models.models import User
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import traceback

# Clase que contiene la logica de consulta de información de usuarios
class GetUserDetail(BaseQuery):
    def __init__(self, user_id):
        self.user_id = user_id

    # Función que realiza creación del usuario
    def query(self):
        try:
            user_to_consult = User.query.filter(User.id == self.user_id).first()
            if user_to_consult == None:
                raise UserNameNotExists
            return user_to_consult
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)
