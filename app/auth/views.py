# _*_coding:utf-8_*_
from flask import render_template

from ..auth import auth

@auth.route('/')
def index():
    return render_template('index.html')
