from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .models import ExamSheet
from .serializers import SchoolboyExamListSerializer, SchoolboyExamSerializer
from rest_framework.renderers import JSONRenderer
from .validators import SchoolboyExamSheetValidator
from rest_framework.response import Response

class SchoolboyExamListView(ListAPIView):
    queryset = ExamSheet.availables.all()
    serializer_class = SchoolboyExamListSerializer
    renderer_classes = [JSONRenderer]
    
    def list(self, request, *args, **kwargs):
        if not self.get_queryset().exists():
            return Response({'message': 'There are no exam sheets avalible at this moment.'}, status=204)
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

    def post(self,request):
        exam_result_serializer = ExamResultSerializer(**request.data, request.user)

        if  exam_result_serializer.is_valid():
            return Response(**exam_result_serializer.save())
        else:
            return Response(**exam_result_serializer.get_errors())
