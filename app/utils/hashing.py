# Description: Hashing utility functions for password hashing and verification.
import hashlib
import os

def hash_password(password):
    """
    Hash a password with a randomly generated salt.
    Returns the salt and hashed password as hex strings.
    """
    salt = os.urandom(16)
    hashed = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return salt.hex(), hashed.hex()

def verify_password(salt_hex, hashed_hex, password_attempt):
    """
    Verify a password attempt against the stored salt and hashed password.
    """
    salt = bytes.fromhex(salt_hex)
    hashed_attempt = hashlib.pbkdf2_hmac('sha256', password_attempt.encode(), salt, 100000)
    return hashed_attempt.hex() == hashed_hex
