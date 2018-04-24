# _*_coding:utf-8_*_
from flask import render_template, redirect, url_for
from flask_login import current_user,login_required
from sqlalchemy import desc
from app import db
from forms import CommentForm
from app.models import ComingMovies,Comment
from . import douban

@douban.route('/')
@login_required
def douban_index():
    form = CommentForm()
    movies = ComingMovies.query.order_by(ComingMovies.average.desc())
    return render_template('movie/douban.html', movies=movies,form=form)


# 提交评论
@douban.route('/<movie>',methods=['POST'])
def comment_post(movie):
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment()
        comment.comment_text = form.text.data
        # comment.user = current_user._get_current_object()
        comment.user_id = current_user.id
        movie_obj = ComingMovies.query.filter_by(title=movie).first()
        comment.movie_id= movie_obj.id
        db.session.add(comment)
        db.session.commit()

        return redirect('/')