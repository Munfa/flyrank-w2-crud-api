from fastapi import FastAPI, HTTPException

app = FastAPI()

tasks = [
    {'id': 1, 'title': 'Do homework', 'done': True},
    {'id': 2, 'title': 'Clean the room', 'done': False},
    {'id': 3, 'title': 'Water the plants', 'done': False}
]

@app.get("/")
async def root():
    return { "name": "Task API", 
             "version": "1.0", 
             "endpoints": ["/tasks"] }

@app.get("/health")
async def health():
    return { "status": "ok" }

@app.get("/tasks")
async def get_tasks():
    return tasks

@app.get("/tasks/{task_id}")
async def get_task(task_id: int):
    for task in tasks:
        if task['id'] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
