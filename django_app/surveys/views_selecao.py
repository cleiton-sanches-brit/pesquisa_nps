"""
Views para seleção automática de convidados
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Survey
from .utils_selecao import selecionar_convidados_automatico, criar_convites_automaticos


@login_required
def criar_lista_convidados(request, survey_id):
    """View para criar lista de convidados automaticamente"""
    survey = get_object_or_404(Survey, id=survey_id)
    
    if request.method == 'POST':
        # Executar seleção automática
        resultado = criar_convites_automaticos(survey_id, percentual=1/6)
        
        if resultado['sucesso']:
            messages.success(request, 
                f"Lista de convidados criada com sucesso!\n"
                f"Total de respondentes: {resultado['total_respondentes']}\n"
                f"Elegíveis (não convidados nos últimos 180 dias): {resultado['total_elegiveis']}\n"
                f"Excluídos (já convidados recentemente): {resultado['total_excluidos']}\n"
                f"Emails selecionados (1/6): {resultado['emails_selecionados']}\n"
                f"Convites criados: {resultado['convites_criados']}"
            )
            
            if resultado['convites_ja_existentes'] > 0:
                messages.info(request, 
                    f"{resultado['convites_ja_existentes']} email(s) já possuíam convite para esta pesquisa."
                )
            
            if resultado['erros'] > 0:
                messages.warning(request, 
                    f"{resultado['erros']} erro(s) ao criar convites. Verifique os detalhes."
                )
            
            return redirect('survey_invitations', survey_id=survey.id)
        else:
            messages.error(request, f"Erro ao criar lista: {resultado.get('erro', 'Erro desconhecido')}")
    
    # GET - Mostrar preview da seleção
    resultado_preview = selecionar_convidados_automatico(survey_id, percentual=1/6)
    
    return render(request, 'surveys/criar_lista_convidados.html', {
        'survey': survey,
        'preview': resultado_preview
    })


@login_required
def preview_selecao_convidados(request, survey_id):
    """API para preview da seleção (sem criar convites)"""
    survey = get_object_or_404(Survey, id=survey_id)
    
    resultado = selecionar_convidados_automatico(survey_id, percentual=1/6)
    
    return JsonResponse({
        'sucesso': True,
        'survey': survey.title,
        'total_respondentes': resultado['total_respondentes'],
        'total_elegiveis': resultado['total_elegiveis'],
        'total_excluidos': resultado['total_excluidos'],
        'quantidade_selecionada': resultado['quantidade_selecionada'],
        'percentual': resultado['percentual_usado'],
        'emails_selecionados': resultado['emails_selecionados']
    })




