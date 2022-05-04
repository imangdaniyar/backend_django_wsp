from rest_framework import serializers

from .models import *


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"


class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = "__all__"


class CourseScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSchedule
        fields = "__all__"
        depth = 1


class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tutor
        fields = ('email',
                  'first_name',
                  'last_name')


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('email',
                  'first_name',
                  'last_name')
