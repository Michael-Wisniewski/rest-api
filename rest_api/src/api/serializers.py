from rest_framework.serializers import ModelSerializer, SerializerMethodField, DateTimeField
from .models import ExamSheet, Question, Answer, ExamResult
from django.urls import reverse
from jsonschema import validate
from django.core.exceptions import ObjectDoesNotExist
import json

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
                    "id": { "type" : "number" },
                    "version": { "type" : "number" },
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
    
class TeacherExamListSerializer(ModelSerializer):
    url = SerializerMethodField()
    filled = SerializerMethodField()
    passed = SerializerMethodField()
    updated = DateTimeField(format="%Y-%m-%d")

    class Meta:
        model = ExamSheet
        fields = ('title', 'available', 'version', 'updated', 'filled', 'passed', 'url')

    def get_url(self, obj):
        url = self.context['request'].build_absolute_uri(reverse('api:exam_edit', kwargs={'pk': obj.id}))
        return url

    def get_filled(self, obj):
        return obj.filled_exam_sheets.count()

    def get_passed(self, obj):
        count = 0
        for written_exam in obj.filled_exam_sheets.all():
            if written_exam.get_mark > 50:
                count +=1
        return count

class TeacherExamEditSerializer(ModelSerializer):
    _is_valid = False
    _error_msg, _error_code, _data = (None,)*3
    _schema = {
                "type": "object",
                "properties": {
                    "id": { "type": "integer", "minimum": 0 },
                    "title": { "type": "string", "minLength": 1 },
                    "available": { "type": "boolean" },
                    "questions": {
                        "type": "array",
                        "items": [
                            {
                                "type": "object",
                                "properties": {
                                    "id": { "type": "integer", "minimum": 0 },
                                    "text": { "type": "string", "minLength": 1 },
                                    "points": { "type": "integer", "minimum": 1, "maximum": 5 },
                                    "delete": { "type": "boolean" },
                                    "answers": {
                                        "type": "array",
                                        "minItems": 2,
                                        "items": [
                                            {
                                                "type": "object",
                                                "properties": {
                                                    "id": { "type": "integer", "minimum": 0 },
                                                    "is_correct": { "type": "boolean" },
                                                    "text": { "type": "string", "minLength": 1 },
                                                    "delete": { "type": "boolean" }
                                                },
                                                "required": [
                                                    "is_correct",
                                                    "text"
                                                ]
                                            }
                                        ]
                                    }
                                },
                                "required": [
                                    "text",
                                    "points",
                                    "answers"
                                ]
                            }
                        ]
                    }
                },
                "required": [
                    "id",
                    "title",
                    "available"
                ]
            }

    def __init__(self, data):
        self._data = data

    def is_valid(self):
        examsheet = ExamSheet.objects.get(id=self._data['id'])

        try:
            validate(self._data, self._schema)
        except:
            self._error_msg = 'Corrupted data.'
            self._error_code = 406
            return False 

        if ExamSheet.objects.filter(title=self._data['title']).exclude(id=self._data['id']):
            self._error_msg = 'Exam sheet with this title already exists.'
            self._error_code = 406
            return False

        if 'questions' in self._data:
            for question in self._data['questions']:
                updated_answers_ids = []
                valid_answers = 0
                correct_answers = 0

                for answer in question['answers']:
                    if 'id' in answer:
                        updated_answers_ids.append(answer['id'])
                    if not 'delete' in answer:
                        valid_answers +=1
                    if answer['is_correct'] and not 'delete' in answer:
                        correct_answers +=1
                
                if 'id' in question:
                    try:
                        question_object = Question.objects.get(id=question['id'], examsheet=examsheet)
                        existing_answers = question_object.answers.all()
                        
                        if existing_answers.exclude(id__in=updated_answers_ids):
                            self._error_msg = 'Answer does not correspond to question.'
                            self._error_code = 406
                            return False
                    except ObjectDoesNotExist:
                        self._error_msg = 'Question does not correspond to exam sheet.'
                        self._error_code = 406
                        return False

                if valid_answers < 2:
                    self._error_msg = 'There must be at last two answers for every question.'
                    self._error_code = 406
                    return False

                if correct_answers != 1:
                    self._error_msg = 'There must be only one correct answer for every question.'
                    self._error_code = 406
                    return False

        elif self._data['available']:
            self._error_msg = 'Active exam has to have at lest one question.'
            self._error_code = 406
            return False

        return True

    def save(self):
        data = self._data
        examsheet = ExamSheet.objects.get(id=data['id'])
        examsheet.title = data['title']
        examsheet.available = data['available']
        examsheet.save()

        for question in data['questions']:
            if 'delete' in question:
                Question.objects.get(id=question['id']).delete()
            else:

                if 'id' in question:
                    question_object = Question.objects.get(id=question['id'])
                    question_object.text = question['text']
                    question_object.points = question['points']
                    question_object.save()
                else:
                    new_question = Question.objects.create(examsheet=examsheet, text=question['text'], points=question['points'])
                    question['id'] = new_question.id

                for answer in question['answers']:
                    if 'delete' in answer:
                        Answer.objects.get(id=answer['id']).delete()
                    else:
                        if 'id' in answer:
                            answer_object = Answer.objects.get(id=answer['id'])
                            answer_object.text = answer['text']
                            answer_object.is_correct = answer['is_correct']
                            answer_object.save()
                        else:
                            new_answer = Answer.objects.create(question_id=question['id'], text=answer['text'], is_correct=answer['is_correct'])

    def get_errors(self):
        return {'data': {'message': self._error_msg}, 'status': self._error_code}

class NewExamSheetSerializer(ModelSerializer):
    class Meta:
        model = ExamSheet
        fields = '__all__'

    def save(self, **kwargs):
        self._validated_data['version'] = 0
        self.validated_data['author'] = self.context['author']
        super(NewExamSheetSerializer, self).save(**kwargs)

class TeacherAnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'is_correct', 'text']

class TeacherQuestionSerializer(ModelSerializer):
    answers = TeacherAnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'points', 'answers']

class TeacherExamSerializer(ModelSerializer):
    questions = TeacherQuestionSerializer(many=True)

    class Meta:
        model = ExamSheet
        fields = ('id', 'title', 'available', 'version', 'questions')