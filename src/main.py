'''
This module contains the main application code.
'''
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from src.core.database import Base, engine, get_db

async def startup():
    Base.metadata.create_all(bind=engine)

app = FastAPI(on_startup=[startup])

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def health_check(db=Depends(get_db)):
    try:
        db.execute(text("SELECT 1")).scalar()
        return {"status": "healthy", "database": "connected"}
    except SQLAlchemyError as exc:
        raise HTTPException(status_code=500, detail="Database connection failed") from exc
