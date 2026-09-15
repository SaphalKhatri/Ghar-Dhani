from fastapi import APIRouter,Depends,HTTPException,status
from typing import List,Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.leases import Lease
from app.models.flat import Flat
from app.models.tenant import Tenant
from app.schemas.lease import LeaseCreate,LeaseUpdate,LeaseResponse

router=APIRouter(prefix="/api/leases",tags=["Leases"])

@router.post("/",response_model=LeaseResponse,status_code=status.HTTP_201_CREATED)
def create_lease(lease:LeaseCreate,db:Session=Depends(get_db)):
    tenant=db.query(Tenant).filter(Tenant.tenant_id==lease.tenant_id).first() #check if tenenat exists
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tenant with id {lease.tenant_id}not found",
        )

    flat=db.query(Flat).filter(Flat.flat_id==lease.flat_id).first()# check if flat exists
    if not flat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"flat  of id {lease.flat_id} ntoo foiunf"
        )
    #check if alt has has an active lease or nor
    existing_lease=(
        db.query(Lease).filter(Lease.flat_id==lease.flat_id,Lease.status=="active").first()
    )
    if existing_lease:
        raise HTTPException(
            status=status.HTTP_400_BAD_REQUEST,
            detail=" flat has an active lease,End the lease first",
        )
    
    #create
    new_lease=Lease(**lease.model_dump())
    flat.status="occupied"
    db.add(new_lease)
    db.commit()
    db.refresh(new_lease)
    return new_lease

@router.get("/"response_model=List[LeaseResponse])
def get_all_leases(status_filter:Optional[str]=None,db:Session=Depends(get_db)):
    query=db.query(Lease)
    if status_filter:
        query=query.filter(Lease.status==status_filter).all()
    return query

@router.put("/{lease_id}",response_model=LeaseResponse)\
def update_lease(lease_id:int, lease_update:LeaseUpdate,db:Session=Depends(get_db)):

    lease=db.query(Lease).filter(Lease.lease_id== lease_id).first()
    if not lease:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f" lease of id:{lease_id} not  found"
        )
        #update the lease fields
    for field,value in lease_update.model_dump(exclude_unset=True).items():
        setattr(lease,field,value)
    #if lease is marked ended then make fiels available
    if lease.status=="ended":
        flat.status="available"
    
    db.commit()
    db.refresh(lease)
    return lease
