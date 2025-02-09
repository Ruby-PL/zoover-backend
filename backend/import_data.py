
import json
import logging
from contextlib import contextmanager
from datetime import datetime
from sqlalchemy.orm import sessionmaker
from db import SessionLocal, Base
from models import (
    Accommodation, AccommodationFact, AccommodationFilter, AccommodationReviewByGroup,
    AccommodationReviewAspect, Review, ReviewScoreAspect, Country, Region, City
)

# Configure logging
logging.basicConfig(level=logging.INFO)

Base.metadata.create_all(bind=SessionLocal().bind)

@contextmanager
def session_scope():
    """Provide a transactional scope around database operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        logging.error(f"Database error: {e}")
        raise
    finally:
        session.close()

def load_json(filename):
    """Load JSON file and return the data."""
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def get_location_data(parent_ids, parents_list, session):
    """Finds the correct country, region, and city based on the parents[] array."""
    country_id = parent_ids.get("countryId")
    region_id = parent_ids.get("regionId")
    city_id = parent_ids.get("cityId")

    country_name, region_name, city_name = "Unknown", "Unknown", "Unknown"

    for parent in parents_list:
        if parent["id"] == country_id and parent["destinationType"] == "COUNTRY":
            country_name = parent["name"]
        if parent["id"] == region_id and parent["destinationType"] == "REGION":
            region_name = parent["name"]
        if parent["id"] == city_id and parent["destinationType"] == "CITY":
            city_name = parent["name"]

    # Check if country exists in the database
    country = session.query(Country).filter_by(id=country_id).first()
    if not country:
        country = Country(id=country_id, name=country_name)
        session.add(country)
    else:
        # If the country exists, update its name if necessary
        if country.name != country_name:
            country.name = country_name

    # Check if region exists in the database
    region = session.query(Region).filter_by(id=region_id).first()
    if not region:
        region = Region(id=region_id, name=region_name, country_id=country_id)
        session.add(region)
    else:
        # If the region exists, update its name if necessary
        if region.name != region_name:
            region.name = region_name

    # Check if city exists in the database
    city = session.query(City).filter_by(id=city_id).first()
    if not city:
        city = City(id=city_id, name=city_name, country_id=country_id, region_id=region_id)
        session.add(city)
    else:
        # If the city exists, update its name if necessary
        if city.name != city_name:
            city.name = city_name

    # Flush the session to ensure the IDs are available for the accommodation
    session.flush()

    return city_id, region_id, country_id

def import_accommodations(data):
    """Imports accommodations along with related details."""
    with session_scope() as session:
        for item in data:
            city_id, region_id, country_id = get_location_data(item["parentIds"], item["parents"], session)

            review_calc = item.get("reviewCalculations", {})
            adjusted = review_calc.get("adjusted", {})
            per_traveled_with = review_calc.get("perTraveledWith", {})
            overall = review_calc.get("overall", {})
            per_aspect_group = review_calc.get("perAspectGroup", {})

            last_review_timestamp = review_calc.get("lastReviewDate")
            last_review_date = datetime.utcfromtimestamp(last_review_timestamp / 1000) if last_review_timestamp else None

            accommodation = Accommodation(
                id=item["id"],
                name=item["name"],
                type=item["type"],
                country_id=country_id,
                region_id=region_id,
                city_id=city_id,
                stars=item.get("stars"),
                photos_count=item.get("photosCount"),
                popularity_score=item.get("popularityScore"),
                booking_info=item.get("bookingInfo", {}),
                default_price=item.get("bookingInfo", {}).get("defaultPrice"),

                # Store review calculations in the accommodation table
                last_review_date=last_review_date,
                overall_rating=overall.get("rating"),
                overall_review_count=overall.get("count"),
                adjusted_price=adjusted.get("price"),
                adjusted_rating=adjusted.get("rating"),
            )
            session.merge(accommodation)

            # Insert Accommodation Facts
            for fact in item.get("facts", []):
                fact_value = fact.get("value", "N/A")  
                session.merge(AccommodationFact(
                    accommodation_id=accommodation.id,
                    fact_name=fact["name"],
                    fact_value=fact_value,
                    fact_group=fact["group"]
                ))

            # Insert Review Ratings by Travel Group
            for travel_group, values in per_traveled_with.items():
                session.merge(AccommodationReviewByGroup(
                    accommodation_id=accommodation.id,
                    travel_group=travel_group,
                    rating=values.get("rating"),
                    review_count=values.get("count")
                ))

            # Insert Review Ratings by Aspect
            for aspect, values in per_aspect_group.items():
                session.merge(AccommodationReviewAspect(
                    accommodation_id=accommodation.id,
                    aspect=aspect,
                    rating=values.get("rating"),
                    review_count=values.get("count")
                ))

        logging.info("Accommodations and review calculations imported successfully!")

def import_reviews(data):
    """Imports reviews and their aspect scores."""
    with session_scope() as session:
        for item in data:
            accommodation = session.query(Accommodation).filter_by(id=item["accommodationId"]).first()
            if not accommodation:
                logging.warning(f"Accommodation {item['accommodationId']} not found for review {item['id']}")
                continue

            created_at = datetime.fromisoformat(item["createdAt"].replace("Z", ""))
            updated_at = datetime.fromisoformat(item["updatedAt"].replace("Z", ""))

            review = Review(
                id=item["id"],
                accommodation_id=item["accommodationId"],
                title=item["title"],
                user_name=item["userName"],
                user_email=item["userEmail"],
                user_ip_address=item["userIpAddress"],
                travel_party=item["travelParty"],
                travel_date=item["travelDate"],
                general_score=item["generalScore"],
                status=item["status"],
                text=item["text"],
                locale=item["locale"],
                source=item["source"],
                zoover_review_id=item["zooverReviewId"],
                created_at=created_at,
                updated_at=updated_at
            )
            session.merge(review)

            # Insert Review Score Aspects
            score_aspects = json.loads(item["scoreAspects"])
            for aspect, score in score_aspects.items():
                session.merge(ReviewScoreAspect(
                    review_id=review.id,
                    aspect=aspect,
                    score=score
                ))

        logging.info("Reviews imported successfully!")

if __name__ == "__main__":
    accommodations_data = load_json("data/accommodations.json")
    reviews_data = load_json("data/reviews.json")

    logging.info("Starting accommodation import...")
    import_accommodations(accommodations_data)

    logging.info("Starting review import...")
    import_reviews(reviews_data)

    logging.info("Import completed!")

