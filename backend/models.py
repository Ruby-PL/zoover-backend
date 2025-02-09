
from sqlalchemy import Column, String, Integer, Float, ForeignKey, JSON, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Accommodation(Base):
    __tablename__ = 'accommodations'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(String)
    country_id = Column(String, ForeignKey('countries.id'), nullable=False)
    region_id = Column(String, ForeignKey('regions.id'))
    city_id = Column(String, ForeignKey('cities.id'), nullable=False)
    stars = Column(Integer)
    photos_count = Column(Integer)
    popularity_score = Column(Float)
    booking_info = Column(JSON)
    default_price = Column(Integer)

    last_review_date = Column(DateTime) 
    overall_rating = Column(Float) 
    overall_review_count = Column(Integer)
    adjusted_price = Column(Float) 
    adjusted_rating = Column(Float)

    max_stars = Column(Integer) 
    min_stars = Column(Integer)
    distance_to_beach = Column(Integer)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    city = relationship("City", back_populates="accommodations")
    country = relationship("Country", back_populates="accommodations")
    region = relationship("Region", back_populates="accommodations")
    reviews = relationship("Review", back_populates="accommodation", cascade="all, delete-orphan")
    review_groups = relationship("AccommodationReviewByGroup", back_populates="accommodation", cascade="all, delete-orphan")
    review_aspects = relationship("AccommodationReviewAspect", back_populates="accommodation", cascade="all, delete-orphan")
    facts = relationship("AccommodationFact", back_populates="accommodation", cascade="all, delete-orphan")
    filters = relationship("AccommodationFilter", back_populates="accommodation", cascade="all, delete-orphan")


class AccommodationFact(Base):
    __tablename__ = 'accommodation_facts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    accommodation_id = Column(String, ForeignKey('accommodations.id'))
    fact_name = Column(String, nullable=False)
    fact_value = Column(String, nullable=True)
    fact_group = Column(String, nullable=False)

    accommodation = relationship("Accommodation", back_populates="facts")


class AccommodationFilter(Base):
    __tablename__ = 'accommodation_filters'

    id = Column(Integer, primary_key=True, autoincrement=True)
    accommodation_id = Column(String, ForeignKey('accommodations.id'))
    category = Column(String)
    value = Column(String)

    accommodation = relationship("Accommodation", back_populates="filters")


class AccommodationReviewByGroup(Base):
    __tablename__ = 'accommodation_review_by_group'

    id = Column(Integer, primary_key=True, autoincrement=True)
    accommodation_id = Column(String, ForeignKey('accommodations.id'))
    travel_group = Column(String)
    rating = Column(Float)
    review_count = Column(Integer)

    accommodation = relationship("Accommodation", back_populates="review_groups")


class AccommodationReviewAspect(Base):
    __tablename__ = 'accommodation_review_aspects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    accommodation_id = Column(String, ForeignKey('accommodations.id'))
    aspect = Column(String)  
    rating = Column(Float)
    review_count = Column(Integer)

    accommodation = relationship("Accommodation", back_populates="review_aspects")


class Review(Base):
    __tablename__ = 'reviews'

    id = Column(String, primary_key=True)
    accommodation_id = Column(String, ForeignKey('accommodations.id'), nullable=False)
    title = Column(String)
    user_name = Column(String)
    user_email = Column(String)
    user_ip_address = Column(String)
    travel_party = Column(String)
    travel_date = Column(String)
    general_score = Column(Float)
    status = Column(String)
    text = Column(String)
    locale = Column(String)
    source = Column(String)
    zoover_review_id = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    accommodation = relationship("Accommodation", back_populates="reviews")
    score_aspects = relationship("ReviewScoreAspect", back_populates="review", cascade="all, delete-orphan")


class ReviewScoreAspect(Base):
    __tablename__ = 'review_score_aspects'

    id = Column(Integer, primary_key=True, autoincrement=True)
    review_id = Column(String, ForeignKey('reviews.id'))
    aspect = Column(String)
    score = Column(Float)

    review = relationship("Review", back_populates="score_aspects")


class Country(Base):
    __tablename__ = 'countries'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    cities = relationship("City", back_populates="country")
    regions = relationship("Region", back_populates="country")
    accommodations = relationship("Accommodation", back_populates="country")


class Region(Base):
    __tablename__ = 'regions'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    country_id = Column(String, ForeignKey('countries.id'), nullable=False)

    country = relationship("Country", back_populates="regions")
    cities = relationship("City", back_populates="region")
    accommodations = relationship("Accommodation", back_populates="region")


class City(Base):
    __tablename__ = 'cities'

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    region_id = Column(String, ForeignKey('regions.id'))
    country_id = Column(String, ForeignKey('countries.id'), nullable=False)

    country = relationship("Country", back_populates="cities")
    region = relationship("Region", back_populates="cities")
    accommodations = relationship("Accommodation", back_populates="city")

