from itertools import count
from pyexpat import model
from statistics import mode
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from requests import session
from sqlalchemy.orm import Session
from .. import models, schemas, oauth
from ..database import get_db
from typing import List, Optional
from sqlalchemy import select, join

router = APIRouter(
    tags=['RequestApproval']
)

@router.post("/request", status_code=status.HTTP_201_CREATED)
def request(request: schemas.RequestWithQuant, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    request_query = db.query(models.Request).filter(models.Request.med_id == request.med_id, models.Request.owner_id == current_user.id)
    found = request_query.first()
    query = db.query(models.Request).filter(models.Request.med_id == request.med_id, models.Request.approval != "no")
    # q1 = query.first()
    # if q1:
    #     return {"message":"Already Requested"}
    if found:
        #raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has alredy selected medicine with id {request.med_id}")
        return {"message":"Requested Earlier"}
    new_request = models.Request(med_id = request.med_id, owner_id = current_user.id, ownerof_med = request.ownerof_med, reqquantity = request.reqquantity)
    db.add(new_request)
    db.commit()
    return {"message":"successful"}

@router.get("/requestsinfo")
def get_requests(db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    results = db.query(models.Medicine, models.Request).join(models.Request, models.Medicine.med_id == models.Request.med_id)
    res = results.filter(models.Request.owner_id == current_user.id).all()
    return res
    
@router.get("/approval")
def get_requests(db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    meds = db.query(models.Medicine, models.Request).filter(models.Medicine.med_id == models.Request.med_id, models.Medicine.owner_id == current_user.id).all()
    return  meds
    
@router.get("/myapproval")
def get_requests(db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    meds = db.query(models.Medicine, models.Request).filter(models.Medicine.med_id == models.Request.med_id, models.Medicine.owner_id == current_user.id, models.Request.approval != "Empty").all()
    return  meds

@router.get("/approvalinfo/{id}")
def get_requests(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    meds = db.query(models.Medicine, models.Request,models.User.name,models.User.email,models.User.phone).filter(models.Medicine.med_id == models.Request.med_id
    , models.Medicine.owner_id == current_user.id, models.Medicine.med_id == id
    , models.Request.owner_id == models.User.id ).all()
    return  meds

@router.put("/approve/{id}/{id1}")
def update_approve(id: int, id1: int, new_data: schemas.Request, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    query = db.query(models.Request).filter( models.Request.owner_id == id ,models.Request.med_id == id1)
    found = query.first()
    if found == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"Medicine with id {id} does not exist")
    query.update(new_data.dict(), synchronize_session=False)
    db.commit()
    return query.first()

@router.get("/approved/{id}/{id1}")
def get_approve(id: int,id1: int, db: Session = Depends(get_db), current_user: int = Depends(oauth.get_current_user)):
    query = db.query(models.Request.approval).filter( models.Request.owner_id == id ,models.Request.med_id == id1)
    found = query.first()
    return found

@router.get("/barcodeinfo/{id}")
def get_barcodemed(id: str, db: Session = Depends(get_db)):
    med_info = db.query(models.BarcodeMed).filter(models.BarcodeMed.barcode == id).first()
    if not med_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Medicine with id {id} is not found")
    return med_info