import jwt
import bcrypt
from datetime import datetime, timedelta
from app.config import ACCESS_SECRET, REFRESH_SECRET, ACCESS_EXPIRE_MINUTES, REFRESH_EXPIRE_DAYS
from typing import Optional

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    if not isinstance(password, str):
        raise ValueError(f"Password must be a string, got {type(password)}")
    
    # Convert to bytes and truncate to 72 bytes (bcrypt's maximum)
    pwd_bytes = password.encode('utf-8')[:72]
    
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    
    # Return the hash as a string
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    try:
        return bcrypt.checkpw(
            plain_password.encode('utf-8')[:72],
            hashed_password.encode('utf-8')
        )
    except Exception:
        return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str: # Added type hints and Optional for expires_delta
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_EXPIRE_MINUTES)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, ACCESS_SECRET, algorithm="HS256")

def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str: # Added type hints and Optional for expires_delta
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_EXPIRE_DAYS)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, REFRESH_SECRET, algorithm="HS256")