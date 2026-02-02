# DSEC AI Newsletter - Backend API

FastAPI backend for the DSEC AI Newsletter platform.

## Features

- **RESTful API** with FastAPI
- **Async SQLAlchemy** for database operations
- **SQLite** database (upgradeable to PostgreSQL)
- **Pydantic** schemas for validation
- **Auto-generated API docs** at `/docs`

## Setup

### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Create a `.env` file in the project root (parent directory) with:

```bash
# Database
DATABASE_URL=sqlite+aiosqlite:///./newsletter.db

# SMTP (from existing configuration)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
SENDER_NAME=DSEC AI Newsletter

# API
BASE_URL=http://localhost:8000
```

### 4. Run Migration (Optional)

Migrate existing JSON data to database:

```bash
python -m app.utils.migration
```

### 5. Start Server

```bash
uvicorn app.main:app --reload --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Articles
- `GET /api/v1/articles` - List articles (with pagination, filters)
- `GET /api/v1/articles/{id}` - Get article by ID
- `POST /api/v1/articles` - Create article
- `PUT /api/v1/articles/{id}` - Update article
- `DELETE /api/v1/articles/{id}` - Delete article

### Subscribers
- `GET /api/v1/subscribers` - List subscribers
- `GET /api/v1/subscribers/{id}` - Get subscriber by ID
- `POST /api/v1/subscribers` - Add subscriber
- `PUT /api/v1/subscribers/{id}` - Update subscriber
- `POST /api/v1/subscribers/{id}/unsubscribe` - Unsubscribe
- `DELETE /api/v1/subscribers/{id}` - Delete subscriber
- `POST /api/v1/subscribers/import` - Bulk import

## Database Models

- **Article** - Scraped articles with metadata
- **Subscriber** - Email subscribers
- **Newsletter** - Created newsletters
- **Template** - Reusable templates
- **NewsletterArticle** - Newsletter-Article junction
- **EmailSend** - Email send tracking
- **EmailOpen** - Open tracking (pixel)
- **LinkClick** - Click tracking (URL)

## Development

### Run Tests

```bash
pytest
```

### Database Migrations

Using Alembic for schema changes:

```bash
# Generate migration
alembic revision --autogenerate -m "Description"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

## Project Structure

```
backend/
├── app/
│   ├── models/          # SQLAlchemy models
│   ├── schemas/         # Pydantic schemas
│   ├── api/v1/          # API routes
│   ├── services/        # Business logic
│   ├── utils/           # Utilities (migration, etc.)
│   ├── config.py        # Configuration
│   ├── database.py      # Database setup
│   └── main.py          # FastAPI app
├── tests/
├── alembic/
└── requirements.txt
```
