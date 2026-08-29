import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routes import children, camps, bookings

app = FastAPI(
    title="VaxLink API",
    description="Backend API for VaxLink - Multilingual, Voice-First Vaccination & Health Companion",
    version="1.0.0"
)

# Enable CORS for local development frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(children.router, prefix="/api")
app.include_router(camps.router, prefix="/api")
app.include_router(bookings.router, prefix="/api")

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "VaxLink Backend API"}

@app.get("/api")
def api_root():
    return {
        "message": "Welcome to VaxLink API",
        "endpoints": [
            "/api/children",
            "/api/children/{id}",
            "/api/children/{id}/schedule",
            "/api/camps",
            "/api/camps/{id}",
            "/api/camps/{id}/slots",
            "/api/camps/{id}/slots/{slot_id}/book"
        ]
    }

# Serve frontend static files
FRONTEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend"))

if os.path.exists(FRONTEND_DIR):
    app.mount("/src", StaticFiles(directory=os.path.join(FRONTEND_DIR, "src")), name="src")
    
    @app.get("/{full_path:path}")
    def serve_frontend(full_path: str):
        if full_path.startswith("api") or full_path.startswith("health"):
            return None
        file_path = os.path.join(FRONTEND_DIR, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
