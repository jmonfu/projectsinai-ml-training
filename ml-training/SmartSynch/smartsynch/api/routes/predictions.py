"""
Prediction Routes

API endpoints for task categorization predictions.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import logging
from ...models.predictor import Predictor

logger = logging.getLogger(__name__)
router = APIRouter()

# Keyword sets for each category
KEYWORDS = {
    "Research": [
        ("research", 3.0),
        ("analyze", 2.5),
        ("investigate", 2.5),
        ("study", 2.0),
        ("evaluate", 2.0),
        ("compare", 2.0),
        ("explore", 1.5),
        ("assessment", 1.5),
        ("review", 1.5),
        ("findings", 1.5),
        ("analysis", 1.5)
    ],
    "Development": [
        ("implement", 2.0),
        ("code", 2.0),
        ("develop", 2.0),
        ("programming", 1.5),
        ("api", 1.5),
        ("database", 1.5),
        ("queries", 1.5),
        ("optimize", 1.5),
        ("bug", 2.0),
        ("fix", 1.5)
    ],
    "Design": [
        ("design", 2.5), ("ui", 2.5), ("ux", 2.5), ("wireframe", 2.5),
        ("mockup", 2.0), ("layout", 2.0), ("interface", 2.0),
        ("prototype", 1.5), ("visual", 1.5)
    ],
    "Meeting": [
        ("meeting", 2.5), ("standup", 2.5), ("sync", 2.5),
        ("discussion", 2.0), ("review meeting", 2.5),
        ("presentation", 1.5), ("demo", 1.5)
    ],
    "Planning": [
        ("planning", 3.0),
        ("plan", 3.0),
        ("roadmap", 2.5),
        ("timeline", 2.5),
        ("milestone", 2.0),
        ("schedule", 2.0),
        ("strategy", 2.0),
        ("migration", 2.0),
        ("prioritize", 1.5),
        ("estimate", 1.5)
    ]
}

class TaskRequest(BaseModel):
    title: str
    description: str

class PredictionResponse(BaseModel):
    category: str
    confidence: float

predictor = Predictor()

def predict_with_keywords(text: str) -> tuple[str, float] | None:
    """Predict category based on weighted keyword matching"""
    text = text.lower()
    logger.info(f"Processing text: {text}")
    
    # Pre-check for review tasks
    is_review = "review" in text
    review_keywords = ["design", "implementation", "research", "findings", "analysis"]
    is_multi_review = is_review and sum(1 for k in review_keywords if k in text) >= 2
    logger.info(f"Is review: {is_review}, Is multi-review: {is_multi_review}")
    
    # Check each category's keywords
    matches = {}
    for category, keyword_list in KEYWORDS.items():
        score = 0
        matched_keywords = []
        
        # Special handling for multi-aspect reviews
        if is_multi_review and category == "Research":
            score += 4.0  # Boost Research score for review tasks
        
        for keyword_tuple in keyword_list:
            keyword, weight = keyword_tuple  # Unpack the tuple
            count = text.count(keyword)
            if count > 0:
                # Title words count more
                title_bonus = 2.0 if keyword in text.split('.')[0] else 1.0
                
                # Adjust weights for mixed tasks
                if is_review:
                    if category == "Development":
                        weight *= 0.5  # Reduce Development weight for reviews
                    if category == "Research":
                        weight *= 1.5  # Boost Research weight for reviews
                
                current_score = count * weight * title_bonus
                score += current_score
                matched_keywords.append(f"{keyword}({count})")
                logger.info(f"Matched {category}: {keyword} (count={count}, weight={weight}, score={current_score})")
        
        if score > 0:
            base_confidence = 70.0
            score_bonus = min(25.0, score * 2.0)
            
            # Adjust confidence for reviews
            if is_multi_review:
                if category == "Research":
                    score_bonus = min(15.0, score_bonus)  # Cap review confidence
                else:
                    score_bonus *= 0.6  # Reduce confidence for other categories
            
            confidence = base_confidence + score_bonus
            matches[category] = (score, confidence)
            logger.info(f"Category {category}: final_score={score}, confidence={confidence}")
    
    if matches:
        best_category = max(matches.items(), key=lambda x: x[1][0])[0]
        confidence = matches[best_category][1]
        
        # Cap confidence based on task type
        if is_multi_review:
            confidence = min(85.0, confidence)
        elif is_review or len(matches) > 1:
            confidence = min(90.0, confidence)
        else:
            confidence = min(95.0, confidence)
            
        logger.info(f"Selected category: {best_category} with confidence {confidence}")
        return best_category, confidence
    
    logger.info("No keyword matches found")
    return None

@router.post("/predict", response_model=PredictionResponse)
async def predict_task(task: TaskRequest):
    """Predict category for a single task"""
    try:
        # Try keyword matching first
        text = f"{task.title}. {task.description}"
        keyword_result = predict_with_keywords(text)
        if keyword_result:
            category, confidence = keyword_result
            return PredictionResponse(
                category=category,
                confidence=confidence
            )
        
        # Fall back to Hugging Face API
        return predictor.predict(task.title, task.description)
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e)) 