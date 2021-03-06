from mixer.backend.django import mixer
import pytest
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from api.models import ExamSheet, Question, Answer, ExamResult
from api.serializers import *
from  django.urls import reverse
import json
from django.core.exceptions import ObjectDoesNotExist
import copy

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

@pytest.mark.django_db
class TestTeacherExamListSerializer(TestCase):
    
    def setUp(cls):
        super(TestTeacherExamListSerializer, cls).setUp()
        teacher = mixer.blend(User, is_staff=True)
        cls.schoolboy = mixer.blend(User, is_staff=False)
        cls.examsheet = mixer.blend(ExamSheet, author=teacher, available=True)
        mixer.blend(ExamResult, author=cls.schoolboy, exam=cls.examsheet, earned_points=8, points_to_get=10)
        path = reverse('api:examsheet_list')
        request = RequestFactory().get(path)
        cls.serializer = TeacherExamListSerializer(cls.examsheet, context={'request': request})

    @classmethod
    def tearDownClass(cls):
        pass

    def test_exam_sheet_shortcut(self):
        serialized_data = self.serializer.data
        path = reverse('api:exam_edit', kwargs={'pk': self.examsheet.id})
        request = RequestFactory().get(path)

        self.assertEqual(serialized_data['title'], self.examsheet.title)
        self.assertEqual(serialized_data['available'], self.examsheet.available)
        self.assertEqual(serialized_data['version'], self.examsheet.version)
        self.assertEqual(serialized_data['updated'], self.examsheet.updated.strftime('%Y-%m-%d'))
        self.assertEqual(serialized_data['filled'], 1)
        self.assertEqual(serialized_data['passed'], 1)
        self.assertEqual(serialized_data['url'], request.build_absolute_uri())

    def test_exam_pass_rate(self):
        mixer.blend(ExamResult, author=self.schoolboy, exam=self.examsheet, earned_points=5, points_to_get=10)
        serialized_data = self.serializer.data
        self.assertEqual(serialized_data['filled'], 2)
        self.assertEqual(serialized_data['passed'], 1)

@pytest.mark.django_db
class TestTeacherNewExamSheetSerializer(TestCase):
    
    def setUp(cls):
        super(TestTeacherNewExamSheetSerializer, cls).setUp()
        cls.teacher = mixer.blend(User, is_staff=True)
        cls.data = {}
        cls.data['title'] = 'Exam title'

    @classmethod
    def tearDownClass(cls):
        pass

    def test_new_examsheet_save(self):
        serializer = NewExamSheetSerializer(data=self.data, context={'author': self.teacher})
        serializer.is_valid()
        serializer.save()
        newest_examsheet = ExamSheet.objects.last()
        self.assertEqual(newest_examsheet.id, serializer.data['id'])

    def test_empty_data(self):
        del self.data['title']
        serializer = NewExamSheetSerializer(data=self.data, context={'author': self.teacher})
        serializer.is_valid()
        errors = serializer.errors
        self.assertEqual(errors['title'][0], 'This field is required.')

    def test_empty_title(self):
        self.data['title'] = ''
        serializer = NewExamSheetSerializer(data=self.data, context={'author': self.teacher})
        serializer.is_valid()
        errors = serializer.errors
        self.assertEqual(errors['title'][0], 'This field may not be blank.')

    def test_doubled_title(self):
        teacher = mixer.blend(User, is_staff=True)
        examsheet = mixer.blend(ExamSheet, author=teacher)
        self.data['title'] = examsheet.title
        serializer = NewExamSheetSerializer(data=self.data, context={'author': self.teacher})
        serializer.is_valid()
        errors = serializer.errors
        self.assertEqual(errors['title'][0], 'exam sheet with this title already exists.')

