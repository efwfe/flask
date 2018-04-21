# _*_coding:utf-8_*_

from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField,PasswordField
from wtforms.validators import DataRequired, length, Email, Regexp, EqualTo, ValidationError
from flask_wtf import FlaskForm
from ..models import User,Role

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), length(1, 64), Email()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('keep me logged in')
    submit = SubmitField('Login In')


class RegisterForm(FlaskForm):
    eamil = StringField('Email', validators=[DataRequired(), Email(), length(1, 64)])
    username = StringField('Username', validators=[DataRequired(),
                                                   length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                          'Usernames must have only letters, '
                                                          'numbers, dots or underscores')])
    password = PasswordField('Password',
                             validators=[DataRequired(), EqualTo('password2', message='password is not match '), ])
    password2 = PasswordField('confirm password', validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered')

    def validate_username(self, field):
        if User.query.filter_by(name=field.data).first():
            raise ValidationError('Username is already in user')

