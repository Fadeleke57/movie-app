#!/bin/bash

BASE_URL="http://127.0.0.1:5000"

echo "Starting smoke tests..."

#Test Health Check
health_check(){
echo "Testing /health endpoint..."
response=$(curl -s -X GET "$BASE_URL/api/health")
echo "Response: $response"
}

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

#Test Add To Watchlist
echo "Testing /add-to-watchlist endpoint..."
response=$(curl -s -X POST "$BASE_URL/watchlist/add-to-watchlist" -H "Content-Type: application/json" -d '{
  "username": "testuser123",
  "imdb_id": "tt0319343"
}')
echo "Response: $response"

#Test Delete From Watchlist
echo "Testing /delete-from-watchlist endpoint..."
response=$(curl -s -X DELETE "$BASE_URL/watchlist/delete-from-watchlist" -H "Content-Type: application/json" -d '{
  "username": "testuser123",
  "imdb_id": "tt0319343"
}')
echo "Response: $response"

echo "Smoke tests completed."

# Reset Database
python3 manage.py drop_db
python3 manage.py init_db

