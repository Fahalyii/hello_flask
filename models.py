from database import db
from flask_login import UserMixin

# -------------------------------
# User Table
# -------------------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # customer, restaurant_manager, admin

    reservations = db.relationship('Reservation', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    waitlists = db.relationship('Waitlist', backref='user', lazy=True)
    notifications = db.relationship('Notification', backref='user', lazy=True)

# -------------------------------
# Restaurant Table
# -------------------------------
class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(200))
    cuisine = db.Column(db.String(100))
    image = db.Column(db.String(255))
    manager_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    tables = db.relationship('Table', backref='restaurant', lazy=True)
    menu_items = db.relationship('MenuItem', backref='restaurant', lazy=True)
    reviews = db.relationship('Review', backref='restaurant', lazy=True)
    waitlists = db.relationship('Waitlist', backref='restaurant', lazy=True)

# -------------------------------
# Table Table
# -------------------------------
class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    capacity = db.Column(db.Integer, nullable=False)
    is_available = db.Column(db.Boolean, default=True)

    reservations = db.relationship('Reservation', backref='table', lazy=True)

# -------------------------------
# Reservation Table
# -------------------------------
class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    table_id = db.Column(db.Integer, db.ForeignKey('table.id'))
    status = db.Column(db.String(50), default='Confirmed')  # Pending, Confirmed, Cancelled
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    guest_count = db.Column(db.Integer)

# -------------------------------
# Waitlist Table
# -------------------------------
class Waitlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    status = db.Column(db.String(50), default='Waiting')  # Waiting, Notified, Cancelled
    joined_at = db.Column(db.DateTime, server_default=db.func.now())

# -------------------------------
# Notification Table
# -------------------------------
class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    message = db.Column(db.String(255))
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

# -------------------------------
# Menu Item Table
# -------------------------------
class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)

# -------------------------------
# Review Table
# -------------------------------
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id'))
    rating = db.Column(db.Integer)  # 1 to 5
    comment = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
