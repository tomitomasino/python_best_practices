'''
This module contains the main application code.
'''
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from src.core.database import Base, engine, get_db
from src.core.config import config
from src.core.middleware import deployment_validator

async def startup():
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=config["app"]["name"],
    debug=config["api"]["debug"],
    on_startup=[startup]
)

app.middleware("http")(deployment_validator)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def health_check(db=Depends(get_db)):
    try:
        db.execute(text("SELECT 1")).scalar()
        return {
            "status": "healthy",
            "database": "connected",
            "environment": config["app"]["environment"],
            "version": config["app"]["version"]
        }
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=500, detail="Database connection failed") from exc