@pytest.mark.django_db
class TestTeacherExamSerializer(TestCase):
    
    def setUp(cls):
        super(TestTeacherExamSerializer, cls).setUp()
        cls.teacher = mixer.blend(User, is_staff=True)
        examsheet = mixer.blend(ExamSheet, author=cls.teacher)
        question = mixer.blend(Question, examsheet=examsheet)
        answers = mixer.cycle(2).blend(Answer, question=question, is_correct=False)
        answers[0].is_correct = True
        answers[0].save()
        cls.data = TeacherExamSerializer(examsheet).data

    @classmethod
    def tearDownClass(cls):
        pass

    def test_correct_data_validation(self):
        serializer = TeacherExamEditSerializer(self.data)
        self.assertEqual(serializer.is_valid(), True)

    def test_corrupted_data_validation(self):
        del self.data['title']
        serializer = TeacherExamEditSerializer(self.data)
        serializer.is_valid()
        error = serializer.get_errors()
        self.assertEqual(error['data']['message'], 'Corrupted data.')

    def test_doubled_title_validation(self):
        new_examsheet = mixer.blend(ExamSheet, author=self.teacher)
        self.data['title'] = new_examsheet.title
        serializer = TeacherExamEditSerializer(self.data)
        serializer.is_valid()
        error = serializer.get_errors()
        self.assertEqual(error['data']['message'], 'Exam sheet with this title already exists.')

    def test_corrupted_question_validation(self):
        self.data['questions'][0]['id'] += 1
        serializer = TeacherExamEditSerializer(self.data)
        serializer.is_valid()
        error = serializer.get_errors()
        self.assertEqual(error['data']['message'], 'Question does not correspond to exam sheet.')

    def test_corrupted_answer_validation(self):
        self.data['questions'][0]['answers'][0]['id'] += 1
        serializer = TeacherExamEditSerializer(self.data)
        serializer.is_valid()
        error = serializer.get_errors()
        self.assertEqual(error['data']['message'], 'Answer does not correspond to question.')

    def test_only_one_answer_validation(self):
        self.data['questions'][0]['answers'][0]['delete'] = True
        serializer = TeacherExamEditSerializer(self.data)
        serializer.is_valid()
        error = serializer.get_errors()
        self.assertEqual(error['data']['message'], 'There must be at last two answers for every question.')

    def test_two_correct_answers_validation(self):
        self.data['questions'][0]['answers'][1]['is_correct'] = True
        serializer = TeacherExamEditSerializer(self.data)
        serializer.is_valid()
        error = serializer.get_errors()
        self.assertEqual(error['data']['message'], 'There must be only one correct answer for every question.')

    def test_available_exam_without_questions_validation(self):
        self.data['available'] = True
        del self.data['questions']
        serializer = TeacherExamEditSerializer(self.data)
        serializer.is_valid()
        error = serializer.get_errors()
        self.assertEqual(error['data']['message'], 'Active exam has to have at lest one question.')
    
    def test_save_valid_data(self):
        serializer = TeacherExamEditSerializer(self.data)
        serializer.save()       

    def test_delete_question(self):
        self.data['questions'][0]['delete'] = True
        serializer = TeacherExamEditSerializer(self.data)
        serializer.save()
        self.assertEqual(Question.objects.all().exists(), False)

    def test_add_new_question(self):
        new_question = copy.deepcopy(self.data['questions'][0])
        del new_question['id']
        del new_question['answers'][0]['id']
        del new_question['answers'][1]['id']
        self.data['questions'].append(new_question)
        serializer = TeacherExamEditSerializer(self.data)
        serializer.save()
        self.assertEqual(Question.objects.all().count(), 2)
        self.assertEqual(Answer.objects.all().count(), 4)

    def test_delete_answer(self):
        self.data['questions'][0]['answers'][0]['delete'] = True
        self.data['questions'][0]['answers'].append({'is_correct': True, 'text': 'string'})
        serializer = TeacherExamEditSerializer(self.data)
        serializer.save()
        self.assertEqual(Answer.objects.all().count(), 2)
