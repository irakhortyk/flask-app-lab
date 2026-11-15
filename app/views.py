import logging
from flask import render_template, request, redirect, url_for, flash
from app import app
from app.forms import ContactForm

contact_logger = logging.getLogger("contact_logger")
contact_logger.setLevel(logging.INFO)
if not contact_logger.handlers:
    file_handler = logging.FileHandler("contacts.log", encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    contact_logger.addHandler(file_handler)


@app.route("/")
@app.route("/resume")
def resume():
    return render_template("resume.html", title="Резюме — Ірина Хортюк")


@app.route("/contacts", methods=["GET", "POST"])
@app.route("/contact", methods=["GET", "POST"])
def contacts():
    form = ContactForm()
    if request.method == "POST":
        if form.validate_on_submit():
            contact_logger.info(
                f"Name: {form.name.data} | Email: {form.email.data} | "
                f"Phone: {form.phone.data} | Subject: {form.subject.data} | "
                f"Message: {form.message.data}"
            )
            flash("Ваше повідомлення успішно відправлено та записано в лог!", "success")
            return redirect(url_for("contacts"))
        else:
            flash("Помилка відправки форми! Перевірте правильність заповнення полів.", "danger")

    return render_template("contacts.html", title="Контакти — Ірина Хортюк", form=form)


@app.route("/homepage")
def homepage():
    agent = request.user_agent
    return render_template("homepage.html", title="Головна сторінка", agent=agent)