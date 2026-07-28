from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator
from database import init_db


app = FastAPI()

@app.on_event("startup")
def startup():
    init_db()


class Task(BaseModel):
    title: str
    done: bool = False

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError("Title is required")
        return v

@app.get("/")
async def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
async def health():
    return {"status": "ok"}
