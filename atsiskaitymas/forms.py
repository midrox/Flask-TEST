from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, BooleanField, StringField, PasswordField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
from wtforms_sqlalchemy.fields import QuerySelectField
from atsiskaitymas import models


MESSAGE_BAD_EMAIL = 'Incorrect email address, try again.'

class RegisterForm(FlaskForm):
    username = StringField('Name', [DataRequired()])
    email = StringField('Email', [DataRequired(), Email(MESSAGE_BAD_EMAIL)])
    password = PasswordField('Password', [DataRequired()])
    password_verification = PasswordField('Verify New Password', [EqualTo('password', "Passwords do not match")])
    submit = SubmitField('Register')

    def check_name(self, username):
        user = models.User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username exists. Choose diferent username')

    def check_email(self, email):
        user = models.User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('An email address already in use.')        

class LoginForm(FlaskForm):
    email = StringField('Email', [DataRequired(), Email(MESSAGE_BAD_EMAIL)])
    password = PasswordField('Password', [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login') 

class ProfileForm(FlaskForm):
    username = StringField('Name', [DataRequired()])
    email = StringField('Email', [DataRequired(), Email(MESSAGE_BAD_EMAIL)])
    submit = SubmitField('Enter')

    def check_name(self, username):
        user = models.User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username exists. Choose diferent username')

    def check_email(self, email):
        user = models.User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('An email address already in use.')        

class CarRegisterForm(FlaskForm):
    car_brand = StringField('Car brand', [DataRequired()])
    model = StringField('Model', [DataRequired()])
    years = IntegerField('Year of manufacture', [DataRequired()])
    engine = StringField('Engine capacity', [DataRequired()])
    plate = StringField('License plate', [DataRequired()])
    vin = StringField('Vehicle identification number', [DataRequired()])
    submit = SubmitField('Register')

class RepairForm(FlaskForm):
    description = TextAreaField('Fault description')
    status = SelectField('Status', choices=["New Order", 
    "Accepted", 
    "Being repaired", 
    "Repaired", 
    "The repaired car is returned"], default="New Order")
    price = IntegerField('Price', default=0)
    submit = SubmitField('Save order')