"""
Comando de management para criar lista de convidados automaticamente
Uso: python manage.py criar_lista_convidados <survey_id>
"""
from django.core.management.base import BaseCommand
from surveys.models import Survey
from surveys.utils_selecao import criar_convites_automaticos


class Command(BaseCommand):
    help = 'Cria lista de convidados automaticamente para uma pesquisa (1/6 dos respondentes, excluindo os que receberam convite nos últimos 180 dias)'

    def add_arguments(self, parser):
        parser.add_argument('survey_id', type=int, help='ID da pesquisa')
        parser.add_argument(
            '--percentual',
            type=float,
            default=1/6,
            help='Percentual a selecionar (padrão: 1/6 = 0.1667)'
        )

    def handle(self, *args, **options):
        survey_id = options['survey_id']
        percentual = options['percentual']
        
        try:
            survey = Survey.objects.get(id=survey_id)
        except Survey.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Pesquisa com ID {survey_id} não encontrada'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Criando lista de convidados para: {survey.title}'))
        self.stdout.write(f'Percentual: {percentual * 100:.2f}%')
        self.stdout.write('')
        
        resultado = criar_convites_automaticos(survey_id, percentual)
        
        if resultado['sucesso']:
            self.stdout.write(self.style.SUCCESS('=' * 60))
            self.stdout.write(self.style.SUCCESS('RESULTADO DA SELEÇÃO'))
            self.stdout.write(self.style.SUCCESS('=' * 60))
            self.stdout.write(f"Total de respondentes: {resultado['total_respondentes']}")
            self.stdout.write(f"Elegíveis (não convidados nos últimos 180 dias): {resultado['total_elegiveis']}")
            self.stdout.write(f"Excluídos (já convidados recentemente): {resultado['total_excluidos']}")
            self.stdout.write(f"Emails selecionados: {resultado['emails_selecionados']}")
            self.stdout.write(f"Convites criados: {resultado['convites_criados']}")
            
            if resultado['convites_ja_existentes'] > 0:
                self.stdout.write(self.style.WARNING(f"Convites já existentes: {resultado['convites_ja_existentes']}"))
            
            if resultado['erros'] > 0:
                self.stdout.write(self.style.ERROR(f"Erros: {resultado['erros']}"))
                for erro in resultado['detalhes_erros']:
                    self.stdout.write(self.style.ERROR(f"  - {erro}"))
            
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('✅ Lista de convidados criada com sucesso!'))
            self.stdout.write('')
            self.stdout.write('Próximo passo: Envie os convites pelo Django Admin ou via interface web.')
        else:
            self.stdout.write(self.style.ERROR(f"❌ Erro: {resultado.get('erro', 'Erro desconhecido')}"))




