from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List


app = FastAPI(
    title="To-Do List API",
    description="Simple To-Do List API built with FastAPI",
    version="1.0.0"
)


# -----------------------------
# Data Model
# -----------------------------

class Task(BaseModel):
    id: int
    title: str
    done: bool


# -----------------------------
# In-memory task storage
# -----------------------------

tasks: List[Task] = [
    Task(id=1, title="Learn FastAPI", done=False),
    Task(id=2, title="Build a REST API", done=False)
]


# -----------------------------
# GET - Get all tasks
# -----------------------------

@app.get("/tasks", response_model=List[Task], status_code=200)
def get_tasks():
    return tasks


# -----------------------------
# POST - Create a task
# -----------------------------

@app.post("/tasks", response_model=Task, status_code=201)
def create_task(task: Task):
    # Check if ID already exists
    for existing_task in tasks:
        if existing_task.id == task.id:
            raise HTTPException(
                status_code=400,
                detail="Task with this ID already exists"
            )

    tasks.append(task)
    return task


# -----------------------------
# GET - Get task by ID
# -----------------------------

@app.get("/tasks/{task_id}", response_model=Task, status_code=200)
def get_task_by_id(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task

    raise HTTPException(
        status_code=400,
        detail="Task ID not found"
    )


# -----------------------------
# PUT - Update task
# -----------------------------

@app.put("/tasks/{task_id}", response_model=Task, status_code=200)
def update_task(task_id: int, updated_task: Task):

    for index, task in enumerate(tasks):

        if task.id == task_id:

            # Make sure the ID in the body matches the URL
            if updated_task.id != task_id:
                raise HTTPException(
                    status_code=400,
                    detail="Task ID in body must match task ID in URL"
                )

            tasks[index] = updated_task
            return updated_task

    raise HTTPException(
        status_code=400,
        detail="Task ID not found"
    )


# -----------------------------
# DELETE - Delete task
# -----------------------------

@app.delete("/tasks/{task_id}", status_code=201)
def delete_task(task_id: int):

    for index, task in enumerate(tasks):

        if task.id == task_id:
            deleted_task = tasks.pop(index)

            return {
                "message": "Task deleted successfully",
                "task": deleted_task
            }

    raise HTTPException(
        status_code=400,
        detail="Task ID not found"
    )