import os
os.environ["MAPS_GEOCODING_KEY"] = "MAPS_GEOCODING_KEY"
os.environ["HIKING_PROJECT_KEY"] = "HIKING_PROJECT_KEY"

import helperfunctions
import unittest
import responses
import json


maps_api_response = {'results': [{'geometry': {'location': {'lat': 37.7749295, 'lng': -122.4194155}}}]}

geocoding_search_terms = "san francisco"

geocoding_api_url = "https://maps.googleapis.com/maps/api/geocode/json"
geocoding_api_payload = {
    "address": geocoding_search_terms,
    "key": "MAPS_GEOCODING_KEY"
}

maps_api_response_fail = {}

class TestHelperFunctions(unittest.TestCase):
    """TestCase for helperfunctions.py."""

    @responses.activate
    def test_call_geocoding_api(self):
        """An single test."""

        responses.add(responses.GET, geocoding_api_url, body=json.dumps(maps_api_response),
                      status=200, content_type="application/json")
        
        response = helperfunctions.call_geocoding_api(geocoding_search_terms)

        self.assertEqual(response, {'lat': 37.7749295, 'lng': -122.4194155})

    
    @responses.activate
    def test_call_geocoding_api_fail(self):
        """An single test."""

        responses.add(responses.GET, geocoding_api_url, body=json.dumps(maps_api_response_fail),
                      status=200, content_type="application/json")
        
        response = helperfunctions.call_geocoding_api(geocoding_search_terms)

        self.assertEqual(response, "Invalid search terms")



    """def call_geocoding_api(search_terms):
    '''Query Google Maps Geocoding API to convert search terms to

    long/lat coordinates'''

    api_url = "https://maps.googleapis.com/maps/api/geocode/json"
    payload = {
        "address": search_terms,
        "key": MAPS_GEOCODING_KEY
    }

    r = requests.get(api_url, params=payload)
    response = r.json()

    print(response)

    # Check to see if search was valid
    if response.get("results"):
        lat_long = response["results"][0]["geometry"]["location"]
        return lat_long

    # Return error message if message invalid
    else:
        return "Invalid search terms"
    
    """

    @unittest.mock.patch("helperfunctions.db")
    @unittest.mock.patch("helperfunctions.Trip_User")
    def test_delete_trip_users(self, fake_Trip_User, fake_db):

        Trip_User = unittest.mock.Mock()
        fake_Trip_User.query.filter_by.return_value.all.return_value = [Trip_User]

        helperfunctions.delete_trip_users(1)
        
        print(fake_Trip_User.mock_calls)
        fake_Trip_User.query.filter_by.assert_called()
        fake_db.session.delete.assert_called_with(Trip_User)
        fake_db.session.commit.assert_called()



'''def delete_trip_users(trip_id):
    """Deletes all Trip_User instances associated with a given trip_id"""

    trip_users = Trip_User.query.filter_by(trip_id=trip_id).all()

    for tu in trip_users:
        db.session.delete(tu)

    db.session.commit()'''

if __name__ == "__main__":
    unittest.main()