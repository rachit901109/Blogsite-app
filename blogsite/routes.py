import os,secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from blogsite import app, db, bcrypt
from blogsite.forms import Registration_form, Login_form, Update_account_form
from blogsite.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

dummy_posts = [
    {
        'title':'Visualizing MNIST',
        'author':'Rachit Patni',
        'content':"""Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur vitae hendrerit nisi. Phasellus sed sapien neque. Ut vel tincidunt erat. Nam in lobortis augue, non accumsan sem. Morbi a ipsum nec lectus porttitor tristique. Duis ac ante et diam venenatis lacinia id id nibh. Maecenas faucibus gravida diam, vel elementum odio euismod quis. Aliquam blandit risus id odio hendrerit interdum condimentum at ante. Ut dictum pulvinar pellentesque. Vestibulum faucibus elit mauris, eu pretium nisi condimentum ac. Cras feugiat gravida aliquet.

                    Nullam tempor tellus nunc, non faucibus ipsum ultrices non. Vestibulum accumsan dui ac mauris elementum, vel commodo neque interdum. Phasellus pharetra id felis eu viverra. Aliquam fringilla magna ut dolor fringilla placerat. Praesent accumsan maximus nisi, vitae maximus nunc rutrum scelerisque. Duis eu congue dui. Vestibulum elementum suscipit justo a imperdiet. Etiam sed eros vel justo faucibus sagittis eu vitae orci. Curabitur eu nibh sit amet massa feugiat euismod. Fusce mauris risus, semper ut condimentum posuere, tincidunt vel lorem. Aenean in vulputate urna. Nulla blandit risus at ex sodales, eu pretium arcu accumsan. Nam sed nisl bibendum justo consequat sagittis vitae et elit. Ut accumsan, ex nec pellentesque convallis, mi enim lobortis sapien, sed mattis purus leo non diam. Suspendisse potenti.

                    Nunc nec dui a nisl rhoncus suscipit vitae non risus. Curabitur ac sapien fermentum, dignissim mauris ac, finibus quam. Sed gravida varius dui ac malesuada. Donec mollis, enim a viverra laoreet, diam metus ultricies libero, id varius risus ipsum at eros. Curabitur auctor tincidunt rutrum. Curabitur efficitur tortor sapien, consectetur dapibus elit consectetur eget. Fusce cursus cursus sem quis porta. Integer rutrum sem a hendrerit molestie. Duis molestie quam id elementum fringilla. Suspendisse potenti. Pellentesque mattis nunc nec ipsum lacinia, a ullamcorper elit hendrerit. Cras at turpis eu mi dapibus accumsan in nec arcu. Duis vitae lorem ullamcorper, consequat dui ut, porta libero. In hac habitasse platea dictumst. Nunc sed leo dolor.
                """,
        'date_posted':'August 4,2023'
    },
    {
        'title':'Implementing CNN',
        'author':'Varun Pillai',
        'content':"""Morbi sodales fermentum quam, a euismod quam feugiat a. Phasellus non libero nec dolor dignissim sagittis ac consequat diam. Nullam lobortis, tortor et posuere fringilla, magna nulla viverra libero, in tempus ligula nulla at dolor. Pellentesque volutpat auctor massa, quis tristique urna molestie scelerisque. Mauris interdum suscipit risus at hendrerit. Phasellus eu nibh in ex sollicitudin efficitur. Mauris mauris lacus, facilisis non urna sed, vulputate dapibus ex. Phasellus consequat nibh vel tempor malesuada. Aliquam sed ex quis nisi consectetur suscipit a ut dui. Praesent ante lacus, tristique eget aliquet eu, molestie sed ipsum. Cras gravida leo ac quam fringilla, in tempor lacus ullamcorper. Nam ex nisl, ornare eu vulputate eu, eleifend porttitor turpis. Maecenas posuere ligula vitae justo gravida, a rhoncus lectus volutpat. Nullam semper ut augue ac rhoncus.
                """,
        'date_posted':'July 23,2023'
    }
]

@app.route('/')
@app.route('/home')
def home():
    # return "<h1> Home Page </h1>"
    return render_template('home.html',dummy_posts=dummy_posts,page_title='CaseBook')


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