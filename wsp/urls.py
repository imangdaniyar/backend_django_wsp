"""wsp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework import permissions
from drf_yasg.views import get_schema_view  # new
from drf_yasg import openapi  # new

schema_view = get_schema_view(  # new
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    # url=f'{settings.APP_URL}/api/v3/',
    patterns=[path('api/', include('app.urls')), ],
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
                  path(  # new
                      'swagger-ui/',
                      TemplateView.as_view(
                          template_name='swaggerui/swaggerui.html',
                          extra_context={'schema_url': 'openapi-schema'}
                      ),
                      name='swagger-ui'),
                  re_path(  # new
                      r'^swagger(?P<format>\.json|\.yaml)$',
                      schema_view.without_ui(cache_timeout=0),
                      name='schema-json'),
                  path('api/', include('app.urls')),
                  path('admin/', admin.site.urls),
              ] + static(settings.MEDIA_URL,
                         document_root=settings.MEDIA_ROOT)
