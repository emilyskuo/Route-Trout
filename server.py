from flask import (Flask, render_template, redirect, request, flash, session,
                   jsonify)
from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension
import os

from model import (User, Trail, User_Trail, Trip, Trip_User,
                   Trip_Trail, db, connect_to_db)

from helperfunctions import (call_geocoding_api, call_hiking_project_api,
                             seed_trails_into_db, delete_trip_users,
                             delete_trip_trails, delete_trip)

HIKING_PROJECT_KEY = os.environ['HIKING_PROJECT_KEY']
MAPS_JS_KEY = os.environ['MAPS_JS_KEY']

app = Flask(__name__)


@app.route("/")
def index():
    """Display homepage"""

    return render_template("index.html")


# ~~~~~ ACCOUNT-RELATED ROUTES ~~~~~ #

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

    # Validate if username or email already exists in
    # the users table in database
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


# No direct hyperlink access here
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

    if "user_id" in session:
        user = User.query.get(session.get("user_id"))

        return render_template("/account-userinfo.html", user=user)

    else:
        flash("You need to be logged in to access that page")

        return redirect("/login")


@app.route("/account/updateacctinfo", methods=["POST"])
def update_account_info():
    """Update a user's account information"""

    if "user_id" in session:
        fname = request.form.get("fname")
        lname = request.form.get("lname")
        cell = request.form.get("cell")
        city = request.form.get("city")
        state = request.form.get("state")
        zipcode = request.form.get("zipcode")

        user = User.query.get(session["user_id"])

        # Form fields are not required - only update database if text was
        # entered in that field and not the same as what's already in the db
        if len(fname) > 0 and fname != user.fname:
            user.fname = fname

        if len(lname) > 0 and lname != user.lname:
            user.lname = lname

        if len(cell) > 0 and cell != user.cell:
            user.cell = cell

        if len(city) > 0 and city != user.city:
            user.city = city

        if len(state) > 0 and state != user.state:
            user.state = state

        if len(zipcode) > 0 and zipcode != user.zipcode:
            user.zipcode = zipcode

        db.session.add(user)
        db.session.commit()

        flash("Information updated!")

        return redirect("/account/updateacctinfo")

    else:
        flash("You need to be logged in to access that page")

        return redirect("/login")


@app.route("/account/changepassword")
def show_change_pass_form():
    """Show form for users to change their password"""

    if "user_id" in session:
        return render_template("account-changepass.html")

    else:
        flash("You need to be logged in to access that page")
        return redirect("/login")


@app.route("/account/changepassword", methods=["POST"])
def change_user_password():
    """Change a user's password"""

    if "user_id" in session:
        old_pass = request.form.get("oldpass")
        new_pass = request.form.get("newpass")

        user = User.query.get(session["user_id"])

        if user.check_password(old_pass):
            user.set_password(new_pass)

            db.session.add(user)
            db.session.commit()

            flash("Password successfully updated")

            return redirect("/account/changepassword")

        else:
            flash("Incorrect password, please try again")

            return redirect("/account/changepassword")

    else:
        flash("You need to be logged in to access that page")

        return redirect("/login")


@app.route("/account/savedtrails")
def display_saved_trails():
    """Display a user's saved trails"""

    # Query database to find User_trail objects belonging to user
    # & not marked complete
    if "user_id" in session:
        user_id = session.get("user_id")
        saved_trails = User_Trail.query.filter((User_Trail.user_id == user_id)
                                               & (User_Trail.is_completed.is_(False))).all()

        return render_template("account-savedlist.html",
                               saved_trails=saved_trails)

    else:
        flash("You need to be logged in to access that page")

        return redirect("/login")


@app.route("/account/completedtrails")
def display_completed_trails():
    """Display a user's completed trails"""

    # Query database to find User_trail objects belonging to user
    # & not marked complete
    if "user_id" in session:
        user_id = session.get("user_id")
        completed_trails = User_Trail.query.filter((User_Trail.user_id == user_id)
                                                   & (User_Trail.is_completed.is_(True))).all()

        return render_template("account-completedlist.html",
                               completed_trails=completed_trails)

    else:
        flash("You need to be logged in to access that page")

        return redirect("/login")


