"""Seed test data into hikingapp database"""

from sqlalchemy import func

from model import User, Trail, User_Trail, db, connect_to_db
from server import app

from datetime import datetime


def load_users():
    """Create user instances"""

    user1 = User(username="hello", email="hello@hello.com", password="hello", fname="hel", lname="lo", cell="1234567890")
    user2 = User(username="dude", email="dude@hello.com", password="hello", fname="du", lname="de", cell="1234567891")

    db.session.add(user1)
    db.session.add(user2)

    db.session.commit()


def load_trails():
    """Create trail instances"""

    trail1 = Trail(trail_id=1234, trail_name="Sample trail", length=7, long=123.123, lat=123.123)
    trail2 = Trail(trail_id=12345, trail_name="Sample trail 2", length=3, long=321.123, lat=321.123)

    db.session.add(trail1)
    db.session.add(trail2)

    db.session.commit()


def load_user_trails():
    """Create user_trail instances"""

    users = User.query.all()

    ut1 = User_Trail(user_id=users[0].user_id, trail_id=1234, is_completed=True, date_added=datetime.now())
    ut2 = User_Trail(user_id=users[1].user_id, trail_id=1234, is_completed=False, date_added=datetime.now())
    ut3 = User_Trail(user_id=users[1].user_id, trail_id=12345, is_completed=False, date_added=datetime.now())
    ut4 = User_Trail(user_id=users[0].user_id, trail_id=12345, is_completed=True, date_added=datetime.now())

    db.session.add(ut1)
    db.session.add(ut2)
    db.session.add(ut3)
    db.session.add(ut4)

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


# To seed sample data into the database, run this file
if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them. Delete all entries within tables
    db.create_all()
    User_Trail.query.delete()
    Trail.query.delete()
    User.query.delete()

    print("Tables created, all rows deleted")

    # Seed sample data into the database, and set the values for user_id and ut_id
    load_users()
    load_trails()
    load_user_trails()
    set_val_user_id()
    set_val_user_trail_id()

    print("Sample data seeded")
