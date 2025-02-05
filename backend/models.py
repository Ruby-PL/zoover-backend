from sqlalchemy import Column, String, Integer, Float, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from db import Base

# Country Table
class Country(Base):
    __tablename__ = "countries"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    cities = relationship("City", back_populates="country")

# City Table
class City(Base):
    __tablename__ = "cities"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    country_id = Column(String, ForeignKey("countries.id"))
    country = relationship("Country", back_populates="cities")
    regions = relationship("Region", back_populates="city")

# Region Table
class Region(Base):
    __tablename__ = "regions"
    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    city_id = Column(String, ForeignKey("cities.id"))
    city = relationship("City", back_populates="regions")
    accommodations = relationship("Accommodation", back_populates="region")

# Accommodation Table
class Accommodation(Base):
    __tablename__ = "accommodations"
    id = Column(String, primary_key=True)
    type = Column(String)
    photos_count = Column(Integer)
    popularity_score = Column(Float)
    booking_price = Column(Integer)
    booking_days = Column(Integer)
    departure_date = Column(DateTime)
    airport = Column(String)

    region_id = Column(String, ForeignKey("regions.id"))
    region = relationship("Region", back_populates="accommodations")

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    facts = relationship("AccommodationFact", back_populates="accommodation", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="accommodation", cascade="all, delete-orphan")
    travel_parties = relationship("AccommodationTravelParty", back_populates="accommodation")

# Accommodation Facts Table
class AccommodationFact(Base):
    __tablename__ = "accommodation_facts"
    id = Column(Integer, primary_key=True, autoincrement=True)
    accommodation_id = Column(String, ForeignKey("accommodations.id", ondelete="CASCADE"))
    key = Column(String)
    value = Column(String)
    accommodation = relationship("Accommodation", back_populates="facts")

# Travel Party Table
class TravelParty(Base):
    __tablename__ = "travel_parties"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    reviews = relationship("Review", back_populates="travel_party")
    accommodations = relationship("AccommodationTravelParty", back_populates="travel_party")

# Many-to-Many Table: Accommodation <-> Travel Party
class AccommodationTravelParty(Base):
    __tablename__ = "accommodation_travel_party"
    accommodation_id = Column(String, ForeignKey("accommodations.id"), primary_key=True)
    travel_party_id = Column(Integer, ForeignKey("travel_parties.id"), primary_key=True)
    
    accommodation = relationship("Accommodation", back_populates="travel_parties")
    travel_party = relationship("TravelParty", back_populates="accommodations")

# Review Table
class Review(Base):
    __tablename__ = "reviews"
    id = Column(String, primary_key=True)
    accommodation_id = Column(String, ForeignKey("accommodations.id", ondelete="CASCADE"))
    title = Column(String)
    user_name = Column(String)
    
    travel_party_id = Column(Integer, ForeignKey("travel_parties.id"))
    travel_party = relationship("TravelParty", back_populates="reviews")

    travel_date = Column(String)
    general_score = Column(Float)
    status = Column(String)
    review_text = Column(String)
    locale = Column(String)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    accommodation = relationship("Accommodation", back_populates="reviews")
    aspect_scores = relationship("ReviewAspectScore", back_populates="review")

# Aspect Table
class Aspect(Base):
    __tablename__ = "aspects"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

# Many-to-Many Table: Review <-> Aspect Scores
class ReviewAspectScore(Base):
    __tablename__ = "review_aspect_scores"
    review_id = Column(String, ForeignKey("reviews.id"), primary_key=True)
    aspect_id = Column(Integer, ForeignKey("aspects.id"), primary_key=True)
    score = Column(Float, nullable=False)

    review = relationship("Review", back_populates="aspect_scores")
    aspect = relationship("Aspect")

