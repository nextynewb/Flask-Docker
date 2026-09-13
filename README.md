# Flask CRUD API with MongoDB

A modern Flask REST API with full CRUD (Create, Read, Update, Delete) functionality using MongoDB as the database, all containerized with Docker for easy deployment and development.

## 🚀 Features

- **Full CRUD Operations** - Create, Read, Update, Delete users
- **MongoDB Integration** - NoSQL database with proper error handling
- **Docker Containerization** - Both Flask app and MongoDB in containers
- **RESTful API Design** - Clean, intuitive endpoints
- **Health Monitoring** - Database connection health checks
- **Automated Testing** - Comprehensive test suite included
- **Error Handling** - Proper HTTP status codes and error messages
- **Data Validation** - Input validation and sanitization
- **Timestamp Tracking** - Created/updated timestamps for all records

## 📁 Project Structure

```
docker-class/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker image configuration
├── docker-compose.yml       # Multi-container Docker setup
├── .dockerignore           # Docker build exclusions
├── .gitignore              # Git exclusions
├── README.md               # This file
├── test_api.py             # Automated testing script
├── sample_requests.http    # Sample HTTP requests for manual testing
└── run-docker.sh           # Docker convenience script
```

## 🛠️ Prerequisites

- **Python 3.9+** (for local development)
- **Docker & Docker Desktop** (for containerized deployment)
- **Git** (for version control)

## ⚡ Quick Start

### Option 1: Docker Deployment (Recommended)

1. **Clone and navigate to the project:**
```bash
git clone <your-repo-url>
cd docker-class
```

2. **Start with Docker Compose:**
```bash
# Using Docker Compose V2 (recommended)
docker compose up --build

# Or if you have the older docker-compose installed
docker-compose up --build
```

3. **Access the API:**
   - API Documentation: http://localhost:8080/
   - Health Check: http://localhost:8080/health
   - Users API: http://localhost:8080/users

### Option 2: Local Development

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Start MongoDB** (choose one):
```bash
# Using Docker
docker run -d -p 27017:27017 --name mongodb mongo:7.0

# Or using local MongoDB installation
brew services start mongodb-community
```

3. **Run the Flask app:**
```bash
python app.py
```

4. **Access the API:**
   - API Documentation: http://localhost:9696/
   - Health Check: http://localhost:9696/health
   - Users API: http://localhost:9696/users

## 📡 API Endpoints

### Core Endpoints

| Method | Endpoint | Description | Request Body |
|--------|----------|-------------|--------------|
| `GET` | `/` | API documentation | None |
| `GET` | `/health` | Health check | None |
| `GET` | `/users` | Get all users | None |
| `GET` | `/users/<id>` | Get specific user | None |
| `POST` | `/users` | Create new user | `{"name": "string", "email": "string", "age": number}` |
| `PUT` | `/users/<id>` | Update user | `{"name": "string", "email": "string", "age": number}` |
| `DELETE` | `/users/<id>` | Delete user | None |

### User Data Schema

```json
{
  "_id": "ObjectId",
  "name": "string (required)",
  "email": "string (required)", 
  "age": "number (optional)",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

## 🧪 Testing the API

### 1. Automated Testing
```bash
# Run the comprehensive test suite
python3 test_api.py
```

### 2. Manual Testing with curl

```bash
# Create a user
curl -X POST http://localhost:8080/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice Smith","email":"alice@example.com","age":28}'

# Get all users
curl http://localhost:8080/users

# Get specific user (replace USER_ID with actual ID)
curl http://localhost:8080/users/USER_ID

# Update a user
curl -X PUT http://localhost:8080/users/USER_ID \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice Johnson","age":29}'

# Delete a user
curl -X DELETE http://localhost:8080/users/USER_ID

# Health check
curl http://localhost:8080/health
```

### 3. Using HTTP Client
Open `sample_requests.http` in VS Code with the REST Client extension, or import into Postman.

## 🐳 Docker Configuration

### Services

- **flask-app**: Flask API server (Port 8080 → 9696)
- **mongodb**: MongoDB database (Port 27017)

### Docker Commands

```bash
# Build and start all services
docker compose up --build

# Run in background
docker compose up -d --build

# View logs
docker compose logs

# Stop services
docker compose down

# Remove volumes (⚠️ deletes database data)
docker compose down -v

# Rebuild specific service
docker compose build flask-app
```

## 🔧 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `MONGO_URI` | `mongodb://mongodb:27017/flask_crud_db` | MongoDB connection string |
| `FLASK_ENV` | `development` | Flask environment |

## 🚨 Troubleshooting

### Common Issues

#### Port Conflicts
```bash
# Error: Port 27017 already in use
# Solution: Stop local MongoDB
brew services stop mongodb-community

# Or use different port in docker-compose.yml
ports:
  - "27018:27017"
```

#### Docker Issues
```bash
# Docker daemon not running
open -a Docker

# Permission issues
sudo chown -R $(whoami) /path/to/project

# Clean Docker environment
docker system prune -a
```

#### MongoDB Connection Issues
```bash
# Check MongoDB container status
docker compose logs mongodb

# Test connection
docker exec -it <mongodb-container> mongosh
```

### Health Check Responses

**Healthy:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-07-03T13:36:16.396451"
}
```

**Unhealthy:**
```json
{
  "status": "unhealthy", 
  "database": "disconnected",
  "error": "Connection refused",
  "timestamp": "2025-07-03T13:36:16.396451"
}
```

## 📊 Development

### Adding New Features

1. **Modify `app.py`** for new endpoints
2. **Update `requirements.txt`** for new dependencies  
3. **Add tests** to `test_api.py`
4. **Update API documentation** in this README

### Database Management

```bash
# Connect to MongoDB in Docker
docker exec -it <mongodb-container-name> mongosh

# View databases
show dbs

# Use project database
use flask_crud_db

# View collections
show collections

# Query users
db.users.find().pretty()
```

## 🔐 Security Notes

- Environment variables for sensitive data
- Input validation on all endpoints
- Proper error handling without exposing internals
- MongoDB connection authentication (add in production)

## 🚀 Deployment

### Production Considerations

1. **Environment Variables**: Use `.env` files or container orchestration secrets
2. **Database**: Use managed MongoDB service (MongoDB Atlas)
3. **Reverse Proxy**: Add Nginx for production
4. **SSL/TLS**: Configure HTTPS
5. **Monitoring**: Add logging and monitoring solutions

### Docker Production Build

```dockerfile
# Multi-stage build for production
FROM python:3.9-slim as production
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
EXPOSE 9696
CMD ["gunicorn", "--bind", "0.0.0.0:9696", "app:app"]
```

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

If you encounter any issues or have questions:

1. Check the troubleshooting section above
2. Review the Docker logs: `docker compose logs`
3. Test the health endpoint: `curl http://localhost:8080/health`
4. Open an issue in the repository

---

**Happy coding!** 🎉 