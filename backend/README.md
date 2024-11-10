# ClusterMingle Backend 🚀

FastAPI-based backend service for ClusterMingle, featuring ML-powered group clustering and rotation algorithms.

## Directory Structure 📁

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── api/                    # API endpoints
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── core/                   # Core configurations
│   │   ├── __init__.py
│   │   └── config.py
│   ├── db/                     # Database models and config
│   │   ├── __init__.py
│   │   ├── database.py
│   │   └── models.py
│   ├── schemas/               # Pydantic models
│   │   ├── __init__.py
│   │   └── schemas.py
│   └── services/             # Business logic
│       ├── __init__.py
│       └── clustering.py
├── cleanup.py                # Cache cleanup utility
├── clustermingle.db         # SQLite database
└── requirements.txt         # Project dependencies
```

## Setup 🛠️

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

## API Endpoints 🔌

### Users
- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/` - List all users

### Groups
- `POST /api/v1/groups/create` - Create initial groups
- `POST /api/v1/groups/rotate` - Rotate existing groups

## Database 💾

The project uses SQLite for data storage. The database file is `clustermingle.db`.

## Cache Cleanup 🧹

To remove Python cache files and cleanup the project:

```bash
# Using the cleanup script
python cleanup.py

# Or using command line
find . -type d -name "__pycache__" -exec rm -r {} +
find . -type f -name "*.pyc" -delete
find . -type f -name ".DS_Store" -delete
```

## Testing API Endpoints 🧪

1. Create a user:
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/users/" \
-H "Content-Type: application/json" \
-d '{
    "first_name": "John",
    "last_name": "Doe",
    "industry": "Technology",
    "topics": "AI Machine Learning Cloud Computing",
    "fun_fact": "I love skydiving"
}'
```

2. Get all users:
```bash
curl "http://127.0.0.1:8000/api/v1/users/"
```

3. Create groups:
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/groups/create" \
-H "Content-Type: application/json" \
-d '{"n_clusters": 2}'
```

4. Rotate groups:
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/groups/rotate" \
-H "Content-Type: application/json" \
-d '{
    "previous_groups": [[1,2],[3,4]],
    "n_clusters": 2
}'
```

## Interactive API Documentation 📚

FastAPI provides automatic interactive API documentation:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Features ✨

- FastAPI for high-performance API
- SQLite database for simple data storage
- ML-powered clustering for group creation
- Smart group rotation algorithm
- Automatic API documentation
- Type checking with Pydantic
- Comprehensive error handling
- Cache cleanup utilities

## Development 🔧

1. API modifications should be made in `app/api/routes.py`
2. Database models are in `app/db/models.py`
3. Data validation schemas are in `app/schemas/schemas.py`
4. Clustering logic is in `app/services/clustering.py`

## Notes 📝

- The clustering algorithm uses TF-IDF and K-means for group creation
- Group rotation ensures minimal repeat interactions
- SQLite is used for simplicity, suitable for <150 users
- API includes comprehensive error handling and validation
- All endpoints return JSON responses