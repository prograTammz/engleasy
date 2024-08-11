# Engleasy (English made easy)

## Project Description

## Frontend

### Installation

```bash
    cd frontend
    npm install
    npm run dev
```

## Backend

Engleasy Assessment is a backend service designed to facilitate English language assessments. The service provides functionality for generating, scoring, and managing English proficiency tests using a chatbot interface. The backend is built with Python and FastAPI, and it supports real-time communication via WebSocket. The project also utilizes MongoDB for storing user data and scores, Redis for caching, and AWS S3 for storing audio files.

### Key Features

- **English Proficiency Tests**: Automatically generate tests that cover reading, writing, listening, and speaking.
- **Chatbot Interface**: Interact with users via a chatbot that supports both text and voice input.
- **Scoring System**: Assess and score user responses according to CEFR standards.
- **WebSocket Communication**: Real-time interaction for ongoing tests.
- **AWS S3 Integration**: Store and retrieve audio files in/from AWS S3.
- **MongoDB & Redis**: Store user data, test results, and cached information efficiently.

### Project Structure

```plaintext
backend/
├── app/
│   ├── models/        # Pydantic models for data validation
│   ├── routers/       # API route handlers
│   ├── services/      # Business logic and interaction with external services
│   ├── utils/         # Utility functions and database clients
│   ├── main.py        # Application entry point
│   └── Dockerfile     # Docker configuration
├── tests/
│   ├── services/      # Unit tests for services
│   ├── utils/         # Unit tests for utility functions
│   └── ...
├── .env               # Environment variables
├── docker-compose.yml # Docker Compose configuration
└── README.md          # Project documentation
```

### Prerequisites

Before setting up the project, ensure you have the following installed:

- **Docker**: Install Docker
- **Docker Compose**: Install Docker Compose

### Setup and Installation

#### 1. Environment Variables

Create .env file and fill the required keys similar to example:

```plaintext
    SECRET_KEY=your_secret_key
    MONGO_URL=mongodb://db_mongodb:27017
    REDIS_HOST=db_redis
    REDIS_PORT=6379
    AWS_ACCESS_KEY_ID=your_aws_access_key
    AWS_SECRET_ACCESS_KEY=your_aws_secret_key
    AWS_S3_REGION_NAME=your_aws_region
    AWS_STORAGE_BUCKET_NAME=your_bucket_name
```

#### 2. Build and Run with Docker

To run the server you can use the following command:

```bash
    docker-compose up --build
```

To be able to run the testing you can run both of the following commands:

```bash
    docker-compose up -d --build
    docker-compose exec fastapi pytest --cov=app
```
