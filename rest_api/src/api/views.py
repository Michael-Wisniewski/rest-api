from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .models import ExamSheet
from .serializers import *
from rest_framework.renderers import JSONRenderer
from .validators import SchoolboyExamSheetValidator, TeacherExamSheetValidator
from rest_framework.response import Response

#
from django.contrib.auth.models import User

class SchoolboyExamListView(ListAPIView):
    queryset = ExamSheet.availables.all()
    serializer_class = SchoolboyExamListSerializer
    renderer_classes = [JSONRenderer]
    
    def list(self, request, *args, **kwargs):
        if not self.get_queryset().exists():
            return Response({'message': 'There are no exam sheets available at this moment.'}, status=204)
        else:
            return super(SchoolboyExamListView, self).list(request, *args, **kwargs)

class SchoolboyNewExamView(APIView):
    renderer_classes = [JSONRenderer]
   
    def get(self, request, pk):
        examsheet_validator = SchoolboyExamSheetValidator(pk)
        if examsheet_validator.is_valid():
            examsheet_object = examsheet_validator.get_examsheet()
            exam_serializer = SchoolboyExamSerializer(examsheet_object)
            return Response(exam_serializer.data)
        else:
            return Response(**examsheet_validator.get_errors())

    def post(self,request, *args, **kwargs):
        exam_result_serializer = ExamResultSerializer(request.user, **request.data)
        if  exam_result_serializer.is_valid():
            return Response(**exam_result_serializer.save())
        else:
            return Response(**exam_result_serializer.get_errors())

class TeacherExamListView(ListAPIView):
    queryset = None
    serializer_class = TeacherExamListSerializer
    renderer_classes = [JSONRenderer]

    def list(self, request, *args, **kwargs):
        self.queryset = request.user.exam_sheets.filter(deleted=False)
        if not self.get_queryset().exists():
            return Response({'message': 'You did not add any exam sheets.'}, status=204)
        else:
            return super(TeacherExamListView, self).list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        examsheet_serializer = NewExamSheetSerializer(data=request.data, context={'author': request.user})
        if examsheet_serializer.is_valid():
            examsheet_serializer.save()
            return Response({'message': 'Empty examsheet added.', 'id': examsheet_serializer.data['id']}, status=200)
        else:
            return Response(examsheet_serializer.errors, status=406)

class TeacherExamEditView(APIView):
    renderer_classes = [JSONRenderer]
    
    def get(self, request, pk):
        examsheet_validator = TeacherExamSheetValidator(pk, request.user)
        if  examsheet_validator.is_valid():
            examsheet_object = examsheet_validator.get_examsheet()
            examsheet_serializer = TeacherExamSerializer(examsheet_object)
            return Response(examsheet_serializer.data)
        else:
            return Response(**examsheet_validator.get_errors())

    def post(self, request, *args, **kwargs):

        user=User.objects.get(pk=1)
