'''
This module contains the main application code.
'''

from fastapi import FastAPI
from src.core.database import Base, engine

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