@app.route("/account/trips")
def display_user_trips():
    """Display a user's trips"""

    if "user_id" in session:
        user_id = session.get("user_id")
        user_trips = Trip_User.query.filter_by(user_id=user_id).all()

        active_trips = []
        archived_trips = []

        for ut in user_trips:
            if ut.trip.is_archived is True:
                archived_trips.append(ut)
            else:
                active_trips.append(ut)

        return render_template("account-trips.html", active_trips=active_trips,
                               archived_trips=archived_trips)

    else:
        flash("You need to be logged in to access that page")

        return redirect("/login")


@app.route("/logout")
def log_out_user():
    """Log out user"""

    if "user_id" in session:
        del session["user_id"]
        flash("Logged out")

    return redirect("/")


# ~~~~~ SEARCH-RELATED ROUTES ~~~~~ #

@app.route("/search")
def display_search_results():
    """Display search results"""

    return render_template("search.html", MAPS_JS_KEY=MAPS_JS_KEY)


# ~~~~~ TRAIL-RELATED ROUTES ~~~~~ #

@app.route("/trail/<int:trail_id>")
def display_trail_info(trail_id):
    """Display trail information page"""

    trail = Trail.query.get(trail_id)
    user_id = session.get("user_id")
    trips = []

    if user_id:
        trips = Trip_User.query.filter_by(user_id=user_id).all()

    return render_template("trail.html", trail=trail,
                           MAPS_JS_KEY=MAPS_JS_KEY, trips=trips)


# ~~~~~ TRIP-RELATED ROUTES ~~~~~ #

@app.route("/createnewtrip", methods=["GET"])
def show_new_trip_form():
    """Show form for user to create a new Trip instance"""

    if "user_id" in session:

        return render_template("createnewtrip.html")

    else:
        flash("You need to be logged in to access that page")

        return redirect("/login")


@app.route("/createnewtrip", methods=["POST"])
def create_new_trip():
    """Create a new Trip instance"""

    if "user_id" in session:
        trip_name = request.form.get("trip-name")
        accommodations = request.form.get("accommodations")
        creator_id = session.get("user_id")

        # Create new trip instance
        new_trip = Trip(trip_name=trip_name, creator_id=creator_id,
                        trip_accommodations=accommodations)

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
        user_id = session.get("user_id")
        new_tu = Trip_User(trip_id=new_trip.trip_id, user_id=user_id)

        db.session.add(new_tu)
        db.session.commit()

        return redirect(f"/trip/{new_trip.trip_id}")

    else:
        flash("You need to be logged in to access that page")

        return redirect("/login")


@app.route("/trip/<int:trip_id>")
def show_trip(trip_id):
    """Display Trip instance information"""

    trip = Trip.query.get(trip_id)
    all_users = User.query.all()

    return render_template("trip.html", trip=trip, all_users=all_users,
                           MAPS_JS_KEY=MAPS_JS_KEY)


@app.route("/trail/<trail_id>/addtotrip/<trip_id>")
def add_trail_to_trip(trail_id, trip_id):
    """Adds a Trail_Trip instance"""

    if "user_id" in session:
        tt_query = Trip_Trail.query.filter((Trip_Trail.trail_id == trail_id) &
                                        (Trip_Trail.trip_id == trip_id)).first()

        if not tt_query:
            user_id = session.get("user_id")
            tt = Trip_Trail(trail_id=trail_id, trip_id=trip_id,
                            added_by=user_id)

            db.session.add(tt)
            db.session.commit()

            flash("Trail added to trip!")

        else:
            flash("Trail added to trip!")

        return redirect(f"/trail/{trail_id}")

    else:
        flash("You need to be logged in to access that page")

        return redirect("/login")


# ~~~~~ AJAX REQUEST/JSON ROUTES ~~~~~ #

@app.route("/user/loggedin")
def is_user_logged_in():
    """Check if user is logged in"""

    if "user_id" in session:
        return "true"

    else:
        return "false"


@app.route("/json/search-coords")
def get_search_coordinates():
    """Call Google Maps Geocoding API with search terms & return json

    of coordinates"""

    search_terms = request.args.get("search")
    lat_long = call_geocoding_api(search_terms)

    if lat_long != "Invalid search terms":
        return jsonify(lat_long)

    else:
        return "Invalid search terms"


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

        saved_trail = User_Trail(user_id=session["user_id"], trail_id=trail_id)

        db.session.add(saved_trail)
        db.session.commit()

        return "Trail added"

    else:
        return "You must sign in to save trails"


