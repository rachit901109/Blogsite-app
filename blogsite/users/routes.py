from flask import render_template, url_for, flash, redirect, request, Blueprint
from blogsite import db, bcrypt
from blogsite.users.forms import Registration_form, Login_form, Update_account_form, Request_resetform, Reset_passform
from blogsite.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
from blogsite.users.utils import save_picture, send_reset_email

users = Blueprint(name='users',import_name=__name__)

@users.route('/register',methods=['GET','POST'])
def register():
    form = Registration_form()
    # if form is valid create user add to db commit flash success and return to login; else render register page again
    if form.validate_on_submit():
        hash_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hash_pass)
        db.session.add(user)
        db.session.commit()
        flash(message=f"Welcome {form.username.data}!", category='success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form,page_title='Register')


# test user was created before adding hashing feature therefore its password isnt hashed and it can't be used
@users.route('/login',methods=['GET','POST'])
def login():
    # if logged in user tries to login again; Not need now cause for logged in user page is now updated
    if current_user.is_authenticated:
        flash(message=f'You are already logged in as {current_user.username}',category='warning')
        return redirect(url_for('main.home'))
    form = Login_form()
    # if all fields on form are valid, check if hashed-password for submitted email matches password save in DB else flash mail password didnt match error
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data.encode('utf-8')):
            login_user(user, form.remember.data)
            # return user to previous page if he came to login from a prev page else return to home
            next_page = request.args.get('next')
            flash(message=f"Logged in as {user.username}!", category='success')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('main.home'))
        else:
            flash(message='Email and password did not match',category='danger')
    return render_template('login.html', form=form,page_title='Login')


# logout functionality made easy by login manager
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


# account details and feature to update details
@users.route('/account',methods=['GET','POST'])
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
        return redirect(url_for('users.account'))
    # fill form with current users data
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    img_file = url_for('static',filename=r'profile_pic/'+current_user.img_file)
    return render_template('account.html', page_title='Account', form = form, img_file = img_file)


# query page to see all users and posts
@users.route('/Query')
def query():
    user_list = []
    post_list = []
    for user in User.query.all():
        user_list.append({'id':user.id,'name':user.username,'mail':user.email,'pfp':user.img_file})
    for post in Post.query.all():
        post_list.append({'id':post.id,'title':post.title,'posted_date':post.date_posted.strftime(r"%B %d, %Y"),'author':post.user_id})
    return render_template('query.html', page_title='Query DB', user_list=user_list,post_list=post_list)


# route to show posts made by a user
@users.route('/user/<string:username>/posts')
def user_posts(username):
    page = request.args.get(key='page',default=1,type=int)
    user = User.query.filter_by(username=username).first_or_404()
    img_file = url_for('static',filename=r'profile_pic/'+user.img_file)
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(per_page=3)
    return render_template('user_posts.html',page_title=username,user=user,posts=posts,img_file=img_file)


# route to request a password change takes email
@users.route('/reset_password', methods=['GET','POST'])
def reset_request():
    if current_user.is_authenticated:
        flash(message=f'You are already logged in as {current_user.username}',category='warning')
        return redirect(url_for('main.home'))
    form = Request_resetform()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash(message=f"Link to reset password is send to {user.email}. Link is only valid for 15 mins.", category="info")
        return redirect(url_for('users.login'))
    return render_template('reset_request.html',page_title="Request Password Reset",form=form)


# route to change password if token is valid
@users.route('/reset_password/<token>', methods=['GET','POST'])
def reset_token(token):
    if current_user.is_authenticated:
        flash(message=f'You are already logged in as {current_user.username}',category='warning')
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)

    if user is None:
        flash(message="Token is invalid or expired", category="warning")
        return redirect(url_for('users.reset_request'))
    form=Reset_passform()
    if form.validate_on_submit():
        hash_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hash_pass
        db.session.commit()
        flash(message=f"Password changed successfully", category='success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html',page_title="Request Password Reset",form=form)
