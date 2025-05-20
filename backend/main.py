from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import os

app = FastAPI()

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL", "sql_app.db")

class Item(BaseModel):
    name: str
    description: str = None

@app.on_event("startup")
def startup():
    if not os.path.exists(DATABASE_URL):
        open(DATABASE_URL, "w").close()
    
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.post("/items/")
async def create_item(item: Item):
    print(f"Using database at: {DATABASE_URL}")  # デバッグ用出力
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    # テーブル存在確認
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='items'")
    print(f"Tables found: {cursor.fetchall()}")  # デバッグ用出力
    cursor.execute(
        "INSERT INTO items (name, description) VALUES (?, ?)",
        (item.name, item.description)
    )
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    return {"id": item_id, **item.dict()}

@app.get("/items/")
async def read_items():
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description FROM items")
    items = cursor.fetchall()
    conn.close()
    return {"items": [{"id": i[0], "name": i[1], "description": i[2]} for i in items]}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    conn = sqlite3.connect(DATABASE_URL)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description FROM items WHERE id=?", (item_id,))
    item = cursor.fetchone()
    conn.close()
    
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return {"id": item[0], "name": item[1], "description": item[2]}