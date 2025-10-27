from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import SurveyResponse, Answer, Survey, Question
from ..schemas import SurveyResponse, SurveyResponseCreate, SurveyResponsePublic

router = APIRouter()


@router.post("/responses", response_model=SurveyResponse)
async def create_response(
    response: SurveyResponseCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    """Cria uma nova resposta de pesquisa (endpoint público)"""
    
    # Verificar se a pesquisa existe e está ativa
    survey = db.query(Survey).filter(
        Survey.id == response.survey_id,
        Survey.is_active == True
    ).first()
    
    if not survey:
        raise HTTPException(status_code=404, detail="Pesquisa não encontrada ou inativa")
    
    # Verificar se já existe resposta com o mesmo respondent_id
    existing_response = db.query(SurveyResponse).filter(
        SurveyResponse.survey_id == response.survey_id,
        SurveyResponse.respondent_id == response.respondent_id
    ).first()
    
    if existing_response:
        raise HTTPException(
            status_code=400, 
            detail="Já existe uma resposta para este respondente nesta pesquisa"
        )
    
    # Obter IP e User Agent
    client_ip = request.client.host
    user_agent = request.headers.get("user-agent", "")
    
    # Criar a resposta
    db_response = SurveyResponse(
        survey_id=response.survey_id,
        respondent_id=response.respondent_id,
        respondent_email=response.respondent_email,
        ip_address=client_ip,
        user_agent=user_agent
    )
    db.add(db_response)
    db.commit()
    db.refresh(db_response)
    
    # Criar as respostas individuais
    for answer_data in response.answers:
        # Verificar se a pergunta existe na pesquisa
        question = db.query(Question).filter(
            Question.id == answer_data.question_id,
            Question.survey_id == response.survey_id
        ).first()
        
        if not question:
            raise HTTPException(
                status_code=400, 
                detail=f"Pergunta {answer_data.question_id} não encontrada nesta pesquisa"
            )
        
        # Verificar se é obrigatória
        if question.is_required and not answer_data.answer_text and not answer_data.answer_value:
            raise HTTPException(
                status_code=400, 
                detail=f"Pergunta '{question.question_text}' é obrigatória"
            )
        
        db_answer = Answer(
            response_id=db_response.id,
            question_id=answer_data.question_id,
            answer_text=answer_data.answer_text,
            answer_value=answer_data.answer_value,
            answer_choice_id=answer_data.answer_choice_id
        )
        db.add(db_answer)
    
    db.commit()
    db.refresh(db_response)
    return db_response


@router.get("/responses", response_model=List[SurveyResponse])
async def get_responses(
    survey_id: Optional[int] = Query(None, description="Filtrar por ID da pesquisa"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Lista respostas de pesquisas (endpoint administrativo)"""
    query = db.query(SurveyResponse)
    
    if survey_id:
        query = query.filter(SurveyResponse.survey_id == survey_id)
    
    responses = query.offset(skip).limit(limit).all()
    return responses


@router.get("/responses/{response_id}", response_model=SurveyResponse)
async def get_response(response_id: int, db: Session = Depends(get_db)):
    """Obtém uma resposta específica por ID"""
    response = db.query(SurveyResponse).filter(SurveyResponse.id == response_id).first()
    
    if not response:
        raise HTTPException(status_code=404, detail="Resposta não encontrada")
    
    return response


@router.get("/surveys/{survey_id}/responses", response_model=List[SurveyResponse])
async def get_survey_responses(
    survey_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Lista todas as respostas de uma pesquisa específica"""
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    
    if not survey:
        raise HTTPException(status_code=404, detail="Pesquisa não encontrada")
    
    responses = db.query(SurveyResponse).filter(
        SurveyResponse.survey_id == survey_id
    ).offset(skip).limit(limit).all()
    
    return responses


@router.delete("/responses/{response_id}")
async def delete_response(response_id: int, db: Session = Depends(get_db)):
    """Remove uma resposta"""
    response = db.query(SurveyResponse).filter(SurveyResponse.id == response_id).first()
    
    if not response:
        raise HTTPException(status_code=404, detail="Resposta não encontrada")
    
    db.delete(response)
    db.commit()
    
    return {"message": "Resposta removida com sucesso"}
