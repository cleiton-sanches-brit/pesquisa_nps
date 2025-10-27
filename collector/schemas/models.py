from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, DECIMAL, Email
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class Customer(Base):
    __tablename__ = "dashboard_customer"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    email = Column(Email, nullable=False)
    company = Column(String(200), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Relationships
    responses = relationship("Response", back_populates="customer")


class Survey(Base):
    __tablename__ = "dashboard_survey"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    survey_type = Column(String(10), nullable=False)  # nps, csat, ces, custom
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    created_by_id = Column(Integer, ForeignKey("auth_user.id"))
    
    # Relationships
    questions = relationship("Question", back_populates="survey")
    responses = relationship("Response", back_populates="survey")


class Question(Base):
    __tablename__ = "dashboard_question"
    
    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("dashboard_survey.id"))
    text = Column(Text, nullable=False)
    question_type = Column(String(10), nullable=False)  # scale, text, choice, rating
    is_required = Column(Boolean, default=True)
    order = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    survey = relationship("Survey", back_populates="questions")


class Response(Base):
    __tablename__ = "dashboard_response"
    
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("dashboard_customer.id"))
    survey_id = Column(Integer, ForeignKey("dashboard_survey.id"))
    score = Column(Integer, nullable=True)
    comment = Column(Text, nullable=True)
    submitted_at = Column(DateTime, server_default=func.now())
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    
    # Relationships
    customer = relationship("Customer", back_populates="responses")
    survey = relationship("Survey", back_populates="responses")


class SurveySummary(Base):
    __tablename__ = "dashboard_surveysummary"
    
    id = Column(Integer, primary_key=True, index=True)
    survey_id = Column(Integer, ForeignKey("dashboard_survey.id"))
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    total_responses = Column(Integer, nullable=False)
    average_score = Column(DECIMAL(5, 2), nullable=False)
    promoters = Column(Integer, nullable=False)
    passives = Column(Integer, nullable=False)
    detractors = Column(Integer, nullable=False)
    nps_score = Column(DECIMAL(5, 2), nullable=False)
    calculated_at = Column(DateTime, server_default=func.now())
