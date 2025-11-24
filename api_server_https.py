"""
gsWstudio.ai - HTTPS FastAPI Server
Exposes Python backend as REST API with SSL/HTTPS support
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import asyncio
import logging
import os
from datetime import datetime
from dotenv import load_dotenv

# Import framework
from zipwp_python_framework import GSWStudioPlatform, BusinessInput
from ai_client import create_ai_client

# Load environment
load_dotenv()

# Configure logging
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI(
    title="gsWstudio.ai API",
    description="Autonomous WordPress site generation API with HTTPS support",
    version="1.0.0"
)

# CORS configuration
cors_origins = os.getenv("API_CORS_ORIGINS", "https://localhost:3002,http://localhost:3002,http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory job storage
jobs: Dict[str, Dict[str, Any]] = {}


# ============================================================================
# REQUEST/RESPONSE MODELS
# ============================================================================

class SiteGenerationRequest(BaseModel):
    """Request model for site generation"""
    business_name: str = Field(..., description="Name of the business")
    business_type: str = Field(..., description="Type of business")
    description: Optional[str] = Field(None, description="Business description")
    industry: Optional[str] = Field(None, description="Industry category")
    target_audience: Optional[str] = Field("general public", description="Target audience")
    goals: Optional[List[str]] = Field(None, description="Business goals")
    tone: Optional[str] = Field("professional and approachable", description="Content tone")
    design_preference: Optional[str] = Field("modern and clean", description="Design preference")
    
    # Deployment options
    deploy: bool = Field(False, description="Whether to deploy to WordPress")
    wp_site_url: Optional[str] = Field(None, description="WordPress site URL")
    wp_username: Optional[str] = Field(None, description="WordPress admin username")
    wp_password: Optional[str] = Field(None, description="WordPress application password")
    wp_ssh_host: Optional[str] = Field(None, description="SSH host for WP-CLI")
    wp_ssh_user: Optional[str] = Field(None, description="SSH username")
    wp_ssh_key: Optional[str] = Field(None, description="Path to SSH private key")


class SiteGenerationResponse(BaseModel):
    """Response model for site generation"""
    job_id: str
    status: str
    message: str
    result: Optional[Dict[str, Any]] = None


class JobStatusResponse(BaseModel):
    """Response model for job status"""
    job_id: str
    status: str
    progress: int
    message: str
    result: Optional[Dict[str, Any]] = None
    created_at: str
    updated_at: str


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": "gsWstudio.ai API",
        "version": "1.0.0",
        "status": "operational",
        "protocol": "HTTPS" if os.path.exists("ssl/cert.pem") else "HTTP",
        "endpoints": {
            "health": "/health",
            "generate_site": "/api/v1/sites/generate",
            "job_status": "/api/v1/jobs/{job_id}",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "ai_mode": "real" if os.getenv("ANTHROPIC_API_KEY") else "mock",
        "ssl_enabled": os.path.exists("ssl/cert.pem")
    }


@app.post("/api/v1/sites/generate", response_model=SiteGenerationResponse)
async def generate_site(
    request: SiteGenerationRequest,
    background_tasks: BackgroundTasks
):
    """Generate a WordPress site"""
    try:
        import uuid
        job_id = str(uuid.uuid4())
        
        jobs[job_id] = {
            "status": "queued",
            "progress": 0,
            "message": "Job queued",
            "result": None,
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat()
        }
        
        background_tasks.add_task(process_site_generation, job_id, request)
        
        logger.info(f"Site generation job created: {job_id}")
        
        return SiteGenerationResponse(
            job_id=job_id,
            status="queued",
            message="Site generation job started. Use job_id to check status.",
            result=None
        )
        
    except Exception as e:
        logger.error(f"Failed to create site generation job: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/jobs/{job_id}", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    """Get status of a site generation job"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = jobs[job_id]
    
    return JobStatusResponse(
        job_id=job_id,
        status=job["status"],
        progress=job["progress"],
        message=job["message"],
        result=job["result"],
        created_at=job["created_at"],
        updated_at=job["updated_at"]
    )


