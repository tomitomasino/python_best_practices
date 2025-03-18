"""
This module contains tests for the FastAPI endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from decimal import Decimal

from src.main import app
from src.core.database import Base, get_db
from src.core.config import Settings
from src.core.business import calculate_discount, validate_order

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
    print(app)
    client = TestClient(app)
    return client

@pytest.fixture
def test_settings():
    """Override settings for testing with development parameters"""
    settings = Settings(
        ENVIRONMENT="development",
        DATABASE_URL="sqlite://",
        DATABASE_POOL_SIZE=1
    )
    settings.load_business_params()
    return settings

@pytest.fixture(autouse=True)
def override_settings(monkeypatch, test_settings):
    """Apply test settings"""
    monkeypatch.setattr("src.core.config.get_settings", lambda: test_settings)

def test_read_root(client):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}

def test_health_check_success(client):
    """Test health check endpoint when database is connected"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "environment": "test",
        "version": Settings().APP_VERSION
    }

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

def test_maintenance_mode(client, test_settings):
    """Test endpoints when maintenance mode is enabled"""
    test_settings.MAINTENANCE_MODE = True
    
    # Health check should still work
    health_response = client.get("/health")
    assert health_response.status_code == 200
    
    # Other endpoints should return 503
    root_response = client.get("/")
    assert root_response.status_code == 503
    assert root_response.json()["detail"] == "System is under maintenance"

def test_disabled_environment(client, test_settings):
    """Test endpoints when environment is disabled"""
    test_settings.DEPLOYMENT_ENABLED = False
    
    # All endpoints including health check should return 503
    for endpoint in ["/", "/health"]:
        response = client.get(endpoint)
        assert response.status_code == 503
        assert response.json()["detail"] == "This environment is currently disabled"

def test_business_parameters(test_settings):
    """Test loading business parameters"""
    # Business parameters are loaded automatically
    assert test_settings.get_business_param("pricing.minimum_order") == 50
    assert test_settings.get_business_param("inventory.low_stock_threshold") == 10
    assert test_settings.get_business_param("notifications.shipping_updates") is True
    
    # Test nested lists
    discount_tiers = test_settings.get_business_param("pricing.discount_tiers")
    assert len(discount_tiers) == 2
    assert discount_tiers[0]["threshold"] == 100
    
    # Test default value for non-existent parameter
    assert test_settings.get_business_param("nonexistent.path", default="default") == "default"

def test_environment_specific_parameters(test_settings):
    """Test that development environment has specific parameters"""
    assert test_settings.get_business_param("pricing.minimum_order") == 20  # Development value
    assert test_settings.get_business_param("inventory.max_items_per_order") == 50  # Development value
    
    # Switch to production parameters
    test_settings.ENVIRONMENT = "production"
    test_settings.load_business_params()
    
    assert test_settings.get_business_param("pricing.minimum_order") == 50  # Production value
    assert test_settings.get_business_param("inventory.max_items_per_order") == 20  # Production value

def test_discount_calculation(test_settings):
    """Test discount calculation using development parameters"""
    assert calculate_discount(Decimal('40')) == Decimal('0')
    assert calculate_discount(Decimal('60')) == Decimal('3')   # 5% of 60 in development
    assert calculate_discount(Decimal('250')) == Decimal('25') # 10% of 250 in development

def test_order_validation(test_settings):
    """Test order validation using business parameters"""
    valid_order = {
        "items": [{"quantity": 2}, {"quantity": 3}],
        "total": Decimal('100')
    }
    assert validate_order(valid_order["items"], valid_order["total"]) is True
    
    invalid_order = {
        "items": [{"quantity": 25}],  # Exceeds max_items_per_order
        "total": Decimal('40')  # Below minimum_order
    }
    assert validate_order(invalid_order["items"], invalid_order["total"]) is False
