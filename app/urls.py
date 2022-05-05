from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from .views import *

router = DefaultRouter()
router.register(r'news', NewsViewSet, basename='news')
# router.register(r'course', CourseViewSet, basename='course')
router.register(r'schedule', ScheduleViewSet, basename='schedule')
router.register(r'course_schedule', CourseScheduleViewSet, basename='course_schedule')
router.register(r'tutor', TutorViewSet, basename='tutor')
router.register(r'student', StudentViewSet, basename='student')
urlpatterns = router.urls

urlpatterns += [
    # JWT
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),

    # API Views
    path('course_files/', CourseFilesView.as_view(), name='course_files'),
    path('specialities/', SpecialityView.as_view(), name='specialities'),
    path('courses/', CourseView.as_view(), name='courses'),
    path('faculties/', FacultyView.as_view(), name='faculties'),

    # FBV Views
    path('positions/', get_positions, name='positions'),

]
# urlpatterns += staticfiles_urlpatterns
