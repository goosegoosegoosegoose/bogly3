"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash, url_for
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag


app = Flask(__name__)

app.config['SECRET_KEY'] = "whatnow"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///bogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

@app.route('/')
def homepage():
    """?"""

    return redirect('/users')

@app.route('/users')
def users():
    """users list interface"""

    users = User.query.all()

    return render_template("users.html", users=users)

@app.route('/users/new', methods=["GET", "POST"])
def create_user():
    """Create user form"""
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        if request.form['image_url'] == '':
            image_url = None
        else:
            image_url = request.form['image_url']

        new_user = User(first_name=first_name, last_name=last_name, image_url=image_url)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/users')
    else:
        return render_template("userform.html")


@app.route('/users/<int:user_id>')
def user_page(user_id):
    """User information"""

    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id==user.id).all()

    return render_template("userpage.html", user=user, posts=posts)

@app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
def edit_user(user_id):
    """Edit user info"""

    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        if request.form['image_url'] == '':
            user.image_url = None
        else:
            user.image_url = request.form['image_url']

        db.session.commit()

        return redirect(f'/users/{user.id}')
    else:
        return render_template("useredit.html", user=user)

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    """Delete user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new', methods=["GET", "POST"])
def create_post(user_id):
    """New post form"""

    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        post_tags = request.form.getlist('tags')

        new_post = Post(title=title, content=content, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()

        for id in post_tags:
            new_post.unique_tags.append(PostTag(tag_id=id))
        db.session.add(new_post)
        db.session.commit()
        return redirect(f'/users/{user_id}')
    else:
        return render_template("postform.html", user=user, tags=tags)

@app.route('/posts/<int:post_id>')
def post_page(post_id):
    """Show Post"""

    post = Post.query.get_or_404(post_id)
    tags = post.tags

    return render_template("postpage.html", post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def post_edit(post_id):
    """Edit post form"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    if request.method == 'POST':
        post.title = request.form['title']
        post.content = request.form['content']
        post.tags = []
        db.session.commit()

        post_tags = request.form.getlist('tags')

        for id in post_tags:
            post.unique_tags.append(PostTag(tag_id=id))
        db.session.add(post)
        db.session.commit()

        return redirect(f'/posts/{post_id}')
    else:
        return render_template("postedit.html", post=post, tags=tags)

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """delete the post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/users/{post.user_id}')

@app.route('/tags')
def tags():
    """tag page"""

    tags = Tag.query.all()

    return render_template("tags.html", tags = tags)

@app.route('/tags/new', methods=['GET', 'POST'])
def create_tag():
    """Tag form"""

    if request.method == 'POST':
        name = request.form['name']
        new_tag = Tag(name=name)

        db.session.add(new_tag)
        db.session.commit()

        return redirect('/tags')
    else:
        return render_template("tagform.html")

@app.route('/tags/<int:tag_id>')
def tag_page(tag_id):
    """Tag info page"""

    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts

    return render_template("tagpage.html", tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=['GET', 'POST'])
def edit_tag(tag_id):
    """Tag form"""
    
    tag = Tag.query.get_or_404(tag_id)

    if request.method == 'POST':
        if request.form['name']=='':
            
            flash("Please enter somthing")
            return redirect(url_for("edit_tag"))

        else:
            tag.name = request.form['name']

            db.session.commit()

        return redirect(f'/tags/{tag_id}')
    else:
        return render_template("tagedit.html", tag=tag)

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """Delete a tag"""

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')

    # cant delete a tag thats being used despite using ondelte='CASCADE', probably because it's a primary key?