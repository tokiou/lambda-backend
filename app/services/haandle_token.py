from datetime import datetime, timedelta
from jwt import PyJWTError, encode, decode
import jwt
from typing import Optional
from fastapi import HTTPException, status
from dotenv import load_dotenv
import os
from fastapi.security import HTTPAuthorizationCredentials
from jwt.exceptions import InvalidTokenError
from typing import Optional
from fastapi.security import HTTPBearer
from fastapi import Request


dotenv_path = os.path.join(os.path.dirname(os.path.dirname
                                           (os.path.dirname(__file__))),
                           '.lambda_env')

load_dotenv(dotenv_path)
TOKEN_SECRET_KEY = os.getenv('TOKEN_SECRET_KEY')
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

class TokenData:
    def __init__(self, username: str):
        self.username = username


async def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, TOKEN_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def create_new_access_token(refresh_token):
    try:
        # Decodificar el refresh token
        payload = jwt.decode(refresh_token, TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        
        # Generar un nuevo access token
        new_access_token = await create_access_token({"sub": user_id})
        
        return new_access_token
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token has expired")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")

            user_id = self.verify_jwt(credentials.credentials)
            if not user_id:
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return user_id
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> str:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(jwtoken, TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
            return user_id  # Devolvemos el user_id si el token es válido
        except InvalidTokenError:
            raise credentials_exception

            
            