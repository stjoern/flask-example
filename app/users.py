"""Serve the api request."""

from config import client
from app import app
from bson.json_util import dumps
from flask import request, jsonify, Response
import json
import ast
import imp


# Import the helpers module
helper_module = imp.load_source('*', './app/helpers.py')

# Initialize database
dblist = client.database_names()
if "restapi" not in dblist:
    db = client["restapi"]
    
# Select the database
db = client.restapi
collist = db.collection_names()

collection = db["users"] if "users" not in collist else db.users
collection_groups = db["groups"] if "groups" not in collist else db.groups

groups = db.groups.find_one({'_id': 0})
if not groups:
    db.groups.insert({'_id':0, 'name':['User Group 1','User Group 2','User Group 3']})

@app.route("/")
def get_initial_response():
    """Welcome message for the API."""
    # Message to the user
    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'Welcome to the test.'
    }
    resp = jsonify(message)
    return resp


@app.route("/user/<new_user>", methods=['PUT'])
def create_user(new_user):
    """
       Function to create new users.
       """
    try:
        # Create new users
        try:
            body = ast.literal_eval(json.dumps(request.get_json()))
        except:
            return "", 400

        user_new = {'username': new_user}
        if collection.find({'username': new_user}).count() > 0:
            return "User {} already exists!".format(new_user)
        
        # check if group provided exists
        existing_groups = collection_groups.find_one({},{"_id":0})
        if set(body.get("groups",[])).issubset(existing_groups.get("name"))!=True or len(body.get("groups",[]))==0:
            return "{} cannot be inserted, the group is not correct.".format(body)
        body.update(user_new)
        record_created = collection.insert(body)

        if isinstance(record_created, list):
            return jsonify([str(v) for v in record_created]), 201
        else:
            # Return Id of the newly created item
            return jsonify(str(record_created)), 201
    except:
        # Error while trying to create the resource
        return "", 500


@app.route("/users/", methods=['GET'])
def fetch_users():
    """
       Function to fetch the users.
       """
    try:
        query_params = helper_module.parse_query_params(request.query_string)
        # Check if dictionary is not empty
        if query_params:

            query = {k: int(v) if isinstance(v, str) and v.isdigit() else v for k, v in query_params.items()}

            records_fetched = collection.find(query)
            if records_fetched.count() > 0:
                return dumps(records_fetched)
            else:
                # No records are found
                return "", 404

        # If dictionary is empty
        else:
            if collection.find().count > 0:
                return dumps(collection.find())
            else:
                return jsonify([])
    except:
        return "", 500

@app.route("/user/<user>", methods=['POST'])
def update_user(user):
    """
       Function to update the user.
    """
    try:
        # Update the user
        body = ast.literal_eval(json.dumps(request.get_json()))
        resp = jsonify(body)
        existing_groups = collection_groups.find_one({},{"_id":0})
        if set(body.get("groups",[])).issubset(existing_groups.get("name"))!=True or len(body.get("groups",[]))==0:
            return "{} cannot be inserted, the group is not correct.".format(body)
        item = collection.find_one({"username": user})
        body.update({'username': user})
        
        record_updated = collection.replace_one({"username": user}, body)
    except Exception as e:
        print(e)
        resp.status_code = 500
    return resp

@app.route("/user/<user>", methods=['DELETE'])
def remove_user(user):
    """
       Function to remove the user.
    """
    try:
        resp = Response(status=200)
        record_deleted = collection.delete_one({ "username" : user })
        if record_deleted.deleted_count > 0:
          resp.status_code = 204
          return resp
        else:
          # Entity not found, perhaps already deleted, return 404
          resp.status_code = 404
          return resp
    except:
      # Something went wrong server side, so return Internal Server Error.
      resp.status_code = 500
      return resp

@app.route("/groups/", methods=['GET'])
def fetch_groups():
    """
       Function to fetch the groups.
       """
    try:
        existing_groups = collection_groups.find_one({},{"_id":0})
        if existing_groups:
            return dumps(existing_groups.get('name',[]))

        # If dictionary is empty
        else:
           return jsonify([])
    except:
        return "", 500
