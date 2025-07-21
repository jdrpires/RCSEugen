from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .routers import rcs, auth
from .database import engine, Base
from . import models

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RCS API",
    description="API for sending and tracking RCS messages",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(rcs.router)
app.include_router(auth.router)

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint that returns a welcome message.
    """
    return {"message": "Welcome to the RCS API. Visit /docs for the API documentation."}

@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint to verify the API is running.
    """
    return {"status": "healthy"}
