# 用了python的fastapi框架

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
import uvicorn
import json


class Task(BaseModel):
    id: int
    content: str
    createdTime: str


app = FastAPI()


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
        tasks.append(dict_task)
        f.seek(0)
        json.dump(tasks, f)
        print("加载入文件完成...")


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