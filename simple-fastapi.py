## run command
# uvicorn simple-fastapi:app --host 0.0.0.0 --port 8080

from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

# Create a FastAPI app
app = FastAPI()

# Define the input schema for the endpoint
class Input(BaseModel):
    x1: float
    x2: float
    x3: float
    x4: float

@app.get("/time")
def get_time():
    return datetime.now()

@app.post("/echo")
def echo(input: Input):
    return {input.x1, input.x2, input.x3, input.x4}
