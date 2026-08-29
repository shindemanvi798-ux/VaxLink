from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints import auth, children

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Backend API for Saathi - Immunization & Health Companion",
    version="2.0.0" # Bumping to 2.0.0 for the rewrite
)

# Enable CORS for the frontend to communicate with this backend
# For the pilot, we allow all origins. In production, restrict this to your Vercel/Netlify domain.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root health check endpoint (useful for Render/Railway to know the app is alive)
@app.get("/health")
def health_check():
    return {"status": "ok", "service": settings.PROJECT_NAME}

# Register all our modular API routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(children.router, prefix="/children", tags=["Children & Vaccines"])

# We will add the other routers (children, camps, etc.) here as we build them.
