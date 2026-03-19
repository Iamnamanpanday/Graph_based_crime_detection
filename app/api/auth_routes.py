from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from app.db.session import get_db
from app.core.security import verify_password, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

# For prototype, we use a hardcoded investigator account. 
# In Phase 3, these will be pulled from an 'users' table.
INVESTIGATOR_USER = {
    "username": "investigator_admin",
    "password": "secure_pass_2024"
}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != INVESTIGATOR_USER["username"] or form_data.password != INVESTIGATOR_USER["password"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": form_data.username, "role": "investigator"},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
