from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import classify, generate, submit


app = FastAPI(
    title="Nexus Connected - Augmented Form API",
    version="1.0.0",
    description="Backend FastAPI pour formulaire augmenté (missions fixes + champs dynamiques AI).",
)

# CORS pour ton frontend (Vite/React)
origins = [
    settings.FRONTEND_ORIGIN,
    "http://localhost:3000",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusion des routes
app.include_router(classify.router, prefix="/api")
app.include_router(generate.router, prefix="/api")
app.include_router(submit.router, prefix="/api")


@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok", "message": "Nexus backend is alive ✨"}
