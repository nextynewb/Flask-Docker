# Flask CRUD API with MongoDB

A Flask application with full CRUD (Create, Read, Update, Delete) functionality using MongoDB as the database, all containerized with Docker.

## Setup

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Option 1: Run with Python (Local)

1. Run the Flask app:
```bash
python app.py
```

2. Open your browser and navigate to:
   - `http://localhost:9696/` - API documentation
   - `http://localhost:9696/health` - Health check
   - `http://localhost:9696/users` - CRUD operations for users

### Option 2: Run with Docker

1. Build and run with Docker Compose (recommended):
```bash
docker-compose up --build
```

2. Or build and run with Docker directly:
```bash
# Build the image
docker build -t flask-hello-world .

# Run the container
docker run -p 8080:5000 flask-hello-world
```

3. Test the API endpoints:
   - `http://localhost:8080/` - API documentation
   - `http://localhost:8080/health` - Health check
   - `http://localhost:8080/users` - CRUD operations for users

## API Endpoints

### User Management (CRUD)
- `GET /` - API documentation and available endpoints
- `GET /health` - Health check for app and database
- `GET /users` - Get all users
- `GET /users/<id>` - Get a specific user by ID
- `POST /users` - Create a new user (requires: name, email, optional: age)
- `PUT /users/<id>` - Update a user by ID
- `DELETE /users/<id>` - Delete a user by ID

### Testing the API
1. Use the provided test script: `python3 test_api.py`
2. Use the sample HTTP requests in `sample_requests.http`
3. Use curl commands or Postman

### Example curl commands:
```bash
# Create a user
curl -X POST http://localhost:8080/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John Doe","email":"john@example.com","age":30}'

# Get all users
curl http://localhost:8080/users

# Update a user (replace USER_ID with actual ID)
curl -X PUT http://localhost:8080/users/USER_ID \
  -H "Content-Type: application/json" \
  -d '{"name":"John Updated","age":31}'

# Delete a user (replace USER_ID with actual ID)
curl -X DELETE http://localhost:8080/users/USER_ID
```

The app runs in debug mode on `0.0.0.0:9696` by default. 