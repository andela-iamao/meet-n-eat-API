import json
import bcrypt
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required

user_app = Blueprint("user_app", __name__)


@user_app.route("/login",  methods=['POST'])
def login():
    from user.models import User
    from user.util import Validator

    req_body = json.loads(request.data)
    try:
        validate = Validator(req_body)
        validate.is_present("email", "password")
        validate.is_email()

        user = User.objects.filter(email=req_body['email']).first()

        if user:
            validate.is_password(user.password)

            return jsonify({
                'user': user.serialize,
                'access_token': create_access_token(identity=str(user.id))
            }), 200
        raise Exception("credentials do not match", 401)

    except Exception as e:
        return jsonify({'message': e[0]}), e[1]


@user_app.route("/signup", methods=['POST'])
def signup():
    from user.models import User
    from user.util import Validator

    req_body = json.loads(request.data)
    try:
        validate = Validator(req_body)
        validate.is_present("email", "password", "username", "first_name", "last_name")
        validate.is_all_valid()
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(req_body['password'], salt)
        user = User(
            bio=req_body['bio'],
            email=req_body['email'],
            password=hashed_password,
            username=req_body['username'],
            last_name=req_body['last_name'],
            first_name=req_body['first_name'],
        )
        user.save()
        return jsonify({
            'user': user.serialize,
            'access_token': create_access_token(identity=str(user.id))
        }), 201
    except Exception as e:
        return jsonify({'message': e[0]}), e[1]


@user_app.route("/", methods=['GET'])
# @jwt_required
def get_all():
    from user.models import User
    users = User.objects.filter().all()
    return jsonify({
        'data': [user.serialize for user in users],
        'metadata': {}
    })


@user_app.route("/<uid>", methods=["GET", "PUT", "DELETE"])
def user_profile(uid):
    from user.util import Validator
    try:
        user = Validator.user_exists(uid)
        if request.method == 'GET':
            return jsonify({'user': user.serialize}), 200

        elif request.method == 'PUT':
            return jsonify({}), 204

        elif request.method == 'DELETE':
            return jsonify({}), 204
    except Exception as e:
        return jsonify({'message': e[0]}), e[1]
