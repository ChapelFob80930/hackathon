import openai
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv(dotenv_path="key.env")

# Set your OpenAI API key from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI app
app = FastAPI()

# Define request body schema
class BusinessIdeaRequest(BaseModel):
    problem_statement: str
    audience: str

# Root endpoint (test)
@app.get("/")
def read_root():
    return {"message": "Welcome to the Hackathon Backend!"}

# Business idea generation endpoint using OpenAI API
@app.post("/generate_idea/")
def generate_idea(request: BusinessIdeaRequest):
    try:
        # Create the prompt for OpenAI API
        prompt = f"Create a business idea for the problem: {request.problem_statement}. The target audience is: {request.audience}."
        
        # Call OpenAI API for text generation using ChatCompletion (for newer versions of openai)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # You can use gpt-4 if you have access
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=100  # Limit the length of the response
        )

        # Get the text response from OpenAI API
        idea = response['choices'][0]['message']['content'].strip()
        return {"idea": idea}
    except Exception as e:
        return {"error": str(e)}
