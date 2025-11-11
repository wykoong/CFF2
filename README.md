# Customer Feedback Portal (minimal)

This project implements a small Flask-based Customer Feedback Portal.
The idea of this Customer Feedback Portal is evaluate and experience the use of Specification Driven Development method for Vibe Coding.



## Quickstart (development)

1. Create venv and install:
   ```cmd
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. Apply migrations:
   ```cmd
   python scripts/run_migrations.py
   ```

3. Run (development):
   ```cmd
   set FLASK_APP=src.app:create_app
   set FLASK_ENV=development
   flask run --port 5000
   ```

4. Open in browser:
   ```
   http://127.0.0.1:5000/api/feedback
   ```

## Testing

### Run all tests
```cmd
pytest -v
```

### Run tests with logging output
```cmd
pytest -v -o log_cli=true -o log_cli_level=DEBUG
```

### Run specific test file
```cmd
pytest tests/test_models.py -v
pytest tests/test_feedback_endpoints.py -v
pytest tests/test_dao.py -v
pytest tests/test_validation.py -v
```

### Run specific test function
```cmd
pytest tests/test_feedback_endpoints.py::TestFeedbackEndpoints::test_post_valid_feedback -v
```

### Generate coverage report
```cmd
pip install pytest-cov
pytest --cov=src --cov-report=html --cov-report=term
```
Then open `htmlcov/index.html` in browser to view detailed coverage.

### Test structure
Tests are organized by module:
- `test_models.py` - Feedback model tests
- `test_feedback_endpoints.py` - API endpoint tests (GET/POST, validation, edge cases)
- `test_dao.py` - Database access tests
- `test_validation.py` - Email validation tests
- `conftest.py` - Shared fixtures (app, client, db)
- `utils.py` - Test utility functions

### Quick test commands
```cmd
# Run with short traceback
pytest -v --tb=short

# Run with detailed output and disable capture
pytest -v -s

# Run only failed tests from last run
pytest -v --lf

# Run tests matching a pattern
pytest -v -k "valid_feedback"

# Run tests with markers (if configured)
pytest -v -m "integration"
```

## Database

See `.specify/db/migrations` for DB schema.

## Project Structure
```
CFF2/
├── src/
│   ├── app.py              # Flask app factory
│   ├── dao.py              # Database access
│   ├── models.py           # Data models
│   └── api/
│       └── feedback.py     # Feedback endpoints
├── tests/
│   ├── conftest.py         # Shared fixtures
│   ├── test_models.py
│   ├── test_feedback_endpoints.py
│   ├── test_dao.py
│   ├── test_validation.py
│   └── utils.py
├── templates/
│   └── public/
│       └── feedback.html   # Public feedback form
├── .specify/
│   └── db/
│       └── migrations/
│           └── 001_create_feedback_table.sql
└── README.md
```

## Development Notes

- Tests use an in-memory SQLite database for speed
- Each test is isolated and cleans up after itself
- Logging is configured at DEBUG level in tests for diagnostics
- Template folder is explicitly configured to support tests and production

## Endpoints

- `GET /` - Redirect to feedback form
- `GET /api/feedback` - Public feedback form
- `POST /api/feedback` - Submit feedback
- `GET /health` - Health check endpoint