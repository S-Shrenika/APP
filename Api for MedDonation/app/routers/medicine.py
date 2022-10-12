from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import true, func
from sqlalchemy.orm import Session
from .. import models, schemas, oauth
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    tags=['Medicine']
)

@router.get("/allmed", response_model=List[schemas.Med])
def get_meds(db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user), limit: int = 10, skip: int = 0
,search: Optional[str] = ""):
    meds = db.query(models.Medicine).filter(models.Medicine.owner_id != current_user.id).all()
    return meds

@router.get("/meds")
def get_meds(db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    meds = db.query(models.Medicine).filter(models.Medicine.owner_id == current_user.id).all()
    med = db.query(models.Medicine, func.count(models.Request.med_id).label("Totalcount")).filter(models.Medicine.owner_id == current_user.id).join(models.Request, models.Medicine.med_id == models.Request.med_id, isouter=True).group_by(models.Medicine.med_id).all()
    return med

@router.post("/meds", status_code=status.HTTP_201_CREATED, response_model=schemas.Med)
def create_meds(toy: schemas.MedCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    new_med = models.Medicine(owner_id=current_user.id, **toy.dict())
    db.add(new_med)
    db.commit()
    db.refresh(new_med)
    return new_med

@router.get("/meds/{id}", response_model=schemas.Med)
def get_med(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    med_info = db.query(models.Medicine).filter(models.Medicine.med_id == id).first()
    if not med_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Medicine with id {id} is not found")
    return med_info

@router.delete("/meds/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_med(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth.get_current_user)):
    med_query = db.query(models.Medicine).filter(models.Medicine.med_id == id)
    med = med_query.first()
    if med == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Medicine with id {id} does not exist")
    if med.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    med_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/meds/{id}", response_model=schemas.Med)
def update_med(id: int, new_toy: schemas.MedCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    med_query = db.query(models.Medicine).filter(models.Medicine.med_id == id)
    med = med_query.first()
    if med == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Medicine with id {id} does not exist")
    if med.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized to perform requested action")
    med_query.update(new_toy.dict(), synchronize_session=False)
    db.commit()
    return med_query.first()

