#!/bin/bash

# Create logs directory if it doesn't exist
mkdir -p ../logs

# Generate timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="../logs/test_results_${TIMESTAMP}.txt"

# Run tests and save output
echo "Starting tests at $(date)" | tee "$LOG_FILE"
echo "----------------------------------------" | tee -a "$LOG_FILE"

./test_predictions.sh | tee -a "$LOG_FILE"

echo "----------------------------------------" | tee -a "$LOG_FILE"
echo "Tests completed at $(date)" | tee -a "$LOG_FILE"
echo "Results saved to: $LOG_FILE" 