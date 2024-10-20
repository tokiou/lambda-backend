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


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        try:
            credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
            payload = jwt.decode(jwtoken, TOKEN_SECRET_KEY, algorithms=[ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            return True
        except InvalidTokenError:
            raise credentials_exception
            
            