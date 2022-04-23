from __main__ import app, client
from flask import Flask, request, jsonify
import json
import ast
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import datetime
import hashlib


jwt = JWTManager(app) # initialize JWTManager
app.config['JWT_SECRET_KEY'] = 'Your_Secret_Key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1) # define the life span of the token


@app.route("/register", methods=["POST"])
def register():
	new_user = request.get_json() # store the json body request
	new_user["password"] = hashlib.sha256(new_user["password"].encode("utf-8")).hexdigest() # encrpt password
    # users_collection = client["twitter-user"]["record"]
	doc = client["twitter-user"]["record"].find_one({"username": new_user["username"]}) # check if user exist
	if not doc:
		client["twitter-user"]["record"].insert_one(new_user)
		return jsonify({'msg': 'User created successfully'}), 201
	else:
		return jsonify({'msg': 'Username already exists'}), 409

@app.route("/login", methods=["POST"])
def login():
	login_details = request.get_json() # store the json body request
	user_from_db = client["twitter-user"]["record"].find_one({'username': login_details['username']})  # search for user in database

	if user_from_db:
		encrpted_password = hashlib.sha256(login_details['password'].encode("utf-8")).hexdigest()
		if encrpted_password == user_from_db['password']:
			access_token = create_access_token(identity=user_from_db['username']) # create jwt token
			return jsonify(access_token=access_token), 200

	return jsonify({'msg': 'The username or password is incorrect'}), 401


@app.route("/profile", methods=["GET"])
@jwt_required()
def profile():
	current_user = get_jwt_identity() # Get the identity of the current user
	user_from_db = client["twitter-user"]["record"].find_one({'username' : current_user})
	if user_from_db:
		del user_from_db['_id'], user_from_db['password'] # delete data we don't want to return
		return jsonify({'profile' : user_from_db }), 200
	else:
		return jsonify({'msg': 'Profile not found'}), 404

@app.route('/', methods = ['GET'])
def retrieveAll():
    print("reached get method: /get")
    data = {}
    a=0
    result = client["mytestdb"]["collection1"].find()
    for i in result:
        data[a] = [str(item) for item in i.items()]
        a=a+1
    return jsonify(data)



@app.route('/postData', methods = ['POST'])
def postData():
    # currentCollection = mongo.db.col1
    data = request.data.decode()
    data = ast.literal_eval(data)
    print(type(data))
    inserted_id = client["mytestdb"]["collection1"].insert_one(data)
    return {"objectID":str(inserted_id)}




