"""URL configuration for project_name.

Routes the Django admin and the app-level URLconf. See:
https://docs.djangoproject.com/en/3.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_name.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
]
