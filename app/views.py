import logging

from django.http import JsonResponse
from django.template.defaulttags import csrf_token
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ViewSet

from .models import *
from .serializers import *

logger = logging.getLogger(__name__)


#
# class CourseViewSet(ModelViewSet):
#     queryset = Course.objects.all()
#     serializer_class = CourseSerializer


class NewsViewSet(ViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def list(self, request):
        queryset = News.objects.all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = News.objects.all()
        news = get_object_or_404(queryset, pk=pk)
        serializer = self.serializer_class(news)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = News.objects.get_or_none(id=pk)
        if instance:
            serializer = self.serializer_class(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, pk, *args, **kwargs)

    def destroy(self, request, pk=None, *args, **kwargs):
        instance = News.objects.get_or_none(id=pk)
        if instance:
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ScheduleViewSet(ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    def create(self, request, *args, **kwargs):
        serializer = ScheduleCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = Schedule.objects.get_retake_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class CourseScheduleViewSet(ModelViewSet):
    queryset = CourseSchedule.objects.all()
    serializer_class = CourseScheduleSerializer


class TutorViewSet(ModelViewSet):
    queryset = Tutor.objects.all()
    serializer_class = TutorSerializer


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class CourseFilesView(APIView):
    @permission_classes([IsAuthenticated])
    def post(self, request, *args, **kwargs):
        data = self.request.data
        serializer = CourseFilesSerializer(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            logger.info(f'{request.user} uploaded file')
            return JsonResponse(serializer.data)
        return JsonResponse({'error': "Course File is not valid!"})

    @permission_classes(IsAuthenticated)
    def get(self, request, *args, **kwargs):
        serializer = CourseFilesRetrieveSerializer(CourseFiles.objects.all(), many=True)
        return JsonResponse(serializer.data, safe=False)


class FacultyView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = FacultySerializer(Faculty.objects.all(), many=True)
        return JsonResponse(serializer.data, safe=False)

    @permission_classes([IsAuthenticated])
    def post(self, request, *args, **kwargs):
        data = self.request.data
        serializer = FacultySerializer(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            logger.info(f'{request.user} faculty created')
            return JsonResponse(serializer.data)
        return JsonResponse({'error': "Faculty is not valid!"})


class SpecialityView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = SpecialitySerializer(Speciality.objects.all(), many=True)
        return JsonResponse(serializer.data, safe=False)

    @permission_classes([IsAuthenticated])
    def post(self, request, *args, **kwargs):
        data = self.request.data
        serializer = SpecialitySerializer(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            logger.info(f'{request.user} faculty created')
            return JsonResponse(serializer.data)
        return JsonResponse({'error': "Faculty is not valid!"})


class CourseView(APIView):
    def get(self, request, *args, **kwargs):
        serializer = CourseSerializer(Course.objects.all(), many=True)
        return JsonResponse(serializer.data, safe=False)

    @permission_classes([IsAuthenticated])
    def post(self, request, *args, **kwargs):
        data = self.request.data
        serializer = CourseSerializer(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            logger.info(f'{request.user} course created')
            return JsonResponse(serializer.data)
        return JsonResponse({'error': "Faculty is not valid!"})

@api_view(['GET', 'POST'])
def get_positions(request):
    serializer = PositionSerializer(Position.objects.all(), many=True)
    if request.method == 'GET':
        return JsonResponse(serializer.data, safe=False)
    if request.method == 'POST':
        data = request.data
        serializer = PositionCreateSerializer(data=data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse({'error': "Position is not valid!"})
