from sentence_transformers import SentenceTransformer
from smartsynch.models.predictor import Predictor

class PredictionService:
    def __init__(self):
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        model_path = 'models/fine_tuned/20241205_162911/model.pt'
        self.classifier = Predictor(model_path)

    async def predict(self, text: str):
        # Generate embedding using the same model as training
        embedding = self.embedding_model.encode([text], convert_to_tensor=True)
        return self.classifier.predict(embedding) 