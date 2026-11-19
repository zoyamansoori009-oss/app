from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

#Password Hashing
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

#JWT Settings
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_schemas = OAuth2PasswordBearer(
    tokenUrl="login"
)

#Hash Password
def get_password_hash(password):
    return pwd_context.hash(password)


#Verify Password
def verify_password(
    plain_password,
    hashed_password
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )
    
    
#Create JWT Token
def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    to_encode.update({"exp": expire})
    
    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token
    
def get_current_user(
    token: str = Depends(
        oauth2_schemas
    )
):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        
        email = payload.get("sub")
        
        if email is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid Token"        
            )
        return email
    
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Token Expired or Invalid"
        )
    
    return token