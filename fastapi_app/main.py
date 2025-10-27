from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from dotenv import load_dotenv
import os
from routers import surveys, responses
from database import engine, Base

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(
    title="NPS Surveys API",
    description="API para coleta de respostas de pesquisas NPS",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(surveys.router, prefix="/api/v1", tags=["surveys"])
app.include_router(responses.router, prefix="/api/v1", tags=["responses"])

@app.get("/")
async def root():
    return {"message": "NPS Surveys API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is running"}

# Create database tables
@app.on_event("startup")
async def startup_event():
    # Create tables
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8001,
        reload=True
    )
