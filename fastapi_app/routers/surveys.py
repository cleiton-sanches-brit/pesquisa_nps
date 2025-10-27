from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Survey, Question, Choice
from schemas import Survey, SurveyCreate, Question, QuestionCreate

router = APIRouter()


@router.get("/surveys", response_model=List[Survey])
async def get_surveys(
    is_active: Optional[bool] = Query(None, description="Filtrar por status ativo"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Lista todas as pesquisas disponíveis"""
    query = db.query(Survey)
    
    if is_active is not None:
        query = query.filter(Survey.is_active == is_active)
    
    surveys = query.offset(skip).limit(limit).all()
    return surveys


@router.get("/surveys/{survey_id}", response_model=Survey)
async def get_survey(survey_id: int, db: Session = Depends(get_db)):
    """Obtém uma pesquisa específica por ID"""
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    
    if not survey:
        raise HTTPException(status_code=404, detail="Pesquisa não encontrada")
    
    return survey


@router.post("/surveys", response_model=Survey)
async def create_survey(survey: SurveyCreate, db: Session = Depends(get_db)):
    """Cria uma nova pesquisa"""
    # Criar a pesquisa
    db_survey = Survey(
        title=survey.title,
        description=survey.description,
        is_active=survey.is_active
    )
    db.add(db_survey)
    db.commit()
    db.refresh(db_survey)
    
    # Criar as perguntas
    for question_data in survey.questions:
        db_question = Question(
            survey_id=db_survey.id,
            question_text=question_data.question_text,
            question_type=question_data.question_type,
            is_required=question_data.is_required,
            order=question_data.order
        )
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        
        # Criar as opções se existirem
        for choice_data in question_data.choices:
            db_choice = Choice(
                question_id=db_question.id,
                choice_text=choice_data.choice_text,
                value=choice_data.value,
                order=choice_data.order
            )
            db.add(db_choice)
    
    db.commit()
    db.refresh(db_survey)
    return db_survey


@router.put("/surveys/{survey_id}", response_model=Survey)
async def update_survey(
    survey_id: int, 
    survey: SurveyCreate, 
    db: Session = Depends(get_db)
):
    """Atualiza uma pesquisa existente"""
    db_survey = db.query(Survey).filter(Survey.id == survey_id).first()
    
    if not db_survey:
        raise HTTPException(status_code=404, detail="Pesquisa não encontrada")
    
    # Atualizar dados da pesquisa
    db_survey.title = survey.title
    db_survey.description = survey.description
    db_survey.is_active = survey.is_active
    
    # Remover perguntas antigas
    db.query(Question).filter(Question.survey_id == survey_id).delete()
    
    # Criar novas perguntas
    for question_data in survey.questions:
        db_question = Question(
            survey_id=survey_id,
            question_text=question_data.question_text,
            question_type=question_data.question_type,
            is_required=question_data.is_required,
            order=question_data.order
        )
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        
        # Criar as opções
        for choice_data in question_data.choices:
            db_choice = Choice(
                question_id=db_question.id,
                choice_text=choice_data.choice_text,
                value=choice_data.value,
                order=choice_data.order
            )
            db.add(db_choice)
    
    db.commit()
    db.refresh(db_survey)
    return db_survey


@router.delete("/surveys/{survey_id}")
async def delete_survey(survey_id: int, db: Session = Depends(get_db)):
    """Remove uma pesquisa"""
    db_survey = db.query(Survey).filter(Survey.id == survey_id).first()
    
    if not db_survey:
        raise HTTPException(status_code=404, detail="Pesquisa não encontrada")
    
    db.delete(db_survey)
    db.commit()
    
    return {"message": "Pesquisa removida com sucesso"}
