from jose import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import datetime, timedelta
import os

SECRET = os.getenv("JWT_SECRET", "supersecret")
ALGO = "HS256"  # Hashing Algorithm

# Initialize Argon2 password hasher
ph = PasswordHasher()

def hash_password(password: str):
    """
    Hash password using Argon2.
    
    Argon2 advantages:
    - No password length limit (unlike bcrypt's 72-byte limit)
    - Memory-hard algorithm (resistant to GPU attacks)
    - Automatically handles salt and parameters
    - OWASP recommended
    """
    return ph.hash(password)

def verify_password(password: str, hashed: str):
    """
    Verify password against Argon2 hash.
    
    Returns True if password matches, False otherwise.
    """
    try:
        ph.verify(hashed, password)
        return True
    except VerifyMismatchError:
        return False

def create_token(user_id: str, role: str):
    payload = {
        "sub": user_id,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET, algorithm=ALGO)