# _*_coding:utf-8_*_
from flask import Blueprint

auth = Blueprint('auth',__name__)

from . import views