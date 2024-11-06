"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
# FLAW: OWASP A04:2021 – Insecure Design; CWE-209 Generation of Error Message Containing Sensitive Information
# (When simply going to the homepage of the app, the user gets an error message that reveals the complete url mapping of the app)
# (This happens mainly because the DEBUG is on True in settings.py)
# FIX: include the homepage in the urls and turn off DEBUG in settings.py

#    path('', include('polls.urls')),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
]