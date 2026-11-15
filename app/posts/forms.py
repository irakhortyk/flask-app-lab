from datetime import datetime as dt
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, DateTimeLocalField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

CATEGORIES = [
    ("news", "News"),
    ("publication", "Publication"),
    ("tech", "Tech"),
    ("other", "Other")
]


class PostForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[DataRequired(message="Введіть заголовок"), Length(min=2, max=150)]
    )
    content = TextAreaField(
        "Content",
        render_kw={"rows": 5, "cols": 40},
        validators=[DataRequired(message="Введіть текст поста")]
    )
    is_active = BooleanField("Active Post", default=True)
    publish_date = DateTimeLocalField(
        "Publish Date",
        format="%Y-%m-%dT%H:%M",
        default=dt.now,
        validators=[Optional()]
    )
    category = SelectField(
        "Category",
        choices=CATEGORIES,
        default="news",
        validators=[Optional()]
    )
    submit = SubmitField("Submit")