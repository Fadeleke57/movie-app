#!/bin/bash

BASE_URL="http://127.0.0.1:5000"

echo "Starting smoke tests..."

# Test User Account Creation
echo "Testing /user/create-account endpoint..."
response=$(curl -s -X POST "$BASE_URL/user/create-account" -H "Content-Type: application/json" -d '{
  "username": "testuser123",
  "password": "testpass"
}')
echo "Response: $response"

# Test Login
echo "Testing /user/login endpoint..."
response=$(curl -s -X POST "$BASE_URL/user/login" -H "Content-Type: application/json" -d '{
  "username": "testuser123",
  "password": "testpass"
}')
echo "Response: $response"

# Test Update Password
echo "Testing /user/update-password endpoint..."
response=$(curl -s -X POST "$BASE_URL/user/update-password" -H "Content-Type: application/json" -d '{
  "username": "testuser123",
  "old_password": "testpass",
  "new_password": "newpass"
}')
echo "Response: $response"

# Test Search by Title
echo "Testing /search-by-title endpoint..."
response=$(curl -s -X GET "$BASE_URL/search/search-by-title?title=Inception&year=2010&plot=full")
echo "Response: $response"

# Test Search by ID
echo "Testing /search-by-id endpoint..."
response=$(curl -s -X GET "$BASE_URL/search/search-by-id?id=tt1375666&plot=short")
echo "Response: $response"

# Test Search by Keyword
echo "Testing /search-by-keyword endpoint..."
response=$(curl -s -X GET "$BASE_URL/search/search-by-keyword?keyword=star&year=1977&content_type=movie&page=1")
echo "Response: $response"

# Test Search Random Movie
echo "Testing /search-random-movie endpoint..."
response=$(curl -s -X GET "$BASE_URL/search/search-random-movie?plot=short")
echo "Response: $response"

# Test Top Rated Movies
echo "Testing /top-rated-movies endpoint..."
response=$(curl -s -X GET "$BASE_URL/search/top-rated-movies")
echo "Response: $response"

echo "Smoke tests completed."

# Reset Database
python3 manage.py drop_db
python3 manage.py init_db

