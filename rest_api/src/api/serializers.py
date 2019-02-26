from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import ExamSheet, ExamResult
from django.urls import reverse

class SchoolboyExamListSerializer(ModelSerializer):
    author = SerializerMethodField()
    difficulty = SerializerMethodField()
    url = SerializerMethodField()

    def get_author(self, obj):
        author = obj.author
        if author.first_name or author.last_name:
            full_name = author.first_name + ' ' + author.last_name
        else:
            full_name = "Unknown author"
        return full_name

    def get_difficulty(self, obj):
        number_of_questions = obj.questions.count()
        if number_of_questions <= 5:
            difficulty = 'Easy'
        elif number_of_questions <= 10:
            difficulty = 'Medium'
        else:
            difficulty = 'Hard'
        return difficulty

    def get_url(self, obj):
        url = self.context['request'].build_absolute_uri(reverse('api:new_exam', kwargs={'pk': obj.id}))
        return url

    class Meta:
        model = ExamSheet
        fields = ('title', 'author', 'difficulty', 'url')