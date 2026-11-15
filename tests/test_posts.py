import unittest
from app import create_app, db
from app.posts.models import Post


class PostTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("testing")
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_post(self):
        with self.app.app_context():
            response = self.client.post(
                "/post/create",
                data={
                    "title": "My first post",
                    "text": "This is TDD!",
                    "category": "tech",
                    "is_active": True
                },
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Post added successfully", response.data)

            post = db.session.query(Post).filter_by(title="My first post").first()
            self.assertIsNotNone(post)
            self.assertEqual(post.text, "This is TDD!")

    def test_list_posts(self):
        with self.app.app_context():
            p = Post(title="Visible Post", content="Hello SQLAlchemy", is_active=True)
            db.session.add(p)
            db.session.commit()

            response = self.client.get("/post")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Visible Post", response.data)

    def test_view_post_detail(self):
        with self.app.app_context():
            p = Post(title="Detail Post", content="Detailed content here")
            db.session.add(p)
            db.session.commit()

            response = self.client.get(f"/post/{p.id}")
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Detail Post", response.data)
            self.assertIn(b"Detailed content here", response.data)

    def test_update_post(self):
        with self.app.app_context():
            p = Post(title="Old Title", content="Old content")
            db.session.add(p)
            db.session.commit()
            post_id = p.id

            response = self.client.post(
                f"/post/{post_id}/update",
                data={
                    "title": "Updated Title",
                    "content": "Updated content",
                    "category": "news",
                    "is_active": True
                },
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            updated_post = db.session.get(Post, post_id)
            self.assertEqual(updated_post.title, "Updated Title")
            self.assertEqual(updated_post.content, "Updated content")

    def test_delete_post(self):
        with self.app.app_context():
            p = Post(title="Post to delete", content="Will be removed")
            db.session.add(p)
            db.session.commit()
            post_id = p.id

            response = self.client.post(f"/post/{post_id}/delete", follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            deleted_post = db.session.get(Post, post_id)
            self.assertIsNone(deleted_post)

    def test_404_not_found(self):
        with self.app.app_context():
            response = self.client.get("/post/9999")
            self.assertEqual(response.status_code, 404)
            self.assertIn(b"Oops! Page Not Found", response.data)


if __name__ == "__main__":
    unittest.main()