from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.fields.core import BooleanField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import EqualTo, DataRequired, Email, Length, ValidationError
from flaskblog.models import User
from flask_login import current_user

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

class UpdateAccountForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired(), Length(min=2, max=25)])
    email=StringField('Email', validators=[DataRequired(), Email()])
    picture=FileField('Upload Profile Picture', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit=SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user=User.query.filter_by(username=username.data).first()
            if user:
               raise ValidationError('Tên này đã tồn tại, vui lòng chọn tên khác!') 

    def validate_email(self, email):
        if email.data != current_user.email:
            user=User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email đã tồn tại, vui lòng chọn email khác!')



class LoginForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), Email()])
    password=PasswordField('Password', validators=[DataRequired()]) 
    remember=BooleanField('Remember Me')
    submit=SubmitField('Sign Up')


class PostForm(FlaskForm):
    title=StringField('Title', validators=[DataRequired()])
    content=TextAreaField('Content', validators=[DataRequired()]) 
    submit=SubmitField('Submit')


class RequestResetForm(FlaskForm):
    email=StringField('Email', validators=[DataRequired(), Email()])
    submit=SubmitField('Request Password Reset')

    def validate_email(self, email):
        user=User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('Email này không tồn tại, hãy đăng ký!')


class ResetPasswordForm(FlaskForm):
    password=PasswordField('Password', validators=[DataRequired()])
    confirm_password=PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit=SubmitField('Reset Password')


