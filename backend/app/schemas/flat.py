from typing import Optional
from pydantic import BaseModel, ConfigDict


class FlatBase(BaseModel):
    flat_name: str
    rent_amount: float
    status: Optional[str] = "available"


class FlatCreate(FlatBase):
    landlord_id: int


class FlatUpdate(BaseModel):
    flat_name: Optional[str] = None
    rent_amount: Optional[float] = None
    status: Optional[str] = None


class FlatResponse(FlatBase):
    flat_id: int
    landlord_id: int

    model_config = ConfigDict(from_attributes=True)