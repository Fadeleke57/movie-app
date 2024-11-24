import pytest
from app import create_app
from app.utils.db import db
from app.models.user import User
from app.utils.hashing import hash_password, verify_password

@pytest.fixture
def app():
    """Create a Flask application for testing."""
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database for testing
    return app

@pytest.fixture
def client(app):
    """Create a test client for the application."""
    return app.test_client()

@pytest.fixture
def init_db(app):
    """Initialize the database."""
    with app.app_context():
        db.create_all()
        yield
        db.drop_all()

def test_create_user(app, init_db):
    """Test creating a new user."""
    with app.app_context():
        username = "testuser"
        password = "testpassword"

        salt, hashed_password = hash_password(password)

        new_user = User(username=username, salt=salt, hashed_password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        retrieved_user = User.query.filter_by(username=username).first()
        assert retrieved_user is not None
        assert retrieved_user.username == username
        assert retrieved_user.salt == salt
        assert retrieved_user.hashed_password == hashed_password

def test_create_duplicate_user(app, init_db):
    """Test creating a user with a duplicate username."""
    with app.app_context():
        username = "testuser"
        password = "testpassword"

        salt, hashed_password = hash_password(password)
        user1 = User(username=username, salt=salt, hashed_password=hashed_password)
        db.session.add(user1)
        db.session.commit()

        user2 = User(username=username, salt=salt, hashed_password=hashed_password)
        db.session.add(user2)

        with pytest.raises(Exception):
            db.session.commit()

def test_password_hashing_verification():
    """Test password hashing and verification."""
    password = "testpassword"
    salt, hashed_password = hash_password(password)

    assert verify_password(salt, hashed_password, password)
    assert not verify_password(salt, hashed_password, "wrongpassword")

def test_get_user_by_username(app, init_db):
    """Test retrieving a user by username."""
    with app.app_context():
        username = "testuser"
        password = "testpassword"

        salt, hashed_password = hash_password(password)
        new_user = User(username=username, salt=salt, hashed_password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        retrieved_user = User.query.filter_by(username=username).first()
        assert retrieved_user is not None
        assert retrieved_user.username == username
