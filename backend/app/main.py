from fastapi import FastAPI
from app.database import engine,Base 

from app.models.landlord import Landlord
from app.models.lease import Lease
from app.models.flat import Flat 
from app.models.payment import Payment
from app.models.tenant import Tenant

from app.routes import landlord,flats,leases,payments,tenants

app=FastAPI(title="rental management",description="api for rental",version="1.0.0")

