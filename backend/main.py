from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from database import init_db
from routers import auth_router, patients_router, scans_router, stats_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create DB tables on startup."""
    await init_db()
    yield


app = FastAPI(
    title="MediMind API",
    description="AI-Powered Radiology Assistant",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", "http://localhost:3002"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth_router.router)
app.include_router(patients_router.router)
app.include_router(scans_router.router)
app.include_router(stats_router.router)


@app.get("/")
def read_root():
    return {"status": "ok", "message": "MediMind API v2 is running.", "docs": "/docs"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
