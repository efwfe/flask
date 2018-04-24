# _*_coding:utf-8_*_

from app import db, login_manager
from datetime import datetime
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMIN = 16

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),unique=True)
    default = db.Column(db.Boolean,default=False,index=True)
    permissions =db.Column(db.Integer)
    users = db.relationship('User',backref='relo',lazy='dynamic')

    def __repr__(self):
        return '<Role%s>'%self.name

    @staticmethod
    def insert_roles():
        roles = {
            'User':[Permission.FOLLOW, Permission.COMMENT, Permission.WRITE],
            'Moderator':[Permission.FOLLOW, Permission.COMMENT,
                          Permission.WRITE, Permission.MODERATE],
            'Administrator':[Permission.FOLLOW, Permission.COMMENT,
                              Permission.WRITE, Permission.MODERATE,
                              Permission.ADMIN],
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

class Comment(db.Model):
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    comment_text = db.Column(db.Text())
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    movie_id = db.Column(db.Integer,db.ForeignKey('in_movies.id'))

class User(UserMixin,db.Model):
    # __table__ = 'users'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255),unique=True)
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer,db.ForeignKey('roles.id'))
    confirmed = db.Column(db.Boolean, default=False)
    user_comment = db.relationship('Comment',foreign_keys=[Comment.user_id],backref=db.backref('user',lazy='joined'),lazy='dynamic')


    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
    #


    def generate_condirmation_token(self,expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm':self.id})

    def confirm(self,token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def can(self,perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_adminstrator(self):
        return self.cam(Permission.ADMIN)

    def __repr__(self):
        return '<User %r>' % self.name


class ComingMovies(db.Model):
    __tablename__ = 'in_movies'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    image = db.Column(db.String(255),nullable=True)
    average = db.Column(db.Float)
    alt = db.Column(db.String(255))
    title = db.Column(db.String(255))
    commented = db.relationship('Comment',foreign_keys=[Comment.movie_id],backref=db.backref('movie',lazy='joined'),lazy='dynamic')



class AnonymousUser(AnonymousUserMixin):
    def can(self,permissions):
        return False

    def is_active(self):
        return False

login_manager.anonymous_user = AnonymousUser

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
