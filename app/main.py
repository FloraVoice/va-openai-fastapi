from fastapi import FastAPI
from dotenv import load_dotenv

from app.routers import hello, ws


load_dotenv()

app = FastAPI()

app.include_router(hello.router)
app.include_router(ws.router)
