from fastapi import FastAPI
from app.database import engine,Base 

from app.models.landlord import Landlord
from app.models.lease import Lease
from app.models.flat import Flat 
from app.models.payment import Payment
from app.models.tenant import Tenant

from app.routes import landlord,flats,leases,payments,tenants

Base.metadata.create_all(bind=engine)

app=FastAPI(title="rental management",description="api for rental",version="1.0.0")

app.include_router(landlord.router)
app.include_router(flats.router)
app.include_router(leases.router)
app.include_router(payments.router)
app.include_router(tenants.router)