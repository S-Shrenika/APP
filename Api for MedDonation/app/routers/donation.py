from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import true
from sqlalchemy.orm import Session
from .. import models, schemas, oauth
from ..database import get_db
from typing import List, Optional

router = APIRouter(
    tags=['Donation']
)

@router.get("/donation", response_model=List[schemas.Donation])
def get_donation(db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    donation = db.query(models.Donation).filter(models.Donation.owner_id == current_user.id).all()
    return donation

@router.post("/donation", status_code=status.HTTP_201_CREATED, response_model=schemas.Donation)
def create_donation(donation: schemas.DonationCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    new = models.Donation(owner_id=current_user.id, donationtype = donation.donationtype, ngoname = donation.ngoname, dateselected = donation.dateselected )
    db.add(new)
    db.commit()
    db.refresh(new)
    return new