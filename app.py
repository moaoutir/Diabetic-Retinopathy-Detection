from typing import Union

from fastapi import FastAPI
from fastapi import UploadFile, File, Request,Form
import os
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from starlette.responses import FileResponse 
from utils import *
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import base64
from pydantic import BaseModel
from typing import Any

# from starlette.formparsers import MultiPartParser
# MultiPartParser.max_file_size = 2 * 1024 * 1024

app = FastAPI()

app.mount("/static", StaticFiles(directory="user_interface/static"), name="static")

templates = Jinja2Templates(directory="user_interface/templates")

load_saved_artifacts()


@app.get("/", response_class=HTMLResponse)
def read_item(request: Request):
    context={"request": request}
    return templates.TemplateResponse("index.html", context)


@app.post("/classify_image")
async def upload_base64_image(image: UploadFile = File(...)):
    print("image received ")
    
    image_bytes = await image.read()
    predicted_label = image_prediction(image_bytes)

    return predicted_label

