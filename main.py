from supabase import create_client, Client

url: str = "https://fhbnbquxzuumvhmycflu.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZoYm5icXV4enV1bXZobXljZmx1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDE4Mzk0NDksImV4cCI6MjA1NzQxNTQ0OX0.odm7X9uZO6DEkynv4AVIgllDtOojWnIwU1zAtafRMnI"
supabase: Client = create_client(url, key)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None

@app.post("/items/")
async def create_item(item: Item):
    try:
        response = supabase.table("items").insert(item.dict()).execute()
        return response.data
    except:
        raise HTTPException(status_code=400, detail="Item could not be created")
    

@app.get("/items/")
async def read_items():
    try:
        response = supabase.table("items").select("*").execute()
        return response.data
    except:
        raise HTTPException(status_code=404, detail="Items not found")
   
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    try:
        response = supabase.table("items").update(item.dict()).eq("id", item_id).execute()
        return response.data
    except: 
        raise HTTPException(status_code=404, detail="Item not found")
    
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    try:
        response = supabase.table("items").delete().eq("id", item_id).execute()
        return {"message": "Item deleted successfully"}
    except:
        raise HTTPException(status_code=404, detail="Item not found")
    
