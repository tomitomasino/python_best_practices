"""
This module contains tests for the FastAPI endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.main import app
from src.core.database import Base, get_db

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite://"

@pytest.fixture(name="database")
def fixture_db():
    """Create test database"""
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )
    
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    
    def override_get_db():
        try:
            test_db = TestingSessionLocal()
            yield test_db
        finally:
            test_db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield
    
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()

@pytest.fixture(name="client")
def fixture_client(database):  # pylint: disable=unused-argument
    """Create test client"""
    with TestClient(app) as client:
        yield client

def test_read_root(client):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_health_check_success(client):
    """Test health check endpoint when database is connected"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "database": "connected"}

def test_health_check_database_failure(client, monkeypatch):
    """Test health check endpoint when database connection fails"""
    def mock_execute(*args, **kwargs):
        raise OperationalError("statement", {}, "Database connection error")
    
    monkeypatch.setattr("sqlalchemy.orm.Session.execute", mock_execute)
    
    response = client.get("/health")
    assert response.status_code == 500
    assert "Database connection failed" in response.json()["detail"]

def test_invalid_endpoint(client):
    """Test accessing an invalid endpoint"""
    response = client.get("/nonexistent")
    assert response.status_code == 404
