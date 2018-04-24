# _*_coding:utf-8_*_
from flask import render_template, request, jsonify
from . import douban


@douban.app_errorhandler(404)
def forbidden(e):
    return render_template('404.html')

@douban.app_errorhandler(405)
def forbidden(e):
    return render_template('404.html')

@douban.app_errorhandler(403)
def forbidden(e):
    return render_template('404.html')
