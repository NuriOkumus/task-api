from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator
from database import init_db, get_all_tasks, get_task, create_task


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


@app.post("/tasks")
async def create_task_endpoint(task: Task):
    new_task = create_task(task.title, task.done)
    return JSONResponse(status_code=201, content=new_task)

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, task_data: Task):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks[i]["title"] = task_data.title
            tasks[i]["done"] = task_data.done
            return JSONResponse(status_code=200, content=tasks[i])
    return JSONResponse(status_code=404, content={"error": "Task not found"})

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return Response(status_code=204)
    return JSONResponse(status_code=404, content={"error": "Task not found"})
