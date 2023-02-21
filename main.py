from fastapi import FastAPI,Response, UploadFile, File,Form,HTTPException
from fastapi.encoders import jsonable_encoder
from NLP import *
from pydantic import BaseModel
import secrets
from tortoise import Model
from io import StringIO
import csv
from fastapi.responses import HTMLResponse
import uvicorn

from fastapi.staticfiles import StaticFiles
from PIL import Image



class text(BaseModel):
    text : str


app = FastAPI()



@app.get("/")
async def index():
    return{"Message":"Hello World"}  

@app.post("/NLP/Summary")
async def summary(text : text):
    summary = await text_summary(text.text)
    return summary

@app.post("/NLP/Sum")
async def sum(text:text):
    sum = await rangkum(text.text)
    return sum

@app.post("/NLP/Sentiment")
async def sentiment(text:text):
    sentiment = await text_sentiment(text.text)
    json_compatible = jsonable_encoder(sentiment)
    return json_compatible

@app.post("/upload")
def upload(file: UploadFile = File(...)):
    data = file.file.read()
    return data
    
@app.post("/upload/sentiment")
async def sentiment_file(file:UploadFile = File(...)):
    data = file.file.read()
    data = data.decode()

    sentiment = await text_sentiment(data)
    await file.close()
    return sentiment


