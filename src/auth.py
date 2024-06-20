from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from src.database import User, db
from src.constants.http_status_codes import (HTTP_400_BAD_REQUEST,
                                             HTTP_409_CONFLICT,
                                             HTTP_201_CREATED,
                                             HTTP_401_UNAUTHORIZED,
                                             HTTP_200_OK)
import validators
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


@auth.post('/register')
@swag_from('./docs/auth/register.yaml')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if len(password) < 6:
        return jsonify({'error': "Password is too short"}), HTTP_400_BAD_REQUEST

    if len(username) < 3:
        return jsonify({'error': 'Username is too short'}), HTTP_400_BAD_REQUEST

    if not username.isalnum() or ' ' in username:
        return jsonify({'error': 'Username should be alphanumeric, also no spaces'}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({'error': 'Email is not valid'}), HTTP_400_BAD_REQUEST

    if User.query.filter_by(username=username).first() is not None:
        return jsonify({'error': 'Username is already taken'}), HTTP_409_CONFLICT

    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': 'Email is already taken'}), HTTP_409_CONFLICT

    hashed_password = generate_password_hash(password)
    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()
    return jsonify({
        'message': "User created",
        'user': {
            'username': username, "email": email
        }

    }), HTTP_201_CREATED


@auth.post('/login')
@swag_from('./docs/auth/login.yaml')
def login():
    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(email=email).first()
    if user is not None:
        if check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            return jsonify({
                'user': {
                    'refresh': refresh_token,
                    'access': access_token
                }

            }), HTTP_200_OK

    return jsonify({'error': 'Wrong credentials'}), HTTP_401_UNAUTHORIZED


@auth.get('/me')
@jwt_required()
def profile():
    user_id = get_jwt_identity()

    user = User.query.filter_by(id=user_id).first()
    return jsonify({
        'username': user.username,
        'email': user.email
    }), HTTP_200_OK


@auth.post('/token/refresh')
@jwt_required(refresh=True)
def refresh_user_token():
    user_id = get_jwt_identity()
    access_token = create_access_token(identity=user_id)

    return jsonify({
        'access': access_token
    }), HTTP_200_OK
