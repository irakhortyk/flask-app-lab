import unittest
from app import app


class FlaskUserBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "test-secret-key"
        self.client = app.test_client()

    def test_greetings_page(self):
        response = self.client.get("/users/hi/John?age=30")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"JOHN", response.data)
        self.assertIn(b"30", response.data)

    def test_login_page_loads(self):
        response = self.client.get("/users/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

    def test_login_success(self):
        with self.client:
            response = self.client.post(
                "/users/login",
                data={"username": "user1", "password": "12345"},
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"user1", response.data)
            from flask import session
            self.assertEqual(session.get("username"), "user1")

    def test_login_wrong_credentials(self):
        response = self.client.post(
            "/users/login",
            data={"username": "user1", "password": "wrong_password"},
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Wrong data! Try again!", response.data)

    def test_profile_unauthorized_redirect(self):
        response = self.client.get("/users/profile", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

    def test_logout(self):
        with self.client:
            self.client.post("/users/login", data={"username": "user1", "password": "12345"})
            response = self.client.post("/users/logout", follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Login", response.data)
            from flask import session
            self.assertNotIn("username", session)

    def test_add_and_delete_cookie(self):
        with self.client:
            self.client.post("/users/login", data={"username": "user1", "password": "12345"})

            response = self.client.post(
                "/users/profile",
                data={
                    "action": "add_cookie",
                    "cookie_key": "test_key",
                    "cookie_value": "test_val",
                    "cookie_max_age": "3600"
                },
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"test_key", response.data)
            self.assertIn(b"test_val", response.data)

            response_del = self.client.post(
                "/users/profile",
                data={
                    "action": "delete_cookie",
                    "delete_key": "test_key"
                },
                follow_redirects=True
            )
            self.assertEqual(response_del.status_code, 200)

    def test_set_theme_cookie(self):
        with self.client:
            self.client.post("/users/login", data={"username": "user1", "password": "12345"})
            response = self.client.get("/users/set-theme/dark", follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"bg-dark", response.data)


if __name__ == "__main__":
    unittest.main()