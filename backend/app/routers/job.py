# backend/app/routers/job.py

from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

from bson import ObjectId

router = APIRouter()

class JobRequest(BaseModel):
    processing_code: str = Field(..., description="Unique job code generated por el front")

class JobResponse(BaseModel):
    job_id: str
    processing_code: str
    created_at: datetime

@router.post("/", response_model=JobResponse)
async def create_job(request: JobRequest, fastapi_request: Request):
    """
    Recibe { processing_code } y crea un documento en Mongo en collection “jobs”.
    Devolvemos el job_id (ObjectId) y la misma processing_code.
    """
    db = fastapi_request.app.mongodb
    jobs_col = db["jobs"]
    doc = {
        "processing_code": request.processing_code,
        "status": "pending",
        "created_at": datetime.utcnow()
    }
    result = await jobs_col.insert_one(doc)
    return JobResponse(
        job_id=str(result.inserted_id),
        processing_code=request.processing_code,
        created_at=doc["created_at"]
    )
