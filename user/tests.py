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
            SECRET_KEY="i am sec",
            MONGODB_DB=self.db_name)

    def setUp(self):
        self.app_factory = self.create_app()
        self.app = self.app_factory.test_client()
        self.user_data = {
            "username": "surly",
            "password": "surly-1234",
            "email": "surly@email.com",
            "first_name": "Surly",
            "last_name": "Jane",
            "bio": "who in the world am I?"
        }
        user = User(
            username="whiskey-JACK",
            email="sarge@malazan.com",
            first_name="Whiskey",
            last_name="Jack",
            password="bridge-burner",
            bio="first in last out"
        )
        user.save()


    """
        @TEST
       /api/v1/user/signup
            - Test for signup success
            - Test for error on invalid data input
            - Test for unique fields violation
            - Test form required fields
    """
    def test_signup_user_success(self):
        # User signup
        res = self.app.post(
            '/api/v1/user/signup',
            content_type='application/json',
            data=json.dumps(self.user_data))
        assert res.status_code == 201
        assert User.objects.filter(username="surly").count() == 1

    def test_signup_user_error_invalid_data(self):
        invalid_fields = {'email': 'aabc.som', 'password': 'abc'}
        for field in invalid_fields:
            data = dict(self.user_data)
            data[field] = invalid_fields[field]
            res = self.app.post(
                '/api/v1/user/signup',
                content_type='application/json',
                data=json.dumps(data))
            assert res.status_code == 422
            if field == "password":
                assert json.loads(res.data)["message"] == "password must be at least 8 characters long"
            else:
                assert json.loads(res.data)["message"] == "email is not valid"

    def test_signup_user_error_none_unique_fields(self):
        unique_fields = {"username": "whiskey-JACK", "email": "sarge@malazan.com"}
        for field in unique_fields:
            data = dict(self.user_data)
            data[field] = unique_fields[field]
            res = self.app.post(
                '/api/v1/user/signup',
                content_type='application/json',
                data=json.dumps(data))
            assert res.status_code == 409
            assert json.loads(res.data)["message"] == "%s already exists" % field

    def test_signup_user_error_empty_required_fields(self):
        required_fields = ['email', 'first_name', 'last_name', 'username', 'password']
        for field in required_fields:
            data = dict(self.user_data)
            data.pop(field, None)
            res = self.app.post('/api/v1/user/signup', content_type='application/json', data=json.dumps(data))
            assert res.status_code == 422
            assert json.loads(res.data)["message"] == "%s is required" % field

    """
    @TEST
       /api/v1/user/login
            - Test for login success
            - Test for error on invalid credentials
            - Test for required fields
    """
    # Test for login success
    def test_login_user_success(self):
        self.app.post(
            '/api/v1/user/signup',
            content_type='application/json',
            data=json.dumps(self.user_data))
        res = self.app.post(
            '/api/v1/user/login',
            content_type='application/json',
            data=json.dumps(self.user_data))
        assert res.status_code == 200
        assert json.loads(res.data)["access_token"]

    # Test for error on invalid credentials
    def test_login_user_error_invalid_credentials(self):
        self.app.post(
            '/api/v1/user/signup',
            content_type='application/json',
            data=json.dumps(self.user_data))

        fields = {"email": "a@g.com",  "password": "abc"}
        for field in fields:
            data = dict(self.user_data)
            data[field] = fields[field]

            res = self.app.post(
                '/api/v1/user/login',
                content_type='application/json',
                data=json.dumps(data))
            assert res.status_code == 401

    # Test for required fields
    def test_login_user_error_empty_required_field(self):
        required_fields = ['email', 'password']
        for field in required_fields:
            data = dict(self.user_data)
            data.pop(field, None)
            res = self.app.post('/api/v1/user/login', content_type='application/json', data=json.dumps(data))
            assert res.status_code == 422
            assert json.loads(res.data)["message"] == "%s is required" % field

    def tearDown(self):
        db = _get_db()
        db.connection.drop_database(db)
