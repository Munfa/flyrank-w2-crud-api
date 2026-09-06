from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import copy

app = FastAPI()

tasks = [
    {'id': 1, 'title': 'Do homework', 'done': True},
    {'id': 2, 'title': 'Clean the room', 'done': False},
    {'id': 3, 'title': 'Water the plants', 'done': False}
]

initial_tasks = [
    {'id': 1, 'title': 'Do homework', 'done': True},
    {'id': 2, 'title': 'Clean the room', 'done': False},
    {'id': 3, 'title': 'Water the plants', 'done': False}
]

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

@app.get("/")
async def root():
    return { "name": "Task API", 
             "version": "1.0", 
             "endpoints": ["/tasks"] }

@app.get("/health")
async def health():
    return { "status": "ok" }

@app.get("/tasks")
async def get_tasks(done: Optional[bool] = None, search: Optional[str] = None):
    result = tasks
    if done is not None:
        result = [t for t in result if t['done'] == done]
    if search is not None:
        result = [t for t in result if search.lower() in t['title'].lower()]
    return result
    

@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    for task in tasks:
        if task['id'] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.get("/stats")
async def get_stats():
    total = len(tasks)
    done = sum(1 for t in tasks if t['done'])
    return f"Total: {total}, Done: {done}, Open: {total - done}"

@app.get("/reset")
async def reset_tasks():
    tasks.clear()
    tasks.extend(copy.deepcopy(initial_tasks))
    return {"Status": "reset", "Tasks" : tasks}

@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    if not task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required")

    if task:
        new_id = max(t['id'] for t in tasks) + 1
    else:
        new_id = 1

    new_task = {
        'id' : new_id,
        'title' : task.title,
        'done' : False
    }

    tasks.append(new_task)
    return new_task

def find_task_or_404(task_id: int):
    for task in tasks:
        if task['id'] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.put("/tasks/{task_id}")
async def update_task(task_id: int, update: TaskUpdate):
    task = find_task_or_404(task_id)

    if update.title is not None:
        if not update.title.strip():
            raise HTTPException(status_code=400, detail="Title is requried") 

        task['title'] = update.title

    if update.done is not None:
        task['done'] = update.done

    return task

@app.delete("/tasks/{task_id}", status_code=204)
async def delete_task(task_id: int):
    task = find_task_or_404(task_id)
    tasks.remove(task)