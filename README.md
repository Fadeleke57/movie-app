# movie-app


# Movie App

A simple Flask-based movie application that integrates with the OMDB API for fetching movie data and provides user account management functionality.

---

## Features

- **Health Check Route**: Verify the app is running.
- **User Account Management**:
  - Create an account
  - Log in
  - Update password
- **Movie API Integration**: Work in progress.

---

## Requirements

- **Python**: Version 3.8 or higher
- **pip**: Python package manager
- **Docker** (optional): For running the app in a containerized environment.

---

## Setup Instructions

### Running Locally

1. **Clone the Repository**

   ```bash
   git clone <repository_url>
   cd movie-app
   ```

2. **Create a Virtual Environment**

   Create a virtual environment to isolate dependencies:
   ```bash
   python3 -m venv movieapp
   ```

   Activate the virtual environment:
   - On macOS/Linux:
     ```bash
     source movieapp/bin/activate
     ```
   - On Windows:
     ```bash
     .\movieapp\Scripts\activate
     ```

3. **Install Dependencies**

   Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**

   Create a `.env` file in the root directory and add the following:
   ```plaintext
   OMDB_API_KEY=your_omdb_api_key_here
   ```

   Replace `your_omdb_api_key_here` with your actual OMDB API key.

5. **Set Up the Database**

   Use the `manage.py` script to initialize the database:
   ```bash
   python manage.py init_db
   ```

6. **Run the Application**

   Start the Flask development server:
   ```bash
   python run.py
   ```

   By default, the app runs on `http://127.0.0.1:5000`. You can access the app and test the routes.

---

## Testing

unit tests are in the tests folder
to run the tests:
   ```bash
   python -m pytest tests/
   ```

---

### Using Docker

1. **Build the Docker Image**

   Build the Docker image for the application:
   ```bash
   docker build -t movie-app .
   ```

2. **Run the Docker Container**

   Run the container, mapping port `8080` and loading the `.env` file:
   ```bash
   docker run -d -p 8080:8080 --env-file .env movie-app
   ```

3. **Access the Application**

   The app will be available at `http://localhost:8080`.

---

# Movie App API

This is a Flask-based API for managing movie-related functionalities, including user account management, movie search, and more.

