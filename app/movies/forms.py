# _*_coding:utf-8_*_

from wtforms.validators import DataRequired, length, Email, Regexp, EqualTo, ValidationError
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField,PasswordField,TextAreaField

class CommentForm(FlaskForm):
    title = StringField(u'影片:')
    text = TextAreaField(u'评论:',validators=[DataRequired()])
    submit = SubmitField(u'提交')
