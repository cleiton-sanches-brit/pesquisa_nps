from django.test import TestCase
from django.contrib.auth.models import User
from .models import Survey, Question, SurveyResponse, Answer


class SurveyModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_survey_creation(self):
        survey = Survey.objects.create(
            title='Test Survey',
            description='A test survey',
            created_by=self.user
        )
        self.assertEqual(survey.title, 'Test Survey')
        self.assertTrue(survey.is_active)
        
    def test_question_creation(self):
        survey = Survey.objects.create(
            title='Test Survey',
            created_by=self.user
        )
        question = Question.objects.create(
            survey=survey,
            question_text='How likely are you to recommend us?',
            question_type='nps'
        )
        self.assertEqual(question.question_text, 'How likely are you to recommend us?')
        self.assertEqual(question.question_type, 'nps')