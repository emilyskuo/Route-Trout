import requests
import os

from model import Trail, db


GOOGLE_MAPS_KEY = os.environ['GOOGLE_MAPS_KEY']
HIKING_PROJECT_KEY = os.environ['HIKING_PROJECT_KEY']


def call_geocoding_api(search_terms):
    """Query Google Maps Geocoding API to convert search terms to long/lat coordinates"""

    api_url = "https://maps.googleapis.com/maps/api/geocode/json"
    payload = {
        "address": search_terms,
        "key": GOOGLE_MAPS_KEY
    }

    r = requests.get(api_url, params=payload)
    response = r.json()

    if "error_message" not in response:
        lat_long = response["results"][0]["geometry"]["location"]

        return lat_long

    else:
        return "Invalid search terms"


def call_hiking_project_api(lat_long):
    """Query Hiking Project API to retrieve trail list given lat/long coordinates"""

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


def seed_trails_into_db(api_response):
    """Take Hiking Project API response and seed trail data into database"""

    trail_list = []

    for trail in api_response["trails"]:
        trail_id = trail["id"]
        trail_name = trail["name"]
        length = trail["length"]
        difficulty = trail["difficulty"]
        img_thumb_url = trail["imgSmall"]
        img_lg_url = trail["imgSmallMed"]
        long = trail["longitude"]
        lat = trail["latitude"]
        location = trail["location"].split(",")
        city = location[0]
        state = location[1][1:]
        description = trail["summary"]

        if not Trail.query.filter_by(trail_id=trail_id).all():
            new_trail = Trail(trail_id=trail_id, trail_name=trail_name,
                              length=length, difficulty=difficulty,
                              img_thumb_url=img_thumb_url, img_lg_url=img_lg_url,
                              long=long, lat=lat, city=city, state=state,
                              description=description)

            trail_list.append(new_trail)

            db.session.add(new_trail)
            db.session.commit()

        else:
            trail_list.append(Trail.query.get(trail_id))

    return trail_list
