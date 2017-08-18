#-*-coding:utf-8-*-  
# views.py是视图函数，在这里使用模板 

# 关于 FLASK.G
# flask.g
# Just store on this whatever you want. For example a database connection or the user that is currently logged in.
# Starting with Flask 0.10 this is stored on the application context and no longer on the request context which means it becomes available if only the application context is bound and not yet a request.

from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm
from .models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = { 'nickname': 'Miguel' } # fake user
    posts = [ # fake array of posts
        {
            'author': { 'nickname': 'John' },
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': { 'nickname': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        }
    ]

    # render_template（）函数需要传入模板名以及一些模板变量列表，返回一个所有变量被替换的渲染的模板
    return render_template("index.html",
        title = 'Home',
        user = user,
        posts = posts)

# index view function suppressed for brevity
#@app.route('/login', methods = ['GET', 'POST'])
#@oid.loginhandler
#def login():
    # form = LoginForm()
    # if form.validate_on_submit():
    #     flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
    #     return redirect('/index')
    # return render_template('login.html',
    #     title = 'Sign In',
    #     form = form,
    #     providers = app.config['OPENID_PROVIDERS'])

# 登录视图函数
@app.route('/login', methods=['GET', 'POST'])
@oid.loginhandler
def login():
    # 如果是一个已经登录的用户，则返回到index界面
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])

# 用于从数据库加载用户
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

# Flask-OpenID 登录回调
@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember = remember_me)
    return redirect(request.args.get('next') or url_for('index'))

# 在登录之前检查
@app.before_request
def before_request():
    g.user = current_user

# 等出
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))