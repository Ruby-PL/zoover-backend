from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.db import SessionLocal
from backend.models import Accommodation, Review

app = FastAPI(
    title="Zoover API",
    description="A RESTful API for accommodations and reviews",
    version="1.0.0",
    docs_url="/docs",  
    redoc_url="/redoc"
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "FastAPI is working!"}

@app.get("/accommodations")
def list_accommodations(db: Session = Depends(get_db)):
    accommodations = db.query(Accommodation).all()
    return [{"id": acc.id, "name": acc.name, "stars": acc.stars, "city_id": acc.city_id} for acc in accommodations]

@app.get("/accommodations/{accommodation_id}")
def get_accommodation(accommodation_id: str, db: Session = Depends(get_db)):
    accommodation = db.query(Accommodation).filter(Accommodation.id == accommodation_id).first()
    if not accommodation:
        raise HTTPException(status_code=404, detail="Accommodation not found")
    
    return {
        "id": accommodation.id,
        "name": accommodation.name,
        "stars": accommodation.stars,
        "city_id": accommodation.city_id,
        "country_id": accommodation.country_id,
        "popularity_score": accommodation.popularity_score,
    }

@app.get("/accommodations/{accommodation_id}/reviews")
def list_reviews(accommodation_id: str, db: Session = Depends(get_db)):
    reviews = db.query(Review).filter(Review.accommodation_id == accommodation_id).all()
    return [{"id": r.id, "user_name": r.user_name, "general_score": r.general_score, "text": r.text} for r in reviews]

@app.get("/accommodations/{accommodation_id}/reviews/{review_id}")
def get_review(accommodation_id: str, review_id: str, db: Session = Depends(get_db)):
    review = db.query(Review).filter(Review.accommodation_id == accommodation_id, Review.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")

    return {
        "id": review.id,
        "user_name": review.user_name,
        "general_score": review.general_score,
        "text": review.text,
        "travel_party": review.travel_party,
        "created_at": review.created_at,
    }

