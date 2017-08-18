#-*-coding:utf-8-*-  
import os
from flask.ext.login import LoginManager
from flask.ext.openid import OpenID
from config import basedir

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

#
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


# Flask-OpenID扩展需要一个存储文件的临时文件夹的路径，这里的'tmp'就是
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))

from app import views, models