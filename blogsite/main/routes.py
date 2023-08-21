from flask import render_template, request, Blueprint
from blogsite.models import Post

main = Blueprint(name='main',import_name=__name__)

# page is a query parameter- defined set of parameters attached to the end of a URL.
@main.route('/')
@main.route('/home')
def home():
    page = request.args.get(key='page',default=1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=3)
    return render_template('home.html',posts=posts,page_title='CaseBook')


@main.route('/about')
def about():
    # return "Nothing here"
    return render_template('about.html',page_title='About')