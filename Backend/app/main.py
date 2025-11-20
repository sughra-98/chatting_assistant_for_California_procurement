"""

California Procurement Assistant API
AI-powered API with LangChain agents for querying procurement data

"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.config import get_settings
from app.database.mongodb import mongodb
from app.routers import query, stats

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Lifespan events for startup and shutdown of the app 
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info("=" * 70)
    logger.info(" Starting California Procurement Assistant API")
    logger.info("=" * 70)
    
    # Startup
    mongodb.connect()
    logger.info("Backend ready!")
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")
    mongodb.disconnect()


# Initialize FastAPI
app = FastAPI(
    title="California Procurement Assistant API",
    description="AI-powered API with LangChain agents for querying procurement data",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(query.router)
app.include_router(stats.router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "California Procurement Assistant API",
        "version": "2.0.0",
        "status": "running",
        "features": [
            "LangChain Agent",
            "Gemini AI",
            "MongoDB Integration",
            "Natural Language Queries"
        ]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        mongodb.client.admin.command('ping')
        return {
            "status": "healthy",
            "database": "connected",
            "agent": "ready"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )

