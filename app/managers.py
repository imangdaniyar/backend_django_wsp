import datetime

from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Manager, Q, F
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class BaseManager(Manager):
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None


class NewsManager(BaseManager):
    def get_today_news(self):
        return self.filter(created_date=datetime.datetime.today())


class CourseScheduleManager(BaseManager):
    def get_fall_semester_courses(self):
        return self.filter(semester='Fall')

    def get_spring_semester_courses(self):
        return self.filter(semester='Spring')


class ScheduleManager(BaseManager):
    def get_retake_queryset(self):
        return self.annotate(attestation_total=F('attestation_first') + F('attestation_second')).filter(
            attestation_total__lt=30)

    def get_fx_queryset(self):
        return self.filter(final_score__lt=20)