## Table of Contents
- [API Endpoints](#api-endpoints)
  - [Health Check](#health-check)
  - [User Account Management](#user-account-management)
  - [Movie Search](#movie-search)
  - [Watchlist Management](#watchlist-management)

---

## API Endpoints

### Health Check

- **URL**: `/api/health`
- **Method**: `GET`
- **Response**:
  ```json
  {
    "status": "App is running!"
  }
  ```

---

### User Account Management

#### Create Account
- **URL**: `/user/create-account`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response**:
  - **Success**: `201 Created`
    ```json
    {
      "message": "Account created successfully"
    }
    ```
  - **Error**: `400 Bad Request` or `409 Conflict`

#### Log In
- **URL**: `/user/login`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "username": "string",
    "password": "string"
  }
  ```
- **Response**:
  - **Success**: `200 OK`
    ```json
    {
      "message": "Login successful"
    }
    ```
  - **Error**: `400 Bad Request` or `401 Unauthorized`

#### Update Password
- **URL**: `/user/update-password`
- **Method**: `POST`
- **Request Body**:
  ```json
  {
    "username": "string",
    "old_password": "string",
    "new_password": "string"
  }
  ```
- **Response**:
  - **Success**: `200 OK`
    ```json
    {
      "message": "Password updated successfully"
    }
    ```
  - **Error**: `400 Bad Request`, `401 Unauthorized`, or `404 Not Found`

---
### Movie Search

#### Search by Title
- **URL**: `/search-by-title`
- **Method**: `GET`
- **Query Parameters**:
  - `title` (string, required): The title of the movie.
  - `year` (integer, optional): Filter results by release year.
  - `plot` (string, optional): Must be `"short"` or `"full"`. Determines the length of the plot summary.

- **Example Request**:
  ```bash
  curl "http://127.0.0.1:5000/search-by-title?title=Inception&year=2010&plot=full"
  ```

- **Response**:
  - **Success**: `200 OK`
    ```json
    {
      "Title": "Inception",
      "Year": "2010",
      "Plot": "A skilled thief who steals secrets..."
    }
    ```
  - **Error**: `400 Bad Request`
    ```json
    {
      "error": "Missing 'title' parameter."
    }
    ```

#### Search by ID
- **URL**: `/search-by-id`
- **Method**: `GET`
- **Query Parameters**:
  - `id` (string, required): The IMDb ID of the movie.
  - `plot` (string, optional): Must be `"short"` or `"full"`. Determines the length of the plot summary.

- **Example Request**:
  ```bash
  curl "http://127.0.0.1:5000/search-by-id?id=tt1375666&plot=short"
  ```

- **Response**:
  - **Success**: `200 OK`
    ```json
    {
      "Title": "Inception",
      "Year": "2010",
      "Plot": "A skilled thief who steals secrets..."
    }
    ```
  - **Error**: `400 Bad Request`
    ```json
    {
      "error": "Missing 'id' parameter."
    }
    ```

#### Search by Keyword
- **URL**: `/search-by-keyword`
- **Method**: `GET`
- **Query Parameters**:
  - `keyword` (string, required): The search keyword.
  - `year` (integer, optional): Filter results by release year.
  - `content_type` (string, optional): Must be `"movie"`, `"series"`, or `"episode"`. Filters results by content type.
  - `page` (integer, optional): Specifies the page number for paginated results. Defaults to 1.

- **Example Request**:
  ```bash
  curl "http://127.0.0.1:5000/search-by-keyword?keyword=star&year=1977&content_type=movie&page=1"
  ```

- **Response**:
  - **Success**: `200 OK`
    ```json
    [
      {
        "Title": "Star Wars",
        "Year": "1977",
        "imdbID": "tt0076759",
        "Type": "movie",
        "Poster": "http://example.com/poster.jpg"
      },
      {
        "Title": "Star Wars: Episode V",
        "Year": "1980",
        "imdbID": "tt0080684",
        "Type": "movie",
        "Poster": "http://example.com/poster2.jpg"
      }
    ]
    ```
  - **Error**: `400 Bad Request`
    ```json
    {
      "error": "Missing 'keyword' parameter."
    }
    ```

#### Search Random Movie
- **URL**: `/search-random-movie`
- **Method**: `GET`
- **Query Parameters**:
  - `plot` (string, optional): Must be `"short"` or `"full"`. Determines the length of the plot summary.

- **Example Request**:
  ```bash
  curl "http://127.0.0.1:5000/search-random-movie?plot=short"
  ```

- **Response**:
  - **Success**: `200 OK`
    ```json
    {
      "Title": "Avatar",
      "Year": "2009",
      "Plot": "A paraplegic Marine is dispatched to the moon Pandora..."
    }
    ```
  - **Error**: `500 Internal Server Error`
    ```json
    {
      "error": "Failed to fetch data from OMDB API"
    }
    ```

#### Top Rated Movies
- **URL**: `/top-rated-movies`
- **Method**: `GET`

- **Example Request**:
  ```bash
  curl "http://127.0.0.1:5000/top-rated-movies"
  ```

- **Response**:
  - **Success**: `200 OK`
    ```json
    [
      {
        "Title": "The Shawshank Redemption",
        "Year": "1994",
        "imdbID": "tt0111161",
        "Type": "movie",
        "Poster": "http://example.com/poster1.jpg"
      },
      {
        "Title": "The Godfather",
        "Year": "1972",
        "imdbID": "tt0068646",
        "Type": "movie",
        "Poster": "http://example.com/poster2.jpg"
      }
    ]
    ```
  - **Error**: `500 Internal Server Error`
    ```json
    {
      "error": "Failed to fetch data from OMDB API"
    }
    ```
---

### Watchlist Management

#### Add Movie to WatchList by Movie ID
- **Route**: `/add-to-watchlist`
- **Request Type**: `POST`
- **Request Body**:
  - `username` (string, required): The username of the user.
  - `imdb_id` (string, required): The imdb_id of the movie you are trying to insert.
- **Request Format**: JSON
    - **Success Response Example:**
        - code: 201
        - content: {"message": "Movie added to {username}'s watchlist"}
  **Example Request**:
  ```json
  {
    "username": "name",
    "imdb_id": "tt0319343",
  }
  ```

- **Example Response**:
    ```json
    {
        "message": "Movie added to {username}'s watchlist",
        "status": "201" 
    }
    ```

---

## Common Commands

### Initialize the Database
```bash
python manage.py init_db
```

### Drop All Database Tables
```bash
python manage.py drop_db
```

### Run the Application Locally
```bash
python run.py
```

### Build the Docker Image
```bash
docker build -t movie-app .
```

### Run the Docker Container
```bash
docker run -d -p 8080:8080 --env-file .env movie-app
```

### Stop the Docker Container
1. Find the container ID:
   ```bash
   docker ps
   ```
2. Stop the container:
   ```bash
   docker stop <container_id>
   ```

---

## Contribution Guidelines

Contributions are not welcome unless you are in our group!

---

## License

This project is licensed under the MIT License.
