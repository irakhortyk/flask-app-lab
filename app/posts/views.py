from datetime import datetime
from flask import render_template, request, redirect, url_for, flash, session, abort
from app import db
from . import post_bp
from .models import Post
from .forms import PostForm


@post_bp.route("/post")
@post_bp.route("/posts")
def all_posts():
    stmt = (
        db.select(Post)
        .where(Post.is_active == True)  # noqa: E712
        .order_by(Post.posted.desc())
    )
    posts = db.session.scalars(stmt).all()
    return render_template("posts.html", posts=posts)


@post_bp.route("/post/create", methods=["GET", "POST"])
@post_bp.route("/post/add_post", methods=["GET", "POST"])
def create_post():
    form = PostForm()

    if request.method == "POST":
        if "text" in request.form and not request.form.get("content"):
            form.content.data = request.form.get("text")

        if form.validate_on_submit():
            author_name = session.get("username", "Anonymous")
            posted_dt = form.publish_date.data or datetime.utcnow()
            category_val = form.category.data or "news"

            new_post = Post(
                title=form.title.data,
                content=form.content.data,
                is_active=form.is_active.data if form.is_active.data is not None else True,
                posted=posted_dt,
                category=category_val,
                author=author_name
            )
            db.session.add(new_post)
            db.session.commit()
            flash(f"Post added successfully! Post '{new_post.title}' has been added.", "success")
            return redirect(url_for("posts.all_posts"))
        else:
            flash("Enter the correct data in the form!", "danger")

    return render_template("add_post.html", form=form, title="Create a New Post")


@post_bp.route("/post/<int:id>")
def detail_post(id):
    post = db.session.get(Post, id)
    if not post:
        abort(404)
    return render_template("detail_post.html", post=post)


@post_bp.route("/post/<int:id>/update", methods=["GET", "POST"])
@post_bp.route("/post/<int:id>/edit", methods=["GET", "POST"])
def update_post(id):
    post = db.session.get(Post, id)
    if not post:
        abort(404)

    form = PostForm(obj=post)
    if request.method == "GET":
        form.publish_date.data = post.posted

    if request.method == "POST":
        if "text" in request.form and not request.form.get("content"):
            form.content.data = request.form.get("text")

        if form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            if form.is_active.data is not None:
                post.is_active = form.is_active.data
            if form.publish_date.data:
                post.posted = form.publish_date.data
            if form.category.data:
                post.category = form.category.data

            db.session.commit()
            flash("Пост оновлено!", "success")
            return redirect(url_for("posts.detail_post", id=post.id))
        else:
            flash("Enter the correct data in the form!", "danger")

    return render_template("add_post.html", form=form, post=post, title="Редагувати пост")


@post_bp.route("/post/<int:id>/delete", methods=["GET", "POST"])
@post_bp.route("/post/delete/<int:id>", methods=["GET", "POST"])
def delete_post(id):
    post = db.session.get(Post, id)
    if not post:
        abort(404)

    if request.method == "POST":
        db.session.delete(post)
        db.session.commit()
        flash("Пост успішно видалено.", "danger")
        return redirect(url_for("posts.all_posts"))

    return render_template("delete_confirm.html", post=post)