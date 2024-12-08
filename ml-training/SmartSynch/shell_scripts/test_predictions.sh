#!/bin/bash

# Set base URL
BASE_URL="http://localhost:8000"

# Set text colors
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Add error handling
set -e  # Exit on error
trap 'echo "Error on line $LINENO"' ERR

# Add timeout to curl
CURL_OPTS="--max-time 10 --silent --show-error"

echo -e "${GREEN}Testing Task Predictions${NC}\n"
echo -e "${GREEN}Using API at: ${BASE_URL}${NC}\n"

# Email Service Provider Migration
echo -e "\n${GREEN}105. Testing: Email Service Provider Migration${NC}"
curl $CURL_OPTS -X POST "${BASE_URL}/api/smartsynch/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Email Service Provider Migration",
    "description": "Migrate from SendGrid to AWS SES with template management and analytics."
  }' | jq '.'

sleep 1

# Plugin System Architecture
echo -e "\n${GREEN}164. Testing: Plugin System Architecture${NC}"
curl $CURL_OPTS -X POST "${BASE_URL}/api/smartsynch/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Plugin System Architecture",
    "description": "Design and implement extensible plugin architecture with versioning and dependency management."
  }' | jq '.'

sleep 1

# Other Category
echo -e "\n${GREEN}170. Testing: Office Network Upgrade${NC}"
curl $CURL_OPTS -X POST "${BASE_URL}/api/smartsynch/v1/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Office Network Upgrade",
    "description": "Coordinate with IT for office network infrastructure upgrade."
  }' | jq '.'

sleep 1

# Add proper exit
echo -e "\n${GREEN}All tests completed successfully${NC}"
exit 0


