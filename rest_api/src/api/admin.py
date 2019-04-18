from django.contrib import admin
from .models import ExamSheet, Question, Answer, ExamResult 

admin.site.register(ExamSheet)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(ExamResult)