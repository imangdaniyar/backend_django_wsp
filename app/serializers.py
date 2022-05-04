import datetime

from rest_framework import serializers

from .models import *


class CourseSerializer(serializers.ModelSerializer):
    credits = serializers.IntegerField(validators=[MinValueValidator(0),
                                                   MaxValueValidator(7)])

    class Meta:
        model = Course
        fields = "__all__"


class CourseRetrieveSerializer(serializers.Serializer):
    name = serializers.CharField(read_only=True)
    credits = serializers.CharField(read_only=True)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

    def validate(self, data):
        email = data.get('email')
        if email is None or "@kbtu.kz" not in email.lower():
            raise serializers.ValidationError("A valid KBTU email must be entered in")
        return data


class UserSerializer(CustomUserSerializer):
    class Meta:
        fields = ('id',
                  'first_name',
                  'last_name',
                  'position',
                  'email')


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = "__all__"


class TutorSerializer(UserSerializer):
    class Meta:
        model = Tutor
        fields = ('id',
                  'email',
                  'first_name',
                  'last_name')


class TutorRetrieveSerializer(serializers.Serializer):
    first_name = serializers.CharField(read_only=True)
    last_name = serializers.CharField(read_only=True)


class CourseScheduleSerializer(serializers.ModelSerializer):
    tutor = TutorRetrieveSerializer()
    course = CourseRetrieveSerializer()
    begin = serializers.TimeField(format='%H:%M')
    end = serializers.TimeField(format='%H:%M')

    class Meta:
        model = CourseSchedule
        fields = "__all__"

    def validate(self, data):
        week_days = ['monday',
                     'tuesday',
                     'wednesday',
                     'thursday',
                     'friday',
                     'saturday',
                     'sunday']
        work_day_begin = datetime.time(8, 0)
        work_day_end = datetime.time(20, 0)
        if work_day_begin >= data['begin']:
            raise serializers.ValidationError(u'Begin time must be after 8 AM')
        if work_day_end <= data['end']:
            raise serializers.ValidationError(u'Begin time must be before 8 PM')
        if data['week_day'].lower() not in week_days:
            raise serializers.ValidationError(u'Incorrect week day')
        return data


class CourseScheduleShortSerializer(serializers.Serializer):
    tutor = TutorRetrieveSerializer()
    course = CourseRetrieveSerializer()


class StudentSerializer(UserSerializer):
    study_year = serializers.IntegerField(validators=[MinValueValidator(0),
                                                      MaxValueValidator(5)])

    class Meta:
        model = Student
        fields = ('id',
                  'email',
                  'first_name',
                  'last_name',
                  'speciality',
                  'study_year')


class ScheduleSerializer(serializers.ModelSerializer):
    course_schedule = CourseScheduleSerializer()
    student = StudentSerializer()

    class Meta:
        model = Schedule
        fields = "__all__"


class ScheduleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = "__all__"

    def validate(self, data):
        attestation_first = data.get('attestation_first', 0)
        attestation_second = data.get('attestation_second', 0)
        final_score = data.get('final_score', 0)
        if attestation_first > 30 or attestation_first < 0:
            raise serializers.ValidationError("final_score must be in range 0-30")
        if attestation_second > 30 or attestation_second < 0:
            raise serializers.ValidationError("final_score must be in range 0-30")
        if final_score > 30 or final_score < 0:
            raise serializers.ValidationError("final_score must be in range 0-40")
        return data


class CourseFilesRetrieveSerializer(serializers.Serializer):
    file = serializers.FileField()
    course_schedule = CourseScheduleShortSerializer()


class CourseFilesSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseFiles
        fields = "__all__"
