from flask import Flask, request, jsonify, current_app
from flask_pymongo import PyMongo, MongoClient
import uuid
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask.views import MethodView
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, DecodeError
from flask_smorest import Blueprint, abort
from functools import wraps
from bson.objectid import ObjectId
from db import mongo 



blp = Blueprint("User", __name__, description="operation on user")






@blp.route('/login', methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']

    # Verify email and password
    user = mongo.db.users.find_one({'email': email})
    if not user or not check_password_hash(user["password"], password):
        return jsonify({'error': 'Invalid email or password'}), 401

    exp = datetime.utcnow() + timedelta(minutes=480)
    token = jwt.encode({"email": email, "exp": exp}, current_app.config["SECRET_KEY"])
    return jsonify({'token': token }), 200





@blp.route('/signin', methods=['POST'])
def signin():
    email = request.json['email']
    password = request.json['password']
    user = mongo.db.users.find_one({'email': email})
    if user:
        return jsonify({'error': 'email already used'}), 401
    hashed_password = generate_password_hash(password)
    mongo.db.users.insert_one({"email": email, "password": hashed_password})
    

    exp = datetime.utcnow() + timedelta(minutes=480)
    token = jwt.encode({"email": email, "exp": exp}, current_app.config['SECRET_KEY'])
    return jsonify({'user created here is your token': token}), 200



def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], verify=True, algorithms=['HS256'])
        except ExpiredSignatureError:
            return jsonify({'message': 'Token expired!'}), 401
        except jwt.exceptions.InvalidSignatureError:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)

    return decorated


@blp.route('/delete_user', methods=['DELETE'])
@token_required
def deleteuser():
    email = request.json['email']
    password = request.json['password']
    user = mongo.db.users.find_one({'email': email})
    if not user or not check_password_hash(user["password"], password):
        return jsonify({'error': 'Invalid email or password'}), 401  
    if user:
        mongo.db.users.delete_one({"email": email})
        return jsonify({"message":"user deleted successfully!" })
    else:
        return jsonify({"message": "user not found"}), 404


