import pytest
from app.utils.hashing import hash_password, verify_password

def test_hash_password():
    """Test the hash_password function."""
    password = "securepassword"

    # Generate the hash and salt
    salt, hashed_password = hash_password(password)

    # Assertions
    assert isinstance(salt, str), "Salt should be a hex string"
    assert isinstance(hashed_password, str), "Hashed password should be a hex string"
    assert len(salt) > 0, "Salt should not be empty"
    assert len(hashed_password) > 0, "Hashed password should not be empty"

def test_verify_password_success():
    """Test that password verification succeeds for correct input."""
    password = "securepassword"

    # Hash the password and verify
    salt, hashed_password = hash_password(password)
    assert verify_password(salt, hashed_password, password), "Password verification failed for correct input"

def test_verify_password_failure():
    """Test that password verification fails for incorrect input."""
    password = "securepassword"
    wrong_password = "wrongpassword"

    # Hash the password and attempt verification with an incorrect password
    salt, hashed_password = hash_password(password)
    assert not verify_password(salt, hashed_password, wrong_password), "Password verification succeeded for incorrect input"

def test_hashing_is_unique():
    """Test that hashing the same password twice produces different results due to different salts."""
    password = "securepassword"

    # Hash the password twice
    salt1, hashed_password1 = hash_password(password)
    salt2, hashed_password2 = hash_password(password)

    # Assertions
    assert salt1 != salt2, "Salts should be unique"
    assert hashed_password1 != hashed_password2, "Hashed passwords should be unique even for the same input"
