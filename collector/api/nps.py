from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from ..schemas.schemas import (
    NPSSubmitRequest, NPSSubmitResponse, NPSResult, NPSSummary, Response
)
from ..crud.crud import (
    get_customer_by_email, create_customer, get_survey, create_response,
    get_responses_by_survey, get_all_responses, get_nps_responses, calculate_nps_score
)

router = APIRouter()


@router.post("/submit", response_model=NPSSubmitResponse)
async def submit_nps_response(
    request: NPSSubmitRequest,
    http_request: Request,
    db: Session = Depends(get_db)
):
    """
    Endpoint para receber respostas de pesquisas NPS
    """
    # Verificar se a pesquisa existe e está ativa
    survey = get_survey(db, request.survey_id)
    if not survey:
        raise HTTPException(status_code=404, detail="Pesquisa não encontrada")
    
    if not survey.is_active:
        raise HTTPException(status_code=400, detail="Pesquisa não está ativa")
    
    if survey.survey_type != 'nps':
        raise HTTPException(status_code=400, detail="Esta não é uma pesquisa NPS")
    
    # Validar score NPS (0-10)
    if request.score < 0 or request.score > 10:
        raise HTTPException(status_code=400, detail="Score deve estar entre 0 e 10")
    
    # Buscar ou criar cliente
    customer = get_customer_by_email(db, request.customer_email)
    if not customer:
        from ..schemas.schemas import CustomerCreate
        customer_data = CustomerCreate(
            name=request.customer_name,
            email=request.customer_email,
            company=request.customer_company
        )
        customer = create_customer(db, customer_data)
    
    # Verificar se já existe resposta para este cliente nesta pesquisa
    existing_response = db.query(Response).filter(
        Response.customer_id == customer.id,
        Response.survey_id == request.survey_id
    ).first()
    
    if existing_response:
        raise HTTPException(
            status_code=400,
            detail="Já existe uma resposta para este cliente nesta pesquisa"
        )
    
    # Criar resposta
    from ..schemas.schemas import ResponseCreate
    response_data = ResponseCreate(
        customer_name=request.customer_name,
        customer_email=request.customer_email,
        customer_company=request.customer_company,
        survey_id=request.survey_id,
        score=request.score,
        comment=request.comment
    )
    
    response = create_response(db, response_data, customer.id)
    
    # Adicionar informações do request
    response.ip_address = http_request.client.host
    response.user_agent = http_request.headers.get("user-agent", "")
    db.commit()
    
    return NPSSubmitResponse(
        success=True,
        message="Resposta enviada com sucesso",
        response_id=response.id
    )


@router.get("/results", response_model=List[Response])
async def get_nps_results(
    survey_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Lista resultados de pesquisas NPS
    """
    if survey_id:
        responses = get_responses_by_survey(db, survey_id)
    else:
        responses = get_all_responses(db, skip, limit)
    
    return responses


@router.get("/summary", response_model=NPSSummary)
async def get_nps_summary(db: Session = Depends(get_db)):
    """
    Retorna resumo agregado de todas as pesquisas NPS
    """
    # Buscar todas as respostas NPS
    nps_responses = get_nps_responses(db)
    
    if not nps_responses:
        return NPSSummary(
            total_responses=0,
            average_nps=0.0,
            promoters_percentage=0.0,
            passives_percentage=0.0,
            detractors_percentage=0.0,
            surveys=[]
        )
    
    # Calcular estatísticas gerais
    general_stats = calculate_nps_score(nps_responses)
    
    # Agrupar por pesquisa
    surveys_data = {}
    for response in nps_responses:
        survey_id = response.survey_id
        if survey_id not in surveys_data:
            surveys_data[survey_id] = {
                'survey': response.survey,
                'responses': []
            }
        surveys_data[survey_id]['responses'].append(response)
    
    # Calcular estatísticas por pesquisa
    survey_results = []
    for survey_id, data in surveys_data.items():
        survey_stats = calculate_nps_score(data['responses'])
        survey_results.append(NPSResult(
            survey_id=survey_id,
            survey_title=data['survey'].title,
            total_responses=survey_stats['total_responses'],
            average_score=sum(r.score for r in data['responses'] if r.score) / len(data['responses']),
            promoters=survey_stats['promoters'],
            passives=survey_stats['passives'],
            detractors=survey_stats['detractors'],
            nps_score=survey_stats['nps_score']
        ))
    
    # Calcular percentuais
    total = general_stats['total_responses']
    promoters_pct = (general_stats['promoters'] / total * 100) if total > 0 else 0
    passives_pct = (general_stats['passives'] / total * 100) if total > 0 else 0
    detractors_pct = (general_stats['detractors'] / total * 100) if total > 0 else 0
    
    return NPSSummary(
        total_responses=general_stats['total_responses'],
        average_nps=general_stats['nps_score'],
        promoters_percentage=round(promoters_pct, 2),
        passives_percentage=round(passives_pct, 2),
        detractors_percentage=round(detractors_pct, 2),
        surveys=survey_results
    )
