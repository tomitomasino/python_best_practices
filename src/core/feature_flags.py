from enum import Enum
from functools import lru_cache
import requests
from src.core.config import get_settings

class Feature(str, Enum):
    """Available feature flags"""
    NEW_UI = "FEATURE_NEW_UI"
    BETA_API = "FEATURE_BETA_API"

class FeatureFlags:
    """Feature flag manager"""
    def __init__(self):
        self.settings = get_settings()
        
    def is_enabled(self, feature: Feature) -> bool:
        """Check if feature is enabled"""
        return getattr(self.settings, feature.value, False)

@lru_cache()
def get_feature_flags() -> FeatureFlags:
    """Get cached feature flags instance"""
    return FeatureFlags()
