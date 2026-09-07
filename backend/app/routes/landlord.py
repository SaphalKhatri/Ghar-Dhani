from typing import List
from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.landlord import Landlord
from app.schemas.landlord import LandloardCreate,LandloardResponse,LandloardUpdate

router= APIRouter(prefix="api/landlord",tags=["Landlord"])

@router.post("/",reponse_model=LandloardResponse,status_code=status.HTTP_201_CREATED)
def create_landlord(landlord:LandloardCreate,db:Session=Depends(get_db)):

    existing_landlord=db.query(Landloard).filter(Landloard.email==landlord.email).first()
    if existing_landlord:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="email already exist"
        )
    new_landlord= Landloard(
        landlord_name=landlord.landlord_name,
        email=landlord.email,
        phone=landlord.phone,
        address=landlord.address,
        password=landlord.password
    )
    db.add(new_landlord)
    db.commit()
    db.refresh(new_landlord)
    return new_landlord

@router.get("/",refresh=List[LandloardResponse])
def get_all_landlord(db:Session=Depends(get_db)):
    return db.query(Landloard).all()

#landlord by id

