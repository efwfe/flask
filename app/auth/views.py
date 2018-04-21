# _*_coding:utf-8_*_
from flask import render_template, flash, redirect, request, url_for
from flask_login import login_required, login_user
from app.models import User
from ..auth import auth
from forms import LoginForm,RegisterForm

@auth.route('/')
def index():
    return render_template('index.html')

# 登录
@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # check user in database?
        user = User.query.filter_by(email=form.email.data).first()
        print(user)
        if user is not None and user.verify_password(form.password.data):
            print(user.verify_password(form.password.data))
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next')or url_for('auth.index'))
        flash(u'账号或者密码错误') # 中文编码报错的问题
    return render_template('auth/login.html',form = form)

# 登出
@auth.route('/logout')
@login_required
def logout():
    pass

# 注册
@auth.route('/register')
def register():
    form = RegisterForm()
    return render_template('auth/login.html', form=form)

# 认证邮箱
@auth.route('/confirm')
def comfirm():
    pass

@auth.route('/secret')
@login_required
def secret():
    flash('this is a secret page')
    return render_template('index.html')