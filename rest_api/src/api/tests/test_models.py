from mixer.backend.django import mixer
import pytest
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from api.models import ExamSheet, Question, Answer, ExamResult

@pytest.mark.django_db
class TestModels(TestCase):
    
    def setUp(cls):
        super(TestModels, cls).setUp()
        cls.teacher = mixer.blend(User, is_staff=True)
        cls.schoolboy = mixer.blend(User, is_staff=False)
        cls.examsheet = mixer.blend(ExamSheet, author=cls.teacher, available=True)
        cls.question = mixer.blend(Question, examsheet=cls.examsheet) 
        cls.answer = mixer.blend(Answer, question=cls.question)
        cls.examresult = mixer.blend(ExamResult, author=cls.schoolboy, earned_points=5, points_to_get=10, exam=cls.examsheet)
        cls.examsheets = mixer.cycle(4).blend(ExamSheet, author=cls.teacher, title=mixer.sequence("title_{0}"), available=True)

    @classmethod
    def tearDownClass(cls):
        pass

    # ExamSheet unit tests

    def test_string_representation(self):
        self.assertEqual(str(self.examsheet), self.examsheet.title)

    def test_archiving(self):
        self.examsheet.delete()
        self.assertTrue(self.examsheet.deleted)

    def test_version_nonzero_validator(self):
        with self.assertRaisesMessage(ValidationError, 'Zero value is not allowed.'):
            self.examsheet.version = -1
            self.examsheet.save()

    def test_version_is_incrementig(self):
        version = self.examsheet.version
        self.examsheet.save()
        new_version = self.examsheet.version
        self.assertEqual(new_version - version, 1)

    def test_availables_manager(self):
        count_examsheets = ExamSheet.objects.all().count()
        self.examsheets[0].available = False
        self.examsheets[0].save()
        self.examsheets[1].deleted = True
        self.examsheets[1].save()
        count_examsheets_after = ExamSheet.availables.all().count()
        self.assertEqual(count_examsheets_after, count_examsheets - 2)

    # Question unit tests

    def test_question_string_representation(self):
        self.assertEqual(str(self.question), self.question.text)

    # Answer unit tests

    def test_answer_string_representation(self):
        self.assertEqual(str(self.answer), self.answer.text)

    # Exam unit tests

    def test_get_mark(self):
        self.examresult.points_to_get = 10
        self.examresult.earned_points = 5
        score = self.examresult.get_mark
        self.assertEqual(score, 50)

    def test_zero_score(self):
        self.examresult.points_to_get = 10
        self.examresult.earned_points = 0
        score = self.examresult.get_mark
        self.assertEqual(score, 0)

    def test_earned_points_exceeded(self):
        self.examresult.earned_points = 10
        self.examresult.points_to_get = 5
        with self.assertRaisesMessage(ValidationError, 'The maximum value of earned points has been exceeded.'):
            self.examresult.save()

    # User acces rights

    def test_can_schoolboy_save_exam_sheet(self):
        teacher = self.examsheet.author
        teacher.is_staff = False
        with self.assertRaisesMessage(ValidationError, 'Only teacher cad add or edit exam sheet.'):
            self.examsheet.save()

    def test_can_teacher_save_exam_result(self):
        schoolboy = self.examresult.author
        schoolboy.is_staff = True
        with self.assertRaisesMessage(ValidationError, 'Only schoolboy can write an exam.'):
            self.examresult.save()
        