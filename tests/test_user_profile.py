import unittest
from app import create_app, db
from app.models import User

class TestUserProfile(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)
        # Create a user
        user = User(username='john', email='john@example.com')
        user.set_password('123456')
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_profile_page(self):
        # Log in
        self.client.post('/login', data=dict(
            username='john',
            password='123456'
        ), follow_redirects=True)
        # Visit profile page
        response = self.client.get('/user/john')
        self.assertEqual(response.status_code, 200)
        self.assertIn('john', response.get_data(as_text=True))