@app.route("/user/unsave-trail", methods=["POST"])
def unsave_trail_to_user_list():
    """Remove a User-Trail instance"""

    trail_id = request.form.get("trail_id")

    if "user_id" in session:
        user_id = session.get("user_id")
        trail_to_delete = User_Trail.query.filter((User_Trail.user_id == user_id)
                                                  & (User_Trail.trail_id == trail_id)).first()

        db.session.delete(trail_to_delete)
        db.session.commit()

        return "Trail removed"

    else:
        return "You must sign in to edit saved trails"


@app.route("/user/complete-trail", methods=["POST"])
def mark_saved_trail_as_complete():
    """Update a User-Trail's is_completed attribute to True"""

    if "user_id" in session:
        trail_id = int(request.form.get("trail_id"))
        user_id = session["user_id"]

        saved_trail = User_Trail.query.filter((User_Trail.user_id == user_id)
                                              & (User_Trail.trail_id == trail_id)).first()

        if saved_trail:
            saved_trail.is_completed = True

            db.session.add(saved_trail)
            db.session.commit()

        else:
            saved_trail = User_Trail(user_id=user_id, trail_id=trail_id,
                                     is_completed=True)

            db.session.add(saved_trail)
            db.session.commit()

        return "Trail marked as complete"

    else:
        return "You must be signed in to save trails"


@app.route("/user/uncomplete-trail", methods=["POST"])
def unmark_saved_trail_as_complete():
    """Update a User-Trail's is_completed attribute to False"""

    if "user_id" in session:

        trail_id = int(request.form.get("trail_id"))

        saved_trail = User_Trail.query.filter((User_Trail.user_id == session["user_id"])
                                              & (User_Trail.trail_id == trail_id)).first()

        saved_trail.is_completed = False

        db.session.add(saved_trail)
        db.session.commit()

        return "Trail unmarked as complete"


