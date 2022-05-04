from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import Model
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager


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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Course(models.Model):
    name = models.CharField(max_length=100)
    credits = models.IntegerField()

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.name or ''


class News(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_date = models.DateField(auto_now=True)
    image = models.ImageField(upload_to='media/images/news', null=True)
    file = models.FileField(upload_to='media//files/news', null=True)

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'

    def __str__(self):
        return self.title or ''


class Student(CustomUser):
    is_student = models.BooleanField(default=True)

    class Meta:
        # proxy = True
        ordering = ('first_name',)

    def __str__(self):
        return f'{self.last_name} {self.first_name}' or ''


class Tutor(CustomUser):
    is_tutor = models.BooleanField(default=False)

    class Meta:
        # proxy = True
        ordering = ('first_name',)

    def __str__(self):
        return f'{self.last_name} {self.first_name}' or ''


class CourseSchedule(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='tutors')
    begin = models.DateTimeField()
    end = models.DateTimeField()

    class Meta:
        verbose_name = 'Course Schedule'
        verbose_name_plural = 'Course Schedules'

    def __str__(self):
        return self.course.__str__() or ''


class Schedule(models.Model):
    course_schedule = models.ForeignKey(CourseSchedule, on_delete=models.CASCADE, null=True)
    student = models.ForeignKey(Student, related_name='students', on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name = 'Schedule'
        verbose_name_plural = 'Schedules'

    def __str__(self):
        return self.course_schedule.__str__() or ''
