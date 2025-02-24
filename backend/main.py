from fastapi import FastAPI
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
import requests
import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Fetch environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Database setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Movie(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    rating = Column(Integer)

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Movie API is running!"}

@app.get("/search")
def search_movies(query: str):
    """
    Fetch movies based on user query from TMDb API
    """
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}"
    response = requests.get(url).json()
    return response.get("results", [])

@app.get("/ai-recommend")
def ai_recommend(description: str):
    """
    Get AI-generated movie recommendations based on user descriptions
    """
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Find a movie based on this description: {description}",
        max_tokens=100
    )
    return {"recommendation": response["choices"][0]["text"].strip()}
