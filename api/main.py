# main.py
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import spacy
import json
import os
import random
from typing import List, Dict, Optional
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="AI-Powered Career Guidance Platform",
    description="A platform to help underserved students navigate their career paths",
    version="1.0.0"
)

# Configure CORS to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load SpaCy NLP model or use a fallback
try:
    nlp = spacy.load("en_core_web_sm")
    print("SpaCy model loaded successfully")
except OSError:
    print("SpaCy model not found. Using a simple tokenizer instead.")
    # Simple fallback tokenizer
    class SimpleNLP:
        def __call__(self, text):
            class Doc:
                def __init__(self, text):
                    self.text = text
                    self.ents = []
            return Doc(text)
    nlp = SimpleNLP()

# Load or create job market data
job_market_data_path = "job_market_data.json"
if os.path.exists(job_market_data_path):
    with open(job_market_data_path, "r") as f:
        job_market_data = json.load(f)
    print(f"Loaded job market data from {job_market_data_path}")
else:
    job_market_data = {
        "required_skills": [
            "Python", "JavaScript", "Machine Learning", "Data Analysis", 
            "SQL", "Cloud Computing", "Agile Methodologies", "DevOps",
            "Artificial Intelligence", "Blockchain", "Communication",
            "Critical Thinking", "Problem Solving", "Teamwork"
        ],
        "career_paths": {
            "Data Scientist": {
                "required_skills": ["Python", "Machine Learning", "Data Analysis", "SQL"],
                "salary_range": "$80,000 - $150,000",
                "growth_rate": "High",
                "education": "Bachelor's or Master's in Computer Science, Statistics, or related field"
            },
            "Web Developer": {
                "required_skills": ["JavaScript", "HTML/CSS", "React", "Node.js"],
                "salary_range": "$70,000 - $120,000",
                "growth_rate": "Medium",
                "education": "Bachelor's in Computer Science or self-taught with portfolio"
            },
            "AI Engineer": {
                "required_skills": ["Python", "Machine Learning", "Artificial Intelligence", "Deep Learning"],
                "salary_range": "$90,000 - $160,000",
                "growth_rate": "Very High",
                "education": "Master's or PhD in Computer Science or related field"
            }
        }
    }
    with open(job_market_data_path, "w") as f:
        json.dump(job_market_data, f, indent=2)
    print(f"Created default job market data at {job_market_data_path}")

