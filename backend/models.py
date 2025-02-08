from sqlalchemy import create_engine, Column, String, Integer, Float, ForeignKey, Table, JSON, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

# Many-to-Many relation between Accommodation and Features
accommodation_features = Table(
    'accommodation_features', Base.metadata,
    Column('accommodation_id', String, ForeignKey('accommodations.id'), primary_key=True),
    Column('feature_id', String, ForeignKey('features.id'), primary_key=True)
)

class Accommodation(Base):
    __tablename__ = 'accommodations'
    
    id = Column(String, primary_key=True)
    name = Column(String)
    stars = Column(Integer)
    address = Column(String)
    zipcode = Column(String)
    phone = Column(String)
    email = Column(String)
    website = Column(String)
    country_id = Column(String, ForeignKey('countries.id'))
    city_id = Column(String, ForeignKey('cities.id'))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    reviews = relationship("Review", back_populates="accommodation")
    features = relationship("Feature", secondary=accommodation_features, back_populates="accommodations")
    weighted_scores = relationship("WeightedScore", back_populates="accommodation")


class Feature(Base):
    __tablename__ = 'features'
    
    id = Column(String, primary_key=True)
    name = Column(String)
    accommodations = relationship("Accommodation", secondary=accommodation_features, back_populates="features")


class Review(Base):
    __tablename__ = 'reviews'
    
    id = Column(String, primary_key=True)
    title = Column(String)
    user_name = Column(String)
    user_email = Column(String)
    user_ip_address = Column(String)
    travel_party = Column(String)
    travel_date = Column(DateTime)
    general_score = Column(Float)
    status = Column(String)
    text = Column(String)
    locale = Column(String)
    source = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    accommodation_id = Column(String, ForeignKey('accommodations.id'))
    
    accommodation = relationship("Accommodation", back_populates="reviews")
    score_aspects = relationship("ReviewScoreAspect", back_populates="review")


class ReviewScoreAspect(Base):
    __tablename__ = 'review_score_aspects'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    review_id = Column(String, ForeignKey('reviews.id'))
    aspect = Column(String)
    score = Column(Float)
    
    review = relationship("Review", back_populates="score_aspects")


class WeightedScore(Base):
    __tablename__ = 'weighted_scores'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    accommodation_id = Column(String, ForeignKey('accommodations.id'))
    aspect = Column(String)
    score = Column(Float)
    
    accommodation = relationship("Accommodation", back_populates="weighted_scores")


class Country(Base):
    __tablename__ = 'countries'
    
    id = Column(String, primary_key=True)
    name = Column(String)
    cities = relationship("City", back_populates="country")


class City(Base):
    __tablename__ = 'cities'
    
    id = Column(String, primary_key=True)
    name = Column(String)
    country_id = Column(String, ForeignKey('countries.id'))
    
    country = relationship("Country", back_populates="cities")
    accommodations = relationship("Accommodation", back_populates="city")

