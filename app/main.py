from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import connect_to_mongo, close_mongo_connection
from .routers import auth, users, tournaments, cubes

app = FastAPI(
    title="FNDC Tournament System API",
    description="API for managing Magic: The Gathering tournaments and cube proposals",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(tournaments.router)
app.include_router(cubes.router)


@app.on_event("startup")
async def startup_event():
    try:
        await connect_to_mongo()
        print("✅ MongoDB connection established successfully")
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        # En producción, podrías querer hacer exit(1) aquí
        # pero para desarrollo, continuamos


@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()


@app.get("/")
async def root():
    return {
        "message": "Welcome to FNDC Tournament System API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"} 