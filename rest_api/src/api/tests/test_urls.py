from django.urls import resolve, reverse
from django.test import TestCase

class TestUrls(TestCase):

    @classmethod
    def tearDownClass(cls):
        pass

    def test_schoobloy_exam_list(self):
        path = reverse('api:exam_list')
        resolved = resolve(path)
        self.assertEqual(resolved.func.__name__, 'SchoolboyExamListView')

    def test_schoobloy_new_exam(self):
        path = reverse('api:new_exam', kwargs={'pk': 1})
        resolved = resolve(path)
        self.assertEqual(resolved.func.__name__, 'SchoolboyNewExamView')