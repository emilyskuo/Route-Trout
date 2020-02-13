"""Create database classes & tables for hiking trails app"""

from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model):
    """Users of hiking app"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    fname = db.Column(db.String(50), nullable=True)
    lname = db.Column(db.String(50), nullable=True)
    cell = db.Column(db.String(15), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(2), nullable=True)
    zipcode = db.Column(db.String(5), nullable=True)

    def __repr__(self):
        """Define representation of user objects"""

        return f"<User id={self.user_id}, username={self.username}>"


class Trail(db.Model):
    """Hiking trails for hiking app"""

    __tablename__ = "trails"

    trail_id = db.Column(db.Integer, primary_key=True)
    # Trail ids will be saved from Hiking Project API
    trail_name = db.Column(db.String(200), nullable=False)
    length = db.Column(db.Float, nullable=False)
    difficulty = db.Column(db.String(50))
    img_thumb_url = db.Column(db.String(200))
    img_lg_url = db.Column(db.String(200))
    long = db.Column(db.Float, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    description = db.Column(db.String(200))
    # avg_user_rating = db.Column(db.Float)

    def __repr__(self):
        """Define representation of trail objects"""

        return f"<Trail id={self.trail_id}, name={self.trail_name}>"


class User_Trail(db.Model):
    """Users' saved trails for hiking app"""

    __tablename__ = "user_trails"
    ut_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    trail_id = db.Column(db.Integer, db.ForeignKey("trails.trail_id"), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    date_added = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', backref='user_trails')
    trail = db.relationship('Trail', backref='user_trails')

    def __repr__(self):
        """Define representation of user-trail objects"""

        return f"<UT id={self.ut_id}, user_id={self.user_id}, trail_id={self.trail_id}>"


def connect_to_db(app):
    """Connect database to Flask app"""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///hikingapp'
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
    db.app = app
    db.init_app(app)


# For testing database & relations, run this file interactively
if __name__ == "__main__":
    from server import app
    connect_to_db(app)

    print("Connected to db")
