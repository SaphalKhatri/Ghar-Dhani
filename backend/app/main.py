from fastapi import FastAPI
from app.database import engine,Base 

from app.models.landlord import Landlord



app=FastAPI(title="rental management",description="api for rental",version="1.0.0")

@app.get("/")
def health_check():
    return {"message":"ok"}
