from flask import Flask
from flask_smorest import Api 
from flask_pymongo import PyMongo
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from db import mongo




app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisissecret'
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
mongo.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)


from resources.persons import blp as PersonsBlueprint
from resources.users import blp as UserBlueprint

app.register_blueprint(PersonsBlueprint)
app.register_blueprint(UserBlueprint)







