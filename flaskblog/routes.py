from flask.globals import request
from flaskblog import app, db, bcrypt
from flask import render_template, flash
from flask_login import current_user, login_required, login_user, logout_user 
from flask.helpers import url_for
from sqlalchemy.orm import backref
from werkzeug.utils import redirect
# from wtforms import form
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import Post, User
import secrets
import os
from PIL import Image


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
    if current_user.is_authenticated:
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


def save_picture(form_picture):
    random_hex=secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_picture.filename)
    picture_fn=random_hex + f_ext
    picture_path=os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size=(125, 125)
    i=Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route('/account', methods=['POST', 'GET'])
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file=save_picture(form.picture.data)
            current_user.image_file=picture_file
        current_user.username=form.username.data
        current_user.email=form.email.data
        db.session.commit()
        flash('Tài khoản của bạn đã được cập nhật', "success")
        return redirect(url_for('account'))
    elif request.method=='GET':
        form.data.username=current_user.username
        form.data.email=current_user.email
    image_file=url_for('static', filename='profile_pics' + current_user.image_file)
    return render_template('account.html', title='Account', form=form, image_file=image_file)