# _*_coding:utf-8_*_

from threading import Thread

from flask import render_template
from flask_mail import  Message
from . import mail
from manage import app

def send_asnyc_message(app,msg):
    with app.app_context():
        mail.send(msg)

def send_email(to,subject, template,**kwargs):
    msg = Message(app.config['FLASK_MAIL_SUBJECT_PREFIX']+' '+subject,
                  sender=app.config['FLASK_MAIL_SENDER'],recipients=[to]
                  )

    msg.body = render_template(template + '.txt',**kwargs)
    msg.html = render_template(template + '.html',**kwargs)

    thr = Thread(target=send_asnyc_message,args=[app,msg])
    thr.start()

    return thr