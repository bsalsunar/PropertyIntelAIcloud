from backend.database import create_tables, save_analysis
from fastapi import FastAPI
from pydantic import BaseModel
from backend.ai_engine import analyze_listing_with_ai

app = FastAPI(
    title="PropertyIntelAI API",
    description="AI-powered real estate listing quality and SEO analyzer using a structured knowledge base.",
    version="1.0.0"
)

create_tables()


class ListingRequest(BaseModel):
    listing_text: str


@app.get("/")
def home():
    return {
        "message": "PropertyIntelAI API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.post("/analyze")
def analyze_listing(request: ListingRequest):
    result = analyze_listing_with_ai(request.listing_text)
    save_analysis(request.listing_text, result)
    return result
