# Importación de dependencias
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID

# Creación de variable db
db = SQLAlchemy()

# Clase que cotiene la definición del modelo de base de datos de Notifiación
class Notification(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    rol = db.Column(db.String(64))
    type = db.Column(db.String(64))
    template = db.Column(db.String(4000))
    description = db.Column(db.String(300))
    status = db.Column(db.String(16), default="Activo")
    created_by = db.Column(db.Integer)
    created_at = db.Column(DateTime, default=datetime.utcnow)
    updated_at = db.Column(DateTime, default=datetime.utcnow)
    # Indices de la tabla
    __table_args__ = (db.Index('idx_created_by', 'created_by'),
                      db.Index('idx_rol', 'rol'),
                      db.Index('idx_status', 'status'),)
    

# Clase que autogenera el esquema del modelo notificación
class NotificationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Notification
        load_instance = True