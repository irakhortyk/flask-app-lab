from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, DecimalField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, NumberRange

class ContactForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            DataRequired(message="Це поле є обов'язковим"),
            Length(min=4, max=10, message="Довжина імені має бути від 4 до 10 символів")
        ]
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="Це поле є обов'язковим"),
            Email(message="Введіть коректну адресу електронної пошти")
        ]
    )
    phone = StringField(
        "Phone",
        validators=[
            DataRequired(message="Це поле є обов'язковим"),
            Regexp(r"^\+380\d{9}$", message="Формат телефону має бути: +380????????? (9 цифр після +380)")
        ]
    )
    subject = SelectField(
        "Subject",
        choices=[
            ("general", "Загальне питання"),
            ("support", "Технічна підтримка"),
            ("cooperation", "Співпраця"),
            ("feedback", "Відгук або пропозиція")
        ],
        validators=[DataRequired()]
    )
    message = TextAreaField(
        "Message",
        validators=[
            DataRequired(message="Це поле є обов'язковим"),
            Length(max=500, message="Повідомлення не може перевищувати 500 символів")
        ]
    )
    submit = SubmitField("Send Message")

class ProductForm(FlaskForm):
    name = StringField(
        "Назва товару",
        validators=[
            DataRequired(message="Введіть назву товару"),
            Length(min=3, message="Назва має містити мінімум 3 символи")
        ]
    )
    content = TextAreaField(
        "Опис товару",
        validators=[DataRequired(message="Введіть опис товару")],
        render_kw={"rows": 5, "cols": 40}
    )
    price = DecimalField(
        "Ціна (грн)",
        places=2,
        validators=[
            DataRequired(message="Вкажіть ціну товару"),
            NumberRange(min=0.01, message="Ціна має бути додатною")
        ]
    )
    category = SelectField(
        "Категорія",
        choices=[
            ("Електроніка", "Електроніка"),
            ("Одяг", "Одяг"),
            ("Книги", "Книги"),
            ("Аксесуари", "Аксесуари")
        ],
        validators=[DataRequired()]
    )
    quantity = IntegerField(
        "Кількість одиниць",
        validators=[
            DataRequired(message="Вкажіть кількість (або 0)"),
            NumberRange(min=0, message="Кількість не може бути від'ємною")
        ]
    )
    image = FileField(
        "Зображення товару (PNG, JPG, JPEG)",
        validators=[
            FileAllowed(["png", "jpg", "jpeg"], "Дозволені лише формати PNG, JPG та JPEG!")
        ]
    )
    submit = SubmitField("Зберегти товар")