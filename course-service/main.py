from fastapi import FastAPI

app = FastAPI(title="Course Microservice", version="1.0.0")

#  course data (Mock data)
courses = [
    {"id": 1, "name": "Computer Science", "duration": "4 Years"},
    {"id": 2, "name": "Information Technology", "duration": "3 Years"},
    {"id": 3, "name": "Software Engineering", "duration": "4 Years"}
]

@app.get("/")
def read_root():
    return {"message": "Course Microservice is running"}

@app.get("/api/courses")
def get_all_courses():
    """Get all courses"""
    return courses

@app.get("/api/courses/{course_id}")
def get_course(course_id: int):
    """Get a course by ID"""
    course = next((c for c in courses if c["id"] == course_id), None)
    if course:
        return course
    return {"error": "Course not found"}