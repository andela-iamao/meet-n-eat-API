import json
import bcrypt
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

user_app = Blueprint('user_app', __name__)


@user_app.route('/login',  methods=["POST"])
def login():
    from user.models import User
    from user.util import Validator

    req_body = json.loads(request.data)
    try:
        validate = Validator(req_body)
        validate.is_present('email')
        validate.is_present('password')
        print 'both are present'
        validate.is_email()
        user = User.objects.filter(email=req_body["email"]).first()

        if user:
            validate.is_password(user.password)

            return jsonify({
                "user": user.serialize,
                "access_token": create_access_token(identity=str(user.id))
            })

    except Exception as e:
        return jsonify({"message": e[0]}), e[1]


@user_app.route('/signup', methods=["POST"])
def signup():
    from user.models import User
    from user.util import Validator

    req_body = json.loads(request.data)
    try:
        Validator(req_body).is_all_valid()
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(req_body["password"], salt)
        user = User(
            bio=req_body["bio"],
            email=req_body["email"],
            password=hashed_password,
            username=req_body["username"],
            last_name=req_body["last_name"],
            first_name=req_body["first_name"],
        )
        user.save()
        return jsonify({
            "status": 200,
            "payload": user.serialize
        }), 201
    except Exception as e:
        return jsonify({"message": e[0]}), e[1]

