from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import os, json

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['http://localhost:3001'], allow_methods=['*'], allow_headers=['*'])

@app.get("/")
def read_root():
    return {"message": "Hello from backend"}

@app.post("/api/test")
async def test_api(request: Request):
    data = await request.json()
    return {"received": data}

@app.get("/api/dbcheck")
def check_db():
    try:
        conn = sqlite3.connect("app.db")
        cur = conn.cursor()
        cur.execute("SELECT datetime('now')")
        time = cur.fetchone()[0]
        return {"db_time": time}
    except Exception as e:
        return {"error": str(e)}