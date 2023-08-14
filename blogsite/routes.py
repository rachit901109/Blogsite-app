import os,secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from blogsite import app, db, bcrypt
from blogsite.forms import Registration_form, Login_form, Update_account_form, Post_form
from blogsite.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home():
    # return "<h1> Home Page </h1>"
    return render_template('home.html',posts=Post.query.all(),page_title='CaseBook')


@app.route('/about')
def about():
    # return "Nothing here"
    return render_template('about.html',page_title='About')


@app.route('/register',methods=['GET','POST'])
def register():
    form = Registration_form()
    # if form is valid create user add to db commit flash success and return to login; else render register page again
    if form.validate_on_submit():
        hash_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hash_pass)
        db.session.add(user)
        db.session.commit()
        flash(message=f"Welcome {form.username.data}!", category='success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form,page_title='Register')


@app.route('/login',methods=['GET','POST'])
def login():
    # if logged in user tries to login again; Not need now cause for logged in user page is now updated
    if current_user.is_authenticated:
        flash(message=f'You are already logged in as {current_user.username}',category='warning')
        return redirect(url_for('home'))
    form = Login_form()
    # if all fields on form are valid, check if hashed-password for submitted email matches password save in DB else flash mail password didnt match error
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, form.remember.data)
            # return user to previous page if he came to login from a prev page else return to home
            next_page = request.args.get('next')
            flash(message=f"Logged in as {user.username}!", category='success')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('home'))
        else:
            flash(message='Email and password did not match',category='danger')
    return render_template('login.html', form=form,page_title='Login')

# logout functionality made easy by login manager
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# saves uploaded pic in profile_pic with a random name; use this name to load the updated pfp
def save_picture(pfp):
    random_hex = secrets.token_hex(8)
    _,ext = os.path.splitext(pfp.filename)
    pfp_name = random_hex+ext
    pfp_path = os.path.join(app.root_path,'static/profile_pic',pfp_name)

    resized_img = Image.open(pfp)
    resized_img.thumbnail(tuple([150,150]))

    resized_img.save(pfp_path)
    return pfp_name

# account details and feature to update details
@app.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = Update_account_form()
    if form.validate_on_submit():
        if form.pfp.data:
            pfp_name = save_picture(form.pfp.data)
            current_user.img_file = pfp_name
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(message="Account has been updated", category='success')
        return redirect(url_for('account'))
    # fill form with current users data
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    img_file = url_for('static',filename=r'profile_pic/'+current_user.img_file)
    return render_template('account.html', page_title='Account', form = form, img_file = img_file)

# query page to see all users and posts
@app.route('/Query')
def query():
    user_list = []
    for user in User.query.all():
        user_list.append({'id':user.id,'name':user.username,'mail':user.email,'pfp':user.img_file})
    return render_template('query.html', page_title='Query DB', user_list=user_list)

# add posts
@app.route('/New Post',methods=['GET','POST'])
@login_required
def new_post():
    form = Post_form()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content= form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(message='Post Created',category='success')
        return redirect(url_for('home'))
    return render_template('create_post.html', page_title='New Post', form=form)