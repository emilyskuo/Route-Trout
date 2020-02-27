import requests
import os

from model import (User, Trail, User_Trail, Trip, Trip_User,
                   Trip_Trail, Trip_Comment, db, connect_to_db)


GOOGLE_MAPS_KEY = os.environ['GOOGLE_MAPS_KEY']
HIKING_PROJECT_KEY = os.environ['HIKING_PROJECT_KEY']


def call_geocoding_api(search_terms):
    """Query Google Maps Geocoding API to convert search terms to

    long/lat coordinates"""

    api_url = "https://maps.googleapis.com/maps/api/geocode/json"
    payload = {
        "address": search_terms,
        "key": GOOGLE_MAPS_KEY
    }

    r = requests.get(api_url, params=payload)
    response = r.json()

    # Check to see if search was valid
    if "error_message" not in response:
        lat_long = response["results"][0]["geometry"]["location"]
        return lat_long

    # Return error message if message invalid
    else:
        return "Invalid search terms"


def call_hiking_project_api(lat_long):
    """Query Hiking Project API to retrieve trail list given

    lat/long coordinates"""

    hiking_api_url = "https://www.hikingproject.com/data/get-trails"

    payload = {
        "lat": lat_long["lat"],
        "lon": lat_long["lng"],
        "maxResults": 30,
        "key": HIKING_PROJECT_KEY
    }

    r = requests.get(hiking_api_url, params=payload)
    response = r.json()

    return response


def convert_trail_difficulty(color_difficulty):
    """Convert Hiking Project API's difficulty rating from color to words"""

    if color_difficulty == "green":
        difficulty = "Easy"
    elif color_difficulty == "greenBlue":
        difficulty = "Moderately Easy"
    elif color_difficulty == "blue":
        difficulty = "Intermediate"
    elif color_difficulty == "blueBlack":
        difficulty = "Somewhat Difficult"
    elif color_difficulty == "black":
        difficulty = "Difficult"
    elif color_difficulty == "dblack":
        difficulty = "Extremely Difficult"

    return difficulty


def seed_trails_into_db(api_response):
    """Take Hiking Project API response and seed trail data into database if

    trail does not already exist"""

    for trail in api_response["trails"]:
        trail_id = trail["id"]
        trail_name = trail["name"]
        length = trail["length"]
        difficulty = convert_trail_difficulty(trail["difficulty"])
        img_thumb_url = trail["imgSmall"]
        img_lg_url = trail["imgSmallMed"]
        long = trail["longitude"]
        lat = trail["latitude"]
        location = trail["location"].split(",")
        city = location[0]
        state = location[1][1:]
        description = trail["summary"]
        ascent = trail["ascent"]
        descent = trail["descent"]
        high_altitude = trail["high"]
        low_altitude = trail["low"]

        if not Trail.query.filter_by(trail_id=trail_id).all():
            new_trail = Trail(trail_id=trail_id, trail_name=trail_name,
                              length=length, difficulty=difficulty,
                              img_thumb_url=img_thumb_url,
                              img_lg_url=img_lg_url,
                              long=long, lat=lat, city=city, state=state,
                              description=description, ascent=ascent,
                              descent=descent, high_altitude=high_altitude,
                              low_altitude=low_altitude)

            db.session.add(new_trail)
            db.session.commit()


def delete_trip_users(trip_id):
    """Deletes all Trip_User instances associated with a given trip_id"""

    trip_users = Trip_User.query.filter_by(trip_id=trip_id).all()

    for tu in trip_users:
        db.session.delete(tu)

    db.session.commit()


def delete_trip_trails(trip_id):
    """Deletes all Trip_Trail instances associated with a given trip_id"""

    trip_trails = Trip_Trail.query.filter_by(trip_id=trip_id).all()

    for tt in trip_trails:
        db.session.delete(tt)

    db.session.commit()


def delete_trip_comments(trip_id):
    """Deletes all Trip_Comment instances associated with a given trip_id"""

    trip_comments = Trip_Comment.query.filter_by(trip_id=trip_id).all()

    for tc in trip_comments:
        db.session.delete(tc)

    db.session.commit()


def delete_trip(trip_id):
    """Deletes all Trip instances associated with a given trip_id"""
    trip = Trip.query.get(trip_id)

    flash_msg = f"{trip.trip_name} has been deleted"

    db.session.delete(trip)
    db.session.commit()

    return flash_msg
