from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from blogsite import db
from blogsite.posts.forms import Post_form
from blogsite.models import Post
from flask_login import current_user, login_required

posts = Blueprint(name='posts',import_name=__name__)


# @login required to ensure only logged in user update posts
@posts.route('/post/new',methods=['GET','POST'])
@login_required
def new_post():
    form = Post_form()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content= form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash(message='Post Created',category='success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html', page_title='New Post', form=form)


# display individual posts by post id flask allows to create variable in our routes
@posts.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html',page_title=post.title,post=post)


# route to update post once updated return to individual post 
@posts.route('/post/<int:post_id>/update',methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    # if current user is author of post only then allow
    if post.author != current_user:
        abort(403)
    form = Post_form()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash(message='Updated Post',category='success')
        return redirect(url_for('posts.post',post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', page_title='Update Post', form=form, legend='Update Post')
    

# delte a post return to home
@posts.route('/post/<int:post_id>/delete',methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash(message='Post deleted Succesfully',category='info')
    return redirect(url_for('main.home'))
