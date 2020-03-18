## ![Route Trout logo](https://user-images.githubusercontent.com/58803587/76805145-4e54e600-679b-11ea-9c78-8c5677de99d3.png "Route Trout")
# Route Trout

Route Trout is a resource for hikers to search for trails and plan hiking trips. Users can search for trails by location, and see the search results displayed in a list and a map. Registered users' passwords are kept secure with bcrypt, a tool that adds unique salts to each password prior to hashing.  Logged in users can add trails to their saved or completed lists, and also plan hiking trips. The Trips feature is designed to help people plan hiking trips by mapping out where they're staying, what trails are nearby, and which trails they plan to hike during that trip.

**Contents**
- [Tech Stack](#tech-stack)
- [Features](#features)
- [Future Features](#future-features)
- [Installation](#installation)
- [About the Developer](#about-the-developer)

## Tech Stack

**Backend:** Python 3, PostgreSQL, Flask, SQLAlchemy, Jinja, bcrypt

**Frontend:** JavaScript, jQuery, HTML 5, CSS 3, Bootstrap, Select 2

**APIs:** Google Maps Geocoding, Google Maps JavaScript, Hiking Project

**Deployment:** Google Cloud Platform, Cloudflare, Apache2

## Features

**Seach for hiking trails**

To search for trails, users input a location, which is converted into coordinates using the Google Maps Geocoding API which are then sent to the Hiking Project API. The resulting JSON response is parsed & seeding into the database, and displayed as cards & mapped out. The cards are populated using JavaScript and jQuery, and formatted using Bootstrap. Each card has mouseenter and mouseleave event listeners that manipulate the animation attribute on each map marker to associate a trail with its location. The map markers all have an info window and zoom action when clicked. Closing the info window reverses the zoom.

![Search for trails](https://user-images.githubusercontent.com/58803587/76893349-70a53d00-6849-11ea-9c20-3c328d695a2a.gif "Search for hiking trails")

**Add trails to saved or completed lists**

On each trail page, there are buttons so that logged in users can easily save trails for future outings or mark already-hiked trails as completed. Each button click submits an AJAX request to the server to update the database accordingly.

![Save Trails](https://user-images.githubusercontent.com/58803587/76901133-e1535600-6857-11ea-921a-90676eec85f3.gif "Mark trails saved or completed")

**Plan hiking trips**

One of they key features on Route Trout is trip planning. Users can create trips to keep track of where they're staying, where they plan to hike, and other users involved. Once a trip is created, a separate layer of map markers appears on the search results page to visualize the trip. These trip markers are easily toggled off or on using the "hide" or "show" buttons at the bottom of the map.

![Trips](https://user-images.githubusercontent.com/58803587/76902715-d4cffd00-6859-11ea-88f5-0125ed62e983.gif "Plan hiking trips")

**Password security**

All passwords are uniquely salted prior to hashing using the Python bcrypt library. This ensures that every hashed password stored in the database is unique.

## Future Features

- Display a user's recently viewed trails
- Implement discussions within trips
- Friendships between users

## Installation

**Prerequisites**

To run Route Trout, you will need API keys for [Google Maps Geocoding](https://developers.google.com/maps/documentation/geocoding/start), [Google Maps JavaScript](https://developers.google.com/maps/documentation/javascript/tutorial), and the [Hiking Project](https://www.hikingproject.com/data). Python 3 and PostgreSQL also need to be installed on your machine.

**Running Route Trout on your machine**

Clone this repository
```
$ git clone https://github.com/emilyskuo/Route-Trout.git
```
Optional: Create and activate a virtual environment using virtualenv
```
$ pip3 install virtualenv
$ virtualenv env
$ source env/bin/activate
```
Install dependencies from requirements.txt
```
$ pip3 install -r requirements.txt
```
Create environmental variables to hold your API keys
```
$ export MAPS_GEOCODING_KEY='{YOUR GEOCODING API KEY HERE}'
$ export MAPS_JS_KEY='{YOUR MAPS JS API KEY HERE}'
$ export HIKING_PROJECT_KEY='{YOUR HIKING PROJECT API KEY HERE}'
```
Create your database & seed sample data
```
$ createdb hikingapp
$ python3 seed.py
```
Run the app on localhost
```
$ python3 server.py
```

## About the Developer

Emily Kuo is a software engineer in the San Francisco Bay Area, and previously worked as an Account Director in the pharmaceutical advertising industry. Her love of hiking & planning trips led her to build Route Trout as her capstone project at Hackbright Academy.