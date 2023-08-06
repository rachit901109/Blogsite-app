from flask import render_template, url_for, flash, redirect
from blogsite import app
from blogsite.forms import Registration_form, Login_form

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
    if form.validate_on_submit():
        flash(message=f"Welcome {form.username.data}!", category='success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form,page_title='Register')


@app.route('/login',methods=['GET','POST'])
def login():
    form = Login_form()
    if form.validate_on_submit():
        if form.email.data == 'abc@gmail.com' and form.password.data == '123123':
            flash(message='Login successfull',category='success')
            return redirect(url_for('home'))
        else:
            flash(message='Username and password did not match',category='danger')
    return render_template('login.html', form=form,page_title='Login')
