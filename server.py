from flask import (Flask, render_template, redirect, request, flash, session,
                   jsonify)
from flask_sqlalchemy import SQLAlchemy
from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension
import requests
import os
from datetime import datetime

from model import (User, Trail, User_Trail, Trip, Trip_User,
                   Trip_Trail, Trip_Comment, db, connect_to_db)

from helperfunctions import (call_geocoding_api, call_hiking_project_api,
                             seed_trails_into_db, delete_trip_users,
                             delete_trip_trails, delete_trip_comments,
                             delete_trip)

GOOGLE_MAPS_KEY = os.environ['GOOGLE_MAPS_KEY']
HIKING_PROJECT_KEY = os.environ['HIKING_PROJECT_KEY']

app = Flask(__name__)

app.secret_key = "supersecret"

# For getting error messages in Jinja when variables are undefined
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def index():
    """Display homepage"""

    return render_template("index.html")


# ~~~~~ ACCOUNT-RELATED ROUTES - registration, login, account info, logout ~~~~~ #

@app.route("/register")
def reg_form():
    """Display registration form"""

    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register_user():
    """Creates new user if user does not yet exist"""

    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

# Validate if username or email already exists in the users table in database
    if not User.query.filter((User.email == email) |
                             (User.username == username)).all():

        user = User(username=username, email=email)

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("User created!")

        return redirect("/login")

# If one does exist, flash message to indicate if email or username
    else:
        if User.query.filter_by(email=email).all():
            flash(f"There's already an account associated with {email}")
        else:
            flash(f"The username {username} is already taken")

        return redirect("/register")


@app.route("/login")
def show_login_form():
    """Display login form"""

    return render_template("login.html")


@app.route("/login", methods=["POST"])
def log_in_user():
    """Validate user login"""

    username = request.form.get("username")
    password = request.form.get("password")

    # Validate that user's username exists in database
    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        session["user_id"] = user.user_id
        flash("Login successful")

        return redirect("/")

    else:
        flash("Incorrect login information")
        return redirect("/login")


@app.route("/account")
def show_account_options():
    """Display account options for logged in users"""

    if "user_id" in session:

        return render_template("account.html")

    else:
        flash("You need to be logged in to access that page")

        return redirect("/login")


@app.route("/account/updateacctinfo")
def show_acct_info_form():
    """Display form for user to update account information"""

    return render_template("/account-userinfo.html")


@app.route("/account/updateacctinfo", methods=["POST"])
def update_account_info():
    """Update a user's account information"""

    fname = request.form.get("fname")
    lname = request.form.get("lname")
    cell = request.form.get("cell")
    city = request.form.get("city")
    state = request.form.get("state")
    zipcode = request.form.get("zipcode")

    user = User.query.get(session["user_id"])

    # Form fields are not required - only update database if text was entered
    # in that field
    if len(fname) > 0:
        user.fname = fname

    if len(lname) > 0:
        user.lname = lname

    if len(cell) > 0:
        user.cell = cell

    if len(city) > 0:
        user.city = city

    if len(state) > 0:
        user.state = state

    if len(zipcode) > 0:
        user.zipcode = zipcode

    db.session.add(user)
    db.session.commit()

    flash("Information updated!")

    return redirect("/account")


@app.route("/account/changepassword")
def show_change_pass_form():

    return render_template("account-changepass.html")


@app.route("/account/changepassword", methods=["POST"])
def change_user_password():
    """Change a user's password"""

    old_pass = request.form.get("oldpass")
    new_pass = request.form.get("newpass")

    user = User.query.get(session["user_id"])

    if user.check_password(old_pass):
        user.set_password(new_pass)

        db.session.add(user)
        db.session.commit()

        flash("Password successfully updated")

        return redirect("/account")

    else:
        flash("Incorrect password, please try again")

        return redirect("/account")


@app.route("/account/savedtrails")
def display_saved_trails():
    """Display a user's saved trails"""

    # Query database to find User_trail objects belonging to user
    # & not marked complete
    saved_trails = User_Trail.query.filter((User_Trail.user_id == session["user_id"])
                                           & (User_Trail.is_completed.is_(False))).all()

    return render_template("account-savedlist.html", saved_trails=saved_trails)


@app.route("/account/completedtrails")
def display_completed_trails():
    """Display a user's completed trails"""

    # Query database to find User_trail objects belonging to user
    # & not marked complete
    completed_trails = User_Trail.query.filter((User_Trail.user_id == session["user_id"])
                                               & (User_Trail.is_completed.is_(True))).all()

    return render_template("account-completedlist.html",
                           completed_trails=completed_trails)


