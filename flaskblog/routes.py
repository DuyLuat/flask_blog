from flask.globals import request
from flaskblog import app, db, bcrypt
from flask import Flask, render_template, flash
from flask_login import current_user, login_required, login_user, logout_user 
from flask.helpers import url_for
from sqlalchemy.orm import backref
from werkzeug.utils import redirect
# from wtforms import form
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import Post, User

posts=[
    {
        'title': 'Blog Post 1',
        'author': 'Đào Duy Luật',
        'content': 'This is firt post',
        'date_post': '12/12/2020'
    },
    {
        'title': 'Blog Post 2',
        'author': 'Đào Duy Hưng',
        'content': 'This is second post',
        'date_post': '12/12/2021'
    },
    {
        'title': 'Blog Post 3',
        'author': 'Đào Ngân Hà',
        'content': 'This is thirth post',
        'date_post': '13/12/2021'
    }
]


@app.route('/')
@app.route('/home')
def home():
    title='This is test page'
    return render_template('home.html', posts=posts, title=title)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated():
        return redirect(url_for('home'))
    form=RegistrationForm()

    if form.validate_on_submit():
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user=User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        flash('Tài khoản của bạn đã được tạo, bây giờ bạn có thể đăng nhập!','success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title='Register')

@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page=request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Đăng nhập không thành công!','danger')
    return render_template('login.html', form=form, title='Login')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    return render_template('account.html', title='Account')