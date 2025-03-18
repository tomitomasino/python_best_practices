from fastapi import Request, HTTPException
from src.core.config import config

async def deployment_validator(request: Request, call_next):
    """Middleware to control deployment status"""
    deployment_config = config["app"]["deployment"]
    
    if not deployment_config["enabled"]:
        raise HTTPException(
            status_code=503,
            detail="This environment is currently disabled"
        )
    
    if deployment_config["maintenance_mode"]:
        if request.url.path != "/health":  # Always allow health checks
            raise HTTPException(
                status_code=503,
                detail="System is under maintenance"
            )
    
    response = await call_next(request)
    return response