@app.route("/account/trips")
def display_user_trips():
    """Display a user's trips"""

    user_trips = Trip_User.query.filter_by(user_id=session["user_id"]).all()

    return render_template("account-trips.html", user_trips=user_trips)


@app.route("/logout")
def log_out_user():
    """Log out user"""

    if "user_id" in session:
        del session["user_id"]
        flash("Logged out")

    return redirect("/")


@app.route("/user/loggedin")
def is_user_logged_in():
    """Check if user is logged in"""

    if "user_id" in session:
        return "true"

    else:
        return "false"


# ~~~~~ SEARCH-RELATED ROUTES ~~~~~ #

@app.route("/search")
def display_search_results():
    """Display search results"""

    return render_template("search.html", GOOGLE_MAPS_KEY=GOOGLE_MAPS_KEY)


@app.route("/json/search-coords")
def get_search_coordinates():
    """Call Google Maps Geocoding API with search terms & return json

    of coordinates"""

    search_terms = request.args.get("search")
    lat_long = call_geocoding_api(search_terms)

    return jsonify(lat_long)


@app.route("/json/search")
def return_json_search_results():
    """Search for trails given a location, seed trails into database, and

    return json response"""

    search_terms = request.args.get("search")
    lat_long = call_geocoding_api(search_terms)

    if lat_long != "Invalid search terms":
        response = call_hiking_project_api(lat_long)
        seed_trails_into_db(response)

        json_response = jsonify(response["trails"])

        return json_response

    else:
        return "Invalid search terms"


# ~~~~~ TRAIL-RELATED ROUTES ~~~~~ #

@app.route("/trail/<int:trail_id>")
def display_trail_info(trail_id):
    """Display trail information page"""

    trail = Trail.query.get(trail_id)
    trips = Trip_User.query.filter_by(user_id=session["user_id"]).all()

    print(trips)

    return render_template("trail.html", trail=trail,
                           GOOGLE_MAPS_KEY=GOOGLE_MAPS_KEY, trips=trips)


@app.route("/json/latlongbyid/<trail_id>")
def get_lat_long_by_trail_id(trail_id):
    """Return json lat/long coordinates of a trail given its trail id"""

    trail = Trail.query.get(trail_id)
    lat = trail.lat
    long = trail.long

    lat_long = {
        "lat": lat,
        "lng": long
    }

    return jsonify(lat_long)


@app.route("/user/save-trail", methods=["POST"])
def save_trail_to_user_list():
    """Instantiate a User-Trail instance"""

    if "user_id" in session:
        trail_id = request.form.get("trail_id")
        date_added = datetime.now()

        saved_trail = User_Trail(user_id=session["user_id"], trail_id=trail_id,
                                 date_added=date_added)

        db.session.add(saved_trail)
        db.session.commit()

        return "Trail added"

    else:
        return "You must sign in to save trails"


@app.route("/user/unsave-trail", methods=["POST"])
def unsave_trail_to_user_list():
    """Remove a User-Trail instance"""

    trail_id = request.form.get("trail_id")
    trail_to_delete = User_Trail.query.filter((User_Trail.user_id == session["user_id"])
                                              & (User_Trail.trail_id == trail_id)).first()

    db.session.delete(trail_to_delete)
    db.session.commit()

    return "Trail removed"


@app.route("/user/complete-trail", methods=["POST"])
def mark_saved_trail_as_complete():
    """Update a User-Trail's is_completed attribute to True"""

    if "user_id" in session:
        user_id = session["user_id"]
        trail_id = int(request.form.get("trail_id"))

        saved_trail = User_Trail.query.filter((User_Trail.user_id == user_id)
                                              & (User_Trail.trail_id == trail_id)).first()

        if saved_trail:
            saved_trail.is_completed = True

            db.session.add(saved_trail)
            db.session.commit()

        else:

            date_added = datetime.now()
            saved_trail = User_Trail(user_id=user_id, trail_id=trail_id,
                                     date_added=date_added, is_completed=True)

            db.session.add(saved_trail)
            db.session.commit()

        return "Trail marked as complete"

    else:
        return "You must be signed in to save trails"


@app.route("/user/uncomplete-trail", methods=["POST"])
def unmark_saved_trail_as_complete():
    """Update a User-Trail's is_completed attribute to False"""

    user_id = session["user_id"]
    trail_id = int(request.form.get("trail_id"))

    saved_trail = User_Trail.query.filter((User_Trail.user_id == user_id)
                                          & (User_Trail.trail_id == trail_id)).first()

    saved_trail.is_completed = False

    db.session.add(saved_trail)
    db.session.commit()

    return "Trail unmarked as complete"


