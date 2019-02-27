from mixer.backend.django import mixer
import pytest
from api.views import *
from django.urls import reverse
from django.test import TestCase, RequestFactory
import json
from django.contrib.auth.models import User
from api.models import ExamSheet, Question, Answer
from rest_framework import authentication

def diable_session_auth(self, request):
    pass
authentication.SessionAuthentication.enforce_csrf = diable_session_auth

@pytest.mark.django_db
class TestSchoolboyExamListView(TestCase):

    def setUp(cls):
        super(TestSchoolboyExamListView, cls).setUp()
        path = reverse('api:exam_list')
        user = User(is_staff=False)
        factory = RequestFactory()
        cls.request = factory.get(path)
        cls.request.user = user

    @classmethod
    def tearDownClass(cls):
        pass

    def test_get_empty_list(self):
        response = SchoolboyExamListView().as_view()(self.request).render()
        message = json.loads(response.content.decode('utf-8'))
        self.assertEqual(message['message'], 'There are no exam sheets avalible at this moment.')

    def test_get_examsheet_list(self):
        teacher = mixer.blend(User, is_staff=True)
        mixer.blend(ExamSheet, author=teacher, available=True)
        response = SchoolboyExamListView().as_view()(self.request)
        self.assertEqual(response.status_code, 200)

@pytest.mark.django_db
class TestSchoolboyNewExamView(TestCase):

    def setUp(cls):
        super(TestSchoolboyNewExamView, cls).setUp()
        teacher = mixer.blend(User, is_staff=True)
        cls.exam = mixer.blend(ExamSheet, author=teacher, available=True)
        question = mixer.blend(Question, examsheet=cls.exam)
        answer = mixer.blend(Answer, question=question)
        cls.data = {}
        cls.data['id'] = cls.exam.id
        cls.data['version'] = cls.exam.version
        cls.data['answers'] = [answer.id]
        cls.path = reverse('api:new_exam', kwargs={'pk': cls.exam.id})    
        cls.factory = RequestFactory()
    
    @classmethod
    def tearDownClass(cls):
        pass

    def test_get_exam(self):
        request = self.factory.get(self.path)
        response = SchoolboyNewExamView().as_view()(request, pk=self.exam.id).render()
        self.assertEqual(response.status_code, 200)

    def test_get_invalid_exam(self):
        pk = self.exam.id
        self.exam.delete()
        request = self.factory.get(self.path)
        response = SchoolboyNewExamView().as_view()(request, pk=pk)
        self.assertEqual(response.status_code, 410)

    def test_post_valid_exam(self):
        json_data = json.dumps(self.data)
        request = self.factory.post(self.path, json_data, content_type='application/json')
        request.user = mixer.blend(User, is_staff=False)
        response = SchoolboyNewExamView().as_view()(request, pk=self.exam.id).render()
        self.assertEqual(response.status_code, 200)

    def test_post_unvalid_exam(self):
        del self.data['answers']
        json_data = json.dumps(self.data)
        request = self.factory.post(self.path, json_data, content_type='application/json')
        response = SchoolboyNewExamView().as_view()(request, pk=self.exam.id).render()
        self.assertEqual(response.status_code, 406)