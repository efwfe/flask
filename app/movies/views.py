# _*_coding:utf-8_*_
from flask import render_template
from sqlalchemy import desc

from app.models import ComingMovies
from . import douban


@douban.route('/')
def douban():
    movies = ComingMovies.query.order_by(ComingMovies.average.desc())
    return render_template('movie/douban.html', movies=movies)
