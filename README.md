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
