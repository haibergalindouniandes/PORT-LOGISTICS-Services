# Importación de dependencias
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import UUID

# Creación de variable db
db = SQLAlchemy()

# Clase que cotiene la definición del modelo de base de datos de Orders
class Orders(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    shipping_company = db.Column(db.Integer)
    order_number = db.Column(db.String(64), unique=True)
    booking_number = db.Column(db.String(64), unique=True)
    warehouse_dropoff_date = db.Column(DateTime)
    documents_cut_off_date = db.Column(DateTime)
    first_receiving_date = db.Column(DateTime)
    cut_off_date = db.Column(DateTime)
    status = db.Column(db.String(16), default="Activo")
    created_by = db.Column(db.Integer)
    created_at = db.Column(DateTime, default=datetime.utcnow())
    updated_by = db.Column(db.Integer)
    updated_at = db.Column(DateTime)
    # Indices de la tabla
    __table_args__ = (db.Index('idx_booking_number', 'booking_number'),
                      db.Index('idx_warehouse_dropoff_date', 'warehouse_dropoff_date'),
                      db.Index('idx_cut_off_date', 'cut_off_date'),)
    

# Clase que autogenera el esquema del modelo Orders
class OrderSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Orders
        load_instance = True