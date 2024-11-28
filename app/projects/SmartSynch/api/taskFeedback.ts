export async function submitTaskFeedback(
  title: string,
  description: string,
  predictedCategory: string,
  actualCategory: string,
  accepted: boolean
) {
  await fetch('/api/feedback', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      title,
      description,
      predicted_category: predictedCategory,
      actual_category: actualCategory,
      accepted
    })
  });
} 