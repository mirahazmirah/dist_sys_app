from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.infrastructure.database import engine, Base
from .logging import LoggingMiddleware
from .security import SecurityMiddleware
from api.routers import student, driver, bus, taxi, bicycle

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Educational Logic: Ensure tables exist on startup ---
    # In Distributed Systems, schema consistency is key before node entry.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="Campus Ride API", 
    version="0.2.0",
    lifespan=lifespan
)

# Add Middlewares
app.add_middleware(LoggingMiddleware)
app.add_middleware(SecurityMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "https://frontend-production-50e0.up.railway.app",  # Production Railway
    "http://localhost:3000",                            # Local Development (Next.js)
    "http://127.0.0.1:3000",                            # Local Alternative
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Transit Routers
app.include_router(student.router, prefix="/api/v1")
app.include_router(driver.router, prefix="/api/v1")
app.include_router(bus.router, prefix="/api/v1")
app.include_router(taxi.router, prefix="/api/v1")
app.include_router(bicycle.router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok", "database": "connected"}
