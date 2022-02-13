from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField,PasswordField,EmailField,BooleanField
from wtforms.validators import input_required,Email,EqualTo
from ..models import User
from wtforms import ValidationError

class RegisterForm(FlaskForm):
    """Register form"""
    username=StringField('Username',validators=[input_required(message="Username required")],render_kw={"placeholder": "Your Username"})
    email=EmailField('Email Address',validators=[input_required(message="Email Address required"),Email()],render_kw={"placeholder": "Your Email Address"})
    password=PasswordField('Password',validators=[input_required(message="Password required"),EqualTo('confirm_password',message='Passwords must match')],render_kw={"placeholder": "Your password"})
    confirm_password=PasswordField('Confirm Password',validators=[input_required()],render_kw={"placeholder": "Confirm password"})
    reqister=SubmitField("Register")

    def validate_email(self, data_field):
        if User.query.filter_by(email=data_field.data).first():
            raise ValidationError('There is an account with that email')

    def validate_username(self, data_field):
        if User.query.filter_by(username=data_field.data).first():
            raise ValidationError('That username is taken')



class LoginForm(FlaskForm):
    email=EmailField('Email Address',validators=[input_required(message='Email Address Required'),Email()],render_kw={"placeholder":"Your Email Address"})
    password=PasswordField('Password',validators=[input_required(message='Password Required')],render_kw={"placeholder":"Your Login Password"})
    remember = BooleanField('Remember me')
    login=SubmitField("Login")