from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import os
from datetime import datetime

app = Flask(__name__)

# MongoDB connection
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://mongodb:27017/flask_crud_db')
client = MongoClient(MONGO_URI)
db = client.flask_crud_db
users_collection = db.users

# Convert MongoDB documents to JSON
def serialize_user(user):
    if user:
        user['_id'] = str(user['_id'])
        return user
    return None

@app.route('/')
def home():
    return jsonify({
        "message": "Flask CRUD API with MongoDB",
        "endpoints": {
            "GET /": "This help message",
            "GET /users": "Get all users",
            "GET /users/<id>": "Get user by ID",
            "POST /users": "Create new user",
            "PUT /users/<id>": "Update user by ID",
            "DELETE /users/<id>": "Delete user by ID"
        }
    })

# CREATE - Add a new user
@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        
        if not data or 'name' not in data or 'email' not in data:
            return jsonify({"error": "Name and email are required"}), 400
        
        user = {
            "name": data['name'],
            "email": data['email'],
            "age": data.get('age', None),
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        result = users_collection.insert_one(user)
        user['_id'] = str(result.inserted_id)
        
        return jsonify({"message": "User created successfully", "user": serialize_user(user)}), 201
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# READ - Get all users
@app.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = list(users_collection.find())
        serialized_users = [serialize_user(user) for user in users]
        return jsonify({"users": serialized_users, "count": len(serialized_users)}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# READ - Get user by ID
@app.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        if not ObjectId.is_valid(user_id):
            return jsonify({"error": "Invalid user ID format"}), 400
        
        user = users_collection.find_one({"_id": ObjectId(user_id)})
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify({"user": serialize_user(user)}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# UPDATE - Update user by ID
@app.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    try:
        if not ObjectId.is_valid(user_id):
            return jsonify({"error": "Invalid user ID format"}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        # Build update document
        update_data = {}
        if 'name' in data:
            update_data['name'] = data['name']
        if 'email' in data:
            update_data['email'] = data['email']
        if 'age' in data:
            update_data['age'] = data['age']
        
        update_data['updated_at'] = datetime.utcnow()
        
        result = users_collection.update_one(
            {"_id": ObjectId(user_id)}, 
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            return jsonify({"error": "User not found"}), 404
        
        updated_user = users_collection.find_one({"_id": ObjectId(user_id)})
        return jsonify({"message": "User updated successfully", "user": serialize_user(updated_user)}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# DELETE - Delete user by ID
@app.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        if not ObjectId.is_valid(user_id):
            return jsonify({"error": "Invalid user ID format"}), 400
        
        result = users_collection.delete_one({"_id": ObjectId(user_id)})
        
        if result.deleted_count == 0:
            return jsonify({"error": "User not found"}), 404
        
        return jsonify({"message": "User deleted successfully"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Health check for MongoDB connection
@app.route('/health', methods=['GET'])
def health_check():
    try:
        # Test MongoDB connection
        client.admin.command('ping')
        return jsonify({
            "status": "healthy",
            "database": "connected",
            "timestamp": datetime.utcnow().isoformat()
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696) 