
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field

app = FastAPI(title="Book Publisher API")

@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(status_code=status.HTTP_204_NO_CONTENT)

class BookCreate(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    price: float = Field(gt=0)

class Book(BookCreate):
    id: int

books: dict[int, Book] = {}
next_id = 1

@app.get("/")
def home():
    return {"message": "Book Publisher API is running"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/books", response_model=Book, status_code=201)
def create_book(data: BookCreate):
    global next_id
    book = Book(id=next_id, **data.model_dump())
    books[next_id] = book
    next_id += 1
    return book

@app.get("/books", response_model=list[Book])
def list_books():
    return list(books.values())

@app.get("/books/{book_id}", response_model=Book)
def get_book(book_id: int):
    book = books.get(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=Book)
def update_book(book_id: int, data: BookCreate):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    book = Book(id=book_id, **data.model_dump())
    books[book_id] = book
    return book

@app.delete("/books/{book_id}", status_code=204)
def delete_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    del books[book_id]
