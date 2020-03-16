import unittest

from server import app, db, connect_to_db
import seed

MAPS_JS_KEY = "key"
HIKING_PROJECT_KEY = "key"


class TestFlaskRoutes(unittest.TestCase):
    """Test Flask routes"""

    def setUp(self):
        """Set up prior to every test"""

        self.client = app.test_client()
        app.config["TESTING"] = True

    def test_index(self):
        """Confirm that index returns correct HTML."""

        result = self.client.get("/")

        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Search for hiking trails here!", result.data)

    def test_register(self):
        """Test registration form"""

        result = self.client.get("/register")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<form action="/register" method="POST">', result.data)

    def test_login(self):
        """Test user log in form """

        result = self.client.get("/login")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<form action="/login" method="POST">', result.data)

    def test_account_pg(self):
        """Test account page when logged in"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

        result = self.client.get("/account")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Update your account information", result.data)

    def test_account_pg_catch(self):
        """Test account page when not logged in"""
        
        result = self.client.get("/account", follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"You need to be logged in", result.data)

    def test_logout(self):
        """Test logout page"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

        result = self.client.get("/logout", follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Logged out", result.data)

    def test_search_results(self):
        """Test search results page"""

        result = self.client.get("/search")
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"<h2>Search Results</h2>", result.data)


class TestdbRoutes(unittest.TestCase):
    """Test database routes"""

    def setUp(self):
        """Set up prior to every test"""

        self.client = app.test_client()
        app.config["TESTING"] = True

        # Set fake login
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables if not already created. Delete all entries in tables
        db.create_all()
        seed.User_Trail.query.delete()
        seed.Trip_User.query.delete()
        seed.Trip_Trail.query.delete()
        seed.Trip.query.delete()
        seed.Trail.query.delete()
        seed.User.query.delete()

        # Seed sample data into the database, and set the PK id values
        seed.load_sample_users()
        seed.load_sample_trails()
        seed.load_sample_user_trails()
        seed.load_sample_trips()
        seed.load_sample_trip_users()
        seed.load_sample_trip_trails()
        seed.set_val_user_id()
        seed.set_val_user_trail_id()
        seed.set_val_trip_id()
        seed.set_val_trip_user_id()
        seed.set_val_trip_trail_id()

    def tearDown(self):
        """Tear down at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_trail_page(self):
        """Test a sample trail page"""

        result = self.client.get("/trail/1234")
        self.assertIn(b'<h1 id="trail-name">Sample trail</h1>', result.data)

    def test_login_submission(self):
        """Test user log in form submission"""

        result = self.client.post("/login",
                                  data={"username": "hello",
                                        "password": "hello"},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Login successful", result.data)

    def test_login_wrong_submission(self):
        """Test user log in form submission with wrong info"""

        result = self.client.post("/login",
                                  data={"username": "hello",
                                        "password": "goobye"},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"Incorrect login information", result.data)

    def test_register_submission(self):
        """Test registration form submission"""

        result = self.client.post("/register",
                                  data={"username": "username",
                                        "email": "hello@username.com",
                                        "password": "userpassword"},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'<form action="/login" method="POST">', result.data)

    def test_register_submission_username_catch(self):
        """Test registration form submission if username already taken"""

        result = self.client.post("/register",
                                  data={"username": "hello",
                                        "email": "hello@username.com",
                                        "password": "userpassword"},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"The username hello is already taken", result.data)

    def test_register_submission_email_catch(self):
        """Test registration form submission if email already taken"""

        result = self.client.post("/register",
                                  data={"username": "newuser",
                                        "email": "hello@hello.com",
                                        "password": "userpassword"},
                                  follow_redirects=True)
        self.assertEqual(result.status_code, 200)
        self.assertIn(b"There&#39;s already an account associated with hello@hello.com", result.data)



if __name__ == "__main__":

    unittest.main()
