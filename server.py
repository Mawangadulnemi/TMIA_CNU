import funs

from fastapi import FastAPI
from pydantic import BaseModel

class Item(BaseModel):
    text: str


app = FastAPI()


@app.post("/api/speaking-style")
async def response(item: Item):
    return {"response": funs.run(item.text)}
