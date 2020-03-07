"""Create database classes & tables for hiking trails app"""

from flask_sqlalchemy import SQLAlchemy
import bcrypt

db = SQLAlchemy()


class User(db.Model):
    """Users of hiking app"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password_hash = db.Column(db.Binary(128))
    fname = db.Column(db.String(50))
    lname = db.Column(db.String(50))
    cell = db.Column(db.String(15))
    city = db.Column(db.String(50))
    state = db.Column(db.String(2))
    zipcode = db.Column(db.String(5))

    def __repr__(self):
        """Define representation of user objects"""

        return f"<User id={self.user_id}, username={self.username}>"

    def set_password(self, password):
        """Generate hash for users' passwords"""

        self.password_hash = bcrypt.hashpw(password.encode("utf-8"),
                                           bcrypt.gensalt(15))

    def check_password(self, password):
        """Check if password matches with password hash"""

        password = password.encode("utf-8")

        return bcrypt.checkpw(password, self.password_hash)


class Trail(db.Model):
    """Hiking trails for hiking app"""

    __tablename__ = "trails"

    trail_id = db.Column(db.Integer, primary_key=True)
    # Trail ids will be saved from Hiking Project API
    trail_name = db.Column(db.String(200), nullable=False)
    length = db.Column(db.Float)
    difficulty = db.Column(db.String(50))
    img_thumb_url = db.Column(db.String(200))
    img_lg_url = db.Column(db.String(200))
    long = db.Column(db.Float)
    lat = db.Column(db.Float)
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    description = db.Column(db.String(200))
    ascent = db.Column(db.Float)
    descent = db.Column(db.Float)
    high_altitude = db.Column(db.Float)
    low_altitude = db.Column(db.Float)

    def __repr__(self):
        """Define representation of trail objects"""

        return f"<Trail id={self.trail_id}, name={self.trail_name}>"


class User_Trail(db.Model):
    """Users' saved trails for hiking app.

    Association table between Users and Trails"""

    __tablename__ = "user_trails"
    ut_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"),
                        nullable=False)
    trail_id = db.Column(db.Integer, db.ForeignKey("trails.trail_id"),
                         nullable=False)
    is_completed = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref='user_trails')
    trail = db.relationship('Trail', backref='user_trails')

    def __repr__(self):
        """Define representation of user-trail objects"""

        return f"<UT id={self.ut_id}, user_id={self.user_id}, trail_id={self.trail_id}>"


class Trip(db.Model):
    """Trip data for users' trips"""

    __tablename__ = "trips"

    trip_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trip_name = db.Column(db.String(100), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey("users.user_id"),
                           nullable=False)
    trip_accommodations = db.Column(db.String(255))
    accom_long = db.Column(db.Float)
    accom_lat = db.Column(db.Float)
    is_archived = db.Column(db.Boolean, default=False)

    def __repr__(self):
        """Define representation of trip objects"""

        return f"<Trip name={self.trip_name}>"


class Trip_User(db.Model):
    """Users associated with a given trip.

    Association table between User and Trip tables"""

    __tablename__ = "trip_users"

    tu_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"),
                        nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.trip_id"),
                        nullable=False)

    user = db.relationship('User', backref='trip_users')
    trip = db.relationship('Trip', backref='trip_users')

    def __repr__(self):
        """Define representation of trip_user objects"""

        return f"<Trip_user id={self.tu_id}>"


class Trip_Trail(db.Model):
    """Trails associated with a given trip.

    Association table between Trail and Trip tables"""

    __tablename__ = "trip_trails"

    tt_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    trail_id = db.Column(db.Integer, db.ForeignKey("trails.trail_id"),
                         nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.trip_id"),
                        nullable=False)
    added_by = db.Column(db.Integer, db.ForeignKey("users.user_id"),
                         nullable=False)

    trail = db.relationship('Trail', backref='trip_trails')
    trip = db.relationship('Trip', backref='trip_trails')
    user = db.relationship('User', backref='trip_trails')

    def __repr__(self):
        """Define representation of trip_trail objects"""

        return f"<Trip_trail id={self.tt_id}>"


def connect_to_db(app, db_name='postgresql:///hikingapp'):
    """Connect database to Flask app"""

    app.config['SQLALCHEMY_DATABASE_URI'] = db_name
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


# For testing database & relations, run this file interactively
if __name__ == "__main__":  # pragma: no cover
    from server import app
    connect_to_db(app)

    print("Connected to db")
