from flask import render_template, request
from app import app


@app.route("/")
@app.route("/resume")
def resume():
    return render_template("resume.html", title="Резюме — Ірина Хортюк")


@app.route("/contacts")
def contacts():
    return render_template("contacts.html", title="Контакти — Ірина Хортюк")


@app.route("/homepage")
def homepage():
    agent = request.user_agent
    return render_template("homepage.html", title="Головна сторінка", agent=agent)