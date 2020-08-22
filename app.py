"""Blogly application."""
from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, redirect, render_template, flash, session
from models import db, connect_db, User, Post, Tag, PostTag
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'ihaveasecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


connect_db(app)
db.drop_all()
db.create_all()


@app.route("/", methods=['GET'])
def root():
    """Homepage redirect to list of users"""
    return redirect("/users")


@app.route("/users", methods=['GET'])
def list_users():
    """List users and show add form."""
    users = User.query.all()
    return render_template('users/index.html', users=users)


@app.route('/users/new', methods=["GET"])
def users_new_form():
    """Show a form to create a new user"""

    return render_template('users/new.html')


@app.route("/users/new", methods=["POST"])
def users_new():
    """Handle form submission for creating a new user"""

    new_user = User(
        first_name=request.form['first_name'] or None,
        last_name=request.form['last_name'],
        image_url=request.form['image_url'])

    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show info on a single user."""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(user.id == user_id).all()
    return render_template('users/show.html', user=user)


@app.route("/<int:user_id>/edit")
def show_editpage(user_id):
    """Show info on a single user."""
    user = User.query.get_or_404(user_id)
    return render_template('users/edit.html', user=user)


@app.route('/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Handle form submission for updating an existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/<int:user_id>/delete")
def delete(user_id):
    """Show info on a single user."""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(f"/users")
