from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth
from ..database import  get_db

router = APIRouter(
    tags=['Users']
)

@router.post("/users", status_code=status.HTTP_201_CREATED)
#, response_model=schemas.UserOut
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):
    query = db.query(models.User).filter(models.User.email == user.email).first()
    if not query:
        hashed_password = utils.hash(user.password)
        user.password = hashed_password
        new_user = models.User(**user.dict())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"id":new_user.id, "email": new_user.email, "name": new_user.name, "dob":new_user.dob}
    else:
        return {"message":"email already exists"}
        

   
@router.get("/user/{id}", response_model=schemas.UserOut)
def get_user(id: int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} is not found")
    return user

@router.put("/user/{id}", response_model=schemas.UserOut)
def update_user(id: int, user: schemas.UserUpdate, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    query = db.query(models.User).filter(models.User.id == id)
    userdata = query.first()
    if userdata == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"User with id {id} does not exist")
    if userdata.id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    query.update(user.dict(), synchronize_session=False)
    db.commit()
    return query.first()