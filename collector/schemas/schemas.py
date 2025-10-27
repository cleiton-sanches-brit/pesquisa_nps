from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from decimal import Decimal


class CustomerBase(BaseModel):
    name: str
    email: EmailStr
    company: Optional[str] = None


class CustomerCreate(CustomerBase):
    pass


class Customer(CustomerBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class SurveyBase(BaseModel):
    title: str
    description: Optional[str] = None
    survey_type: str
    is_active: bool = True


class Survey(SurveyBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ResponseBase(BaseModel):
    customer_name: str
    customer_email: EmailStr
    customer_company: Optional[str] = None
    survey_id: int
    score: Optional[int] = None
    comment: Optional[str] = None


class ResponseCreate(ResponseBase):
    pass


class Response(ResponseBase):
    id: int
    submitted_at: datetime
    
    class Config:
        from_attributes = True


class NPSSubmitRequest(BaseModel):
    customer_name: str
    customer_email: EmailStr
    customer_company: Optional[str] = None
    survey_id: int
    score: int
    comment: Optional[str] = None


class NPSSubmitResponse(BaseModel):
    success: bool
    message: str
    response_id: Optional[int] = None


class NPSResult(BaseModel):
    survey_id: int
    survey_title: str
    total_responses: int
    average_score: float
    promoters: int
    passives: int
    detractors: int
    nps_score: float


class NPSSummary(BaseModel):
    total_responses: int
    average_nps: float
    promoters_percentage: float
    passives_percentage: float
    detractors_percentage: float
    surveys: List[NPSResult]
