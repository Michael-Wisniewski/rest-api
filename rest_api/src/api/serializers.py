from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import ExamSheet, Question, Answer, ExamResult
from django.urls import reverse
from jsonschema import validate
from django.core.exceptions import ObjectDoesNotExist

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

class SchoolboyAnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text']

class SchoolboyQuestionSerializer(ModelSerializer):
    answers = SchoolboyAnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['text', 'answers']

class SchoolboyExamSerializer(ModelSerializer):
    questions = SchoolboyQuestionSerializer(many=True)

    class Meta:
        model = ExamSheet
        fields = ['id', 'title', 'version', 'questions']

class ExamResultSerializer(object):
    _is_valid = False
    _error_msg, _error_code, _data, _user = (None,)*4
    _schema = {
                "type": "object",
                "properties": {
                    "id": {"type" : "number"},
                    "version": {"type" : "number"},
                    "answers": {
                                    "type": "array",
                                    "items": { "type": "number" }
                                   }
                },
                "required":[
                    "id",
                    "version",
                    "answers"
                ],
                "additionalProperties":False
            }

    def __init__(self, user, **data):
        self._data = data
        self._user = user

    def is_valid(self):
    
        try:
            validate(self._data, self._schema)
        except:
            self._error_msg = 'Corrupted data.'
            self._error_code = 406
            return False 
    
        try:
            examsheet = ExamSheet.objects.get(pk=self._data['id']) 
            
            if examsheet.version != int(self._data['version']):
                self._error_msg = 'Used exam sheet is out of date.'
                self._error_code = 409
                return False
            elif not examsheet.available:
                self._error_msg = 'Used exam sheet is no loger available.'
                self._error_code = 410
                return False
            elif examsheet.deleted:
                self._error_msg = 'Used exam sheet was deleted.'
                self._error_code = 410
                return False
            else:
                questions_to_answer = examsheet.questions

                if questions_to_answer.count() != len(self._data['answers']) or\
                   questions_to_answer.exclude(answers__id__in=self._data['answers']).count():
                    
                    self._error_msg = 'Wrong number of answers or answers do not correspond to questions.'
                    self._error_code = 406
                    return False   
                else:
                    return True

        except ObjectDoesNotExist:
            self._error_msg = 'The exam sheet does not exist.'
            self._error_code = 406
            return False

    def get_errors(self):
        return {'data': {'message': self._error_msg}, 'status': self._error_code}

    def save(self):
        earned_points, points_to_get = (0,)*2
        examsheet = ExamSheet.objects.get(pk=self._data['id'])

        questions_to_answer = examsheet.questions.all()

        for question_to_answer in questions_to_answer.all():
            points_to_get += question_to_answer.points

            for answer in question_to_answer.answers.all():
                if answer.is_correct and (answer.id in self._data['answers']):
                    earned_points += question_to_answer.points

        exam_result = ExamResult(author=self._user, exam=examsheet, earned_points=earned_points, points_to_get=points_to_get)
        exam_result.save()
        return {'data': {'message': 'Your score is: '+ str(exam_result.get_mark) + '%'}, 'status': 200}
    