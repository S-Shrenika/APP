from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials:schemas.UserLogin , db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    access_token = oauth.create_access_token(data={"user_id": user.id})
    #return "ok"
    return {"access_token": access_token, "token_type": "bearer", "owner_id":user.id}
    
