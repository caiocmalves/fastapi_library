import json
from typing import Literal, Optional
from uuid import uuid4
from fastapi import FastAPI, HTTPException
import random
import os
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel


app = FastAPI()

class Book (BaseModel):
    name: str
    price: float
    book_id: Optional[str] = uuid4().hex
    genre: Literal["fiction", "non-fiction"]


BOOKS_FILE = "books.json"
BOOK_DATABASE = []


if os.path.exists(BOOKS_FILE):
    with open (BOOKS_FILE, "r") as f:
        BOOK_DATABASE = json.load(f)


#rota boas vindas
@app.get("/")
async def home():
    return "Welcome to my bookstore"

#listar books
@app.get("/list-books")
async def listBooks():
    return {"books" : BOOK_DATABASE}


#listar books by index
@app.get("/list-books-by-index/{index}")
async def listBooksByIndex(index: int):
    if index < 0 or index >= len(BOOK_DATABASE):
        raise HTTPException(404, "Index out of range")
    
    return {"books": BOOK_DATABASE[index]}


#listar books aleatorio
@app.get("/get-random-books")
async def listBooksRandom():
    return random.choice(BOOK_DATABASE)
    #return {"books:" : BOOK_DATABASE[random.randint(0,len(BOOK_DATABASE)-1)]}


@app.post("/add-book")
async def add_book(book: Book):
    book.book_id = uuid4().hex
    json_book = jsonable_encoder(book)
    BOOK_DATABASE.append(json_book)
    
    with open(BOOKS_FILE, "w") as f:
        json.dump(BOOK_DATABASE, f)
    return {"message" : f'Book {book} was added'}

