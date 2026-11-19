import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from app.config import config_map


class Base(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    })


db = SQLAlchemy(model_class=Base)
migrate = Migrate()

app = Flask(__name__)
app.config.from_object(config_map["development"])
os.makedirs(app.instance_path, exist_ok=True)

db.init_app(app)
migrate.init_app(app, db)

from app import views  # noqa: E402, F401
from app import models  # noqa: E402, F401
from app.users.views import users_bp  # noqa: E402
from app.products.views import products_bp  # noqa: E402
from app.posts import post_bp  # noqa: E402
from app.posts import models as post_models  # noqa: E402, F401

app.register_blueprint(users_bp)
app.register_blueprint(products_bp)
app.register_blueprint(post_bp)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404


def create_app(config_name=None):
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    config_cls = config_map.get(config_name, config_map["default"])
    app.config.from_object(config_cls)
    os.makedirs(app.instance_path, exist_ok=True)
    return app