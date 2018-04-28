# _*_coding:utf-8_*_
from flask import render_template, flash, redirect, request, url_for, session, make_response
from flask_login import login_required, login_user, logout_user, current_user

from app import db
from app.models import User
from ..auth import auth
from forms import *
from ..mail import send_email
from ..utils.captcha import captcha

# 验证码
@auth.route('/verify')
def verify():
    catp = captcha.Captcha().instance()
    name, text, value = catp.generate_captcha()
    session[text.upper()] = text
    response = make_response(value)
    response.headers['Content-Type'] = 'image/jpeg'
    return  response

# 登录
@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # check verify
        code = form.verify.data
        if session[code.upper().decode()] == code:
            # check user in database
            user = User.query.filter_by(email=form.email.data).first()
            if user is not None and user.verify_password(form.password.data):
                login_user(user, form.remember_me.data)
                return redirect(request.args.get('next')or url_for('douban.douban_index'))
            flash(u'账号或者密码错误') # 中文编码报错的问题
        else:
            flash(u'验证码错误')
            return render_template('auth/login.html',form = form)

    return render_template('auth/login.html',form = form)

# 登出
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash(u'您已登出，欢迎再次访问')
    return redirect(url_for('auth.login'))

# 注册
@auth.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        code = form.verify.data
        if session[code.upper().decode()] ==form.verify.data:
            user=User(email=form.email.data,name=form.username.data,password=form.password.data)
            try:
                db.session.add(user)
                db.session.commit()
            except:
                db.session.rollback()
                flash(u'邮箱已经被占用')
                return redirect(url_for('auth.register'))
            token = user.generate_condirmation_token()
            send_email(user.email,'请认证您的邮箱:','mail/new_user',user=user,token=token)
            return redirect(url_for('auth.login'))
        else:
            flash(u'验证码错误')
            return render_template('auth/register.html', form=form)
    flash(u"填写不完整")
    return render_template('auth/register.html', form=form)

# 认证邮箱
@auth.route('/confirm/<token>')
@login_required
def check_confirm(token):
    if current_user.confirmed:
        return redirect(url_for('douban.douban'))
    if current_user.confirm(token):
        flash('You have confirmed your account .Thanks!')
    else:
        flash(u'链接已过期，请点击一下链接获取验证码')
        return redirect(url_for('auth.unconfirm'))
    return redirect(url_for('douban.douban'))

@auth.route('/unconfirmed')
@login_required
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return render_template('auth/unconfirmed.html')
    return redirect(url_for('auth.reconfirm'))

@auth.route('/confirm')
@login_required
def reconfirm():
    token = current_user.generate_condirmation_token(),
    send_email(current_user.email,u'激活您的账号','mail/new_user',user=current_user,token=token)
    flash('A new mail had sent to you ')
    return redirect(url_for('auth.index'))

# 用户资料展示
@auth.route('/userinfo',methods=['GET','POST'])
@login_required
def user_info():
    user = User.query.filter(User.name==current_user.name).first()
    form = UserInfo()
    if form.validate_on_submit():
        user.name = form.name.data
        # user.email = form.email.data
        db.session.add(user)
        db.session.commit()
        flash(u'资料已更新')
        return redirect(url_for('auth.user_info'))
    # form.email.data=user.email
    form.name.data =user.name
    return render_template('auth/userinfo.html',form=form)

# 用户资料修改

@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template("auth/change_password.html", form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Reset Your Password',
                       'auth/email/reset_password',
                       user=user, token=token,
                       next=request.args.get('next'))
        flash('An email with instructions to reset your password has been '
              'sent to you.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = ChangeEmailForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm your email address',
                       'auth/email/change_email',
                       user=current_user, token=token)
            flash('An email with instructions to confirm your new email '
                  'address has been sent to you.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid email or password.')
    return render_template("auth/change_email.html", form=form)


@auth.route('/change_email/<token>')
@login_required
def change_email(token):
    if current_user.change_email(token):
        db.session.commit()
        flash('Your email address has been updated.')
    else:
        flash('Invalid request.')
    return redirect(url_for('main.index'))




