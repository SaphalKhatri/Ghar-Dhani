from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.flat import Flat
from app.models.landlord import Landlord
from app.schemas.flat import FlatCreate, FlatUpdate, FlatResponse

router = APIRouter(prefix="/api/flats", tags=["Flats"])


@router.post("/", response_model=FlatResponse, status_code=status.HTTP_201_CREATED)
def create_flat(flat: FlatCreate, db: Session = Depends(get_db)):
    # Make sure the landlord exists
    landlord = db.query(Landlord).filter(Landlord.landlord_id == flat.landlord_id).first()
    if not landlord:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Landlord with ID {flat.landlord_id} does not exist.",
        )

    new_flat = Flat(**flat.model_dump())
    db.add(new_flat)
    db.commit()
    db.refresh(new_flat)
    return new_flat


@router.get("/", response_model=List[FlatResponse])
def get_all_flats(landlord_id: Optional[int] = None, db: Session = Depends(get_db)):
    query = db.query(Flat)
    if landlord_id:
        query = query.filter(Flat.landlord_id == landlord_id)
    return query.all()


@router.get("/{flat_id}", response_model=FlatResponse)
def get_flat_by_id(flat_id: int, db: Session = Depends(get_db)):
    flat = db.query(Flat).filter(Flat.flat_id == flat_id).first()
    if not flat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Flat with ID {flat_id} not found.",
        )
    return flat


@router.put("/{flat_id}", response_model=FlatResponse)
def update_flat(flat_id: int, flat_update: FlatUpdate, db: Session = Depends(get_db)):
    flat = db.query(Flat).filter(Flat.flat_id == flat_id).first()
    if not flat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Flat with ID {flat_id} not found.",
        )

    for field, value in flat_update.model_dump(exclude_unset=True).items():
        setattr(flat, field, value)

    db.commit()
    db.refresh(flat)
    return flat


@router.delete("/{flat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_flat(flat_id: int, db: Session = Depends(get_db)):
    flat = db.query(Flat).filter(Flat.flat_id == flat_id).first()
    if not flat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Flat with ID {flat_id} not found.",
        )
    db.delete(flat)
    db.commit()
    return None