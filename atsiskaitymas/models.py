from datetime import datetime
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, current_user
from sqlalchemy import DateTime
from atsiskaitymas import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    is_admin = db.Column(db.Boolean(), default=False)
    is_staff = db.Column(db.Boolean(), default=False)
    

    def __repr__(self) -> str:
        return self.username

class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    car_brand = db.Column('Car brand', db.String(40), nullable=False)
    model = db.Column('Model', db.String(30), nullable=False)
    registration_time = db.Column(DateTime, default=datetime.utcnow())
    years = db.Column('Year of manufacture', db.Integer, nullable=False)
    engine = db.Column('Engine capacity', db.String(30), nullable=False)
    plate = db.Column('License plate', db.String(20), nullable=False)
    vin = db.Column('Vehicle identification number', db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User")

    def __repr__(self) -> str:
        return f'{self.car_brand} {self.model} License plate: {self.plate} made: {self.years}'

class Repair(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    registration_time = db.Column(DateTime, default=datetime.utcnow())
    status = db.Column(db.String(40), default="New Order", nullable=False)
    price = db.Column(db.Numeric(8,2), nullable=False, default=0)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'))
    car = db.relationship("Car", lazy=True)
    

    def __repr__(self) -> str:
        return self.description


class Admin(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

