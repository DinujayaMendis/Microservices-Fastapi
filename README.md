# FastAPI Microservices Architecture with API Gateway

This repository contains a fully functional Microservices Architecture implemented using Python and FastAPI. It demonstrates how to build, route, and manage multiple independent services through a centralized API Gateway.

[cite_start]This project was developed as part of the IT4020 - Modern Topics in IT module (Practical 3)[cite: 5, 28].

## 🚀 Key Features

* [cite_start]**API Gateway Pattern:** A single entry point (Port 8000) that seamlessly routes client requests to the appropriate underlying microservices [cite: 377-379].
* [cite_start]**Independent Microservices:** * **Student Service (Port 8001):** Handles CRUD operations for student records [cite: 77-78, 220].
  * [cite_start]**Course Service (Port 8002):** Manages course-related data [cite: 397-399].
* [cite_start]**JWT Authentication:** Secure API endpoints at the gateway level using JSON Web Tokens (JWT) to ensure only authorized clients can access the services [cite: 400-401].
* [cite_start]**Middleware Logging:** Intercepts and logs all incoming requests and outgoing responses, including execution time tracking [cite: 402-403].
* [cite_start]**Global Error Handling:** Custom exception handlers that catch HTTP exceptions and unexpected server errors, returning clean, structured JSON responses [cite: 404-405].

## 🛠️ Tools & Technologies

* [cite_start]Python 3.8+ [cite: 12]
* [cite_start]FastAPI (High-performance web framework) [cite: 13]
* [cite_start]Uvicorn (ASGI server for running the apps) [cite: 14]
* [cite_start]HTTPx (For asynchronous gateway routing) [cite: 15]
* [cite_start]Pydantic (For robust data validation) [cite: 15]
* PyJWT (For securing the gateway)

  
# Terminal 1: Start Student Service
cd student-service
uvicorn main:app --reload --port 8001

# Terminal 2: Start Course Service
cd course-service
uvicorn main:app --reload --port 8002

# Terminal 3: Start API Gateway
cd gateway
uvicorn main:app --reload --port 8000

## 📁 Project Structure

```text
microservices-fastapi/
│
├── gateway/                 # API Gateway application
│   └── main.py              # Routing, JWT, Logging, and Error Handling logic
│
├── student-service/         # Student Microservice
│   ├── main.py              # FastAPI endpoints
│   ├── models.py            # Pydantic models
│   ├── service.py           # Business logic
│   └── data_service.py      # Mock data layer
│
├── course-service/          # Course Microservice
│   └── main.py              # Course endpoints and mock data
│
└── requirements.txt         # Project dependencies


