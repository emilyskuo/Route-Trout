from flask import (Flask, render_template, redirect, request, flash, session)
from flask_sqlalchemy import flask_sqlalchemy
from jinja2 import StrictUndefined
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Trail, User_Trail, db, connect_to_db

app = Flask(__name__)

app.secret_key = "supersecret"

# For getting error messages in Jinja when variables are undefined
app.jinja_env.undefined = StrictUndefined



