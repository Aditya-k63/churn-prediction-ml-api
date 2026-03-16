from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = "churn-super-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ── Password hashing 
pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")

# ── OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ── Fake user database (replace with real DB later)
USERS_DB = {
    "aditya": {
        "username": "aditya",
        "hashed_password": pwd_context.hash("password123"),
        "role": "admin"
    },
    "viewer": {
        "username": "viewer",
        "hashed_password": pwd_context.hash("viewer123"),
        "role": "viewer"
    }
}

# ── Helper functions

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """Dependency - decodes JWT and returns the user dict."""
    credentials_exception = HTTPException(
        status_code=401,
        detail="Invalid or expired token. Please login again.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = USERS_DB.get(username)
    if user is None:
        raise credentials_exception
    return user

def require_admin(current_user: dict = Depends(get_current_user)) -> dict:
    """Dependency - only allows admin role."""
    if current_user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Access denied. Admins only."
        )
    return current_user