@app.route("/user/is-trail-saved/<trail_id>")
def check_if_trail_saved_for_user(trail_id):
    """For a given user, check if a trail is saved in user_trails"""

    user_id = session.get("user_id")

    if user_id:
        ut = User_Trail.query.filter((User_Trail.user_id == user_id) &
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


@app.route("/json/getallusertrips")
def get_users_trips():
    """Gets all trips associated with a given user"""

    user_id = session.get("user_id")

    all_tu = Trip_User.query.filter_by(user_id=user_id).all()

    if all_tu:
        tu_dict = {}

        for tu in all_tu:
            if tu.trip.is_archived is False:
                tu_dict[tu.trip_id] = {
                    "trip_name": tu.trip.trip_name,
                    "trip_lat": tu.trip.accom_lat,
                    "trip_lng": tu.trip.accom_long,
                    "trip_id": tu.trip_id
                }

        return jsonify(tu_dict)
    
    else:
        return "none"


@app.route("/json/gettriptrailinfo")
def get_trip_trail_info():
    """Gets trip_trail information associated with a given trip"""

    trip_id = request.args.get("trip_id")

    all_tt = Trip_Trail.query.filter_by(trip_id=trip_id).all()

    if not all_tt:
        return "No tt here"

    tt_dict = {}

    for tt in all_tt:
        tt_dict[tt.trail_id] = {
            "trail_name": tt.trail.trail_name,
            "trail_lat": tt.trail.lat,
            "trail_lng": tt.trail.long,
            "trail_id": tt.trail_id,
            "trip_id": tt.trip_id,
            "trip_name": tt.trip.trip_name,
        }

    return jsonify(tt_dict)


@app.route("/json/tripinfo")
def get_trip_info():
    """Return JSON of trip coordinates & accom address"""

    trip_id = request.args.get("trip_id")

    trip = Trip.query.get(trip_id)

    trip_trails = []

    for trip_trail in trip.trip_trails:
        trip_trails.append({
            "trail_id": trip_trail.trail_id,
            "trail_name": trip_trail.trail.trail_name,
            "trail_lat_long": {
                "lat": trip_trail.trail.lat,
                "lng": trip_trail.trail.long,
                }
        })

    lat_long = {
        "lat": trip.accom_lat,
        "lng": trip.accom_long}

    response = {
        "lat_long": lat_long,
        "accom_text": trip.trip_accommodations,
        "trip_trails": trip_trails,
    }

    return jsonify(response)


@app.route("/deletetrip", methods=["POST"])
def delete_a_trip():
    """Deletes trip from database"""

    if "user_id" in session:
        trip_id = request.form.get("trip_id")

        delete_trip_users(trip_id)
        delete_trip_trails(trip_id)
        flash_msg = delete_trip(trip_id)

        flash(flash_msg)

        return redirect("/account/trips")

    else:
        return "You need to be logged in to access that page"


@app.route("/istriparchived")
def check_if_trip_archived():
    """Checks whether a trip's is_archived attribute is True or False"""

    trip_id = request.args.get("trip_id")

    trip = Trip.query.get(trip_id)

    if trip.is_archived:
        return "true"

    else:
        return "false"


@app.route("/archivetrip", methods=["POST"])
def archive_a_trip():
    """Archive's a trip in database"""

    if "user_id" in session:
        trip_id = request.form.get("trip_id")
        trip = Trip.query.get(trip_id)
        trip.is_archived = True

        db.session.add(trip)
        db.session.commit()

        return "Successfully archived"

    else:
        return "You need to be logged in to access that page"


@app.route("/unarchivetrip", methods=["POST"])
def unarchive_a_trip():
    """Unarchive's a trip in database"""

    if "user_id" in session:
        trip_id = request.form.get("trip_id")
        trip = Trip.query.get(trip_id)
        trip.is_archived = False

        db.session.add(trip)
        db.session.commit()

        return "Successfully unarchived"

    else:
        return "You need to be logged in to access that page"


@app.route("/updatetripname", methods=["POST"])
def update_trip_name():
    """Update the name for a given trip"""

    if "user_id" in session:
        trip_id = request.form.get("trip_id")
        trip_name = request.form.get("trip_name")

        trip = Trip.query.get(trip_id)

        if trip:
            trip.trip_name = trip_name

            db.session.add(trip)
            db.session.commit()

            return trip_name

        else:
            return "An error has occurred"

    else:
        return "You need to be logged in to access that page"


@app.route("/updatetripaccoms", methods=["POST"])
def update_trip_accommodations():
    """Update the accommodations & associated lat/long for a given trip"""

    if "user_id" in session:
        trip_id = request.form.get("trip_id")
        trip_accom = request.form.get("trip_accom")

        trip = Trip.query.get(trip_id)

        trip.trip_accommodations = trip_accom
        lat_long = call_geocoding_api(trip_accom)

        if lat_long != "Invalid search terms":
            trip.accom_long = lat_long["lng"]
            trip.accom_lat = lat_long["lat"]

            db.session.add(trip)
            db.session.commit()

            return f"{trip_accom}"

        else:
            return "Address could not be read"

    else:
        return "You need to be logged in to access that page"


@app.route("/addtripusers", methods=["POST"])
def add_trip_users():
    """Add Trip_User instances"""

    if "user_id" in session:
        trip_id = int(request.form.get("trip_id"))
        user_id = int(request.form.get("user_id"))
        tu_query = Trip_User.query.filter((Trip_User.user_id == user_id) &
                                        (Trip_User.trip_id == trip_id)).first()

        if tu_query:
            return "User already added to trip"

        else:
            tu = Trip_User(trip_id=trip_id, user_id=user_id)

            db.session.add(tu)
            db.session.commit()

            username = tu.user.username

            return username

    else:
        return "You need to be logged in to access that page"


@app.route("/removetripusers", methods=["POST"])
def remove_trip_users():
    """Remove Trip_User instances"""

    if "user_id" in session:
        trip_id = int(request.form.get("trip_id"))
        user_id = int(request.form.get("user_id"))
        tu = Trip_User.query.filter((Trip_User.user_id == user_id) &
                                    (Trip_User.trip_id == trip_id)).first()

        if tu:
            username = tu.user.username
            db.session.delete(tu)
            db.session.commit()

            return username

        else:
            return "An error has occurred"

    else:
        return "You need to be logged in to access that page"


@app.route("/removetriptrails", methods=["POST"])
def remove_trip_trail():
    """Removes a Trail_Trip instance"""

    if "user_id" in session:
        trip_id = request.form.get("trip_id")
        trail_id = request.form.get("trail_id")
        tt_query = Trip_Trail.query.filter((Trip_Trail.trail_id == trail_id) &
                                        (Trip_Trail.trip_id == trip_id)).first()

        if tt_query:

            db.session.delete(tt_query)
            db.session.commit()

            return str(trail_id)

        else:
            return "An error has occurred"

    else:
        return "You need to be logged in to access that page"


connect_to_db(app)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # For getting error messages in Jinja when variables are undefined
    app.jinja_env.undefined = StrictUndefined
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run()
