import os
from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings
from pathlib import Path
import yaml

class Settings(BaseSettings):
    """Application settings loaded from environment variables and business parameters"""
    # Environment variables for infrastructure
    APP_NAME: str = "IKEA API"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DATABASE_URL: str = "sqlite:///./dev.db"
    DATABASE_POOL_SIZE: int = 5
    DATABASE_POOL_TIMEOUT: int = 30
    MAINTENANCE_MODE: bool = False
    DEPLOYMENT_ENABLED: bool = True
    
    # Feature flags
    FEATURE_NEW_UI: bool = False
    FEATURE_BETA_API: bool = False
    
    # Business parameters from YAML
    _business_params: dict = {}
    
    def load_business_params(self):
        """Load business parameters for current environment"""
        config_dir = Path(__file__).parent.parent.parent / "business_params"
        params_file = config_dir / f"{self.ENVIRONMENT}.yaml"
        
        if params_file.exists():
            with open(params_file, "r") as f:
                self._business_params = yaml.safe_load(f)
    
    def get_business_param(self, path: str, default=None):
        """Get business parameter by dot-notation path"""
        if not self._business_params:
            self.load_business_params()
            
        keys = path.split('.')
        value = self._business_params
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
            else:
                return default
        return value if value is not None else default

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    settings = Settings()
    settings.load_business_params()
    return settings
