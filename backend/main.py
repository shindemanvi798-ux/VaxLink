from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routes import children, camps, bookings

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for Saathi - Immunization & Health Companion",
    version="2.0.0"
)

# Enable CORS for the frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root health check endpoint
@app.get("/health")
def health_check():
    return {"status": "ok", "service": settings.PROJECT_NAME}

# Register all our in-memory/demo API routers with /api prefix
app.include_router(children.router, prefix="/api")
app.include_router(camps.router, prefix="/api")
app.include_router(bookings.router, prefix="/api")