@app.delete("/api/v1/jobs/{job_id}")
async def delete_job(job_id: str):
    """Delete a completed job"""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    
    del jobs[job_id]
    return {"message": "Job deleted successfully"}


@app.get("/api/v1/jobs")
async def list_jobs():
    """List all jobs"""
    return {
        "total": len(jobs),
        "jobs": [
            {
                "job_id": job_id,
                "status": job["status"],
                "progress": job["progress"],
                "created_at": job["created_at"]
            }
            for job_id, job in jobs.items()
        ]
    }


# ============================================================================
# BACKGROUND TASKS
# ============================================================================

async def process_site_generation(job_id: str, request: SiteGenerationRequest):
    """Background task to process site generation"""
    try:
        jobs[job_id]["status"] = "processing"
        jobs[job_id]["progress"] = 10
        jobs[job_id]["message"] = "Initializing platform..."
        jobs[job_id]["updated_at"] = datetime.utcnow().isoformat()
        
        ai_client = create_ai_client()
        platform = GSWStudioPlatform(ai_api_key=os.getenv("ANTHROPIC_API_KEY", "mock"))
        platform.ai_client = ai_client
        
        hosting_info = None
        if request.deploy and request.wp_site_url:
            hosting_info = {
                "wp_credentials": {
                    "site_url": request.wp_site_url,
                    "username": request.wp_username,
                    "password": request.wp_password,
                    "ssh_host": request.wp_ssh_host,
                    "ssh_user": request.wp_ssh_user,
                    "ssh_key": request.wp_ssh_key
                }
            }
        
        jobs[job_id]["progress"] = 20
        jobs[job_id]["message"] = "Generating site architecture..."
        jobs[job_id]["updated_at"] = datetime.utcnow().isoformat()
        
        result = await platform.create_site(
            business_name=request.business_name,
            business_type=request.business_type,
            description=request.description,
            hosting_info=hosting_info
        )
        
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["progress"] = 100
        jobs[job_id]["message"] = "Site generation completed successfully"
        jobs[job_id]["result"] = result
        jobs[job_id]["updated_at"] = datetime.utcnow().isoformat()
        
        logger.info(f"Job {job_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Job {job_id} failed: {e}")
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["progress"] = 0
        jobs[job_id]["message"] = f"Error: {str(e)}"
        jobs[job_id]["updated_at"] = datetime.utcnow().isoformat()


# ============================================================================
# STARTUP/SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Run on server startup"""
    logger.info("gsWstudio.ai API starting...")
    logger.info(f"AI Mode: {'Real API' if os.getenv('ANTHROPIC_API_KEY') else 'Mock'}")
    logger.info(f"SSL: {'Enabled' if os.path.exists('ssl/cert.pem') else 'Disabled'}")
    logger.info(f"CORS Origins: {cors_origins}")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on server shutdown"""
    logger.info("gsWstudio.ai API shutting down...")


# ============================================================================
# RUN SERVER WITH HTTPS SUPPORT
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    
    # Check for SSL certificates
    ssl_keyfile = "ssl/key.pem"
    ssl_certfile = "ssl/cert.pem"
    
    if os.path.exists(ssl_keyfile) and os.path.exists(ssl_certfile):
        logger.info(f"🔐 Starting HTTPS server on https://{host}:{port}")
        logger.info("⚠️  Using self-signed certificate - browsers will show security warning")
        logger.info("   Click 'Advanced' → 'Proceed to localhost' to continue")
        
        uvicorn.run(
            "api_server_https:app",
            host=host,
            port=port,
            reload=True,
            log_level="info",
            ssl_keyfile=ssl_keyfile,
            ssl_certfile=ssl_certfile
        )
    else:
        logger.warning("⚠️  SSL certificates not found. Running in HTTP mode.")
        logger.info(f"   Run './generate_ssl.sh' to generate certificates for HTTPS")
        logger.info(f"Starting HTTP server on http://{host}:{port}")
        
        uvicorn.run(
            "api_server_https:app",
            host=host,
            port=port,
            reload=True,
            log_level="info"
        )
