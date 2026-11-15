import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import config_map

db = SQLAlchemy()
migrate = Migrate()

app = Flask(__name__)
app.config.from_object(config_map["development"])
os.makedirs(app.instance_path, exist_ok=True)

db.init_app(app)
migrate.init_app(app, db)

from app import views  # noqa: E402, F401
from app.users.views import users_bp  # noqa: E402
from app.products.views import products_bp  # noqa: E402
from app.posts import post_bp  # noqa: E402
from app.posts import models  # noqa: E402, F401

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