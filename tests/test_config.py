import unittest
from flask import current_app
from app import create_app

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.app = create_app('TestingConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
