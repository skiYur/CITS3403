import unittest
from flask import url_for
from app import create_app, db
from app.models import User

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_and_login(self):
        # Test registration
        response = self.client.post(url_for('auth.register'), data={
            'username': 'john',
            'email': 'john@example.com',
            'password': '123456',
            'password2': '123456'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Registration successful', response.get_data(as_text=True))

        # Test login
        response = self.client.post(url_for('auth.login'), data={
            'username': 'john',
            'password': '123456'
        }, follow_redirects=True)
        self.assertIn('Login successful', response.get_data(as_text=True))
