from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Model
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager, BaseManager, NewsManager, CourseScheduleManager, ScheduleManager
from .validators import validate_university_email


class Position(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'

    def __str__(self):
        return self.name.__str__() or ''


class CustomUser(AbstractBaseUser, PermissionsMixin):
    objects = CustomUserManager()

    email = models.EmailField(_('Email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    first_name = models.CharField(max_length=45, null=True)
    last_name = models.CharField(max_length=45, null=True)
    activation_code = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    login_at = models.DateTimeField(null=True)
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Course(models.Model):
    objects = BaseManager()

    name = models.CharField(max_length=100)
    credits = models.IntegerField(default=3)

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.name or ''


class News(models.Model):
    objects = NewsManager()

    title = models.CharField(max_length=255)
    content = models.TextField()
    created_date = models.DateField(auto_now=True)
    image = models.ImageField(upload_to='media/news/images', null=True)
    file = models.FileField(upload_to='media/news/files', null=True)

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'

    def __str__(self):
        return self.title or ''


class Faculty(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Faculty'
        verbose_name_plural = 'Faculties'

    def __str__(self):
        return self.name or ''


class Speciality(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Speciality'
        verbose_name_plural = 'Specialities'

    def __str__(self):
        return self.name or ''


class Student(CustomUser):
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE, null=True)
    study_year = models.IntegerField(default=1)

    class Meta:
        # proxy = True
        ordering = ('first_name',)

    def __str__(self):
        return f'{self.last_name} {self.first_name}' or ''


class Tutor(CustomUser):
    class Meta:
        # proxy = True
        ordering = ('first_name',)

    def __str__(self):
        return f'{self.last_name} {self.first_name}' or ''


class CourseSchedule(models.Model):
    objects = CourseScheduleManager()

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='tutors')
    week_day = models.CharField(max_length=10)
    begin = models.TimeField()
    end = models.TimeField()
    semester = models.CharField(max_length=50, default='Fall')

    class Meta:
        verbose_name = 'Course Schedule'
        verbose_name_plural = 'Course Schedules'

    def __str__(self):
        return self.course.__str__() or ''


class CourseFiles(models.Model):
    file = models.FileField(upload_to='media/courses/files/')
    course_schedule = models.ForeignKey(CourseSchedule, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Course File'
        verbose_name_plural = 'Course Files'

    def __str__(self):
        return self.file or ''


class Schedule(models.Model):
    objects = ScheduleManager()

    course_schedule = models.ForeignKey(CourseSchedule, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, related_name='students', on_delete=models.CASCADE, default=1)
    attestation_first = models.IntegerField(default=0)
    attestation_second = models.IntegerField(default=0)
    final_score = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Attestation'
        verbose_name_plural = 'Attestations'

    def __str__(self):
        return self.course_schedule.__str__() or ''

    @property
    def total_score(self):
        return self.attestation_first + self.attestation_second + self.final_score
