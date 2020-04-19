# 用了python的fastapi框架

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
import uvicorn
import json


class Task(BaseModel):
    id: int
    content: str
    createdTime: str


app = FastAPI()
origins = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/tasks")
async def get_tasks():
    tasks = []
    with open('data.json', 'r') as f:
        tasks = json.load(f)
    return tasks


@app.post("/api/tasks")
async def add_task(task: Task):
    dict_task = jsonable_encoder(task)
    with open('data.json', 'r+') as f:
        tasks = json.load(f)
        next_id = 1
        if tasks:
            next_id = max([t['id'] for t in tasks]) + 1
        dict_task['id'] = next_id
        tasks.append(dict_task)
        f.seek(0)
        f.truncate()
        json.dump(tasks, f)
        print("加载入文件完成...")


@app.put("/api/tasks/{id}")
async def modify(task: Task):
    dict_task = jsonable_encoder(task)
    id = dict_task['id']
    with open('data.json', 'r+') as f:
        tasks = json.load(f)
        for i in range(len(tasks)):
            if tasks[i]["id"] == id:
                tasks[i] = dict_task
                break
        f.seek(0)
        f.truncate()
        json.dump(tasks, f)


@app.get("/api/tasks/{id}")
async def get_task(id: int):
    result = None
    with open('data.json', 'r') as f:
        tasks = json.load(f)
        for task in tasks:
            if task["id"] == id:
                result = task
                break
    return result


@app.delete("/api/tasks/{id}")
async def delete_task(id: int):
    with open('data.json', mode='r+') as f:
        tasks = json.load(f)
        for task in tasks:
            if task["id"] == id:
                tasks.remove(task)
                break
        f.seek(0)
        f.truncate()
        json.dump(tasks, f)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)