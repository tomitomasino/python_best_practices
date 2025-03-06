# MODEL REPOSITORY

## Repo configuration

- feature branch is deleted on PR merge
- merge to main with PR and 1 revirewer

## Run test

```bash
pytest tests/test_data_exporter.py -v
```

## Run pylint

```bash
pylint src/test.py    
```



## API app project structure - to consider
```
├── app/
│   ├── api/                    # API routes
│   │   ├── __init__.py
│   │   ├── v1/                # API version 1
│   │   │   ├── __init__.py
│   │   │   ├── endpoints/     # API endpoint modules
│   │   │   └── dependencies/  # Endpoint dependencies
│   ├── core/                  # Core application code
│   │   ├── __init__.py
│   │   ├── config.py         # Configuration management
│   │   ├── security.py       # Security utilities
│   │   └── errors.py         # Custom exceptions
│   ├── db/                   # Database related code
│   │   ├── __init__.py
│   │   ├── session.py       # Database session management
│   │   └── base.py         # Base DB class
│   ├── models/             # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── user.py        # Example model
│   ├── schemas/           # Pydantic models for request/response
│   │   ├── __init__.py
│   │   └── user.py       # Example schema
│   ├── services/         # Business logic
│   │   ├── __init__.py
│   │   └── user.py      # Example service
│   └── utils/           # Utility functions