import os
import uuid
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from tinydb import TinyDB, Query
from app.forms import ProductForm

products_bp = Blueprint(
    "products",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/products/static"
)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "products.json")

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def get_db_table():
    db = TinyDB(DB_PATH, encoding="utf-8", ensure_ascii=False, indent=4)
    return db, db.table("products")


def save_uploaded_image(image_file):
    if image_file and getattr(image_file, "filename", ""):
        ext = os.path.splitext(secure_filename(image_file.filename))[1].lower()
        unique_filename = f"{uuid.uuid4().hex}{ext}"
        full_path = os.path.join(UPLOAD_FOLDER, unique_filename)
        image_file.save(full_path)
        return f"uploads/{unique_filename}"
    return ""


@products_bp.route("/product")
@products_bp.route("/products")
def list_products():
    db, table = get_db_table()
    products = table.all()
    db.close()
    return render_template("products/products.html", products=products, mode="list")


@products_bp.route("/product/add", methods=["GET", "POST"])
def add_product():
    form = ProductForm()
    if request.method == "POST":
        if form.validate_on_submit():
            db, table = get_db_table()
            all_items = table.all()
            new_id = max([item.get("id", 0) for item in all_items], default=0) + 1
            image_rel_path = save_uploaded_image(form.image.data)

            product_data = {
                "id": new_id,
                "name": form.name.data,
                "content": form.content.data,
                "price": round(float(form.price.data), 2),
                "category": form.category.data,
                "quantity": int(form.quantity.data),
                "image": image_rel_path,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            table.insert(product_data)
            db.close()
            flash(f'Товар "{product_data["name"]}" успішно додано!', "success")
            return redirect(url_for("products.list_products"))
        else:
            flash("Помилка валідації форми! Перевірте введені дані.", "danger")

    return render_template("products/products.html", form=form, mode="add")


@products_bp.route("/product/<int:id>")
def detail_product(id):
    db, table = get_db_table()
    ProductQuery = Query()
    product = table.get(ProductQuery.id == id)
    db.close()

    if not product:
        flash(f"Товар із ID {id} не знайдено!", "warning")
        return redirect(url_for("products.list_products"))

    return render_template("products/detail_product.html", product=product)


@products_bp.route("/product/<int:id>/edit", methods=["GET", "POST"])
def edit_product(id):
    db, table = get_db_table()
    ProductQuery = Query()
    product = table.get(ProductQuery.id == id)

    if not product:
        db.close()
        flash(f"Товар із ID {id} не знайдено!", "warning")
        return redirect(url_for("products.list_products"))

    form = ProductForm(data=product if request.method == "GET" else None)

    if request.method == "POST":
        if form.validate_on_submit():
            new_image_path = save_uploaded_image(form.image.data)
            final_image = new_image_path if new_image_path else product.get("image", "")

            updated_data = {
                "id": product["id"],
                "name": form.name.data,
                "content": form.content.data,
                "price": round(float(form.price.data), 2),
                "category": form.category.data,
                "quantity": int(form.quantity.data),
                "image": final_image,
                "created_at": product["created_at"]
            }
            table.update(updated_data, ProductQuery.id == id)
            db.close()
            flash(f'Товар "{updated_data["name"]}" успішно оновлено!', "success")
            return redirect(url_for("products.detail_product", id=id))
        else:
            flash("Помилка при редагуванні! Перевірте поля форми.", "danger")

    db.close()
    return render_template("products/products.html", form=form, product=product, mode="edit")


@products_bp.route("/product/<int:id>/delete", methods=["POST"])
def delete_product(id):
    db, table = get_db_table()
    ProductQuery = Query()
    product = table.get(ProductQuery.id == id)

    if product:
        table.remove(ProductQuery.id == id)
        db.close()
        flash(f'Товар "{product["name"]}" успішно видалено!', "info")
    else:
        db.close()
        flash("Товар не знайдено!", "warning")

    return redirect(url_for("products.list_products"))