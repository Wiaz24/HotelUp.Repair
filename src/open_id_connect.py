from fastapi.security import OpenIdConnect
from fastapi import Security, HTTPException, Depends
from starlette.status import HTTP_403_FORBIDDEN
from typing import Optional, List
import jwt
from jwt.exceptions import PyJWTError

# Initialize OpenID Connect
oauth2_scheme = OpenIdConnect(
    openIdConnectUrl=f"https://cognito-idp.us-east-1.amazonaws.com/us-east-1_m6K9nuUJX/.well-known/openid-configuration",
    auto_error=True
)

async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        if token.startswith('Bearer '):
            token = token.split(' ')[1]
            
        decoded_token = jwt.decode(
            token,
            options={"verify_signature": False}
        )
        
        user_roles = decoded_token.get("cognito:groups", [])
        return {"roles": user_roles, "sub": decoded_token.get("sub")}
        
    except PyJWTError:  # Changed from InvalidTokenError
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Invalid authentication token"
        )

def requires_role(required_roles: List[str]):
    async def role_checker(user: dict = Depends(get_current_user)):
        user_roles = user.get("roles", [])
        if not any(role in user_roles for role in required_roles):
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN,
                detail="You don't have the required role to access this resource"
            )
        return user
    return role_checker