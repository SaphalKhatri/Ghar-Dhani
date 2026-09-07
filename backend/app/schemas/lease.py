from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict


class LeaseBase(BaseModel):
    tenant_id: int
    flat_id: int
    start_date: date
    end_date: Optional[date] = None
    status: Optional[str] = "active"


class LeaseCreate(LeaseBase):
    pass


class LeaseUpdate(BaseModel):
    end_date: Optional[date] = None
    status: Optional[str] = None


class LeaseResponse(LeaseBase):
    lease_id: int

    model_config = ConfigDict(from_attributes=True)