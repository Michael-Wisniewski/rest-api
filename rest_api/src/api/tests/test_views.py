from mixer.backend.django import mixer
import pytest
from api.views import *
from django.urls import reverse
from django.test import TestCase, RequestFactory, override_settings
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
        user = mixer.blend(User, is_staff=False)
        factory = RequestFactory()
        cls.request = factory.get(path)
        cls.request.user = user

    @classmethod
    def tearDownClass(cls):
        pass

    def test_get_empty_list(self):
        response = SchoolboyExamListView().as_view()(self.request).render()
        message = json.loads(response.content.decode('utf-8'))
        print(message)
        self.assertEqual(message['message'], 'There are no exam sheets available at this moment.')

    def test_get_examsheet_list(self):
        teacher = mixer.blend(User, is_staff=True)
        mixer.blend(ExamSheet, author=teacher, available=True)
        response = SchoolboyExamListView().as_view()(self.request)
        self.assertEqual(response.status_code, 200)

@pytest.mark.django_db
class TestSchoolboyNewExamView(TestCase):

    def setUp(cls):
        super(TestSchoolboyNewExamView, cls).setUp()
        cls.schoolboy =  mixer.blend(User, is_staff=False)
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
        request.user = self.schoolboy
        response = SchoolboyNewExamView().as_view()(request, pk=self.exam.id)
        self.assertEqual(response.status_code, 200)

    def test_get_invalid_exam(self):
        pk = self.exam.id
        self.exam.delete()
        request = self.factory.get(self.path)
        request.user = self.schoolboy
        response = SchoolboyNewExamView().as_view()(request, pk=pk)
        self.assertEqual(response.status_code, 410)

    def test_post_valid_exam(self):
        json_data = json.dumps(self.data)
        request = self.factory.post(self.path, json_data, content_type='application/json')
        request.user = self.schoolboy
        response = SchoolboyNewExamView().as_view()(request, pk=self.exam.id)
        self.assertEqual(response.status_code, 200)

    def test_post_unvalid_exam(self):
        del self.data['answers']
        json_data = json.dumps(self.data)
        request = self.factory.post(self.path, json_data, content_type='application/json')
        request.user = self.schoolboy
        response = SchoolboyNewExamView().as_view()(request, pk=self.exam.id)
        self.assertEqual(response.status_code, 406)

@pytest.mark.django_db
class TestTeacherExamListView(TestCase):

    def setUp(cls):
        super(TestTeacherExamListView, cls).setUp()
        cls.path = reverse('api:examsheet_list')
        cls.teacher = mixer.blend(User, is_staff=True)
        factory = RequestFactory()
        cls.request = factory.get(cls.path)
        cls.request.user = cls.teacher

    @classmethod
    def tearDownClass(cls):
        pass

    def test_get_empty_list(self):
        response = TeacherExamListView().as_view()(self.request)
        self.assertEqual(response.status_code, 204)

    def test_get_examsheet_list(self):
        mixer.blend(ExamSheet, author=self.teacher)
        response = TeacherExamListView().as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_post_valid_examsheet(self):
        data = {}
        data['title'] = 'Exam title'
        json_data = json.dumps(data)
        factory = RequestFactory()
        request = factory.post(self.path, json_data, content_type='application/json')
        request.user = self.teacher
        response = TeacherExamListView().as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_post_unvalid_examsheet(self):
        factory = RequestFactory()
        request = factory.post(self.path)
        request.user = self.teacher
        response = TeacherExamListView().as_view()(request)
        self.assertEqual(response.status_code, 406)

@pytest.mark.django_db
class TestTeacherExamEditView(TestCase):

    def setUp(cls):
        super(TestTeacherExamEditView, cls).setUp()

        cls.teacher = mixer.blend(User, is_staff=True)
        cls.examsheet = mixer.blend(ExamSheet, author=cls.teacher)
        question = mixer.blend(Question, examsheet=cls.examsheet)
        answers = mixer.cycle(2).blend(Answer, question=question, is_correct=False)
        answers[0].is_correct = True
        answers[0].save()
        cls.data = TeacherExamSerializer(cls.examsheet).data
        cls.path = reverse('api:exam_edit', kwargs={'pk': cls.examsheet.id})
        cls.factory = RequestFactory()
        
    @classmethod
    def tearDownClass(cls):
        pass

    def test_get_exam(self):
        request = self.factory.get(self.path)
        request.user = self.teacher
        response = TeacherExamEditView().as_view()(request, pk=self.examsheet.id)
        self.assertEqual(response.status_code, 200)

    def test_get_deleted_exam(self):
        self.examsheet.delete()
        request = self.factory.get(self.path)
        request.user = self.teacher
        response = TeacherExamEditView().as_view()(request, pk=self.examsheet.id)
        self.assertEqual(response.status_code, 410)

    def test_post_valid_examsheet(self):       
        json_data = json.dumps(self.data)
        request = self.factory.post(self.path, json_data, content_type='application/json')
        request.user = self.teacher
        response = TeacherExamEditView().as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_post_deleted_examsheet(self): 
        self.examsheet.delete()      
        json_data = json.dumps(self.data)
        request = self.factory.post(self.path, json_data, content_type='application/json')
        request.user = self.teacher
        response = TeacherExamEditView().as_view()(request)
        self.assertEqual(response.status_code, 410)

    def test_post_invalid_examsheet(self): 
        del self.data['title']
        json_data = json.dumps(self.data)
        request = self.factory.post(self.path, json_data, content_type='application/json')
        request.user = self.teacher
        response = TeacherExamEditView().as_view()(request)
        self.assertEqual(response.status_code, 406)

    def test_delete_valid_examsheet(self):
        request = self.factory.delete(self.path)
        request.user = self.teacher
        response = TeacherExamEditView().as_view()(request, pk=self.examsheet.id)
        self.assertEqual(response.status_code, 200)

    def test_delete_unvalid_examsheet(self):
        request = self.factory.delete(self.path)
        request.user = self.teacher
        response = TeacherExamEditView().as_view()(request, pk=0)
        self.assertEqual(response.status_code, 404)