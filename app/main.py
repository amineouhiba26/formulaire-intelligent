from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import classify, generate, submit, submissions
from app.database import connect_to_mongo, close_mongo_connection


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
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Database lifecycle events
@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()


# Inclusion des routes
app.include_router(classify.router, prefix="/api")
app.include_router(generate.router, prefix="/api")
app.include_router(submit.router, prefix="/api")
app.include_router(submissions.router, prefix="/api")


@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok", "message": "Nexus backend is alive ✨"}


