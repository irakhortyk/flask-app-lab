import os
import tempfile
import unittest
from app import app
import app.products.views as product_views


class FlaskProductCRUDTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False

        self.temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.temp_db.close()
        self.original_db_path = product_views.DB_PATH
        product_views.DB_PATH = self.temp_db.name

        self.client = app.test_client()

    def tearDown(self):
        product_views.DB_PATH = self.original_db_path
        if os.path.exists(self.temp_db.name):
            os.remove(self.temp_db.name)

    def test_create_and_read_product(self):
        response = self.client.post(
            "/product/add",
            data={
                "name": "Ноутбук",
                "content": "Потужний ноутбук для роботи",
                "price": "35000.50",
                "category": "Електроніка",
                "quantity": "5"
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("Ноутбук".encode("utf-8"), response.data)

        detail_resp = self.client.get("/product/1")
        self.assertEqual(detail_resp.status_code, 200)
        self.assertIn("Потужний ноутбук для роботи".encode("utf-8"), detail_resp.data)

    def test_update_product(self):
        self.client.post(
            "/product/add",
            data={
                "name": "Смартфон",
                "content": "Старий опис",
                "price": "12000.00",
                "category": "Електроніка",
                "quantity": "3"
            }
        )
        edit_resp = self.client.post(
            "/product/1/edit",
            data={
                "name": "Смартфон Pro",
                "content": "Оновлений опис товару",
                "price": "15000.00",
                "category": "Електроніка",
                "quantity": "10"
            },
            follow_redirects=True
        )
        self.assertEqual(edit_resp.status_code, 200)
        self.assertIn("Смартфон Pro".encode("utf-8"), edit_resp.data)
        self.assertIn("Оновлений опис товару".encode("utf-8"), edit_resp.data)

    def test_delete_product(self):
        self.client.post(
            "/product/add",
            data={
                "name": "Книга Python",
                "content": "Навчальний посібник",
                "price": "650.00",
                "category": "Книги",
                "quantity": "2"
            }
        )
        del_resp = self.client.post("/product/1/delete", follow_redirects=True)
        self.assertEqual(del_resp.status_code, 200)

        not_found_resp = self.client.get("/product/1", follow_redirects=True)
        self.assertIn("не знайдено".encode("utf-8"), not_found_resp.data)


if __name__ == "__main__":
    unittest.main()