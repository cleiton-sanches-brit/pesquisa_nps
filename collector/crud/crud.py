from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..schemas.models import Customer, Survey, Response
from ..schemas.schemas import CustomerCreate, ResponseCreate
from typing import List, Optional


def get_customer_by_email(db: Session, email: str) -> Optional[Customer]:
    """Busca cliente por email"""
    return db.query(Customer).filter(Customer.email == email).first()


def create_customer(db: Session, customer: CustomerCreate) -> Customer:
    """Cria um novo cliente"""
    db_customer = Customer(
        name=customer.name,
        email=customer.email,
        company=customer.company
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def get_survey(db: Session, survey_id: int) -> Optional[Survey]:
    """Busca pesquisa por ID"""
    return db.query(Survey).filter(Survey.id == survey_id).first()


def get_active_surveys(db: Session) -> List[Survey]:
    """Lista todas as pesquisas ativas"""
    return db.query(Survey).filter(Survey.is_active == True).all()


def create_response(db: Session, response: ResponseCreate, customer_id: int) -> Response:
    """Cria uma nova resposta"""
    db_response = Response(
        customer_id=customer_id,
        survey_id=response.survey_id,
        score=response.score,
        comment=response.comment
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    return db_response


def get_responses_by_survey(db: Session, survey_id: int) -> List[Response]:
    """Busca respostas por pesquisa"""
    return db.query(Response).filter(Response.survey_id == survey_id).all()


def get_all_responses(db: Session, skip: int = 0, limit: int = 100) -> List[Response]:
    """Lista todas as respostas com paginação"""
    return db.query(Response).offset(skip).limit(limit).all()


def get_nps_responses(db: Session) -> List[Response]:
    """Busca respostas de pesquisas NPS"""
    return db.query(Response).join(Survey).filter(
        Survey.survey_type == 'nps',
        Response.score.isnot(None)
    ).all()


def calculate_nps_score(responses: List[Response]) -> dict:
    """Calcula score NPS a partir das respostas"""
    if not responses:
        return {
            'total_responses': 0,
            'promoters': 0,
            'passives': 0,
            'detractors': 0,
            'nps_score': 0.0
        }
    
    promoters = sum(1 for r in responses if r.score and r.score >= 9)
    passives = sum(1 for r in responses if r.score and r.score in [7, 8])
    detractors = sum(1 for r in responses if r.score and r.score <= 6)
    
    total = len(responses)
    nps_score = ((promoters - detractors) / total * 100) if total > 0 else 0
    
    return {
        'total_responses': total,
        'promoters': promoters,
        'passives': passives,
        'detractors': detractors,
        'nps_score': round(nps_score, 2)
    }
