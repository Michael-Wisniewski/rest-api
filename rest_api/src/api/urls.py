from django.urls import path, include
from .views import SchoolboyExamListView, SchoolboyNewExamView, TeacherExamListView, TeacherExamEditView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = 'api'

urlpatterns = [
    path('schoolboy/exam_list/', SchoolboyExamListView.as_view(), name='exam_list'),
    path('schoolboy/new_exam/<int:pk>/', SchoolboyNewExamView.as_view(), name='new_exam'),
    path('teacher/examsheet_list/', TeacherExamListView.as_view(), name='examsheet_list'),
    path('teacher/exam_edit/<int:pk>/', TeacherExamEditView.as_view(), name='exam_edit'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]