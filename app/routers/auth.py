from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import schemas, models, utils, oauth2
from ..database import get_db

router = APIRouter(tags=['Authentication'])

@router.get('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user or not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Invalid credentials")
    
    # create a token
    access_token = oauth2.create_access_token(data = {"user_id": user.id})

    # return token
    return {"access_token": access_token, "type": "bearer"}
    
    
