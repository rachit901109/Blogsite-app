import os,secrets
from PIL import Image
from flask import url_for, current_app
from blogsite import mail
from flask_mail import Message


# saves uploaded pic in profile_pic with a random name; use this name to load the updated pfp
def save_picture(pfp):
    random_hex = secrets.token_hex(8)
    _,ext = os.path.splitext(pfp.filename)
    pfp_name = random_hex+ext
    pfp_path = os.path.join(current_app.root_path,'static/profile_pic',pfp_name)

    resized_img = Image.open(pfp)
    resized_img.thumbnail(tuple([150,150]))

    resized_img.save(pfp_path)
    return pfp_name



# send reset password link to users mail. creates token and sends mail
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(subject="Password Reset Request", sender=os.environ.get('My_Mail_Add'), recipients=[user.email])
    msg.body=f"Reset link only valid for 15 mins {url_for('users.reset_token',token=token,_external=True)}\nIgnore if you didn't make request."
    mail.send(msg)