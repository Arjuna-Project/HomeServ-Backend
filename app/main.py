from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import (
    auth,
    user,
    area,
    service,
    professionals,
    packages,
    bookings,
    contact,
    professional_auth,
    professional_dashboard,
    professional_jobs,
)

app = FastAPI(title="HomeServ API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(area.router)
app.include_router(service.router)
app.include_router(professionals.router)
app.include_router(packages.router)
app.include_router(bookings.router)
app.include_router(contact.router)
app.include_router(professional_auth.router)
app.include_router(professional_dashboard.router)
app.include_router(professional_jobs.router)

@app.get("/")
def root():
    return {"message": "Backend alive (localhost)"}
