from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime
from decimal import Decimal


class ChoiceBase(BaseModel):
    choice_text: str
    value: str
    order: int = 0


class ChoiceCreate(ChoiceBase):
    pass


class Choice(ChoiceBase):
    id: int
    
    class Config:
        from_attributes = True


class QuestionBase(BaseModel):
    question_text: str
    question_type: str  # nps, text, choice, rating
    is_required: bool = True
    order: int = 0


class QuestionCreate(QuestionBase):
    choices: List[ChoiceCreate] = []


class Question(QuestionBase):
    id: int
    choices: List[Choice] = []
    
    class Config:
        from_attributes = True


class SurveyBase(BaseModel):
    title: str
    description: Optional[str] = None
    is_active: bool = True


class SurveyCreate(SurveyBase):
    questions: List[QuestionCreate] = []


class Survey(SurveyBase):
    id: int
    created_at: datetime
    updated_at: datetime
    questions: List[Question] = []
    
    class Config:
        from_attributes = True


class AnswerBase(BaseModel):
    question_id: int
    answer_text: Optional[str] = None
    answer_value: Optional[str] = None
    answer_choice_id: Optional[int] = None


class AnswerCreate(AnswerBase):
    pass


class Answer(AnswerBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class SurveyResponseBase(BaseModel):
    survey_id: int
    respondent_id: str
    respondent_email: Optional[EmailStr] = None
    answers: List[AnswerCreate]


class SurveyResponseCreate(SurveyResponseBase):
    pass


class SurveyResponse(SurveyResponseBase):
    id: int
    submitted_at: datetime
    answers: List[Answer] = []
    
    class Config:
        from_attributes = True


class NPSResultBase(BaseModel):
    survey_id: int
    period_start: datetime
    period_end: datetime
    total_responses: int
    promoters: int
    passives: int
    detractors: int
    nps_score: Decimal


class NPSResultCreate(NPSResultBase):
    pass


class NPSResult(NPSResultBase):
    id: int
    calculated_at: datetime
    
    class Config:
        from_attributes = True


class SurveyResponsePublic(BaseModel):
    """Schema para resposta pública (sem dados sensíveis)"""
    survey_id: int
    respondent_id: str
    answers: List[AnswerCreate]
    
    class Config:
        from_attributes = True
