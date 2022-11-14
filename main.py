from typing import Union

from fastapi import FastAPI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

TELEGRAM_KEY = os.getenv('TELEGRAM_KEY')


@app.get("/")
def read_root():
    return {"Hello": TELEGRAM_KEY}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

