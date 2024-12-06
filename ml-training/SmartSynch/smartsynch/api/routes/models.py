from fastapi import APIRouter
from pydantic import BaseModel
from transformers import pipeline

router = APIRouter()

class PredictionRequest(BaseModel):
    title: str
    description: str

MODEL_CONFIGS = {
    "task-categorization": {
        "model": "facebook/bart-large-mnli",  # Good for multi-class classification
        "task": "zero-shot-classification",
        "labels": ["Development", "Design", "Research", "Meeting", "Planning"]
    }
}

models = {}

@router.post("/predict/{model_name}")
async def predict(model_name: str, request: PredictionRequest):
    if model_name not in MODEL_CONFIGS:
        return {"error": f"Model {model_name} not supported"}
        
    if model_name not in models:
        config = MODEL_CONFIGS[model_name]
        models[model_name] = pipeline(
            task=config["task"],
            model=config["model"]
        )
    
    # Combine title and description for better context
    text = f"{request.title}. {request.description}"
    result = models[model_name](
        text, 
        candidate_labels=MODEL_CONFIGS[model_name]["labels"]
    )
    
    return {
        "title": request.title,
        "description": request.description,
        "category": result["labels"][0],  # Best matching category
        "confidence": round(result["scores"][0] * 100, 2),
        "all_scores": dict(zip(result["labels"], result["scores"]))
    } 