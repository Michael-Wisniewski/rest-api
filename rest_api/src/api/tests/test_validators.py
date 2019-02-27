import pytest
from api.models import ExamSheet
from django.test import TestCase
from api.validators import SchoolboyExamSheetValidator
from django.contrib.auth.models import User
from django.test import TestCase
from mixer.backend.django import mixer

@pytest.mark.django_db
class TestSchoolboyExamSheetValidator(TestCase):

    def setUp(cls):
        super(TestSchoolboyExamSheetValidator, cls).setUp()
        teacher = mixer.blend(User, is_staff=True)
        cls.examsheet = mixer.blend(ExamSheet, author=teacher, available=True)
        
    @classmethod
    def tearDownClass(cls):
        pass
    
    def test_exam_sheet_is_deleted(self):
        self.examsheet.delete()
        validator = SchoolboyExamSheetValidator(self.examsheet.id)
        response = validator.get_errors()
        self.assertEqual(response['data']['message'], 'This exam is no longer available.')

    def test_exam_sheet_is_unavailable(self):
        self.examsheet.available = False
        self.examsheet.save()
        validator = SchoolboyExamSheetValidator(self.examsheet.id)
        response = validator.get_errors()
        self.assertEqual(response['data']['message'], 'This exam is not available at this moment.')

    def test_exam_sheet_does_not_exist(self):
        validator = SchoolboyExamSheetValidator(0)
        response = validator.get_errors()
        self.assertEqual(response['data']['message'], 'The exam sheet does not exist.')

    def test_exam_sheet_is_valid(self):
        validator = SchoolboyExamSheetValidator(self.examsheet.id)
        response = validator.is_valid()
        self.assertEqual(response, True)

    def test_get_examsheet(self):
        validator = SchoolboyExamSheetValidator(self.examsheet.id)
        examsheet_object = validator.get_examsheet()
        self.assertEqual(examsheet_object, self.examsheet)