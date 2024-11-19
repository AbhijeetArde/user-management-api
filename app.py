import uuid
import boto3
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_inputs import Inputs
from flask_inputs.validators import JsonSchema
from datetime import datetime

# Initialize the Flask application
app = Flask(__name__)
api = Api(app)

# DynamoDB setup
dynamodb = boto3.resource('dynamodb', region_name='us-west-2')  # Ensure your AWS credentials are set up
users_table = dynamodb.Table('UsersTable')  # DynamoDB table name

# Input validation schema
user_schema = {
    "type": "object",
    "properties": {
        "lastname": {"type": "string"},
        "dob": {"type": "string", "format": "date"},
        "address": {"type": "string"},
        "gender": {"type": "string"},
        "email": {"type": "string", "format": "email"},
        "phone_number": {"type": "string", "pattern": "^[0-9]{10}$"}
    },
    "required": ["lastname", "dob", "email", "phone_number"]
}

# Input validation using Flask-Inputs
class UserInputs(Inputs):
    json = [JsonSchema(schema=user_schema)]

# Create a new user
class UserCreate(Resource):
    def post(self):
        data = request.get_json()
        inputs = UserInputs(request)
        if not inputs.validate():
            return {"message": "Invalid input data"}, 400

        try:
            user = {
                'user_id': str(uuid.uuid4()),
                'lastname': data['lastname'],
                'dob': data['dob'],
                'address': data.get('address', ''),
                'gender': data.get('gender', ''),
                'email': data['email'],
                'phone_number': data['phone_number']
            }
            users_table.put_item(Item=user)
            return {"message": "User created", "user_id": user['user_id']}, 201
        except Exception as e:
            return {"message": str(e)}, 500

# Get user by ID
class UserRetrieve(Resource):
    def get(self, user_id):
        try:
            response = users_table.get_item(Key={'user_id': user_id})
            if 'Item' not in response:
                return {"message": "User not found"}, 404
            return jsonify(response['Item'])
        except Exception as e:
            return {"message": str(e)}, 500

# Update user by ID
class UserUpdate(Resource):
    def put(self, user_id):
        data = request.get_json()
        inputs = UserInputs(request)
        if not inputs.validate():
            return {"message": "Invalid input data"}, 400

        try:
            response = users_table.get_item(Key={'user_id': user_id})
            if 'Item' not in response:
                return {"message": "User not found"}, 404

            updated_user = response['Item']
            updated_user.update(data)

            users_table.put_item(Item=updated_user)
            return {"message": "User updated"}, 200
        except Exception as e:
            return {"message": str(e)}, 500

# Delete user by ID
class UserDelete(Resource):
    def delete(self, user_id):
        try:
            response = users_table.delete_item(Key={'user_id': user_id})
            if response.get('DeletedItem', None) is None:
                return {"message": "User not found"}, 404
            return {"message": "User deleted"}, 200
        except Exception as e:
            return {"message": str(e)}, 500

# Add the resources (endpoints) to the API
api.add_resource(UserCreate, '/users')
api.add_resource(UserRetrieve, '/users/<string:user_id>')
api.add_resource(UserUpdate, '/users/<string:user_id>')
api.add_resource(UserDelete, '/users/<string:user_id>')

if __name__ == '__main__':
    app.run(debug=True)
