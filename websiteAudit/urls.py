"""
URL configuration for websiteAudit project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
# This docstring provides guidance on how to configure URLs in a Django project. It explains how to define URL patterns using function views, class-based views, and how to include other URL configurations from different apps.

from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
# These lines import necessary modules and functions.
# 'admin' is imported from 'django.contrib' for administrative interface.
# 'path' is imported from 'django.urls' to define URL patterns.

urlpatterns = [
    path('api/', include('api.urls')),
    path('', admin.site.urls),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# print(urlpatterns)
# 'urlpatterns' is a Python list where each element is a call to the 'path' function, defining a specific URL pattern.
# Here, it includes a single pattern for the Django admin interface.
# 'path('admin/', admin.site.urls)' defines a URL pattern for the admin site.
# Any URL that starts with 'admin/' will be directed to Django's admin interface.

