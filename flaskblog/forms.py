from flask_wtf import FlaskForm
from flask_wtf.recaptcha import validators
from wtforms import StringField, SubmitField, PasswordField
from wtforms.fields.core import BooleanField
from wtforms.validators import EqualTo, DataRequired, Email, Length, ValidationError
from flaskblog.models import User

class RegistrationForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired(), Length(min=2, max=25)])
    email=StringField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('Password', validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit=SubmitField('Sign Up')

    def validate_username(self, username):
        user=User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Tên đã tồn tại, vui lòng chọn tên khác!')
    
    def validate_email(self, email):
        user=User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email đã tồn tại, vui lòng chọn email khác!')


class LoginForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('Password', validators=[DataRequired()])
    remember=BooleanField('Remember Me')
    submit=SubmitField('Login')