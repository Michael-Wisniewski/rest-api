from django.urls import path, include
from .views import SchoolboyExamListView, SchoolboyNewExamView

app_name = 'api'

urlpatterns = [
    path('schoolboy/exam_list/', SchoolboyExamListView.as_view(), name='exam_list'),
    path('schoolboy/new_exam/<int:pk>/', SchoolboyNewExamView.as_view(), name='new_exam')
]