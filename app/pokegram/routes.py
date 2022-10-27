from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required, current_user
from app.models  import Post
from .forms import PostForm

pokegram = Blueprint('pokegram', __name__, template_folder='pokegram_templates')

@pokegram.route('/posts/create', methods=["GET", "POST"])
@login_required
def createPost():
    form = PostForm()
    if request.method == "POST":
        if form.validate():
            title = form.title.data
            img_url = form.img_url.data
            caption = form.caption.data

            post = Post(title, img_url, caption, current_user.id)

            post.saveToDB()

            return redirect(url_for('homePage'))

    return render_template('create_post.html', form=form)

@pokegram.route('/posts')
def viewPosts():
    posts = Post.query.order_by(Post.date_created).all()[::-1]
    return render_template('feed.html', posts=posts)

@pokegram.route('/posts/<int:post_id>')
def viewSinglePost(post_id):
    # post = Post.query.filter_by(id = post_id).first()
    post = Post.query.get(post_id)

    if post:
        return render_template('single_post.html', post=post)
    else:
        return redirect(url_for('pokegram.viewPosts'))

@pokegram.route('/posts/<int:post_id>/update', methods=["GET", "POST"])
@login_required
def updatePost(post_id):
    post = Post.query.get(post_id)
    if current_user.id != post.user_id:
        flash('You cannot update this post...', 'danger')
        return redirect(url_for('pokegram.viewPosts'))

    form = PostForm()

    if request.method == "POST":
        if form.validate():
            title = form.title.data
            img_url = form.img_url.data
            caption = form.caption.data

            post.title = title
            post.img_url = img_url
            post.caption = caption

            post.saveChanges()

            return redirect(url_for('pokegram.viewSinglePost', post_id=post_id))

    return render_template('update_post.html', form=form, post=post)

@pokegram.route('/posts/<int:post_id>/delete', methods=["GET"])
@login_required
def deletePost(post_id):
    post = Post.query.get(post_id)
    if current_user.id == post.user_id:
        post.deleteFromDB()  
    else:
        flash('You cannot delete this post...', 'danger')
    return redirect(url_for('pokegram.viewPosts'))