# Example resources database
resources = {
    "Python": [
        {"title": "Python for Beginners", "url": "https://www.python.org/about/gettingstarted/", "type": "tutorial"},
        {"title": "Advanced Python Programming", "url": "https://realpython.com/", "type": "course"}
    ],
    "JavaScript": [
        {"title": "JavaScript Fundamentals", "url": "https://javascript.info/", "type": "tutorial"},
        {"title": "Modern JavaScript", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript", "type": "documentation"}
    ],
    "Machine Learning": [
        {"title": "Intro to ML", "url": "https://www.coursera.org/learn/machine-learning", "type": "course"},
        {"title": "TensorFlow Basics", "url": "https://www.tensorflow.org/learn", "type": "tutorial"}
    ],
    "Data Analysis": [
        {"title": "Data Analysis with Python", "url": "https://pandas.pydata.org/docs/getting_started/index.html", "type": "tutorial"},
        {"title": "SQL for Data Analysis", "url": "https://mode.com/sql-tutorial/", "type": "tutorial"}
    ]
}

# Pydantic models for request/response validation
class ResumeInput(BaseModel):
    text: str

class ProgressUpdate(BaseModel):
    student_id: str
    skill: str

class CareerGoal(BaseModel):
    title: str
    reason: Optional[str] = None

class StudentProfile(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    education: Optional[str] = None
    career_goal: Optional[CareerGoal] = None

# Student data storage (replace with database in production)
students = {}

# Helper functions
def extract_skills(text):
    # In a real implementation, this would use more sophisticated NLP
    # For now, we'll use a simple keyword matching approach
    skills = []
    for skill in job_market_data["required_skills"]:
        if skill.lower() in text.lower():
            skills.append(skill)
    return skills

def find_skill_gaps(resume_skills, market_skills):
    return list(set(market_skills) - set(resume_skills))

def generate_learning_pathway(skill_gaps, resources):
    pathway = {}
    for skill in skill_gaps:
        if skill in resources:
            pathway[skill] = random.choice(resources[skill])
    return pathway

def recommend_careers(skills):
    matches = []
    for career, details in job_market_data["career_paths"].items():
        required_skills = details["required_skills"]
        matching_skills = [skill for skill in skills if skill in required_skills]
        match_percentage = len(matching_skills) / len(required_skills) * 100 if required_skills else 0
        matches.append({
            "title": career,
            "match_percentage": round(match_percentage, 1),
            "matching_skills": matching_skills,
            "missing_skills": [skill for skill in required_skills if skill not in skills],
            "details": details
        })
    # Sort by match percentage (descending)
    return sorted(matches, key=lambda x: x["match_percentage"], reverse=True)

# API Routes
@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <html>
        <head>
            <title>AI-Powered Career Guidance Platform</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    background: linear-gradient(135deg, #6e8efb, #a777e3);
                    color: white;
                }
                .container {
                    text-align: center;
                    padding: 2rem;
                    border-radius: 10px;
                    background-color: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                }
                h1 {
                    font-size: 2.5rem;
                    margin-bottom: 1rem;
                }
                p {
                    font-size: 1.2rem;
                    margin-bottom: 2rem;
                }
                .api-link {
                    display: inline-block;
                    background-color: white;
                    color: #6e8efb;
                    padding: 0.8rem 1.5rem;
                    border-radius: 30px;
                    text-decoration: none;
                    font-weight: bold;
                    transition: all 0.3s ease;
                }
                .api-link:hover {
                    transform: translateY(-3px);
                    box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Welcome to the AI-Powered Career Guidance Platform</h1>
                <p>Helping underserved students navigate their career paths with AI-powered insights</p>
                <a class="api-link" href="/docs">Explore API Documentation</a>
            </div>
        </body>
    </html>
    """

@app.post("/analyze_resume")
def analyze_resume(resume: ResumeInput):
    skills = extract_skills(resume.text)
    skill_gaps = find_skill_gaps(skills, job_market_data["required_skills"])
    pathway = generate_learning_pathway(skill_gaps, resources)
    career_matches = recommend_careers(skills)
    
    # Store student data
    student_id = f"student_{len(students) + 1}"
    students[student_id] = {
        "skills": skills,
        "skill_gaps": skill_gaps,
        "pathway": pathway,
        "career_matches": career_matches,
        "progress": {skill: False for skill in pathway},
        "profile": {}
    }
    
    return {
        "student_id": student_id, 
        "skills": skills,
        "skill_gaps": skill_gaps, 
        "pathway": pathway,
        "career_matches": career_matches[:3]  # Return top 3 matches
    }

@app.get("/student/{student_id}")
def get_student_info(student_id: str):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    return students[student_id]

@app.post("/update_progress")
def update_progress(update: ProgressUpdate):
    if update.student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    if update.skill not in students[update.student_id]["progress"]:
        raise HTTPException(status_code=400, detail="Invalid skill")
    
    students[update.student_id]["progress"][update.skill] = True
    return {"message": "Progress updated successfully"}

@app.post("/update_profile/{student_id}")
def update_profile(student_id: str, profile: StudentProfile):
    if student_id not in students:
        raise HTTPException(status_code=404, detail="Student not found")
    
    students[student_id]["profile"] = profile.dict(exclude_unset=True)
    return {"message": "Profile updated successfully"}

@app.get("/resources/{skill}")
def get_resources(skill: str):
    if skill not in resources:
        raise HTTPException(status_code=404, detail="Resources not found for this skill")
    return resources[skill]

@app.get("/market_data")
def get_market_data():
    return job_market_data

# Run the application
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
