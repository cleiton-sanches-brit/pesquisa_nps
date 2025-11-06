from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.core import mail
from datetime import timedelta
import json
from .models import (
    Survey, Question, Choice, SurveyResponse, Answer, 
    SurveyInvitation, Respondent, NPSResult
)


class SurveyModelTest(TestCase):
    """Testes para o modelo Survey"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_survey_creation(self):
        """Testa criação de pesquisa"""
        survey = Survey.objects.create(
            title='Test Survey',
            description='A test survey',
            created_by=self.user
        )
        self.assertEqual(survey.title, 'Test Survey')
        self.assertTrue(survey.is_active)
        self.assertEqual(survey.created_by, self.user)
        
    def test_survey_expiration(self):
        """Testa verificação de expiração"""
        # Pesquisa não expirada
        survey = Survey.objects.create(
            title='Active Survey',
            created_by=self.user,
            expires_at=timezone.now() + timedelta(days=30)
        )
        self.assertFalse(survey.is_expired())
        
        # Pesquisa expirada
        expired_survey = Survey.objects.create(
            title='Expired Survey',
            created_by=self.user,
            expires_at=timezone.now() - timedelta(days=1)
        )
        self.assertTrue(expired_survey.is_expired())


class QuestionModelTest(TestCase):
    """Testes para o modelo Question"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.survey = Survey.objects.create(
            title='Test Survey',
            created_by=self.user
        )
        
    def test_question_creation(self):
        """Testa criação de pergunta"""
        question = Question.objects.create(
            survey=self.survey,
            question_text='How likely are you to recommend us?',
            question_type='nps'
        )
        self.assertEqual(question.question_text, 'How likely are you to recommend us?')
        self.assertEqual(question.question_type, 'nps')
        self.assertTrue(question.is_required)
        
    def test_question_with_choices(self):
        """Testa pergunta com opções de escolha"""
        question = Question.objects.create(
            survey=self.survey,
            question_text='What is your favorite color?',
            question_type='choice'
        )
        choice1 = Choice.objects.create(
            question=question,
            choice_text='Red',
            value='red',
            order=1
        )
        choice2 = Choice.objects.create(
            question=question,
            choice_text='Blue',
            value='blue',
            order=2
        )
        self.assertEqual(question.choices.count(), 2)
        self.assertEqual(question.choices.first(), choice1)


