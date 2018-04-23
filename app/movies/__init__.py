# _*_coding:utf-8_*_
from flask import Blueprint

douban = Blueprint('douban',__name__)

from . import views