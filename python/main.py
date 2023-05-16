import os
import logging
import pathlib
from fastapi import FastAPI, Form, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import json
import hashlib
import sqlite3

app = FastAPI()
logger = logging.getLogger("uvicorn")
logger.level = logging.INFO
images = pathlib.Path(__file__).parent.resolve() / "images"
data_base = pathlib.Path(__file__).parent.resolve() / "mercari.sqlite3"
origins = [ os.environ.get('FRONT_URL', 'http://localhost:9000') ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET","POST","PUT","DELETE"],
    allow_headers=["*"],
)

conn = sqlite3.connect(data_base)

# create the category table
def create_category_table(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS category (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    conn.commit()

create_category_table(conn)

# create the item table
def create_items_table(conn: sqlite3.Connection):
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category_id INTEGER,
                image_name TEXT NOT NULL,
                FOREIGN KEY(category_id) REFERENCES category(id)
            )
        """)
        conn.commit()
    except Exception as e:
        print(f"An error occurred: {e}")

conn = sqlite3.connect(data_base)

create_items_table(conn)


@app.get("/")
def root():
    return {"message": "Hello, world!"}

@app.post("/items")
def add_item(name: Optional[str] = Form(None), category: Optional[str] = Form(None), image: UploadFile = File(...)):
    # Open connection to database
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()

    # hash image using sha256
    imageContent = image.file.read()
    hashedImage = hashlib.sha256(imageContent).hexdigest()
    hashedImg = hashedImage + os.path.splitext(image.filename)[1]

    # Check if the category already exists
    cursor.execute("SELECT id FROM category WHERE name=?", (category,))
    category_id = cursor.fetchone()

    # If the category doesn't exist, add it
    if category_id is None:
        cursor.execute("INSERT INTO category (name) VALUES (?)", (category,))
        conn.commit()
        # Fetch the new category id
        cursor.execute("SELECT id FROM category WHERE name=?", (category,))
        category_id = cursor.fetchone()

    # Create a new item
    cursor.execute("""
        INSERT INTO items (name, category_id, image_name)
        VALUES (?, ?, ?)
    """, (name, category_id[0], hashedImg))

    # Commit and close connection
    conn.commit()
    conn.close()

    return {"message": f"item received: {name}"}




# Define a route for the "/items" URL with a GET method
@app.get("/items")
def read_items():
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT items.id, items.name, category.name, items.image_name
        FROM items
        INNER JOIN category ON items.category_id = category.id
    ''')
    item_results = cursor.fetchall()

    conn.close()
    return item_results



# Define an endpoint that handles ids
@app.get("/items/{item_id}")
def read_item(item_id: int):
    with open("items.json") as file:
        data = json.load(file)

    for item in data["items"]:
        if item["id"] == int(item_id):
            return item

    raise HTTPException(status_code=404, detail="Item not found")

@app.get("/image/{image_filename}")
async def get_image(image_filename):
    # Create image path
    image = images / image_filename

    if not image_filename.endswith(".jpg"):
        raise HTTPException(status_code=400, detail="Image path does not end with .jpg")

    if not image.exists():
        logger.debug(f"Image not found: {image}")
        image = images / "default.jpg"

    return FileResponse(image)

# search for items
@app.get("/search")
def search_item(keyword: str):
    conn = sqlite3.connect(data_base)
    cursor = conn.cursor()
    search_keyword = f"%{keyword}%"
    cursor.execute('''
        SELECT items.id, items.name, category.name, items.image_name
        FROM items
        INNER JOIN category ON items.category_id = category.id
        WHERE items.name LIKE ?
    ''', (search_keyword,))
    search_results = cursor.fetchall()

    conn.close()
    return search_results
