from fastapi import FastAPI
from app.api import endpoints
import os
import uvicorn

app = FastAPI()
app.include_router(endpoints.router)
