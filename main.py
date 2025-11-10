from fastapi import FastAPI, Query
import os
import openai
from fastapi.middleware.cors import CORSMiddleware

openai.api_key = os.getenv("OPENAI_API_KEY")  # store key securely

app = FastAPI(title="Clinica AI", description="Medical Study Assistant for Students")

# Allow cross-origin requests (needed for plugins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Clinica AI API is running!"}

@app.get("/explain")
def explain_topic(topic: str = Query(..., description="Medical topic to explain")):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Clinica AI, a concise medical tutor."},
                {"role": "user", "content": f"Explain {topic} in 5 bullet points in simple medical language."}
            ],
            temperature=0.5
        )
        answer = response.choices[0].message["content"]
        return {"topic": topic, "explanation": answer}
    except Exception as e:
        return {"error": str(e)}

@app.get("/quiz")
def generate_quiz(topic: str = Query(..., description="Medical topic for MCQs")):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are Clinica AI, a medical tutor creating MCQs."},
                {"role": "user", "content": f"Create 3 multiple-choice questions with 4 options and answers on {topic}."}
            ],
            temperature=0.5
        )
        quiz = response.choices[0].message["content"]
        return {"topic": topic, "quiz": quiz}
    except Exception as e:
        return {"error": str(e)}
