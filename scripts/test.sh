#!/bin/bash
set -e

BASE_URL="http://localhost/api"

read -p "Enter key to store: " key
read -p "Enter value to store: " value

echo ""
echo "Storing key/value in Redis..."
curl -s -X POST "$BASE_URL/cache" \
     -H "Content-Type: application/json" \
     -d "{\"key\":\"$key\",\"value\":\"$value\"}"
echo -e "\n"

echo "Retrieving key from Redis..."
curl -s "$BASE_URL/cache?key=$key"
echo -e "\n"


