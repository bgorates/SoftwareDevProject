from fastapi import FastAPI
from database import engine, Base
from models import *

app = FastAPI()  #create an instance of the FastAPI application

Base.metadata.create_all(bind=engine)

@app.get("/")

def read_root():
    return {"message": "Scheduler API is running"}




