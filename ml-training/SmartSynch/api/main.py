from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from smartsynch.models.classifier import TaskClassifier

app = FastAPI()
classifier = TaskClassifier()

class TaskRequest(BaseModel):
    title: str
    description: str

class TaskResponse(BaseModel):
    category: str
    confidence: float

@app.post("/predict", response_model=TaskResponse)
async def predict_category(task: TaskRequest):
    try:
        result = classifier.predict(task.title, task.description)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 