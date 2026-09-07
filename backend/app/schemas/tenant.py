from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict


class TenantBase(BaseModel):
    tenant_name: str
    email: EmailStr
    phone: Optional[str] = None
    address: Optional[str] = None


class TenantCreate(TenantBase):
    pass


class TenantUpdate(BaseModel):
    tenant_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class TenantResponse(TenantBase):
    tenant_id: int

    model_config = ConfigDict(from_attributes=True)