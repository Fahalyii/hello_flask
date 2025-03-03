from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # "customer" or "restaurant_manager"

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200), nullable=False)
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tables = db.relationship('Table', backref='restaurant', lazy=True)

class Table(db.Model):  # ✅ This is the missing Table model!
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    capacity = db.Column(db.Integer, nullable=False)
    is_available = db.Column(db.Boolean, default=True)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'))  # ✅ Linked to Table
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(50), default="Pending")  # "Confirmed", "Cancelled"
