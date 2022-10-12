from fastapi import FastAPI
from . import models
from .database import engine
from .routers import medicine, user, auth, requestApproval, donation
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(medicine.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(requestApproval.router)
app.include_router(donation.router)

@app.get("/")
async def root():
    return {"message": "Welcome!!"}


