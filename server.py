from flask import (Flask, render_template, redirect, request, flash, session,
                   jsonify)
from flask_sqlalchemy import SQLAlchemy
from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension
import requests
import os
from datetime import datetime

from model import User, Trail, User_Trail, db, connect_to_db
from helperfunctions import (call_geocoding_api, call_hiking_project_api,
                             seed_trails_into_db)

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

        user = User(username=username, email=email, password=password)

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

    # Validate that user's username and password match database
    user = User.query.filter((User.username == username) &
                             (User.password == password)).first()
    if user:
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

        saved_trails = User_Trail.query.filter((User_Trail.user_id == session["user_id"])
                                               & (User_Trail.is_completed == False)).all()

        completed_trails = User_Trail.query.filter((User_Trail.user_id == session["user_id"])
                                                   & (User_Trail.is_completed == True)).all()
        return render_template("account.html", saved_trails=saved_trails,
                               completed_trails=completed_trails)

    else:
        flash("You need to be logged in to access that page")
        return redirect("/login")


@app.route("/account", methods=["POST"])
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


@app.route("/search")
def display_search_results():
    """Display search results"""

    return render_template("search.html", GOOGLE_MAPS_KEY=GOOGLE_MAPS_KEY)


# modularize API calls, maybe put them in a helper functions file,
# call them here, and serve them as json
# then use ajax requests to update data on client side

@app.route("/json/search-coords")
def get_search_coordinates():
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


@app.route("/trail/<int:trail_id>")
def display_trail_info(trail_id):
    """Display trail information page"""

    trail = Trail.query.get(trail_id)

    return render_template("trail.html", trail=trail,
                           GOOGLE_MAPS_KEY=GOOGLE_MAPS_KEY)


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

        print(saved_trail)

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

    print(saved_trail)

    saved_trail.is_completed = False

    db.session.add(saved_trail)
    db.session.commit()

    return "Trail unmarked as complete"


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
