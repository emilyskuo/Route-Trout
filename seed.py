"""Seed test data into hikingapp database"""

from sqlalchemy import func

from model import (User, Trail, User_Trail, Trip, Trip_User,
                   Trip_Trail, db, connect_to_db)
from server import app


def load_sample_users():
    """Create sample user instances"""

    user1 = User(username="hello", email="hello@hello.com")
    user2 = User(username="dude", email="dude@hello.com")

    user1.set_password("hello")
    user2.set_password("dudeman")

    db.session.add_all([user1, user2])

    db.session.commit()


def load_sample_trails():
    """Create sample trail instances"""

    trail1 = Trail(trail_id=1234, trail_name="Sample trail")
    trail2 = Trail(trail_id=12345, trail_name="Sample trail 2")

    db.session.add_all([trail1, trail2])

    db.session.commit()


def load_sample_user_trails():
    """Create sample user_trail instances"""

    users = User.query.all()

    ut1 = User_Trail(user_id=users[0].user_id, trail_id=1234, is_completed=True)
    ut2 = User_Trail(user_id=users[1].user_id, trail_id=1234, is_completed=False)
    ut3 = User_Trail(user_id=users[1].user_id, trail_id=12345, is_completed=False)
    ut4 = User_Trail(user_id=users[0].user_id, trail_id=12345, is_completed=True)

    db.session.add_all([ut1, ut2, ut3, ut4])

    db.session.commit()


def load_sample_trips():
    """Create sample trip instances"""

    trip1 = Trip(trip_name="Test trip 1", creator_id=1)
    trip2 = Trip(trip_name="Test trip 2", creator_id=2)

    db.session.add_all([trip1, trip2])

    db.session.commit()


def load_sample_trip_users():
    """Create sample trip_user instances"""

    tu1 = Trip_User(trip_id=1, user_id=1)
    tu2 = Trip_User(trip_id=1, user_id=2)
    tu3 = Trip_User(trip_id=2, user_id=1)

    db.session.add_all([tu1, tu2, tu3])

    db.session.commit()


def load_sample_trip_trails():
    """Create sample trip_trail instances"""

    tt1 = Trip_Trail(trip_id=1, trail_id=1234, added_by=2)
    tt2 = Trip_Trail(trip_id=1, trail_id=12345, added_by=1)
    tt3 = Trip_Trail(trip_id=2, trail_id=1234, added_by=1)

    db.session.add_all([tt1, tt2, tt3])

    db.session.commit()


def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_user_trail_id():
    """Set value for the next ut_id after seeding database"""

    # Get the Max ut_id in the database
    result = db.session.query(func.max(User_Trail.ut_id)).one()
    max_id = int(result[0])

    # Set the value for the next ut_id to be max_id + 1
    query = "SELECT setval('user_trails_ut_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_trip_id():
    """Set value for the next trip_id after seeding database"""

    # Get the Max trip_id in the database
    result = db.session.query(func.max(Trip.trip_id)).one()
    max_id = int(result[0])

    # Set the value for the next trip_id to be max_id + 1
    query = "SELECT setval('trips_trip_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_trip_user_id():
    """Set value for the next tu_id after seeding database"""

    # Get the Max tu_id in the database
    result = db.session.query(func.max(Trip_User.tu_id)).one()
    max_id = int(result[0])

    # Set the value for the next tu_id to be max_id + 1
    query = "SELECT setval('trip_users_tu_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


def set_val_trip_trail_id():
    """Set value for the next tt_id after seeding database"""

    # Get the Max tt_id in the database
    result = db.session.query(func.max(Trip_Trail.tt_id)).one()
    max_id = int(result[0])

    # Set the value for the next tt_id to be max_id + 1
    query = "SELECT setval('trip_trails_tt_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


# To seed sample data into the database, run this file
if __name__ == "__main__":
    connect_to_db(app)

    # Create tables if not already created. Delete all entries in tables
    db.create_all()
    User_Trail.query.delete()
    Trip_User.query.delete()
    Trip_Trail.query.delete()
    Trip.query.delete()
    Trail.query.delete()
    User.query.delete()

    print("Tables created, all rows deleted")

    # Seed sample data into the database, and set the PK id values
    load_sample_users()
    load_sample_trails()
    load_sample_user_trails()
    load_sample_trips()
    load_sample_trip_users()
    load_sample_trip_trails()
    set_val_user_id()
    set_val_user_trail_id()
    set_val_trip_id()
    set_val_trip_user_id()
    set_val_trip_trail_id()

    print("Sample data seeded")