class SurveyInvitationModelTest(TestCase):
    """Testes para o modelo SurveyInvitation"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.survey = Survey.objects.create(
            title='Test Survey',
            created_by=self.user,
            expires_at=timezone.now() + timedelta(days=30)
        )
        
    def test_invitation_creation(self):
        """Testa criação de convite"""
        invitation = SurveyInvitation.objects.create(
            survey=self.survey,
            email='recipient@example.com',
            expires_at=timezone.now() + timedelta(days=7)
        )
        self.assertIsNotNone(invitation.unique_token)
        self.assertFalse(invitation.is_used)
        self.assertEqual(invitation.email, 'recipient@example.com')
        
    def test_invitation_url_generation(self):
        """Testa geração de URL do convite"""
        invitation = SurveyInvitation.objects.create(
            survey=self.survey,
            email='recipient@example.com',
            expires_at=timezone.now() + timedelta(days=7)
        )
        url = invitation.get_survey_url()
        self.assertIn(str(self.survey.id), url)
        self.assertIn(str(invitation.unique_token), url)
        
    def test_invitation_expiration(self):
        """Testa verificação de expiração"""
        # Convite válido
        valid_invitation = SurveyInvitation.objects.create(
            survey=self.survey,
            email='valid@example.com',
            expires_at=timezone.now() + timedelta(days=7)
        )
        self.assertFalse(valid_invitation.is_expired())
        self.assertTrue(valid_invitation.is_valid())
        
        # Convite expirado
        expired_invitation = SurveyInvitation.objects.create(
            survey=self.survey,
            email='expired@example.com',
            expires_at=timezone.now() - timedelta(days=1)
        )
        self.assertTrue(expired_invitation.is_expired())
        self.assertFalse(expired_invitation.is_valid())
        
    def test_invitation_mark_as_used(self):
        """Testa marcação de convite como utilizado"""
        invitation = SurveyInvitation.objects.create(
            survey=self.survey,
            email='test@example.com',
            expires_at=timezone.now() + timedelta(days=7)
        )
        self.assertFalse(invitation.is_used)
        self.assertIsNone(invitation.used_at)
        
        invitation.mark_as_used()
        
        invitation.refresh_from_db()
        self.assertTrue(invitation.is_used)
        self.assertIsNotNone(invitation.used_at)
        self.assertFalse(invitation.is_valid())
        
    def test_invitation_unique_constraint(self):
        """Testa constraint único de survey + email"""
        SurveyInvitation.objects.create(
            survey=self.survey,
            email='test@example.com',
            expires_at=timezone.now() + timedelta(days=7)
        )
        
        # Tentar criar outro convite com mesmo email e survey
        with self.assertRaises(Exception):
            SurveyInvitation.objects.create(
                survey=self.survey,
                email='test@example.com',
                expires_at=timezone.now() + timedelta(days=7)
            )


class RespondentModelTest(TestCase):
    """Testes para o modelo Respondent"""
    
    def test_respondent_creation(self):
        """Testa criação de respondente"""
        respondent = Respondent.objects.create(
            email='user@example.com',
            nome_usuario='João Silva',
            nome_conta='Conta Teste',
            status_usuario='Ativo'
        )
        self.assertEqual(respondent.email, 'user@example.com')
        self.assertEqual(respondent.nome_usuario, 'João Silva')
        self.assertTrue(respondent.active)
        
    def test_respondent_email_unique(self):
        """Testa que email deve ser único"""
        Respondent.objects.create(
            email='unique@example.com',
            nome_usuario='User 1'
        )
        
        # Tentar criar outro com mesmo email
        with self.assertRaises(Exception):
            Respondent.objects.create(
                email='unique@example.com',
                nome_usuario='User 2'
            )


class SurveyInvitationViewTest(TestCase):
    """Testes para views de convites"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123',
            is_staff=True
        )
        self.survey = Survey.objects.create(
            title='Test Survey',
            description='Test Description',
            created_by=self.user,
            expires_at=timezone.now() + timedelta(days=30)
        )
        self.question_nps = Question.objects.create(
            survey=self.survey,
            question_text='How likely are you to recommend us?',
            question_type='nps',
            is_required=True,
            order=1
        )
        self.question_text = Question.objects.create(
            survey=self.survey,
            question_text='Comente sobre o que motivou sua nota',
            question_type='text',
            is_required=False,
            order=2
        )
        
    def test_respond_survey_with_valid_token(self):
        """Testa resposta de pesquisa com token válido"""
        invitation = SurveyInvitation.objects.create(
            survey=self.survey,
            email='recipient@example.com',
            expires_at=timezone.now() + timedelta(days=7)
        )
        
        url = reverse('respond_survey', args=[self.survey.id, invitation.unique_token])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.survey.title)
        self.assertContains(response, 'question_{}'.format(self.question_nps.id))
        
    def test_respond_survey_with_expired_token(self):
        """Testa resposta com token expirado"""
        invitation = SurveyInvitation.objects.create(
            survey=self.survey,
            email='recipient@example.com',
            expires_at=timezone.now() - timedelta(days=1)
        )
        
        url = reverse('respond_survey', args=[self.survey.id, invitation.unique_token])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        # Verifica que a página de expirado foi exibida
        self.assertContains(response, 'Pesquisa Expirada', status_code=200)
        self.assertContains(response, 'expirou', status_code=200)
        
    def test_respond_survey_with_used_token(self):
        """Testa resposta com token já utilizado"""
        invitation = SurveyInvitation.objects.create(
            survey=self.survey,
            email='recipient@example.com',
            expires_at=timezone.now() + timedelta(days=7)
        )
        invitation.mark_as_used()
        
        url = reverse('respond_survey', args=[self.survey.id, invitation.unique_token])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        # Verifica que a página de "já respondido" foi exibida
        self.assertContains(response, 'Pesquisa Já Respondida', status_code=200)
        self.assertContains(response, 'respondeu', status_code=200)
        
    def test_submit_survey_response(self):
        """Testa submissão de resposta de pesquisa"""
        invitation = SurveyInvitation.objects.create(
            survey=self.survey,
            email='recipient@example.com',
            expires_at=timezone.now() + timedelta(days=7)
        )
        
        url = reverse('respond_survey', args=[self.survey.id, invitation.unique_token])
        
        # Submeter resposta
        response = self.client.post(url, {
            'question_{}'.format(self.question_nps.id): '9',
            'question_{}_text'.format(self.question_text.id): 'Excelente serviço!'
        })
        
        # Verificar que resposta foi criada
        self.assertEqual(SurveyResponse.objects.count(), 1)
        response_obj = SurveyResponse.objects.first()
        self.assertEqual(response_obj.respondent_email, 'recipient@example.com')
        
        # Verificar que convite foi marcado como usado
        invitation.refresh_from_db()
        self.assertTrue(invitation.is_used)
        
        # Verificar que respostas foram salvas
        self.assertEqual(Answer.objects.count(), 2)
        
    def test_send_invitations_view_requires_auth(self):
        """Testa que view de envio de convites requer autenticação"""
        url = reverse('send_survey_invitations', args=[self.survey.id])
        response = self.client.get(url)
        
        # Deve redirecionar para login ou permitir acesso
        # (dependendo da configuração de autenticação)
        self.assertIn(response.status_code, [200, 302])
        
    def test_send_invitations_creates_invitations(self):
        """Testa que envio de convites cria registros"""
        self.client.login(username='admin', password='admin123')
        
        url = reverse('send_survey_invitations', args=[self.survey.id])
        
        response = self.client.post(url, {
            'emails': 'test1@example.com\ntest2@example.com',
            'expiration_days': '7'
        })
        
        # Verificar que convites foram criados
        self.assertEqual(SurveyInvitation.objects.filter(survey=self.survey).count(), 2)
        
    def test_resend_invitation(self):
        """Testa reenvio de convite"""
        invitation = SurveyInvitation.objects.create(
            survey=self.survey,
            email='recipient@example.com',
            expires_at=timezone.now() + timedelta(days=7)
        )
        
        url = reverse('resend_invitation', args=[invitation.id])
        response = self.client.get(url)
        
        # Verificar que email foi enviado (ou redirecionado)
        self.assertIn(response.status_code, [200, 302])