@app.route("/user/is-trail-saved/<trail_id>")
def check_if_trail_saved_for_user(trail_id):
    """For a given user, check if a trail is saved in user_trails"""

    ut = User_Trail.query.filter((User_Trail.user_id == session["user_id"]) &
                                 (User_Trail.trail_id == trail_id)).first()

    response = {}

    if ut:
        response["saved"] = True
        if ut.is_completed:
            response["completed"] = True
        else:
            response["completed"] = False
    else:
        response["saved"] = False
        response["completed"] = False

    return jsonify(response)


# ~~~~~ TRIP-RELATED ROUTES ~~~~~ #

@app.route("/createnewtrip", methods=["GET"])
def show_new_trip_form():
    """Show form for user to create a new Trip instance"""

    return render_template("createnewtrip.html")


@app.route("/createnewtrip", methods=["POST"])
def create_new_trip():
    """Create a new Trip instance"""

    trip_name = request.form.get("trip-name")
    accommodations = request.form.get("accommodations")
    trip_start_date = request.form.get("start-date")
    trip_end_date = request.form.get("end-date")
    creator_id = session.get("user_id")

    # Create new trip instance
    new_trip = Trip(trip_name=trip_name, creator_id=creator_id,
                    trip_accommodations=accommodations,
                    trip_start_date=trip_start_date,
                    trip_end_date=trip_end_date)

    # If accommodations field was filled in, find the lat/long
    # and add the values to new_trip
    if accommodations:
        lat_long = call_geocoding_api(accommodations)
        if lat_long != "Invalid search terms":
            accomm_long = lat_long["lng"]
            accomm_lat = lat_long["lat"]

            new_trip.accom_lat = accomm_lat
            new_trip.accom_long = accomm_long

    db.session.add(new_trip)
    db.session.commit()

    # Add Trip_User instance for creator of the trip upon creation of the trip
    new_tu = Trip_User(trip_id=new_trip.trip_id, user_id=session["user_id"],
                       date_joined=datetime.now())

    db.session.add(new_tu)
    db.session.commit()

    return redirect(f"/trip/{new_trip.trip_id}")


@app.route("/trip/<int:trip_id>")
def show_trip(trip_id):
    """Display Trip instance information"""

    trip = Trip.query.get(trip_id)
    all_users = User.query.all()

    return render_template("trip.html", trip=trip, all_users=all_users,
                           GOOGLE_MAPS_KEY=GOOGLE_MAPS_KEY)


@app.route("/trail/<trail_id>/addtotrip/<trip_id>")
def add_trail_to_trip(trail_id, trip_id):
    """Adds a Trail_Trip instance"""

    tt_query = Trip_Trail.query.filter((Trip_Trail.trail_id == trail_id) &
                                       (Trip_Trail.trip_id == trip_id)).first()

    if not tt_query:
        tt = Trip_Trail(trail_id=trail_id, trip_id=trip_id,
                        added_by=session["user_id"], date_added=datetime.now())

        db.session.add(tt)
        db.session.commit()

        flash("Trail added to trip!")

    else:
        flash("Trail added to trip!")

    return redirect(f"/trail/{trail_id}")


@app.route("/json/tripinfo")
def get_trip_info():
    """Return JSON of trip coordinates & accom address"""

    trip_id = request.args.get("trip_id")

    trip = Trip.query.get(trip_id)

    lat_long = {
        "lat": trip.accom_lat,
        "lng": trip.accom_long}

    response = {
        "lat_long": lat_long,
        "accom_text": trip.trip_accommodations
    }

    return jsonify(response)


@app.route("/deletetrip/<trip_id>")
def delete_a_trip(trip_id):
    """Deletes trip from database"""

    delete_trip_users(trip_id)
    delete_trip_trails(trip_id)
    delete_trip_comments(trip_id)
    flash_msg = delete_trip(trip_id)

    flash(flash_msg)

    return redirect("/account/trips")


@app.route("/trip/user/getallusertrips")
def get_users_trips():
    """Gets all trips associated with a given user"""

    all_tu = Trip_User.query.filter_by(user_id=session["user_id"]).all()

    tu_dict = {}

    for tu in all_tu:
        if tu.trip.is_archived is False:
            tu_dict[tu.trip_id] = {
                "trip_name": tu.trip.trip_name,
                "trip_lat": tu.trip.accom_lat,
                "trip_lng": tu.trip.accom_long,
                "trip_trails": {
                    "list_trails": tu.trip.trip_trails
                }
            }
            print(tu_dict)
            for tt in tu.trip.trip_trails:
                tu_dict["trip_trails"][tt.trail.trail_id] = {
                    "trail_name": tt.trail.trail_name,
                    "trail_long": tt.trail.long,
                    "trail_lat": tt.trail.lat,
                    "trail_id": tt.trail.trail_id
                }

    return jsonify(tu_dict)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
