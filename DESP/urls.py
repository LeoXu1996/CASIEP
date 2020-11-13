"""DESP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path
from login import views as login_views
from user import views as user_views
from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('admin', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('logout', login_views.logout,name='logout'),
    path('supervisor', login_views.supervisor,name='supervisor'),
    path('administrator', login_views.administrator,name='administrator'),
    path('user', login_views.user,name='user'),
    path('expert', login_views.expert,name='expert'),
    path('manager', login_views.manager,name='manager'),
    path('captcha', include('captcha.urls')),
    url(r'', include('login.urls')),
    url(r'supervisor', include('supervisor.urls')),
    url(r'administrator',include('administrator.urls')),
    url(r'user', include('user.urls')),
    url(r'visualization', include('visualization.urls'))

]
