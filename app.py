from fastapi import FastAPI, Body
from pydantic import BaseModel
from main import handler

app = FastAPI()

class RequestBody(BaseModel):
    prompt: str
    session_id: str

@app.post("/")
async def run_handler(body: RequestBody):
    event = {"body": body.json()}
    result = handler(event, None)
    return result
