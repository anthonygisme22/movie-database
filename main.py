from fastapi import FastAPI, Query  # FastAPI for handling API requests
from sqlalchemy import create_engine, Column, String, Integer  # SQLAlchemy for database management
from sqlalchemy.orm import sessionmaker, declarative_base  # ORM setup
import requests  # Handling external API calls
import openai  # AI-based movie recommendations

# Initialize FastAPI application
app = FastAPI()

# Database Configuration
DATABASE_URL = "postgresql://user:password@localhost/movies"
engine = create_engine(DATABASE_URL)  # Connect to PostgreSQL
SessionLocal = sessionmaker(bind=engine)  # Create session
Base = declarative_base()  # Base class for ORM models

# Define Movie Model (Database Table)
class Movie(Base):
    __tablename__ = "movies"  # Table name in PostgreSQL
    id = Column(Integer, primary_key=True, index=True)  # Unique ID for each movie
    title = Column(String, index=True)  # Movie title
    description = Column(String)  # Movie description
    rating = Column(Integer)  # User rating

# Create table in database
Base.metadata.create_all(bind=engine)

# TMDb API Integration
TMDB_API_KEY = "your_tmdb_api_key"
@app.get("/search")
def search_movies(query: str):
    """
    Fetch movies based on user query from TMDb API
    """
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}"
    response = requests.get(url).json()
    return response.get("results", [])

# AI-powered Recommendations (OpenAI API)
openai.api_key = "your_openai_api_key"
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
    return {"recommendation": response["choices"][0]["text"]}