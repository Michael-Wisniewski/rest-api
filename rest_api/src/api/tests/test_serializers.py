from mixer.backend.django import mixer
import pytest
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from api.models import ExamSheet, Question, Answer
from api.serializers import *
from  django.urls import reverse

@pytest.mark.django_db
class TestSchoolboyExamListSerializer(TestCase):

    def setUp(cls):
        super(TestSchoolboyExamListSerializer, cls).setUp()
        cls.teacher = mixer.blend(User, is_staff=True)
        cls.examsheet = mixer.blend(ExamSheet, author=cls.teacher, available=True)
        question = mixer.blend(Question, examsheet=cls.examsheet)
        answers = mixer.cycle(2).blend(Answer, question=question)
        path = reverse('api:new_exam', kwargs={'pk': cls.examsheet.id})
        cls.request = RequestFactory().get(path)
        cls.serializer = SchoolboyExamListSerializer(cls.examsheet, context={'request': cls.request})
    
    @classmethod
    def tearDownClass(cls):
        pass

    def test_exam_sheet_shortcut(self):
        serialized_data = self.serializer.data
        fullname = self.teacher.first_name + ' ' + self.teacher.last_name 
        self.assertEqual(serialized_data['title'], self.examsheet.title)
        self.assertEqual(serialized_data['author'], fullname)
        self.assertEqual(serialized_data['url'], self.request.build_absolute_uri())
    
    def test_exam_sheet_with_unknown_author(self):
        self.teacher.first_name = ''
        self.teacher.last_name = ''
        self.teacher.save()
        serialized_data = self.serializer.data
        self.assertEqual(serialized_data['author'], 'Unknown author')

    def test_exam_sheet_easy_difficulty(self):
        serialized_data = self.serializer.data
        self.assertEqual(serialized_data['difficulty'], 'Easy')

    def test_exam_sheet_medium_difficulty(self):
        mixer.cycle(5).blend(Question, examsheet=self.examsheet)
        serialized_data = self.serializer.data
        self.assertEqual(serialized_data['difficulty'], 'Medium')

    def test_exam_sheet_hard_difficulty(self):
        mixer.cycle(10).blend(Question, examsheet=self.examsheet)
        serialized_data = self.serializer.data
        self.assertEqual(serialized_data['difficulty'], 'Hard')

@pytest.mark.django_db
class TestExamResultSerializer(TestCase):

    def setUp(cls):
        super(TestExamResultSerializer, cls).setUp()
        cls.schoolboy = mixer.blend(User, is_staff=False)
        teacher = mixer.blend(User, is_staff=True)
        cls.examsheet = mixer.blend(ExamSheet, author=teacher, available=True)
        question = mixer.blend(Question, examsheet=cls.examsheet)
        answers = mixer.cycle(2).blend(Answer, question=question)
        answers[0].is_correct = True
        answers[0].save()
        cls.data = {}
        cls.data['id'] = cls.examsheet.id
        cls.data['version'] = cls.examsheet.version
        cls.data['answers'] = [answers[0].id]
        
    @classmethod
    def tearDownClass(cls):
        pass
    
    def test_corrupted_data(self):
        self.data['extra_param'] = ''
        serializer = ExamResultSerializer(self.schoolboy, **self.data)
        serializer.is_valid()
        error = serializer.get_errors()
        self.assertEqual(error['data']['message'], 'Corrupted data.')
    
    def test_exam_out_of_date(self):
        self.data['version'] -= 1
        serializer = ExamResultSerializer(self.schoolboy, **self.data)
        serializer.is_valid()
        error = serializer.get_errors()        
        self.assertEqual(error['data']['message'], 'Used exam sheet is out of date.')

    def test_exam_not_available(self):
        self.examsheet.available = False
        self.examsheet.version -= 1
        self.examsheet.save()
        serializer = ExamResultSerializer(self.schoolboy, **self.data)
        serializer.is_valid()
        error = serializer.get_errors()
        self.assertEqual(error['data']['message'], 'Used exam sheet is no loger available.')

    def test_exam_was_deleted(self):
        self.examsheet.deleted = True
        self.examsheet.version -= 1
        self.examsheet.save()
        serializer = ExamResultSerializer(self.schoolboy, **self.data)
        serializer.is_valid()
        error = serializer.get_errors()
        self.assertEqual(error['data']['message'], 'Used exam sheet was deleted.')

    def test_to_many_answers(self):
        Answer.objects.first().delete()
        serializer = ExamResultSerializer(self.schoolboy, **self.data)
        serializer.is_valid()
        error = serializer.get_errors()
        self.assertEqual(error['data']['message'], 'Wrong number of answers or answers do not correspond to questions.')

    def test_exam_does_not_exists(self):
        self.data['id'] += 1
        serializer = ExamResultSerializer(self.schoolboy, **self.data)
        serializer.is_valid()
        error = serializer.get_errors()        
        self.assertEqual(error['data']['message'], 'The exam sheet does not exist.')

    def test_save(self):
        serializer = ExamResultSerializer(self.schoolboy, **self.data)
        serializer.is_valid()
        user = User.objects.create(is_staff=False)
        response = serializer.save()        
        self.assertEqual(response['data']['message'], 'Your score is: 100%')
