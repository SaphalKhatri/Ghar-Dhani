from typing import Optional 
from pydantic import BaseModel,EmailStr,ConfigDict

class Landloard(BaseModel):
    landlord_name:str
    email:EmailStr
    phone:Optional[str]=None
    address:Optional[str]=None

class LandloardCreate(Landloard):
    password:str

class LandloardUpdate(BaseModel):
    landlord_name:Optional[str]=None
    email:Optional[str]=None
    phone:Optional[str]=None
    address:Optional[str]=None

class LandloardResponse(Landloard):
    landlord_id:int

    model_config=ConfigDict(from_attributes=True)