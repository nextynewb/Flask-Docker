#!/usr/bin/env python3
"""
Test script for Flask CRUD API with MongoDB
This script demonstrates all CRUD operations
"""

import requests
import json
import time

BASE_URL = "http://localhost:8080"

def test_api():
    print("🧪 Testing Flask CRUD API with MongoDB")
    print("=" * 50)
    
    # Test health check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health Status: {response.status_code}")
        print(f"Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return
    
    # Test home endpoint
    print("\n2️⃣ Testing Home Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"Home Status: {response.status_code}")
        print(f"Available endpoints: {response.json()['endpoints']}")
    except Exception as e:
        print(f"❌ Home endpoint failed: {e}")
    
    # CREATE - Add users
    print("\n3️⃣ Testing CREATE operations...")
    users_to_create = [
        {"name": "John Doe", "email": "john@example.com", "age": 30},
        {"name": "Jane Smith", "email": "jane@example.com", "age": 25},
        {"name": "Bob Johnson", "email": "bob@example.com"}  # No age
    ]
    
    created_users = []
    for user in users_to_create:
        try:
            response = requests.post(f"{BASE_URL}/users", json=user)
            print(f"Create Status: {response.status_code}")
            if response.status_code == 201:
                created_user = response.json()['user']
                created_users.append(created_user)
                print(f"✅ Created user: {created_user['name']} (ID: {created_user['_id']})")
            else:
                print(f"❌ Failed to create user: {response.json()}")
        except Exception as e:
            print(f"❌ Create failed: {e}")
    
    # READ - Get all users
    print("\n4️⃣ Testing READ operations (Get All)...")
    try:
        response = requests.get(f"{BASE_URL}/users")
        print(f"Get All Status: {response.status_code}")
        if response.status_code == 200:
            users_data = response.json()
            print(f"✅ Found {users_data['count']} users")
            for user in users_data['users']:
                print(f"   - {user['name']} ({user['email']}) - ID: {user['_id']}")
    except Exception as e:
        print(f"❌ Get all failed: {e}")
    
    # READ - Get specific user
    if created_users:
        print("\n5️⃣ Testing READ operations (Get by ID)...")
        test_user_id = created_users[0]['_id']
        try:
            response = requests.get(f"{BASE_URL}/users/{test_user_id}")
            print(f"Get By ID Status: {response.status_code}")
            if response.status_code == 200:
                user = response.json()['user']
                print(f"✅ Found user: {user['name']} ({user['email']})")
        except Exception as e:
            print(f"❌ Get by ID failed: {e}")
    
    # UPDATE - Update a user
    if created_users:
        print("\n6️⃣ Testing UPDATE operations...")
        test_user_id = created_users[0]['_id']
        update_data = {
            "name": "John Doe Updated",
            "age": 31
        }
        try:
            response = requests.put(f"{BASE_URL}/users/{test_user_id}", json=update_data)
            print(f"Update Status: {response.status_code}")
            if response.status_code == 200:
                updated_user = response.json()['user']
                print(f"✅ Updated user: {updated_user['name']} (Age: {updated_user['age']})")
        except Exception as e:
            print(f"❌ Update failed: {e}")
    
    # DELETE - Delete a user
    if len(created_users) > 1:
        print("\n7️⃣ Testing DELETE operations...")
        test_user_id = created_users[-1]['_id']  # Delete the last user
        try:
            response = requests.delete(f"{BASE_URL}/users/{test_user_id}")
            print(f"Delete Status: {response.status_code}")
            if response.status_code == 200:
                print(f"✅ Deleted user with ID: {test_user_id}")
        except Exception as e:
            print(f"❌ Delete failed: {e}")
    
    # Final check - Get all users again
    print("\n8️⃣ Final state check...")
    try:
        response = requests.get(f"{BASE_URL}/users")
        if response.status_code == 200:
            users_data = response.json()
            print(f"✅ Final count: {users_data['count']} users remaining")
    except Exception as e:
        print(f"❌ Final check failed: {e}")
    
    print("\n🎉 CRUD API testing completed!")

if __name__ == "__main__":
    print("Waiting 5 seconds for services to be ready...")
    time.sleep(5)
    test_api() 