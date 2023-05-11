import os
import logging
import pathlib
from fastapi import FastAPI, Form, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import json
import hashlib

app = FastAPI()
logger = logging.getLogger("uvicorn")
logger.level = logging.INFO
images = pathlib.Path(__file__).parent.resolve() / "images"
origins = [ os.environ.get('FRONT_URL', 'http://localhost:9000') ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["GET","POST","PUT","DELETE"],
    allow_headers=["*"],
)
item_id_num = 1  # Initialize the item ID counter

@app.get("/")
def root():
    return {"message": "Hello, world!"}

@app.post("/items")
def add_item(name: Optional[str] = Form(None), category: Optional[str] = Form(None), image: UploadFile = File(...)):
    # Load existing items from the file
    with open("items.json") as file:
        data = json.load(file)

    # Access the global item ID counter
    global item_id_num

    # hash image using sha256
    imageContent = image.file.read()
    hashedImage = hashlib.sha256(imageContent).hexdigest()
    hashedImg = hashedImage + os.path.splitext(image.filename)[1]

    # Create a new item dictionary
    new_item = {"id": item_id_num,"name": name, "category": category, "imageFile": hashedImg}

    # Increment the item ID counter for the next item
    item_id_num += 1

    # Append the new item to the existing list of items
    data["items"].append(new_item)

    # Save the updated items to the file
    with open("items.json", "w") as file:
        json.dump(data, file, indent=2)
    #logger.info(f"Receive item: {name}")
    return {"message": f"item received: {name}"}

# Define a route for the "/items" URL with a GET method
@app.get("/items")
def read_items():
    with open("items.json") as file:
        data = json.load(file)

    return data

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