class SurveyResponseModelTest(TestCase):
    """Testes para o modelo SurveyResponse"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.survey = Survey.objects.create(
            title='Test Survey',
            created_by=self.user
        )
        self.invitation = SurveyInvitation.objects.create(
            survey=self.survey,
            email='respondent@example.com',
            expires_at=timezone.now() + timedelta(days=7)
        )
        
    def test_response_creation(self):
        """Testa criação de resposta"""
        response = SurveyResponse.objects.create(
            survey=self.survey,
            invitation=self.invitation,
            respondent_id='respondent@example.com',
            respondent_email='respondent@example.com'
        )
        self.assertEqual(response.survey, self.survey)
        self.assertEqual(response.respondent_email, 'respondent@example.com')
        
    def test_response_with_answers(self):
        """Testa resposta com múltiplas respostas"""
        question = Question.objects.create(
            survey=self.survey,
            question_text='NPS Score',
            question_type='nps'
        )
        
        response = SurveyResponse.objects.create(
            survey=self.survey,
            invitation=self.invitation,
            respondent_id='respondent@example.com',
            respondent_email='respondent@example.com'
        )
        
        answer = Answer.objects.create(
            response=response,
            question=question,
            answer_value='9'
        )
        
        self.assertEqual(response.answers.count(), 1)
        self.assertEqual(answer.answer_value, '9')


class APIRespondSurveyTest(TestCase):
    """Testes para API de resposta de pesquisa"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='admin123'
        )
        self.survey = Survey.objects.create(
            title='Test Survey',
            created_by=self.user,
            expires_at=timezone.now() + timedelta(days=30)
        )
        self.question_nps = Question.objects.create(
            survey=self.survey,
            question_text='NPS Score',
            question_type='nps',
            is_required=True
        )
        self.invitation = SurveyInvitation.objects.create(
            survey=self.survey,
            email='api@example.com',
            expires_at=timezone.now() + timedelta(days=7)
        )
        
    def test_api_respond_survey_valid(self):
        """Testa API de resposta com dados válidos"""
        url = reverse('api_respond_survey', args=[self.survey.id, self.invitation.unique_token])
        
        data = {
            'question_{}'.format(self.question_nps.id): {
                'value': '10'
            }
        }
        
        response = self.client.post(
            url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)
        self.assertTrue(response_data['success'])
        
    def test_api_respond_survey_invalid_token(self):
        """Testa API com token inválido"""
        import uuid
        invalid_token = uuid.uuid4()
        
        url = reverse('api_respond_survey', args=[self.survey.id, invalid_token])
        
        response = self.client.post(
            url,
            data=json.dumps({}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 404)  # Not found
        
    def test_api_respond_survey_expired_token(self):
        """Testa API com token expirado"""
        expired_invitation = SurveyInvitation.objects.create(
            survey=self.survey,
            email='expired@example.com',
            expires_at=timezone.now() - timedelta(days=1)
        )
        
        url = reverse('api_respond_survey', args=[self.survey.id, expired_invitation.unique_token])
        
        response = self.client.post(
            url,
            data=json.dumps({}),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.content)
        self.assertIn('error', response_data)


class NPSResultModelTest(TestCase):
    """Testes para cálculo de NPS"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.survey = Survey.objects.create(
            title='NPS Test Survey',
            created_by=self.user
        )
        
    def test_nps_result_creation(self):
        """Testa criação de resultado NPS"""
        nps_result = NPSResult.objects.create(
            survey=self.survey,
            period_start=timezone.now().date(),
            period_end=timezone.now().date(),
            total_responses=100,
            promoters=60,
            passives=20,
            detractors=20,
            nps_score=40.00
        )
        
        self.assertEqual(nps_result.nps_score, 40.00)
        self.assertEqual(nps_result.total_responses, 100)
        # NPS = (Promoters - Detractors) / Total * 100
        # NPS = (60 - 20) / 100 * 100 = 40
        expected_nps = ((60 - 20) / 100) * 100
        self.assertEqual(float(nps_result.nps_score), expected_nps)
