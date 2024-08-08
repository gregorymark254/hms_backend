from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Import Base here for discovery by alembic
from app.utils.database import Base
from app import auth, appointments, users, payments, prescription, billing, patients, medication, doctors
app = FastAPI()


origins = [
    "http://localhost:3000",
    "https://medixsolutions.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hospital Management System"}


app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(appointments.router, prefix="/appointments", tags=["appointments"])
app.include_router(billing.router, prefix="/billing", tags=["billing"])
app.include_router(doctors.router, prefix="/doctors", tags=["doctors"])
app.include_router(medication.router, prefix="/medication", tags=["medication"])
app.include_router(patients.router, prefix="/patients", tags=["patients"])
app.include_router(payments.router, prefix="/payments", tags=["payments"])
app.include_router(prescription.router, prefix="/prescription", tags=["prescription"])
