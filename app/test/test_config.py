import unittest
import os
from flask import current_app
from app import create_app


class TestDevelopmentConfig(unittest.TestCase):
    def test_app_is_development(self):
        app = create_app("development")
        self.assertTrue(app.config['DEBUG'] is False)
        self.assertFalse(current_app is None)
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] ==
                        "postgresql://localhost/yummy_api")


class TestTestingConfig(unittest.TestCase):
    def test_app_is_testing(self):
        app = create_app("testing")
        self.assertTrue(app.config['DEBUG'])
        self.assertTrue(app.config['SQLALCHEMY_DATABASE_URI'] ==
                        "postgresql://localhost/test_db")


class TestProductionConfig(unittest.TestCase):
    def test_app_is_production(self):
        app = create_app("production")
        self.assertTrue(app.config['DEBUG'] is False)
