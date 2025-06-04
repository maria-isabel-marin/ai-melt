# backend/app/schemas/metaphor_schema.py

from pydantic import BaseModel, Field
from typing import Any
from bson import ObjectId
from pydantic import validator

# Clase auxiliar para ObjectId
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class ProcessBatchRequest(BaseModel):
    processing_code: str = Field(..., description="Job code que generó el front")
    batch_index: int = Field(..., ge=0, description="Índice del batch en la lista")
    batch_text: str = Field(..., min_length=1, description="Texto actual del batch")
    prompt_tokens: int = Field(..., ge=1, description="Tokens por prompt")

    @validator("processing_code")
    def upper_case_code(cls, v):
        return v.upper()

class MetaphorOut(BaseModel):
    id: str = Field(..., alias="_id")
    expression: str
    sourceDomain: str
    targetDomain: str
    conceptualMetaphor: str
    type: str
    confirmed: bool

    class Config:
        allow_population_by_field_name = True
        # json_encoders = {ObjectId: str}
