from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .models import ExamSheet
from .serializers import SchoolboyExamListSerializer
from rest_framework.renderers import JSONRenderer

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
    pass