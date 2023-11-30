from flask import render_template, request, Blueprint, flash
from blogsite.models import Post, User
from blogsite.main.forms import Recommendation_engine_form
from blogsite.post_recommendations.recommendation_systems import ibcf_recommendation
from flask import current_app

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


@main.route('/recommendation_engine', methods=['GET', 'POST'])
def recommendation_engine():
    form=Recommendation_engine_form()
    recommended_posts = None

    with current_app.app_context():
        form.username.choices = [(user.username,user.username) for user in User.query.all()]

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # print(user,form.username.data,recommended_posts)
        engine = form.engine.data
        if user:
            if engine == 'ibcf':
                recommended_posts = ibcf_recommendation(user.id)
                # print("got here",recommended_posts)
                return render_template('recommendation_engine.html',form=form, recommended_posts=recommended_posts, page_title='Recommendation Engine')
            # yet to implement content based recommendation
            # elif engine == 'content-based':
            #     return render_template('recommendation_engine.html',page_title='Recommendation Engine')
        else:
            flash(message='User not found',category='danger')
    return render_template('recommendation_engine.html',form=form, recommended_posts=recommended_posts, page_title='Recommendation Engine')