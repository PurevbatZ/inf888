from supabase import create_client, Client
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# SUPA BASE URL AND KEYS
url: str = "https://slwaziijzcvakvcjqdbd.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InNsd2F6aWlqemN2YWt2Y2pxZGJkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDE4Mzk3NjksImV4cCI6MjA1NzQxNTc2OX0.Ot872fwBsjxDGTwS1-6rLuvJSodCatIoh6KneuVhjWM"

supabase: Client = create_client(url, key)

app = FastAPI()

# Table model
class Book(BaseModel):
    bookID: int
    title: str
    authors: str
    average_rating: float
    publication_date: str
    publisher: str
    
#Message
@app.get("/")
def root():
    return {"message": "FastAPI is live on Render :)"}

# CREATE
@app.post("/books/")
def create_book(book: Book):
    data = supabase.table("books").insert(book.dict()).execute()
    if data.data:
        return data.data
    raise HTTPException(status_code=400, detail="Book could not be created")

# READ ALL
@app.get("/books/")
def read_books():
    data = supabase.table("books").select("*").execute()
    if data.data:
        return data.data
    raise HTTPException(status_code=404, detail="No books found")

# READ BY ID
@app.get("/books/{book_id}")
def read_book(book_id: int):
    data = supabase.table("books").select("*").eq("bookID", book_id).execute()
    if data.data:
        return data.data[0]  # Return the first (and only) matching result
    raise HTTPException(status_code=404, detail="Book not found")

# UPDATE
@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    data = supabase.table("books").update(book.dict()).eq("bookID", book_id).execute()
    if data.data:
        return data.data
    raise HTTPException(status_code=404, detail="Book not found")

# DELETE
@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    data = supabase.table("books").delete().eq("bookID", book_id).execute()
    if data.data:
        return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")
