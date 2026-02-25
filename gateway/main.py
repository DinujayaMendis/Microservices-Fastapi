# gateway/main.py
from fastapi import FastAPI, HTTPException, Request, Depends, Header
from fastapi.responses import JSONResponse
import httpx
import jwt
import time
import logging
from typing import Any


app = FastAPI(title="API Gateway", version="1.0.0")

# Logging ලෑස්ති කිරීම (Setup logging)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GatewayLogger")

# අලුත් Middleware එක
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # ena request eka satahan karamu
    logger.info(f"Incoming Request: {request.method} {request.url.path}")
    
    # Request eka issarahata yawamu
    response = await call_next(request)
    
    # gatahwunu welawa balamu
    process_time = time.time() - start_time
    
    # Response ekai welawai satahn karamu
    logger.info(f"Response Status: {response.status_code} | Time Taken: {process_time:.4f}s")
    
    return response



# --- new Error Handlers (Activity 4) ---

# 1. api balaporoththu wena  Errors (ex: 401, 404)lassanata yawanna
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    # Error ekath log(satahan) karamu
    logger.error(f"HTTP Error {exc.status_code} at {request.url.path}: {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error_code": exc.status_code,
            "message": exc.detail,
            "path": request.url.path
        },
    )

# 2. api balaporoththu wenne nathi, nohithapu Errors (500) awoth allagannna
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unexpected Error at {request.url.path}: {str(exc)}")
    
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error_code": 500,
            "message": "Oops! There was a problem with the server. Please try again later.",
            "details": str(exc)
        },
    )


SECRET_KEY = "my_super_secret_key" # this is the key to sign the VIP Pass (Token) - in production, use a secure method to store this!

# 1. VIP Pass  (Token Endpoint)
@app.get("/token")
def get_token():
    token = jwt.encode({"user": "student"}, SECRET_KEY, algorithm="HS256")
    return {"access_token": token}

# 2. VIP Pass  check (Dependency)
async def verify_token(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="VIP Pass (Token) None.!")
    
    token = authorization.split(" ")[1]
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="VIP Pass (Token) That's wrong.!")
    

# Service URLs
SERVICES = {
    "student": "http://localhost:8001",
    "course": "http://localhost:8002"
}


async def forward_request(service: str, path: str, method: str, **kwargs) -> Any:
    """Forward request to the appropriate microservice"""
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")

    url = f"{SERVICES[service]}{path}"

    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(url, **kwargs)
            elif method == "POST":
                response = await client.post(url, **kwargs)
            elif method == "PUT":
                response = await client.put(url, **kwargs)
            elif method == "DELETE":
                response = await client.delete(url, **kwargs)
            else:
                raise HTTPException(status_code=405, detail="Method not allowed")
            return JSONResponse(
                content=response.json() if response.text else None,
                status_code=response.status_code
        )
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")
        
@app.get("/")
def read_root():
    return {"message": "API Gateway is running", "available_services": list(SERVICES.keys())}


# Student Service Routes
@app.get("/gateway/students", dependencies=[Depends(verify_token)])
async def get_all_students():
    """Get all students through gateway"""
    return await forward_request("student", "/api/students", "GET")


@app.get("/gateway/students/{student_id}")
async def get_student(student_id: int):
    """Get a student by ID through gateway"""
    return await forward_request("student", f"/api/students/{student_id}", "GET")


@app.post("/gateway/students")
async def create_student(body: dict):
    """Create a new student through gateway"""
    # body = await request.json()
    return await forward_request("student", "/api/students", "POST", json=body)


@app.put("/gateway/students/{student_id}")
async def update_student(student_id: int, body: dict):
    """Update a student through gateway"""
    # body = await request.json()
    return await forward_request("student", f"/api/students/{student_id}", "PUT", json=body)


@app.delete("/gateway/students/{student_id}")
async def delete_student(student_id: int):
    """Delete a student through gateway"""
    return await forward_request("student", f"/api/students/{student_id}", "DELETE")


#course

# Course Service Routes
@app.get("/gateway/courses")
async def get_all_courses():
    """Get all courses through gateway"""
    return await forward_request("course", "/api/courses", "GET")

@app.get("/gateway/courses/{course_id}")
async def get_course(course_id: int):
    """Get a course by ID through gateway"""
    return await forward_request("course", f"/api/courses/{course_id}", "GET")