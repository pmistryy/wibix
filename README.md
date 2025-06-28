# Wibix Semantic Search FastAPI

A FastAPI application that provides semantic search capabilities using vector embeddings and PostgreSQL.

## Features

- CSV data upload and vectorization
- Semantic search by ID, name, or both
- Smart search with separate ID and name vectors
- Docker support
- PostgreSQL integration

## Setup

### Option 1: Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your database:**
   - Create a database and user
   - Copy `env.example` to `.env` and update with your connection details:
     ```
     DATABASE_URL=postgresql://user:password@localhost/dbname
     ```

3. **Create database tables:**
   ```bash
   python init_db.py
   ```

4. **Run the app:**
   ```bash
   uvicorn app.main:app --reload
   ```

### Option 2: Docker

1. **Configure your database connection:**
   ```bash
   # Copy and edit the environment file
   cp env.example .env
   # Edit .env with your database details
   ```

2. **Build and run with Docker:**
   ```bash
   docker compose up --build
   ```

## Database Configuration

The application supports various database connections:

### Local PostgreSQL
```
DATABASE_URL=postgresql://username:password@localhost:5432/database_name
```

### Remote PostgreSQL
```
DATABASE_URL=postgresql://username:password@your-server.com:5432/database_name
```

### Cloud Databases
- **AWS RDS**: `postgresql://username:password@your-rds-endpoint.amazonaws.com:5432/database_name`
- **Google Cloud SQL**: `postgresql://username:password@your-instance-ip:5432/database_name`
- **Azure Database**: `postgresql://username:password@your-server.database.windows.net:5432/database_name`

## Usage

### Upload CSV Data
```bash
curl -F "file=@sample_data.csv" http://localhost:8000/upload_csv/
```

### Search API
```bash
# Get best match
curl "http://localhost:8000/search/best/?query=Alice"

# Get multiple results
curl "http://localhost:8000/search/?query=engineer"
```

### API Endpoints
- `POST /upload_csv/` - Upload and vectorize CSV data
- `GET /search/` - Get multiple search results
- `GET /search/best/` - Get only the best match
- `GET /docs` - Interactive API documentation

## Project Structure

```
app/
  main.py              # FastAPI application
  api/endpoints.py     # API endpoints
  db/
    models.py          # Database models
    database.py        # Database connection
  services/
    vectorizer.py      # Text vectorization
    search.py          # Semantic search logic
  schemas/
    data.py            # Pydantic schemas
```

## Docker Commands

```bash
# Build and start
docker compose up --build

# Run in background
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f app
```

## Notes

- Uses Sentence Transformers for embeddings
- Stores vectors as pickled numpy arrays in PostgreSQL
- Uses cosine similarity for semantic search
- Supports both ID and name-based searches
- Automatically handles updates vs new entries 