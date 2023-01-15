from flask import request, make_response, current_app
from flask_pymongo import PyMongo
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask.json import jsonify
from db import mongo
from functools import wraps
import jwt
from resources.users import token_required
from bson.objectid import ObjectId




blp = Blueprint("Persons", __name__, description="operation on persons")




@blp.route("/add_person", methods=["POST"])
@token_required
def add_person():
   # Extract person data from request
    person = request.json
    person_id = mongo.db.persons.insert_one(person).inserted_id
    return jsonify({"message": "Person added successfully"}), 201




@blp.route("/get_person/<id>", methods=["GET"])
@token_required
def get_person(id):
    if not ObjectId.is_valid(id):
        return jsonify({"message": "Invalid id"}), 400
    person = mongo.db.persons.find_one({"_id": ObjectId(id)})
    if person:
        person["_id"] = str(person["_id"])
        return jsonify(person)
    else:
        return jsonify({"message": "Person not found"}), 404



@blp.route("/get_persons", methods=["GET"])
@token_required
def get_all_persons():
    persons = list(mongo.db.persons.find())
    if len(persons) == 0:
        return jsonify({"message": "No persons found"}), 404
    for person in persons:
        person["_id"] = str(person["_id"])
    return jsonify(persons)
 



@blp.route("/update_person/<id>", methods=["PUT"])
@token_required
def update_person(id):
    if not ObjectId.is_valid(id):
       return jsonify({"message": "Invalid id"}), 400
    person = mongo.db.persons.find_one({"_id": ObjectId(id)})
    if person:
        update_data = {}
        if 'name' in request.form:
            update_data["name"] = request.form.get("name")
        if 'id' in request.form:
            update_data["id"] = request.form.get("id")
        if 'birth_certificate' in request.form:
            update_data["birth_certificate"] = request.form.getlist("birth_certificate")
        if 'id_card' in request.form:
            update_data["id_card"] = request.form.getlist("id_card")
        if 'passeport' in request.form:
            update_data["passeport"] = request.form.getlist("passeport")
        if 'other_docs' in request.form:
            update_data["other_docs"] = request.form.getlist("other_docs")
        mongo.db.persons.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_data }
        )
        return jsonify({"message": "Person updated successfully!"}), 200
    else:
        return jsonify({"message": "Person not found"}), 404



@blp.route("/delete_person/<id>", methods=["DELETE"])
@token_required
def delete_person(id):
    if not ObjectId.is_valid(id):
        return jsonify({"message": "Invalid id"}), 400
    person = mongo.db.persons.find_one({"_id": ObjectId(id)})
    if person:
        mongo.db.persons.delete_one({"_id": ObjectId(id)})
        return jsonify({"message": "Person deleted successfully!" })
    else:
        return jsonify({"message": "Person not found"}), 404





