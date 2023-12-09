# Importación de dependencias
from queries.base_query import BaseQuery
from errors.errors import ApiError, InvalidToken, MissingToken
from models.models import User
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
import traceback

# Clase que contiene la logica de creción de usuarios
class GetUserDetail(BaseQuery):
    def __init__(self, headers):
        self.validateHeaders(headers)

    # Función que valida los headers
    def validateHeaders(self, headers):
        if not "Authorization" in headers:
            raise MissingToken
        self.token = headers["Authorization"]

    # Función que valida el token enviado
    def validateToken(self):
        userToConsult = User.query.filter(User.token == self.token.replace("Bearer ", "")).first()
        if userToConsult == None:
            raise InvalidToken
        expireAt = userToConsult.expireAt
        currentDateTime = datetime.today()
        if expireAt < currentDateTime:
            raise InvalidToken# pragma: no cover
        return userToConsult

    # Función que realiza creación del usuario
    def query(self):
        try:
            return self.validateToken()
        except SQLAlchemyError as e:# pragma: no cover
            traceback.print_exc()
            raise ApiError(e)
