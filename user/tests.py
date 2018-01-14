from app import create_app as create_app_base
from flask import jsonify
from mongoengine.connection import _get_db
import unittest
import json

from user.models import User


class UserTest(unittest.TestCase):
    def create_app(self):
        self.db_name = "meet-n-eat-test"
        return create_app_base(
            TESTING=True,
            MONGODB_DB=self.db_name
        )

    def setUp(self):
        self.app_factory = self.create_app()
        self.app = self.app_factory.test_client()
        user = User(
            username="whiskey-JACK",
            email="sarge@malazan.com",
            first_name="Whiskey",
            last_name="Jack",
            password="bridge-burner",
            bio="first in last out"
        )
        user.save()

    def test_signup_user_success(self):
        # User signup
        rv = self.app.post(
            '/api/v1/user/signup',
            content_type='application/json',
            data=json.dumps({
                "username": "surly",
                "password": "surly-1234",
                "email": "surly@email.com",
                "first_name": "Surly",
                "last_name": "Jane",
                "bio": "who in the world am I?"
            }))
        assert User.objects.filter(username="surly").count() == 1

    def test_signup_user_error_duplicate_username(self):
        res = self.app.post(
            '/api/v1/user/signup',
            content_type='application/json',
            data=json.dumps({
                "username": "whiskey-JACK",
                "password": "surly-1234",
                "email": "surly@email.com",
                "first_name": "Surly",
                "last_name": "Jane",
                "bio": "who in the world am I?"
            }))
        assert res.status_code == 409
        assert json.loads(res.data)["message"] == "username already exists"

    def tearDown(self):
        db = _get_db()
        db.connection.drop_database(db)
