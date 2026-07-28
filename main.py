from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator
from database import init_db, get_all_tasks, get_task


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

@app.get("/tasks")
async def get_tasks():
    return get_all_tasks()

@app.get("/tasks/{task_id}")
async def get_task_by_id(task_id: int):
    task = get_task(task_id)
    if task:
        return task
    return JSONResponse(status_code=404, content={"error": "Task not found"})
