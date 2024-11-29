interface PredictionResponse {
  category: string | number;
  category_id: number;
  confidence: number;
  probabilities?: {
    [key: string]: number;
  };
}

interface PredictionRequest {
  title: string;
  description: string;
}

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function predictTaskCategory(
  title: string, 
  description: string
): Promise<PredictionResponse> {
  try {
    const requestData: PredictionRequest = {
      title: title.trim(),
      description: description.trim()
    };

    const response = await fetch(`${API_URL}/api/v1/predict`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(requestData)
    });
    
    if (!response.ok) {
      const errorData = await response.json().catch(() => null);
      throw new Error(
        errorData?.message || 
        `Prediction failed with status: ${response.status}`
      );
    }
    
    const data = await response.json();
    return data as PredictionResponse;

  } catch (error) {
    console.error('Error predicting task category:', error);
    throw error instanceof Error 
      ? error 
      : new Error('Failed to predict task category');
  }
} 