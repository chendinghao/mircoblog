#-*-coding:utf-8-*-  
from app import db

# 用户模型
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nickname = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    posts = db.relationship('Post', backref = 'author', lazy='dynamic')
    def __repr__(self):
        return '<User %r>' % (self.nickname)
    
    # 返回 False 表示用户的对象因为某些原因不允许被认证
    def is_authenticated(self):
        return True

    # 返回 False 表示用户是无效的
    def is_active(self):
        return True

    # 返回 False 表示用户是伪造的，不允许登录
    def is_annoymous(self):
        return False

    # 返回用户唯一标识符
    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)