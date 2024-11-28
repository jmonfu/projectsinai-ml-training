interface PredictionResponse {
  category: string | number;
  category_id: number;
  confidence: number;
  probabilities?: {
    [key: string]: number;
  };
}

export async function predictTaskCategory(
  title: string, 
  description: string
): Promise<PredictionResponse> {
  const response = await fetch('/api/v1/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, description })
  });
  
  if (!response.ok) {
    throw new Error('Prediction failed');
  }
  
  return response.json();
} 