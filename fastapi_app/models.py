from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base


class Survey(Base):
    __tablename__ = "surveys_survey"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by_id = Column(Integer, ForeignKey("auth_user.id"))
    
    # Relationships
    questions = relationship("Question", back_populates="survey")
    responses = relationship("SurveyResponse", back_populates="survey")


class Question(Base):
    __tablename__ = "surveys_question"
    
    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("surveys_survey.id"))
    question_text = Column(Text, nullable=False)
    question_type = Column(String(10), nullable=False)  # nps, text, choice, rating
    is_required = Column(Boolean, default=True)
    order = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    survey = relationship("Survey", back_populates="questions")
    choices = relationship("Choice", back_populates="question")
    answers = relationship("Answer", back_populates="question")


class Choice(Base):
    __tablename__ = "surveys_choice"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("surveys_question.id"))
    choice_text = Column(String(200), nullable=False)
    value = Column(String(50), nullable=False)
    order = Column(Integer, default=0)
    
    # Relationships
    question = relationship("Question", back_populates="choices")


class SurveyResponse(Base):
    __tablename__ = "surveys_surveyresponse"
    
    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("surveys_survey.id"))
    respondent_id = Column(String(100), nullable=False)
    respondent_email = Column(String(255), nullable=True)
    submitted_at = Column(DateTime, server_default=func.now())
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    
    # Relationships
    survey = relationship("Survey", back_populates="responses")
    answers = relationship("Answer", back_populates="response")


class Answer(Base):
    __tablename__ = "surveys_answer"
    
    id = Column(Integer, primary_key=True, index=True)
    response_id = Column(Integer, ForeignKey("surveys_surveyresponse.id"))
    question_id = Column(Integer, ForeignKey("surveys_question.id"))
    answer_text = Column(Text, nullable=True)
    answer_value = Column(String(100), nullable=True)
    answer_choice_id = Column(Integer, ForeignKey("surveys_choice.id"), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    response = relationship("SurveyResponse", back_populates="answers")
    question = relationship("Question", back_populates="answers")
    answer_choice = relationship("Choice")


class NPSResult(Base):
    __tablename__ = "surveys_npsresult"
    
    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("surveys_survey.id"))
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    total_responses = Column(Integer, nullable=False)
    promoters = Column(Integer, nullable=False)
    passives = Column(Integer, nullable=False)
    detractors = Column(Integer, nullable=False)
    nps_score = Column(DECIMAL(5, 2), nullable=False)
    calculated_at = Column(DateTime, server_default=func.now())
